# Garden Volunteer Activity Tracker

- Reference task: `reference-task-calc-full-r01-019`
- Application: `libreoffice_calc`
- Review decision: `pending`

## Task instruction

Complete the Garden Volunteer Activity tracker by calculating each volunteer’s completed years of service from their enrollment date, presenting attendance as percentages, and standardizing all soil readings to two displayed decimal places.

## Required skills

### 1. Enter a date-difference formula that returns whole years

Skill ID: `4e6fcf72-daf3-439f-a232-c434ce416af6.skill-01`

Procedure:

1. Select the first output cell beside the date column, for example D2.
2. Type a formula such as `=DATEDIF(C2,TODAY(),"Y")` and press Enter. `C2` is a relative reference, so it can adjust to each row when propagated later.
3. The `"Y"` unit returns completed whole years between the date in C2 and the current date.

Efficiency tip: Enter the formula once in the first result cell, then use a propagation command such as the fill handle rather than retyping it for each row.

Source task: `4e6fcf72-daf3-439f-a232-c434ce416af6`

Source instruction: Please calculate the ages of the employees according to their birthday.

Directly referenced source actions:

- Action 0: <code>`CLICK` on the first table cell of the column &#x27;Age&#x27;, D2</code>
- Action 1: <code>`TYPING` the formula `=DATEDIF(C2,TODAY(),&quot;Y&quot;)` where &#x27;C2&#x27; is the column containing the first employee&#x27;s birthdate</code>
- Action 2: <code>`PRESS` &#x27;Enter</code>

### 2. Increase displayed decimal places for an entire column

Skill ID: `6e99a1ad-07d2-4b66-a1ce-ece6d99c20a5.skill-01`

Procedure:

1. Click the column header for the numeric column to select the whole column; for example, click column C.
2. Use the toolbar’s Increase Decimal button to add displayed decimal places. Each activation increases the displayed precision by one decimal place; double-click it when two additional places are needed.
3. For example, a value displayed as 12 can be shown as 12.00 after increasing the decimal places twice. This changes display formatting, not the stored numeric value.

Efficiency tip: Select the entire column first so one formatting command updates all existing values and cells entered later, instead of adjusting decimal places cell by cell.

Source task: `6e99a1ad-07d2-4b66-a1ce-ece6d99c20a5`

Source instruction: Help me format column "spent" by keeping two decimal points. 

Directly referenced source actions:

- Action 0: <code>`CLICK` column C.</code>
- Action 1: <code>`DOUBLE_CLICK` the &#x27;Increase Decimal&#x27; button.</code>

### 3. Apply percentage number formatting to a cell range

Skill ID: `04d9aeaf-7bed-4024-bedb-e10e6f00eb7f.skill-06`

Procedure:

1. Select the cells containing ratio or change results; for example, drag from B2 to D6.
2. Click the Percent (%) button on the formatting toolbar. Calc displays the selected numeric values as percentages while retaining their underlying values.

Efficiency tip: Select the entire result range before applying the format so all existing values use one consistent number format.

Source task: `04d9aeaf-7bed-4024-bedb-e10e6f00eb7f`

Source instruction: In a new sheet with 4 headers "Year", "CA changes", "FA changes", and "OA changes", calculate the percentage annual changes compared to last year in 2015 to 2019 for the Current Assets, Fixed Assets, and Other Assets columns. 

Directly referenced source actions:

- Action 25: <code>`CLICK` cell B2</code>
- Action 26: <code>`DRAG_TO` D6</code>
- Action 27: <code>`CLICK` percent symbol</code>

### 4. Autofill a formula down a contiguous adjacent data range

Skill ID: `a9f325aa-8c05-4e4f-8341-9e4358565f4f.skill-02`

Procedure:

1. Select the cell containing the completed formula, such as C2.
2. Move to the small square at the cell's bottom-right corner (the fill handle) and double-click it.
3. Calc fills the formula downward for the contiguous rows detected in the neighboring data column, adjusting relative references; for example, `B2` becomes `B3`, `B4`, and so on.

Efficiency tip: Double-clicking the fill handle is faster than dragging it through a long contiguous data block; verify that the adjacent source column has no unintended blank rows, because blanks can limit propagation.

Source task: `a9f325aa-8c05-4e4f-8341-9e4358565f4f`

Source instruction: I want to copy the movie titles in 'Garbage Movie Titles' column to the 'Clean Movie Titles' column. But please remove the adundant whitespaces and canonicalize the letter cases by capitalizing the first letter of each words and leave other letters as lower case.

Directly referenced source actions:

- Action 3: <code>`CLICK C2</code>
- Action 4: <code>`DOUBLE_CLICK` bottom right corner of the cell</code>

## Initial artifact

- Domain: Community garden volunteer activity tracker
- Workbook: [initial_artifact.xlsx](artifact/initial_artifact.xlsx)
- Blueprint: [artifact_blueprint.json](artifact/artifact_blueprint.json)
- QA report: [artifact_qa.json](artifact/artifact_qa.json)

Initial state:

- The workbook opens on the "Volunteer Activity" sheet.
- The data block is contiguous with no blank records between rows 2 and 25.
- The Enrollment Date column is immediately adjacent to the blank Completed Years column, enabling formula propagation based on the contiguous records.
- No percentage formatting has been applied to Attendance Ratio.
- No two-decimal display format has been applied to Soil Reading.
- No formulas exist in Completed Years.

Artifact construction requirements:

- All names, garden zones, dates, and metrics must be synthetic and privacy-safe.
- Create one worksheet named "Volunteer Activity" with a simple bold header row and 24 contiguous data rows (rows 2-25).
- Store Enrollment Date as real spreadsheet date values in ISO-style display format such as YYYY-MM-DD.
- Store Attendance Ratio as numeric decimal fractions, not text (for example, 0.875). Leave its initial number format as General.
- Store Soil Reading as numeric values, including a mixture of whole numbers and values with one decimal place. Leave its initial number format as General so it does not already display two decimal places.
- Leave Completed Years blank for all data rows; do not seed formulas in that column.
- Use enrollment dates safely in the past, between 2013 and 2023, so whole-year results are nonnegative and meaningful relative to TODAY().

| Sheet | Rows | Purpose | Columns |
| --- | ---: | --- | --- |
| Volunteer Activity | 24 | Track synthetic volunteer participation and garden measurement records requiring tenure calculation and presentation formatting. | Volunteer Code (text), Garden Zone (text), Enrollment Date (date), Completed Years (integer), Attendance Ratio (decimal), Soil Reading (decimal) |

Must remain incomplete before recording:

- Completed Years must remain blank until the recorded task.
- Attendance Ratio must not be preformatted as percentages.
- Soil Reading must not be preformatted to two decimal places.
- Do not include charts, pivot tables, conditional formatting, or additional worksheets.

Artifact previews:

### Volunteer Activity

![Volunteer_Activity.png](artifact/previews/Volunteer_Activity.png)

## Operator guide

### Demonstration 1

- Skill: `4e6fcf72-daf3-439f-a232-c434ce416af6.skill-01`
- Intent: In the first Completed Years cell, enter a DATEDIF-based formula that calculates completed whole years from that row's Enrollment Date through TODAY().
- Efficiency: Enter the formula only once with a relative reference to the first enrollment date; avoid manually calculating each volunteer's tenure.
- Visible success: The first Completed Years result displays a nonnegative whole-number tenure, while the formula bar shows a date-difference formula using the whole-years unit.

### Demonstration 2

- Skill: `a9f325aa-8c05-4e4f-8341-9e4358565f4f.skill-02`
- Intent: Propagate the completed-years formula from the first result cell through every populated volunteer record.
- Efficiency: Use the fill handle's double-click behavior or an equivalent fill-down command, because the neighboring records are contiguous.
- Visible success: Every Completed Years cell from row 2 through row 25 contains a result, and row-relative date references are evident when different filled cells are selected.

### Demonstration 3

- Skill: `04d9aeaf-7bed-4024-bedb-e10e6f00eb7f.skill-06`
- Intent: Display each attendance ratio as a percentage.
- Efficiency: Select all populated Attendance Ratio cells as one range before applying the number format.
- Visible success: Values formerly shown as fractions such as 0.875 visibly display with percent signs, such as 88% or 87.5%, while retaining their values.

### Demonstration 4

- Skill: `6e99a1ad-07d2-4b66-a1ce-ece6d99c20a5.skill-01`
- Intent: Increase the displayed decimal precision for the Soil Reading column until values consistently show two decimal places.
- Efficiency: Format the entire Soil Reading column in one action sequence rather than modifying individual cells.
- Visible success: All displayed Soil Reading values, including whole-number entries, show two digits after the decimal separator (for example, 8.00 and 7.50).

Recording start: The workbook is open with the 24-row Volunteer Activity table visible; Completed Years is empty, Attendance Ratio is shown as raw decimal fractions, and Soil Reading is in General format.

Recording end: The Volunteer Activity sheet shows calculated whole completed years for every record, percentage-formatted Attendance Ratio cells, and Soil Reading displayed uniformly with two decimal places.

Allowed variation: The expert may use toolbar controls, menu commands, keyboard shortcuts, or another equivalent Calc method. Formula propagation may use a fill handle or an equivalent fill-down command, provided the relative formula is visibly extended through the contiguous records.

## Expected incidental operations

- **scaffolding:** Select the first blank result cell under Completed Years before entering the formula. Reason: A starting output cell is required to establish the relative-reference formula.
- **scaffolding:** Select the contiguous Attendance Ratio data cells before applying percentage formatting. Reason: The percentage format should apply consistently to the full populated result range.
- **scaffolding:** Select the Soil Reading column before changing displayed decimal precision. Reason: Column-wide selection ensures the requested numeric display convention applies to all existing values.

## Source-similarity audit

| Measure | Maximum | Most similar source task |
| --- | ---: | --- |
| Lexical sequence similarity | 0.295699 | 12382c62-0cd1-4bf2-bdc8-1d20bf9b2371 |
| Semantic cosine similarity | 0.370169 | 04d9aeaf-7bed-4024-bedb-e10e6f00eb7f |

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
  --reference-task-id reference-task-calc-full-r01-019
```

The ordinary launcher reads the collected central review file and refuses pending, revision-requested, or rejected tasks.
