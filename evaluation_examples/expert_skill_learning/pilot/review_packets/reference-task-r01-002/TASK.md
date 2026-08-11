# Workshop Grant Reconciliation

- Reference task: `reference-task-r01-002`
- Application: `libreoffice_calc`
- Review decision: `pending`

## Task instruction

Reconcile the workshop grants by calculating each workshop's Net Allocation after reversals, recoveries, and all listed delivery costs, then create a new-sheet Pivot Table that shows the total Net Allocation for each Service Area.

## Required skills

### 1. Build a row formula that subtracts a range total

Skill ID: `035f41ba-6653-43ab-aa63-c86d449d62e5.skill-01`

Procedure:

1. Select the output cell in the row to calculate.
2. Enter and commit a formula that subtracts individual values and a contiguous range total from a starting value. For example, use `=B2-C2-D2-SUM(F2:H2)`.
3. When reused on another table, replace the cell references with the relevant sale, return, adjustment, and expense columns.

Efficiency tip: Use a single SUM range for adjacent expense columns instead of subtracting each expense cell separately.

Source task: `035f41ba-6653-43ab-aa63-c86d449d62e5`

Source instruction: Help me fill in the Gross profit column by subtracting all the available expenses including discounts, allowances, material and labor charges, and overhead from the actual sale, i.e., the sales after deducting the returns. Then under column A named "Year_Profit" in a new sheet, display the Year Column in Sheet 1 as text appended by a "_" with the corresponding integer digits of Gross Profit value.

Directly referenced source actions:

- Action 0: <code>`CLICK` on cell J2</code>
- Action 1: <code>`TYPING` &#x27;=B2-C2-D2-SUM(F2:H2)&#x27;</code>

### 2. Create a Pivot Table from selected worksheet data

Skill ID: `1954cced-e748-45c4-9c26-9855b97fbc5e.skill-01`

Procedure:

1. Select the data to summarize. For example, click a column header to use that entire column as the source when the column contains the needed records.
2. Click the Pivot Table toolbar icon to open the Pivot Table creation workflow.
3. Confirm the detected source selection, for example by pressing Enter when the proposed range is correct.

Efficiency tip: Select the complete contiguous source range before launching the command when possible; this avoids correcting an automatically detected range in the Pivot Table source dialog.

Source task: `1954cced-e748-45c4-9c26-9855b97fbc5e`

Source instruction: Create a Pivot Table in a new sheet (Sheet2) to count how many times each "Invoice No." appears.

Directly referenced source actions:

- Action 0: <code>`CLICK` on grey cell box A for selecting entire column</code>
- Action 1: <code>`CLICK` on pivot table icon</code>
- Action 2: <code>`PRESS` enter</code>

## Initial artifact

- Domain: community workshop grant reconciliation
- Workbook: [initial_artifact.xlsx](artifact/initial_artifact.xlsx)
- Blueprint: [artifact_blueprint.json](artifact/artifact_blueprint.json)
- QA report: [artifact_qa.json](artifact/artifact_qa.json)

Initial state:

- The workbook title is "Workshop Grant Reconciliation".
- Only the "Funding Log" sheet exists initially.
- The data range is contiguous from A1:I17. Row 1 contains headers and rows 2-17 contain the provided source values.
- Column I is headed "Net Allocation" but cells I2:I17 are blank.
- Columns A through H contain: Workshop ID, Award Received, Credit Reversal, Asset Recovery, Service Area, Venue Cost, Materials Cost, and Facilitator Cost, respectively.

Artifact construction requirements:

- All records are synthetic and privacy-safe. Create a single worksheet named "Funding Log" with a bold, lightly shaded header row, autofilter enabled on A1:I17, and 16 data records in rows 2-17.
- Populate rows 2-17 with the following tab-separated values, in the stated column order: W-101	18400	350	125	Northside	2100	980	640; W-102	22150	0	300	Northside	1860	1425	720; W-103	16750	225	0	Harbor	1940	760	515; W-104	19600	410	185	Harbor	1725	1190	680; W-105	23800	0	450	Meadow	2450	1380	940; W-106	15450	190	75	Meadow	1280	845	390; W-107	20700	600	220	Northside	2185	1110	765; W-108	18100	0	160	Harbor	1560	920	575; W-109	24900	525	0	Meadow	2690	1540	880; W-110	17200	140	210	Northside	1495	875	460; W-111	21450	0	330	Harbor	2050	1260	710; W-112	15900	285	95	Meadow	1375	690	425; W-113	22800	365	140	Northside	2320	1450	830; W-114	18850	0	250	Harbor	1680	1040	605; W-115	20350	455	110	Meadow	1905	1175	695; W-116	17600	210	0	Northside	1430	815	480.
- Format columns B:D and F:I as currency with zero decimal places. Keep column E as text. Set reasonable widths so every header and ordinary value is readable.
- Do not seed any formulas in column I and do not create a pivot table, pivot output sheet, conditional formatting, charts, or summary values.

| Sheet | Rows | Purpose | Columns |
| --- | ---: | --- | --- |
| Funding Log | 16 | Source reconciliation records whose calculated net allocations will be summarized by service area. | Workshop ID (text), Award Received (currency), Credit Reversal (currency), Asset Recovery (currency), Service Area (text), Venue Cost (currency), Materials Cost (currency), Facilitator Cost (currency), Net Allocation (currency) |

Must remain incomplete before recording:

- Do not prefill a Net Allocation formula or values in any row.
- Do not pre-create any native Pivot Table or a separate summary sheet.
- Do not add unrelated calculations, charts, or extra datasets.

Artifact previews:

### Funding Log

![Funding_Log.png](artifact/previews/Funding_Log.png)

## Operator guide

### Demonstration 1

- Skill: `035f41ba-6653-43ab-aa63-c86d449d62e5.skill-01`
- Intent: Calculate Net Allocation as the award less the credit reversal, asset recovery, and combined venue-to-facilitator costs for each workshop record.
- Efficiency: Enter the expression once in the first data row using one SUM range for the three adjacent cost columns, then fill it down the populated table.
- Visible success: I2 contains a row-relative formula equivalent to =B2-C2-D2-SUM(F2:H2), and I2:I17 display currency results with references adjusted by row.

### Demonstration 2

- Skill: `1954cced-e748-45c4-9c26-9855b97fbc5e.skill-01`
- Intent: Create a native Pivot Table on a new worksheet that summarizes the sum of Net Allocation for each Service Area.
- Efficiency: Start from the full contiguous table so the detected Pivot Table source already contains the headers, all records, and the calculated measure.
- Visible success: A separate pivot output sheet visibly lists Northside, Harbor, and Meadow with a summed Net Allocation value for each.

Recording start: The workbook opens to the single Funding Log sheet with the populated source table and a blank Net Allocation column.

Recording end: Funding Log retains all 16 records with completed Net Allocation formulas, and a new worksheet contains a native Pivot Table showing total Net Allocation grouped by Service Area.

Allowed variation: The expert may use formula fill, copy/paste, or another efficient equivalent to populate the calculated column, and may use any suitable native LibreOffice Calc Pivot Table workflow and layout so long as the completed workbook visibly provides the requested summed service-area summary.

## Expected incidental operations

- **scaffolding:** Extend the completed Net Allocation formula from the first record through the remaining populated records. Reason: Every record needs a calculated value for the requested service-area summary.
- **substantive_prerequisite:** Use the complete contiguous Funding Log data range, including the calculated Net Allocation column, as the Pivot Table source. Reason: The pivot summary must include both the grouping field and calculated measure.
- **task_specific:** Configure the new Pivot Table to group by Service Area and aggregate Net Allocation as a sum on a new worksheet. Reason: This produces the requested reconciliation summary rather than an unconfigured pivot object.

## Source-similarity audit

| Measure | Maximum | Most similar source task |
| --- | ---: | --- |
| Lexical sequence similarity | 0.319018 | 1954cced-e748-45c4-9c26-9855b97fbc5e |
| Semantic cosine similarity | 0.437947 | 035f41ba-6653-43ab-aa63-c86d449d62e5 |

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
  --reference-task-id reference-task-r01-002
```

The ordinary launcher reads the collected central review file and refuses pending, revision-requested, or rejected tasks.
