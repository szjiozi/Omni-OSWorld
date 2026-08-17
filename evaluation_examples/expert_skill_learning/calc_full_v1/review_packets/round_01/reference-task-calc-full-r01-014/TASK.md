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

本操作将在“ Handoff Summary ”中制作两项交接信息：先将“Coverage Setup”的按班次排列的覆盖目标矩阵转置为按 kiosk 纵向排列的布局，再依据“CheckIn Log”建立按 Kiosk 分组、按 Ticket Code 计数的 Pivot Table。

#### 启动后的初始状态检查

- 确认工作簿已打开，当前活动工作表为“Handoff Summary”，并且该表尚未放入覆盖目标布局或 Pivot Table。
- 切换到“Coverage Setup”，确认 A1:D4 是完整的带标题矩阵：第一行为 Shift、Kiosk North、Kiosk Central、Kiosk South；其余三行包含 Morning、Midday、Afternoon 及对应数值。
- 切换到“CheckIn Log”，确认 A1:D31 是连续的数据区域，列标题包括 Check-in Time、Kiosk、Ticket Code、Repair Type，且 Ticket Code 列的数据行均非空。
- 返回“Handoff Summary”，确认将在上方放置转置表、在较下方的空白区域放置 Pivot Table，以避免两项结果互相覆盖。

#### 第 1 步：复制覆盖目标源矩阵

1. 单击底部工作表标签“Coverage Setup”。
2. 拖动选择完整区域 A1:D4；选择范围必须包含标题行和左侧的 Shift 标签列。
3. 按 Ctrl+C 复制该区域。

- 对应 skills：无；这是准备或检查步骤。
- 高效操作：一次选中完整的带标题区域并复制，可使转置后的表同时保留 kiosk、班次和数值标签，无需手工重排。
- 完成标志：A1:D4 周围显示选中边框；复制后该区域通常会出现移动的虚线边框。

#### 第 2 步：将覆盖矩阵转置到交接汇总表

1. 切换回“Handoff Summary”。
2. 单击 A1，作为转置覆盖表的左上角位置。
3. 右键单击 A1，选择“选择性粘贴”，再选择“转置”。如果界面先打开“选择性粘贴”对话框，请勾选或选择“转置”后确认。
4. 单击空白单元格以取消复制状态。

- 对应 skills：`eb03d19a-b88d-4de4-8a64-ca0ac66f426b.skill-01`
- 高效操作：在目标区域只指定左上角单元格即可；使用“选择性粘贴”的转置功能比逐个复制单元格更快，也能避免错位。
- 完成标志：A1:D4 显示旋转后的表格：第一行是 Shift、Morning、Midday、Afternoon，第一列依次是 Kiosk North、Kiosk Central、Kiosk South，所有覆盖目标数值均已保留在旋转后的对应位置。

#### 第 3 步：以签到记录作为 Pivot Table 数据源

1. 切换到“CheckIn Log”。
2. 选择 A1:D31，包括四个字段标题及全部 30 条记录。
3. 打开“数据”菜单，选择“数据透视表”，再选择“插入或编辑…”。
4. 在数据源选择中保留当前选中的单元格区域，并继续进入 Pivot Table 布局窗口。

- 对应 skills：无；这是准备或检查步骤。
- 高效操作：选择完整的连续数据区域而非单独一列，Pivot Table 才能同时使用 Kiosk 作为分组字段和 Ticket Code 作为计数字段。
- 完成标志：显示 Pivot Table 的布局窗口，可看到 Check-in Time、Kiosk、Ticket Code 和 Repair Type 等可用字段。

#### 第 4 步：设置 kiosk 分组与票号数据字段

1. 在布局窗口中，将字段“Kiosk”拖入“行字段”区域。
2. 将字段“Ticket Code”拖入“数据字段”区域。
3. 不要将 Check-in Time 或 Repair Type 放入行、列或数据区域，除非界面自动带入后需要将其移除。

- 对应 skills：无；这是准备或检查步骤。
- 高效操作：只使用完成任务所需的两个字段：将 Kiosk 放在行区域、将 Ticket Code 放在数据区域，可让结果保持简洁且易于交接查看。
- 完成标志：布局窗口的“行字段”区域包含 Kiosk，“数据字段”区域包含 Ticket Code。

#### 第 5 步：将 Ticket Code 数据字段设置为计数

1. 在 Pivot Table 布局窗口的“数据字段”区域中，双击“Ticket Code”字段。
2. 在数据字段选项中选择“Count”作为汇总方式；不要选择 Sum。
3. 确认设置返回布局窗口，并检查 Ticket Code 数据字段的显示名称已反映 Count 或计数。
4. 确认布局设置以继续选择输出位置。

- 对应 skills：`30e3e107-1cfb-46ee-a755-2cd080d7ba6a.skill-08`
- 高效操作：在刚加入数据字段后立即打开其设置，可以直接确认聚合方式，避免先生成不符合要求的汇总表后再返工。
- 完成标志：Ticket Code 数据字段的汇总方式显示为 Count/计数，表示它将统计每个 kiosk 中非空 Ticket Code 的出现次数。

#### 第 6 步：将 kiosk 计数 Pivot Table 放到交接汇总表

1. 在 Pivot Table 的输出位置设置中，选择将结果放在现有工作表。
2. 指定“Handoff Summary”上的 A7 作为输出区域左上角；该位置位于 A1:D4 转置表下方，并留有空白行。
3. 确认创建 Pivot Table。必要时切换回“Handoff Summary”查看结果。

- 对应 skills：无；这是准备或检查步骤。
- 高效操作：将 Pivot Table 放在转置表下方并预留空行，能让两个交接输出清晰分开，也便于以后刷新或扩展 Pivot Table。
- 完成标志：“Handoff Summary”从 A7 附近开始出现 Pivot Table，其中按 Kiosk 列出 Kiosk North、Kiosk Central、Kiosk South，并显示 Ticket Code 的 Count/计数列及总计。

#### 第 7 步：核对交接汇总输出

1. 检查上方转置表的行列方向：kiosk 应在第一列纵向显示，Morning、Midday、Afternoon 应横向显示在第一行。
2. 检查 Pivot Table 的行项目是 kiosk，数据字段是 Ticket Code 的 Count/计数。
3. 确认 Pivot Table 的三个 kiosk 计数相加为 30，并确认其位置未覆盖转置覆盖表。

- 对应 skills：无；这是准备或检查步骤。
- 高效操作：最后同时核对布局方向和计数汇总方式，可快速发现将数据字段误设为求和或将 Pivot Table 放错位置等问题。
- 完成标志：“Handoff Summary”清楚地同时展示转置后的覆盖目标布局和独立的 kiosk Ticket Code 计数 Pivot Table。

#### 最终结果检查

- 查看“Handoff Summary”：上方应有一个 4×4 的覆盖目标表，第一行依次为 Shift、Morning、Midday、Afternoon，第一列为 Kiosk North、Kiosk Central、Kiosk South；各目标数字应与“Coverage Setup”中对应的原始数据一致但方向已旋转。
- 在“Handoff Summary”下方确认存在 Pivot Table：行标签按 Kiosk North、Kiosk Central、Kiosk South 分组，并显示 Ticket Code 的计数结果（通常还会有总计行）。
- 确认 Pivot Table 的数据字段标题明确包含“Count”或“计数”，而不是“Sum”或“求和”；三个 kiosk 的计数合计应为 CheckIn Log 中的 30 条数据记录。
- 确认两个输出没有重叠，且“Coverage Setup”和“CheckIn Log”中的原始数据仍保留。

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
