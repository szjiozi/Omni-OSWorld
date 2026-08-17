# Field Service Payment Review

- Reference task: `reference-task-calc-full-r01-007`
- Application: `libreoffice_calc`
- Review decision: `pending`

## Task instruction

Complete the Field Service Payment Review: calculate each technician's earned amount from the hourly rate and logged service duration, display the payment figures using German-style decimal separators, and mark earned amounts above 200 with a custom bright-green font. Then create a chart comparing technician earnings and place it on a newly added worksheet named Payment Overview.

## Required skills

### 1. Move a chart to a newly inserted worksheet

Skill ID: `12382c62-0cd1-4bf2-bdc8-1d20bf9b2371.skill-03`

Procedure:

1. Select the chart object and cut it with Ctrl+X.
2. Click the plus button beside the sheet tabs to insert a new worksheet; the new sheet becomes active.
3. Paste with Ctrl+V to place the cut chart on the new worksheet.

Efficiency tip: Use cut and paste rather than recreating the chart on the destination sheet; this preserves its data links, formatting, and title.

Source task: `12382c62-0cd1-4bf2-bdc8-1d20bf9b2371`

Source instruction: Create a clustered column chart showing the Sales and COGS data for each week in a new sheet. Set the chart title as "Sales & COGS".

Directly referenced source actions:

- Action 7: <code>`CLICK` on chart to select it</code>
- Action 8: <code>`HOTKEY` ctrl-X</code>
- Action 9: <code>`CLICK` on + to left of sheet1</code>
- Action 10: <code>`HOTKEY` ctrl+v</code>

### 2. Rename a worksheet from its sheet tab

Skill ID: `51719eea-10bc-4246-a428-ac7c433dd4b3.skill-05`

Procedure:

1. Double-click the worksheet tab to make its name editable.
2. Type the desired new name, for example `Sheet2`, and press Enter to commit the rename.

Efficiency tip: Rename the sheet tab immediately after creation so later formulas, navigation, and references use a meaningful sheet name.

Source task: `51719eea-10bc-4246-a428-ac7c433dd4b3`

Source instruction: Calculate revenue in a new column according to the Retail Price sheet (consider product price and quantity and discount), and generate a Pivot Table in a new sheet (Sheet2) that summarizes the revenue of each product.

Directly referenced source actions:

- Action 18: <code>`DOUBLE_CLICK` Pivot Table Sheet1_1</code>
- Action 19: <code>`TYPING` Sheet2</code>
- Action 20: <code>`PRESS` enter</code>

### 3. Create a conditional-format style with a custom font color

Skill ID: `21ab7b40-77c2-4ae6-8321-e00d3a086c73.skill-05`

Procedure:

1. From the conditional-formatting style or accent dropdown, choose `New Style` to create a style for cells that meet the rule.
2. Open the style’s Font Effects settings, open the font-color picker, and choose `Custom Color`.
3. Enter a hexadecimal color such as `00ff00`, then confirm the color and the style dialogs. The resulting style applies green font color whenever it is assigned to a conditional-formatting rule.

Efficiency tip: Create a reusable custom style from the conditional-formatting style selector instead of manually changing font color on each matching cell.

Source task: `21ab7b40-77c2-4ae6-8321-e00d3a086c73`

Source instruction: Please calculate the period rate for my data in a new column with header "Period Rate (%)", convert the results as number type, and highlight the highest result with green (#00ff00) font.

Directly referenced source actions:

- Action 15: <code>`CLICK` accent dropdown</code>
- Action 16: <code>`CLICK` new style</code>
- Action 17: <code>`CLICK` font effects</code>
- Action 18: <code>`CLICK` font color dropdown</code>
- Action 19: <code>`CLICK` custom color...</code>
- Action 20: <code>`DOUBLE_CLICK` Hex text box</code>
- Action 21: <code>`TYPING` &#x27;00ff00&#x27;</code>
- Action 22: <code>`PRESS` enter</code>
- Action 23: <code>`CLICK` OK</code>

### 4. Apply a locale-specific number format to a selected cell range

Skill ID: `a01fbce3-2793-461f-ab86-43680ccbae25.skill-01`

Procedure:

1. Select the cells whose displayed numeric separators should follow a different locale; for example, drag from A2 through B20.
2. Right-click the selected range and choose Format Cells.
3. In the Format Cells dialog, open the Language dropdown, type or select the desired locale, such as “German (aus),” and press Enter to apply that selection.
4. Click OK. The selected cells retain their underlying numeric values and decimal precision, while their displayed decimal separator follows the chosen locale (for example, a comma).

Efficiency tip: Select the full target range before opening Format Cells so the locale change is applied in one operation rather than formatting cells individually.

Source task: `a01fbce3-2793-461f-ab86-43680ccbae25`

Source instruction: I need to set the decimal separator as a comma (,) for localized data representation and clarity in visualization. Can you help me to update all the numbers in the sheet? Also please keep the decimal numbers as-is.

Directly referenced source actions:

- Action 0: <code>`MOVE_TO` cell A2</code>
- Action 1: <code>`DRAG_TO` cell B20</code>
- Action 2: <code>`RIGHT_CLICK`</code>
- Action 3: <code>`CLICK` Format Cells.</code>
- Action 4: <code>`CLICK` Language dropdown</code>
- Action 5: <code>`TYPING` German (aus)</code>
- Action 6: <code>`PRESS` enter</code>
- Action 7: <code>`CLICK` OK.</code>

### 5. Multiply a numeric rate by a duration converted to decimal hours

Skill ID: `357ef137-7eeb-4c80-a3bb-0951f26a8aff.skill-01`

Procedure:

1. Select the destination cell where the numeric product should appear.
2. Enter a formula that multiplies the rate by the duration expressed as hours plus minutes divided by 60. For example, use `=F3*(HOUR(D3)+MINUTE(D3)/60)`, where `F3` contains a numeric rate and `D3` contains a time or duration value.
3. Press Enter to calculate the result. `HOUR(D3)` supplies the whole-hour component, while `MINUTE(D3)/60` converts the remaining minutes into a fractional hour before multiplication.

Efficiency tip: Enter the conversion directly within the multiplication formula so Calc calculates a numeric amount in one cell, rather than creating helper cells solely to convert the duration.

Source task: `357ef137-7eeb-4c80-a3bb-0951f26a8aff`

Source instruction: I have calculated the total work hours from the everday hours. And I have an hourly rate. Now I want to multiply the total hours with the hourly rate to get a total earned amount. However, I can't get a correct answer by directly multiply the two cells. Here the "total hours" is of time and "hourly rate" is just a number. How can I get the correct product of them?

Directly referenced source actions:

- Action 0: <code>`CLICK` E3</code>
- Action 1: <code>`TYPING` &#x27;=F3*(HOUR(D3)+MINUTE(D3)/60)&#x27;</code>
- Action 2: <code>`PRESS` Enter</code>

## Initial artifact

- Domain: mobile equipment maintenance shift payments
- Workbook: [initial_artifact.xlsx](artifact/initial_artifact.xlsx)
- Blueprint: [artifact_blueprint.json](artifact/artifact_blueprint.json)
- QA report: [artifact_qa.json](artifact/artifact_qa.json)

Initial state:

- The workbook opens with one active worksheet named Shift Log.
- Shift Log contains a styled header row in A1:E1 and populated source data in rows 2:13.
- There is no chart object anywhere in the workbook.
- There is no conditional formatting on the Earned Amount range.
- No worksheet exists for the payment chart.
- Cells E2:E13 are blank and ready for formulas.

Artifact construction requirements:

- Use wholly synthetic technician names, work-order IDs, and payment values.
- On the Shift Log sheet, populate 12 data rows (rows 2-13) with distinct technician names, work-order IDs, service durations between 1:15 and 7:45, and hourly rates between 28.50 and 46.75.
- Store each Service Duration as a Calc time serial value and display it initially with the number format [HH]:MM.
- Format Hourly Rate initially as a numeric value with two decimal places, not as currency.
- Leave the Earned Amount cells empty; they are intended to be calculated during the task.
- Use a German-language locale selection target for the numeric display requirement; the underlying numbers must remain unchanged.
- Do not create native charts, conditional-format rules, or extra worksheets in the initial workbook.

| Sheet | Rows | Purpose | Columns |
| --- | ---: | --- | --- |
| Shift Log | 12 | Source log of paid field-service shifts, with a blank calculated earnings column. | Technician (text), Work Order (text), Service Duration (decimal), Hourly Rate (decimal), Earned Amount (currency) |

Must remain incomplete before recording:

- Do not prefill formulas or values in E2:E13.
- Do not pre-create the conditional-format rule or its custom green font style.
- Do not insert, rename, or prepopulate the chart worksheet.
- Do not create the technician earnings chart.

Artifact previews:

### Shift Log

![Shift_Log.png](artifact/previews/Shift_Log.png)

## Operator guide

### Demonstration 1

- Skill: `357ef137-7eeb-4c80-a3bb-0951f26a8aff.skill-01`
- Intent: Calculate each Earned Amount by multiplying the hourly rate by the service duration converted from hours and minutes to decimal hours.
- Efficiency: Enter the decimal-hour conversion directly in the earnings calculation and fill it down, avoiding helper columns.
- Visible success: Every populated shift row has a numeric Earned Amount consistent with its rate and displayed duration.

### Demonstration 2

- Skill: `a01fbce3-2793-461f-ab86-43680ccbae25.skill-01`
- Intent: Apply a German locale-specific numeric display format to the Hourly Rate and Earned Amount values while preserving their values and precision.
- Efficiency: Select all target payment cells before opening the formatting dialog so one locale choice updates the full selection.
- Visible success: The targeted payment numbers visibly use comma decimal separators, while calculations remain numeric.

### Demonstration 3

- Skill: `21ab7b40-77c2-4ae6-8321-e00d3a086c73.skill-05`
- Intent: Add a conditional-format rule that identifies Earned Amount values above 200 and uses a custom font color of #00FF00 for matching cells.
- Efficiency: Create the custom conditional-format style from the rule's style selector so it can be reused rather than manually formatting individual cells.
- Visible success: At least one qualifying Earned Amount is shown in bright green text, and nonqualifying values are not.

### Demonstration 4

- Skill: `12382c62-0cd1-4bf2-bdc8-1d20bf9b2371.skill-03`
- Intent: Create a technician-versus-earned-amount chart, insert a fresh worksheet, and move the chart object onto that new worksheet.
- Efficiency: Cut and paste the completed chart rather than recreating it, preserving its chart settings and links.
- Visible success: The chart is no longer on Shift Log and is visible on its own newly inserted worksheet with linked earnings data.

### Demonstration 5

- Skill: `51719eea-10bc-4246-a428-ac7c433dd4b3.skill-05`
- Intent: Rename the newly inserted chart worksheet to Payment Overview.
- Efficiency: Rename the new tab as soon as it is created, before continuing work on the chart sheet.
- Visible success: The workbook tab for the chart sheet visibly reads Payment Overview.

Recording start: One-sheet workbook with the populated Shift Log source table, blank Earned Amount cells, and no chart, conditional formatting, or additional worksheet.

Recording end: Shift Log contains calculated payment values with German-style numeric display and green-font conditional emphasis for earnings above 200; a chart comparing technician earnings is located on a separate worksheet named Payment Overview.

Allowed variation: The expert may use menu commands, dialogs, keyboard shortcuts, autofill, or equivalent Calc workflows. Chart type and threshold may follow the task wording as long as the result clearly compares technician earnings and the specified visual and worksheet outcomes are present.

## Expected incidental operations

- **substantive_prerequisite:** Create a chart from the completed Technician and Earned Amount data before relocating it. Reason: A chart object must exist in order to demonstrate moving it to a newly inserted worksheet.
- **scaffolding:** Fill or copy the decimal-hours earnings formula down through all populated shift rows. Reason: The review requires a complete calculated earnings column rather than a single isolated result.
- **task_specific:** Create a conditional-format rule for unusually high earned amounts and assign the newly created custom-font-color style to that rule. Reason: The requested high-payment emphasis requires both a rule and the mandated reusable custom style.
- **scaffolding:** Select the completed numeric payment range before applying the locale-specific number format. Reason: The locale display change should consistently cover all relevant rate and earnings values.

## Source-similarity audit

| Measure | Maximum | Most similar source task |
| --- | ---: | --- |
| Lexical sequence similarity | 0.266667 | 0bf05a7d-b28b-44d2-955a-50b41e24012a |
| Semantic cosine similarity | 0.427664 | 035f41ba-6653-43ab-aa63-c86d449d62e5 |

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
  --reference-task-id reference-task-calc-full-r01-007
```

The ordinary launcher reads the collected central review file and refuses pending, revision-requested, or rejected tasks.
