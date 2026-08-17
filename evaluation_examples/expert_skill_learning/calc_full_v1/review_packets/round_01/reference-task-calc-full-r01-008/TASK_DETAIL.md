# Garden Supply Delivery Register

- Reference task: `reference-task-calc-full-r01-008`
- Application: `libreoffice_calc`
- Review decision: `pending`

## Task instruction

Complete the Line Total calculation for every delivery in the Garden Supply Delivery Register, then add a default-named worksheet and use it to show a Pivot Table summary of total delivery spending for each Garden Zone.

## Required skills

### 1. Create a Pivot Table with a row field and summed data field

Skill ID: `535364ea-05bd-46ea-9937-9f55c68507e8.skill-01`

Procedure:

1. Select the source data range, for example with Ctrl+A when the active sheet contains only the dataset.
2. Click the Pivot Table command and accept the detected source range in the initial dialog.
3. In the Pivot Table Layout dialog, drag the category field from Available Fields to Row Fields. For example, drag a field such as Product or Sales Channel to Row Fields.
4. Drag the numeric measure from Available Fields to Data Fields. For example, drag Revenue to Data Fields; Calc creates an aggregate, normally Sum, for that numeric field.
5. Confirm the layout with OK to generate the Pivot Table. Repeat the same layout pattern with different row fields as needed.

Efficiency tip: Select the entire source range before invoking the Pivot Table command so Calc can detect the source automatically, then drag fields directly into the layout areas rather than opening separate field-setting dialogs.

Source task: `535364ea-05bd-46ea-9937-9f55c68507e8`

Source instruction: Create two pivot tables in a new sheet showing the total revenue for each product and sales channel.

Directly referenced source actions:

- Action 0: <code>`HOTKEY` ctrl-a</code>
- Action 1: <code>`CLICK` pivot table icon</code>
- Action 2: <code>`PRESS` enter</code>
- Action 3: <code>`MOVE_TO` product in available fields box</code>
- Action 4: <code>`DRAG_TO` row fields box</code>
- Action 5: <code>`MOVE_TO` revenue in available fields box</code>
- Action 6: <code>`DRAG_TO` data fields box</code>
- Action 7: <code>`CLICK` ok</code>
- Action 12: <code>`HOTKEY` ctrl-a</code>
- Action 13: <code>`CLICK` pivot table icon</code>
- Action 14: <code>`PRESS` enter</code>
- Action 15: <code>`MOVE_TO` sales channel in available fields box</code>
- Action 16: <code>`DRAG_TO` row fields box</code>
- Action 17: <code>`MOVE_TO` revenue in available fields box</code>
- Action 18: <code>`DRAG_TO` data fields box</code>

### 2. AutoFill a formula down a contiguous data range using the fill handle

Skill ID: `0bf05a7d-b28b-44d2-955a-50b41e24012a.skill-02`

Procedure:

1. Select the cell that contains the formula to propagate.
2. Double-click the small fill handle at the cell’s bottom-right corner.
3. Calc fills the formula down alongside the neighboring contiguous data range, adjusting relative references for each row. For example, `=TEXT(C2,"0000000")` in D2 becomes `=TEXT(C3,"0000000")` in D3.

Efficiency tip: Double-click the fill handle when the adjacent source-data column is contiguous; this is faster and less error-prone than dragging through a long range.

Source task: `0bf05a7d-b28b-44d2-955a-50b41e24012a`

Source instruction: I would like to copy all the numbers in the 'Old ID' column to the 'New 7 Digit Id' column, and pad them with zeros in front, to fill them up to seven digits.

Directly referenced source actions:

- Action 2: <code>`CLICK` cell D2</code>
- Action 3: <code>`DOUBLE_CLICK` the bottom right corner of cell D2</code>

### 3. Insert a new worksheet with the default name

Skill ID: `30e3e107-1cfb-46ee-a755-2cd080d7ba6a.skill-01`

Procedure:

1. Click the plus button beside the worksheet tabs to add a new worksheet.
2. Calc creates the sheet with its next default name, for example, Sheet2; no sheet-tab rename action is needed when that default is desired.

Efficiency tip: Use the plus button when the default generated sheet name is acceptable; this avoids opening a rename workflow.

Source task: `30e3e107-1cfb-46ee-a755-2cd080d7ba6a`

Source instruction: Please create a new sheet. Keep its sheet name as "Sheet2". Merge cells A1:C1 in the new sheet and write "Demographic Profile" with blue (#0000ff) fill and bold white text. Then I want to create three pivot tables to show the percentage of Sex, Civil Status, and Highest Educational Attainment. They should be stacked one by one in Sheet2, each separated with a blank line.

Directly referenced source actions:

- Action 0: <code>`CLICK` on + to left of sheet1</code>

### 4. Create a Pivot Table from the current sheet selection

Skill ID: `1de60575-bb6e-4c3d-9e6a-2fa699f9f197.skill-01`

Procedure:

1. Click inside the source table and press Ctrl+A to select its current data range.
2. Click the toolbar command represented by the Pivot Table insert/edit icon.
3. In the initial Pivot Table dialog, verify that the selected range is the intended source and confirm it. For example, selecting a five-column table with Ctrl+A makes that table the Pivot Table source.

Efficiency tip: Use Ctrl+A when the active sheet contains one contiguous table; it quickly selects the complete source range before opening the Pivot Table command.

Source task: `1de60575-bb6e-4c3d-9e6a-2fa699f9f197`

Source instruction: Summarize the total revenue for each promotion type in a new sheet (Sheet2) with the promotion names as the column headers using the Pivot Table feature.

Directly referenced source actions:

- Action 0: <code>`HOTEKY` &#x27;ctrl-a&#x27;</code>
- Action 1: <code>`CLICK` curved arrow icon in the top bar representing insert or edit pivot table</code>
- Action 2: <code>`CLICK` ok</code>

## Initial artifact

- Domain: community garden supply deliveries
- Workbook: [initial_artifact.xlsx](artifact/initial_artifact.xlsx)
- Blueprint: [artifact_blueprint.json](artifact/artifact_blueprint.json)
- QA report: [artifact_qa.json](artifact/artifact_qa.json)

Initial state:

- The workbook contains exactly one worksheet named Delivery Log.
- Delivery Log has one contiguous table in A1:E25 with headers in row 1 and 24 data rows.
- The active cell may be within the Delivery Log table.
- No pivot table exists anywhere in the workbook.
- There is no Sheet2 initially, so the next inserted worksheet receives Calc's default name Sheet2.

Artifact construction requirements:

- Use entirely synthetic, privacy-safe delivery records with fictional garden zones and non-identifying supplier codes.
- Populate 24 delivery records with varied values so each Garden Zone occurs multiple times and summed delivery amounts differ by zone.
- Format Unit Price and Line Total as currency with two decimal places; format Quantity as an integer.
- Seed the Line Total formula only in E2 as =C2*D2. Leave E3:E25 empty so formula propagation is required during the task.

| Sheet | Rows | Purpose | Columns |
| --- | ---: | --- | --- |
| Delivery Log | 24 | Source register of supply deliveries whose line totals and zone-level spending summary must be prepared. | Delivery Code (text), Garden Zone (text), Quantity (integer), Unit Price (currency), Line Total (currency) |

Must remain incomplete before recording:

- Do not prefill Line Total formulas or values in E3:E25.
- Do not add Sheet2 before the recorded task.
- Do not create, configure, or prepopulate any pivot table or summary table.

Artifact previews:

### Delivery Log

![Delivery_Log.png](artifact/previews/Delivery_Log.png)

## Operator guide

### Demonstration 1

- Skill: `0bf05a7d-b28b-44d2-955a-50b41e24012a.skill-02`
- Intent: Propagate the seeded Line Total calculation from the first delivery row through the remaining contiguous delivery rows.
- Efficiency: Keep the seeded formula cell adjacent to the contiguous Quantity data and double-click its fill handle to extend it through all delivery records efficiently.
- Visible success: Every Line Total cell from E2 through E25 displays a calculated currency amount, with relative row references reflected in the formulas.

### Demonstration 2

- Skill: `30e3e107-1cfb-46ee-a755-2cd080d7ba6a.skill-01`
- Intent: Insert one blank worksheet and retain its automatically assigned default name.
- Efficiency: Use the sheet-tab plus control rather than a rename workflow, because the required default worksheet name is Sheet2.
- Visible success: A new worksheet tab named Sheet2 is visible alongside Delivery Log.

### Demonstration 3

- Skill: `1de60575-bb6e-4c3d-9e6a-2fa699f9f197.skill-01`
- Intent: Start Pivot Table creation using the current full delivery-table selection as the source.
- Efficiency: Activate Delivery Log and select its one contiguous table in a single action so Calc detects the entire source range without manual range editing.
- Visible success: The Pivot Table setup flow opens with the Delivery Log table range recognized as the data source.

### Demonstration 4

- Skill: `535364ea-05bd-46ea-9937-9f55c68507e8.skill-01`
- Intent: Configure and generate a pivot summary on Sheet2 that groups delivery spending by Garden Zone and totals Line Total.
- Efficiency: In the layout dialog, drag Garden Zone directly to Row Fields and Line Total directly to Data Fields; the numeric amount should default to a Sum aggregation.
- Visible success: Sheet2 visibly contains a pivot table with one row per Garden Zone and a summed Line Total amount for each zone, plus the pivot grand total.

Recording start: Delivery Log is the only sheet; its 24-row delivery table has only E2 seeded with the Line Total formula, and no pivot table exists.

Recording end: Delivery Log contains calculated Line Total values for all 24 records, and Sheet2 contains the completed Garden Zone by summed Line Total pivot table.

Allowed variation: The expert may insert Sheet2 before or after filling the line totals, may use menu or toolbar access to Pivot Table, and may choose any clear non-overlapping placement on Sheet2. Equivalent use of keyboard shortcuts is acceptable.

## Expected incidental operations

- **scaffolding:** Navigate between Delivery Log and the newly inserted Sheet2 worksheet as needed. Reason: The line-total source table and the requested pivot-table destination are on different sheets.
- **substantive_prerequisite:** Confirm the pivot table source range and choose a placement location on Sheet2. Reason: Calc requires a source-range confirmation and output destination to generate the requested summary.
- **scaffolding:** Select the contiguous source table before opening the Pivot Table command. Reason: This supplies the complete delivery data range for the pivot table.

## Source-similarity audit

| Measure | Maximum | Most similar source task |
| --- | ---: | --- |
| Lexical sequence similarity | 0.366762 | 26a8440e-c166-4c50-aef4-bfb77314b46b |
| Semantic cosine similarity | 0.518412 | 51719eea-10bc-4246-a428-ac7c433dd4b3 |

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
  --reference-task-id reference-task-calc-full-r01-008
```

The ordinary launcher reads the collected central review file and refuses pending, revision-requested, or rejected tasks.
