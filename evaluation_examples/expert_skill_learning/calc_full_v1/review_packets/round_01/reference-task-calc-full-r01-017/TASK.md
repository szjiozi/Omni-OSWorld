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

本指南将在 `Daily Readings` 中把两列已有的种子公式自动填充到全部 24 条日读数，然后以 Reading Date 和 Net Delivered kWh 创建折线图，设置标题，并将图表移到表格右侧。

#### 启动后的初始状态检查

- 确认当前活动工作表标签是 `Daily Readings`，并且 A1:F25 是连续的数据表。
- 确认 E1 为 `Net Delivered kWh`、F1 为 `Variance to Target kWh`；E2 和 F2 已有公式，而 E3:E25 与 F3:F25 仍为空。
- 确认右侧约从 H 列开始有空白区域，且工作表中尚未出现图表对象。

#### 第 1 步：确认 Net Delivered 的种子公式

1. 选择单元格 E2，查看公式输入行，确认该单元格使用公式 `=B2-C2`。
2. 确认相邻的输入记录从第 2 行连续延续到第 25 行，且 E3:E25 尚未填入结果。

- 对应 skills：无；这是准备或检查步骤。
- 高效操作：先确认种子公式和数据边界，可以避免把填充柄应用到错误的列或错误的范围。
- 完成标志：E2 显示一个数值结果，公式栏显示 `=B2-C2`，而 E3:E25 为空。

#### 第 2 步：自动填充 Net Delivered kWh

1. 保持选中 E2，将指针移到选中框右下角的小方块（填充柄）。
2. 双击填充柄。Calc 会沿着连续的日读数将公式填充到最后一条记录。
3. 选择 E25，查看公式栏中的相对引用是否已变为 `=B25-C25`。

- 对应 skills：`4172ea6e-6b77-4edb-a9cc-c0014bd1603b.skill-02`
- 高效操作：双击填充柄比手动向下拖过 24 行更快，且会按照相邻连续数据自动停止。
- 完成标志：E2:E25 全部显示计算结果且没有空白；E25 的公式为 `=B25-C25`。

#### 第 3 步：自动填充 Variance to Target kWh

1. 选择 F2，确认公式栏显示 `=E2-D2`。
2. 将指针移到 F2 右下角的填充柄并双击。
3. 选择 F25，确认公式栏中的公式已按行调整为 `=E25-D25`。

- 对应 skills：`7efeb4b1-3d19-4762-b163-63328d66303b.skill-02`
- 高效操作：对 F2 同样双击填充柄，能够让目标差异公式恰好延伸到连续表格的最后一行。
- 完成标志：F2:F25 都有数值结果且没有空白；F25 的公式为 `=E25-D25`。

#### 第 4 步：创建 Net Delivered 的折线图

1. 先选择 A1:A25；按住 Ctrl 后再选择 E1:E25，使 Reading Date 与 Net Delivered kWh 同时作为图表数据源。
2. 打开 `Insert` > `Chart...`，在图表类型中选择折线图，然后完成创建并将图表保留在 `Daily Readings` 工作表上。
3. 观察完成的图表：横轴应显示 Reading Date 的日期类别，图中应只有一条 Net Delivered kWh 数值线。若已经如此显示，无需调整。
4. 如果横轴显示的是数值而不是日期，或曲线不是 E 列的净交付数据，双击图表进入编辑状态，打开 `Format` > `Data Ranges`。在 `Data Series` 中把 `Categories` 改为 `Daily Readings.$A$2:$A$25`，并将该数据系列的 `Y-Values` 改为 `Daily Readings.$E$2:$E$25`，然后确认。

- 对应 skills：无；这是准备或检查步骤。
- 高效操作：只选择日期列和净交付列，能避免把 Generated、Exported、Target 等不需要的列误加入图表。
- 完成标志：工作表中出现一张折线图，日期用于横轴类别，图中显示 Net Delivered kWh 的一条折线。

#### 第 5 步：设置图表标题

1. 单击图表使其成为当前对象，并打开右侧边栏中的 `Chart Elements` 控制。
2. 启用或选择图表标题元素，然后单击出现的标题文本框。
3. 输入 `Daily Net Delivery Trend`，按 Enter 应用。
4. 如果图表中已经显示该精确标题，无需再次修改；如果标题文字仍是默认文本或没有显示，重新选择标题元素，并在标题文本框中用 `Daily Net Delivery Trend` 替换全部文字后按 Enter。

- 对应 skills：`12382c62-0cd1-4bf2-bdc8-1d20bf9b2371.skill-02`
- 高效操作：直接使用图表元素中的标题编辑功能，不必重新运行图表创建流程。
- 完成标志：折线图上方或图内的标题区域清晰显示 `Daily Net Delivery Trend`。

#### 第 6 步：将图表移到表格右侧

1. 单击图表的外部边框或上边缘，直到整个图表对象被选中。
2. 拖动整个图表到数据表右侧的空白区域，目标是靠近 E2 右方、约 H 列起的区域，同时让 A:F 的源数据保持可见。
3. 如果图表创建后已经位于右侧空白区域且没有遮住源表，无需调整位置。若它遮住了标题或任一源数据单元格，重新选中图表外框并将其整体向右拖动；必要时可水平滚动以查看目标区域。

- 对应 skills：`347ef137-7eeb-4c80-a3bb-0951f26a8aff.skill-02`
- 高效操作：拖动图表外框或上边缘会移动整个对象；不要拖动折线本身，以免只选中数据系列。
- 完成标志：带有 `Daily Net Delivery Trend` 标题的图表完整位于表格右侧空白区，A:F 数据表未被遮挡。

#### 第 7 步：完成最终核对

1. 依次查看 E25 和 F25 的公式栏，确认分别为 `=B25-C25` 和 `=E25-D25`。
2. 确认 E2:E25 和 F2:F25 均无空白，并保持两位小数的数值显示。
3. 确认图表标题为 `Daily Net Delivery Trend`，横轴为日期，只有净交付的折线，且图表在右侧空白区域。

- 对应 skills：无；这是准备或检查步骤。
- 高效操作：末行公式抽查加上图表外观检查，能快速确认自动填充、系列选择和版面位置都正确。
- 完成标志：计算列完整、图表内容正确且标题和位置均满足要求。

#### 最终结果检查

- `Daily Readings` 工作表中，输入数据 A:D 未被改动，且 E2:E25 与 F2:F25 均已填满并显示两位小数的计算结果。
- 抽查最后一行：选择 E25 时，公式栏应为 `=B25-C25`；选择 F25 时，公式栏应为 `=E25-D25`。
- 工作表上只有一个折线图；横轴类别是 Reading Date，绘制的数据是 Net Delivered kWh。
- 图中可见精确标题 `Daily Net Delivery Trend`，并且整个图表位于数据表右侧的空白区域，没有遮住 A:F 的标题或数据。

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
