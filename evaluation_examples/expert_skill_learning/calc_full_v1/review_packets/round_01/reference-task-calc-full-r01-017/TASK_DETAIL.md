# Solar Microgrid Review

- Reference task: `reference-task-calc-full-r01-017`
- Application: `libreoffice_calc`
- Review decision: `pending`

## Task instruction

Complete the daily net-delivery and target-variance calculations for all solar microgrid readings, then create a line chart of net delivery by reading date. Title it 'Daily Net Delivery Trend' and place it in the open area to the right of the data table.

## Required skills

### 1. Autofill a formula down a contiguous column

Skill ID: `4172ea6e-6b77-4edb-a9cc-c0014bd1603b.skill-02`

Procedure:

1. Select the cell containing the formula at the top of the output column.
2. Double-click the small fill handle at the cell’s bottom-right corner. Calc extends the formula downward alongside the adjacent contiguous data range, adjusting relative references for each row.
3. For example, double-clicking the fill handle of C2 containing `=A2+B2` fills subsequent rows with row-adjusted formulas such as `=A3+B3`.

Efficiency tip: Double-clicking the fill handle is faster than dragging it through a long contiguous table and avoids manually estimating the last row.

Source task: `4172ea6e-6b77-4edb-a9cc-c0014bd1603b`

Source instruction: I want to work out the maturity date for all the loans. Please do it for me in a new column with header "Maturity Date".

Directly referenced source actions:

- Action 5: <code>`CLICK` cell C2`</code>
- Action 6: <code>`DOUBLE_CLICK` bottom right corner of the cell C2`</code>

### 2. Reposition a chart object by dragging

Skill ID: `347ef137-7eeb-4c80-a3bb-0951f26a8aff.skill-02`

Procedure:

1. Click or point at the chart object's edge to target the chart rather than an individual data series.
2. Drag the chart from its top edge toward the desired location, such as moving it to the right side of the worksheet page.
3. Scroll horizontally if necessary to reach or verify the new placement while keeping the chart layout organized.

Efficiency tip: Reposition a chart by dragging it directly rather than reopening chart settings; scroll only as needed to expose the intended destination.

Source task: `347ef137-7eeb-4c80-a3bb-0951f26a8aff`

Source instruction: Here are two tables recording the per-month costs in 2019 and 2020. I want to create two column bar charts reflecting per-month total costs for each year from these data. Help me, Mr. Assistant!

Directly referenced source actions:

- Action 13: <code>`MOVE_TO` top edge of chart</code>
- Action 14: <code>`DRAG_TO` right edge of page</code>
- Action 15: <code>`SCROLL_LEFT`</code>

### 3. Set a chart title using chart elements

Skill ID: `12382c62-0cd1-4bf2-bdc8-1d20bf9b2371.skill-02`

Procedure:

1. Click the chart, then open its Chart Elements controls in the right sidebar.
2. Enable or select the chart title element and click the title text box.
3. Type the desired title, for example `Sales & COGS`, and press Enter to apply the text.

Efficiency tip: Edit the title directly through the chart-elements title control instead of reopening the full chart wizard.

Source task: `12382c62-0cd1-4bf2-bdc8-1d20bf9b2371`

Source instruction: Create a clustered column chart showing the Sales and COGS data for each week in a new sheet. Set the chart title as "Sales & COGS".

Directly referenced source actions:

- Action 2: <code>`CLICK` chart elements on right sidebar</code>
- Action 3: <code>`CLICK` title text box</code>
- Action 4: <code>`TYPING` &#x27;Sales &amp; COGS&#x27;</code>
- Action 5: <code>`PRESS` enter</code>

### 4. Autofill a formula down a contiguous data range

Skill ID: `7efeb4b1-3d19-4762-b163-63328d66303b.skill-02`

Procedure:

1. Select the cell containing the formula to propagate, for example B2.
2. Move to the small square at the cell's bottom-right corner (the fill handle) and double-click it.
3. Calc fills the formula downward alongside the contiguous neighboring data range, adjusting relative references for each row. For example, `ROW(B2)` in B2 becomes `ROW(B3)` in B3.

Efficiency tip: Double-clicking the fill handle is faster than dragging it through a long table and typically stops at the end of adjacent populated data.

Source task: `7efeb4b1-3d19-4762-b163-63328d66303b`

Source instruction: Fill the Sequence Numbers as "No. #" in the "Seq No." column

Directly referenced source actions:

- Action 3: <code>`CLICK` B2</code>
- Action 4: <code>`DOUBLE_CLICK` bottom right corner of cell</code>

## Initial artifact

- Domain: Solar microgrid performance monitoring
- Workbook: [initial_artifact.xlsx](artifact/initial_artifact.xlsx)
- Blueprint: [artifact_blueprint.json](artifact/artifact_blueprint.json)
- QA report: [artifact_qa.json](artifact/artifact_qa.json)

Initial state:

- The workbook title is 'Solar Microgrid Review'.
- The 'Daily Readings' sheet is active.
- Columns A:D are fully populated without blank rows from row 1 through row 25.
- E1 is labeled 'Net Delivered kWh' and only E2 contains its seed formula; E3:E25 are blank.
- F1 is labeled 'Variance to Target kWh' and only F2 contains its seed formula; F3:F25 are blank.
- There is ample empty worksheet space to the right of the table, beginning around column H, for positioning a chart.
- No chart title or chart object exists initially.

Artifact construction requirements:

- All data is synthetic and privacy-safe.
- Create a single worksheet named 'Daily Readings'.
- Populate rows 1-25 with a contiguous daily table. Row 1 contains headers and rows 2-25 contain 24 consecutive synthetic daily readings.
- Use realistic decimal values: Generated kWh should range roughly from 380 to 760, Exported kWh from 250 to 610, and Target kWh from 400 to 650.
- Seed the formula in E2 as =B2-C2 and format column E as a decimal number with two places.
- Seed the formula in F2 as =E2-D2 and format column F as a decimal number with two places.
- Do not create a chart in the initial workbook; the chart needed for the task will be created during the demonstration.

| Sheet | Rows | Purpose | Columns |
| --- | ---: | --- | --- |
| Daily Readings | 24 | Daily synthetic solar microgrid readings and calculated delivery metrics | Reading Date (date), Generated kWh (decimal), Exported kWh (decimal), Target kWh (decimal), Net Delivered kWh (decimal), Variance to Target kWh (decimal) |

Must remain incomplete before recording:

- Do not prefill E3:E25 or F3:F25.
- Do not pre-create, title, or position the chart.
- Do not alter the input readings in columns A:D.

Artifact previews:

### Daily Readings

![Daily_Readings.png](artifact/previews/Daily_Readings.png)

## Operator guide

### Demonstration 1

- Skill: `4172ea6e-6b77-4edb-a9cc-c0014bd1603b.skill-02`
- Intent: Propagate the seeded Net Delivered kWh calculation from E2 through the contiguous daily-record range.
- Efficiency: Use the fill handle’s double-click behavior rather than dragging through all 24 records.
- Visible success: Every daily row from E2 through E25 displays a row-adjusted net-delivery result, with no blanks in the calculated column.

### Demonstration 2

- Skill: `7efeb4b1-3d19-4762-b163-63328d66303b.skill-02`
- Intent: Propagate the seeded Variance to Target kWh calculation from F2 through the same contiguous daily-record range.
- Efficiency: Use the fill handle’s double-click behavior so the calculation stops with the adjacent uninterrupted table.
- Visible success: Every daily row from F2 through F25 displays a row-adjusted variance result, with no blanks in the calculated column.

### Demonstration 3

- Skill: `12382c62-0cd1-4bf2-bdc8-1d20bf9b2371.skill-02`
- Intent: Set the line chart title to 'Daily Net Delivery Trend'.
- Efficiency: After creating the line chart, edit its title through the chart title/element controls rather than rebuilding the chart.
- Visible success: The displayed line chart visibly shows the exact title 'Daily Net Delivery Trend'.

### Demonstration 4

- Skill: `347ef137-7eeb-4c80-a3bb-0951f26a8aff.skill-02`
- Intent: Move the completed chart into the empty area to the right of the daily readings table.
- Efficiency: Drag the chart by its outer object boundary or top edge, not by an individual plotted series.
- Visible success: The titled chart is visibly positioned in the open right-side worksheet area and does not obscure the source table.

Recording start: The active Daily Readings sheet contains the populated input table, only the two seed formulas in row 2, and no chart.

Recording end: Both calculation columns are fully populated through the last reading, and a titled line chart of net delivery is visibly placed to the right of the table.

Allowed variation: The expert may create the chart before or after completing the calculations, use an equivalent line-chart creation path, and place the finished chart anywhere clearly to the right of the source table without covering headers or data.

## Expected incidental operations

- **substantive_prerequisite:** Create a line chart using Reading Date as the category axis and the completed Net Delivered kWh values as the plotted series. Reason: A chart object must exist before its title can be set and it can be repositioned.
- **scaffolding:** Select the relevant chart source range and place the newly created chart initially on the Daily Readings sheet. Reason: This is the minimal setup needed to produce the requested visible chart deliverable.

## Source-similarity audit

| Measure | Maximum | Most similar source task |
| --- | ---: | --- |
| Lexical sequence similarity | 0.37561 | 3a7c8185-25c1-4941-bd7b-96e823c9f21f |
| Semantic cosine similarity | 0.49437 | 0326d92d-d218-48a8-9ca1-981cd6d064c7 |

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
  --reference-task-id reference-task-calc-full-r01-017
```

The ordinary launcher reads the collected central review file and refuses pending, revision-requested, or rejected tasks.
