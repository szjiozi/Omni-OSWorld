# LibreOffice Calc full reference-task dataset

This directory expands the expert-skill reference-task pipeline from the
three-source engineering pilot to every LibreOffice Calc task in the pinned
OSWorld-Human source revision.

## Frozen source

- Repository: `https://github.com/WukLab/osworld-human`
- Commit: `deff1a7cd8940f6040a895593097fc3c5511f36b`
- Application: `libreoffice_calc`
- Raw source tasks: 47
- Raw single actions: 623
- Copy policy: byte-for-byte; the 47 JSON files are never rewritten
- Integrity: `source/osworld_human/<commit>/SHA256SUMS`
- Provenance: `source/osworld_human/<commit>/PROVENANCE.json`

The pinned upstream root did not contain a `LICENSE` file. Its README is copied
unchanged beside the vendored task directory so the source's evaluation-only
usage warning remains attached to the data.

## Skill extraction

The frozen three-task pilot skill pool is reused for its three source task IDs.
The remaining 44 tasks were extracted independently with one durable checkpoint
per task under `generated/skill_extraction/checkpoints/`.

- Reused pilot skills: 12
- Full skill pool: 124
- Explicit `no_reusable_skill` outcomes: 1
- Waiver candidate: `2bd59342-0664-4ccb-ba87-79379096cc08`

No cross-task skill deduplication is applied in this version.

## Existing annotation coverage

The four pilot reference tasks already have completed annotation episodes and
must not be regenerated or recorded again. Their 12 covered skills are recorded
in `legacy_annotation_coverage.json` and start full-dataset generation as
already covered.

## Round 1 status

- New reference candidates: 20
- Previously covered skills: 12
- Newly candidate-covered skills: 66
- Total currently covered skills: 78 / 124
- Skills left for later approved-coverage rounds: 46
- Human review decision: pending for all 20 new candidates

Open `review_packets/round_01/index.md`, review one task directory at a time,
and fill its `review.json`. Each packet contains the concise `TASK.md`, the
internal `TASK_DETAIL.md`, the initial XLSX and previews, QA, task config, source
similarity evidence, and the Chinese reference solution guide.

Do not generate round 2 until every round-1 packet has a review decision. The
copy-pasteable collect command in each `TASK.md` and in the round index uses the
full `calc_full_v1` paths and writes `generated/round_01/coverage_state.json`.
