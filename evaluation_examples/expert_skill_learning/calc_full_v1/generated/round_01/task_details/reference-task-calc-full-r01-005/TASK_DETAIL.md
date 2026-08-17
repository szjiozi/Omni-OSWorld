# Replenishment Review

- Reference task: `reference-task-calc-full-r01-005`
- Application: `libreoffice_calc`
- Review decision: `pending`

## Task instruction

Prepare the replenishment review workbook for management: classify every dispatch record from the SKU catalog, create seven-digit ticket-code displays, flag the single largest restock cost, sort the complete dispatch log by SKU from A to Z, and show the total units dispatched on the Summary sheet.

## Required skills

### 1. Enter an exact-match VLOOKUP formula

Skill ID: `7e429b8d-a3f0-4ed0-9b58-08957d00b127.skill-01`

Procedure:

1. Select the destination cell where the lookup result should appear.
2. Type a VLOOKUP formula that uses a lookup key, a table range, the return-column number, and `FALSE` for an exact match. For example, enter `=VLOOKUP(E2,$A$2:$B$7,2,FALSE)` to find the value from E2 in the first column of the fixed A2:B7 table and return the matching value from its second column.
3. Press Enter to commit the formula. In `$A$2:$B$7`, the `$` before each column and row fixes both columns and rows when the formula is filled.

Efficiency tip: Use absolute references such as `$A$2:$B$7` for a fixed lookup table so the table range does not shift when the formula is copied to other rows.

Source task: `7e429b8d-a3f0-4ed0-9b58-08957d00b127`

Source instruction: I have a lookup table for the officers of each branch. Please, here is another table in which I need to fill with the officer names according the headoffice (i.e., the branch name). Help me to complete this.

Directly referenced source actions:

- Action 0: <code>`CLICK` F2</code>
- Action 1: <code>`TYPING` =VLOOKUP(E2, $A$2:$B$7, 2, FALSE)</code>
- Action 2: <code>`PRESS` Enter.</code>

### 2. Configure a formula-based conditional formatting rule

Skill ID: `21ab7b40-77c2-4ae6-8321-e00d3a086c73.skill-04`

Procedure:

1. With the intended result range active, open Format > Conditional > Condition.
2. Change the condition type from a cell-value comparison to `Formula is`.
3. Enter a Boolean formula that tests the current row. For example, use `$C2=MAX($C$2:$C$25)` to test whether each cell in column C equals the maximum of C2:C25.
4. In this example, `$C2` fixes column C but leaves row 2 relative, so the row changes as the rule is evaluated down the range. `$C$2:$C$25` fixes both the column and rows for the maximum range.
5. After choosing or creating the desired style, confirm the conditional-formatting dialog to save the rule.

Efficiency tip: Use a relative row reference in the condition formula so one rule can evaluate every row in the selected range, rather than creating a separate rule per cell.

Source task: `21ab7b40-77c2-4ae6-8321-e00d3a086c73`

Source instruction: Please calculate the period rate for my data in a new column with header "Period Rate (%)", convert the results as number type, and highlight the highest result with green (#00ff00) font.

Directly referenced source actions:

- Action 8: <code>`CLICK` format</code>
- Action 9: <code>`MOVE_TO` &#x27;conditional...&#x27;</code>
- Action 10: <code>`CLICK` &#x27;condition&#x27;</code>
- Action 11: <code>`CLICK` &#x27;cell value&#x27; dropdown</code>
- Action 12: <code>`CLICK` &#x27;Formula is&#x27; option</code>
- Action 13: <code>`CLICK` text field</code>
- Action 14: <code>`TYPING` $C2=MAX($C$2:$C$25)</code>
- Action 24: <code>`CLICK` OK</code>

### 3. Format a numeric cell value as fixed-width text with leading zeros

Skill ID: `0bf05a7d-b28b-44d2-955a-50b41e24012a.skill-01`

Procedure:

1. Select the destination cell and enter a TEXT formula that references the source cell with a zero-only number format.
2. For example, enter `=TEXT(C2,"0000000")` in D2 to display the value from C2 as seven digits, adding leading zeros when necessary.
3. The result is text, so use this method when a fixed-width identifier-like display is needed rather than a numeric value for later arithmetic.

Efficiency tip: Enter the formula once in the first destination cell, then propagate it rather than manually editing each value.

Source task: `0bf05a7d-b28b-44d2-955a-50b41e24012a`

Source instruction: I would like to copy all the numbers in the 'Old ID' column to the 'New 7 Digit Id' column, and pad them with zeros in front, to fill them up to seven digits.

Directly referenced source actions:

- Action 0: <code>`DOUBLE_CLICK` cell D2</code>
- Action 1: <code>`TYPING` &#x27;=TEXT(C2,&quot;0000000&quot;)&#x27; in the formula bar</code>

### 4. Build a cross-sheet range-total formula

Skill ID: `26a8440e-c166-4c50-aef4-bfb77314b46b.skill-03`

Procedure:

1. Select the destination cell and type a formula that totals a range on another worksheet, for example `=SUM($Sheet1.B2:B11)`, then press Enter.
2. In `$Sheet1.B2:B11`, the `$` before `Sheet1` fixes the source sheet only. Column B and rows 2 through 11 remain relative, so they can adjust when the formula is filled to another location.
3. Use the same pattern with any source sheet and source range, such as `=SUM($Data.C2:C20)`.

Efficiency tip: Enter the formula once in the first result cell, then use autofill separately to propagate the relative references instead of manually editing equivalent formulas.

Source task: `26a8440e-c166-4c50-aef4-bfb77314b46b`

Source instruction: Create a table with two column headers ("Month" and "Total") in a new sheet named "Sheet2" to show the total sales for all months.

Directly referenced source actions:

- Action 12: <code>`CLICK` cell B2</code>
- Action 13: <code>`TYPING` &#x27;=SUM($Sheet1.B2:B11)&#x27;</code>
- Action 14: <code>`PRESS` enter</code>

### 5. Sort a full table by a column in ascending order

Skill ID: `3a7c8185-25c1-4941-bd7b-96e823c9f21f.skill-01`

Procedure:

1. Click the header of the column that should control the ordering, such as column A, to select the entire column.
2. Click the ascending-sort toolbar icon (A–Z with a downward arrow).
3. If Calc asks whether to extend the selection, choose “Extend selection” so values in adjacent columns move together with their original rows.

Efficiency tip: Select a cell or the full key column before using the toolbar sort button; when Calc offers to extend the selection, choose it so every row stays intact rather than sorting just one column.

Source task: `3a7c8185-25c1-4941-bd7b-96e823c9f21f`

Source instruction: Sort the data according to column A in an ascending order and then create a line chart with the "Date Time" column on the X-axis and quantity on the Y-axis.

Directly referenced source actions:

- Action 0: <code>`CLICK` on the A grey cell to select the entire column</code>
- Action 1: <code>`CLICK` the ascending sort icon az with the down arrow</code>
- Action 2: <code>`CLICK` extend selection</code>

## Initial artifact

- Domain: warehouse replenishment review
- Workbook: [initial_artifact.xlsx](artifact/initial_artifact.xlsx)
- Blueprint: [artifact_blueprint.json](artifact/artifact_blueprint.json)
- QA report: [artifact_qa.json](artifact/artifact_qa.json)

Initial state:

- Catalog contains a two-column lookup table with headers SKU and Supply Group and eight populated data rows.
- Dispatch_Log contains 18 populated, intentionally non-alphabetical operational rows with headers Ticket Number, SKU, Units Dispatched, Restock Cost, Supply Group, and Ticket Code. Columns E and F are entirely blank beneath their headers.
- Summary is present with its metric labels, but the value for Total Units Dispatched is blank.
- No conditional formatting exists anywhere in the workbook, and Dispatch_Log is not sorted by SKU.

Artifact construction requirements:

- Create a synthetic, privacy-safe workbook titled "Replenishment Review" with the three sheets listed below. Use only fictional SKU codes, categories, and numeric operational data.
- Catalog values, rows 2-9: (SKU-104, Fasteners), (SKU-118, Safety), (SKU-203, Packaging), (SKU-217, Adhesives), (SKU-305, Hand Tools), (SKU-322, Electrical), (SKU-411, Cleaning), (SKU-426, Storage).
- Dispatch_Log rows 2-19 should contain these unsorted records in columns A-D: (4821, SKU-305, 14, 238.50), (930, SKU-104, 60, 84.00), (17654, SKU-426, 8, 416.00), (7210, SKU-217, 25, 187.50), (365, SKU-203, 90, 135.00), (11902, SKU-322, 12, 324.00), (2548, SKU-118, 18, 270.00), (8061, SKU-411, 35, 157.50), (402, SKU-104, 40, 56.00), (14870, SKU-305, 9, 153.00), (6103, SKU-203, 120, 180.00), (996, SKU-426, 5, 260.00), (21509, SKU-217, 30, 225.00), (7334, SKU-322, 20, 540.00), (1876, SKU-118, 10, 150.00), (320, SKU-411, 22, 99.00), (16801, SKU-305, 16, 272.00), (5097, SKU-203, 75, 112.50). The highest Restock Cost is the unique value 540.00.
- Format Dispatch_Log column D as currency with two decimal places. Make all headers bold with a modest fill color; otherwise keep styling ordinary. Keep Ticket Number in column A as numeric General format so the requested leading-zero text result is visibly distinct.
- Summary should have values/labels in A1:B3: (Metric, Value), (Total Units Dispatched, blank), (Review Note, "Highest restock cost is flagged in Dispatch_Log"). B2 must be blank initially and have no formula.
- Do not add any formulas, conditional-formatting rules, filters, tables, pivot tables, charts, or pre-applied sort state beyond the ordinary input tables.

| Sheet | Rows | Purpose | Columns |
| --- | ---: | --- | --- |
| Catalog | 8 | Reference table used to classify replenishment SKUs. | SKU (text), Supply Group (text) |
| Dispatch_Log | 18 | Unsorted replenishment dispatch records requiring classification, ticket-code display values, ordering, and an exception highlight. | Ticket Number (integer), SKU (text), Units Dispatched (integer), Restock Cost (currency), Supply Group (text), Ticket Code (text) |
| Summary | 20 | Small management summary for the overall dispatched-unit total. | Metric (text), Value (text) |

Must remain incomplete before recording:

- Do not prefill Dispatch_Log!E2:E19 with lookup results.
- Do not prefill Dispatch_Log!F2:F19 with fixed-width ticket codes.
- Do not place a total formula in Summary!B2.
- Do not create the formula-based highlight for the maximum Restock Cost.
- Do not sort the Dispatch_Log records before the recorded task.

Artifact previews:

### Catalog

![Catalog.png](artifact/previews/Catalog.png)

### Dispatch Log

![Dispatch_Log.png](artifact/previews/Dispatch_Log.png)

### Summary

![Summary.png](artifact/previews/Summary.png)

## Operator guide

### Demonstration 1

- Skill: `7e429b8d-a3f0-4ed0-9b58-08957d00b127.skill-01`
- Intent: Classify every Dispatch_Log record by looking up its SKU in Catalog and returning the corresponding Supply Group with an exact-match VLOOKUP.
- Efficiency: Enter the first lookup with an absolute Catalog table range, then fill it down the Supply Group column so the fixed reference does not drift.
- Visible success: Every previously blank Supply Group cell contains the appropriate category, including repeated SKUs returning the same category.

### Demonstration 2

- Skill: `21ab7b40-77c2-4ae6-8321-e00d3a086c73.skill-04`
- Intent: Create a formula-based conditional-formatting rule on Dispatch_Log Restock Cost values that visibly flags the unique highest cost in the log.
- Efficiency: Apply one rule to the entire Restock Cost data range and use a relative current-row reference with an absolute maximum range.
- Visible success: Only the row/cell containing the 540.00 Restock Cost receives the chosen highlight style.

### Demonstration 3

- Skill: `0bf05a7d-b28b-44d2-955a-50b41e24012a.skill-01`
- Intent: Generate seven-character, leading-zero Ticket Code text values for all dispatch records from their numeric ticket numbers.
- Efficiency: Create the TEXT formula once from the numeric Ticket Number and fill it down rather than editing codes individually.
- Visible success: Ticket Code displays values such as 0004821 and 0000930 as fixed-width text for every record.

### Demonstration 4

- Skill: `26a8440e-c166-4c50-aef4-bfb77314b46b.skill-03`
- Intent: Calculate the Total Units Dispatched metric in Summary from the Units Dispatched range on Dispatch_Log using a cross-sheet range-total formula.
- Efficiency: Use one SUM formula that references the Units Dispatched range on Dispatch_Log rather than manually adding values.
- Visible success: Summary!B2 shows the aggregate dispatched-unit total, 649, and it is formula-derived.

### Demonstration 5

- Skill: `3a7c8185-25c1-4941-bd7b-96e823c9f21f.skill-01`
- Intent: Order the complete Dispatch_Log table by SKU in ascending alphabetical order.
- Efficiency: Sort the whole contiguous log, or extend the selection when prompted, so ticket details, costs, and generated values travel with their SKU rows.
- Visible success: Dispatch_Log records are in ascending SKU order from SKU-104 through SKU-426 with intact row associations.

Recording start: Open the supplied Replenishment Review workbook with the Catalog reference data, unsorted Dispatch_Log inputs, blank derived columns, and blank Summary total.

Recording end: The dispatch log is SKU-ascending, fully classified and assigned seven-digit text ticket codes, its unique largest restock cost is visibly formula-highlighted, and Summary shows the cross-sheet total of 649 units.

Allowed variation: The expert may perform the sort before or after filling formulas and may use equivalent range-selection or autofill methods. Use LibreOffice Calc-compatible argument separators and an equivalent visible conditional style, while retaining an exact-match lookup and a formula-based maximum test.

## Expected incidental operations

- **scaffolding:** Select the relevant destination ranges and use a fill-down/autofill method to propagate first-row formulas through all 18 dispatch records. Reason: The requested classifications and ticket-code displays must cover the complete log efficiently rather than only one row.
- **scaffolding:** Navigate between Dispatch_Log, Catalog, and Summary sheets while entering or validating formulas. Reason: The lookup source and aggregate source are on different sheets from their destinations.
- **task_specific:** Choose a clearly visible highlight style while saving the conditional-format rule. Reason: A conditional-format rule needs an applied style for the maximum-cost exception to be observable.
- **scaffolding:** Select the complete Dispatch_Log table or confirm extension of the selection when sorting. Reason: All record fields must remain associated when the SKU ordering is changed.

## Source-similarity audit

| Measure | Maximum | Most similar source task |
| --- | ---: | --- |
| Lexical sequence similarity | 0.299766 | 0a2e43bf-b26c-4631-a966-af9dfa12c9e5 |
| Semantic cosine similarity | 0.434468 | 51719eea-10bc-4246-a428-ac7c433dd4b3 |

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
  --reference-task-id reference-task-calc-full-r01-005
```

The ordinary launcher reads the collected central review file and refuses pending, revision-requested, or rejected tasks.
