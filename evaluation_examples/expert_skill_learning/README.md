# Expert Skill Reference Task Construction

Human reviewers should follow the field-by-field and decision guidance in
[`reviewer.md`](reviewer.md) before editing the pilot review form.
Human experts should follow [`annotator.md`](annotator.md) before launching an
AWS recording session.

This directory contains the version-controlled contracts for the first pilot of
the OSWorld expert-skill benchmark. The pilot uses exactly three
`libreoffice_calc` source tasks from OSWorld-Human.

The construction LLM receives only the original task instruction and indexed
`human-ground-truth.single-action` steps. Local code attaches the trusted task
ID, app name, and action provenance after validating the model response.

The frozen Pilot source selection is recorded in `pilot/source_tasks.json` at
OSWorld-Human commit `deff1a7cd8940f6040a895593097fc3c5511f36b`. The three
tasks cover formula/autofill and cross-sheet references, formula-based
conditional formatting, and Pivot Table field configuration.

The accepted atomic extraction is stored in `pilot/skill_pool.json`, with its
model, prompt hashes, token usage, cost, and developer quality review in
`pilot/extraction_run.json`. It contains 12 independently reusable skills. They
cover 38 source actions without duplicate assignments; two actions that only
type and commit a task-specific header are retained in the source manifest as
scaffolding but are intentionally not promoted to skills.

The original task-only C2 output remains in `pilot/reference_tasks.json` for
provenance. The current package output is `pilot/reference_packages.json`: each
candidate contains an outcome-oriented task instruction, an initial XLSX
artifact specification, a non-binding operator guide, and declared incidental
operations. Its generation metadata is in
`pilot/reference_package_generation_run.json`.

The current round has four pending packages and covers all 12 skills at the
candidate level. `similarity_reference.semantic` is real cosine similarity from
`text-embedding-3-small`; the old sequence similarity is retained as a lexical
audit only. Neither score is an automatic accept/reject threshold. Approved
coverage is computed only from `pilot/reference_package_reviews.json`; the
initial `pilot/coverage_state.json` therefore remains 0/12 approved.
The generator pre-populates one review form per package. A deterministic packet
exporter then gathers each task's instruction, full skill guides, exact source
actions, artifact, previews, task config, and editable review into
`pilot/review_packets/<reference-task-id>/`. Reviewers work one directory at a
time and edit only its `review.json`; untouched forms are treated as pending.
The packet collector validates those forms, merges them into the pipeline's
central `pilot/reference_package_reviews.json`, and recomputes approved coverage.

`pilot/artifact_blueprints.json` and `pilot/artifacts/` contain four generated,
rendered, formula-error-scanned XLSX workbooks. All are synthetic and need no
manual pre-recording setup. One post-generation QC edit is explicitly recorded
in the blueprint document: an enrollment flag was changed so the workbook has
the requested eight Review rows rather than nine.

Current scope:

1. extract English app-operation skills with concrete procedures and examples;
2. combine 2–5 same-app skills into non-1:1 reference tasks;
3. let a human approve, request revision, or reject each package;
4. generate the initial artifact from the approved/pending artifact spec, then
   let a human inspect or replace it when needed;
5. launch a setup-only OSWorld environment and record the expert using explicit
   Enter-to-start and Enter-to-stop controls;
6. let a second annotator watch the MP4 locally and optionally relaunch the
   artifact environment for inspection.

Agent execution, model training, automatic final-state evaluation, and formal
benchmark-scale coverage are not part of this construction phase.

Prompts live in `prompts/*.txt`; JSON contracts live in `schemas/`; token prices
used for cost estimates live in `pricing/`. The price table is dated and must be
updated deliberately rather than silently applying an unknown model price.

The recommended pilot construction model is `gpt-5.6-terra`. The client remains
OpenAI-compatible through configurable `model` and `base_url` values. Current
official prices are recorded from:

- https://developers.openai.com/api/docs/pricing
- https://developers.openai.com/api/docs/models/gpt-5.6-terra
- https://developers.openai.com/api/docs/guides/embeddings#obtaining-the-embeddings

Example extraction command after selecting the three source task IDs:

```bash
conda activate osworld-aws-dev
export OPENAI_API_KEY=<set-outside-the-repository>
python scripts/python/extract_reference_skills.py \
  --source-manifest evaluation_examples/expert_skill_learning/pilot/source_tasks.json
```

The source manifest includes all 40 copied `single_actions` and can run without
an external OSWorld-Human clone. Add `--source-root /path/to/osworld-human` to
verify every copied task against its pinned raw-file SHA256 before extraction.

Generate reference packages with a reproducible seed and semantic audit:

```bash
python scripts/python/generate_reference_packages.py \
  --skill-pool \
    evaluation_examples/expert_skill_learning/pilot/skill_pool.json \
  --source-manifest \
    evaluation_examples/expert_skill_learning/pilot/source_tasks.json \
  --seed 20260805
```

Only sampled skills are mandatory. Limited task-specific, prerequisite, and
repeated operations are allowed when they keep the task natural, and must be
declared separately. The sampler groups 2–5 same-app skills, retries model
rejections, and reports unresolved skills if `--max-attempts` is exhausted.

Render the complete, deterministic construction documents that preserve the old
review-page content:

```bash
python scripts/python/manage_reference_review_packets.py details
```

Each `pilot/task_details/<reference-task-id>/TASK_DETAIL.md` is the exact input
to a separate LLM call that generates a structured Chinese novice guide:

```bash
python scripts/python/generate_reference_reviewer_guides.py
```

The guide output records the TASK_DETAIL SHA256, prompt hash, model, token usage,
and cost in `pilot/reviewer_guides.json`. Finally create or refresh the
self-contained reviewer directories:

```bash
python scripts/python/manage_reference_review_packets.py export
```

The frozen four-guide run used `gpt-5.6-terra`, 12374 input tokens, 7606 output
tokens, and an estimated `$0.116020`. Each guide covers every required skill ID
and is bound to its exact TASK_DETAIL input hash.

Start at `pilot/review_packets/index.md`, open one task's `TASK.md`, inspect the
initial-state preview, launch the environment to inspect the workbook itself,
and fill that directory's standalone `review.json`. `TASK.md` is the concise
reviewer-facing page; `TASK_DETAIL.md` remains in the packet as the complete,
unlinked guide-generation input. The exporter preserves local review edits. If
an already-reviewed task's inputs or Chinese guide change, it refuses to refresh
the stale packet; `--force` explicitly refreshes the packet and resets that local
decision so the changed task must be reviewed again.

After reviewing, validate and collect all per-task forms:

```bash
python scripts/python/manage_reference_review_packets.py collect
```

The collector is the normal write path for the central review file. It verifies
packet input and output hashes, merges reviews in stable package order, writes
`pilot/reference_package_reviews.json`, and updates `pilot/coverage_state.json`.
It can operate on one packet with `--task-id <reference-task-id>`.

The lower-level coverage command remains available for validation or debugging:

```bash
python scripts/python/review_reference_packages.py \
  --skill-pool evaluation_examples/expert_skill_learning/pilot/skill_pool.json \
  --packages evaluation_examples/expert_skill_learning/pilot/reference_packages.json \
  --reviews evaluation_examples/expert_skill_learning/pilot/reference_package_reviews.json \
  --output evaluation_examples/expert_skill_learning/pilot/coverage_state.json
```

Exit code 2 means review is incomplete, not that schema validation failed.
Resume generation only after every previous package has a decision. Rejected
exact combinations are blocked; revision requests regenerate the same sampled
skills with the reviewer instructions; uncovered skills are resampled globally.

Generate new artifact blueprints and XLSX files:

```bash
python scripts/python/generate_reference_artifacts.py \
  --packages evaluation_examples/expert_skill_learning/pilot/reference_packages.json \
  --build-output-dir results/expert_skill_learning/artifacts \
  --node <bundled-node> \
  --node-modules <directory-containing-artifact-tool>
```

Rebuild already frozen blueprints deterministically, without an API call, by
replacing `--packages` with
`--blueprints-input evaluation_examples/expert_skill_learning/pilot/artifact_blueprints.json`.
The builder preserves deliberately incomplete result columns, applies exact
initial number formats and AutoFilter requirements, renders every sheet, and
scans for spreadsheet formula errors.

Generate constrained annotation setup blueprints and inject trusted standard
OSWorld actions:

```bash
conda run -n osworld-aws-dev python \
  scripts/python/generate_reference_task_configs.py
```

The LLM never receives or emits the trusted host artifact path, SHA256, or raw
setup commands. Local code verifies the artifact and writes exactly one
`upload_file` followed by one `open`; reference configs never contain an
evaluator. Frozen Pilot outputs are in
`pilot/annotation_setup_blueprints.json`, `pilot/task_configs/`, and
`pilot/task_config_manifest.json`. The accepted four-call run used 6712 input
tokens and 678 output tokens, with an estimated cost of `$0.021560`.

After a package is approved, launch and record it on AWS:

```bash
python scripts/python/record_reference_task.py \
  --reference-task-id reference-task-r01-001
```

Use `--allow-pending` only for an engineering smoke. The first Enter begins
timestamped XInput/MP4/screenshot collection; the second Enter stops recording,
normalizes privacy-filtered shortcut events, burns a bottom-centered key overlay
into the default `recording.mp4`, preserves `recording_raw.mp4`, saves and
downloads the final XLSX, writes the annotation bundle, and requests instance
termination. See `annotator.md` for the complete preflight and recovery flow.

Do not commit API keys, raw credentials, private user data, or authenticated
browser profiles. Pilot artifacts and recordings may initially be pushed to the
GitHub remote, but they must be checked for sensitive content first.
