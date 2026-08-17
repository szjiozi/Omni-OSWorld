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

本指南完成社区工作坊活动财务台账：将两列已有的首行公式快速填充到全部活动记录，把完整的 Event Code 列交给 Upload 工作表，并在 Event Ledger 中创建比较 Gross Revenue 与 Community Share 的簇状柱形图。

#### 启动后的初始状态检查

- 确认当前活动工作表是“Event Ledger”。
- 确认 Event Ledger 的数据位于 A1:F19，A 列为 Event Code，B 列为 Gross Revenue，C 列为 Community Share，D:F 为已填好的输入数据。
- 确认 B2 已有公式 =D2*E2，C2 已有公式 =B2+F2，而 B3:C19 在开始时仍为空白。
- 确认“Upload”工作表存在，且仅在 A1 显示标题“Event Code”；尚未填入活动代码。
- 确认 Event Ledger 中尚未插入图表。

#### 第 1 步：向下填充 Gross Revenue 公式

1. 在“Event Ledger”中单击 B2，查看输入行或公式栏，确认公式为 =D2*E2。
2. 如 B2 没有该公式，请在 B2 输入 =D2*E2 并按 Enter。
3. 保持 B2 为选中状态。将鼠标移到该单元格右下角的小方块（填充柄）。鼠标指针变为可填充状态后，双击填充柄。
4. 检查 B3:B19 是否已自动填入按各行 Registrations 与 Fee per Registration 计算的 Gross Revenue。

- 对应 skills：`04d9aeaf-7bed-4024-bedb-e10e6f00eb7f.skill-05`
- 高效操作：先确认种子公式正确，再用填充柄双击；这样 Calc 会利用相邻的连续数据行自动判断应填充到第几行，不必手动拖到最后一条记录。
- 完成标志：B2:B19 均显示货币金额；选中任一填充后的单元格（如 B19）时，可看到其公式使用对应行的相对引用，例如 =D19*E19。

#### 第 2 步：向下填充 Community Share 公式

1. 单击 C2，确认公式为 =B2+F2。
2. 如 C2 没有该公式，请在 C2 输入 =B2+F2 并按 Enter。
3. 选中 C2，找到单元格右下角的填充柄并双击它。
4. 检查 C3:C19，确认每一行均已根据同一行的 Gross Revenue 和 Sponsor Grant 自动计算 Community Share。

- 对应 skills：`21ab7b40-77c2-4ae6-8321-e00d3a086c73.skill-02`
- 高效操作：C 列依靠已连续存在的相邻记录和 B 列结果确定填充范围。双击填充柄可避免逐行复制公式。
- 完成标志：C2:C19 都已填有带两位小数的货币结果，C19 不为空；公式随行号变化，例如 C19 为 =B19+F19。

#### 第 3 步：复制 Event Code 列到 Upload

1. 仍在“Event Ledger”工作表时，单击列标“A”，使整列 A 被选中。
2. 按 Ctrl+C 复制整列。
3. 切换到“Upload”工作表。
4. 单击 A1，然后按 Ctrl+V 粘贴。若出现粘贴相关提示，使用普通粘贴即可。
5. 检查 Upload 的 A 列：标题和活动代码应一同出现。

- 对应 skills：`1273e544-688f-496b-8d89-3e0f40aa0606.skill-01`
- 高效操作：单击列标“A”会一次选中整列，包含标题和所有活动代码；这比手工框选 A1:A19 更快，也不会漏掉标题。
- 完成标志：Upload!A1 显示“Event Code”，Upload!A2:A19 显示完整活动代码列表，从 EVT-101 到 EVT-118。

#### 第 4 步：创建活动收入比较簇状柱形图

1. 切换回“Event Ledger”工作表。
2. 拖动选择连续区域 A1:C19，必须包含标题行、Event Code 列、Gross Revenue 列和 Community Share 列。
3. 选择“插入”菜单中的“图表…”，或使用工具栏上的插入图表按钮。
4. 在图表向导中选择“柱形图”，并选择“簇状柱形图”变体。
5. 确认数据范围为 A1:C19，数据系列为 Gross Revenue 与 Community Share，并让第一行作为系列名称、第一列作为类别标签（Event Code）。
6. 完成向导以将图表嵌入当前工作表；如图表放置位置遮住数据，可在不改变其数据范围的情况下拖动图表到表格旁的空白区域。

- 对应 skills：`12382c62-0cd1-4bf2-bdc8-1d20bf9b2371.skill-01`
- 高效操作：在插入图表前一次选中 A1:C19，可让 Calc 自动识别第一列为 Event Code 类别标签，并将后两列识别为两个比较数据系列。
- 完成标志：Event Ledger 上出现嵌入式簇状柱形图，横轴类别为各 Event Code，并对每个代码并列显示 Gross Revenue 和 Community Share 两个系列。

#### 第 5 步：完成最终核对

1. 检查 Event Ledger 的 B2:C19，确认两列均没有空白的活动记录行。
2. 检查“Upload”中的 A1:A19，确认标题及 18 个 Event Code 都已粘贴。
3. 单击图表并查看其图例和横轴，确认图例包含 Gross Revenue、Community Share，横轴为 Event Code。

- 对应 skills：无；这是准备或检查步骤。
- 高效操作：最终从数据、交接表和图表三个位置核对，可同时发现遗漏的公式行、漏复制的活动代码或错误的图表数据范围。
- 完成标志：计算列、Upload 活动代码清单和嵌入式比较图表均完整可见。

#### 最终结果检查

- 在“Event Ledger”中检查 B2:B19：每一行都有“Gross Revenue”计算结果，且显示为带两位小数的货币。例如 B2 的公式应为 =D2*E2，最后一条记录 B19 也不应为空。
- 检查 C2:C19：每一行都有“Community Share”计算结果，且显示为带两位小数的货币。例如 C2 的公式应为 =B2+F2，最后一条记录 C19 也不应为空。
- 切换到“Upload”工作表，确认 A1 为“Event Code”，A2:A19 已依次显示 EVT-101 至 EVT-118。
- 返回“Event Ledger”，确认工作表中存在嵌入式簇状柱形图；图表类别为 Event Code，且包含 Gross Revenue 和 Community Share 两个独立数据系列。

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
