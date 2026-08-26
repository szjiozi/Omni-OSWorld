# OSWorld Annotation Portal deployment

This directory contains the AWS control-plane draft for the four-annotator
pilot. Deployment is intentionally separate from implementation because it
creates billable resources.

## Architecture

```text
annotator browser
  -> CloudFront default HTTPS domain
  -> CloudFront VPC Origin
  -> gateway EC2 private address:8080
  -> private worker EC2:5000/5910 (maximum four)

gateway -> t4g.nano NAT instance -> public AWS APIs
        -> Cognito (fixed users, no sign-up)
        -> DynamoDB (sessions, assignments, locks)
        -> private S3 (completed bundles)
```

The gateway is the only noVNC proxy and has no public IP. CloudFront reaches it
through a VPC Origin in a dedicated private `/24`. A `t4g.nano` NAT instance in
an existing public subnet gives the gateway outbound access without the fixed
cost of a managed NAT Gateway or several interface endpoints. Port 8080 is
limited to the AWS-managed CloudFront origin-facing prefix list. Worker
security groups accept ports 5000 and 5910 only from the gateway security group
and never from annotator public IPs. CloudFront forwards cookies, query strings,
and WebSocket headers with caching disabled.

## Prerequisites

- Region `ap-east-1` is enabled for the account.
- A VPC with DNS hostnames and an internet gateway.
- A subnet with automatic public IPv4 assignment and an internet-gateway
  default route for the small NAT instance.
- One unused `/24` inside the VPC. The deployment script selects it without
  overlapping existing subnets; override with `--gateway-private-subnet-cidr`
  if the VPC has non-obvious future allocations.
- A worker subnet reachable from the gateway.
- The current Canonical Ubuntu 24.04 AMI ID. The deployment script resolves it
  from Canonical's public SSM parameter and self-bootstraps the gateway.
- The existing private encrypted OSWorld Ubuntu worker AMI.
- The regional managed prefix list ID for
  `com.amazonaws.global.cloudfront.origin-facing`.

Do not bake `.env`, `secret_keys.sh`, AWS credentials, Cognito passwords, or
annotation results into the gateway AMI.

## One-command deployment

The script creates the non-compute control plane first, uploads a deterministic
source archive to the new private S3 bucket, and only then creates the gateway
and CloudFront distribution. It never packages `.git`, results, credentials,
`secret_keys.sh`, or the rest of the repository.

```bash
source secret_keys.sh
conda run -n osworld-aws-dev python \
  scripts/python/deploy_annotation_portal.py \
  --profile osworld-dev \
  --region ap-east-1 \
  --allow-pending
```

`--allow-pending` is for the current engineering pilot only. Remove it after
the corresponding review decisions are approved. On the first deployment the
four Cognito accounts are created and their temporary passwords are written to
the git-ignored file:

```text
evaluation_examples/expert_skill_learning/annotation_portal/credentials.generated.json
```

The file is created with mode `0600` and is never overwritten. Distribute each
credential privately. Users must set a permanent password on first login.

The deployment is idempotent: a changed source bundle receives a content-hash
S3 key, then the deployer verifies and refreshes the running gateway through
SSM. The retained private S3 bucket remains the source of completed annotation
bundles. The gateway role intentionally includes the minimum SSM agent channel
permissions so operators can diagnose the private instance without SSH or a
public IP. A source deployment atomically acquires a DynamoDB maintenance lock
only when the active workspace count is zero. New launches are rejected while
that lock is live; the lock is released after deployment and has a 30-minute
TTL as an abnormal-exit fallback.

Do not use the source deployer to add ordinary annotation tasks. It restarts the
gateway and is reserved for application/infra changes.

## Publish more tasks without interrupting annotation

Task batches are immutable pilot snapshots. The publisher validates the local
catalog, uploads a content-addressed archive to private S3, installs it at
`/opt/osworld/published-pilots/<sha256>/pilot`, and atomically switches the
gateway's `live-pilot` symlink. The running service reloads the catalog on the
next request. A workspace freezes its catalog version and absolute task config
path at launch, so a batch switch does not alter an already provisioning,
recording, or finalizing workspace.

```bash
source secret_keys.sh
conda run -n osworld-aws-dev python \
  scripts/python/publish_annotation_batch.py \
  --profile osworld-dev \
  --region ap-east-1 \
  --assignments \
    evaluation_examples/expert_skill_learning/annotation_portal/assignments.example.json \
  --allow-pending
```

Remove `--allow-pending` for approved production batches. Assignment writes are
upserts: existing assignments and active workspaces are not removed. The
publisher does not restart systemd or any worker.

The full Calc dataset uses a round-oriented construction layout rather than the
old pilot layout. The publisher normalizes it only inside a temporary directory,
then publishes the immutable snapshot. Round 1 is distributed round-robin across
the four fixed accounts, five tasks each. `--replace-assignments` deletes stale
assignments for those four usernames before writing the new set; historical
workspace/submission records are not deleted:

```bash
PYTHONPATH=. conda run -n osworld-aws-dev python \
  scripts/python/publish_annotation_batch.py \
  --profile osworld-dev \
  --region ap-east-1 \
  --dataset-root evaluation_examples/expert_skill_learning/calc_full_v1 \
  --dataset-round round_01 \
  --assignments evaluation_examples/expert_skill_learning/annotation_portal/assignments.example.json \
  --replace-assignments \
  --allow-pending
```

Each task review is persisted in DynamoDB under the immutable catalog version and
task ID. The API representation is the exact six-field `review.json`; the reviewer
field is set from the authenticated username. The task page displays one assigned
task at a time with previous/next navigation and offers both save and download.
The immutable batch is never modified in place. Before running the local review
collector, sync durable online reviews into the dataset packets:

```bash
PYTHONPATH=. conda run -n osworld-aws-dev python \
  scripts/python/sync_annotation_portal_reviews.py \
  --profile osworld-dev --region ap-east-1
```

The sync refuses to replace a different non-empty local review unless
`--overwrite` is explicit.

The annotation result downloader performs this review sync automatically for the
tasks it downloads. It also places the validated six-field Portal review at
`<username>/<task_id>/<run_id>/review.json`, next to the selected recording and
artifact. A different non-empty local packet review remains protected unless
`--overwrite-reviews` is explicit.

Keyboard and pointer overlays are rendered after capture. Their PTS origin is
calibrated from the guest stop monotonic timestamp minus the actual MP4 duration;
the recorder also waits for FFmpeg progress to confirm the first encoded frame
before the Start API returns. This removes variable encoder-startup lag from both
Portal and direct-noVNC annotations. A ready-to-recording UI update must preserve
the existing noVNC iframe so its authenticated VNC connection is not restarted.

The task card renders the published review packet's `TASK.md` as its sole task
instruction source. It must not separately concatenate the package instruction,
operator guide, or skill list, because those can diverge from a human-edited
`TASK.md`. Publishing a new immutable pilot snapshot updates this content without
changing a workspace that has already launched.

Once a worker is ready, the Portal offers three lifecycle controls in addition to
recording. `Fullscreen desktop` applies the browser Fullscreen API to a wrapper around
the existing iframe, so it does not reconnect VNC and can keep an `Exit fullscreen`
control above the desktop. The user can also press Escape. `Close without submitting` is available only
in `ready`; it terminates the worker and transitions the workspace to `terminated`,
releasing both locks without creating a submission. A terminal `failed`, `expired`,
or `terminated` panel offers `Retry workspace`, which performs a normal fresh launch
for the same task. Provisioning is deliberately not cancellable in the pilot: the
controller must finish resolving the concrete worker before cleanup can safely avoid
an orphan EC2 instance.

## Submission history, discard, and local download

Each user can preview only their own submitted `recording.mp4`. The browser
requests an owner-checked same-origin Portal endpoint, and the gateway streams
the private S3 object with HTTP Range/206 support through CloudFront. The UI
does not expose or directly connect to a regional S3 presigned URL, which avoids
annotator proxy failures on a second domain. `Discard this run` tags every object in that run and
changes DynamoDB state to `discarded`; it can be restored for seven days. The
gateway janitor then removes every version under that exact run prefix and marks
the record `deleted`. This retention is implemented by the portal janitor rather
than an age-based S3 lifecycle rule, because S3 object age is not the discard
timestamp.

Administrators should use the verified downloader rather than a raw `aws s3
sync`. It discovers only `COMPLETE.json` runs, skips discarded results by
default, reads the Portal's durable final-video selection, prevents manifest
path traversal, and verifies each file's size and SHA256 before an atomic local
rename:

```bash
source secret_keys.sh
conda run -n osworld-aws-dev python \
  scripts/python/download_annotation_results.py \
  --profile osworld-dev \
  --region ap-east-1 \
  --video-only
```

Default output is `results/reference_annotations/portal/<user>/<task>/<run>/`.
Final-only selection is the default; `--final-only` may be passed explicitly,
while `--all-runs` retrieves every matching complete, non-discarded run. Use
`--username`, `--task-id`, or `--run-id` to narrow the download; omit
`--video-only` to retrieve final XLSX, raw video, event logs, and manifests too.

After CloudFront creates a VPC Origin, AWS creates the service-managed
`CloudFront-VPCOrigins-Service-SG`. The deployer resolves that group and adds a
port-8080 ingress rule to the gateway security group. Do not edit the
service-managed group itself and do not replace this rule with `0.0.0.0/0`.

## Current pilot deployment

The 2026-08-17 Hong Kong deployment passed its public health and access-control
smoke checks:

```text
Portal URL: https://d3iwl4nu2200t4.cloudfront.net/
Region: ap-east-1
Stack: osworld-annotation-portal
Gateway: i-0ae4ef8209ca7ec1b (private, SSM managed)
```

All four fixed users exist and are in the first-login password-change state.
No annotation worker was launched during deployment validation. Temporary
passwords remain only in the git-ignored local `0600` credentials file.

## Cost envelope

At the 2026-08 Hong Kong on-demand rates, the always-on pilot footprint is
approximately **USD 24/month**: one `t3.micro` gateway, one `t4g.nano` NAT
instance, one public IPv4 address, and 48 GiB of gp3 storage. Cognito,
DynamoDB, S3, and CloudFront should remain at or near zero for four annotators
at pilot traffic levels. A live `t3.xlarge` desktop costs about USD 0.24/hour
plus small prorated IPv4 and gp3 charges; its hard TTL is three hours. Portal
workers explicitly use the gp3 baseline of 3,000 IOPS and 125 MiB/s so they do
not incur the repository's higher default performance charges.

## Manual template validation

```bash
aws cloudformation validate-template \
  --profile osworld-dev \
  --region ap-east-1 \
  --template-body file://infra/annotation_portal/template.yaml
```

Use `AllowPending=true` only for the engineering smoke while the four pilot
packages are awaiting human review. Formal annotation must use the default
`false` value.

## Fixed users without the deployment helper

After the stack exists, create the four preselected accounts without email:

```bash
python scripts/python/create_annotation_portal_users.py \
  --profile osworld-dev \
  --region ap-east-1 \
  --user-pool-id <stack-output-user-pool-id> \
  --credentials-output /a/private/path/annotation-temp-passwords.json
```

The output is created with mode `0600` and is refused if it already exists.
Distribute each row privately. There is no registration page and no email
password recovery in this pilot.

## Deployment gates

1. Validate the template.
2. Deploy the stack; no worker is launched until a user requests a task.
3. Verify `/healthz` through the CloudFront URL.
4. Log in with one temporary account and complete the password challenge.
5. Run one pending task end to end and verify the S3 `COMPLETE.json` marker.
6. Confirm the worker is terminated and no EBS/ENI is left behind.
7. Only then test four simultaneous workspace admissions.

The application supports four concurrent users, but real performance still
requires one four-user smoke: keep four noVNC sessions active, then submit at
roughly the same time while observing gateway CPU, memory, swap, network, and
finalization latency. Do not claim that concurrency has no slowdown until this
gate passes. Upgrade the gateway from `t3.micro` to `t3.small` only if that
measurement shows a gateway bottleneck.

The task-packet/history/dynamic-publish changes described above were deployed
on 2026-08-17. Post-deploy checks passed: public health returned 200,
unauthenticated tasks returned 401, the new frontend bundle was visible,
`live-pilot` contained four task packets, the maintenance lock was released,
and both active workspace and live worker counts were zero. The four-user
concurrency smoke remains a separate pending gate.
