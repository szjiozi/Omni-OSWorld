# Service Estimate Review

- Reference task: `reference-task-calc-full-r01-003`
- Application: `libreoffice_calc`
- Review decision: `pending`

## Task instruction

Prepare the service-estimate review workbook: add readable estimate notes for every service request using the rate card, lay out the Overview checklist as a horizontal heading row instead of its current vertical list, and zoom out the worksheet slightly for easier review.

## Required skills

### 1. Move a cell or range while transposing it

Skill ID: `26a8440e-c166-4c50-aef4-bfb77314b46b.skill-05`

Procedure:

1. Select the source cell or range and press Ctrl+X to cut it.
2. Select the top-left destination cell, right-click it, open Paste Special, and choose Transpose.
3. Calc moves the cut content to the destination while swapping its row and column orientation. For example, cutting a vertical range and transposing it pastes the values horizontally.

Efficiency tip: Use Cut rather than Copy when the original cell should be removed after the transposed placement, avoiding a separate delete step.

Source task: `26a8440e-c166-4c50-aef4-bfb77314b46b`

Source instruction: Create a table with two column headers ("Month" and "Total") in a new sheet named "Sheet2" to show the total sales for all months.

Directly referenced source actions:

- Action 18: <code>`HOTKEY` ctrl+x</code>
- Action 19: <code>`CLICK` on B2</code>
- Action 20: <code>`RIGHT_CLICK`</code>
- Action 21: <code>`MOVE_TO` paste special</code>
- Action 22: <code>`CLICK` transpose</code>

### 2. Propagate a text formula down an output column

Skill ID: `4de54231-e4b5-49e3-b2ba-61a0bec721c0.skill-03`

Procedure:

1. Select the first output cell containing the completed formula, such as E2.
2. Double-click the bottom-right fill handle of that cell.
3. Calc copies the formula down to the last row detected from neighboring continuous data, updating relative references such as A2 to A3, A4, and so on while preserving absolute references such as $A$1.

Efficiency tip: After entering a row formula, reselect its first cell and double-click its fill handle instead of copying and pasting or dragging through every destination row.

Source task: `4de54231-e4b5-49e3-b2ba-61a0bec721c0`

Source instruction: I have compute the acceleration in row 2 and I want you to fill out other rows for column B and D. Next concatenate the values from columns A to D, including their headers (the pattern is "Header: cell value, ..., Header: cell value"), into a new column named "Combined Data" for all rows. In the new column, only keep 2 decimal digits.

Directly referenced source actions:

- Action 8: <code>`CLICK` on cell E2</code>
- Action 9: <code>`DOUBLE_CLICK` bottom right corner of the cell E2</code>

### 3. Decrease worksheet zoom with the status-bar zoom slider

Skill ID: `1334ca3e-f9e3-4db8-9ca7-b4c653be7d17.skill-01`

Procedure:

1. In LibreOffice Calc, locate the zoom slider in the bottom-right status bar.
2. Click on the left/decrease side of the slider to zoom the worksheet out. For example, one click reduces the displayed cell size so more rows and columns fit on screen.
3. Repeat only as needed until cells are comfortably selectable at the desired scale.

Efficiency tip: Use the slider for a quick incremental adjustment; click closer to the desired level rather than repeatedly clicking the decrease end when a larger reduction is needed.

Source task: `1334ca3e-f9e3-4db8-9ca7-b4c653be7d17`

Source instruction: The cells are so big that I can not click on the cell I want, zoom out a little bit.

Directly referenced source actions:

- Action 0: <code>`CLICK` on the left-hand side of the zoom slider at the bottom right corner of the screen</code>

### 4. Build a cross-sheet lookup formula with row arithmetic

Skill ID: `51719eea-10bc-4246-a428-ac7c433dd4b3.skill-01`

Procedure:

1. In the first result cell, enter a formula that looks up a value from another sheet and combines it with values from the current row.
2. For example, enter `=VLOOKUP(C2,$'Retail Price'.$A$2:$B$23,2,FALSE())*E2*(1-F2)` and press Enter. `VLOOKUP` finds the value matching `C2` in the first column of the source range and returns its second column; the remaining multiplication applies the current row's values.
3. In `$'Retail Price'.$A$2:$B$23`, the `$` before the quoted sheet name fixes the source sheet, while `$A$2:$B$23` fixes both columns and rows of the lookup range. The references `C2`, `E2`, and `F2` remain relative, so they adjust when copied to another row.

Efficiency tip: Type the complete formula once in the first result cell, then propagate it rather than rebuilding the lookup and arithmetic separately for every row.

Source task: `51719eea-10bc-4246-a428-ac7c433dd4b3`

Source instruction: Calculate revenue in a new column according to the Retail Price sheet (consider product price and quantity and discount), and generate a Pivot Table in a new sheet (Sheet2) that summarizes the revenue of each product.

Directly referenced source actions:

- Action 5: <code>`TYPING` &#x27;=VLOOKUP(C2,$&#x27;Retail Price&#x27;.$A$2:$B$23,2,FALSE())*E2*(1-F2)&#x27;</code>
- Action 6: <code>`PRESS` enter</code>

## Initial artifact

- Domain: service-estimate review
- Workbook: [initial_artifact.xlsx](artifact/initial_artifact.xlsx)
- Blueprint: [artifact_blueprint.json](artifact/artifact_blueprint.json)
- QA report: [artifact_qa.json](artifact/artifact_qa.json)

Initial state:

- The workbook opens on `Service Requests`, with the active cell in A1 or another neutral cell near the top of that sheet.
- `Service Requests` has continuous populated neighboring data in A2:D19 so a formula entered in E2 can be filled through row 19.
- `Estimate Note` is intentionally blank for every request.
- The lookup table on `Rate Card` is complete and fixed before the task begins.
- The Overview checklist labels exist only as the vertical source in A3:A6; the horizontal destination B2:E2 is blank.
- No worksheet has been zoomed out yet.

Artifact construction requirements:

- Use only fictional service-request data and fictional service codes; do not include real people, businesses, addresses, or account identifiers.
- Create a `Rate Card` sheet with the two-column table `Service Code`, `Unit Rate` in A1:B7. Use these six literal lookup entries: DIAG / 42.50, CALIB / 68.00, REPAIR / 115.75, INSTALL / 89.25, TRAIN / 54.00, AUDIT / 76.50. Format Unit Rate as currency with two decimal places.
- Create a `Service Requests` sheet with headers in A1:E1: `Request ID`, `Service Code`, `Units`, `Adjustment`, `Estimate Note`. Populate A2:D19 with 18 fictional requests, using request IDs SR-4101 through SR-4118, service codes drawn from the Rate Card, positive whole-number Units from 1 through 5, and Adjustment decimal values from 0.00 through 0.20. Keep all codes valid lookup keys. Format Adjustment as percentage with zero decimal places and leave E2:E19 completely blank.
- Suggested deterministic request rows, in A:D order: SR-4101/DIAG/2/0.00; SR-4102/CALIB/1/0.10; SR-4103/REPAIR/3/0.05; SR-4104/INSTALL/2/0.00; SR-4105/TRAIN/4/0.15; SR-4106/AUDIT/1/0.00; SR-4107/DIAG/5/0.20; SR-4108/REPAIR/1/0.10; SR-4109/CALIB/3/0.00; SR-4110/INSTALL/4/0.05; SR-4111/TRAIN/2/0.00; SR-4112/AUDIT/3/0.10; SR-4113/DIAG/1/0.00; SR-4114/REPAIR/2/0.15; SR-4115/CALIB/4/0.05; SR-4116/INSTALL/1/0.00; SR-4117/TRAIN/3/0.10; SR-4118/AUDIT/2/0.00.
- Create an `Overview` sheet for a compact review checklist. Put the four text labels `Rate verified`, `Adjustment reviewed`, `Estimate prepared`, and `Ready to send` vertically in A3:A6. Leave B2:E2 blank as the intended horizontal checklist-heading location. Leave A3:A6 unmerged and otherwise ordinarily formatted.
- Use ordinary header styling (for example, bold text and a light fill) for all table headers. Do not add formulas, charts, pivot tables, conditional formatting, data validation, or prebuilt transposed output. Start at normal/default worksheet zoom, preferably 100%.

| Sheet | Rows | Purpose | Columns |
| --- | ---: | --- | --- |
| Rate Card | 6 | Fixed fictional unit-rate lookup table for service estimates. | Service Code (text), Unit Rate (currency) |
| Service Requests | 18 | Fictional service requests requiring readable calculated estimate notes. | Request ID (text), Service Code (text), Units (integer), Adjustment (decimal), Estimate Note (text) |
| Overview | 6 | Review checklist whose labels need to be reoriented into a horizontal heading row. | Checklist labels source and destination area (text) |

Must remain incomplete before recording:

- Do not prepopulate or seed any formula in `Service Requests!E2:E19`.
- Do not transpose, copy, or delete the `Overview!A3:A6` checklist labels before the recorded task.
- Do not create a native Pivot Table, chart, conditional-format rule, validation list, or additional sheet.
- Do not alter the rate-card values or the request inputs in A2:D19.

Artifact previews:

### Overview

![Overview.png](artifact/previews/Overview.png)

### Rate Card

![Rate_Card.png](artifact/previews/Rate_Card.png)

### Service Requests

![Service_Requests.png](artifact/previews/Service_Requests.png)

## Operator guide

### Demonstration 1

- Skill: `26a8440e-c166-4c50-aef4-bfb77314b46b.skill-05`
- Intent: On Overview, move the four checklist labels from A3:A6 into the blank B2:E2 heading area while changing their vertical orientation to horizontal.
- Efficiency: Use Cut rather than Copy so the old vertical checklist is cleared automatically after the horizontal placement.
- Visible success: B2:E2 displays the four labels left-to-right in their original top-to-bottom order, and A3:A6 no longer contains those source labels.

### Demonstration 2

- Skill: `51719eea-10bc-4246-a428-ac7c433dd4b3.skill-01`
- Intent: In the first Estimate Note cell on Service Requests, create a text-producing formula that looks up the unit rate for that row's service code and calculates rate × units × (1 − adjustment), presenting the resulting amount in a readable estimate note.
- Efficiency: Build the full relative-row calculation once, using absolute references for the Rate Card lookup range, rather than constructing separate formulas per request.
- Visible success: E2 shows readable text including a calculated currency estimate, and changing-row references are visible in the formula while the Rate Card table reference remains fixed.

### Demonstration 3

- Skill: `4de54231-e4b5-49e3-b2ba-61a0bec721c0.skill-03`
- Intent: Propagate the completed Estimate Note formula from E2 down through all 18 request rows.
- Efficiency: After confirming E2, use the fill handle's double-click behavior to extend through the contiguous request records instead of manually copying each result.
- Visible success: Every cell from E2 through E19 contains a text estimate note with row-appropriate calculated values; there are no blank output cells in that range.

### Demonstration 4

- Skill: `1334ca3e-f9e3-4db8-9ca7-b4c653be7d17.skill-01`
- Intent: Reduce the worksheet display zoom so more of the service-request table is comfortably visible.
- Efficiency: Use the status-bar slider to make one intentional reduction, selecting a comfortable smaller scale instead of many small adjustments.
- Visible success: The status bar indicates a lower zoom than the initial default and visibly more rows or columns fit in the worksheet view.

Recording start: Open the supplied Service Estimate Review workbook in Calc with its three sheets in the described incomplete state.

Recording end: Service Requests has populated text estimate notes in E2:E19 based on the Rate Card and each request row; Overview has the checklist labels only across B2:E2; and worksheet zoom is visibly lower than at the start.

Allowed variation: Equivalent Calc commands, formula syntax accepted by the installed locale, and a different modest zoom-out level are acceptable. The estimate text may use a comparable clear label and currency formatting, provided it remains a text result that uses the Rate Card lookup and the same-row Units and Adjustment arithmetic.

## Expected incidental operations

- **scaffolding:** Switch between the Service Requests, Rate Card, and Overview sheets as needed. Reason: The estimate formula refers to the lookup table on another sheet, while the checklist change is on Overview.
- **scaffolding:** Select the relevant source range, output cell, or destination anchor before carrying out each requested worksheet action. Reason: Range and cell selection is inherent setup for entering the calculation and placing the moved checklist labels.
- **task_specific:** Enter one complete text-producing estimate formula in the first Estimate Note cell before propagating it. Reason: A first-row formula is required as the source for the requested filled output column.

## Source-similarity audit

| Measure | Maximum | Most similar source task |
| --- | ---: | --- |
| Lexical sequence similarity | 0.342723 | 42e0a640-4f19-4b28-973d-729602b5a4a7 |
| Semantic cosine similarity | 0.427412 | 51719eea-10bc-4246-a428-ac7c433dd4b3 |

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
  --reference-task-id reference-task-calc-full-r01-003
```

The ordinary launcher reads the collected central review file and refuses pending, revision-requested, or rejected tasks.
