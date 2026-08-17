# Repair Fair Handoff

- Reference task: `reference-task-calc-full-r01-014`
- Application: `libreoffice_calc`
- Review decision: `pending`

## Task instruction

Prepare the Repair Fair Handoff sheet for the event coordinator: present the coverage targets in a kiosk-by-shift layout, and add a Pivot Table that shows how many check-in ticket records were logged at each kiosk.

## Required skills

### 1. Paste a copied cell range with rows and columns transposed

Skill ID: `eb03d19a-b88d-4de4-8a64-ca0ac66f426b.skill-01`

Procedure:

1. Select the rectangular source range to transpose. For example, drag from B2 through F5.
2. Copy the selected range with Ctrl+C.
3. Right-click the destination's top-left cell, such as B8, open Paste Special, and choose Transpose.
4. Calc pastes the copied values and formulas with the original rows becoming columns and the original columns becoming rows.

Efficiency tip: Copy the full source range once, then use Paste Special directly at the destination's top-left cell; do not manually rearrange rows and columns.

Source task: `eb03d19a-b88d-4de4-8a64-ca0ac66f426b`

Source instruction: Apply matrix transposition to the table in B2:F5 and paste the transposed table at B8 (i.e., the top-left cell of the transposed table should be at B8)

Directly referenced source actions:

- Action 0: <code>`MOVE_TO` B2</code>
- Action 1: <code>`DRAG_TO` F5</code>
- Action 2: <code>`HOTKEY` &#x27;Ctrl + C&#x27; to copy the table.</code>
- Action 3: <code>`RIGHT_CLICK` cell B8.</code>
- Action 4: <code>`MOVE_TO` Paste Special...</code>
- Action 5: <code>`CLICK` Transpose</code>

### 2. Count occurrences in a Pivot Table data field

Skill ID: `30e3e107-1cfb-46ee-a755-2cd080d7ba6a.skill-08`

Procedure:

1. Double-click the field entry in the Pivot Table Data Fields area to open its data-field options.
2. Choose Count as the aggregation. This counts non-empty occurrences of the selected field rather than summing numeric values.

Efficiency tip: Configure the aggregation immediately after adding the data field, while its settings dialog is easy to access from the Data Fields area.

Source task: `30e3e107-1cfb-46ee-a755-2cd080d7ba6a`

Source instruction: Please create a new sheet. Keep its sheet name as "Sheet2". Merge cells A1:C1 in the new sheet and write "Demographic Profile" with blue (#0000ff) fill and bold white text. Then I want to create three pivot tables to show the percentage of Sex, Civil Status, and Highest Educational Attainment. They should be stacked one by one in Sheet2, each separated with a blank line.

Directly referenced source actions:

- Action 24: <code>`DOUBLE_CLICK on sex box in data fields</code>
- Action 25: <code>`CLICK` Count</code>
- Action 44: <code>`DOUBLE_CLICK on civil status box in data fields</code>
- Action 45: <code>`CLICK` Count</code>
- Action 64: <code>`DOUBLE_CLICK on Highest Educational Attainment box in data fields</code>
- Action 65: <code>`CLICK` Count</code>

## Initial artifact

- Domain: community repair fair check-in handoff
- Workbook: [initial_artifact.xlsx](artifact/initial_artifact.xlsx)
- Blueprint: [artifact_blueprint.json](artifact/artifact_blueprint.json)
- QA report: [artifact_qa.json](artifact/artifact_qa.json)

Initial state:

- The workbook opens with the Handoff Summary sheet active.
- Handoff Summary is blank and will receive the transposed coverage layout and the Pivot Table.
- Coverage Setup contains a completed rectangular source matrix in A1:D4: headers in row 1 are Shift, Kiosk North, Kiosk Central, and Kiosk South; rows 2-4 are Morning, Midday, and Afternoon with small integer volunteer-coverage targets.
- CheckIn Log contains a normal contiguous table in A1:D31 with headers Check-in Time, Kiosk, Ticket Code, and Repair Type. Ticket Code is text and populated for every record; Kiosk contains Kiosk North, Kiosk Central, or Kiosk South.
- No formulas are required in the initial workbook.

Artifact construction requirements:

- All names, ticket codes, kiosks, and check-in records are synthetic and privacy-safe.
- Populate CheckIn Log with 30 realistic records across three kiosks so that Ticket Code is non-empty in every data row. Repeat some ticket codes to make the count-based summary useful.
- Use ordinary header styling only. Do not create a native Pivot Table, conditional-format rule, chart, filter, or transposed output in the initial workbook.
- Leave sufficient empty area on the Handoff Summary sheet for both requested outputs.

| Sheet | Rows | Purpose | Columns |
| --- | ---: | --- | --- |
| Coverage Setup | 40 | Provides the 4-by-4 shift-by-kiosk coverage matrix to be transposed for the handoff view. | Shift (text), Kiosk North (integer), Kiosk Central (integer), Kiosk South (integer) |
| CheckIn Log | 30 | Provides check-in records for a Pivot Table that counts tickets by kiosk. | Check-in Time (date), Kiosk (text), Ticket Code (text), Repair Type (text) |
| Handoff Summary | 10 | Blank destination sheet for the transposed coverage layout and the kiosk check-in count Pivot Table. | (blank initial sheet) (text) |

Must remain incomplete before recording:

- Do not transpose or otherwise recreate the Coverage Setup matrix on Handoff Summary.
- Do not create a Pivot Table or any other summary of the CheckIn Log data.
- Do not preconfigure the Pivot Table aggregation; the recorded task must visibly set the Ticket Code data field to Count.

Artifact previews:

### CheckIn Log

![CheckIn_Log.png](artifact/previews/CheckIn_Log.png)

### Coverage Setup

![Coverage_Setup.png](artifact/previews/Coverage_Setup.png)

### Handoff Summary

![Handoff_Summary.png](artifact/previews/Handoff_Summary.png)

## Operator guide

### Demonstration 1

- Skill: `eb03d19a-b88d-4de4-8a64-ca0ac66f426b.skill-01`
- Intent: Transpose the complete shift-by-kiosk coverage matrix from Coverage Setup into the upper area of Handoff Summary.
- Efficiency: Copy the entire labeled source block once and use Paste Special with the transpose option at the chosen destination rather than retyping or rearranging values.
- Visible success: The pasted layout has kiosks listed vertically and shifts across the top, with all coverage target values preserved in their rotated positions.

### Demonstration 2

- Skill: `30e3e107-1cfb-46ee-a755-2cd080d7ba6a.skill-08`
- Intent: Create a kiosk-level Pivot Table from CheckIn Log and set the Ticket Code data field to count non-empty check-in occurrences.
- Efficiency: After adding Ticket Code to the Pivot Table data fields, open its data-field settings immediately and select Count rather than accepting a numeric aggregation default.
- Visible success: The Pivot Table lists each kiosk and a count-based Ticket Code result; its data-field label indicates Count rather than Sum.

Recording start: The workbook is open on the blank Handoff Summary sheet; Coverage Setup and CheckIn Log contain the prepared source data only.

Recording end: Handoff Summary visibly contains a transposed coverage-target layout and a separate Pivot Table counting Ticket Code check-ins for each kiosk.

Allowed variation: The expert may choose any non-overlapping placement on Handoff Summary, provided the transposed matrix is clearly identifiable and the Pivot Table visibly reports Ticket Code occurrence counts by Kiosk. Equivalent Calc Pivot Table creation workflows are acceptable.

## Expected incidental operations

- **scaffolding:** Navigate between the source sheets and the blank Handoff Summary sheet. Reason: The two requested deliverables use separate source ranges and share a designated presentation sheet.
- **task_specific:** Create a Pivot Table from the CheckIn Log range and place it in an unused area of Handoff Summary. Reason: A Pivot Table object is required before its row field and count data field can be configured.
- **substantive_prerequisite:** Assign Kiosk as the Pivot Table row field and Ticket Code as its data field. Reason: These field placements are necessary so the requested occurrence count is displayed by kiosk.

## Source-similarity audit

| Measure | Maximum | Most similar source task |
| --- | ---: | --- |
| Lexical sequence similarity | 0.359673 | 1de60575-bb6e-4c3d-9e6a-2fa699f9f197 |
| Semantic cosine similarity | 0.327701 | 51719eea-10bc-4246-a428-ac7c433dd4b3 |

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
  --reference-task-id reference-task-calc-full-r01-014
```

The ordinary launcher reads the collected central review file and refuses pending, revision-requested, or rejected tasks.
