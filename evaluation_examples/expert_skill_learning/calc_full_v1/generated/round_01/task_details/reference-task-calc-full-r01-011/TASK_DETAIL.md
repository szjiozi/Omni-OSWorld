# Community Workshop Event Finance

- Reference task: `reference-task-calc-full-r01-011`
- Application: `libreoffice_calc`
- Review decision: `pending`

## Task instruction

Complete the Event Ledger for the community workshop program: calculate Gross Revenue as Registrations multiplied by Fee per Registration and Community Share as Gross Revenue plus Sponsor Grant for every event. Populate the Upload handoff sheet with the complete Event Code column, then add a clustered column chart on Event Ledger comparing Gross Revenue and Community Share for each Event Code.

## Required skills

### 1. Autofill a formula downward by double-clicking the fill handle

Skill ID: `04d9aeaf-7bed-4024-bedb-e10e6f00eb7f.skill-05`

Procedure:

1. Select a formula cell, such as B2.
2. Double-click the fill handle at the cell's bottom-right corner. Calc fills the formula down through the contiguous data region determined by adjacent populated cells.
3. Repeat on another formula column when needed, such as C2 or D2; relative row references update in each filled row.

Efficiency tip: Double-clicking the fill handle is faster and less error-prone than manually dragging to an estimated final row when an adjacent column defines the data extent.

Source task: `04d9aeaf-7bed-4024-bedb-e10e6f00eb7f`

Source instruction: In a new sheet with 4 headers "Year", "CA changes", "FA changes", and "OA changes", calculate the percentage annual changes compared to last year in 2015 to 2019 for the Current Assets, Fixed Assets, and Other Assets columns. 

Directly referenced source actions:

- Action 16: <code>`CLICK` cell B2</code>
- Action 17: <code>`DOUBLE_CLICK` bottom right corner</code>
- Action 21: <code>`CLICK` cell C2</code>
- Action 22: <code>`DOUBLE_CLICK` bottom right corner</code>
- Action 23: <code>`MOVE_TO` cell D2</code>
- Action 24: <code>`DOUBLE_CLICK` bottom right corner</code>

### 2. Autofill a formula downward by double-clicking the fill handle

Skill ID: `21ab7b40-77c2-4ae6-8321-e00d3a086c73.skill-02`

Procedure:

1. Select the cell that contains the completed formula.
2. Double-click the small fill handle at the cell’s bottom-right corner. Calc extends the formula down through the contiguous neighboring data rows; for example, a formula in C2 is filled down alongside populated rows in adjacent columns.

Efficiency tip: Double-clicking the fill handle is faster and less error-prone than dragging it through a long adjacent data region.

Source task: `21ab7b40-77c2-4ae6-8321-e00d3a086c73`

Source instruction: Please calculate the period rate for my data in a new column with header "Period Rate (%)", convert the results as number type, and highlight the highest result with green (#00ff00) font.

Directly referenced source actions:

- Action 5: <code>`CLICK` cell C2</code>
- Action 6: <code>`DOUBLE_CLICK` bottom right corner of the cell C2</code>

### 3. Copy an entire spreadsheet column

Skill ID: `1273e544-688f-496b-8d89-3e0f40aa0606.skill-01`

Procedure:

1. Click the column header letter for the column you want to copy, such as column A. Calc highlights the entire column, including any header cell.
2. Press Ctrl+C to copy the selected column to the clipboard.

Efficiency tip: Click the column letter once rather than dragging through all populated cells; this selects the complete column, including its header, in one action.

Source task: `1273e544-688f-496b-8d89-3e0f40aa0606`

Source instruction: Copy the "Revenue" column along with the header to a new sheet named "Sheet2".

Directly referenced source actions:

- Action 0: <code>`CLICK` on grey box with A for selecting entire column</code>
- Action 1: <code>`HOTKEY` ctrl+c</code>

### 4. Insert a chart from a selected data range

Skill ID: `12382c62-0cd1-4bf2-bdc8-1d20bf9b2371.skill-01`

Procedure:

1. Select the contiguous cell range containing the category labels and numeric series, for example a table with week labels in the first column and two value columns.
2. Use the Insert Chart toolbar icon to create a chart based on the current selection.
3. In the chart wizard, choose a Column chart with the Clustered Column variant if it is not already selected, then finish inserting the chart.

Efficiency tip: Select the complete source range before inserting the chart so Calc can create the chart with the correct data series and category labels without later manual range edits.

Source task: `12382c62-0cd1-4bf2-bdc8-1d20bf9b2371`

Source instruction: Create a clustered column chart showing the Sales and COGS data for each week in a new sheet. Set the chart title as "Sales & COGS".

Directly referenced source actions:

- Action 0: <code>`HOTKEY` ctrl-A</code>
- Action 1: <code>`CLICK` insert chart icon</code>

## Initial artifact

- Domain: Community workshop event finance
- Workbook: [initial_artifact.xlsx](artifact/initial_artifact.xlsx)
- Blueprint: [artifact_blueprint.json](artifact/artifact_blueprint.json)
- QA report: [artifact_qa.json](artifact/artifact_qa.json)

Initial state:

- The active sheet is "Event Ledger".
- The Event Ledger data region is contiguous from A1:F19, and columns D:F are populated for every record, enabling adjacent-region formula filling.
- Only the first data-row formulas in B2 and C2 are present; their corresponding formula columns have not been completed.
- The Upload template exists but contains only its A1 header.

Artifact construction requirements:

- Use wholly synthetic, privacy-safe event records with no real people, organizations, addresses, or account identifiers.
- Create sheet "Event Ledger" with headers in row 1 and 18 contiguous event records in rows 2-19. Populate input columns A and D:F as follows: EVT-101,24,35,120; EVT-102,18,40,80; EVT-103,31,28,150; EVT-104,16,45,60; EVT-105,27,32,110; EVT-106,22,38,90; EVT-107,35,25,175; EVT-108,19,42,70; EVT-109,29,30,130; EVT-110,14,50,55; EVT-111,33,27,160; EVT-112,21,36,85; EVT-113,26,34,100; EVT-114,17,48,65; EVT-115,30,29,140; EVT-116,23,37,95; EVT-117,28,31,125; EVT-118,20,44,75. The values after each event code correspond respectively to Registrations, Fee per Registration, and Sponsor Grant.
- On "Event Ledger", set seed formula B2 to =D2*E2 and seed formula C2 to =B2+F2. Leave B3:C19 truly blank, with no formulas or values.
- Format B:C and E:F as currency with two decimal places. Format D as an integer.
- Create a second sheet named "Upload". Set A1 to "Event Code" and leave A2:A19 blank. It is a handoff template for the event-code list.
- Use ordinary header styling only, such as bold text and a light fill. Do not add a native chart, Pivot Table, filter, conditional formatting rule, or data validation.

| Sheet | Rows | Purpose | Columns |
| --- | ---: | --- | --- |
| Event Ledger | 19 | Source records and calculated event-finance comparison data. | Event Code (text), Gross Revenue (currency), Community Share (currency), Registrations (integer), Fee per Registration (currency), Sponsor Grant (currency) |
| Upload | 19 | Blank handoff column for copied event codes. | Event Code (text) |

Must remain incomplete before recording:

- Do not prefill formulas or calculated results in B3:C19.
- Do not copy Event Ledger column A into the Upload sheet.
- Do not create any chart before the recorded task.

Artifact previews:

### Event Ledger

![Event_Ledger.png](artifact/previews/Event_Ledger.png)

### Upload

![Upload.png](artifact/previews/Upload.png)

## Operator guide

### Demonstration 1

- Skill: `04d9aeaf-7bed-4024-bedb-e10e6f00eb7f.skill-05`
- Intent: Extend the Gross Revenue seed calculation from B2 through every listed event by double-clicking its fill handle.
- Efficiency: Use the existing populated records in the adjacent input columns as the boundary, avoiding a manual drag through the event list.
- Visible success: Gross Revenue cells B2:B19 display calculated currency amounts, with the formula filled through the last event row.

### Demonstration 2

- Skill: `21ab7b40-77c2-4ae6-8321-e00d3a086c73.skill-02`
- Intent: Extend the Community Share seed calculation from C2 through every listed event by double-clicking its fill handle.
- Efficiency: After Gross Revenue is available, double-click the Community Share seed cell's fill handle so row-relative references are extended consistently.
- Visible success: Community Share cells C2:C19 are filled with calculated currency values, including the final event row.

### Demonstration 3

- Skill: `1273e544-688f-496b-8d89-3e0f40aa0606.skill-01`
- Intent: Copy the entire Event Code column from Event Ledger for the Upload handoff sheet.
- Efficiency: Select the A column header directly rather than selecting only the visible event-code cells, so the header and complete column are copied together.
- Visible success: The full Event Code column is visibly selected and copied; after the ordinary paste step, Upload shows the Event Code header and all event codes in column A.

### Demonstration 4

- Skill: `12382c62-0cd1-4bf2-bdc8-1d20bf9b2371.skill-01`
- Intent: Insert a clustered column chart comparing Gross Revenue and Community Share by Event Code.
- Efficiency: Select the already contiguous A1:C19 comparison table before chart insertion so Event Code labels and both calculated series are detected without later source-range edits.
- Visible success: An embedded clustered column chart is present on Event Ledger with Event Code categories and separate Gross Revenue and Community Share series.

Recording start: Event Ledger is active with only B2 and C2 seeded as formulas, all lower calculated cells blank, no chart, and Upload containing only its header.

Recording end: Event Ledger has completed B2:C19 calculations and an embedded clustered column comparison chart sourced from A1:C19; Upload A1:A19 contains the copied Event Code header and event-code list.

Allowed variation: The expert may complete the two calculated columns in either order, use keyboard shortcuts where appropriate, and use any efficient equivalent chart-insertion path, provided the intended full-column copy, formula fills, and clustered comparison chart are visibly demonstrated.

## Expected incidental operations

- **substantive_prerequisite:** Enter or confirm the seeded Gross Revenue formula in B2 and the seeded Community Share formula in C2 before extending each formula column. Reason: The two formula-fill demonstrations require a completed starting formula in the first data row of each calculated column.
- **task_specific:** Move the copied Event Code column to the Upload sheet and paste it beginning at A1. Reason: Copying the full source column produces the requested populated handoff template.

## Source-similarity audit

| Measure | Maximum | Most similar source task |
| --- | ---: | --- |
| Lexical sequence similarity | 0.336957 | 3a7c8185-25c1-4941-bd7b-96e823c9f21f |
| Semantic cosine similarity | 0.487496 | 035f41ba-6653-43ab-aa63-c86d449d62e5 |

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
  --reference-task-id reference-task-calc-full-r01-011
```

The ordinary launcher reads the collected central review file and refuses pending, revision-requested, or rejected tasks.
