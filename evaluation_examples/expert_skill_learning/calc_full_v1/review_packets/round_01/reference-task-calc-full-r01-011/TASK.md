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

此工作簿用于完成社区工作坊活动的收入台账：向下填充两列现有计算公式，将完整的 Event Code 列交给 `Upload` 工作表，并在 `Event Ledger` 中创建比较 Gross Revenue 与 Community Share 的簇状柱形图。

#### 启动后的初始状态检查

- 确认当前打开的工作簿含有 `Event Ledger` 和 `Upload` 两个工作表，且 `Event Ledger` 是活动工作表。
- 确认 `Event Ledger` 的标题位于第 1 行，记录连续至第 19 行；`B2` 显示公式 `=D2*E2`，`C2` 显示公式 `=B2+F2`，而 `B3:C19` 尚为空白。
- 确认 `Upload` 中只有 `A1` 的 `Event Code` 标题，`A2:A19` 为空，且 `Event Ledger` 中尚未插入图表。

#### 第 1 步：向下填充 Gross Revenue 公式

1. 在 `Event Ledger` 中单击 `B2`。确认编辑栏或单元格中的公式为 `=D2*E2`；如果 `B2` 不是该公式，直接输入 `=D2*E2` 后按 `Enter`。
2. 选中 `B2` 后，找到选中框右下角的小方块（填充柄），双击它。Calc 会根据相邻连续的记录自动向下复制公式。
3. 查看 `B2:B19`。预期所有行都会显示两位小数的货币金额，不需要进一步调整。若 `B3:B19` 中仍有空白，选中 `B2` 后再次双击填充柄；若仍未扩展到第 19 行，可将 `B2` 复制并粘贴到 `B3:B19`，以完成同一按行公式。

- 对应 skills：`04d9aeaf-7bed-4024-bedb-e10e6f00eb7f.skill-05`
- 高效操作：利用相邻的连续输入记录来决定填充终点，比手动拖动到第 19 行更快，也不容易填错行数。
- 完成标志：`B2:B19` 都已填入计算结果，最后一个活动所在的 `B19` 显示货币金额而不是空白。

#### 第 2 步：向下填充 Community Share 公式

1. 单击 `C2`，确认公式为 `=B2+F2`。如果该单元格没有此公式，输入 `=B2+F2` 并按 `Enter`。
2. 选中 `C2`，双击其右下角的填充柄，让 Calc 沿连续活动记录向下填充。
3. 预期 `C2:C19` 都会显示货币计算结果，其中每一行是 Gross Revenue 加 Sponsor Grant，因此不需要调整。若 `C3:C19` 出现空白或填充没有到最后一行，重新选中 `C2` 并双击填充柄；必要时将 `C2` 复制到 `C3:C19`。

- 对应 skills：`21ab7b40-77c2-4ae6-8321-e00d3a086c73.skill-02`
- 高效操作：先完成 Gross Revenue 列后再双击 Community Share 的填充柄，可使每一行都引用同一行已计算完成的 B 列数值。
- 完成标志：`C2:C19` 已全部显示计算后的货币金额，`C19` 也有数值。

#### 第 3 步：复制 Event Code 列到 Upload

1. 在 `Event Ledger` 中单击列标 `A`，选中整列 Event Code；可看到整列 A 被高亮。
2. 按 `Ctrl+C` 复制整列。
3. 切换到 `Upload` 工作表，单击 `A1`，然后按 `Ctrl+V` 粘贴。这样会用来源列的标题和记录替换该模板列中的对应内容。
4. 预期 `Upload` 的 `A1` 仍显示 `Event Code`，`A2:A19` 显示完整事件代码列表，因此无需调整。若粘贴后没有从 `A1` 开始，撤销该次粘贴，重新单击 `A1` 后再按 `Ctrl+V`；若只有标题而没有代码，返回 `Event Ledger` 并确认是单击列标 `A` 后复制，再执行粘贴。

- 对应 skills：`1273e544-688f-496b-8d89-3e0f40aa0606.skill-01`
- 高效操作：单击列标一次即可选中整列，能同时带上标题和所有现有、后续可见的 Event Code 单元格，无须逐行拖选。
- 完成标志：`Upload` 的 A 列从 `A1` 到 `A19` 已显示 `Event Code` 标题和 18 个 Event Code，首尾分别为 `EVT-101` 与 `EVT-118`。

#### 第 4 步：创建 Gross Revenue 与 Community Share 比较图表

1. 切换回 `Event Ledger`，选择连续区域 `A1:C19`，其中包含 `Event Code`、`Gross Revenue` 和 `Community Share` 三个标题及全部 18 条记录。
2. 使用 `Insert` > `Chart...` 打开图表向导。在图表类型中选择 `Column`，并选择 `Clustered Column` 变体；完成向导时点击 `Finish`。
3. 完成后应看到嵌入式图表，横轴类别为 Event Code，图例或系列名称为 Gross Revenue 和 Community Share，且每个 Event Code 有两根并列柱形；如果已经如此显示，不需要调整。
4. 如果类别标签显示为数值、系列不正确或缺少一个系列，双击图表进入编辑状态，打开 `Format` > `Data Ranges`。在 `Data Series` 中将类别范围改为 `Event Ledger.A2:A19`，并确认 Gross Revenue 的 `Y-Values` 为 `Event Ledger.B2:B19`、Community Share 的 `Y-Values` 为 `Event Ledger.C2:C19`；同时使用第 1 行作为系列名称。完成后关闭对话框。
5. 若图表覆盖了源数据，或没有位于工作表的空白区域，单击图表外边框以选中整个对象，再拖动它，使其左上角靠近 `E2` 且 `A1:C19` 仍清晰可见。若图表已经处于该空白区域且不遮挡源数据，则不需要移动。

- 对应 skills：`12382c62-0cd1-4bf2-bdc8-1d20bf9b2371.skill-01`
- 高效操作：在插入图表前一次性选择连续的 `A1:C19`，通常可让 Calc 自动把第一列识别为类别、后两列识别为两个数值系列，避免之后修改数据范围。
- 完成标志：`Event Ledger` 上显示一个簇状柱形嵌入式图表；每个 Event Code 都有 Gross Revenue 和 Community Share 两个独立柱形系列。

#### 最终结果检查

- `Event Ledger` 的 `B2:B19` 均为货币金额，且由 `=D2*E2` 按行计算；例如最后一行 `B19` 不再为空。
- `Event Ledger` 的 `C2:C19` 均为货币金额，且每行均为对应 Gross Revenue 加 Sponsor Grant；`C19` 已有计算结果。
- `Upload` 工作表的 `A1:A19` 包含 `Event Code` 标题以及 `EVT-101` 至 `EVT-118` 的完整列表。
- `Event Ledger` 上存在嵌入式簇状柱形图：横轴类别是 Event Code，图例中有 Gross Revenue 和 Community Share 两个独立系列，且源数据区域未被图表遮挡。

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
