# Community Workshop Event Finance

- Reference task: `reference-task-calc-full-r01-011`
- Application: `libreoffice_calc`
- Review decision: `pending`

## Task instruction

Complete the Event Ledger for the community workshop program: calculate Gross Revenue as Registrations multiplied by Fee per Registration and Community Share as Gross Revenue plus Sponsor Grant for every event. Populate the Upload handoff sheet with the complete Event Code column, then add a clustered column chart on Event Ledger comparing Gross Revenue and Community Share for each Event Code.

## Required skills

### 1. Autofill a formula downward by double-clicking the fill handle

Skill ID: `04d9aeaf-7bed-4024-bedb-e10e6f00eb7f.skill-05`

Procedure:

1. Select a formula cell, such as B2.
2. Double-click the fill handle at the cell's bottom-right corner. Calc fills the formula down through the contiguous data region determined by adjacent populated cells.
3. Repeat on another formula column when needed, such as C2 or D2; relative row references update in each filled row.

Efficiency tip: Double-clicking the fill handle is faster and less error-prone than manually dragging to an estimated final row when an adjacent column defines the data extent.

Source task: `04d9aeaf-7bed-4024-bedb-e10e6f00eb7f`

Source instruction: In a new sheet with 4 headers "Year", "CA changes", "FA changes", and "OA changes", calculate the percentage annual changes compared to last year in 2015 to 2019 for the Current Assets, Fixed Assets, and Other Assets columns. 

Directly referenced source actions:

- Action 16: <code>`CLICK` cell B2</code>
- Action 17: <code>`DOUBLE_CLICK` bottom right corner</code>
- Action 21: <code>`CLICK` cell C2</code>
- Action 22: <code>`DOUBLE_CLICK` bottom right corner</code>
- Action 23: <code>`MOVE_TO` cell D2</code>
- Action 24: <code>`DOUBLE_CLICK` bottom right corner</code>

### 2. Autofill a formula downward by double-clicking the fill handle

Skill ID: `21ab7b40-77c2-4ae6-8321-e00d3a086c73.skill-02`

Procedure:

1. Select the cell that contains the completed formula.
2. Double-click the small fill handle at the cell’s bottom-right corner. Calc extends the formula down through the contiguous neighboring data rows; for example, a formula in C2 is filled down alongside populated rows in adjacent columns.

Efficiency tip: Double-clicking the fill handle is faster and less error-prone than dragging it through a long adjacent data region.

Source task: `21ab7b40-77c2-4ae6-8321-e00d3a086c73`

Source instruction: Please calculate the period rate for my data in a new column with header "Period Rate (%)", convert the results as number type, and highlight the highest result with green (#00ff00) font.

Directly referenced source actions:

- Action 5: <code>`CLICK` cell C2</code>
- Action 6: <code>`DOUBLE_CLICK` bottom right corner of the cell C2</code>

### 3. Copy an entire spreadsheet column

Skill ID: `1273e544-688f-496b-8d89-3e0f40aa0606.skill-01`

Procedure:

1. Click the column header letter for the column you want to copy, such as column A. Calc highlights the entire column, including any header cell.
2. Press Ctrl+C to copy the selected column to the clipboard.

Efficiency tip: Click the column letter once rather than dragging through all populated cells; this selects the complete column, including its header, in one action.

Source task: `1273e544-688f-496b-8d89-3e0f40aa0606`

Source instruction: Copy the "Revenue" column along with the header to a new sheet named "Sheet2".

Directly referenced source actions:

- Action 0: <code>`CLICK` on grey box with A for selecting entire column</code>
- Action 1: <code>`HOTKEY` ctrl+c</code>

### 4. Insert a chart from a selected data range

Skill ID: `12382c62-0cd1-4bf2-bdc8-1d20bf9b2371.skill-01`

Procedure:

1. Select the contiguous cell range containing the category labels and numeric series, for example a table with week labels in the first column and two value columns.
2. Use the Insert Chart toolbar icon to create a chart based on the current selection.
3. In the chart wizard, choose a Column chart with the Clustered Column variant if it is not already selected, then finish inserting the chart.

Efficiency tip: Select the complete source range before inserting the chart so Calc can create the chart with the correct data series and category labels without later manual range edits.

Source task: `12382c62-0cd1-4bf2-bdc8-1d20bf9b2371`

Source instruction: Create a clustered column chart showing the Sales and COGS data for each week in a new sheet. Set the chart title as "Sales & COGS".

Directly referenced source actions:

- Action 0: <code>`HOTKEY` ctrl-A</code>
- Action 1: <code>`CLICK` insert chart icon</code>

## Initial state preview

### Event Ledger

![Event_Ledger.png](artifact/previews/Event_Ledger.png)

### Upload

![Upload.png](artifact/previews/Upload.png)

## Operator guide

### Existing operation-intent guide

#### Demonstration 1

- Skill: `04d9aeaf-7bed-4024-bedb-e10e6f00eb7f.skill-05`
- Intent: Extend the Gross Revenue seed calculation from B2 through every listed event by double-clicking its fill handle.
- Efficiency: Use the existing populated records in the adjacent input columns as the boundary, avoiding a manual drag through the event list.
- Visible success: Gross Revenue cells B2:B19 display calculated currency amounts, with the formula filled through the last event row.

#### Demonstration 2

- Skill: `21ab7b40-77c2-4ae6-8321-e00d3a086c73.skill-02`
- Intent: Extend the Community Share seed calculation from C2 through every listed event by double-clicking its fill handle.
- Efficiency: After Gross Revenue is available, double-click the Community Share seed cell's fill handle so row-relative references are extended consistently.
- Visible success: Community Share cells C2:C19 are filled with calculated currency values, including the final event row.

#### Demonstration 3

- Skill: `1273e544-688f-496b-8d89-3e0f40aa0606.skill-01`
- Intent: Copy the entire Event Code column from Event Ledger for the Upload handoff sheet.
- Efficiency: Select the A column header directly rather than selecting only the visible event-code cells, so the header and complete column are copied together.
- Visible success: The full Event Code column is visibly selected and copied; after the ordinary paste step, Upload shows the Event Code header and all event codes in column A.

#### Demonstration 4

- Skill: `12382c62-0cd1-4bf2-bdc8-1d20bf9b2371.skill-01`
- Intent: Insert a clustered column chart comparing Gross Revenue and Community Share by Event Code.
- Efficiency: Select the already contiguous A1:C19 comparison table before chart insertion so Event Code labels and both calculated series are detected without later source-range edits.
- Visible success: An embedded clustered column chart is present on Event Ledger with Event Code categories and separate Gross Revenue and Community Share series.

Recording start: Event Ledger is active with only B2 and C2 seeded as formulas, all lower calculated cells blank, no chart, and Upload containing only its header.

Recording end: Event Ledger has completed B2:C19 calculations and an embedded clustered column comparison chart sourced from A1:C19; Upload A1:A19 contains the copied Event Code header and event-code list.

Allowed variation: The expert may complete the two calculated columns in either order, use keyboard shortcuts where appropriate, and use any efficient equivalent chart-insertion path, provided the intended full-column copy, formula fills, and clustered comparison chart are visibly demonstrated.

### 中文详细参考方案

> 以下是一个可以参考的操作 guide。标注者可以根据实际 LibreOffice 界面采用等价操作。

本指南完成社区工作坊活动账本：先将两列已有首行公式快速填充到所有活动，再把完整的 Event Code 列交给 `Upload` 工作表，最后在 `Event Ledger` 中建立 Gross Revenue 与 Community Share 的簇状柱形比较图。

#### 启动后的初始状态检查

- 确认当前打开的是目标工作簿，且活动工作表为 `Event Ledger`。
- 确认 `Event Ledger` 的表头位于第 1 行，事件数据从第 2 行连续到第 19 行；`A1:C19` 中的 B、C 列除第 2 行外尚未填充。
- 单击 `B2` 和 `C2`，在输入行确认已有公式分别为 `=D2*E2` 与 `=B2+F2`。若其中一个公式意外缺失，先在对应单元格输入该公式并按 `Enter`。
- 确认存在名为 `Upload` 的工作表，其中目前只有 `A1` 的 `Event Code` 表头，`A2:A19` 为空。
- 确认 `Event Ledger` 中尚未有图表。

#### 第 1 步：向下填充 Gross Revenue 公式

1. 在 `Event Ledger` 中单击公式单元格 `B2`。
2. 将指针移到所选单元格右下角的小方块（填充柄）；当可以拖动时，双击该填充柄。
3. 不要修改已填充单元格中的相对引用；Calc 会按行自动将公式延伸。

- 对应 skills：`04d9aeaf-7bed-4024-bedb-e10e6f00eb7f.skill-05`
- 高效操作：双击填充柄会按照相邻连续数据区域自动判断最后一行，比手动拖到第 19 行更快，也避免拖错范围。
- 完成标志：`B2:B19` 均显示货币金额，且选中任一后续单元格（如 `B3`）可见按本行计算的公式，例如 `=D3*E3`。

#### 第 2 步：向下填充 Community Share 公式

1. 单击 `C2`，确认它仍包含公式 `=B2+F2`。
2. 双击 `C2` 右下角的小方块填充柄，使公式沿相邻连续事件记录向下扩展。
3. 保留公式的默认相对引用，不要把 `B2` 或 `F2` 改成固定引用。

- 对应 skills：`21ab7b40-77c2-4ae6-8321-e00d3a086c73.skill-02`
- 高效操作：先完成 B 列后再填充 C 列，可让 Community Share 公式在每一行都引用已计算完成的同一行 Gross Revenue。
- 完成标志：`C2:C19` 均填有货币金额；单击 `C19` 时可见其公式对应第 19 行，且最后一项不为空。

#### 第 3 步：复制完整 Event Code 列到 Upload

1. 在 `Event Ledger` 中，单击列标 `A`，选中整个 Event Code 列。
2. 按 `Ctrl+C` 复制整列。
3. 切换到 `Upload` 工作表，单击 `A1`，然后按 `Ctrl+V` 粘贴。
4. 如出现粘贴选项，保持普通粘贴即可，使来源列的表头和事件代码一起写入目标列。

- 对应 skills：`1273e544-688f-496b-8d89-3e0f40aa0606.skill-01`
- 高效操作：直接选择列标 `A` 可一次包含表头和所有现有、后续可见单元格，不必逐行框选事件代码。
- 完成标志：`Upload` 的 A 列显示 `Event Code` 表头以及从 `EVT-101` 到 `EVT-118` 的完整连续代码列表。

#### 第 4 步：创建 Gross Revenue 与 Community Share 簇状柱形图

1. 切换回 `Event Ledger`。
2. 选中连续区域 `A1:C19`，其中包括 Event Code 表头、Gross Revenue 表头、Community Share 表头及全部 18 行数据。
3. 使用工具栏上的 `Insert Chart` 图标，或打开 `Insert` > `Chart...`。
4. 在图表向导中选择 `Column` 图表类型，并选择 `Clustered Column` 变体。
5. 确认类别来自 Event Code，数据系列为 Gross Revenue 和 Community Share；然后点击 `Finish` 将图表嵌入当前工作表。

- 对应 skills：`12382c62-0cd1-4bf2-bdc8-1d20bf9b2371.skill-01`
- 高效操作：在插入图表前一次选中完整的 `A1:C19`，可让 Calc 自动识别第一列为类别标签、第一行为系列名称，减少后续调整数据范围的需要。
- 完成标志：`Event Ledger` 上出现嵌入式柱形图，横轴按 Event Code 显示活动类别，并为 Gross Revenue 和 Community Share 显示并列的两组柱形及对应系列标识。

#### 第 5 步：完成最终可见性检查

1. 在 `Event Ledger` 中检查 `B19` 和 `C19` 都已计算，确保两个公式列没有在中途停止。
2. 在 `Upload` 中检查 `A1:A19`，确认表头和 18 个事件代码均已粘贴。
3. 在 `Event Ledger` 中检查图表仍可见，并确认它比较的是 Gross Revenue 与 Community Share，而不是输入列 D:F。

- 对应 skills：无；这是准备或检查步骤。
- 高效操作：最终检查时优先查看末行和图表系列；这些位置最容易发现填充范围不足、粘贴遗漏或图表源范围选错的问题。
- 完成标志：两个计算列、`Upload` 的完整事件代码清单以及 `Event Ledger` 的两系列簇状柱形图均同时存在并可见。

#### 最终结果检查

- 在 `Event Ledger` 中检查 `B2:B19`：每一行都有 Gross Revenue 的货币计算结果；例如 `B2` 的公式为 `=D2*E2`，末行 `B19` 不应为空。
- 检查 `C2:C19`：每一行都有 Community Share 的货币计算结果；例如 `C2` 的公式为 `=B2+F2`，末行 `C19` 不应为空。
- 切换到 `Upload`，确认 `A1` 为 `Event Code`，且 `A2:A19` 依次包含全部 18 个事件代码，最后一个为 `EVT-118`。
- 返回 `Event Ledger`，确认工作表中存在嵌入式簇状柱形图；图表使用 Event Code 作为类别，并有 Gross Revenue 与 Community Share 两个独立数据系列。

## Source-task similarity review

| Measure | Maximum | Most similar source task |
| --- | ---: | --- |
| Lexical sequence similarity | 0.336957 | 3a7c8185-25c1-4941-bd7b-96e823c9f21f |
| Semantic cosine similarity | 0.487496 | 035f41ba-6653-43ab-aa63-c86d449d62e5 |

Similarity scores are reviewer aids, not automatic acceptance thresholds. Inspect the contributing source tasks and their complete ordered actions below.

### Source task `04d9aeaf-7bed-4024-bedb-e10e6f00eb7f`

Original instruction:

> In a new sheet with 4 headers "Year", "CA changes", "FA changes", and "OA changes", calculate the percentage annual changes compared to last year in 2015 to 2019 for the Current Assets, Fixed Assets, and Other Assets columns. 

Required skills derived from this source task:

- **Autofill a formula downward by double-clicking the fill handle** — `04d9aeaf-7bed-4024-bedb-e10e6f00eb7f.skill-05`

Complete ordered single-action sequence:

| Action | Related required skill | Original single action |
| ---: | --- | --- |
| 0 |  | <code>`CLICK` on cell A3</code> |
| 1 |  | <code>`DRAG_TO` cell A7</code> |
| 2 |  | <code>`HOTKEY` Ctrl-c</code> |
| 3 |  | <code>`CLICK` the + button to the left of Sheet1 to add a new sheet</code> |
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
| 16 | <strong>★ Autofill a formula downward by double-clicking the fill handle</strong><br><code>04d9aeaf-7bed-4024-bedb-e10e6f00eb7f.skill-05</code> | <strong><code>`CLICK` cell B2</code></strong> |
| 17 | <strong>★ Autofill a formula downward by double-clicking the fill handle</strong><br><code>04d9aeaf-7bed-4024-bedb-e10e6f00eb7f.skill-05</code> | <strong><code>`DOUBLE_CLICK` bottom right corner</code></strong> |
| 18 |  | <code>`CLICK` cell B2</code> |
| 19 |  | <code>`MOVE_TO` bottom right corner of the cell B2</code> |
| 20 |  | <code>`DRAG_TO` cell D2</code> |
| 21 | <strong>★ Autofill a formula downward by double-clicking the fill handle</strong><br><code>04d9aeaf-7bed-4024-bedb-e10e6f00eb7f.skill-05</code> | <strong><code>`CLICK` cell C2</code></strong> |
| 22 | <strong>★ Autofill a formula downward by double-clicking the fill handle</strong><br><code>04d9aeaf-7bed-4024-bedb-e10e6f00eb7f.skill-05</code> | <strong><code>`DOUBLE_CLICK` bottom right corner</code></strong> |
| 23 | <strong>★ Autofill a formula downward by double-clicking the fill handle</strong><br><code>04d9aeaf-7bed-4024-bedb-e10e6f00eb7f.skill-05</code> | <strong><code>`MOVE_TO` cell D2</code></strong> |
| 24 | <strong>★ Autofill a formula downward by double-clicking the fill handle</strong><br><code>04d9aeaf-7bed-4024-bedb-e10e6f00eb7f.skill-05</code> | <strong><code>`DOUBLE_CLICK` bottom right corner</code></strong> |
| 25 |  | <code>`CLICK` cell B2</code> |
| 26 |  | <code>`DRAG_TO` D6</code> |
| 27 |  | <code>`CLICK` percent symbol</code> |

### Source task `12382c62-0cd1-4bf2-bdc8-1d20bf9b2371`

Original instruction:

> Create a clustered column chart showing the Sales and COGS data for each week in a new sheet. Set the chart title as "Sales & COGS".

Required skills derived from this source task:

- **Insert a chart from a selected data range** — `12382c62-0cd1-4bf2-bdc8-1d20bf9b2371.skill-01`

Complete ordered single-action sequence:

| Action | Related required skill | Original single action |
| ---: | --- | --- |
| 0 | <strong>★ Insert a chart from a selected data range</strong><br><code>12382c62-0cd1-4bf2-bdc8-1d20bf9b2371.skill-01</code> | <strong><code>`HOTKEY` ctrl-A</code></strong> |
| 1 | <strong>★ Insert a chart from a selected data range</strong><br><code>12382c62-0cd1-4bf2-bdc8-1d20bf9b2371.skill-01</code> | <strong><code>`CLICK` insert chart icon</code></strong> |
| 2 |  | <code>`CLICK` chart elements on right sidebar</code> |
| 3 |  | <code>`CLICK` title text box</code> |
| 4 |  | <code>`TYPING` &#x27;Sales &amp; COGS&#x27;</code> |
| 5 |  | <code>`PRESS` enter</code> |
| 6 |  | <code>`CLICK` on cell A1 to cancel out of current menu</code> |
| 7 |  | <code>`CLICK` on chart to select it</code> |
| 8 |  | <code>`HOTKEY` ctrl-X</code> |
| 9 |  | <code>`CLICK` on + to left of sheet1</code> |
| 10 |  | <code>`HOTKEY` ctrl+v</code> |

### Source task `1273e544-688f-496b-8d89-3e0f40aa0606`

Original instruction:

> Copy the "Revenue" column along with the header to a new sheet named "Sheet2".

Required skills derived from this source task:

- **Copy an entire spreadsheet column** — `1273e544-688f-496b-8d89-3e0f40aa0606.skill-01`

Complete ordered single-action sequence:

| Action | Related required skill | Original single action |
| ---: | --- | --- |
| 0 | <strong>★ Copy an entire spreadsheet column</strong><br><code>1273e544-688f-496b-8d89-3e0f40aa0606.skill-01</code> | <strong><code>`CLICK` on grey box with A for selecting entire column</code></strong> |
| 1 | <strong>★ Copy an entire spreadsheet column</strong><br><code>1273e544-688f-496b-8d89-3e0f40aa0606.skill-01</code> | <strong><code>`HOTKEY` ctrl+c</code></strong> |
| 2 |  | <code>`CLICK` on + to left of sheet1 if sheet2 does not exist, else click on sheet2</code> |
| 3 |  | <code>`HOTKEY` ctrl+v</code> |

### Source task `21ab7b40-77c2-4ae6-8321-e00d3a086c73`

Original instruction:

> Please calculate the period rate for my data in a new column with header "Period Rate (%)", convert the results as number type, and highlight the highest result with green (#00ff00) font.

Required skills derived from this source task:

- **Autofill a formula downward by double-clicking the fill handle** — `21ab7b40-77c2-4ae6-8321-e00d3a086c73.skill-02`

Complete ordered single-action sequence:

| Action | Related required skill | Original single action |
| ---: | --- | --- |
| 0 |  | <code>`CLICK` on cell C1</code> |
| 1 |  | <code>`TYPING` &#x27;Period Rate (%)&#x27;</code> |
| 2 |  | <code>`PRESS` enter</code> |
| 3 |  | <code>`TYPING` &#x27;=A2/B2&#x27;</code> |
| 4 |  | <code>`PRESS` enter</code> |
| 5 | <strong>★ Autofill a formula downward by double-clicking the fill handle</strong><br><code>21ab7b40-77c2-4ae6-8321-e00d3a086c73.skill-02</code> | <strong><code>`CLICK` cell C2</code></strong> |
| 6 | <strong>★ Autofill a formula downward by double-clicking the fill handle</strong><br><code>21ab7b40-77c2-4ae6-8321-e00d3a086c73.skill-02</code> | <strong><code>`DOUBLE_CLICK` bottom right corner of the cell C2</code></strong> |
| 7 |  | <code>`CLICK` on the 0.0 icon that converts the cell to number type</code> |
| 8 |  | <code>`CLICK` format</code> |
| 9 |  | <code>`MOVE_TO` &#x27;conditional...&#x27;</code> |
| 10 |  | <code>`CLICK` &#x27;condition&#x27;</code> |
| 11 |  | <code>`CLICK` &#x27;cell value&#x27; dropdown</code> |
| 12 |  | <code>`CLICK` &#x27;Formula is&#x27; option</code> |
| 13 |  | <code>`CLICK` text field</code> |
| 14 |  | <code>`TYPING` $C2=MAX($C$2:$C$25)</code> |
| 15 |  | <code>`CLICK` accent dropdown</code> |
| 16 |  | <code>`CLICK` new style</code> |
| 17 |  | <code>`CLICK` font effects</code> |
| 18 |  | <code>`CLICK` font color dropdown</code> |
| 19 |  | <code>`CLICK` custom color...</code> |
| 20 |  | <code>`DOUBLE_CLICK` Hex text box</code> |
| 21 |  | <code>`TYPING` &#x27;00ff00&#x27;</code> |
| 22 |  | <code>`PRESS` enter</code> |
| 23 |  | <code>`CLICK` OK</code> |
| 24 |  | <code>`CLICK` OK</code> |

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
