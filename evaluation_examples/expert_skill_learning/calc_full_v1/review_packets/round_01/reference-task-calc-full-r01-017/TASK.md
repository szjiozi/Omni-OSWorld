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

本任务将在 `Daily Readings` 工作表中把两列已有的起始公式快速填充到所有 24 条每日读数，然后以日期和净交付量创建折线图，设置标题并移到表格右侧。保留 A:D 的原始输入数据不变。

#### 启动后的初始状态检查

- 确认当前打开的工作簿标题为 `Solar Microgrid Review`，活动工作表标签为 `Daily Readings`。
- 确认第 1 行的 E1 为 `Net Delivered kWh`、F1 为 `Variance to Target kWh`；E2 和 F2 已有公式，而 E3:E25、F3:F25 仍为空白。
- 确认 A1:D25 连续包含日期和输入读数，且从大约 H 列开始的右侧区域为空白、尚未有图表对象。

#### 第 1 步：填充净交付量公式

1. 单击 E2。先查看输入行或公式栏，确认该种子公式是 `=B2-C2`。
2. 将指针移到所选单元格 E2 边框右下角的小方块（填充柄）；当指针适合填充时，双击该小方块。
3. 检查 E3:E25 已自动填入结果。可单击 E25，并确认公式栏中的引用已随行号调整为 `=B25-C25`。

- 对应 skills：`4172ea6e-6b77-4edb-a9cc-c0014bd1603b.skill-02`
- 高效操作：双击填充柄会自动依据相邻连续数据区确定终点，比拖动到第 25 行更快，也不必估计最后一行。
- 完成标志：E2:E25 全部显示 Net Delivered kWh 数值，没有空白；末行使用当前行的相对引用。

#### 第 2 步：填充目标差异公式

1. 单击 F2，确认此单元格的种子公式为 `=E2-D2`。
2. 双击 F2 右下角的填充柄，将公式向下扩展。
3. 确认 F3:F25 都出现 Variance to Target kWh 结果。任选末行 F25 检查公式栏，确认其公式为 `=E25-D25`。

- 对应 skills：`7efeb4b1-3d19-4762-b163-63328d66303b.skill-02`
- 高效操作：此列同样使用双击填充柄；连续的相邻表格会使 Calc 自动恰好填充到最后一个读数行。
- 完成标志：F2:F25 均已计算完成且无空白，F 列的每行公式都引用该行 E 列和 D 列。

#### 第 3 步：创建日期净交付量折线图

1. 选择含标题的日期范围 A1:A25；按住 Ctrl 后，再选择含标题的净交付量范围 E1:E25，以便将日期用作类别、净交付量用作唯一数据系列。
2. 打开 `Insert` > `Chart...`。在图表向导中选择 `Line` 图表类型，并确认数据系列使用 `Net Delivered kWh`、类别轴使用 `Reading Date`。保留第一行作为标签的设置。
3. 完成图表向导，将图表插入当前 `Daily Readings` 工作表。此时若图表暂时覆盖表格，下一步会移动它。

- 对应 skills：无；这是准备或检查步骤。
- 高效操作：先只选择日期和净交付量两列，可避免把 Generated、Exported 或 Target 数值误加入同一张图。
- 完成标志：工作表中出现一张折线图；图中按 Reading Date 排列净交付量，且未绘制其他输入列作为额外系列。

#### 第 4 步：设置图表标题

1. 单击图表，然后进入图表编辑状态，使右侧边栏显示图表相关控件。
2. 在右侧边栏打开 `Chart Elements`，启用或选择图表标题元素。
3. 单击出现的标题文本框，输入 `Daily Net Delivery Trend`，然后按 Enter 应用。

- 对应 skills：`12382c62-0cd1-4bf2-bdc8-1d20bf9b2371.skill-02`
- 高效操作：通过右侧的图表元素直接修改标题，不需要重新打开完整的图表创建向导。
- 完成标志：图表上方或指定标题位置清楚显示精确文字 `Daily Net Delivery Trend`。

#### 第 5 步：将完成的图表移到表格右侧

1. 退出图表内部编辑状态（如有需要），单击图表外框或顶部边缘，确保选中的是整个图表对象而不是图中的折线。
2. 从图表的顶部边缘或外侧边框拖动，将整个图表放到数据表右边大约 H 列之后的空白区域。必要时仅做少量水平滚动以检查位置。
3. 调整后确认图表没有覆盖 A:F 列的表头或任何每日读数。

- 对应 skills：`347ef137-7eeb-4c80-a3bb-0951f26a8aff.skill-02`
- 高效操作：拖动图表的外侧边框或顶部边缘即可移动整个对象；不要拖动折线本身，以免只选中数据系列。
- 完成标志：带有 `Daily Net Delivery Trend` 标题的折线图完整位于表格右侧的空白工作表区域，左侧数据表仍清晰可见。

#### 最终结果检查

- 在 `Daily Readings` 中检查 E2:E25：每一行都有两位小数的 Net Delivered kWh 结果，且选中例如 E25 时公式栏显示与该行对应的 `=B25-C25`。
- 检查 F2:F25 没有空白；选中例如 F25 时公式栏显示与该行对应的 `=E25-D25`。
- 图表是折线图，横轴类别来自 `Reading Date`，绘制的数据系列为 `Net Delivered kWh`。
- 图表上可见完全一致的标题 `Daily Net Delivery Trend`，并且图表位于数据表右侧的空白区域，没有遮挡 A:F 列的标题或读数。

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
