# Regional Community Grant Requests

- Reference task: `reference-task-calc-full-r01-001`
- Application: `libreoffice_calc`
- Review decision: `pending`

## Task instruction

Turn the Funding Plan sheet into a concise regional funding snapshot: display every Requested Funding amount as a rounded one-decimal figure in millions with a separated M suffix, then add a column chart comparing requests by region and title it "Regional Funding Requests".

## Required skills

### 1. Format values as rounded millions with a spaced unit suffix

Skill ID: `21df9241-f8d7-4509-b7f1-37e501a823f7.skill-02`

Procedure:

1. Select the cells to format, then right-click the selection and choose Format Cells.
2. Activate the format-code field and enter a custom numeric format such as `0.0,, \M`, then confirm with Enter.
3. The two trailing commas scale the displayed value by one million, `0.0` displays one decimal place, and the literal space before `\M` separates the number from the M suffix. For example, 12500000 displays as `12.5 M`.

Efficiency tip: Apply the custom format to the full intended range before opening Format Cells when possible, so the format is configured once rather than cell by cell.

Source task: `21df9241-f8d7-4509-b7f1-37e501a823f7`

Source instruction: Change the representation of column "Parameter" to show in Millions (M) in Column B and Billions (B) in Column C. The numbers should be rounded to one decimal place, and half should be rounded up. Then remember to place a white space between the digits and the unit.

Directly referenced source actions:

- Action 5: <code>`RIGHT_CLICK`</code>
- Action 6: <code>`CLICK` &#x27;Format Cells...&#x27;</code>
- Action 7: <code>`DOUBLE_CLICK` format code box</code>
- Action 8: <code>`TYPING` &#x27;0.0,, \M&#x27;</code>
- Action 9: <code>`PRESS` enter</code>

### 2. Set a chart title through the Chart elements control

Skill ID: `0326d92d-d218-48a8-9ca1-981cd6d064c7.skill-05`

Procedure:

1. Activate the chart and open Chart elements.
2. Click the title text box, type the desired title, and press Enter to apply it.
3. For example, type `Total` for one chart or `Growth` for another; use the text appropriate to the chart in a new workbook.

Efficiency tip: Edit the title immediately after creating each chart while it is active, avoiding later selection and formatting steps.

Source task: `0326d92d-d218-48a8-9ca1-981cd6d064c7`

Source instruction: Calculate the total sales in an underneath row called "Total" and display the total of each month as bars. Then calculate the month-on-month growth percentage for Feb to Jun in another row called "Growth" and show them in a line chart (Jan should be omitted in the chart as well). Set the chart titles as the two row headers respectively.

Directly referenced source actions:

- Action 18: <code>`CLICK` Chart elements</code>
- Action 19: <code>`CLICK` title text box</code>
- Action 20: <code>`TYPING` &#x27;Total&#x27;</code>
- Action 21: <code>`PRESS` enter</code>
- Action 41: <code>`CLICK` Chart elements</code>
- Action 42: <code>`CLICK` title text box</code>
- Action 43: <code>`TYPING` &#x27;Growth&#x27;</code>
- Action 44: <code>`PRESS` enter</code>

## Initial artifact

- Domain: regional community grant requests
- Workbook: [initial_artifact.xlsx](artifact/initial_artifact.xlsx)
- Blueprint: [artifact_blueprint.json](artifact/artifact_blueprint.json)
- QA report: [artifact_qa.json](artifact/artifact_qa.json)

Initial state:

- The workbook contains one worksheet named Funding Plan.
- Funding Plan contains a contiguous table in A1:C7 with headers in row 1.
- Column C holds six large numeric requested-funding values suitable for a display in millions.
- There is open blank space beginning at E2 for a chart to be inserted.
- No chart title exists because no chart exists initially.

Artifact construction requirements:

- Use entirely synthetic, privacy-safe regional funding data with no real organizations or people.
- Populate all monetary values as numeric whole-dollar amounts, not text.
- Use a simple professional header style: bold white text on a dark teal fill, with light borders for the data table.
- Set the initial number format of Requested Funding to a normal currency or general numeric format; do not apply a millions-scaled custom format.
- Do not create any chart, drawing object, pivot table, or conditional-format rule in the builder.

| Sheet | Rows | Purpose | Columns |
| --- | ---: | --- | --- |
| Funding Plan | 6 | Source table for a regional funding snapshot and comparison chart. | Region (text), Grant Theme (text), Requested Funding (currency) |

Must remain incomplete before recording:

- Requested Funding values must not already display with an M suffix or be scaled to millions.
- A comparison chart of regional requested funding must not already exist.
- No chart title reading Regional Funding Requests may be present.

Artifact previews:

### Funding Plan

![Funding_Plan.png](artifact/previews/Funding_Plan.png)

## Operator guide

### Demonstration 1

- Skill: `21df9241-f8d7-4509-b7f1-37e501a823f7.skill-02`
- Intent: Format all Requested Funding values to show rounded, one-decimal amounts in millions with a space before the M unit suffix.
- Efficiency: Select the entire numeric funding range before opening cell-format settings so that the custom display is applied once to all six values.
- Visible success: Each funding value in column C is displayed in a form such as 3.6 M while retaining its underlying full-dollar numeric value.

### Demonstration 2

- Skill: `0326d92d-d218-48a8-9ca1-981cd6d064c7.skill-05`
- Intent: Give the regional funding comparison chart the title Regional Funding Requests through its chart-elements title interface.
- Efficiency: Set the title while the newly created chart is still active, using the chart-elements title control rather than returning to it later.
- Visible success: The visible chart title reads Regional Funding Requests above the chart.

Recording start: Funding Plan shows the unformatted source table with six regional records and a blank chart area; no chart is present.

Recording end: Funding Plan shows all six Requested Funding cells in rounded millions with a spaced M suffix, plus a visible regional comparison chart titled Regional Funding Requests.

Allowed variation: The expert may use an equivalent Calc chart type that clearly compares funding across regions, may place the chart anywhere in the provided blank area, and may use either a selection-first or chart-wizard workflow. The amount display must remain a one-decimal millions representation with a visibly separated M suffix.

## Expected incidental operations

- **scaffolding:** Select the Region labels and Requested Funding values as the source data for the comparison chart. Reason: The chart needs category labels and a numeric series before its title can be set.
- **substantive_prerequisite:** Insert a column-style chart comparing requested funding by region in the available blank area of Funding Plan. Reason: An active chart is required in order to use the chart-elements title control.

## Source-similarity audit

| Measure | Maximum | Most similar source task |
| --- | ---: | --- |
| Lexical sequence similarity | 0.30273 | 0a2e43bf-b26c-4631-a966-af9dfa12c9e5 |
| Semantic cosine similarity | 0.418443 | 0326d92d-d218-48a8-9ca1-981cd6d064c7 |

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
  --reference-task-id reference-task-calc-full-r01-001
```

The ordinary launcher reads the collected central review file and refuses pending, revision-requested, or rejected tasks.
