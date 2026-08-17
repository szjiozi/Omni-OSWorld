# Coastal Lab Dispatch Completion

- Reference task: `reference-task-calc-full-r01-012`
- Application: `libreoffice_calc`
- Review decision: `pending`

## Task instruction

Complete the Coastal Lab Dispatch Log by calculating the daily completion rate as verified kits divided by planned kits for every dispatch date, then add a lines-only line chart that shows how the completion rate changes across the dates.

## Required skills

### 1. Insert a lines-only line chart from selected spreadsheet data

Skill ID: `0a2e43bf-b26c-4631-a966-af9dfa12c9e5.skill-04`

Procedure:

1. With the intended data range selected, click the chart insertion icon to open chart creation.
2. Choose the Line chart type, then select the lines-only variant (the option without point markers, shown as the third icon from the right in this interface).
3. Click Finish to insert the chart using the current selection.

Efficiency tip: Choose the chart family and variant before finishing, so the chart is created correctly without needing to reopen its type settings afterward.

Source task: `0a2e43bf-b26c-4631-a966-af9dfa12c9e5`

Source instruction: Work out the monthly total sales in a new row called "Total" and then create a line chart to show the results (x-axis be Months).

Directly referenced source actions:

- Action 16: <code>`CLICK` chart icon</code>
- Action 17: <code>`CLICK` Line</code>
- Action 18: <code>`CLICK` icon representing lines only (3rd from the right)</code>
- Action 19: <code>`CLICK` Finish</code>

### 2. Autofill a formula down an adjacent data region

Skill ID: `51719eea-10bc-4246-a428-ac7c433dd4b3.skill-02`

Procedure:

1. Select the cell containing the completed formula, such as `G2`.
2. Move to the small fill handle at the cell's bottom-right corner.
3. Double-click the fill handle. Calc copies the formula downward to match the contiguous neighboring rows, adjusting relative references for each destination row.

Efficiency tip: Double-clicking the fill handle is faster and less error-prone than manually dragging it through a long adjacent data region.

Source task: `51719eea-10bc-4246-a428-ac7c433dd4b3`

Source instruction: Calculate revenue in a new column according to the Retail Price sheet (consider product price and quantity and discount), and generate a Pivot Table in a new sheet (Sheet2) that summarizes the revenue of each product.

Directly referenced source actions:

- Action 7: <code>`CLICK` cell G2</code>
- Action 8: <code>`MOVE_TO` bottom right corner of the cell G2`</code>
- Action 9: <code>`DOUBLE_CLICK`</code>

### 3. Create a row-wise division formula with relative references

Skill ID: `21ab7b40-77c2-4ae6-8321-e00d3a086c73.skill-01`

Procedure:

1. Select the first result cell in the output column and type a division formula using relative references.
2. For example, enter `=A2/B2` in the first result row and press Enter. When copied to later rows, Calc changes it to `=A3/B3`, `=A4/B4`, and so on.

Efficiency tip: Enter the formula once with relative references, then use an autofill technique instead of manually rewriting it for each row.

Source task: `21ab7b40-77c2-4ae6-8321-e00d3a086c73`

Source instruction: Please calculate the period rate for my data in a new column with header "Period Rate (%)", convert the results as number type, and highlight the highest result with green (#00ff00) font.

Directly referenced source actions:

- Action 3: <code>`TYPING` &#x27;=A2/B2&#x27;</code>
- Action 4: <code>`PRESS` enter</code>

## Initial artifact

- Domain: Coastal laboratory sample-dispatch tracking
- Workbook: [initial_artifact.xlsx](artifact/initial_artifact.xlsx)
- Blueprint: [artifact_blueprint.json](artifact/artifact_blueprint.json)
- QA report: [artifact_qa.json](artifact/artifact_qa.json)

Initial state:

- The workbook opens with the "Dispatch Log" sheet active.
- Row 1 contains headers and rows 2 through 25 contain the 24 source records.
- Column B, Completion Rate, is entirely blank from B2:B25 but is already percentage-formatted to one decimal place.
- Columns C and D contain contiguous complete numeric data for every record, enabling an entered formula in B2 to be filled down automatically.
- No chart object exists anywhere in the workbook.

Artifact construction requirements:

- All records and names must be synthetic and privacy-safe.
- Create one worksheet named "Dispatch Log" with 24 daily records, using consecutive dates in April 2026.
- Populate Planned Kits with varied whole-number values from 80 to 160 and Verified Kits with varied whole-number values that are positive and no greater than the corresponding Planned Kits value.
- Use realistic variation in the verified-to-planned ratio so the resulting trend is visibly non-flat.
- Apply a percentage number format with one decimal place to the blank Completion Rate column.
- Use a clear bold header row and ordinary table styling; do not create a chart, Pivot Table, conditional-format rule, or formula in the Completion Rate data cells.

| Sheet | Rows | Purpose | Columns |
| --- | ---: | --- | --- |
| Dispatch Log | 24 | Daily planned and verified kit counts, with a blank calculated completion-rate field for analysis. | Dispatch Date (date), Completion Rate (decimal), Planned Kits (integer), Verified Kits (integer) |

Must remain incomplete before recording:

- Do not prepopulate B2:B25 with formulas or values.
- Do not pre-create any chart or substitute another chart type for the requested lines-only line chart.
- Do not add totals, extra worksheets, or unrelated analysis.

Artifact previews:

### Dispatch Log

![Dispatch_Log.png](artifact/previews/Dispatch_Log.png)

## Operator guide

### Demonstration 1

- Skill: `21ab7b40-77c2-4ae6-8321-e00d3a086c73.skill-01`
- Intent: In the first blank Completion Rate cell, calculate each day's verified-kit share of its planned-kit count with a relative-reference division formula.
- Efficiency: Enter the calculation once using row-relative references; it will then adapt correctly for all later dates when filled.
- Visible success: B2 displays a percentage consistent with Verified Kits divided by Planned Kits for row 2.

### Demonstration 2

- Skill: `51719eea-10bc-4246-a428-ac7c433dd4b3.skill-02`
- Intent: Extend the first Completion Rate formula through every remaining dispatch record.
- Efficiency: Use the fill handle on the completed first formula to populate the contiguous records rather than retyping formulas.
- Visible success: B2:B25 are populated, and formulas in later rows reference the corresponding Planned Kits and Verified Kits cells.

### Demonstration 3

- Skill: `0a2e43bf-b26c-4631-a966-af9dfa12c9e5.skill-04`
- Intent: Create a line-only chart of the completed daily completion-rate trend from the selected Dispatch Date and Completion Rate data.
- Efficiency: Choose the Line chart family and its no-marker, lines-only variant before finishing chart creation.
- Visible success: A chart is visible with dates as categories and one connected Completion Rate line that has no point markers.

Recording start: The Dispatch Log sheet is active with the source table present, the Completion Rate cells blank, and no chart in the workbook.

Recording end: The Dispatch Log sheet retains all 24 records, B2:B25 show calculated percentage completion rates, and a readable lines-only line chart displays the daily rate trend.

Allowed variation: The operator may use keyboard entry, the formula bar, a fill-handle double-click, or an equivalent Calc autofill method. The chart may be positioned anywhere on the Dispatch Log sheet, provided it visibly uses Dispatch Date as the category axis and Completion Rate as the sole plotted series.

## Expected incidental operations

- **scaffolding:** Select the date and completed rate columns, including their headers, as the chart source range. Reason: The chart needs the daily dates as category labels and the calculated completion rates as its plotted series.
- **task_specific:** Place or resize the inserted chart so it is visibly readable without obscuring the dispatch table. Reason: This makes the completed trend visualization clearly inspectable in the final workbook.

## Source-similarity audit

| Measure | Maximum | Most similar source task |
| --- | ---: | --- |
| Lexical sequence similarity | 0.376022 | 0a2e43bf-b26c-4631-a966-af9dfa12c9e5 |
| Semantic cosine similarity | 0.355283 | 3a7c8185-25c1-4941-bd7b-96e823c9f21f |

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
  --reference-task-id reference-task-calc-full-r01-012
```

The ordinary launcher reads the collected central review file and refuses pending, revision-requested, or rejected tasks.
