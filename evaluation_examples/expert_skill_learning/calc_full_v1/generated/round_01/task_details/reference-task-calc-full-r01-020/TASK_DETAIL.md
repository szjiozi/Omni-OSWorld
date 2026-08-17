# Community Garden Supply Budget

- Reference task: `reference-task-calc-full-r01-020`
- Application: `libreoffice_calc`
- Review decision: `pending`

## Task instruction

Finish the Community Garden Supply Plan by giving the title cell A1 a #2F6B4F background and completing the Line Cost calculations for every listed supply item from the existing first calculation.

## Required skills

### 1. Apply a custom cell background color by hexadecimal value

Skill ID: `30e3e107-1cfb-46ee-a755-2cd080d7ba6a.skill-03`

Procedure:

1. Select the target cell or merged range, for example A1:C1 via its merged anchor cell A1.
2. Open the background/fill color dropdown next to the paint-bucket control and choose Custom Color.
3. Select the hexadecimal input, replace its value with an exact color such as `0000ff`, and press Enter to apply the fill.

Efficiency tip: Enter an exact hexadecimal color value in the custom-color dialog instead of approximating the shade from the palette.

Source task: `30e3e107-1cfb-46ee-a755-2cd080d7ba6a`

Source instruction: Please create a new sheet. Keep its sheet name as "Sheet2". Merge cells A1:C1 in the new sheet and write "Demographic Profile" with blue (#0000ff) fill and bold white text. Then I want to create three pivot tables to show the percentage of Sex, Civil Status, and Highest Educational Attainment. They should be stacked one by one in Sheet2, each separated with a blank line.

Directly referenced source actions:

- Action 7: <code>`CLICK` cell A1</code>
- Action 8: <code>`CLICK` arrow next to paint button dropdown</code>
- Action 9: <code>`CLICK` Custom color</code>
- Action 10: <code>`DOUBLE_CLICK` on text inside Hex # box</code>
- Action 11: <code>`TYPING` 0000ff</code>
- Action 12: <code>`PRESS` enter</code>

### 2. AutoFill a formula down by double-clicking the fill handle

Skill ID: `d681960f-7bc3-4286-9913-a8812ba3261a.skill-02`

Procedure:

1. Select the cell that contains the formula to propagate.
2. Point to the small square at the selected cell's bottom-right corner (the fill handle).
3. Double-click the fill handle. Calc copies the formula downward through the rows indicated by the neighboring contiguous data, adjusting relative references for each destination row.

Efficiency tip: Double-clicking the fill handle is faster and less error-prone than dragging across a long list, because Calc extends the formula through the adjacent contiguous data region.

Source task: `d681960f-7bc3-4286-9913-a8812ba3261a`

Source instruction: According to the scale table shown above, calculate and give each student a grade in the table below

Directly referenced source actions:

- Action 3: <code>`CLICK` F10</code>
- Action 4: <code>`DOUBLE_CLICK` bottom right corner of the cell</code>

## Initial artifact

- Domain: Community garden supply budget
- Workbook: [initial_artifact.xlsx](artifact/initial_artifact.xlsx)
- Blueprint: [artifact_blueprint.json](artifact/artifact_blueprint.json)
- QA report: [artifact_qa.json](artifact/artifact_qa.json)

Initial state:

- The workbook opens on the single sheet named "Supply Plan".
- A1 contains the plan title and has no custom background color.
- Row 3 contains table headers.
- D4 contains the only existing line-cost formula; D5:D27 are blank.
- There are no totals, charts, Pivot Tables, conditional-format rules, or additional sheets.

Artifact construction requirements:

- Use entirely synthetic, privacy-safe garden supply planning data.
- Seed the first line-extension formula only in D4 as =B4*C4. Leave D5:D27 empty so the formula propagation is visibly incomplete.
- Format columns C and D as currency with two decimal places. Use ordinary table-header styling in row 3, but do not apply a background fill to A1.
- Set A1 text to "Community Garden Supply Plan" and make it bold with a larger font; leave it unfilled so its requested final color change is visible.
- Keep columns A:C populated continuously from rows 4 through 27, ensuring that double-clicking the fill handle of D4 can extend the formula through the full data region.

| Sheet | Rows | Purpose | Columns |
| --- | ---: | --- | --- |
| Supply Plan | 27 | Itemized supply budget whose line costs need to be completed and whose title needs final visual branding. | Supply Item (text), Units (integer), Unit Cost (currency), Line Cost (currency) |

Must remain incomplete before recording:

- Do not prefill D5:D27 with formulas or values.
- Do not pre-apply the requested hexadecimal background color to A1.
- Do not add a grand-total row, chart, Pivot Table, or new worksheet.

Artifact previews:

### Supply Plan

![Supply_Plan.png](artifact/previews/Supply_Plan.png)

## Operator guide

### Demonstration 1

- Skill: `30e3e107-1cfb-46ee-a755-2cd080d7ba6a.skill-03`
- Intent: Apply the requested exact custom background color to the title cell A1.
- Efficiency: Enter the exact hexadecimal value in the custom color control rather than choosing an approximate palette swatch.
- Visible success: A1, containing "Community Garden Supply Plan," visibly displays the specified custom fill color #2F6B4F.

### Demonstration 2

- Skill: `d681960f-7bc3-4286-9913-a8812ba3261a.skill-02`
- Intent: Propagate the seeded Line Cost formula from D4 through every populated supply-item row.
- Efficiency: Use the formula cell's fill handle and double-click it so Calc follows the neighboring contiguous item data instead of manually dragging to the last row.
- Visible success: D4:D27 contain calculated currency amounts, with no blank Line Cost cells alongside populated rows 4:27.

Recording start: The Supply Plan sheet is open with unfilled title cell A1, populated input columns A:C for rows 4:27, formula only in D4, and blank D5:D27.

Recording end: The title cell A1 has fill #2F6B4F, and Line Cost is calculated in D4:D27 using the propagated relative-reference formula; no unrelated summaries or sheets have been added.

Allowed variation: The expert may use equivalent Calc menus, toolbar controls, keyboard navigation, or selection methods, provided the exact title color and the formula-filled line-cost range are visibly achieved.

## Expected incidental operations

None.

## Source-similarity audit

| Measure | Maximum | Most similar source task |
| --- | ---: | --- |
| Lexical sequence similarity | 0.388406 | abed40dc-063f-4598-8ba5-9fe749c0615d |
| Semantic cosine similarity | 0.426272 | 01b269ae-2111-4a07-81fd-3fcd711993b0 |

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
  --reference-task-id reference-task-calc-full-r01-020
```

The ordinary launcher reads the collected central review file and refuses pending, revision-requested, or rejected tasks.
