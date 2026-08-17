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

## Initial state preview

### Supply Rounds

![Supply_Rounds.png](artifact/previews/Supply_Rounds.png)

## Operator guide

### Existing operation-intent guide

#### Demonstration 1

- Skill: `21df9241-f8d7-4509-b7f1-37e501a823f7.skill-01`
- Intent: Copy the contiguous Round A range A1:C7 from Supply Rounds and paste it at A1 on the Archive worksheet.
- Efficiency: Copy the full Round A snapshot as one contiguous selection, including its title and headers, so the archive keeps its context.
- Visible success: Archive visibly shows the Round A title, the three input headers, and all five Round A item and quantity records.

#### Demonstration 2

- Skill: `1e8df695-bd1b-45b3-b557-e7d599cf7597.skill-01`
- Intent: In D3, create a subtraction formula that calculates remaining packs as Prepared Packs minus Issued Packs for that row.
- Efficiency: Use relative references in the first result row so a single formula can be efficiently propagated through the first block.
- Visible success: D3 displays 55, and its formula subtracts the row's Issued Packs value from its Prepared Packs value.

#### Demonstration 3

- Skill: `f9584479-3d0d-4c79-affa-9ad7afdd8850.skill-03`
- Intent: Copy the completed Round A formula range D3:D7 to both D11:D15 and D19:D23 so the later rounds calculate their own remaining packs.
- Efficiency: After the Round A formulas are prepared, copy the entire five-cell formula range once and paste it at the top of each matching later-round result area.
- Visible success: Every Remaining Packs cell in Rounds B and C contains a result, with formulas referencing Prepared Packs and Issued Packs on the corresponding local row.

#### Demonstration 4

- Skill: `04d9aeaf-7bed-4024-bedb-e10e6f00eb7f.skill-02`
- Intent: Insert a new blank worksheet using the sheet-tab plus button, then identify it as Archive for the copied snapshot.
- Efficiency: Use the sheet-tab plus control to immediately create the blank destination before renaming it for the archive.
- Visible success: A separate worksheet named Archive is present alongside Supply Rounds.

Recording start: The workbook opens on the single Supply Rounds worksheet with the three populated input blocks, blank Remaining Packs cells, and no Archive worksheet.

Recording end: The workbook has Supply Rounds and Archive sheets. Supply Rounds has calculated Remaining Packs formulas in all three blocks, and Archive contains the copied Round A A1:C7 snapshot.

Allowed variation: The expert may complete the archive copy before or after the calculations, and may use any equivalent Calc method to fill the first formula down, provided the displayed formulas and copied values have the required final relationships.

### 中文详细参考方案

> 以下是一个可以参考的操作 guide。标注者可以根据实际 LibreOffice 界面采用等价操作。

本指南将在 "Supply Rounds" 的三个配送批次中计算 Remaining Packs（Prepared Packs 减 Issued Packs），并新建名为 "Archive" 的工作表，保存 Round A 的 A1:C7 输入快照。公式先在 Round A 建立并填满，再整体复制到后两个结构相同的批次。

#### 启动后的初始状态检查

- 确认当前打开的工作簿只有一个名为 "Supply Rounds" 的工作表。
- 确认 "Supply Rounds" 中有三个区块：Round A 位于 A1:D7、Round B 位于 A9:D15、Round C 位于 A17:D23。
- 确认 D3:D7、D11:D15 和 D19:D23 目前为空；不要覆盖 A:C 中已有的物品和数量。
- 确认尚未存在名为 "Archive" 的工作表。

#### 第 1 步：新建并命名 Archive 工作表

1. 在窗口底部的工作表标签区域，点击工作表标签旁的 `+` 按钮。
2. Calc 会立即创建并切换到一个新的空白工作表。
3. 将新工作表改名为 `Archive`：可双击新工作表标签，输入 `Archive` 后按 Enter。

- 对应 skills：`04d9aeaf-7bed-4024-bedb-e10e6f00eb7f.skill-02`
- 高效操作：先创建空白目标表，可在复制时直接粘贴，避免在工作表之间临时来回切换。
- 完成标志：底部能看到独立的 "Archive" 工作表标签，且当前表格为空白。

#### 第 2 步：复制 Round A 输入快照到 Archive

1. 切换回 "Supply Rounds" 工作表。
2. 选中连续区域 A1:C7：点击 A1，然后拖动到 C7，使整个三列七行区域被选中。
3. 按 Ctrl+C 复制。
4. 切换到 "Archive" 工作表，点击 A1 作为粘贴区域的左上角。
5. 按 Ctrl+V 粘贴。

- 对应 skills：`21df9241-f8d7-4509-b7f1-37e501a823f7.skill-01`
- 高效操作：一次选中 A1:C7 可保留标题、三列标题和全部五条记录，不必逐项重新输入。
- 完成标志："Archive" 的 A1:C7 已显示 "Round A — Tuesday"、第 2 行的三个标题及五行 Round A 的物品和数量。

#### 第 3 步：在 Round A 创建首个剩余包数公式

1. 返回 "Supply Rounds" 工作表。
2. 点击 D3；这是 Round A 的第一条记录 Seed Trays 对应的 Remaining Packs 单元格。
3. 输入公式 `=B3-C3`，然后按 Enter。
4. 如需要确认计算关系，再次选中 D3，查看公式栏是否显示 `=B3-C3`。

- 对应 skills：`1e8df695-bd1b-45b3-b557-e7d599cf7597.skill-01`
- 高效操作：使用相对引用的首行公式，后续向下填充时行号会自动变化，无需逐行重新键入。
- 完成标志：D3 显示 55，表示 84 个 Prepared Packs 减去 29 个 Issued Packs。

#### 第 4 步：填充 Round A 的其余公式

1. 选中 D3:D7。可先点击 D3，再拖动到 D7。
2. 使用菜单 `工作表` > `填充单元格` > `向下填充`，将 D3 的公式填充到 D4:D7。
3. 检查 D3:D7 是否均显示计算结果。

- 对应 skills：无；这是准备或检查步骤。
- 高效操作：用填充命令将一个已验证的公式扩展到相邻行，比手动输入五个公式更快且更不易出错。
- 完成标志：D3:D7 全部有整数结果；从上到下应显示 55、45、74、19、78。

#### 第 5 步：将完整公式范围复制到 Round B 和 Round C

1. 选中已完成的公式范围 D3:D7。
2. 按 Ctrl+C 复制该五单元格公式范围。
3. 点击 D11，即 Round B 的第一条数据行的 Remaining Packs 单元格，然后按 Ctrl+V。
4. 点击 D19，即 Round C 的第一条数据行的 Remaining Packs 单元格，然后再次按 Ctrl+V。
5. 分别查看 D11:D15 和 D19:D23，确认没有空白的 Remaining Packs 单元格。

- 对应 skills：`f9584479-3d0d-4c79-affa-9ad7afdd8850.skill-03`
- 高效操作：复制完整的五单元格公式区域一次，再粘贴到两个同结构区域，Calc 会自动保留相对引用并按新行计算。
- 完成标志：Round B 的 D11:D15 显示 45、37、71、16、81；Round C 的 D19:D23 显示 57、45、76、19、93。

#### 最终结果检查

- 工作簿底部有且仅需确认存在两个相关工作表："Supply Rounds" 和 "Archive"。
- 在 "Supply Rounds" 中检查 D3:D7、D11:D15、D19:D23 均不再为空，且每个单元格显示整数的剩余包数。
- 抽查公式：选中 D3 时公式栏为 `=B3-C3`；选中 D11 时应为 `=B11-C11`；选中 D19 时应为 `=B19-C19`，说明引用已随粘贴位置自动调整。
- 核对结果示例：D3 为 55，D7 为 78，D11 为 45，D15 为 81，D19 为 57，D23 为 93。
- 打开 "Archive"，确认 A1:C7 显示 "Round A — Tuesday"、第 2 行的 Item/Prepared Packs/Issued Packs 标题，以及五条 Round A 物品和数量记录。

## Source-task similarity review

| Measure | Maximum | Most similar source task |
| --- | ---: | --- |
| Lexical sequence similarity | 0.338109 | 4172ea6e-6b77-4edb-a9cc-c0014bd1603b |
| Semantic cosine similarity | 0.420299 | 51719eea-10bc-4246-a428-ac7c433dd4b3 |

Similarity scores are reviewer aids, not automatic acceptance thresholds. Inspect the contributing source tasks and their complete ordered actions below.

### Source task `04d9aeaf-7bed-4024-bedb-e10e6f00eb7f`

Original instruction:

> In a new sheet with 4 headers "Year", "CA changes", "FA changes", and "OA changes", calculate the percentage annual changes compared to last year in 2015 to 2019 for the Current Assets, Fixed Assets, and Other Assets columns. 

Required skills derived from this source task:

- **Insert a new worksheet with the sheet-tab plus button** — `04d9aeaf-7bed-4024-bedb-e10e6f00eb7f.skill-02`

Complete ordered single-action sequence:

| Action | Related required skill | Original single action |
| ---: | --- | --- |
| 0 |  | <code>`CLICK` on cell A3</code> |
| 1 |  | <code>`DRAG_TO` cell A7</code> |
| 2 |  | <code>`HOTKEY` Ctrl-c</code> |
| 3 | <strong>★ Insert a new worksheet with the sheet-tab plus button</strong><br><code>04d9aeaf-7bed-4024-bedb-e10e6f00eb7f.skill-02</code> | <strong><code>`CLICK` the + button to the left of Sheet1 to add a new sheet</code></strong> |
| 4 |  | <code>`TYPING` &#x27;Year&#x27;</code> |
| 5 |  | <code>`PRESS` tab</code> |
| 6 |  | <code>`TYPING` &#x27;CA changes&#x27;</code> |
| 7 |  | <code>`PRESS` tab</code> |
| 8 |  | <code>`TYPING` &#x27;FA changes&#x27;</code> |
| 9 |  | <code>`PRESS` tab</code> |
| 10 |  | <code>`TYPING` &#x27;OA changes&#x27;</code> |
| 11 |  | <code>`PRESS` enter</code> |
| 12 |  | <code>`HOTKEY` ctrl-V</code> |
| 13 |  | <code>`CLICK` cell B2</code> |
| 14 |  | <code>`TYPING` &#x27;=($Sheet1.B3-$Sheet1.B2)/$Sheet1.B2&#x27;</code> |
| 15 |  | <code>`PRESS` enter</code> |
| 16 |  | <code>`CLICK` cell B2</code> |
| 17 |  | <code>`DOUBLE_CLICK` bottom right corner</code> |
| 18 |  | <code>`CLICK` cell B2</code> |
| 19 |  | <code>`MOVE_TO` bottom right corner of the cell B2</code> |
| 20 |  | <code>`DRAG_TO` cell D2</code> |
| 21 |  | <code>`CLICK` cell C2</code> |
| 22 |  | <code>`DOUBLE_CLICK` bottom right corner</code> |
| 23 |  | <code>`MOVE_TO` cell D2</code> |
| 24 |  | <code>`DOUBLE_CLICK` bottom right corner</code> |
| 25 |  | <code>`CLICK` cell B2</code> |
| 26 |  | <code>`DRAG_TO` D6</code> |
| 27 |  | <code>`CLICK` percent symbol</code> |

### Source task `1e8df695-bd1b-45b3-b557-e7d599cf7597`

Original instruction:

> Add a new column named "Profit" right next to the 'CGOS' column and calculate the profit for each week by subtracting "COGS" from "Sales" in that column.

Required skills derived from this source task:

- **Create a row formula using subtraction** — `1e8df695-bd1b-45b3-b557-e7d599cf7597.skill-01`

Complete ordered single-action sequence:

| Action | Related required skill | Original single action |
| ---: | --- | --- |
| 0 |  | <code>`CLICK` on cell D1</code> |
| 1 |  | <code>`TYPING` &#x27;Profit&#x27;</code> |
| 2 |  | <code>`PRESS` enter</code> |
| 3 | <strong>★ Create a row formula using subtraction</strong><br><code>1e8df695-bd1b-45b3-b557-e7d599cf7597.skill-01</code> | <strong><code>`TYPING` &#x27;=B2-C2&#x27;</code></strong> |
| 4 | <strong>★ Create a row formula using subtraction</strong><br><code>1e8df695-bd1b-45b3-b557-e7d599cf7597.skill-01</code> | <strong><code>`PRESS` enter</code></strong> |
| 5 |  | <code>`CLICK` cell D2</code> |
| 6 |  | <code>`DOUBLE_CLICK` bottom right corner of the cell D2</code> |

### Source task `21df9241-f8d7-4509-b7f1-37e501a823f7`

Original instruction:

> Change the representation of column "Parameter" to show in Millions (M) in Column B and Billions (B) in Column C. The numbers should be rounded to one decimal place, and half should be rounded up. Then remember to place a white space between the digits and the unit.

Required skills derived from this source task:

- **Copy a contiguous cell range to another location** — `21df9241-f8d7-4509-b7f1-37e501a823f7.skill-01`

Complete ordered single-action sequence:

| Action | Related required skill | Original single action |
| ---: | --- | --- |
| 0 | <strong>★ Copy a contiguous cell range to another location</strong><br><code>21df9241-f8d7-4509-b7f1-37e501a823f7.skill-01</code> | <strong><code>`CLICK A2</code></strong> |
| 1 | <strong>★ Copy a contiguous cell range to another location</strong><br><code>21df9241-f8d7-4509-b7f1-37e501a823f7.skill-01</code> | <strong><code>`DRAG_TO A8</code></strong> |
| 2 | <strong>★ Copy a contiguous cell range to another location</strong><br><code>21df9241-f8d7-4509-b7f1-37e501a823f7.skill-01</code> | <strong><code>`HOTKEY` CTRL-C</code></strong> |
| 3 | <strong>★ Copy a contiguous cell range to another location</strong><br><code>21df9241-f8d7-4509-b7f1-37e501a823f7.skill-01</code> | <strong><code>`CLICK` B2</code></strong> |
| 4 | <strong>★ Copy a contiguous cell range to another location</strong><br><code>21df9241-f8d7-4509-b7f1-37e501a823f7.skill-01</code> | <strong><code>`HOTKEY` CTRL-V</code></strong> |
| 5 |  | <code>`RIGHT_CLICK`</code> |
| 6 |  | <code>`CLICK` &#x27;Format Cells...&#x27;</code> |
| 7 |  | <code>`DOUBLE_CLICK` format code box</code> |
| 8 |  | <code>`TYPING` &#x27;0.0,, \M&#x27;</code> |
| 9 |  | <code>`PRESS` enter</code> |
| 10 |  | <code>`CLICK` C2</code> |
| 11 |  | <code>`HOTKEY` CTRL-V</code> |
| 12 |  | <code>`RIGHT_CLICK`</code> |
| 13 |  | <code>`CLICK` &#x27;Format Cells...&#x27;</code> |
| 14 |  | <code>`DOUBLE_CLICK` format code box</code> |
| 15 |  | <code>`TYPING` &#x27;0.0,,, \B&#x27;</code> |
| 16 |  | <code>`PRESS` enter</code> |

### Source task `f9584479-3d0d-4c79-affa-9ad7afdd8850`

Original instruction:

> Fill the missing rows and columns which show the total value

Required skills derived from this source task:

- **Copy a selected formula range to multiple locations** — `f9584479-3d0d-4c79-affa-9ad7afdd8850.skill-03`

Complete ordered single-action sequence:

| Action | Related required skill | Original single action |
| ---: | --- | --- |
| 0 |  | <code>`CLICK` B6</code> |
| 1 |  | <code>`TYPING` &#x27;=SUM(B2:B5)&#x27;</code> |
| 2 |  | <code>`PRESS` Enter</code> |
| 3 |  | <code>`CLICK` B6</code> |
| 4 |  | <code>`MOVE_TO` bottom right corner of the cell</code> |
| 5 |  | <code>`DRAG_TO` E6</code> |
| 6 | <strong>★ Copy a selected formula range to multiple locations</strong><br><code>f9584479-3d0d-4c79-affa-9ad7afdd8850.skill-03</code> | <strong><code>`HOTKEY` CTRL-C</code></strong> |
| 7 | <strong>★ Copy a selected formula range to multiple locations</strong><br><code>f9584479-3d0d-4c79-affa-9ad7afdd8850.skill-03</code> | <strong><code>`CLICK` B13</code></strong> |
| 8 | <strong>★ Copy a selected formula range to multiple locations</strong><br><code>f9584479-3d0d-4c79-affa-9ad7afdd8850.skill-03</code> | <strong><code>`HOTKEY` CTRL-V</code></strong> |
| 9 | <strong>★ Copy a selected formula range to multiple locations</strong><br><code>f9584479-3d0d-4c79-affa-9ad7afdd8850.skill-03</code> | <strong><code>`CLICK` B20</code></strong> |
| 10 | <strong>★ Copy a selected formula range to multiple locations</strong><br><code>f9584479-3d0d-4c79-affa-9ad7afdd8850.skill-03</code> | <strong><code>`HOTKEY` CTRL-V</code></strong> |
| 11 |  | <code>`CLICK` F3</code> |
| 12 |  | <code>`TYPING` &#x27;=SUM(B3:E3)&#x27;</code> |
| 13 |  | <code>`PRESS` Enter</code> |
| 14 |  | <code>`CLICK` F3</code> |
| 15 |  | <code>`MOVE_TO` bottom right corner of the cell</code> |
| 16 |  | <code>`DRAG_TO` F6</code> |
| 17 | <strong>★ Copy a selected formula range to multiple locations</strong><br><code>f9584479-3d0d-4c79-affa-9ad7afdd8850.skill-03</code> | <strong><code>`HOTKEY` CTRL-C</code></strong> |
| 18 | <strong>★ Copy a selected formula range to multiple locations</strong><br><code>f9584479-3d0d-4c79-affa-9ad7afdd8850.skill-03</code> | <strong><code>`CLICK` F10</code></strong> |
| 19 | <strong>★ Copy a selected formula range to multiple locations</strong><br><code>f9584479-3d0d-4c79-affa-9ad7afdd8850.skill-03</code> | <strong><code>`HOTKEY` CTRL-V</code></strong> |
| 20 | <strong>★ Copy a selected formula range to multiple locations</strong><br><code>f9584479-3d0d-4c79-affa-9ad7afdd8850.skill-03</code> | <strong><code>`CLICK` F17</code></strong> |
| 21 | <strong>★ Copy a selected formula range to multiple locations</strong><br><code>f9584479-3d0d-4c79-affa-9ad7afdd8850.skill-03</code> | <strong><code>`HOTKEY` CTRL-V</code></strong> |

## Review this package

Before choosing a decision, complete all three checks:

- [ ] **Task naturalness and skill necessity:** Is the reference task a natural Calc task, and is every listed required skill genuinely necessary and observable when solving it?
- [ ] **Initial artifact correctness:** Launch the environment and confirm that the workbook opens correctly, contains the data needed by the instruction, and has not already completed the requested results.
- [ ] **Source-task similarity:** Compare the reference task with the source instructions and complete single-action sequences above. Confirm that it is not merely an entity, field, or value substitution and does not reproduce a source task's complete ordered solution.

Use `approved` when all checks pass. Use `revision_requested` when the package is fixable and provide concrete revision instructions. Use `rejected` when the combination is fundamentally unnatural, infeasible, or too similar to a source task.

Fill [review.json](review.json), then collect completed forms from the repository root:

```bash
python scripts/python/manage_reference_review_packets.py collect \
  --skill-pool evaluation_examples/expert_skill_learning/calc_full_v1/generated/skill_pool.json \
  --packages evaluation_examples/expert_skill_learning/calc_full_v1/generated/round_01/reference_packages.json \
  --source-tasks evaluation_examples/expert_skill_learning/calc_full_v1/source_tasks.json \
  --reviews evaluation_examples/expert_skill_learning/calc_full_v1/generated/round_01/reference_package_reviews.json \
  --artifact-manifest evaluation_examples/expert_skill_learning/calc_full_v1/generated/round_01/artifacts/artifact_manifest.json \
  --task-config-manifest evaluation_examples/expert_skill_learning/calc_full_v1/generated/round_01/task_config_manifest.json \
  --task-detail-root evaluation_examples/expert_skill_learning/calc_full_v1/generated/round_01/task_details \
  --reviewer-guides evaluation_examples/expert_skill_learning/calc_full_v1/generated/round_01/reviewer_guides.json \
  --coverage evaluation_examples/expert_skill_learning/calc_full_v1/generated/round_01/coverage_state.json \
  --packet-root evaluation_examples/expert_skill_learning/calc_full_v1/review_packets/round_01
```

Detailed field guidance is in [`reviewer.md`](../../../../reviewer.md).
