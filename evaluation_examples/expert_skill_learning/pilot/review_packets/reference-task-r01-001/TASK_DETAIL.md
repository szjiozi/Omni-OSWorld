# Workshop Enrollment Queue

- Reference task: `reference-task-r01-001`
- Application: `libreoffice_calc`
- Review decision: `pending`

## Task instruction

In the Workshop Enrollment Queue, create a new "Program Registration Counts" summary that shows how many enrollment records each Program has, using Participant Code as the registration measure. Also make Review entries in the Enrollment Log's Queue Flag column stand out with a formula-driven custom pale-amber background (#FCE4D6), while leaving Ready and Confirmed entries unhighlighted.

## Required skills

### 1. Set a Pivot Table value aggregation to Count

Skill ID: `1954cced-e748-45c4-9c26-9855b97fbc5e.skill-04`

Procedure:

1. Double-click the field shown in the Data Fields area to open its data-field settings.
2. Choose the Count aggregation option instead of a numeric summary such as Sum.
3. Confirm the aggregation setting, then confirm the Pivot Table layout to create or update the table.

Efficiency tip: Open the data-field settings immediately after placing a field so its aggregation is correct before finalizing the layout.

Source task: `1954cced-e748-45c4-9c26-9855b97fbc5e`

Source instruction: Create a Pivot Table in a new sheet (Sheet2) to count how many times each "Invoice No." appears.

Directly referenced source actions:

- Action 7: <code>`DOUBLE_CLICK on invoice no. box in data fields</code>
- Action 8: <code>`CLICK` Count</code>
- Action 9: <code>`PRESS` enter</code>
- Action 10: <code>`CLICK` ok</code>

### 2. Create a formula-based conditional formatting rule

Skill ID: `8b1ce5f2-59d2-4dcc-b0b0-666a714b9a14.skill-01`

Procedure:

1. Select the cells to evaluate; for example, press Ctrl+A to select the current sheet’s used range or select a specific calendar range.
2. Open Format > Conditional > Condition.
3. In the condition type drop-down, choose Formula is.
4. Enter a formula that returns TRUE for cells to format. For example, `=AND(WEEKDAY(A1,2)>5,NOT(ISBLANK(A1)))` evaluates weekend dates while excluding blank cells.
5. After assigning or creating the desired style, confirm the conditional-formatting dialog to save the rule. The relative reference `A1` is evaluated relative to each cell in the formatted range.

Efficiency tip: Select the entire target range before opening Conditional Formatting so one rule applies to all cells at once; use relative references such as A1 so Calc evaluates the corresponding cell in each position.

Source task: `8b1ce5f2-59d2-4dcc-b0b0-666a714b9a14`

Source instruction: Given a partial calendar, please highlight all the weekends (Satureday & Sunday) by setting the cell background as red (#ff0000).

Directly referenced source actions:

- Action 0: <code>`HOTKEY` ctrl-A</code>
- Action 1: <code>`CLICK` format</code>
- Action 2: <code>`MOVE_TO` conditional...</code>
- Action 3: <code>`CLICK` condition</code>
- Action 4: <code>`CLICK` cell value dropdown</code>
- Action 5: <code>`CLICK` formula is</code>
- Action 6: <code>`CLICK` formula text field</code>
- Action 7: <code>`TYPING` =AND(WEEKDAY(A1,2)&gt;5, NOT(ISBLANK(A1)))</code>
- Action 14: <code>`CLICK` OK</code>

### 3. Create a custom cell style with a background color

Skill ID: `8b1ce5f2-59d2-4dcc-b0b0-666a714b9a14.skill-02`

Procedure:

1. In the conditional-formatting dialog’s Apply Style control, open the style drop-down and choose New Style.
2. In the style dialog, open the Background settings, then open the color chooser.
3. Choose the required background color; for example, select red (`#ff0000`).
4. Confirm the style dialog with OK so the new style is available for assignment to the conditional rule.

Efficiency tip: Create a custom style from the conditional-format dialog rather than manually filling cells; the same style can then be reused by other conditional rules.

Source task: `8b1ce5f2-59d2-4dcc-b0b0-666a714b9a14`

Source instruction: Given a partial calendar, please highlight all the weekends (Satureday & Sunday) by setting the cell background as red (#ff0000).

Directly referenced source actions:

- Action 8: <code>`CLICK` Apply style dropdown</code>
- Action 9: <code>`CLICK` New Style...</code>
- Action 10: <code>`CLICK` Background</code>
- Action 11: <code>`CLICK` Color</code>
- Action 12: <code>`CLICK` red</code>
- Action 13: <code>`CLICK` OK</code>

## Initial artifact

- Domain: community workshop enrollment coordination
- Workbook: [initial_artifact.xlsx](artifact/initial_artifact.xlsx)
- Blueprint: [artifact_blueprint.json](artifact/artifact_blueprint.json)
- QA report: [artifact_qa.json](artifact/artifact_qa.json)

Initial state:

- The workbook opens with Enrollment Log as the active sheet.
- Enrollment Log contains a contiguous, filter-free data table in A1:G29 with no blank rows or blank columns inside the table.
- Session Date is formatted as a date, while identifiers and categorical fields are text.
- There is no pre-existing summary sheet, pivot table, native conditional-format rule, or custom pale-amber cell style.
- The Queue Flag column is visible and contains the Review, Ready, and Confirmed values described in the generation notes.

Artifact construction requirements:

- Create a privacy-safe synthetic workbook titled "Workshop Enrollment Queue".
- Populate the Enrollment Log sheet with 28 data rows plus a header row. Use unique synthetic participant codes P-1001 through P-1028; all Participant Code cells must be nonblank text.
- Use four Program values with these exact record totals: Community Garden (8), Digital Basics (7), First Aid (6), and Resume Lab (7). Arrange the rows in a mixed order rather than grouping by Program.
- Use plausible 2026 session dates, neighborhood names, and Attendance Type values such as In Person, Online, and Waitlist.
- Set Queue Flag to "Review" for exactly 8 records distributed across at least three programs; set the remaining records to "Ready" or "Confirmed". Include at least two different non-Review values.
- Apply ordinary header styling and date formatting only. Do not create a pivot table, conditional-formatting rule, or custom colored cell style required by the task.

| Sheet | Rows | Purpose | Columns |
| --- | ---: | --- | --- |
| Enrollment Log | 28 | Synthetic enrollment records for community workshops and queue review. | Registration ID (text), Program (text), Session Date (date), Participant Code (text), Neighborhood (text), Attendance Type (text), Queue Flag (text) |

Must remain incomplete before recording:

- Do not pre-create the Program Registration Counts sheet or any pivot output.
- Do not apply conditional formatting to Queue Flag or any other range.
- Do not create a custom style with the required pale-amber background before the recorded task.

Artifact previews:

### Enrollment Log

![Enrollment_Log.png](artifact/previews/Enrollment_Log.png)

## Operator guide

### Demonstration 1

- Skill: `1954cced-e748-45c4-9c26-9855b97fbc5e.skill-04`
- Intent: Build a program-level registration summary on a new sheet, grouping the enrollment records by Program and counting nonblank Participant Code entries rather than totaling any numeric field.
- Efficiency: After adding Participant Code to the pivot values, open its value settings immediately and set the summary type before confirming the pivot layout.
- Visible success: The new summary shows one row for each of the four programs with counts 8, 7, 6, and 7, for a total of 28 registrations.

### Demonstration 2

- Skill: `8b1ce5f2-59d2-4dcc-b0b0-666a714b9a14.skill-01`
- Intent: Apply one formula-based conditional-formatting rule to Queue Flag cells that evaluates true only when the corresponding flag is Review.
- Efficiency: Select the full Queue Flag data range first and use a row-relative formula such as =G2="Review" so the same rule evaluates each flag cell.
- Visible success: All and only the eight Queue Flag cells containing Review receive the conditional appearance; Ready and Confirmed cells remain unchanged.

### Demonstration 3

- Skill: `8b1ce5f2-59d2-4dcc-b0b0-666a714b9a14.skill-02`
- Intent: Create and assign a new custom style with a pale amber background (#FCE4D6) for the Review condition.
- Efficiency: Create the style from the conditional-formatting workflow so it can be assigned directly to the formula rule instead of manually coloring individual cells.
- Visible success: The Review cells visibly have the new pale-amber fill, and the assigned formatting is a reusable custom style rather than direct cell formatting.

Recording start: The workbook opens on Enrollment Log with the raw 28-row enrollment table and no pivot table, conditional-formatting rule, or required custom style.

Recording end: A new Program Registration Counts sheet contains a pivot summary that counts Participant Code registrations by Program, and Enrollment Log Queue Flag cells with Review are conditionally filled pale amber using a newly created custom style.

Allowed variation: The operator may create the summary sheet before or during pivot creation and may use any equivalent Calc dialogs or menus. The custom style may be named freely, provided it is newly created for the rule and has the specified pale-amber background.

## Expected incidental operations

- **substantive_prerequisite:** Create a new worksheet to hold the program-level registration summary. Reason: A separate destination is needed for the requested pivot-based summary.
- **substantive_prerequisite:** Select the Enrollment Log data and arrange Program as the grouping field and Participant Code as the value field in a pivot layout. Reason: These are the minimum pivot setup actions needed before the value aggregation can be set to Count.
- **scaffolding:** Select the Queue Flag data cells before defining the conditional formatting rule. Reason: The formula-based rule must have a target range containing the queue-status values.

## Source-similarity audit

| Measure | Maximum | Most similar source task |
| --- | ---: | --- |
| Lexical sequence similarity | 0.204633 | 8b1ce5f2-59d2-4dcc-b0b0-666a714b9a14 |
| Semantic cosine similarity | 0.319971 | 8b1ce5f2-59d2-4dcc-b0b0-666a714b9a14 |

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
  --reference-task-id reference-task-r01-001
```

The ordinary launcher reads the collected central review file and refuses pending, revision-requested, or rejected tasks.
