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

## Initial state preview

### CheckIn Log

![CheckIn_Log.png](artifact/previews/CheckIn_Log.png)

### Coverage Setup

![Coverage_Setup.png](artifact/previews/Coverage_Setup.png)

### Handoff Summary

![Handoff_Summary.png](artifact/previews/Handoff_Summary.png)

## Operator guide

### Existing operation-intent guide

#### Demonstration 1

- Skill: `eb03d19a-b88d-4de4-8a64-ca0ac66f426b.skill-01`
- Intent: Transpose the complete shift-by-kiosk coverage matrix from Coverage Setup into the upper area of Handoff Summary.
- Efficiency: Copy the entire labeled source block once and use Paste Special with the transpose option at the chosen destination rather than retyping or rearranging values.
- Visible success: The pasted layout has kiosks listed vertically and shifts across the top, with all coverage target values preserved in their rotated positions.

#### Demonstration 2

- Skill: `30e3e107-1cfb-46ee-a755-2cd080d7ba6a.skill-08`
- Intent: Create a kiosk-level Pivot Table from CheckIn Log and set the Ticket Code data field to count non-empty check-in occurrences.
- Efficiency: After adding Ticket Code to the Pivot Table data fields, open its data-field settings immediately and select Count rather than accepting a numeric aggregation default.
- Visible success: The Pivot Table lists each kiosk and a count-based Ticket Code result; its data-field label indicates Count rather than Sum.

Recording start: The workbook is open on the blank Handoff Summary sheet; Coverage Setup and CheckIn Log contain the prepared source data only.

Recording end: Handoff Summary visibly contains a transposed coverage-target layout and a separate Pivot Table counting Ticket Code check-ins for each kiosk.

Allowed variation: The expert may choose any non-overlapping placement on Handoff Summary, provided the transposed matrix is clearly identifiable and the Pivot Table visibly reports Ticket Code occurrence counts by Kiosk. Equivalent Calc Pivot Table creation workflows are acceptable.

### 中文详细参考方案

> 以下是一个可以参考的操作 guide。标注者可以根据实际 LibreOffice 界面采用等价操作。

本任务在 `Handoff Summary` 上完成两个彼此分开的交接视图：先把 `Coverage Setup` 的完整 shift-by-kiosk 矩阵转置到上方，再根据 `CheckIn Log` 创建按 kiosk 汇总的 Pivot Table，并将 `Ticket Code` 汇总方式明确设为计数。

#### 启动后的初始状态检查

- 确认当前打开的是目标工作簿，且起始活动工作表为无内容的 `Handoff Summary`。
- 检查 `Coverage Setup` 的 A1:D4 是完整的带标题矩阵，包含 `Shift`、三个 kiosk 标题以及 `Morning`、`Midday`、`Afternoon` 三个班次。
- 检查 `CheckIn Log` 的 A1:D31 是连续数据表，标题包含 `Check-in Time`、`Kiosk`、`Ticket Code`、`Repair Type`；特别确认 `Ticket Code` 在数据行中均非空。
- 确认 `Handoff Summary` 尚未存在转置表或 Pivot Table，并预留上方区域给覆盖表、下方或右侧区域给 Pivot Table。

#### 第 1 步：将覆盖目标矩阵转置到交接表

1. 切换到 `Coverage Setup` 工作表。
2. 选择完整矩阵 A1:D4，包括标题行和标题列。
3. 按 `Ctrl+C` 复制所选区域。
4. 切换回 `Handoff Summary`，在上方的空白区域选定一个左上角目标单元格，例如 A1。
5. 右键单击该目标单元格，打开 `Paste Special`，并选择 `Transpose` 以粘贴转置后的内容。

- 对应 skills：`eb03d19a-b88d-4de4-8a64-ca0ac66f426b.skill-01`
- 高效操作：一次选中带标题的整个 A1:D4 区域，能让转置后的表同时保留 kiosk 和 shift 标签，无需另行补写标题。
- 完成标志：`Handoff Summary` 出现一个 4 列 × 4 行的覆盖表：kiosk 名称竖向列在第一列，`Morning`、`Midday`、`Afternoon` 横向位于第一行，所有数值仍与原覆盖目标对应。

#### 第 2 步：创建按 kiosk 分组的 Pivot Table

1. 切换到 `CheckIn Log` 工作表，并单击 A1:D31 连续表格内的任意单元格。
2. 打开 `Data` > `Pivot Table` > `Insert or Edit...`。
3. 确认 Pivot Table 的源数据范围覆盖带标题的 `CheckIn Log` 表，即 A1:D31；如自动识别的范围正确则继续。
4. 在字段布局区域中，将 `Kiosk` 放入 `Row Fields`，使每个 kiosk 成为一行。
5. 将 `Ticket Code` 放入 `Data Fields`，准备对每条非空 ticket 记录进行汇总。
6. 选择将结果放在已有工作表的选项，并把输出位置指定为 `Handoff Summary` 中覆盖表下方或右侧的空白起始单元格，例如 A8；确保不会覆盖转置表。
7. 确认创建 Pivot Table。

- 对应 skills：无；这是准备或检查步骤。
- 高效操作：在插入 Pivot Table 前先选中连续数据表中的任意一个单元格，Calc 通常可自动识别整个相邻数据区域，减少手动输入源范围的机会。
- 完成标志：`Handoff Summary` 的空白区域出现 Pivot Table，行标签按 kiosk 分组，并有一个来自 `Ticket Code` 的数据结果列。

#### 第 3 步：将 Ticket Code 数据字段设为计数

1. 如仍在 Pivot Table 的布局/编辑窗口，双击 `Data Fields` 区域中的 `Ticket Code` 字段；若 Pivot Table 已生成，可通过 `Data` > `Pivot Table` > `Insert or Edit...` 重新打开其字段布局后再双击该字段。
2. 在打开的数据字段选项中选择 `Count`，使 Calc 统计非空 `Ticket Code` 的出现次数，而不是使用数值求和。
3. 确认设置并完成 Pivot Table 的更新。

- 对应 skills：`30e3e107-1cfb-46ee-a755-2cd080d7ba6a.skill-08`
- 高效操作：刚把 `Ticket Code` 加入 `Data Fields` 时立即调整汇总方式，可以避免之后误把数值汇总结果当成所需的记录数量。
- 完成标志：Pivot Table 的值字段标签显示 `Count`，并且 `Kiosk North`、`Kiosk Central`、`Kiosk South` 各自显示 ticket 记录数量，而非金额或求和结果。

#### 第 4 步：检查布局、计数结果并保存

1. 回到 `Handoff Summary`，检查转置覆盖表和 Pivot Table 之间有足够空白，不存在覆盖或混在同一表格内的情况。
2. 核对 Pivot Table 中每个 `Kiosk` 都只作为一个分组行出现，并且数值字段为 `Count` 类型的 `Ticket Code` 结果。
3. 查看 Pivot Table 的总计；由于源表 30 条数据记录的 `Ticket Code` 都非空，三个 kiosk 的计数总和应为 30。
4. 按 `Ctrl+S` 保存。

- 对应 skills：无；这是准备或检查步骤。
- 高效操作：使用 Pivot Table 的总计快速核对源数据行数；这比逐行手动计数更快，也能及早发现源范围漏选。
- 完成标志：`Handoff Summary` 清楚地同时展示转置后的 coverage layout 和独立的 kiosk check-in Count Pivot Table，且 Pivot Table 总计为 `30`。

#### 最终结果检查

- 在 `Handoff Summary` 中确认上方有完整的转置覆盖表：第一行是 `Shift`、`Morning`、`Midday`、`Afternoon`，第一列依次列出 `Kiosk North`、`Kiosk Central`、`Kiosk South`，且各覆盖目标数值与 `Coverage Setup` 对应但方向已旋转。
- 确认同一张 `Handoff Summary` 中另有一个不与覆盖表重叠的 Pivot Table；它按 `Kiosk` 显示 `Kiosk North`、`Kiosk Central`、`Kiosk South`，并显示每个 kiosk 的 `Ticket Code` 非空记录数。
- 确认 Pivot Table 的数值字段标题明确包含 `Count`，而不是 `Sum`；三个 kiosk 的计数合计应为 `30`，因为 `CheckIn Log` 有 30 条数据记录且每条都有 `Ticket Code`。
- 保存工作簿，必要时使用 `File` > `Save` 或按 `Ctrl+S`，以保留 `Handoff Summary` 上的两个结果。

## Source-task similarity review

| Measure | Maximum | Most similar source task |
| --- | ---: | --- |
| Lexical sequence similarity | 0.359673 | 1de60575-bb6e-4c3d-9e6a-2fa699f9f197 |
| Semantic cosine similarity | 0.327701 | 51719eea-10bc-4246-a428-ac7c433dd4b3 |

Similarity scores are reviewer aids, not automatic acceptance thresholds. Inspect the contributing source tasks and their complete ordered actions below.

### Source task `30e3e107-1cfb-46ee-a755-2cd080d7ba6a`

Original instruction:

> Please create a new sheet. Keep its sheet name as "Sheet2". Merge cells A1:C1 in the new sheet and write "Demographic Profile" with blue (#0000ff) fill and bold white text. Then I want to create three pivot tables to show the percentage of Sex, Civil Status, and Highest Educational Attainment. They should be stacked one by one in Sheet2, each separated with a blank line.

Required skills derived from this source task:

- **Count occurrences in a Pivot Table data field** — `30e3e107-1cfb-46ee-a755-2cd080d7ba6a.skill-08`

Complete ordered single-action sequence:

| Action | Related required skill | Original single action |
| ---: | --- | --- |
| 0 |  | <code>`CLICK` on + to left of sheet1</code> |
| 1 |  | <code>`KEY_DOWN` shift</code> |
| 2 |  | <code>`CLICK` C1</code> |
| 3 |  | <code>`RIGHT_CLICK` selection</code> |
| 4 |  | <code>`CLICK` merge cells</code> |
| 5 |  | <code>`TYPING` Demographic Profile</code> |
| 6 |  | <code>`PRESS` enter</code> |
| 7 |  | <code>`CLICK` cell A1</code> |
| 8 |  | <code>`CLICK` arrow next to paint button dropdown</code> |
| 9 |  | <code>`CLICK` Custom color</code> |
| 10 |  | <code>`DOUBLE_CLICK` on text inside Hex # box</code> |
| 11 |  | <code>`TYPING` 0000ff</code> |
| 12 |  | <code>`PRESS` enter</code> |
| 13 |  | <code>`CLICK` font color arrow icon, which is to left of bucket</code> |
| 14 |  | <code>`CLICK` top right color in the color palette (white)</code> |
| 15 |  | <code>`CLICK` bold icon</code> |
| 16 |  | <code>`CLICK` Sheet1</code> |
| 17 |  | <code>`CLICK` column B grey cell</code> |
| 18 |  | <code>`CLICK` pivot table icon</code> |
| 19 |  | <code>`PRESS` enter</code> |
| 20 |  | <code>`MOVE_TO` &#x27;Sex&#x27; in available fields</code> |
| 21 |  | <code>`DRAG_TO` box in row fields</code> |
| 22 |  | <code>`MOVE_TO` &#x27;Sex&#x27; in available fields</code> |
| 23 |  | <code>`DRAG_TO` box in data fields</code> |
| 24 | <strong>★ Count occurrences in a Pivot Table data field</strong><br><code>30e3e107-1cfb-46ee-a755-2cd080d7ba6a.skill-08</code> | <strong><code>`DOUBLE_CLICK on sex box in data fields</code></strong> |
| 25 | <strong>★ Count occurrences in a Pivot Table data field</strong><br><code>30e3e107-1cfb-46ee-a755-2cd080d7ba6a.skill-08</code> | <strong><code>`CLICK` Count</code></strong> |
| 26 |  | <code>`CLICK` &#x27;displayed value&#x27; dropdown</code> |
| 27 |  | <code>`CLICK` Normal dropdown next to &#x27;Type&#x27;</code> |
| 28 |  | <code>`CLICK` &#x27;% of total&#x27;</code> |
| 29 |  | <code>`CLICK` ok</code> |
| 30 |  | <code>`CLICK` source and destination dropdown</code> |
| 31 |  | <code>`CLICK` &#x27;Selection&#x27; under destination</code> |
| 32 |  | <code>`CLICK` text box</code> |
| 33 |  | <code>`TYPING` &#x27;$Sheet2.$A$2&#x27;</code> |
| 34 |  | <code>`CLICK` ok</code> |
| 35 |  | <code>`CLICK` Sheet2</code> |
| 36 |  | <code>`CLICK` Sheet1</code> |
| 37 |  | <code>`CLICK` column C grey cell</code> |
| 38 |  | <code>`CLICK` pivot table icon</code> |
| 39 |  | <code>`PRESS` enter</code> |
| 40 |  | <code>`MOVE_TO` &#x27;Civil Status&#x27; in available fields</code> |
| 41 |  | <code>`DRAG_TO` box in row fields</code> |
| 42 |  | <code>`MOVE_TO` &#x27;Civil Status&#x27; in available fields</code> |
| 43 |  | <code>`DRAG_TO` box in data fields</code> |
| 44 | <strong>★ Count occurrences in a Pivot Table data field</strong><br><code>30e3e107-1cfb-46ee-a755-2cd080d7ba6a.skill-08</code> | <strong><code>`DOUBLE_CLICK on civil status box in data fields</code></strong> |
| 45 | <strong>★ Count occurrences in a Pivot Table data field</strong><br><code>30e3e107-1cfb-46ee-a755-2cd080d7ba6a.skill-08</code> | <strong><code>`CLICK` Count</code></strong> |
| 46 |  | <code>`CLICK` &#x27;displayed value&#x27; dropdown</code> |
| 47 |  | <code>`CLICK` Normal dropdown next to &#x27;Type&#x27;</code> |
| 48 |  | <code>`CLICK` &#x27;% of total&#x27;</code> |
| 49 |  | <code>`PRESS` enter</code> |
| 50 |  | <code>`CLICK` source and destination dropdown</code> |
| 51 |  | <code>`CLICK` &#x27;Selection&#x27; under destination</code> |
| 52 |  | <code>`CLICK` text box</code> |
| 53 |  | <code>`TYPING` &#x27;$Sheet2.$A$7&#x27;</code> |
| 54 |  | <code>`CLICK` ok</code> |
| 55 |  | <code>`CLICK` Sheet2</code> |
| 56 |  | <code>`CLICK` Sheet1</code> |
| 57 |  | <code>`CLICK` column D grey cell</code> |
| 58 |  | <code>`CLICK` pivot table icon</code> |
| 59 |  | <code>`PRESS` enter</code> |
| 60 |  | <code>`MOVE_TO` &#x27;Highest Educational Attainment&#x27; in available fields</code> |
| 61 |  | <code>`DRAG_TO` box in row fields</code> |
| 62 |  | <code>`MOVE_TO` &#x27;Highest Educational Attainment&#x27; in available fields</code> |
| 63 |  | <code>`DRAG_TO` box in data fields</code> |
| 64 | <strong>★ Count occurrences in a Pivot Table data field</strong><br><code>30e3e107-1cfb-46ee-a755-2cd080d7ba6a.skill-08</code> | <strong><code>`DOUBLE_CLICK on Highest Educational Attainment box in data fields</code></strong> |
| 65 | <strong>★ Count occurrences in a Pivot Table data field</strong><br><code>30e3e107-1cfb-46ee-a755-2cd080d7ba6a.skill-08</code> | <strong><code>`CLICK` Count</code></strong> |
| 66 |  | <code>`CLICK` &#x27;displayed value&#x27; dropdown</code> |
| 67 |  | <code>`CLICK` Normal dropdown next to &#x27;Type&#x27;</code> |
| 68 |  | <code>`CLICK` &#x27;% of total&#x27;</code> |
| 69 |  | <code>`PRESS` enter</code> |
| 70 |  | <code>`CLICK` source and destination dropdown</code> |
| 71 |  | <code>`CLICK` &#x27;Selection&#x27; under destination</code> |
| 72 |  | <code>`CLICK` text box</code> |
| 73 |  | <code>`TYPING` &#x27;$Sheet2.$A$13&#x27;</code> |
| 74 |  | <code>`CLICK` ok</code> |

### Source task `eb03d19a-b88d-4de4-8a64-ca0ac66f426b`

Original instruction:

> Apply matrix transposition to the table in B2:F5 and paste the transposed table at B8 (i.e., the top-left cell of the transposed table should be at B8)

Required skills derived from this source task:

- **Paste a copied cell range with rows and columns transposed** — `eb03d19a-b88d-4de4-8a64-ca0ac66f426b.skill-01`

Complete ordered single-action sequence:

| Action | Related required skill | Original single action |
| ---: | --- | --- |
| 0 | <strong>★ Paste a copied cell range with rows and columns transposed</strong><br><code>eb03d19a-b88d-4de4-8a64-ca0ac66f426b.skill-01</code> | <strong><code>`MOVE_TO` B2</code></strong> |
| 1 | <strong>★ Paste a copied cell range with rows and columns transposed</strong><br><code>eb03d19a-b88d-4de4-8a64-ca0ac66f426b.skill-01</code> | <strong><code>`DRAG_TO` F5</code></strong> |
| 2 | <strong>★ Paste a copied cell range with rows and columns transposed</strong><br><code>eb03d19a-b88d-4de4-8a64-ca0ac66f426b.skill-01</code> | <strong><code>`HOTKEY` &#x27;Ctrl + C&#x27; to copy the table.</code></strong> |
| 3 | <strong>★ Paste a copied cell range with rows and columns transposed</strong><br><code>eb03d19a-b88d-4de4-8a64-ca0ac66f426b.skill-01</code> | <strong><code>`RIGHT_CLICK` cell B8.</code></strong> |
| 4 | <strong>★ Paste a copied cell range with rows and columns transposed</strong><br><code>eb03d19a-b88d-4de4-8a64-ca0ac66f426b.skill-01</code> | <strong><code>`MOVE_TO` Paste Special...</code></strong> |
| 5 | <strong>★ Paste a copied cell range with rows and columns transposed</strong><br><code>eb03d19a-b88d-4de4-8a64-ca0ac66f426b.skill-01</code> | <strong><code>`CLICK` Transpose</code></strong> |

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
