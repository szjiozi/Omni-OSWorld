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

The first engineering pilot is limited to five static, artifact-producing
candidates. Notes, master-slide operations, transitions, embedded media, app
settings, and extra-output workflows remain in the skill pool but are deferred
until their artifact and annotation adapters are enabled or reviewed for waiver.

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
