# Daytona Provider

OSWorld `--provider_name daytona` runs tasks on [Daytona](https://www.daytona.io/) sandboxes. The provider runs the sandbox AS the desktop (no nested QEMU — /dev/kvm is unavailable in Daytona sandboxes, so the stock xlangai/ubuntu_osworld qcow2 is NOT used). Reset creates the replacement sandbox from the snapshot first, then deletes the old sandbox in the background after the replacement succeeds, which gives each episode a clean desktop.

## Quickstart

```bash
# 1. Install the SDK
pip install daytona

# 2. Get an API key from the Daytona dashboard
export DAYTONA_API_KEY=...

# 3. Build the auditable Office snapshot once
python -m desktop_env.providers.daytona.build_snapshot \
  --name osworld-video-office-v1 \
  --manifest-out results/osworld-video-office-v1.manifest.json

# 4. Use the built snapshot for launches
export DAYTONA_OSWORLD_SNAPSHOT=osworld-video-office-v1

# 5. Smoke test the provider
DAYTONA_API_KEY=... DAYTONA_OSWORLD_SNAPSHOT=... python -m desktop_env.providers.daytona.smoke_test

# 6. Run OSWorld
python quickstart.py --provider_name daytona --headless True
```

Once built, later runs reuse `DAYTONA_OSWORLD_SNAPSHOT`. A reset never reuses a dirty sandbox. It creates the replacement sandbox from the snapshot first; after that succeeds, the provider deletes the old sandbox in the background. This briefly overlaps two sandboxes per environment, which matters near Daytona org quota limits. If DesktopEnv passes the generic reset target `init_state`, the provider substitutes `DAYTONA_OSWORLD_SNAPSHOT`; other snapshot names are used as given.

## How the provider works

Daytona sandboxes are the guest desktop. OSWorld does not boot a VM inside the sandbox, because `/dev/kvm` is not available there. The stock `xlangai/ubuntu_osworld` qcow2 image is therefore not part of this provider path.

Transport is SSH local port-forwarding via `sandbox.create_ssh_access()` (requires `ssh` on PATH). The provider starts local forwards so the normal OSWorld controller can keep using localhost endpoints. Guest ports 5000/9222/6080(noVNC)/8080 are tunneled to localhost.
The guest server runs as root under the distro Python at `/usr/bin/python3`, and writes its log to `/root/osworld-server.log`.

Sandboxes are created with Daytona auto-stop disabled (`auto_stop_interval=0`) so a long agent pause cannot halt a live episode. The leak backstop is Ctrl-C cleanup plus sweeping sandboxes labeled `osworld.managed` / `osworld.alloc`; in the Daytona dashboard or API, filter by those labels and delete stragglers.

## Prerequisites

- `DAYTONA_API_KEY` must be set for the Daytona SDK.
- `ssh` must be installed and available on `PATH`; the provider uses the local binary for port forwarding.
- `DAYTONA_OSWORLD_SNAPSHOT` should point at a snapshot built for OSWorld runs.
- Daytona org tiers 1/2 have whitelist-restricted sandbox egress (tasks needing arbitrary internet need Tier 3+). Package registries and common developer services are usually allowed, but arbitrary task URLs are not.

## Building the snapshot

Build the Office OSWorld snapshot once per Daytona org:

```bash
python -m desktop_env.providers.daytona.build_snapshot \
  --name osworld-video-office-v1 \
  --manifest-out results/osworld-video-office-v1.manifest.json
export DAYTONA_OSWORLD_SNAPSHOT=osworld-video-office-v1
```

The snapshot build installs the OSWorld server, desktop basics, Calc, Impress,
fixed Office fonts, and `xinput` for human trajectory collection. It writes
`/etc/osworld/snapshot-manifest.json` into the snapshot with package versions,
the OSWorld commit, build-script hash, and capabilities. Keep the snapshot name
stable for repeatable runs, or export the new name before running
`quickstart.py`.

## Running

Use the smoke test before a benchmark run:

```bash
DAYTONA_API_KEY=... DAYTONA_OSWORLD_SNAPSHOT=... python -m desktop_env.providers.daytona.smoke_test
```
- `DAYTONA_SMOKE_REQUIRE_A11Y=1` makes the smoke test require `/accessibility` to return HTTP 200.
- `DAYTONA_SMOKE_SKIP_SNAPSHOT=1` skips the snapshot/revert part of the smoke test.

Some Daytona accounts can create snapshots but receive HTTP 403 when deleting
them. For those accounts, use `DAYTONA_SMOKE_SKIP_SNAPSHOT=1` for routine smoke
tests and rely on the immutable-snapshot soak below for replacement-reset
coverage. A full smoke run may leave an `osworld-smoke-*` snapshot that must be
removed in the Daytona Dashboard.

Then run OSWorld with the Daytona provider:

```bash
python quickstart.py --provider_name daytona --headless True
```

The OSWorld server log is written inside the sandbox at `/root/osworld-server.log`.

Before collecting Phase 0 data, run the repeated replacement-reset soak. This
performs ten clean resets without creating temporary snapshots and writes a
machine-readable report:

```bash
python -m desktop_env.providers.daytona.soak_test \
  --iterations 10 \
  --report results/daytona_phase0_soak.json
```

Validate the four Phase 0 Office tasks through the real setup/evaluator path:

```bash
python scripts/python/generate_phase0_fixtures.py
python scripts/python/validate_phase0_tasks.py \
  --daytona \
  --report results/phase0_daytona_tasks.json
```

After the snapshot is built and both required environment variables are set,
the complete smoke, ten-reset soak, and four-task validation can be run with:

```bash
bash scripts/bash/validate_phase0_daytona.sh
```

The one-shot script skips creation of a disposable smoke snapshot; the
following ten-reset soak still verifies repeated restores from the configured
Office snapshot.

## Environment variables

| Variable                         | Required | Default                         | Purpose |
|----------------------------------|----------|---------------------------------|---------|
| `DAYTONA_API_KEY`                | yes      | —                               | API key read directly by the Daytona SDK. |
| `DAYTONA_API_URL`                | no       | `https://app.daytona.io/api`    | API base URL. |
| `DAYTONA_OSWORLD_SNAPSHOT`       | yes\*    | —                               | Snapshot to restore from on each launch and for the generic `init_state` reset target. |
| `DAYTONA_ALLOW_NO_SNAPSHOT`      | no       | unset                           | `1` permits degraded bare-sandbox allocation. Otherwise allocation fails fast when no snapshot is configured. |
| `DAYTONA_SSH_HOST`               | no       | SSH access response             | Override only the gateway host parsed from `create_ssh_access()`. |
| `DAYTONA_SSH_EXPIRES_MIN`        | no       | `1440`                          | SSH access token lifetime in minutes. |
| `DAYTONA_LAUNCH_TIMEOUT_SEC`     | no       | `300`                           | Wait budget for sandbox creation/start. |
| `DAYTONA_READY_TIMEOUT_SEC`      | no       | `300`                           | Wait budget for the in-sandbox server readiness check. |
| `DAYTONA_SNAPSHOT_TIMEOUT_SEC`   | no       | `600`                           | Wait budget for live sandbox snapshot activation. |
| `DAYTONA_SKIP_READY_CHECK`       | no       | —                               | `1` skips the localhost `:5000` readiness probe. |

\* Required for real OSWorld runs unless `DAYTONA_ALLOW_NO_SNAPSHOT=1` is set. Without a configured snapshot and that override, allocation fails fast. The degraded bare sandbox does not contain the OSWorld desktop/server setup.

## Task coverage caveat

The built snapshot carries the OSWorld server, desktop basics, the baked apt
set (including `wmctrl` and `xinput`), fixed Office fonts, and LibreOffice Calc
and Impress. LibreOffice is included because `/accessibility` checks it and
because it is the Phase 0 task target. Other benchmark task apps (GIMP, VLC,
Thunderbird, Chrome/Chromium with profiles…) are not baked into the baseline;
extend `build_snapshot.py`'s apt step for the app set you evaluate.

Do not assume coverage matches the upstream Ubuntu qcow2 image. If a task depends on an application, browser profile, extension, desktop setting, or fixture file, bake that dependency into the Daytona snapshot before using it for evaluation.

## Viewing the desktop

Use the Daytona dashboard: sandbox ⋮ → VNC. You can also use the local noVNC forward for guest port `6080` while the provider is running.

## Troubleshooting

- **Server readiness fails.** Check `/root/osworld-server.log` in the sandbox. If you intentionally want a control-plane-only launch, set `DAYTONA_SKIP_READY_CHECK=1`; do not use that for benchmark runs.
- **X-access failures.** Symptoms include `cannot open display`, `Authorization required`, blank screenshots, or pyautogui errors from `/execute`. Rebuild the snapshot so the desktop session and OSWorld server share the same display, then inspect `/root/osworld-server.log` on the next run.
- **Stale X locks after restore.** Snapshots can carry `/tmp/.X0-lock` or `/tmp/.X11-unix/X0`; the provider clears stale lock files automatically before it starts the desktop.
- **Ctrl-C during startup.** Interrupting bootstrap deletes the in-flight sandbox, so no manual Daytona cleanup is needed.
- **SSH forwarding refusal or dead tunnel.** Confirm `ssh` is on `PATH`, the access token has not expired, and the local forwarded ports are free. By default the gateway host is parsed from the SSH access response; `DAYTONA_SSH_HOST` only overrides that host. Startup failures raise with the `ssh` stderr tail. If a tunnel dies mid-episode, the controllers surface HTTP/connection errors and the episode fails by design.
