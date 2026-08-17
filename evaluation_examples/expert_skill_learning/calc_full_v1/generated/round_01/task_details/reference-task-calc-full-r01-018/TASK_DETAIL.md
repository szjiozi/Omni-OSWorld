# Workshop Attendance Register

- Reference task: `reference-task-calc-full-r01-018`
- Application: `libreoffice_calc`
- Review decision: `pending`

## Task instruction

Prepare the workshop attendance register by assigning each attendee a sequential text check-in tag, then add a Pivot Table report that shows how many attendees are registered in each workshop track.

## Required skills

### 1. Create a row-based text sequence formula

Skill ID: `7efeb4b1-3d19-4762-b163-63328d66303b.skill-01`

Procedure:

1. Select the first output cell in the sequence column, for example B2.
2. Type a concatenation formula such as `="No. " & ROW(B2)-1` and press Enter. `ROW(B2)` returns 2, so subtracting 1 makes the first result `No. 1`.
3. Adjust the referenced starting row or offset when the sequence begins elsewhere; for example, in row 5 use `="No. " & ROW(B5)-4` to begin at `No. 1`.

Efficiency tip: Enter the formula once in the first data row; do not manually type a separate sequence label in every row.

Source task: `7efeb4b1-3d19-4762-b163-63328d66303b`

Source instruction: Fill the Sequence Numbers as "No. #" in the "Seq No." column

Directly referenced source actions:

- Action 0: <code>`CLICK` B2</code>
- Action 1: <code>`TYPING` =&quot;No. &quot; &amp; ROW(B2)-1 </code>
- Action 2: <code>`PRESS` Enter.</code>

### 2. Place a field in Pivot Table row and data areas

Skill ID: `30e3e107-1cfb-46ee-a755-2cd080d7ba6a.skill-07`

Procedure:

1. In the Pivot Table layout dialog, locate a categorical field in Available Fields.
2. Drag the field to Row Fields to list each distinct category as a row.
3. Drag the same field to Data Fields to create a value calculation for those categories. For example, a field can be placed in both areas to show categories and their counts.

Efficiency tip: Drag the same field directly from Available Fields into each required area instead of searching for it again through menus.

Source task: `30e3e107-1cfb-46ee-a755-2cd080d7ba6a`

Source instruction: Please create a new sheet. Keep its sheet name as "Sheet2". Merge cells A1:C1 in the new sheet and write "Demographic Profile" with blue (#0000ff) fill and bold white text. Then I want to create three pivot tables to show the percentage of Sex, Civil Status, and Highest Educational Attainment. They should be stacked one by one in Sheet2, each separated with a blank line.

Directly referenced source actions:

- Action 20: <code>`MOVE_TO` &#x27;Sex&#x27; in available fields</code>
- Action 21: <code>`DRAG_TO` box in row fields</code>
- Action 22: <code>`MOVE_TO` &#x27;Sex&#x27; in available fields</code>
- Action 23: <code>`DRAG_TO` box in data fields</code>
- Action 40: <code>`MOVE_TO` &#x27;Civil Status&#x27; in available fields</code>
- Action 41: <code>`DRAG_TO` box in row fields</code>
- Action 42: <code>`MOVE_TO` &#x27;Civil Status&#x27; in available fields</code>
- Action 43: <code>`DRAG_TO` box in data fields</code>
- Action 60: <code>`MOVE_TO` &#x27;Highest Educational Attainment&#x27; in available fields</code>
- Action 61: <code>`DRAG_TO` box in row fields</code>
- Action 62: <code>`MOVE_TO` &#x27;Highest Educational Attainment&#x27; in available fields</code>
- Action 63: <code>`DRAG_TO` box in data fields</code>

## Initial artifact

- Domain: Community workshop attendance
- Workbook: [initial_artifact.xlsx](artifact/initial_artifact.xlsx)
- Blueprint: [artifact_blueprint.json](artifact/artifact_blueprint.json)
- QA report: [artifact_qa.json](artifact/artifact_qa.json)

Initial state:

- The workbook opens on the Attendance Log sheet.
- Attendance Log contains one header row and 24 attendance records in rows 2 through 25.
- The Check-in Tag column is visibly blank for every record.
- The Workshop Track field contains repeated categorical values suitable for a frequency Pivot Table.
- No native Pivot Table exists anywhere in the workbook.

Artifact construction requirements:

- All names, workshop titles, and locations are synthetic and privacy-safe.
- Create the source data as a plain cell range rather than a native Excel/Calc table.
- Use ordinary header styling (bold text with a light fill) for the source range.
- Leave the Check-in Tag cells blank; do not seed formulas in that column.
- Do not create a Pivot Table, a summary sheet, conditional formatting, charts, or filters.

| Sheet | Rows | Purpose | Columns |
| --- | ---: | --- | --- |
| Attendance Log | 24 | Source attendance records for labeling and track-frequency reporting. | Session Date (date), Participant Alias (text), Workshop Track (text), Check-in Tag (text), Registration Type (text) |

Must remain incomplete before recording:

- Check-in Tag must not already contain sequence labels or formulas.
- A Pivot Table summarizing Workshop Track must not already exist.
- Do not add manually typed per-record check-in tags as a substitute for the row-based formula.

Artifact previews:

### Attendance Log

![Attendance_Log.png](artifact/previews/Attendance_Log.png)

## Operator guide

### Demonstration 1

- Skill: `7efeb4b1-3d19-4762-b163-63328d66303b.skill-01`
- Intent: Generate sequential text check-in tags beginning at 1 for all attendance records using a row-based concatenation formula.
- Efficiency: Write the formula once in the first Check-in Tag data cell using a ROW-based offset appropriate to row 2, then fill it through the contiguous record range.
- Visible success: Every record in Check-in Tag displays a consecutively numbered text label, beginning with the first record as number 1 and ending with number 24.

### Demonstration 2

- Skill: `30e3e107-1cfb-46ee-a755-2cd080d7ba6a.skill-07`
- Intent: Create a Pivot Table that lists each Workshop Track and counts its attendance records by placing Workshop Track in both row and data areas.
- Efficiency: Drag Workshop Track from the available fields into both the row area and the data area directly, rather than selecting it once and searching for it again.
- Visible success: The Pivot Table visibly has one row per distinct workshop track and an adjacent count/value column showing the number of records for each track.

Recording start: The workbook contains only the populated Attendance Log source range, with Check-in Tag blank and no Pivot Table.

Recording end: The Attendance Log has formula-generated sequential Check-in Tags for all 24 records, and a visible Pivot Table reports the count for each Workshop Track.

Allowed variation: The expert may create the Pivot Table on a newly inserted sheet or in an unused area, and may use fill-down, a fill handle, or another equivalent Calc method to extend the formula. The displayed count label may follow Calc's automatic wording.

## Expected incidental operations

- **substantive_prerequisite:** Select the complete source range including headers when creating the Pivot Table. Reason: The Pivot Table needs the attendance records and their field names as its source.
- **scaffolding:** Fill or copy the initial row-based Check-in Tag formula down through the remaining attendance rows. Reason: The sequence formula must be applied to each record rather than left only in the first data row.
- **task_specific:** Create the Pivot Table on a new worksheet or a clear unused location in the workbook. Reason: A separate report location keeps the attendance log usable and makes the summary visible.

## Source-similarity audit

| Measure | Maximum | Most similar source task |
| --- | ---: | --- |
| Lexical sequence similarity | 0.360856 | 0a2e43bf-b26c-4631-a966-af9dfa12c9e5 |
| Semantic cosine similarity | 0.441439 | 1954cced-e748-45c4-9c26-9855b97fbc5e |

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
  --reference-task-id reference-task-calc-full-r01-018
```

The ordinary launcher reads the collected central review file and refuses pending, revision-requested, or rejected tasks.
