# Workshop Service Billing

- Reference task: `reference-task-r01-004`
- Application: `libreoffice_calc`
- Review decision: `pending`

## Task instruction

Complete the billed-charge calculation for every workshop service record and present those results as currency. Then create a new Pivot Table summary that lists each coordinator and their total billed charge.

## Required skills

### 1. Apply currency formatting with the toolbar

Skill ID: `035f41ba-6653-43ab-aa63-c86d449d62e5.skill-02`

Procedure:

1. Keep the cell or range containing monetary results selected.
2. Click the toolbar's Format as Currency button to apply the currency number format.
3. For example, after calculating a value in J2, select J2 and use the currency icon so the numeric result displays as an amount.

Efficiency tip: Format the first result cell before filling the formula down so copied results retain the same number format.

Source task: `035f41ba-6653-43ab-aa63-c86d449d62e5`

Source instruction: Help me fill in the Gross profit column by subtracting all the available expenses including discounts, allowances, material and labor charges, and overhead from the actual sale, i.e., the sales after deducting the returns. Then under column A named "Year_Profit" in a new sheet, display the Year Column in Sheet 1 as text appended by a "_" with the corresponding integer digits of Gross Profit value.

Directly referenced source actions:

- Action 2: <code>`CLICK` format as currency icon</code>

### 2. Place a field in Pivot Table row labels

Skill ID: `1954cced-e748-45c4-9c26-9855b97fbc5e.skill-02`

Procedure:

1. In the Pivot Table layout dialog, locate the desired field in the Available Fields list.
2. Drag the field into the Row Fields area. For example, drag an identifier field there to produce one row label per distinct identifier.

Efficiency tip: Drag a field directly from Available Fields to Row Fields rather than adding it elsewhere first and repositioning it afterward.

Source task: `1954cced-e748-45c4-9c26-9855b97fbc5e`

Source instruction: Create a Pivot Table in a new sheet (Sheet2) to count how many times each "Invoice No." appears.

Directly referenced source actions:

- Action 3: <code>`MOVE_TO` invoice no. in available fields box</code>
- Action 4: <code>`DRAG_TO` row fields box</code>

## Initial artifact

- Domain: community workshop service billing
- Workbook: [initial_artifact.xlsx](artifact/initial_artifact.xlsx)
- Blueprint: [artifact_blueprint.json](artifact/artifact_blueprint.json)
- QA report: [artifact_qa.json](artifact/artifact_qa.json)

Initial state:

- The workbook opens on the Service Log sheet.
- Service Log contains a single header row and 24 populated data rows.
- The Billed Charge cells are blank, have no formulas, and use General number formatting.
- The source data is a contiguous table with no blank rows or blank headers.
- No pivot-summary sheet exists initially.

Artifact construction requirements:

- All records are synthetic and contain no personal, customer, or financial account information.
- Create 24 service-log records with distinct Work Order IDs such as WO-4101 through WO-4124.
- Use five repeating Coordinator names: Avery Cole, Imani Park, Jules Rowan, Morgan Lee, and Tessa Vale.
- Use plausible Service Tier values such as Setup, Repair, Training, Inspection, and Delivery.
- Populate Units with integers from 1 to 8 and Hourly Rate with varied positive decimal values from 42.50 to 125.00 so that Billed Charge calculations produce varied nonzero amounts.
- Format the Hourly Rate column as plain decimal numbers with two decimal places in the initial workbook so formulas entered in Billed Charge do not inherit a currency format.
- Do not include any Pivot Table object, Pivot Table sheet, conditional formatting, or hidden helper data.

| Sheet | Rows | Purpose | Columns |
| --- | ---: | --- | --- |
| Service Log | 24 | Source records for workshop services. Billed Charge is intentionally blank and should be calculated as Units multiplied by Hourly Rate. | Work Order (text), Coordinator (text), Service Tier (text), Units (integer), Hourly Rate (decimal), Billed Charge (decimal) |

Must remain incomplete before recording:

- Do not enter or fill formulas in Billed Charge.
- Do not apply a currency format to Billed Charge.
- Do not create a Pivot Table or a coordinator summary sheet.

Artifact previews:

### Service Log

![Service_Log.png](artifact/previews/Service_Log.png)

## Operator guide

### Demonstration 1

- Skill: `035f41ba-6653-43ab-aa63-c86d449d62e5.skill-02`
- Intent: Present every calculated Billed Charge value in the Service Log as a currency amount using Calc's currency toolbar control.
- Efficiency: Format the first calculated result cell with the toolbar before filling the formula down when that workflow preserves the number format; otherwise select the completed result range once and format it together.
- Visible success: The Billed Charge column shows currency symbols and two-decimal monetary displays rather than unformatted numeric products.

### Demonstration 2

- Skill: `1954cced-e748-45c4-9c26-9855b97fbc5e.skill-02`
- Intent: In the new Pivot Table layout, place Coordinator in the row-label area for a coordinator-level billed-charge summary.
- Efficiency: Move Coordinator directly from the available Pivot Table fields into the Row Fields area, then ensure the billed amount is summarized as a sum.
- Visible success: The resulting Pivot Table displays one row label for each coordinator, with a corresponding total Billed Charge value.

Recording start: The workbook contains only the populated Service Log source sheet; Billed Charge is blank and unformatted, and no Pivot Table exists.

Recording end: Service Log has calculated, currency-formatted Billed Charge values for all 24 records, and a newly created Pivot Table sheet summarizes summed billed charge by Coordinator in row labels.

Allowed variation: The expert may calculate and format the source results before creating the Pivot Table, or use any equivalent Calc workflow that produces the requested source calculations and a new-sheet pivot summary. The destination sheet name and the order of distinct coordinator labels may vary.

## Expected incidental operations

- **substantive_prerequisite:** Enter a Units × Hourly Rate formula for the first Billed Charge record and fill it through the remaining service-log rows. Reason: The calculated monetary measure is needed before it can be formatted and summarized.
- **scaffolding:** Select the Billed Charge result range before using the currency toolbar control. Reason: The requested display format must be applied to the calculated values.
- **substantive_prerequisite:** Select the complete Service Log data range with headers and initiate creation of a Pivot Table on a new worksheet. Reason: A Pivot Table object and destination sheet are required to expose the Row Fields layout.
- **task_specific:** Configure Billed Charge as a summed data/value field in the Pivot Table. Reason: The requested coordinator summary needs a total billed amount alongside the row labels.

## Source-similarity audit

| Measure | Maximum | Most similar source task |
| --- | ---: | --- |
| Lexical sequence similarity | 0.296053 | 1954cced-e748-45c4-9c26-9855b97fbc5e |
| Semantic cosine similarity | 0.449874 | 1954cced-e748-45c4-9c26-9855b97fbc5e |

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
  --reference-task-id reference-task-r01-004
```

The ordinary launcher reads the collected central review file and refuses pending, revision-requested, or rejected tasks.
