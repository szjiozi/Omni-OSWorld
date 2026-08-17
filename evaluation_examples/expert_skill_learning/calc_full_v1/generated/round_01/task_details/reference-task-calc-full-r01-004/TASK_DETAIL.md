# Garden Supply Round Reconciliation

- Reference task: `reference-task-calc-full-r01-004`
- Application: `libreoffice_calc`
- Review decision: `pending`

## Task instruction

Finish the garden supply reconciliation: calculate Remaining Packs for every item in all three delivery rounds, then add an Archive worksheet containing a copied snapshot of Round A with its title, headers, items, and quantities.

## Required skills

### 1. Copy a contiguous cell range to another location

Skill ID: `21df9241-f8d7-4509-b7f1-37e501a823f7.skill-01`

Procedure:

1. Select the source range by clicking its first cell and dragging through its last cell; for example, select A2:A8.
2. Press Ctrl+C to copy the selected cells.
3. Click the top-left destination cell, such as B2, and press Ctrl+V to paste the range.

Efficiency tip: Copying an existing populated range preserves its values and formulas, avoiding re-entry; paste starting at the top-left destination cell.

Source task: `21df9241-f8d7-4509-b7f1-37e501a823f7`

Source instruction: Change the representation of column "Parameter" to show in Millions (M) in Column B and Billions (B) in Column C. The numbers should be rounded to one decimal place, and half should be rounded up. Then remember to place a white space between the digits and the unit.

Directly referenced source actions:

- Action 0: <code>`CLICK A2</code>
- Action 1: <code>`DRAG_TO A8</code>
- Action 2: <code>`HOTKEY` CTRL-C</code>
- Action 3: <code>`CLICK` B2</code>
- Action 4: <code>`HOTKEY` CTRL-V</code>

### 2. Create a row formula using subtraction

Skill ID: `1e8df695-bd1b-45b3-b557-e7d599cf7597.skill-01`

Procedure:

1. Select the first result cell in the new column, then type a subtraction formula that references the two cells in the same row.
2. For example, enter `=B2-C2` and press Enter to calculate the difference between the values in columns B and C for row 2.
3. Use relative references when the formula will be copied to other rows, so the row numbers adjust automatically.

Efficiency tip: Enter the formula once in the first data row before propagating it; this avoids manually writing separate formulas for every row.

Source task: `1e8df695-bd1b-45b3-b557-e7d599cf7597`

Source instruction: Add a new column named "Profit" right next to the 'CGOS' column and calculate the profit for each week by subtracting "COGS" from "Sales" in that column.

Directly referenced source actions:

- Action 3: <code>`TYPING` &#x27;=B2-C2&#x27;</code>
- Action 4: <code>`PRESS` enter</code>

### 3. Copy a selected formula range to multiple locations

Skill ID: `f9584479-3d0d-4c79-affa-9ad7afdd8850.skill-03`

Procedure:

1. With the prepared formula range still selected, press Ctrl+C to copy it.
2. Click the top-left destination cell and press Ctrl+V. For example, copy the selected range beginning at `B6` and paste starting at `B13`, then paste again starting at `B20`.
3. The pasted formulas retain their relative-reference behavior and adjust based on each new location.
4. The same pattern can be used for a vertically oriented range, such as copying a range beginning at `F3` and pasting it beginning at `F10` and `F17`.

Efficiency tip: Copy the complete prepared range once and paste it at each destination, rather than recreating formulas or formatting separately for every repeated block.

Source task: `f9584479-3d0d-4c79-affa-9ad7afdd8850`

Source instruction: Fill the missing rows and columns which show the total value

Directly referenced source actions:

- Action 6: <code>`HOTKEY` CTRL-C</code>
- Action 7: <code>`CLICK` B13</code>
- Action 8: <code>`HOTKEY` CTRL-V</code>
- Action 9: <code>`CLICK` B20</code>
- Action 10: <code>`HOTKEY` CTRL-V</code>
- Action 17: <code>`HOTKEY` CTRL-C</code>
- Action 18: <code>`CLICK` F10</code>
- Action 19: <code>`HOTKEY` CTRL-V</code>
- Action 20: <code>`CLICK` F17</code>
- Action 21: <code>`HOTKEY` CTRL-V</code>

### 4. Insert a new worksheet with the sheet-tab plus button

Skill ID: `04d9aeaf-7bed-4024-bedb-e10e6f00eb7f.skill-02`

Procedure:

1. Click the + button beside the worksheet tabs.
2. Calc creates and activates a new blank worksheet, ready for entering data or formulas.

Efficiency tip: Use the sheet-tab plus button when a blank worksheet is needed immediately; it avoids opening the Insert Sheet dialog.

Source task: `04d9aeaf-7bed-4024-bedb-e10e6f00eb7f`

Source instruction: In a new sheet with 4 headers "Year", "CA changes", "FA changes", and "OA changes", calculate the percentage annual changes compared to last year in 2015 to 2019 for the Current Assets, Fixed Assets, and Other Assets columns. 

Directly referenced source actions:

- Action 3: <code>`CLICK` the + button to the left of Sheet1 to add a new sheet</code>

## Initial artifact

- Domain: community garden supply rounds
- Workbook: [initial_artifact.xlsx](artifact/initial_artifact.xlsx)
- Blueprint: [artifact_blueprint.json](artifact/artifact_blueprint.json)
- QA report: [artifact_qa.json](artifact/artifact_qa.json)

Initial state:

- The workbook opens with exactly one worksheet named "Supply Rounds".
- The "Supply Rounds" sheet contains three identically structured delivery-round blocks in columns A:D.
- Round A occupies A1:D7. A1 contains "Round A — Tuesday"; row 2 headers are Item, Prepared Packs, Issued Packs, Remaining Packs; rows 3:7 contain five populated supply records in A:C and blank cells in D.
- Round B occupies A9:D15. A9 contains "Round B — Thursday"; row 10 has the same headers; rows 11:15 contain five populated supply records in A:C and blank cells in D.
- Round C occupies A17:D23. A17 contains "Round C — Saturday"; row 18 has the same headers; rows 19:23 contain five populated supply records in A:C and blank cells in D.
- Use these Round A records: Seed Trays / 84 / 29; Compost Bags / 63 / 18; Bamboo Stakes / 120 / 46; Watering Cans / 28 / 9; Plant Labels / 150 / 72.
- Use these Round B records: Seed Trays / 76 / 31; Compost Bags / 58 / 21; Bamboo Stakes / 110 / 39; Watering Cans / 24 / 8; Plant Labels / 135 / 54.
- Use these Round C records: Seed Trays / 91 / 34; Compost Bags / 70 / 25; Bamboo Stakes / 128 / 52; Watering Cans / 31 / 12; Plant Labels / 160 / 67.

Artifact construction requirements:

- All names, items, and quantities are synthetic and privacy-safe.
- Use ordinary spreadsheet styling: make each round title bold with a light fill, make column headers bold, and format pack quantities as integers.
- Do not create any additional sheets, formulas in Remaining Packs, Pivot Tables, or conditional formatting rules.

| Sheet | Rows | Purpose | Columns |
| --- | ---: | --- | --- |
| Supply Rounds | 23 | Three delivery-round input blocks awaiting remaining-pack calculations and an archived Round A snapshot. | Item (text), Prepared Packs (integer), Issued Packs (integer), Remaining Packs (integer) |

Must remain incomplete before recording:

- No second worksheet exists initially.
- All Remaining Packs cells D3:D7, D11:D15, and D19:D23 are blank initially.
- No Archive sheet or copied Round A snapshot exists initially.

Artifact previews:

### Supply Rounds

![Supply_Rounds.png](artifact/previews/Supply_Rounds.png)

## Operator guide

### Demonstration 1

- Skill: `21df9241-f8d7-4509-b7f1-37e501a823f7.skill-01`
- Intent: Copy the contiguous Round A range A1:C7 from Supply Rounds and paste it at A1 on the Archive worksheet.
- Efficiency: Copy the full Round A snapshot as one contiguous selection, including its title and headers, so the archive keeps its context.
- Visible success: Archive visibly shows the Round A title, the three input headers, and all five Round A item and quantity records.

### Demonstration 2

- Skill: `1e8df695-bd1b-45b3-b557-e7d599cf7597.skill-01`
- Intent: In D3, create a subtraction formula that calculates remaining packs as Prepared Packs minus Issued Packs for that row.
- Efficiency: Use relative references in the first result row so a single formula can be efficiently propagated through the first block.
- Visible success: D3 displays 55, and its formula subtracts the row's Issued Packs value from its Prepared Packs value.

### Demonstration 3

- Skill: `f9584479-3d0d-4c79-affa-9ad7afdd8850.skill-03`
- Intent: Copy the completed Round A formula range D3:D7 to both D11:D15 and D19:D23 so the later rounds calculate their own remaining packs.
- Efficiency: After the Round A formulas are prepared, copy the entire five-cell formula range once and paste it at the top of each matching later-round result area.
- Visible success: Every Remaining Packs cell in Rounds B and C contains a result, with formulas referencing Prepared Packs and Issued Packs on the corresponding local row.

### Demonstration 4

- Skill: `04d9aeaf-7bed-4024-bedb-e10e6f00eb7f.skill-02`
- Intent: Insert a new blank worksheet using the sheet-tab plus button, then identify it as Archive for the copied snapshot.
- Efficiency: Use the sheet-tab plus control to immediately create the blank destination before renaming it for the archive.
- Visible success: A separate worksheet named Archive is present alongside Supply Rounds.

Recording start: The workbook opens on the single Supply Rounds worksheet with the three populated input blocks, blank Remaining Packs cells, and no Archive worksheet.

Recording end: The workbook has Supply Rounds and Archive sheets. Supply Rounds has calculated Remaining Packs formulas in all three blocks, and Archive contains the copied Round A A1:C7 snapshot.

Allowed variation: The expert may complete the archive copy before or after the calculations, and may use any equivalent Calc method to fill the first formula down, provided the displayed formulas and copied values have the required final relationships.

## Expected incidental operations

- **substantive_prerequisite:** Propagate the initial subtraction formula from the first Round A result cell through the other Round A result rows to create a complete formula range. Reason: A populated Round A formula range is needed before that range can be copied to both later round blocks.
- **task_specific:** Rename the newly inserted blank worksheet to "Archive". Reason: The requested copied snapshot needs a clearly identified destination worksheet.

## Source-similarity audit

| Measure | Maximum | Most similar source task |
| --- | ---: | --- |
| Lexical sequence similarity | 0.338109 | 4172ea6e-6b77-4edb-a9cc-c0014bd1603b |
| Semantic cosine similarity | 0.420299 | 51719eea-10bc-4246-a428-ac7c433dd4b3 |

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
  --reference-task-id reference-task-calc-full-r01-004
```

The ordinary launcher reads the collected central review file and refuses pending, revision-requested, or rejected tasks.
