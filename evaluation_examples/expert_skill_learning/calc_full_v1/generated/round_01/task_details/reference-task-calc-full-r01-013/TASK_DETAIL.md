# Garden Supply Delivery Review

- Reference task: `reference-task-calc-full-r01-013`
- Application: `libreoffice_calc`
- Review decision: `pending`

## Task instruction

Prepare the garden supply delivery review by creating a bar chart that compares delivered units across the garden zones in the Route Snapshot sheet, then open the Pivot Table layout for the Deliveries records so the delivery data is ready for a garden-zone analysis. Leave the Pivot Table layout open rather than creating its output.

## Required skills

### 1. Open the Pivot Table layout from a selected data range

Skill ID: `30e3e107-1cfb-46ee-a755-2cd080d7ba6a.skill-06`

Procedure:

1. Switch to the worksheet containing the source data and select the relevant source range or column; for example, click a column header to select that column.
2. Click the Pivot Table toolbar icon.
3. Accept the inferred source selection, for example by pressing Enter, to open the Pivot Table layout dialog.

Efficiency tip: Select the intended source column before invoking Pivot Table so Calc can infer the source selection immediately.

Source task: `30e3e107-1cfb-46ee-a755-2cd080d7ba6a`

Source instruction: Please create a new sheet. Keep its sheet name as "Sheet2". Merge cells A1:C1 in the new sheet and write "Demographic Profile" with blue (#0000ff) fill and bold white text. Then I want to create three pivot tables to show the percentage of Sex, Civil Status, and Highest Educational Attainment. They should be stacked one by one in Sheet2, each separated with a blank line.

Directly referenced source actions:

- Action 16: <code>`CLICK` Sheet1</code>
- Action 17: <code>`CLICK` column B grey cell</code>
- Action 18: <code>`CLICK` pivot table icon</code>
- Action 19: <code>`PRESS` enter</code>
- Action 36: <code>`CLICK` Sheet1</code>
- Action 37: <code>`CLICK` column C grey cell</code>
- Action 38: <code>`CLICK` pivot table icon</code>
- Action 39: <code>`PRESS` enter</code>
- Action 56: <code>`CLICK` Sheet1</code>
- Action 57: <code>`CLICK` column D grey cell</code>
- Action 58: <code>`CLICK` pivot table icon</code>
- Action 59: <code>`PRESS` enter</code>

### 2. Insert a bar chart from the selected spreadsheet range

Skill ID: `0326d92d-d218-48a8-9ca1-981cd6d064c7.skill-04`

Procedure:

1. With the chart source ranges selected, click the chart icon in the spreadsheet interface.
2. Choose the Bar chart type to create a bar chart from the selected labels and values.

Efficiency tip: Select the intended source ranges first, then choose the chart type directly from the chart control so the chart is created with the correct data and type in one pass.

Source task: `0326d92d-d218-48a8-9ca1-981cd6d064c7`

Source instruction: Calculate the total sales in an underneath row called "Total" and display the total of each month as bars. Then calculate the month-on-month growth percentage for Feb to Jun in another row called "Growth" and show them in a line chart (Jan should be omitted in the chart as well). Set the chart titles as the two row headers respectively.

Directly referenced source actions:

- Action 16: <code>`CLICK` chart icon</code>
- Action 17: <code>`CLICK` Bar</code>

## Initial artifact

- Domain: community garden supply deliveries
- Workbook: [initial_artifact.xlsx](artifact/initial_artifact.xlsx)
- Blueprint: [artifact_blueprint.json](artifact/artifact_blueprint.json)
- QA report: [artifact_qa.json](artifact/artifact_qa.json)

Initial state:

- The workbook opens on the Deliveries sheet, with cell A1 active.
- Deliveries contains a contiguous source-data range A1:G37 with no blank rows or columns inside the range.
- Route Snapshot contains a contiguous chart-source range A1:B7.
- There are no charts and no Pivot Tables in the workbook.

Artifact construction requirements:

- All names, route labels, item names, and values are synthetic and privacy-safe.
- Use ordinary header styling: bold text with a muted green fill for header rows; keep all data in standard cell ranges rather than Excel tables.
- Do not create any native Pivot Table, chart, named range, or conditional-format rule in the initial workbook.
- The Route Snapshot values are precomputed static summary values, so they can be charted without requiring a formula or Pivot Table.

| Sheet | Rows | Purpose | Columns |
| --- | ---: | --- | --- |
| Deliveries | 36 | Source records for a planned Pivot Table analysis of garden-supply deliveries. | Delivery ID (text), Delivery Date (date), Garden Zone (text), Supply Category (text), Item (text), Units Delivered (integer), Delivery Cost (currency) |
| Route Snapshot | 6 | Prepared zone-level delivery totals to use as the source for a bar chart. | Garden Zone (text), Delivered Units (integer) |

Must remain incomplete before recording:

- Do not preconfigure or insert a native Pivot Table; opening its layout/configuration dialog is part of the recorded work.
- Do not preconfigure or insert a chart; creating the bar chart is part of the recorded work.
- Do not add a completed Pivot Table result sheet or output table.

Artifact previews:

### Deliveries

![Deliveries.png](artifact/previews/Deliveries.png)

### Route Snapshot

![Route_Snapshot.png](artifact/previews/Route_Snapshot.png)

## Operator guide

### Demonstration 1

- Skill: `30e3e107-1cfb-46ee-a755-2cd080d7ba6a.skill-06`
- Intent: Open the Pivot Table layout using the selected delivery-record source range, ready for a garden-zone delivery analysis.
- Efficiency: Use the contiguous data block on Deliveries so Calc can infer the full source immediately; confirm the inferred range rather than manually rebuilding it.
- Visible success: The Calc Pivot Table Layout dialog is open and its source corresponds to the Deliveries data range.

### Demonstration 2

- Skill: `0326d92d-d218-48a8-9ca1-981cd6d064c7.skill-04`
- Intent: Create a bar chart that compares delivered units across garden zones from the Route Snapshot summary.
- Efficiency: Select both columns of the compact Route Snapshot range, including headers, before launching chart creation so zone labels and delivered-unit values are detected together.
- Visible success: A bar chart is visibly inserted on Route Snapshot, with garden-zone categories and bars representing Delivered Units.

Recording start: The workbook is open on Deliveries with only the two ordinary data sheets and no charts or Pivot Tables.

Recording end: A bar chart based on Route Snapshot is visible in the workbook, and the Pivot Table Layout dialog for Deliveries is open without a Pivot Table output having been created.

Allowed variation: The demonstrator may create the chart before or after opening the Pivot Table layout, may select source ranges by dragging or through the name box, and may use menus, toolbar controls, or equivalent keyboard commands. The final recording should show the completed bar chart and the Pivot Table layout dialog open for the delivery source.

## Expected incidental operations

- **scaffolding:** Navigate between the Deliveries and Route Snapshot worksheets as needed. Reason: The Pivot Table source and chart source are intentionally on separate sheets.
- **substantive_prerequisite:** Select the complete contiguous source range on Deliveries before invoking Pivot Table. Reason: Calc needs a source selection in order to infer the Pivot Table input range.
- **substantive_prerequisite:** Accept the inferred Pivot Table source selection. Reason: This opens the Pivot Table layout dialog for the selected delivery records.
- **substantive_prerequisite:** Select the Garden Zone and Delivered Units chart-source range on Route Snapshot. Reason: The bar chart must use the supplied category labels and summary values.
- **task_specific:** Confirm the chart creation dialog after choosing the Bar chart type and leave the resulting chart visible on Route Snapshot. Reason: Calc requires confirmation to insert the requested chart object.

## Source-similarity audit

| Measure | Maximum | Most similar source task |
| --- | ---: | --- |
| Lexical sequence similarity | 0.307054 | abed40dc-063f-4598-8ba5-9fe749c0615d |
| Semantic cosine similarity | 0.47598 | 51719eea-10bc-4246-a428-ac7c433dd4b3 |

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
  --reference-task-id reference-task-calc-full-r01-013
```

The ordinary launcher reads the collected central review file and refuses pending, revision-requested, or rejected tasks.
