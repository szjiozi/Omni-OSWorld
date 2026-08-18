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

在现有工作簿中，将 `Coverage Setup` 的完整班次与服务台覆盖目标矩阵转置到 `Handoff Summary`，然后根据 `CheckIn Log` 创建以 `Kiosk` 为行标签、以非空 `Ticket Code` 出现次数为值的 Pivot Table。

#### 启动后的初始状态检查

- 确认工作簿已经打开，当前活动工作表为 `Handoff Summary`，并且该表仍为空白，没有已有的转置表或 Pivot Table。
- 点击 `Coverage Setup` 工作表标签，确认 A1:D4 是完整连续的覆盖目标矩阵，首行包含 `Shift`、`Kiosk North`、`Kiosk Central`、`Kiosk South`。
- 点击 `CheckIn Log` 工作表标签，确认 A1:D31 是连续的数据表，且含有 `Kiosk` 与 `Ticket Code` 列；每条数据记录的 `Ticket Code` 都非空。

#### 第 1 步：转置覆盖目标矩阵

1. 在 `Coverage Setup` 工作表中，选中 A1:D4；该范围必须包含标题行和三条班次记录。
2. 按 `Ctrl+C` 复制该矩阵。
3. 切换到 `Handoff Summary`，选择 A1 作为上方输出区域的左上角。
4. 右键单击 A1，打开 `Paste Special`，选择 `Transpose`。

- 对应 skills：`eb03d19a-b88d-4de4-8a64-ca0ac66f426b.skill-01`
- 高效操作：一次选中带标题的完整 A1:D4 区域并复制，能让转置结果同时保留行列标签，无需手工重排。
- 完成标志：A1:D4 出现旋转后的完整表格：班次名称横向排列在首行，`Kiosk North`、`Kiosk Central`、`Kiosk South` 纵向排列在首列，所有覆盖目标数值仍在对应的 kiosk 与班次交叉位置。

#### 第 2 步：建立按服务台汇总的 Pivot Table 布局

1. 切换到 `CheckIn Log`，选中 A1:D31 的完整数据区域，包括标题行。
2. 打开 `Data` > `Pivot Table` > `Insert or Edit...`。
3. 在 Pivot Table 布局对话框中，找到字段列表中的 `Kiosk` 和 `Ticket Code`。将 `Kiosk` 放入 `Row Fields` 区域，将 `Ticket Code` 放入 `Data Fields` 区域。
4. 在结果位置设置中，选择将结果输出到 `Handoff Summary` 的未使用区域，例如 A7。若默认预览已显示结果将从 A7 附近开始、且不会覆盖 A1:D4 的转置表，则无需调整。若预览或位置设置显示结果会与转置表重叠，请把结果起始单元格改为 A7 或另一块足够大的空白区域。

- 对应 skills：无；这是准备或检查步骤。
- 高效操作：从表内任意单元格开始选择整个连续数据区域，可避免遗漏标题或末尾记录；使用完整表作为 Pivot Table 来源可让字段名称自动可用。
- 完成标志：布局对话框中，`Kiosk` 显示在 `Row Fields`，`Ticket Code` 显示在 `Data Fields`，并且结果目标是 `Handoff Summary` 中不与转置表重叠的空白区域。

#### 第 3 步：将 Ticket Code 数据字段设为计数

1. 在 Pivot Table 布局对话框的 `Data Fields` 区域，双击 `Ticket Code` 字段条目以打开其数据字段选项。
2. 选择 `Count` 作为汇总方式，然后确认返回 Pivot Table 布局。
3. 完成布局对话框并创建 Pivot Table。若创建后的值字段标题已表示 `Count` 且每个 kiosk 显示一个数值，则无需调整。
4. 如果 Pivot Table 的值字段标题显示 `Sum`，或 `Ticket Code` 没有按出现次数统计，请在 Pivot Table 内双击任意单元格以编辑它，双击 `Data Fields` 中的 `Ticket Code`，选择 `Count` 后确认并更新表格。

- 对应 skills：`30e3e107-1cfb-46ee-a755-2cd080d7ba6a.skill-08`
- 高效操作：刚把 `Ticket Code` 放入 `Data Fields` 后立即修改汇总方式，能避免先生成不正确的默认汇总结果再返工。
- 完成标志：`Handoff Summary` 中出现单独的 Pivot Table：行标签为各 kiosk，值字段标题含有 `Count`，并显示每个 kiosk 的 `Ticket Code` 非空记录数。

#### 第 4 步：核对交付页面

1. 查看 `Handoff Summary`：确认转置覆盖表仍完整可见，Pivot Table 位于不同的空白区域。
2. 确认 Pivot Table 的行中列出了 `Kiosk North`、`Kiosk Central`、`Kiosk South`，且数值字段是 `Ticket Code` 的 `Count`。
3. 如有重叠，单击 Pivot Table 外边框选中整个对象并将其拖到更空的区域，使源转置表保持可见；不要移动或改写转置表中的单元格内容。

- 对应 skills：无；这是准备或检查步骤。
- 高效操作：通过查看字段标题和行标签即可快速确认汇总逻辑，无需逐条手算所有记录。
- 完成标志：`Handoff Summary` 清晰同时展示转置后的 kiosk-by-shift 覆盖目标布局，以及按 kiosk 统计的 `Ticket Code` 计数 Pivot Table。

#### 最终结果检查

- `Handoff Summary` 中上方有一个完整的 4×4 覆盖目标表：第一列为 `Shift`、`Morning`、`Midday`、`Afternoon`，第一行依次显示 `Shift`、`Morning`、`Midday`、`Afternoon`；`Kiosk North`、`Kiosk Central`、`Kiosk South` 位于纵向行标签中，数值与 `Coverage Setup` 的原表旋转对应。
- `Handoff Summary` 的另一块空白区域中有 Pivot Table，按 `Kiosk` 分行，显示 `Kiosk North`、`Kiosk Central`、`Kiosk South`，并有 `Ticket Code` 的计数结果。
- Pivot Table 的数据字段标题明确表示 `Count`，而不是 `Sum`；三个 kiosk 的计数合计应对应 `CheckIn Log` 中 30 条非空 `Ticket Code` 记录。
- 两个输出均位于 `Handoff Summary`，彼此不重叠，且没有遮挡转置覆盖表。

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
