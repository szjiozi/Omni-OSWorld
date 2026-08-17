# Dispatch Route Review

- Reference task: `reference-task-r01-003`
- Application: `libreoffice_calc`
- Review decision: `pending`

## Task instruction

Build a delivery route review dashboard: add and name a new worksheet "Route Dashboard", create a list of route-and-tracking tags from the Dispatch Log for every dispatch, and include a Pivot Table showing the number of tracking codes handled by each carrier.

## Required skills

### 1. Rename a worksheet tab

Skill ID: `1954cced-e748-45c4-9c26-9855b97fbc5e.skill-05`

Procedure:

1. Double-click the worksheet tab to enter tab-name editing mode.
2. Type the replacement name, for example `Sheet2`, and press Enter to apply it.

Efficiency tip: Rename a newly created sheet immediately while its tab is active, so later formulas and references can use a meaningful sheet name.

Source task: `1954cced-e748-45c4-9c26-9855b97fbc5e`

Source instruction: Create a Pivot Table in a new sheet (Sheet2) to count how many times each "Invoice No." appears.

Directly referenced source actions:

- Action 11: <code>`DOUBLE_CLICK` Pivot Table Sheet1_1</code>
- Action 12: <code>`TYPING` Sheet2</code>
- Action 13: <code>`PRESS` enter</code>

### 2. Insert a new worksheet from the sheet tab bar

Skill ID: `035f41ba-6653-43ab-aa63-c86d449d62e5.skill-04`

Procedure:

1. Click the plus button beside the existing worksheet tabs; for example, use the plus control next to Sheet1 to add a blank sheet.
2. Calc creates and activates a new worksheet, ready for cell entry.

Efficiency tip: Use the sheet-tab plus button to add a worksheet immediately, without opening a worksheet-management dialog.

Source task: `035f41ba-6653-43ab-aa63-c86d449d62e5`

Source instruction: Help me fill in the Gross profit column by subtracting all the available expenses including discounts, allowances, material and labor charges, and overhead from the actual sale, i.e., the sales after deducting the returns. Then under column A named "Year_Profit" in a new sheet, display the Year Column in Sheet 1 as text appended by a "_" with the corresponding integer digits of Gross Profit value.

Directly referenced source actions:

- Action 5: <code>`CLICK` on + to left of sheet1</code>

### 3. Fill a formula down using the fill handle

Skill ID: `035f41ba-6653-43ab-aa63-c86d449d62e5.skill-03`

Procedure:

1. Select the cell containing the formula to propagate, such as J2 or A2.
2. Move to the small square at the selection's bottom-right corner until the fill-handle cursor is available.
3. Drag the handle down to the final target row, for example from row 2 through row 10.
4. Calc copies the formula into each row and adjusts relative row references automatically.

Efficiency tip: Drag the fill handle directly to the last adjacent row of data rather than copying and pasting formulas one row at a time.

Source task: `035f41ba-6653-43ab-aa63-c86d449d62e5`

Source instruction: Help me fill in the Gross profit column by subtracting all the available expenses including discounts, allowances, material and labor charges, and overhead from the actual sale, i.e., the sales after deducting the returns. Then under column A named "Year_Profit" in a new sheet, display the Year Column in Sheet 1 as text appended by a "_" with the corresponding integer digits of Gross Profit value.

Directly referenced source actions:

- Action 3: <code>`MOVE_TO` bottom right corner of the cell J2`</code>
- Action 4: <code>`DRAG_TO` bottom right corner of the cell J10</code>
- Action 9: <code>`MOVE_TO` bottom right corner of the cell A2`</code>
- Action 10: <code>`DRAG_TO` bottom right corner of the cell A10</code>

### 4. Add a field as a Pivot Table value

Skill ID: `1954cced-e748-45c4-9c26-9855b97fbc5e.skill-03`

Procedure:

1. Locate the field in the Available Fields list in the Pivot Table layout dialog.
2. Drag it to the Data Fields area. For example, adding an identifier field as a data field creates a value summary for each row-label group.

Efficiency tip: Use the same source field in both Row Fields and Data Fields when you need a grouped list together with a summary of each group.

Source task: `1954cced-e748-45c4-9c26-9855b97fbc5e`

Source instruction: Create a Pivot Table in a new sheet (Sheet2) to count how many times each "Invoice No." appears.

Directly referenced source actions:

- Action 5: <code>`MOVE_TO` invoice no. in available fields box</code>
- Action 6: <code>`DRAG_TO` data fields box</code>

### 5. Concatenate cross-sheet cell values in a formula

Skill ID: `035f41ba-6653-43ab-aa63-c86d449d62e5.skill-05`

Procedure:

1. In the destination cell, enter a concatenation formula that joins source values with text separators. For example, type `=$Sheet1.A2&"_"&$Sheet1.J2`.
2. The `&` operator joins the two references and the quoted underscore literal into one text result.
3. In `$Sheet1.A2`, the `$` fixes the source sheet name `Sheet1`; column A and row 2 remain relative, so filling downward changes it to `$Sheet1.A3`. The same behavior applies to `$Sheet1.J2`.

Efficiency tip: Reference the source sheet directly in the formula so the result updates automatically when the source values change.

Source task: `035f41ba-6653-43ab-aa63-c86d449d62e5`

Source instruction: Help me fill in the Gross profit column by subtracting all the available expenses including discounts, allowances, material and labor charges, and overhead from the actual sale, i.e., the sales after deducting the returns. Then under column A named "Year_Profit" in a new sheet, display the Year Column in Sheet 1 as text appended by a "_" with the corresponding integer digits of Gross Profit value.

Directly referenced source actions:

- Action 8: <code>`TYPING` &#x27;=$Sheet1.A2&amp;&quot;_&quot;&amp;$Sheet1.J2&#x27;</code>

## Initial artifact

- Domain: regional delivery dispatches
- Workbook: [initial_artifact.xlsx](artifact/initial_artifact.xlsx)
- Blueprint: [artifact_blueprint.json](artifact/artifact_blueprint.json)
- QA report: [artifact_qa.json](artifact/artifact_qa.json)

Initial state:

- The workbook opens with exactly one visible worksheet named "Dispatch Log".
- Dispatch Log contains the source table in A1:E31, with headers in row 1 and 30 populated records in rows 2:31.
- No additional worksheet exists when the workbook opens.
- No Pivot Table exists anywhere in the workbook.
- No cross-sheet tag formula or filled-down formula results exist anywhere in the workbook.

Artifact construction requirements:

- Use entirely synthetic, privacy-safe dispatch records with fictional carrier names, route labels, and tracking codes.
- Create one formatted data table with a bold header row and 30 dispatch-record rows. Use ordinary spreadsheet styling only; do not create a Pivot Table or conditional-format rules.
- Use tracking codes such as TRK-4101 through TRK-4130, with repeated carrier names across records so a count-by-carrier Pivot Table is meaningful.
- Use route labels such as North Loop, Harbor Run, Central Link, and West Ridge. Include dates within a single fictional month and parcel counts from 1 to 8.

| Sheet | Rows | Purpose | Columns |
| --- | ---: | --- | --- |
| Dispatch Log | 30 | Source dispatch records for a delivery operations dashboard. | Dispatch Date (date), Carrier (text), Tracking Code (text), Route (text), Parcel Count (integer) |

Must remain incomplete before recording:

- Do not pre-create the dashboard worksheet that the operator must insert and rename.
- Do not pre-create the carrier-count Pivot Table.
- Do not pre-populate the route/tracking tag column or its formulas.

Artifact previews:

### Dispatch Log

![Dispatch_Log.png](artifact/previews/Dispatch_Log.png)

## Operator guide

### Demonstration 1

- Skill: `035f41ba-6653-43ab-aa63-c86d449d62e5.skill-04`
- Intent: Insert a blank worksheet to hold the delivery review dashboard.
- Efficiency: Use the plus control at the sheet-tab bar so the blank dashboard sheet is created directly in the workbook.
- Visible success: A new blank worksheet tab is visible and active beside Dispatch Log.

### Demonstration 2

- Skill: `1954cced-e748-45c4-9c26-9855b97fbc5e.skill-05`
- Intent: Rename the inserted worksheet to "Route Dashboard".
- Efficiency: Rename the newly active tab before creating formulas or reports so the dashboard has a meaningful, stable name.
- Visible success: The active worksheet tab visibly reads "Route Dashboard".

### Demonstration 3

- Skill: `035f41ba-6653-43ab-aa63-c86d449d62e5.skill-05`
- Intent: Create the first Route Dashboard tag by concatenating the Dispatch Log Route and Tracking Code values with a readable separator, then use the fill handle to extend it through all 30 dispatch rows.
- Efficiency: Use a formula with a fixed source-sheet reference and relative row references, such as joining Route and Tracking Code, so the copied rows update automatically.
- Visible success: The first tag displays both source values as one text label, and the completed tag column contains corresponding route/tracking labels for rows 2 through 31.

### Demonstration 4

- Skill: `035f41ba-6653-43ab-aa63-c86d449d62e5.skill-03`
- Intent: Propagate the initial cross-sheet tag formula down the full dispatch-record list using the fill handle.
- Efficiency: Drag the first formula cell's fill handle directly to the last adjacent dispatch row instead of copying formulas row by row.
- Visible success: Each filled tag row has adjusted source-row references and no manual repeated formula entry is needed.

### Demonstration 5

- Skill: `1954cced-e748-45c4-9c26-9855b97fbc5e.skill-03`
- Intent: In the Pivot Table layout, add Tracking Code as a value/data field for the carrier summary.
- Efficiency: After Carrier has been used as the grouping field, add Tracking Code to the data area to produce a count summary for each carrier.
- Visible success: The Pivot Table visibly shows carrier groups with a numeric Tracking Code count/value column.

Recording start: The workbook contains only the populated Dispatch Log source sheet, with no dashboard sheet, Pivot Table, or tag formulas.

Recording end: Route Dashboard is a renamed inserted worksheet containing a filled list of cross-sheet route/tracking tags and a non-overlapping Pivot Table that summarizes Tracking Code counts by Carrier.

Allowed variation: The expert may place the tag list and Pivot Table in any non-overlapping regions of the new worksheet, use an equivalent Calc-supported method to open the Pivot Table layout, and use a semantically equivalent separator in the concatenated tag formula.

## Expected incidental operations

- **substantive_prerequisite:** Create a Pivot Table from the Dispatch Log source range and place it on the newly inserted dashboard worksheet. Reason: A Pivot Table container is required before its fields can be arranged.
- **substantive_prerequisite:** Place Carrier in the Pivot Table row fields. Reason: Carrier groups are needed so the Tracking Code value summary is interpretable as a count by carrier.
- **task_specific:** Enter a descriptive header for the route/tracking tags and position that helper list away from the Pivot Table output. Reason: This makes the concatenated cross-sheet results understandable and avoids overlapping the Pivot Table.
- **task_specific:** Enter the first cross-sheet concatenation formula referencing Route and Tracking Code from Dispatch Log before filling it down. Reason: The fill-handle operation needs an initial relative-reference formula to propagate.

## Source-similarity audit

| Measure | Maximum | Most similar source task |
| --- | ---: | --- |
| Lexical sequence similarity | 0.268041 | 8b1ce5f2-59d2-4dcc-b0b0-666a714b9a14 |
| Semantic cosine similarity | 0.329174 | 1954cced-e748-45c4-9c26-9855b97fbc5e |

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
  --reference-task-id reference-task-r01-003
```

The ordinary launcher reads the collected central review file and refuses pending, revision-requested, or rejected tasks.
