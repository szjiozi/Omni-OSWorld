# Solar Microgrid Review

- Reference task: `reference-task-calc-full-r01-017`
- Application: `libreoffice_calc`
- Review decision: `pending`

## Task instruction

Complete the daily net-delivery and target-variance calculations for all solar microgrid readings, then create a line chart of net delivery by reading date. Title it 'Daily Net Delivery Trend' and place it in the open area to the right of the data table.

## Required skills

### 1. Autofill a formula down a contiguous column

Skill ID: `4172ea6e-6b77-4edb-a9cc-c0014bd1603b.skill-02`

Procedure:

1. Select the cell containing the formula at the top of the output column.
2. Double-click the small fill handle at the cell’s bottom-right corner. Calc extends the formula downward alongside the adjacent contiguous data range, adjusting relative references for each row.
3. For example, double-clicking the fill handle of C2 containing `=A2+B2` fills subsequent rows with row-adjusted formulas such as `=A3+B3`.

Efficiency tip: Double-clicking the fill handle is faster than dragging it through a long contiguous table and avoids manually estimating the last row.

Source task: `4172ea6e-6b77-4edb-a9cc-c0014bd1603b`

Source instruction: I want to work out the maturity date for all the loans. Please do it for me in a new column with header "Maturity Date".

Directly referenced source actions:

- Action 5: <code>`CLICK` cell C2`</code>
- Action 6: <code>`DOUBLE_CLICK` bottom right corner of the cell C2`</code>

### 2. Reposition a chart object by dragging

Skill ID: `347ef137-7eeb-4c80-a3bb-0951f26a8aff.skill-02`

Procedure:

1. Click or point at the chart object's edge to target the chart rather than an individual data series.
2. Drag the chart from its top edge toward the desired location, such as moving it to the right side of the worksheet page.
3. Scroll horizontally if necessary to reach or verify the new placement while keeping the chart layout organized.

Efficiency tip: Reposition a chart by dragging it directly rather than reopening chart settings; scroll only as needed to expose the intended destination.

Source task: `347ef137-7eeb-4c80-a3bb-0951f26a8aff`

Source instruction: Here are two tables recording the per-month costs in 2019 and 2020. I want to create two column bar charts reflecting per-month total costs for each year from these data. Help me, Mr. Assistant!

Directly referenced source actions:

- Action 13: <code>`MOVE_TO` top edge of chart</code>
- Action 14: <code>`DRAG_TO` right edge of page</code>
- Action 15: <code>`SCROLL_LEFT`</code>

### 3. Set a chart title using chart elements

Skill ID: `12382c62-0cd1-4bf2-bdc8-1d20bf9b2371.skill-02`

Procedure:

1. Click the chart, then open its Chart Elements controls in the right sidebar.
2. Enable or select the chart title element and click the title text box.
3. Type the desired title, for example `Sales & COGS`, and press Enter to apply the text.

Efficiency tip: Edit the title directly through the chart-elements title control instead of reopening the full chart wizard.

Source task: `12382c62-0cd1-4bf2-bdc8-1d20bf9b2371`

Source instruction: Create a clustered column chart showing the Sales and COGS data for each week in a new sheet. Set the chart title as "Sales & COGS".

Directly referenced source actions:

- Action 2: <code>`CLICK` chart elements on right sidebar</code>
- Action 3: <code>`CLICK` title text box</code>
- Action 4: <code>`TYPING` &#x27;Sales &amp; COGS&#x27;</code>
- Action 5: <code>`PRESS` enter</code>

### 4. Autofill a formula down a contiguous data range

Skill ID: `7efeb4b1-3d19-4762-b163-63328d66303b.skill-02`

Procedure:

1. Select the cell containing the formula to propagate, for example B2.
2. Move to the small square at the cell's bottom-right corner (the fill handle) and double-click it.
3. Calc fills the formula downward alongside the contiguous neighboring data range, adjusting relative references for each row. For example, `ROW(B2)` in B2 becomes `ROW(B3)` in B3.

Efficiency tip: Double-clicking the fill handle is faster than dragging it through a long table and typically stops at the end of adjacent populated data.

Source task: `7efeb4b1-3d19-4762-b163-63328d66303b`

Source instruction: Fill the Sequence Numbers as "No. #" in the "Seq No." column

Directly referenced source actions:

- Action 3: <code>`CLICK` B2</code>
- Action 4: <code>`DOUBLE_CLICK` bottom right corner of cell</code>

## Initial state preview

### Daily Readings

![Daily_Readings.png](artifact/previews/Daily_Readings.png)

## Operator guide

### Existing operation-intent guide

#### Demonstration 1

- Skill: `4172ea6e-6b77-4edb-a9cc-c0014bd1603b.skill-02`
- Intent: Propagate the seeded Net Delivered kWh calculation from E2 through the contiguous daily-record range.
- Efficiency: Use the fill handle’s double-click behavior rather than dragging through all 24 records.
- Visible success: Every daily row from E2 through E25 displays a row-adjusted net-delivery result, with no blanks in the calculated column.

#### Demonstration 2

- Skill: `7efeb4b1-3d19-4762-b163-63328d66303b.skill-02`
- Intent: Propagate the seeded Variance to Target kWh calculation from F2 through the same contiguous daily-record range.
- Efficiency: Use the fill handle’s double-click behavior so the calculation stops with the adjacent uninterrupted table.
- Visible success: Every daily row from F2 through F25 displays a row-adjusted variance result, with no blanks in the calculated column.

#### Demonstration 3

- Skill: `12382c62-0cd1-4bf2-bdc8-1d20bf9b2371.skill-02`
- Intent: Set the line chart title to 'Daily Net Delivery Trend'.
- Efficiency: After creating the line chart, edit its title through the chart title/element controls rather than rebuilding the chart.
- Visible success: The displayed line chart visibly shows the exact title 'Daily Net Delivery Trend'.

#### Demonstration 4

- Skill: `347ef137-7eeb-4c80-a3bb-0951f26a8aff.skill-02`
- Intent: Move the completed chart into the empty area to the right of the daily readings table.
- Efficiency: Drag the chart by its outer object boundary or top edge, not by an individual plotted series.
- Visible success: The titled chart is visibly positioned in the open right-side worksheet area and does not obscure the source table.

Recording start: The active Daily Readings sheet contains the populated input table, only the two seed formulas in row 2, and no chart.

Recording end: Both calculation columns are fully populated through the last reading, and a titled line chart of net delivery is visibly placed to the right of the table.

Allowed variation: The expert may create the chart before or after completing the calculations, use an equivalent line-chart creation path, and place the finished chart anywhere clearly to the right of the source table without covering headers or data.

### 中文详细参考方案

> 以下是一个可以参考的操作 guide。标注者可以根据实际 LibreOffice 界面采用等价操作。

本指南完成每日净交付量与目标差异的计算，并在“Daily Readings”工作表右侧创建和整理一张按日期显示净交付量的折线图。先利用现有的种子公式快速填满两列，再以 Reading Date 和 Net Delivered kWh 创建图表、设置标题并移动到右侧空白区域。

#### 启动后的初始状态检查

- 确认当前打开的工作簿标题为“Solar Microgrid Review”，且活动工作表标签为“Daily Readings”。
- 确认第 1 行有 Reading Date、Generated kWh、Exported kWh、Target kWh、Net Delivered kWh、Variance to Target kWh 等表头，A:D 列从第 2 行至第 25 行连续有数据。
- 确认 E2 已有公式 `=B2-C2` 而 E3:E25 为空；F2 已有公式 `=E2-D2` 而 F3:F25 为空。
- 确认 H 列附近及其右侧有空白工作表区域，并且当前尚未插入图表。

#### 第 1 步：向下填充 Net Delivered kWh 公式

1. 单击单元格 E2，使其成为当前选中单元格；可在输入栏确认其中是公式 `=B2-C2`。
2. 将鼠标移到 E2 选区右下角的小方块（填充柄）。当指针显示为可填充状态时，双击该小方块。
3. 如需确认公式引用已随行号变化，可单击例如 E3，并在输入栏查看类似 `=B3-C3` 的公式。

- 对应 skills：`4172ea6e-6b77-4edb-a9cc-c0014bd1603b.skill-02`
- 高效操作：填充柄双击会依据相邻的连续数据自动判断终止行，比拖动到第 25 行更快，也不容易少填或多填。
- 完成标志：E2 到 E25 都显示数值，没有空白单元格；每行的净交付量均以本行的 Generated kWh 减去 Exported kWh 得出。

#### 第 2 步：向下填充 Variance to Target kWh 公式

1. 单击 F2，并确认该单元格包含种子公式 `=E2-D2`。
2. 将鼠标移到 F2 右下角的填充柄，然后双击它。
3. 任选 F3 或更靠后的一个已填充单元格查看输入栏，确认公式已变为相应行号的引用，例如 `=E3-D3`。

- 对应 skills：`7efeb4b1-3d19-4762-b163-63328d66303b.skill-02`
- 高效操作：同样使用双击填充柄，让 Calc 沿着连续的读取记录自动填充，不必手动复制 24 行。
- 完成标志：F2 到 F25 都显示差异数值且没有空白；每一行使用该行的 Net Delivered kWh 与 Target kWh 计算。

#### 第 3 步：创建按日期显示净交付量的折线图

1. 选中日期区域 A1:A25。
2. 按住 Ctrl 键不放，再选中 E1:E25；现在应同时选中 Reading Date 和 Net Delivered kWh 两个区域，其中第 1 行的单元格会作为标签。
3. 选择“插入”>“图表”。在图表向导中选择“折线图”类型。
4. 在数据范围或预览中确认只有一个数据系列，系列名称为 `Net Delivered kWh`，类别轴使用 `Reading Date`。如向导提供标签选项，勾选“第一行作为标签”和“第一列作为标签”。
5. 完成图表向导，将图表插入当前“Daily Readings”工作表。

- 对应 skills：无；这是准备或检查步骤。
- 高效操作：先选择不相邻的两列，可避免把 Generated、Exported 和 Target 等不需要的列误加入图表。
- 完成标志：工作表中出现一张折线图，图中只有 Net Delivered kWh 的折线，横轴标签来自 Reading Date。

#### 第 4 步：设置图表标题

1. 双击新建的图表，进入图表编辑状态。
2. 如果右侧边栏未显示，使用“视图”>“侧边栏”将其显示出来，然后打开图表的“图表元素”控制。
3. 启用或选择图表标题元素，单击出现的标题文本框。
4. 输入 `Daily Net Delivery Trend`，然后按 Enter 应用。
5. 单击图表外的工作表空白处，退出标题文字编辑。

- 对应 skills：`12382c62-0cd1-4bf2-bdc8-1d20bf9b2371.skill-02`
- 高效操作：通过图表的标题元素直接修改文字，比重新打开完整图表向导更快，并能保留已设置的数据范围和折线类型。
- 完成标志：折线图上方或标题位置清晰显示完全一致的文字 `Daily Net Delivery Trend`。

#### 第 5 步：将完成的图表移动到数据表右侧

1. 单击图表一次以选中整个图表对象；如果仍处于图表内部编辑状态，先单击图表外部空白处，再单击图表的外框。
2. 将指针放到图表对象的顶部边缘或外部边框上，避免点到折线、坐标轴或标题文字。
3. 按住鼠标左键，将整张图表拖到数据表右侧、约从 H 列开始的空白区域，然后释放鼠标。
4. 如右侧区域暂时看不全，可用底部水平滚动条检查图表位置；确认图表没有覆盖 A:F 列的数据或表头。

- 对应 skills：`347ef137-7eeb-4c80-a3bb-0951f26a8aff.skill-02`
- 高效操作：拖动图表对象的外框或顶部边缘即可改变位置，无需重新创建图表；只在需要检查右侧位置时再使用水平滚动条。
- 完成标志：带有标题的图表位于日读数表右边的开放区域，源数据表仍完整可见。

#### 最终结果检查

- 在“Daily Readings”工作表中，E2:E25 均有计算结果，且任意数据行的公式遵循“Generated kWh - Exported kWh”的逻辑；例如 E2 为 `=B2-C2`。
- F2:F25 均有计算结果，且任意数据行的公式遵循“Net Delivered kWh - Target kWh”的逻辑；例如 F2 为 `=E2-D2`。
- “Net Delivered kWh”和“Variance to Target kWh”两列的数值以两位小数显示。
- 工作表上有且有一个折线图；横轴使用 Reading Date，绘制的数据系列为 Net Delivered kWh。
- 图表可见的标题精确为 `Daily Net Delivery Trend`，并且图表位于数据表右侧的空白区域，没有遮挡 A:F 列的表头或读数。

## Source-task similarity review

| Measure | Maximum | Most similar source task |
| --- | ---: | --- |
| Lexical sequence similarity | 0.37561 | 3a7c8185-25c1-4941-bd7b-96e823c9f21f |
| Semantic cosine similarity | 0.49437 | 0326d92d-d218-48a8-9ca1-981cd6d064c7 |

Similarity scores are reviewer aids, not automatic acceptance thresholds. Inspect the contributing source tasks and their complete ordered actions below.

### Source task `12382c62-0cd1-4bf2-bdc8-1d20bf9b2371`

Original instruction:

> Create a clustered column chart showing the Sales and COGS data for each week in a new sheet. Set the chart title as "Sales & COGS".

Required skills derived from this source task:

- **Set a chart title using chart elements** — `12382c62-0cd1-4bf2-bdc8-1d20bf9b2371.skill-02`

Complete ordered single-action sequence:

| Action | Related required skill | Original single action |
| ---: | --- | --- |
| 0 |  | <code>`HOTKEY` ctrl-A</code> |
| 1 |  | <code>`CLICK` insert chart icon</code> |
| 2 | <strong>★ Set a chart title using chart elements</strong><br><code>12382c62-0cd1-4bf2-bdc8-1d20bf9b2371.skill-02</code> | <strong><code>`CLICK` chart elements on right sidebar</code></strong> |
| 3 | <strong>★ Set a chart title using chart elements</strong><br><code>12382c62-0cd1-4bf2-bdc8-1d20bf9b2371.skill-02</code> | <strong><code>`CLICK` title text box</code></strong> |
| 4 | <strong>★ Set a chart title using chart elements</strong><br><code>12382c62-0cd1-4bf2-bdc8-1d20bf9b2371.skill-02</code> | <strong><code>`TYPING` &#x27;Sales &amp; COGS&#x27;</code></strong> |
| 5 | <strong>★ Set a chart title using chart elements</strong><br><code>12382c62-0cd1-4bf2-bdc8-1d20bf9b2371.skill-02</code> | <strong><code>`PRESS` enter</code></strong> |
| 6 |  | <code>`CLICK` on cell A1 to cancel out of current menu</code> |
| 7 |  | <code>`CLICK` on chart to select it</code> |
| 8 |  | <code>`HOTKEY` ctrl-X</code> |
| 9 |  | <code>`CLICK` on + to left of sheet1</code> |
| 10 |  | <code>`HOTKEY` ctrl+v</code> |

### Source task `347ef137-7eeb-4c80-a3bb-0951f26a8aff`

Original instruction:

> Here are two tables recording the per-month costs in 2019 and 2020. I want to create two column bar charts reflecting per-month total costs for each year from these data. Help me, Mr. Assistant!

Required skills derived from this source task:

- **Reposition a chart object by dragging** — `347ef137-7eeb-4c80-a3bb-0951f26a8aff.skill-02`

Complete ordered single-action sequence:

| Action | Related required skill | Original single action |
| ---: | --- | --- |
| 0 |  | <code>`CLICK` to expand window top right corner</code> |
| 1 |  | <code>`CLICK` A3</code> |
| 2 |  | <code>`KEY_DOWN` Shift</code> |
| 3 |  | <code>`CLICK` A14</code> |
| 4 |  | <code>`KEY_UP` Shift</code> |
| 5 |  | <code>`KEY_DOWN` Ctrl</code> |
| 6 |  | <code>`CLICK` I3</code> |
| 7 |  | <code>`KEY_UP` Ctrl</code> |
| 8 |  | <code>`KEY_DOWN` Shift</code> |
| 9 |  | <code>`CLICK` I14</code> |
| 10 |  | <code>`KEY_UP` Shift</code> |
| 11 |  | <code>`CLICK` Insert chart icon</code> |
| 12 |  | <code>`PRESS` enter</code> |
| 13 | <strong>★ Reposition a chart object by dragging</strong><br><code>347ef137-7eeb-4c80-a3bb-0951f26a8aff.skill-02</code> | <strong><code>`MOVE_TO` top edge of chart</code></strong> |
| 14 | <strong>★ Reposition a chart object by dragging</strong><br><code>347ef137-7eeb-4c80-a3bb-0951f26a8aff.skill-02</code> | <strong><code>`DRAG_TO` right edge of page</code></strong> |
| 15 | <strong>★ Reposition a chart object by dragging</strong><br><code>347ef137-7eeb-4c80-a3bb-0951f26a8aff.skill-02</code> | <strong><code>`SCROLL_LEFT`</code></strong> |
| 16 |  | <code>`CLICK` A20</code> |
| 17 |  | <code>`KEY_DOWN` Shift</code> |
| 18 |  | <code>`CLICK` A31</code> |
| 19 |  | <code>`KEY_UP` Shift</code> |
| 20 |  | <code>`KEY_DOWN` Ctrl</code> |
| 21 |  | <code>`CLICK` I20</code> |
| 22 |  | <code>`KEY_UP` Ctrl</code> |
| 23 |  | <code>`KEY_DOWN` Shift</code> |
| 24 |  | <code>`CLICK` I31</code> |
| 25 |  | <code>`KEY_UP` Shift</code> |
| 26 |  | <code>`CLICK` Insert chart icon</code> |
| 27 |  | <code>`PRESS` enter</code> |

### Source task `4172ea6e-6b77-4edb-a9cc-c0014bd1603b`

Original instruction:

> I want to work out the maturity date for all the loans. Please do it for me in a new column with header "Maturity Date".

Required skills derived from this source task:

- **Autofill a formula down a contiguous column** — `4172ea6e-6b77-4edb-a9cc-c0014bd1603b.skill-02`

Complete ordered single-action sequence:

| Action | Related required skill | Original single action |
| ---: | --- | --- |
| 0 |  | <code>`CLICK` cell C1</code> |
| 1 |  | <code>`TYPING` &#x27;Maturity Date&#x27;</code> |
| 2 |  | <code>`PRESS` enter</code> |
| 3 |  | <code>`TYPING` &#x27;=A2+B2&#x27;</code> |
| 4 |  | <code>`PRESS` enter</code> |
| 5 | <strong>★ Autofill a formula down a contiguous column</strong><br><code>4172ea6e-6b77-4edb-a9cc-c0014bd1603b.skill-02</code> | <strong><code>`CLICK` cell C2`</code></strong> |
| 6 | <strong>★ Autofill a formula down a contiguous column</strong><br><code>4172ea6e-6b77-4edb-a9cc-c0014bd1603b.skill-02</code> | <strong><code>`DOUBLE_CLICK` bottom right corner of the cell C2`</code></strong> |

### Source task `7efeb4b1-3d19-4762-b163-63328d66303b`

Original instruction:

> Fill the Sequence Numbers as "No. #" in the "Seq No." column

Required skills derived from this source task:

- **Autofill a formula down a contiguous data range** — `7efeb4b1-3d19-4762-b163-63328d66303b.skill-02`

Complete ordered single-action sequence:

| Action | Related required skill | Original single action |
| ---: | --- | --- |
| 0 |  | <code>`CLICK` B2</code> |
| 1 |  | <code>`TYPING` =&quot;No. &quot; &amp; ROW(B2)-1 </code> |
| 2 |  | <code>`PRESS` Enter.</code> |
| 3 | <strong>★ Autofill a formula down a contiguous data range</strong><br><code>7efeb4b1-3d19-4762-b163-63328d66303b.skill-02</code> | <strong><code>`CLICK` B2</code></strong> |
| 4 | <strong>★ Autofill a formula down a contiguous data range</strong><br><code>7efeb4b1-3d19-4762-b163-63328d66303b.skill-02</code> | <strong><code>`DOUBLE_CLICK` bottom right corner of cell</code></strong> |

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
