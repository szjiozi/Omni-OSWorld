# Expert Skill Reference Task Construction

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

Current scope:

1. extract English app-operation skills with concrete procedures and examples;
2. combine 2–5 same-app skills into non-1:1 reference tasks;
3. let a human review tasks and manually find or create an artifact;
4. launch a setup-only OSWorld environment and record the expert using explicit
   Enter-to-start and Enter-to-stop controls;
5. let a second annotator watch the MP4 locally and optionally relaunch the
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

Do not commit API keys, raw credentials, private user data, or authenticated
browser profiles. Pilot artifacts and recordings may initially be pushed to the
GitHub remote, but they must be checked for sensitive content first.
