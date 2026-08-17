# Workshop Supply Reimbursements

- Reference task: `reference-task-calc-full-r01-016`
- Application: `libreoffice_calc`
- Review decision: `pending`

## Task instruction

Complete the Net Reimbursement calculation for every workshop supply request, keep the internal test requests on rows 6, 13, and 20 out of view without removing them, and show the overall reimbursement total beside the Total Reimbursement label.

## Required skills

### 1. Auto-fill a formula down a contiguous data region

Skill ID: `7e429b8d-a3f0-4ed0-9b58-08957d00b127.skill-02`

Procedure:

1. Select the cell that already contains the formula to propagate.
2. Double-click the small fill handle at the cell's bottom-right corner.
3. Calc fills the formula downward through the contiguous neighboring data rows, adjusting relative references. For example, a formula beginning with `E2` in the selected row becomes `E3`, `E4`, and so on in subsequent rows, while an absolute range such as `$A$2:$B$7` remains fixed.

Efficiency tip: Double-clicking the fill handle is faster than dragging it for long adjacent datasets, but verify that the neighboring column has continuous rows because Calc uses that region to determine the fill length.

Source task: `7e429b8d-a3f0-4ed0-9b58-08957d00b127`

Source instruction: I have a lookup table for the officers of each branch. Please, here is another table in which I need to fill with the officer names according the headoffice (i.e., the branch name). Help me to complete this.

Directly referenced source actions:

- Action 3: <code>`CLICK` F2</code>
- Action 4: <code>`DOUBLE_CLICK` the bottom right corner of cell F2</code>

### 2. Hide multiple non-adjacent rows

Skill ID: `6054afcb-5bab-4702-90a0-b259b5d3217c.skill-01`

Procedure:

1. Click the header of the first row to hide.
2. Hold Ctrl and click each additional row header that should be hidden; for example, select rows 3, 6, 8, and 9 while retaining the earlier selections.
3. Release Ctrl after all target row headers are selected.
4. Right-click any selected row header and choose Hide rows.
5. The selected rows are hidden without deleting their contents; they can later be restored with the corresponding unhide command.

Efficiency tip: Hold Ctrl while selecting all non-adjacent row headers, then use Hide rows once; this is faster and less error-prone than hiding each row individually.

Source task: `6054afcb-5bab-4702-90a0-b259b5d3217c`

Source instruction: Some data are missed by now and are filled by 'N/A' temporarily. Please hide them in the table for now. Do not delete them and filter is no needed.

Directly referenced source actions:

- Action 0: <code>`CLICK` row 3</code>
- Action 1: <code>`KEY_DOWN` Ctrl</code>
- Action 2: <code>`CLICK` row 6</code>
- Action 3: <code>`CLICK` row 8</code>
- Action 4: <code>`CLICK` row 9</code>
- Action 5: <code>`CLICK` row 12</code>
- Action 6: <code>`CLICK` row 14</code>
- Action 7: <code>`CLICK` row 18</code>
- Action 8: <code>`CLICK` row 19</code>
- Action 9: <code>`CLICK` row 20</code>
- Action 10: <code>`CLICK` row 24</code>
- Action 11: <code>`CLICK` row 27</code>
- Action 12: <code>`CLICK` row 32</code>
- Action 13: <code>`CLICK` row 33</code>
- Action 14: <code>`KEY_UP` Ctrl</code>
- Action 15: <code>`RIGHT_CLICK`</code>
- Action 16: <code>`CLICK` Hide rows</code>

### 3. Create a range-total formula in a spreadsheet cell

Skill ID: `0a2e43bf-b26c-4631-a966-af9dfa12c9e5.skill-01`

Procedure:

1. Select the result cell next to the label, type a SUM formula for the cells to total, and confirm it. For example, enter `=SUM(B2:B11)` in B12 to total that column's values from rows 2 through 11.
2. Use relative references when the formula will be copied across columns: `B2:B11` shifts to `C2:C11`, `D2:D11`, and so on when filled right.

Efficiency tip: Enter the formula once in the first result cell; use autofill afterward rather than manually rewriting the formula for each adjacent column.

Source task: `0a2e43bf-b26c-4631-a966-af9dfa12c9e5`

Source instruction: Work out the monthly total sales in a new row called "Total" and then create a line chart to show the results (x-axis be Months).

Directly referenced source actions:

- Action 2: <code>`PRESS` tab</code>
- Action 3: <code>`TYPING` &#x27;=SUM(B2:B11)&#x27;</code>
- Action 4: <code>`PRESS` enter</code>

## Initial artifact

- Domain: Community workshop supply reimbursements
- Workbook: [initial_artifact.xlsx](artifact/initial_artifact.xlsx)
- Blueprint: [artifact_blueprint.json](artifact/artifact_blueprint.json)
- QA report: [artifact_qa.json](artifact/artifact_qa.json)

Initial state:

- The workbook contains one sheet named Reimbursements.
- Row 1 contains headers and rows 2:25 contain reimbursement records.
- The formula seed exists only in G2; the rest of the Net Reimbursement column is intentionally uncalculated.
- Rows 6, 13, and 20 are ordinary visible records at the start and must remain present rather than being deleted.
- Row 26 is a blank spacer row.
- A label Total Reimbursement is present in F27, immediately to the left of the blank result cell G27.

Artifact construction requirements:

- Use entirely synthetic, privacy-safe workshop and supply data.
- Apply ordinary header styling (bold text with a light fill) to the header row and currency number formatting to the monetary columns.
- Populate rows 2 through 25 with varied positive currency values. Ensure every data row has a nonblank value in the adjacent input columns so the data region is contiguous for autofill.
- Set G2 to the seed formula =D2+E2-F2. Leave G3:G25 blank.
- Leave G27 blank for the final range-total formula.

| Sheet | Rows | Purpose | Columns |
| --- | ---: | --- | --- |
| Reimbursements | 27 | Source table for calculating per-request net reimbursements, concealing selected internal test records, and reporting the overall reimbursement total. | Request ID (text), Workshop (text), Supply Category (text), Materials Cost (currency), Shipping Cost (currency), Sponsor Credit (currency), Net Reimbursement (currency) |

Must remain incomplete before recording:

- Do not pre-fill G3:G25 with formulas or values.
- Do not pre-enter a formula in G27.
- Do not hide rows 6, 13, or 20 initially.
- Do not delete, filter out, or alter the values of any reimbursement record.

Artifact previews:

### Reimbursements

![Reimbursements.png](artifact/previews/Reimbursements.png)

## Operator guide

### Demonstration 1

- Skill: `7e429b8d-a3f0-4ed0-9b58-08957d00b127.skill-02`
- Intent: Propagate the Net Reimbursement formula from the seeded first record through all remaining contiguous reimbursement records.
- Efficiency: Use the seeded formula in G2 and the fill handle’s double-click behavior; the neighboring data columns are continuous through row 25.
- Visible success: G3:G25 display calculated currency results with row-relative formulas, while G2 remains the original seed.

### Demonstration 2

- Skill: `6054afcb-5bab-4702-90a0-b259b5d3217c.skill-01`
- Intent: Hide the three internal test reimbursement records on rows 6, 13, and 20 without deleting their data.
- Efficiency: Use a single multi-selection of row headers and issue the hide command once rather than hiding records individually.
- Visible success: The row-number sequence visibly skips 6, 13, and 20, and the surrounding records remain in place.

### Demonstration 3

- Skill: `0a2e43bf-b26c-4631-a966-af9dfa12c9e5.skill-01`
- Intent: Calculate the overall reimbursement amount in G27 next to the Total Reimbursement label.
- Efficiency: Enter one SUM formula referencing the complete Net Reimbursement data range; the blank spacer row prevents accidental inclusion of the total cell.
- Visible success: G27 shows a currency total produced by a range-total formula covering G2:G25.

Recording start: The Reimbursements sheet is visible with populated source records, only G2 containing the seeded formula, and all rows visible.

Recording end: All reimbursement records have calculated net values, rows 6, 13, and 20 are hidden, and G27 contains the range total for G2:G25.

Allowed variation: The expert may calculate and verify the total before or after hiding the specified records, provided all per-record net formulas are filled, the required records are hidden rather than removed, and the total formula covers the complete record range.

## Expected incidental operations

- **scaffolding:** Navigate to the Reimbursements sheet and select the seeded formula cell and later the total-result cell. Reason: Cell selection is needed to propagate the existing calculation and place the requested total.
- **task_specific:** Enter a SUM range formula in G27 that totals the Net Reimbursement results from the record rows. Reason: This is the natural calculation needed to produce the requested overall reimbursement total.
- **scaffolding:** Select the specified non-adjacent row headers using a multi-selection modifier before applying the row-hide command. Reason: The requested records must be concealed together while preserving their contents.

## Source-similarity audit

| Measure | Maximum | Most similar source task |
| --- | ---: | --- |
| Lexical sequence similarity | 0.317618 | 0bf05a7d-b28b-44d2-955a-50b41e24012a |
| Semantic cosine similarity | 0.454457 | 035f41ba-6653-43ab-aa63-c86d449d62e5 |

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
  --reference-task-id reference-task-calc-full-r01-016
```

The ordinary launcher reads the collected central review file and refuses pending, revision-requested, or rejected tasks.
