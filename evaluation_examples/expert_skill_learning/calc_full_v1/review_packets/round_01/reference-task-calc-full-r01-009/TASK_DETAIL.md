# Workshop Allocation Review

- Reference task: `reference-task-calc-full-r01-009`
- Application: `libreoffice_calc`
- Review decision: `pending`

## Task instruction

Complete the workshop allocation review: add a standardized two-decimal narrative for every allocation record, make the dark report heading readable with white text, and use the Allocation Summary sheet to show each zone’s share of all completed units.

## Required skills

### 1. Set a cell's font color from the color palette

Skill ID: `30e3e107-1cfb-46ee-a755-2cd080d7ba6a.skill-04`

Procedure:

1. With the target cell or merged cell selected, open the font-color dropdown.
2. Choose the desired palette color; for example, choose white for text that needs contrast against a dark fill.

Efficiency tip: Apply font color while the target cell remains selected after fill formatting, avoiding a separate reselection.

Source task: `30e3e107-1cfb-46ee-a755-2cd080d7ba6a`

Source instruction: Please create a new sheet. Keep its sheet name as "Sheet2". Merge cells A1:C1 in the new sheet and write "Demographic Profile" with blue (#0000ff) fill and bold white text. Then I want to create three pivot tables to show the percentage of Sex, Civil Status, and Highest Educational Attainment. They should be stacked one by one in Sheet2, each separated with a blank line.

Directly referenced source actions:

- Action 13: <code>`CLICK` font color arrow icon, which is to left of bucket</code>
- Action 14: <code>`CLICK` top right color in the color palette (white)</code>

### 2. Build a formatted text-concatenation formula with fixed decimal values

Skill ID: `4de54231-e4b5-49e3-b2ba-61a0bec721c0.skill-02`

Procedure:

1. In the first output-row cell, enter a concatenation formula that joins labels, separators, and formatted cell values. For example: =$A$1&": "&FIXED(A2,2)&", "&$B$1&": "&FIXED(B2,2)&", "&$C$1&": "&FIXED(C2,2)&", "&$D$1&": "&FIXED(D2,2)
2. Use & to join text fragments and cell results. FIXED(A2,2) converts the value in A2 to text with two decimal places; apply the same pattern to each value being joined.
3. In $A$1, the first $ fixes column A and the second $ fixes row 1, so the header reference remains A1 when copied. References such as A2 have no absolute markers, so their row changes when filled downward.

Efficiency tip: Use one concatenation formula with header references rather than manually assembling text row by row. Keep header cells absolute so the labels remain fixed when the formula is filled down.

Source task: `4de54231-e4b5-49e3-b2ba-61a0bec721c0`

Source instruction: I have compute the acceleration in row 2 and I want you to fill out other rows for column B and D. Next concatenate the values from columns A to D, including their headers (the pattern is "Header: cell value, ..., Header: cell value"), into a new column named "Combined Data" for all rows. In the new column, only keep 2 decimal digits.

Directly referenced source actions:

- Action 7: <code>`TYPING` &#x27;=$A$1&amp;&quot;: &quot;&amp;FIXED(A2,2)&amp;&quot;, &quot;&amp;$B$1&amp;&quot;: &quot;&amp;FIXED(B2,2)&amp;&quot;, &quot;&amp;$C$1&amp;&quot;: &quot;&amp;FIXED(C2,2)&amp;&quot;, &quot;&amp;$D$1&amp;&quot;: &quot;&amp;FIXED(D2,2)&#x27;</code>

### 3. Display Pivot Table values as a percentage of the total

Skill ID: `30e3e107-1cfb-46ee-a755-2cd080d7ba6a.skill-09`

Procedure:

1. In the data-field options dialog, open the displayed-value or Show Values As controls.
2. Open the Type dropdown, which may initially show Normal, and choose `% of total`.
3. Confirm the data-field options using OK or Enter. The value field will show each category's share of the overall total.

Efficiency tip: Use the built-in percentage display calculation rather than adding helper formulas outside the Pivot Table.

Source task: `30e3e107-1cfb-46ee-a755-2cd080d7ba6a`

Source instruction: Please create a new sheet. Keep its sheet name as "Sheet2". Merge cells A1:C1 in the new sheet and write "Demographic Profile" with blue (#0000ff) fill and bold white text. Then I want to create three pivot tables to show the percentage of Sex, Civil Status, and Highest Educational Attainment. They should be stacked one by one in Sheet2, each separated with a blank line.

Directly referenced source actions:

- Action 26: <code>`CLICK` &#x27;displayed value&#x27; dropdown</code>
- Action 27: <code>`CLICK` Normal dropdown next to &#x27;Type&#x27;</code>
- Action 28: <code>`CLICK` &#x27;% of total&#x27;</code>
- Action 29: <code>`CLICK` ok</code>
- Action 46: <code>`CLICK` &#x27;displayed value&#x27; dropdown</code>
- Action 47: <code>`CLICK` Normal dropdown next to &#x27;Type&#x27;</code>
- Action 48: <code>`CLICK` &#x27;% of total&#x27;</code>
- Action 49: <code>`PRESS` enter</code>
- Action 66: <code>`CLICK` &#x27;displayed value&#x27; dropdown</code>
- Action 67: <code>`CLICK` Normal dropdown next to &#x27;Type&#x27;</code>
- Action 68: <code>`CLICK` &#x27;% of total&#x27;</code>
- Action 69: <code>`PRESS` enter</code>

## Initial artifact

- Domain: community workshop supply allocation review
- Workbook: [initial_artifact.xlsx](artifact/initial_artifact.xlsx)
- Blueprint: [artifact_blueprint.json](artifact/artifact_blueprint.json)
- QA report: [artifact_qa.json](artifact/artifact_qa.json)

Initial state:

- The workbook opens with two sheets: Activity Log and Allocation Summary.
- Activity Log contains a contiguous source table in A1:E19, with headers in row 1 and 18 populated records beneath.
- Allocation Summary contains only the prefilled dark title in A1 and is otherwise blank.
- No formulas are present in Activity Log column E.
- No native Pivot Table exists anywhere in the workbook.
- The Allocation Summary title's font is not white at the start.

Artifact construction requirements:

- Use entirely synthetic, privacy-safe workshop allocation records. Do not use real people, organizations, addresses, or identifiers.
- Populate 18 data records in Activity Log rows 2-19. Use four zones repeatedly (North Hall, Garden Room, Studio Bay, River Annex) so a Pivot Table grouped by Zone has multiple source records per group.
- Use positive decimal values for Scheduled Units, Completed Units, and Rework Units. Completed Units should vary by row and have a nonzero grand total.
- Examples of synthetic batch codes may use the pattern WSA-201 through WSA-218. Do not use any literals from the source tasks.
- Apply normal table header styling to Activity Log row 1. The Record Summary cells must be blank at generation time.
- On Allocation Summary, style A1 with a dark navy fill such as #203864 and bold text, but leave its font color at the default dark/black color so changing it to white is still required. A1 contains the text "Workshop Allocation Share".
- Leave enough blank space beginning at A3 on Allocation Summary for a native Pivot Table result. Do not create a native Pivot Table during generation.

| Sheet | Rows | Purpose | Columns |
| --- | ---: | --- | --- |
| Activity Log | 18 | Source records for individual workshop supply allocations and the required per-record narrative output. | Batch Code (text), Scheduled Units (decimal), Completed Units (decimal), Rework Units (decimal), Record Summary (text) |
| Allocation Summary | 10 | Blank destination for a zone-level native Pivot Table and its existing report title. | Reserved blank summary area (text) |

Must remain incomplete before recording:

- Do not prefill or seed the Record Summary formula or any resulting text in Activity Log!E2:E19.
- Do not preconfigure a Pivot Table, a Pivot Table percentage display calculation, or any substitute summary formulas/charts.
- Do not change the Allocation Summary!A1 font color to white before the recorded task.

Artifact previews:

### Activity Log

![Activity_Log.png](artifact/previews/Activity_Log.png)

### Allocation Summary

![Allocation_Summary.png](artifact/previews/Allocation_Summary.png)

## Operator guide

### Demonstration 1

- Skill: `4de54231-e4b5-49e3-b2ba-61a0bec721c0.skill-02`
- Intent: In Activity Log!E2, create a reusable concatenation formula that produces a labeled record narrative from Batch Code, Scheduled Units, Completed Units, and Rework Units. The three numeric values must be rendered with exactly two decimal places; copy the formula through E19.
- Efficiency: Use absolute references for the row-1 headers and relative references for the current data row, then fill the formula down in one operation.
- Visible success: Each Record Summary cell contains a readable label-and-value string, such as a batch code followed by the three unit measures, and every numeric measure visibly has two decimal places.

### Demonstration 2

- Skill: `30e3e107-1cfb-46ee-a755-2cd080d7ba6a.skill-04`
- Intent: Change the font color of the existing dark-filled "Workshop Allocation Share" title in Allocation Summary!A1 to white.
- Efficiency: Apply the color while A1 is selected; the existing dark fill provides immediate contrast feedback.
- Visible success: The A1 title text is visibly white and legible against its dark navy background.

### Demonstration 3

- Skill: `30e3e107-1cfb-46ee-a755-2cd080d7ba6a.skill-09`
- Intent: Create the native zone-level Pivot Table from Activity Log, summarize Completed Units by Zone, and set its displayed data values to percentage of the overall total.
- Efficiency: Use the data-field display option for percentage of the total instead of calculating shares in cells outside the Pivot Table.
- Visible success: Allocation Summary shows a native Pivot Table with one row per Zone and Completed Units represented as percentages; the category percentages collectively account for the grand total.

Recording start: The workbook has the populated Activity Log source table, a blank Record Summary output column, and a blank Allocation Summary area with a dark-filled, non-white title.

Recording end: Activity Log has completed Record Summary narratives for all 18 records with fixed two-decimal numeric text. Allocation Summary retains its dark-filled white-font title and displays a native Pivot Table that shows each Zone's share of total Completed Units as percentages.

Allowed variation: The expert may use LibreOffice Calc menus, toolbar controls, keyboard shortcuts, or equivalent dialogs. The Pivot Table may be positioned at A3 or another clearly non-overlapping location on Allocation Summary, provided the title remains visible and the resulting zone values are shown as percentages of the overall Completed Units total.

## Expected incidental operations

- **scaffolding:** Fill the first completed Record Summary formula down through the remaining source records. Reason: A reusable row-relative formula must produce one standardized narrative for every allocation record.
- **substantive_prerequisite:** Select the contiguous Activity Log source range and create a native Pivot Table in the reserved Allocation Summary destination area. Reason: A native Pivot Table is required before its value field can be displayed as a share of the grand total.
- **substantive_prerequisite:** Configure the Pivot Table with Zone as the row grouping and the sum of Completed Units as its data field. Reason: This establishes the requested zone-level allocation measure to which the percentage-of-total display is applied.

## Source-similarity audit

| Measure | Maximum | Most similar source task |
| --- | ---: | --- |
| Lexical sequence similarity | 0.335802 | 1de60575-bb6e-4c3d-9e6a-2fa699f9f197 |
| Semantic cosine similarity | 0.396176 | 04d9aeaf-7bed-4024-bedb-e10e6f00eb7f |

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
  --reference-task-id reference-task-calc-full-r01-009
```

The ordinary launcher reads the collected central review file and refuses pending, revision-requested, or rejected tasks.
