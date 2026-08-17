# Regional Funding Board View

- Reference task: `reference-task-calc-full-r01-002`
- Application: `libreoffice_calc`
- Review decision: `pending`

## Task instruction

Prepare the board-ready funding view by duplicating each initiative's planned allocation into the blank Board View column and displaying those copied amounts as rounded billions with one decimal place and a spaced B suffix.

## Required skills

### 1. Paste copied cells into a different column

Skill ID: `21df9241-f8d7-4509-b7f1-37e501a823f7.skill-03`

Procedure:

1. With copied cells still on the clipboard, click the top destination cell in another column, for example C2.
2. Press Ctrl+V to paste the copied range beginning at that cell.

Efficiency tip: After copying, use Ctrl+V immediately in the target cell; this is faster and less error-prone than reselecting and duplicating content manually.

Source task: `21df9241-f8d7-4509-b7f1-37e501a823f7`

Source instruction: Change the representation of column "Parameter" to show in Millions (M) in Column B and Billions (B) in Column C. The numbers should be rounded to one decimal place, and half should be rounded up. Then remember to place a white space between the digits and the unit.

Directly referenced source actions:

- Action 10: <code>`CLICK` C2</code>
- Action 11: <code>`HOTKEY` CTRL-V</code>

### 2. Format values as rounded billions with a spaced unit suffix

Skill ID: `21df9241-f8d7-4509-b7f1-37e501a823f7.skill-04`

Procedure:

1. Select the cells to format, right-click, and choose Format Cells.
2. Activate the format-code field and enter `0.0,,, \B`, then confirm with Enter.
3. The three trailing commas scale the display by one billion, `0.0` shows one decimal place, and the literal space before `\B` leaves a space before the B suffix. For example, 12500000000 displays as `12.5 B`.

Efficiency tip: Use comma scaling in a custom format instead of changing underlying values, so calculations retain their original precision and magnitude.

Source task: `21df9241-f8d7-4509-b7f1-37e501a823f7`

Source instruction: Change the representation of column "Parameter" to show in Millions (M) in Column B and Billions (B) in Column C. The numbers should be rounded to one decimal place, and half should be rounded up. Then remember to place a white space between the digits and the unit.

Directly referenced source actions:

- Action 12: <code>`RIGHT_CLICK`</code>
- Action 13: <code>`CLICK` &#x27;Format Cells...&#x27;</code>
- Action 14: <code>`DOUBLE_CLICK` format code box</code>
- Action 15: <code>`TYPING` &#x27;0.0,,, \B&#x27;</code>
- Action 16: <code>`PRESS` enter</code>

## Initial artifact

- Domain: Synthetic regional infrastructure funding plan
- Workbook: [initial_artifact.xlsx](artifact/initial_artifact.xlsx)
- Blueprint: [artifact_blueprint.json](artifact/artifact_blueprint.json)
- QA report: [artifact_qa.json](artifact/artifact_qa.json)

Initial state:

- The active sheet is "Funding Plan".
- Row 1 contains headers and rows 2-11 contain complete project and source-value data.
- Column C, "Board View", is entirely blank in C2:C11.
- The source range B2:B11 contains numeric values, not text.
- No cells in C2:C11 use a billions-scaled custom number format.

Artifact construction requirements:

- All content is synthetic and privacy-safe; do not use personal names, real organizations, or real account information.
- Create one workbook titled "Regional Funding Board View" with a single worksheet named "Funding Plan".
- Populate rows 2-11 with these records: North Transit | 12450000000; River Resilience | 8750000000; Community Clinics | 3620000000; Grid Modernization | 15180000000; Digital Access | 2190000000; Coastal Protection | 10440000000; School Renewal | 5970000000; Water Reliability | 7310000000; Housing Retrofit | 2860000000; Emergency Logistics | 12990000000.
- Format the source funding values in column B as ordinary USD currency with thousands separators and zero decimal places. Leave column C in General format initially.
- Use a simple styled header row with bold text and a light fill; no native Pivot Tables, charts, conditional formatting, or custom number formats are preconfigured.

| Sheet | Rows | Purpose | Columns |
| --- | ---: | --- | --- |
| Funding Plan | 10 | Lists synthetic funding initiatives and their raw planned allocations, with a blank board-ready display column. | Initiative (text), Planned Allocation (USD) (currency), Board View (currency) |

Must remain incomplete before recording:

- Do not prefill or formula-fill C2:C11.
- Do not apply the rounded-billions display format to C2:C11 before the recorded task.
- Do not alter the numeric source values in B2:B11.

Artifact previews:

### Funding Plan

![Funding_Plan.png](artifact/previews/Funding_Plan.png)

## Operator guide

### Demonstration 1

- Skill: `21df9241-f8d7-4509-b7f1-37e501a823f7.skill-03`
- Intent: Paste the copied planned-allocation values into the blank Board View column beginning at C2.
- Efficiency: Copy the contiguous source range once, then paste starting at the top destination cell so Calc fills the matching range in one action.
- Visible success: C2:C11 are populated with the same underlying numeric amounts as B2:B11, while the Initiative and source columns remain unchanged.

### Demonstration 2

- Skill: `21df9241-f8d7-4509-b7f1-37e501a823f7.skill-04`
- Intent: Format the populated Board View values as rounded billions with one decimal place and a space before the B unit suffix.
- Efficiency: Apply a comma-scaled custom number format to the whole Board View range rather than changing the underlying amounts; use a one-decimal billions format with a literal spaced B suffix (for example, `0.0,,, \B`).
- Visible success: The Board View column shows values such as 12.5 B, 8.8 B, and 3.6 B, while the formula/input line retains the full raw amounts.

Recording start: The Funding Plan sheet is open with populated source values in B2:B11 and a blank Board View destination range C2:C11.

Recording end: The Funding Plan sheet has B2:B11 copied into C2:C11, and every Board View entry displays as a one-decimal rounded number of billions followed by a spaced B suffix.

Allowed variation: The expert may use keyboard shortcuts, menus, the format dialog, or another equivalent LibreOffice Calc method. The pasted values must remain numeric and the Board View display must visibly use a single decimal place, a space, and the B suffix.

## Expected incidental operations

- **substantive_prerequisite:** Select and copy the numeric source range B2:B11 so the values are available on the clipboard. Reason: A copied cell range is required before the mandatory paste operation can be demonstrated.
- **scaffolding:** Select the pasted Board View cells when applying the number format. Reason: The custom display format must be targeted to the completed board-view range.

## Source-similarity audit

| Measure | Maximum | Most similar source task |
| --- | ---: | --- |
| Lexical sequence similarity | 0.382979 | 1de60575-bb6e-4c3d-9e6a-2fa699f9f197 |
| Semantic cosine similarity | 0.474372 | 21df9241-f8d7-4509-b7f1-37e501a823f7 |

Scores are reviewer aids, not automatic acceptance thresholds. Compare the task with the source instructions and actions above for solution leakage.

## Review this package

Check that every required skill is necessary and observable, the task is natural and not a source-solution reproduction, incidental operations are limited, the artifact matches its specification, and the guide remains helpful without prescribing one click-by-click trajectory.

1. Inspect the task, required skills, source evidence, artifact, and guide.
2. Fill [review.json](review.json) using `approved`, `revision_requested`, or `rejected`.
3. From the repository root, collect all completed forms:

```bash
python scripts/python/manage_reference_review_packets.py collect
```

Detailed field guidance is in [`reviewer.md`](../../../reviewer.md).

## Start annotation after approval

```bash
python scripts/python/record_reference_task.py \
  --reference-task-id reference-task-calc-full-r01-002
```

The ordinary launcher reads the collected central review file and refuses pending, revision-requested, or rejected tasks.
