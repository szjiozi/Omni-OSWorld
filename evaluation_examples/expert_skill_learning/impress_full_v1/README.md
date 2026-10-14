# LibreOffice Impress full reference-task dataset

This directory applies the expert-skill reference-task construction pipeline to
every LibreOffice Impress task in the pinned OSWorld-Human source revision.

## Frozen source

- Repository: `https://github.com/WukLab/osworld-human`
- Commit: `deff1a7cd8940f6040a895593097fc3c5511f36b`
- Application: `libreoffice_impress`
- Raw source tasks: 47
- Raw single actions: 366
- Raw grouped actions: 188
- Copy policy: byte-for-byte; source JSON files are never rewritten
- Integrity: `source/osworld_human/<commit>/SHA256SUMS`
- Provenance: `source/osworld_human/<commit>/PROVENANCE.json`

The pinned upstream root does not contain a `LICENSE` file. Its README is copied
unchanged beside the vendored app directory so the source's evaluation-only
usage warning remains attached to the data.

## Construction policy

All 47 source tasks enter skill extraction. Reference-task generation combines
2--5 same-app skills and runs in review-gated rounds with at most 20 candidates
per round. Every valid skill must eventually be covered by an approved recorded
reference task or have an explicit waiver. Cross-task skill deduplication is not
performed in this version.

The first engineering pilot remains limited to five static, artifact-producing
candidates. Its files and review state are historical inputs and are not
rewritten by the deferred-skill adapter described below.

## Deferred-skill artifact adapter

`generated_v2/skill_readiness_policy.json` identifies 21 skills from 18 source
tasks that cannot use the static PPTX builder alone. They now have an explicit
adapter path:

1. `deferred_skill_artifact_catalog.json` maps every deferred skill to either a
   frozen OSWorld source artifact or a native seed profile. Only HTTPS downloads
   from the allowlisted OSWorld Hugging Face cache are accepted.
2. `materialize_impress_artifact_catalog.py` verifies the frozen task JSON hash,
   downloads the declared PPTX and attachments, replaces source slide text with
   privacy-safe workshop content, trims long decks to six slides while preserving
   native OOXML parts, rejects
   macros and (by default) external relationships, and records every SHA256.
3. `deferred_skill_generation_plan.json` groups the 21 deferred skills into 14
   coherent candidate groups (at most 20). The dedicated LLM prompt receives the
   materialized artifact inspection, fixed attachment names, expected output
   names, and adapter requirements.
4. `build_impress_deferred_artifacts.py` installs one adapted primary PPTX per
   candidate, copies required PNG/MP3 inputs, renders previews, and emits an
   artifact manifest containing supporting inputs, UI setup profiles, and extra
   outputs.
5. The normal annotation-config/review-packet path accepts those manifest fields.
   The recorder uploads every input but opens only the primary PPTX, applies the
   allowlisted pre-recording UI setup, and collects required Save As or PNG files
   in addition to the final PPTX.

Materialize the catalog before generating packages:

```bash
python scripts/python/materialize_impress_artifact_catalog.py \
  --output-dir evaluation_examples/expert_skill_learning/impress_full_v1/generated_v2/deferred_artifacts/materialized
```

After the current round has no pending reviews, generate the next deferred
round with `scripts/python/generate_impress_deferred_packages.py`, then build its
artifacts with `scripts/python/build_impress_deferred_artifacts.py`. The generator
enforces the existing review gate and refuses more than 20 candidates.

## Round 1 engineering pilot

- Extracted reusable skills: 66 from 45 source tasks
- Source-task `no_reusable_skills` outcomes: 2
- `pilot_static` skills eligible for this adapter: 46
- Deferred or waiver-candidate skills: 20
- Pending reference candidates: 5 (the review gate remains closed)
- Eligible skills covered by the pending candidates: 21
- Skills unresolved before human review: 45 total, including deferred skills
- Candidate limit: five for this engineering pilot; later rounds remain capped
  at 20 and must wait for the prior round's human decisions

Round outputs are under `generated/round_01/`. Each review packet contains an
editable `initial_artifact.pptx`, rendered initial-state previews, the OSWorld
task config, the full `TASK_DETAIL.md`, the annotator-facing `TASK.md`, and a
local `review.json`. Approval and recording are intentionally not performed by
generation.
