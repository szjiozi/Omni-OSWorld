# Garden Volunteer Activity

- Reference task: `reference-task-calc-full-r01-010`
- Application: `libreoffice_calc`
- Review decision: `pending`

## Task instruction

Create a Pivot Table on a new summary sheet that shows total volunteer service hours for each garden program, with the quarters displayed as column headings.

## Required skills

### 1. Add a numeric field as a Pivot Table data measure

Skill ID: `1de60575-bb6e-4c3d-9e6a-2fa699f9f197.skill-03`

Procedure:

1. Locate the numeric field to summarize in the Available Fields list.
2. Drag it to the Data fields box. For example, dragging “Revenue” to Data fields configures the Pivot Table to aggregate that numeric field.
3. Confirm the Pivot Table layout dialog to create or update the Pivot Table with the configured data measure.

Efficiency tip: Place numeric fields in Data fields only once the row/column layout is set, so it is easier to verify which measure will be summarized.

Source task: `1de60575-bb6e-4c3d-9e6a-2fa699f9f197`

Source instruction: Summarize the total revenue for each promotion type in a new sheet (Sheet2) with the promotion names as the column headers using the Pivot Table feature.

Directly referenced source actions:

- Action 5: <code>`MOVE_TO` &#x27;Revenue&#x27; in available fields section&#x27;</code>
- Action 6: <code>`DRAG_TO` &#x27;Data fields&#x27; box</code>
- Action 7: <code>`CLICK` ok</code>

### 2. Place a field in the Pivot Table column area

Skill ID: `1de60575-bb6e-4c3d-9e6a-2fa699f9f197.skill-02`

Procedure:

1. In the Pivot Table layout dialog, locate the desired categorical field in Available Fields.
2. Drag that field into the Column fields box. For example, dragging a field such as “Promotion” to Column fields creates a separate column heading for each distinct value.

Efficiency tip: Drag fields directly from Available Fields to the desired layout box instead of adding them first and repositioning them afterward.

Source task: `1de60575-bb6e-4c3d-9e6a-2fa699f9f197`

Source instruction: Summarize the total revenue for each promotion type in a new sheet (Sheet2) with the promotion names as the column headers using the Pivot Table feature.

Directly referenced source actions:

- Action 3: <code>`MOVE_TO` &#x27;Promotion&#x27; in available fields section</code>
- Action 4: <code>`DRAG_TO` &#x27;Column fields&#x27; box</code>

## Initial artifact

- Domain: Community garden volunteer activity
- Workbook: [initial_artifact.xlsx](artifact/initial_artifact.xlsx)
- Blueprint: [artifact_blueprint.json](artifact/artifact_blueprint.json)
- QA report: [artifact_qa.json](artifact/artifact_qa.json)

Initial state:

- The workbook opens with the "Activity Log" sheet active.
- Row 1 of "Activity Log" is a styled header row, and rows 2 through 37 contain complete records.
- The source table has no blank rows or blank columns within A1:E37.
- No summary sheet exists initially.
- No native Pivot Table exists initially.

Artifact construction requirements:

- All data is synthetic and privacy-safe.
- Create a workbook titled "Garden Volunteer Activity" with the source records arranged as a contiguous table beginning at A1.
- Use realistic repeated categorical values so the Pivot Table has multiple row and column categories.
- Format Service Hours as a number with one decimal place; do not use formulas, Pivot Tables, charts, filters, or conditional formatting in the initial workbook.

| Sheet | Rows | Purpose | Columns |
| --- | ---: | --- | --- |
| Activity Log | 36 | Source records for a volunteer-hours summary | Program (text), Quarter (text), Garden Site (text), Activity Type (text), Service Hours (decimal) |

Must remain incomplete before recording:

- Do not create a Pivot Table in advance.
- Do not add a Pivot Table output sheet in advance.
- Do not preconfigure Quarter in a Pivot Table column area.
- Do not preconfigure Service Hours as a Pivot Table data measure.

Artifact previews:

### Activity Log

![Activity_Log.png](artifact/previews/Activity_Log.png)

## Operator guide

### Demonstration 1

- Skill: `1de60575-bb6e-4c3d-9e6a-2fa699f9f197.skill-03`
- Intent: In the Pivot Table layout, add the Service Hours numeric field to the Data fields area so the report aggregates volunteer time.
- Efficiency: Set the row and column layout before adding the numeric measure so the intended cross-tab structure is easy to inspect.
- Visible success: The completed Pivot Table displays aggregated Service Hours values rather than individual activity records.

### Demonstration 2

- Skill: `1de60575-bb6e-4c3d-9e6a-2fa699f9f197.skill-02`
- Intent: In the Pivot Table layout, place Quarter in the column area to split the summary into quarter headings.
- Efficiency: Drag Quarter directly from the available fields into the Column fields area rather than adding and repositioning it.
- Visible success: The completed Pivot Table has distinct Quarter headings across the top, with totals aligned under each heading.

Recording start: The workbook is open on the populated Activity Log source sheet, with no Pivot Table or summary output present.

Recording end: A visible Pivot Table summarizes total Service Hours by Program in rows and Quarter in columns on an empty destination sheet or area.

Allowed variation: The expert may use any equivalent LibreOffice Calc Pivot Table workflow, choose any clear empty output location, and may rename the output sheet. The resulting summary should preserve Program as row labels, Quarter as column headings, and aggregated Service Hours as the displayed values.

## Expected incidental operations

- **substantive_prerequisite:** Select the complete Activity Log source table as the Pivot Table source range. Reason: A Pivot Table requires the record table to be identified before its layout can be configured.
- **substantive_prerequisite:** Create the Pivot Table on a new output sheet or other empty worksheet location. Reason: The requested summary needs a dedicated visible destination for the Pivot Table.
- **task_specific:** Place Program in the Pivot Table row area. Reason: Program labels are necessary to show the requested per-program totals beneath the Quarter headings.
- **scaffolding:** Optionally rename the Pivot Table output sheet to a meaningful summary name. Reason: This improves clarity but is not required for the Pivot Table field-placement skills.

## Source-similarity audit

| Measure | Maximum | Most similar source task |
| --- | ---: | --- |
| Lexical sequence similarity | 0.544747 | 535364ea-05bd-46ea-9937-9f55c68507e8 |
| Semantic cosine similarity | 0.575627 | 535364ea-05bd-46ea-9937-9f55c68507e8 |

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
  --reference-task-id reference-task-calc-full-r01-010
```

The ordinary launcher reads the collected central review file and refuses pending, revision-requested, or rejected tasks.
