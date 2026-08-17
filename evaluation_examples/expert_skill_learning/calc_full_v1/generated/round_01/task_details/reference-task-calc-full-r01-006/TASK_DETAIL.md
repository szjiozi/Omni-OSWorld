# Route Operations Review

- Reference task: `reference-task-calc-full-r01-006`
- Application: `libreoffice_calc`
- Review decision: `pending`

## Task instruction

Prepare the Route Review for the municipal route-output report. Copy the 12 daily Output Volume values from Daily Metrics into the Working Output column, then calculate the day-over-day percentage change for every day after the first using formulas that keep Daily Metrics as the fixed source sheet. Build a distinct roster of nonblank Service Route names from the source table, preserving the first-seen order, with the result beginning at E5 on Route Review. Add a lines-only chart of Daily Change by Service Date, and export the completed review as /home/oai/share/route_operations_review.pdf.

## Required skills

### 1. Filter a range to copy only unique nonempty records

Skill ID: `abed40dc-063f-4598-8ba5-9fe749c0615d.skill-01`

Procedure:

1. Select the source range, including its header when present; for example, drag from B2 through B17.
2. Open Data > More Filters > Standard Filter.
3. In the filter criteria, set the relevant field/value condition to Not empty so blank records are excluded.
4. Open Options and enable No duplications to retain only the first occurrence of each repeated value in source order.
5. Enable Copy results to, click its destination box, and enter the top-left output cell reference, for example `$Sheet1.D2`. Here `$Sheet1` fixes the destination sheet, while column D and row 2 remain relative.
6. Confirm with OK to place the filtered unique records beginning at the specified destination cell.

Efficiency tip: Select the complete source range before opening the filter dialog so Calc can use it directly; enter the destination as a cell reference rather than copying results manually.

Source task: `abed40dc-063f-4598-8ba5-9fe749c0615d`

Source instruction: Check the names in column "Names with duplicates" and put the unique ones in column "Unique Names". Keep the original order of the first occurrences.

Directly referenced source actions:

- Action 0: <code>`MOVE_TO` B2</code>
- Action 1: <code>`DRAG_TO` B17</code>
- Action 2: <code>`CLICK` &#x27;Data&#x27; menu</code>
- Action 3: <code>`MOVE_TO` &#x27;More Filters&#x27;</code>
- Action 4: <code>`CLICK` &#x27;Standard Filter&#x27;</code>
- Action 5: <code>`CLICK` &#x27;Value dropdown</code>
- Action 6: <code>`CLICK` Not empty</code>
- Action 7: <code>`CLICK` &#x27;Options&#x27;</code>
- Action 8: <code>`CLICK` &#x27;No duplications&#x27;</code>
- Action 9: <code>`CLICK` copy to</code>
- Action 10: <code>`CLICK` text box below</code>
- Action 11: <code>`TYPING` &#x27;$Sheet1.D2</code>
- Action 12: <code>`CLICK` &#x27;OK&#x27;</code>

### 2. Insert a lines-only chart from the selected spreadsheet range

Skill ID: `0326d92d-d218-48a8-9ca1-981cd6d064c7.skill-07`

Procedure:

1. With the source ranges selected, click the chart icon and choose the Line chart category.
2. Choose the lines-only subtype, represented by the line-style icon, to create a chart without point markers.

Efficiency tip: Choose the specific line subtype during chart insertion instead of creating a default chart and changing its subtype afterward.

Source task: `0326d92d-d218-48a8-9ca1-981cd6d064c7`

Source instruction: Calculate the total sales in an underneath row called "Total" and display the total of each month as bars. Then calculate the month-on-month growth percentage for Feb to Jun in another row called "Growth" and show them in a line chart (Jan should be omitted in the chart as well). Set the chart titles as the two row headers respectively.

Directly referenced source actions:

- Action 38: <code>`CLICK` chart icon</code>
- Action 39: <code>`CLICK` Line</code>
- Action 40: <code>`CLICK` icon representing lines only (3rd from the right)</code>

### 3. Copy a contiguous cell range to another column

Skill ID: `37608790-6147-45d0-9f20-1137bb35703d.skill-01`

Procedure:

1. Select the first cell of the source range, then drag to the last cell to select all contiguous cells. For example, select A2 through A22.
2. Press Ctrl+C, click the destination's top cell (for example, B2), and press Ctrl+V.
3. Calc pastes the copied values into the destination range starting at the selected cell.

Efficiency tip: Copy the entire contiguous source range in one drag-and-paste operation rather than copying cells individually; this preserves the original data while creating a working copy.

Source task: `37608790-6147-45d0-9f20-1137bb35703d`

Source instruction: The information are mixed in one field. Help me split them and fill in the columns of First Name, Last Name and Rank

Directly referenced source actions:

- Action 0: <code>`MOVE_TO` A2</code>
- Action 1: <code>`DRAG_TO` A22</code>
- Action 2: <code>`HOTKEY` CTRL-C</code>
- Action 3: <code>`CLICK` on B2</code>
- Action 4: <code>`HOTKEY` CTRL-V</code>

### 4. Create a percentage-change formula using a fixed source sheet

Skill ID: `04d9aeaf-7bed-4024-bedb-e10e6f00eb7f.skill-03`

Procedure:

1. Select the output cell and type a percentage-change formula that subtracts the prior value and divides by that prior value; for example, enter =($Sheet1.B3-$Sheet1.B2)/$Sheet1.B2 in B2, then press Enter.
2. In $Sheet1.B3 and $Sheet1.B2, the $ fixes the source sheet name only. Column B and the row numbers remain relative, so filling the formula downward changes B3/B2 to B4/B3, while the source remains Sheet1.

Efficiency tip: Build the formula once with the intended relative and absolute references before filling it, so propagated formulas adjust correctly without later edits.

Source task: `04d9aeaf-7bed-4024-bedb-e10e6f00eb7f`

Source instruction: In a new sheet with 4 headers "Year", "CA changes", "FA changes", and "OA changes", calculate the percentage annual changes compared to last year in 2015 to 2019 for the Current Assets, Fixed Assets, and Other Assets columns. 

Directly referenced source actions:

- Action 13: <code>`CLICK` cell B2</code>
- Action 14: <code>`TYPING` &#x27;=($Sheet1.B3-$Sheet1.B2)/$Sheet1.B2&#x27;</code>
- Action 15: <code>`PRESS` enter</code>

### 5. Export a spreadsheet as a PDF to a specified path

Skill ID: `aa3a8974-2e85-438b-b29e-a64df44deb4b.skill-02`

Procedure:

1. Open File > Export as PDF.
2. In the file-name field, enter the full output path and PDF filename, such as /home/user/Resize_Cells_Fit_Page.pdf.
3. Click Export to create the PDF at that location.

Efficiency tip: Type the complete destination path and filename directly in the export dialog to avoid navigating folders and to ensure the PDF is saved exactly where required.

Source task: `aa3a8974-2e85-438b-b29e-a64df44deb4b`

Source instruction: I'm working on a project and need to resize cells in a spreadsheet to fit onto one page and export to PDF for efficient presentation. Could you help me on this? Keep the name of PDF the same as the spreadsheet and place it under my home directory.

Directly referenced source actions:

- Action 6: <code>`CLICK` File in the menu bar.</code>
- Action 7: <code>`CLICK` Export as PDF...</code>
- Action 8: <code>`CLICK` file name field</code>
- Action 9: <code>`TYPING` &#x27;/home/user/Resize_Cells_Fit_Page.pdf&#x27;</code>
- Action 10: <code>`CLICK` Export.</code>

## Initial artifact

- Domain: municipal route output monitoring
- Workbook: [initial_artifact.xlsx](artifact/initial_artifact.xlsx)
- Blueprint: [artifact_blueprint.json](artifact/artifact_blueprint.json)
- QA report: [artifact_qa.json](artifact/artifact_qa.json)

Initial state:

- The workbook opens with the Route Review sheet active.
- Daily Metrics!A1:D13 is a complete source table. Its data must remain unchanged throughout the task.
- Route Review!A5:A16 is prepopulated with the same 12 dates as Daily Metrics!A2:A13 so it can serve as the chart category axis.
- Route Review!B5:B16, Route Review!C5:C16, and Route Review!E5:E20 are blank target areas.
- The Daily Change column is already formatted as a percentage with one decimal place, but contains no formulas.
- No charts, filters, copied output-volume values, unique-route results, or PDF export exist initially.

Artifact construction requirements:

- All content is synthetic and contains no personal, customer, or sensitive operational data.
- Use ordinary header styling with bold text and a light fill. Format Date columns as YYYY-MM-DD, Output Volume as integer, and Daily Change as percentage with one decimal place.
- Do not create a chart, a native filter configuration, an exported PDF, or any formulas in the target areas during workbook generation.

| Sheet | Rows | Purpose | Columns |
| --- | ---: | --- | --- |
| Daily Metrics | 12 | Source data for daily route output and route names. | Service Date (date), Output Volume (integer), Crew Hours (integer), Service Route (text) |
| Route Review | 16 | Incomplete review sheet for a copied output series, fixed-sheet daily-change calculations, a distinct route list, and a trend chart. | Service Date (date), Working Output (integer), Daily Change (decimal), Distinct Route Roster (text) |

Must remain incomplete before recording:

- Do not prepopulate the Working Output values on Route Review.
- Do not enter or seed the Daily Change formulas.
- Do not create the unique nonblank route roster in the Route Review sheet.
- Do not create any chart object.
- Do not export a PDF file.

Artifact previews:

### Daily Metrics

![Daily_Metrics.png](artifact/previews/Daily_Metrics.png)

### Route Review

![Route_Review.png](artifact/previews/Route_Review.png)

## Operator guide

### Demonstration 1

- Skill: `abed40dc-063f-4598-8ba5-9fe749c0615d.skill-01`
- Intent: Produce a distinct-route roster from Daily Metrics!D1:D13 that excludes blank route cells, keeps first-occurrence order, and places the copied filter output beginning at Route Review!E5.
- Efficiency: Select the full Service Route source field with its header before opening the filter options, then provide the review-sheet output anchor directly rather than manually copying visible cells.
- Visible success: The roster beginning at E5 contains only North Loop, Harbor Spur, Cedar Link, Ridge Run, Quarry Way, and Canal Point once each (with any copied source header positioned above those results), and no blank roster item appears.

### Demonstration 2

- Skill: `0326d92d-d218-48a8-9ca1-981cd6d064c7.skill-07`
- Intent: Create a trend chart on Route Review that plots Daily Change by Service Date and uses a line without point markers.
- Efficiency: Select the Service Date categories together with the completed Daily Change series, then choose the lines-only subtype during chart insertion instead of modifying a default chart later.
- Visible success: A chart object is visible on Route Review with dates as its category labels and a single continuous Daily Change line that has no data-point markers.

### Demonstration 3

- Skill: `37608790-6147-45d0-9f20-1137bb35703d.skill-01`
- Intent: Copy Daily Metrics!B2:B13 into Route Review!B5:B16 while preserving the original source values.
- Efficiency: Copy the entire 12-cell Output Volume source series in one operation and paste it at the first Working Output cell.
- Visible success: Route Review!B5:B16 matches the 12 Output Volume values from Daily Metrics!B2:B13, while the source column remains present and unchanged.

### Demonstration 4

- Skill: `04d9aeaf-7bed-4024-bedb-e10e6f00eb7f.skill-03`
- Intent: Calculate day-over-day percentage change in Route Review!C6:C16 from consecutive Output Volume values on the fixed Daily Metrics sheet; C5 remains blank because there is no prior day.
- Efficiency: Create the first formula using Daily Metrics as a sheet-fixed reference while leaving the row references relative, then propagate it down the remaining change rows.
- Visible success: C6:C16 displays percentage results, and inspecting formulas shows each uses a fixed Daily Metrics sheet reference while advancing from one source row pair to the next.

### Demonstration 5

- Skill: `aa3a8974-2e85-438b-b29e-a64df44deb4b.skill-02`
- Intent: Export the completed workbook review as a PDF named route_operations_review.pdf at /home/oai/share/route_operations_review.pdf.
- Efficiency: Enter the complete requested PDF destination and filename in the export dialog to avoid ambiguity about the output location.
- Visible success: A PDF export is completed at the requested path after the review sheet shows the copied series, calculation column, roster, and trend chart.

Recording start: Route Review is active with its date axis prefilled but Working Output, Daily Change, and Distinct Route Roster target areas blank; Daily Metrics contains the intact source table and no chart or PDF exists.

Recording end: Route Review visibly contains the copied 12-row Working Output series, percentage Daily Change formulas from C6 through C16, the nonblank distinct route roster beginning at E5, and a lines-only Daily Change trend chart; the PDF has been exported to /home/oai/share/route_operations_review.pdf.

Allowed variation: The expert may use menus, keyboard shortcuts, or equivalent Calc dialogs, and may perform the independent review-sheet operations in any efficient order. Equivalent selection methods are acceptable, provided the resulting values, formulas, filtered roster, lines-only chart, and PDF are visibly correct.

## Expected incidental operations

- **scaffolding:** Select the relevant source and destination ranges, including selecting the date and calculated-change ranges needed as chart data. Reason: Range selection is required to copy the output series, produce the filtered roster, and define the chart categories and series.
- **substantive_prerequisite:** Fill the initial fixed-sheet percentage-change formula down through the remaining populated review dates. Reason: A complete daily-change series is needed for the requested trend chart rather than a calculation in only one row.
- **task_specific:** Use a chart title or other ordinary default chart labeling if needed to make the trend understandable. Reason: This is a minor presentation choice and must not replace the required lines-only chart subtype.

## Source-similarity audit

| Measure | Maximum | Most similar source task |
| --- | ---: | --- |
| Lexical sequence similarity | 0.232911 | 347ef137-7eeb-4c80-a3bb-0951f26a8aff |
| Semantic cosine similarity | 0.435233 | 04d9aeaf-7bed-4024-bedb-e10e6f00eb7f |

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
  --reference-task-id reference-task-calc-full-r01-006
```

The ordinary launcher reads the collected central review file and refuses pending, revision-requested, or rejected tasks.
