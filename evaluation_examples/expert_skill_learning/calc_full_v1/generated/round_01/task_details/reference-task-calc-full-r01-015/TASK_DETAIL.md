# Fleet Fuel Planning

- Reference task: `reference-task-calc-full-r01-015`
- Application: `libreoffice_calc`
- Review decision: `pending`

## Task instruction

Complete the route fuel estimates for every dispatch record and add the overall estimated-liters total. Then rename the blank analysis worksheet to "Zone Fuel Summary" and use a Pivot Table there to report the summed estimated fuel for each zone.

## Required skills

### 1. Enter a range-total formula in a spreadsheet cell

Skill ID: `0326d92d-d218-48a8-9ca1-981cd6d064c7.skill-01`

Procedure:

1. Select the first result cell in the totals row and type a SUM formula covering the source values for that column.
2. For example, enter `=SUM(B2:B11)` and press Enter to calculate the total for column B.

Efficiency tip: Enter the formula once in the first result cell, then use the fill handle separately to propagate it rather than retyping the formula for every column.

Source task: `0326d92d-d218-48a8-9ca1-981cd6d064c7`

Source instruction: Calculate the total sales in an underneath row called "Total" and display the total of each month as bars. Then calculate the month-on-month growth percentage for Feb to Jun in another row called "Growth" and show them in a line chart (Jan should be omitted in the chart as well). Set the chart titles as the two row headers respectively.

Directly referenced source actions:

- Action 3: <code>`TYPING` &#x27;=SUM(B2:B11)&#x27;</code>
- Action 4: <code>`PRESS` enter</code>

### 2. Autofill an existing formula down a column with the fill handle

Skill ID: `4de54231-e4b5-49e3-b2ba-61a0bec721c0.skill-01`

Procedure:

1. Select the cell that already contains the formula to propagate, such as B2.
2. Double-click the small square fill handle at the cell's bottom-right corner. Calc fills the formula downward to the end of the adjacent contiguous data region, adjusting relative references for each row.
3. Repeat the same operation for another formula column when needed, for example select D2 and double-click its fill handle.

Efficiency tip: Double-clicking the fill handle is faster and less error-prone than dragging it through a long data range; verify that an adjacent column contains uninterrupted data so Calc can detect the intended last row.

Source task: `4de54231-e4b5-49e3-b2ba-61a0bec721c0`

Source instruction: I have compute the acceleration in row 2 and I want you to fill out other rows for column B and D. Next concatenate the values from columns A to D, including their headers (the pattern is "Header: cell value, ..., Header: cell value"), into a new column named "Combined Data" for all rows. In the new column, only keep 2 decimal digits.

Directly referenced source actions:

- Action 0: <code>`CLICK` on cell B2</code>
- Action 1: <code>`DOUBLE_CLICK` bottom right corner of the cell B2</code>
- Action 2: <code>`CLICK` on cell D2</code>
- Action 3: <code>`DOUBLE_CLICK` bottom right corner of the cell D2</code>

### 3. Create a Pivot Table from the selected data range

Skill ID: `51719eea-10bc-4246-a428-ac7c433dd4b3.skill-03`

Procedure:

1. Click within the dataset and use `Ctrl+A` to select the current contiguous data range, including its header row.
2. Click the Pivot Table toolbar icon to open the Pivot Table creation flow.
3. Accept the detected selected range, for example by pressing Enter in the initial creation dialog, to open the Pivot Table field-layout dialog.

Efficiency tip: Select the full current data region before creating the Pivot Table so Calc detects the source range automatically and no manual range entry is needed.

Source task: `51719eea-10bc-4246-a428-ac7c433dd4b3`

Source instruction: Calculate revenue in a new column according to the Retail Price sheet (consider product price and quantity and discount), and generate a Pivot Table in a new sheet (Sheet2) that summarizes the revenue of each product.

Directly referenced source actions:

- Action 10: <code>`HOTKEY` ctrl-A</code>
- Action 11: <code>`CLICK` pivot table icon</code>
- Action 12: <code>`PRESS` enter</code>

### 4. Rename a worksheet from its sheet tab

Skill ID: `535364ea-05bd-46ea-9937-9f55c68507e8.skill-02`

Procedure:

1. Double-click the worksheet tab whose name you want to change.
2. Type the new tab name, for example Sheet2, and press Enter to apply it.
3. The tab label updates, and the new name can be used in references such as $Sheet2.$A$15.

Efficiency tip: Rename a newly created sheet immediately after it is inserted so later cross-sheet references and destination selections use a clear, stable sheet name.

Source task: `535364ea-05bd-46ea-9937-9f55c68507e8`

Source instruction: Create two pivot tables in a new sheet showing the total revenue for each product and sales channel.

Directly referenced source actions:

- Action 8: <code>`DOUBLE_CLICK` Pivot Table Sheet1_1</code>
- Action 9: <code>`TYPING` Sheet2</code>
- Action 10: <code>`PRESS` enter</code>

## Initial artifact

- Domain: municipal vehicle fuel planning
- Workbook: [initial_artifact.xlsx](artifact/initial_artifact.xlsx)
- Blueprint: [artifact_blueprint.json](artifact/artifact_blueprint.json)
- QA report: [artifact_qa.json](artifact/artifact_qa.json)

Initial state:

- The workbook opens with "Dispatch Log" as the active sheet.
- The source dataset is contiguous only through A1:E25, with an uninterrupted neighboring data region suitable for fill-handle propagation.
- The only pre-existing calculated value in Estimated Liters is the seed formula in E2.
- The overall total cell E28 is blank.
- The output worksheet is still named "Analysis" and is blank.

Artifact construction requirements:

- Create a privacy-safe synthetic workbook titled "Fleet Fuel Planning" with realistic fictional route labels, zones, distances, and fuel-use rates.
- On "Dispatch Log", create one contiguous source table in A1:E25. Row 1 is the header row and rows 2:25 contain 24 route records. Use at least three repeating Zone values (for example, Harbor, Northside, and Ridge) so a zone summary is meaningful.
- Populate Route Code with unique synthetic IDs, Zone with repeating text categories, Distance (km) with positive decimal values, and Liters per km with positive decimal values. Ensure every data row has a nonblank value in columns A:D.
- Set E1 to "Estimated Liters". Seed only E2 with the formula =C2*D2. Leave E3:E25 genuinely blank; do not seed formulas there.
- Use decimal number formatting with two decimal places for C2:C25, D2:D25, and E2:E25. Style the header row distinctly, but do not create a native table, Pivot Table, or conditional formatting rule.
- Leave rows 26 and 27 blank. In D28 place the label "Total estimated liters" and leave E28 blank as the designated overall-total result cell.
- Create a second empty worksheet named "Analysis". It must contain no prebuilt report content or Pivot Table.

| Sheet | Rows | Purpose | Columns |
| --- | ---: | --- | --- |
| Dispatch Log | 24 | Source records for route-level fuel estimates and the overall total. | Route Code (text), Zone (text), Distance (km) (decimal), Liters per km (decimal), Estimated Liters (decimal) |
| Analysis | 10 | Blank destination worksheet to be renamed and used for the zone fuel Pivot Table. | (blank output sheet) (text) |

Must remain incomplete before recording:

- Do not fill E3:E25 with formulas or values.
- Do not enter a total formula or value in E28.
- Do not rename the "Analysis" worksheet.
- Do not create or preconfigure any Pivot Table.

Artifact previews:

### Analysis

![Analysis.png](artifact/previews/Analysis.png)

### Dispatch Log

![Dispatch_Log.png](artifact/previews/Dispatch_Log.png)

## Operator guide

### Demonstration 1

- Skill: `4de54231-e4b5-49e3-b2ba-61a0bec721c0.skill-01`
- Intent: Propagate the route-level Estimated Liters calculation from the seeded first record through all remaining route records.
- Efficiency: Use the existing formula in E2 as the single source and double-click its fill handle; columns A:D have no gaps, so Calc can infer the final record row reliably.
- Visible success: Every cell from E2 through E25 displays a calculated fuel estimate, with relative row references reflected in the formulas.

### Demonstration 2

- Skill: `0326d92d-d218-48a8-9ca1-981cd6d064c7.skill-01`
- Intent: Calculate the fleet-wide estimated fuel amount in the designated total cell E28.
- Efficiency: Enter one SUM over the completed Estimated Liters record range rather than adding individual records.
- Visible success: E28 shows a numeric overall total generated by a SUM formula covering the Estimated Liters data rows.

### Demonstration 3

- Skill: `535364ea-05bd-46ea-9937-9f55c68507e8.skill-02`
- Intent: Rename the blank "Analysis" worksheet to "Zone Fuel Summary".
- Efficiency: Rename the blank destination sheet before configuring Pivot Table placement so its report role is clear in the destination selector.
- Visible success: The worksheet tab formerly labeled "Analysis" is visibly labeled "Zone Fuel Summary".

### Demonstration 4

- Skill: `51719eea-10bc-4246-a428-ac7c433dd4b3.skill-03`
- Intent: Create the zone-level fuel Pivot Table from the completed Dispatch Log data and place it on the renamed report sheet.
- Efficiency: Start from the contiguous source table including headers so Calc detects the source fields automatically, then assign the grouping and summed measure in the layout dialog.
- Visible success: "Zone Fuel Summary" contains a native Pivot Table listing zones and a sum of Estimated Liters for each zone.

Recording start: "Dispatch Log" is active with the seeded E2 formula, blank E3:E25 and E28, and an empty worksheet tab named "Analysis".

Recording end: The Dispatch Log has formula-derived estimates in E2:E25 and a SUM total in E28; the output tab is named "Zone Fuel Summary" and contains a Pivot Table that sums Estimated Liters by Zone.

Allowed variation: The expert may create the Pivot Table before or after entering the overall total, and may use equivalent Calc commands or keyboard shortcuts. The finished Pivot Table may use a standard Calc-generated layout as long as it groups by Zone and sums Estimated Liters on the renamed output sheet.

## Expected incidental operations

- **substantive_prerequisite:** Select the complete contiguous route-record range including its header row as the Pivot Table source. Reason: The Pivot Table must summarize the populated route data rather than the separated total area.
- **task_specific:** Configure the Pivot Table with Zone as the row grouping, Estimated Liters as a summed data field, and place the result on the renamed output sheet. Reason: This produces the requested zone-level fuel summary and makes the Pivot Table outcome interpretable.

## Source-similarity audit

| Measure | Maximum | Most similar source task |
| --- | ---: | --- |
| Lexical sequence similarity | 0.325815 | 1de60575-bb6e-4c3d-9e6a-2fa699f9f197 |
| Semantic cosine similarity | 0.410207 | 51719eea-10bc-4246-a428-ac7c433dd4b3 |

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
  --reference-task-id reference-task-calc-full-r01-015
```

The ordinary launcher reads the collected central review file and refuses pending, revision-requested, or rejected tasks.
