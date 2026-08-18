# Coastal Lab Dispatch Completion

- Reference task: `reference-task-calc-full-r01-012`
- Application: `libreoffice_calc`
- Review decision: `pending`

## Task instruction

Complete the Coastal Lab Dispatch Log by calculating the daily completion rate as verified kits divided by planned kits for every dispatch date, then add a lines-only line chart that shows how the completion rate changes across the dates.

## Required skills

### 1. Insert a lines-only line chart from selected spreadsheet data

Skill ID: `0a2e43bf-b26c-4631-a966-af9dfa12c9e5.skill-04`

Procedure:

1. With the intended data range selected, click the chart insertion icon to open chart creation.
2. Choose the Line chart type, then select the lines-only variant (the option without point markers, shown as the third icon from the right in this interface).
3. Click Finish to insert the chart using the current selection.

Efficiency tip: Choose the chart family and variant before finishing, so the chart is created correctly without needing to reopen its type settings afterward.

Source task: `0a2e43bf-b26c-4631-a966-af9dfa12c9e5`

Source instruction: Work out the monthly total sales in a new row called "Total" and then create a line chart to show the results (x-axis be Months).

Directly referenced source actions:

- Action 16: <code>`CLICK` chart icon</code>
- Action 17: <code>`CLICK` Line</code>
- Action 18: <code>`CLICK` icon representing lines only (3rd from the right)</code>
- Action 19: <code>`CLICK` Finish</code>

### 2. Autofill a formula down an adjacent data region

Skill ID: `51719eea-10bc-4246-a428-ac7c433dd4b3.skill-02`

Procedure:

1. Select the cell containing the completed formula, such as `G2`.
2. Move to the small fill handle at the cell's bottom-right corner.
3. Double-click the fill handle. Calc copies the formula downward to match the contiguous neighboring rows, adjusting relative references for each destination row.

Efficiency tip: Double-clicking the fill handle is faster and less error-prone than manually dragging it through a long adjacent data region.

Source task: `51719eea-10bc-4246-a428-ac7c433dd4b3`

Source instruction: Calculate revenue in a new column according to the Retail Price sheet (consider product price and quantity and discount), and generate a Pivot Table in a new sheet (Sheet2) that summarizes the revenue of each product.

Directly referenced source actions:

- Action 7: <code>`CLICK` cell G2</code>
- Action 8: <code>`MOVE_TO` bottom right corner of the cell G2`</code>
- Action 9: <code>`DOUBLE_CLICK`</code>

### 3. Create a row-wise division formula with relative references

Skill ID: `21ab7b40-77c2-4ae6-8321-e00d3a086c73.skill-01`

Procedure:

1. Select the first result cell in the output column and type a division formula using relative references.
2. For example, enter `=A2/B2` in the first result row and press Enter. When copied to later rows, Calc changes it to `=A3/B3`, `=A4/B4`, and so on.

Efficiency tip: Enter the formula once with relative references, then use an autofill technique instead of manually rewriting it for each row.

Source task: `21ab7b40-77c2-4ae6-8321-e00d3a086c73`

Source instruction: Please calculate the period rate for my data in a new column with header "Period Rate (%)", convert the results as number type, and highlight the highest result with green (#00ff00) font.

Directly referenced source actions:

- Action 3: <code>`TYPING` &#x27;=A2/B2&#x27;</code>
- Action 4: <code>`PRESS` enter</code>

## Initial state preview

### Dispatch Log

![Dispatch_Log.png](artifact/previews/Dispatch_Log.png)

## Operator guide

### Existing operation-intent guide

#### Demonstration 1

- Skill: `21ab7b40-77c2-4ae6-8321-e00d3a086c73.skill-01`
- Intent: In the first blank Completion Rate cell, calculate each day's verified-kit share of its planned-kit count with a relative-reference division formula.
- Efficiency: Enter the calculation once using row-relative references; it will then adapt correctly for all later dates when filled.
- Visible success: B2 displays a percentage consistent with Verified Kits divided by Planned Kits for row 2.

#### Demonstration 2

- Skill: `51719eea-10bc-4246-a428-ac7c433dd4b3.skill-02`
- Intent: Extend the first Completion Rate formula through every remaining dispatch record.
- Efficiency: Use the fill handle on the completed first formula to populate the contiguous records rather than retyping formulas.
- Visible success: B2:B25 are populated, and formulas in later rows reference the corresponding Planned Kits and Verified Kits cells.

#### Demonstration 3

- Skill: `0a2e43bf-b26c-4631-a966-af9dfa12c9e5.skill-04`
- Intent: Create a line-only chart of the completed daily completion-rate trend from the selected Dispatch Date and Completion Rate data.
- Efficiency: Choose the Line chart family and its no-marker, lines-only variant before finishing chart creation.
- Visible success: A chart is visible with dates as categories and one connected Completion Rate line that has no point markers.

Recording start: The Dispatch Log sheet is active with the source table present, the Completion Rate cells blank, and no chart in the workbook.

Recording end: The Dispatch Log sheet retains all 24 records, B2:B25 show calculated percentage completion rates, and a readable lines-only line chart displays the daily rate trend.

Allowed variation: The operator may use keyboard entry, the formula bar, a fill-handle double-click, or an equivalent Calc autofill method. The chart may be positioned anywhere on the Dispatch Log sheet, provided it visibly uses Dispatch Date as the category axis and Completion Rate as the sole plotted series.

### 中文详细参考方案

> 以下是一个可以参考的操作 guide。标注者可以根据实际 LibreOffice 界面采用等价操作。

本任务将在 `Dispatch Log` 中计算每个派送日期的完成率：用 `Verified Kits` 除以 `Planned Kits`，再利用日期和完成率创建一张无数据点标记的折线图，以查看每日完成率的变化趋势。

#### 启动后的初始状态检查

- 确认当前活动工作表是 `Dispatch Log`。
- 确认第 1 行是标题行，数据位于第 2 行至第 25 行；`B2:B25` 的 Completion Rate 目前为空。
- 确认 C 列 `Planned Kits` 与 D 列 `Verified Kits` 每一行都有数值，且工作簿中尚未存在图表。

#### 第 1 步：在首行计算完成率

1. 单击单元格 `B2`，它是第一条记录的 Completion Rate 结果位置。
2. 输入公式 `=D2/C2`，然后按 `Enter`。其中 D 列是 `Verified Kits`，C 列是 `Planned Kits`。
3. 保留现有百分比格式，不要把结果改成普通数字格式。

- 对应 skills：`21ab7b40-77c2-4ae6-8321-e00d3a086c73.skill-01`
- 高效操作：先只在首个结果单元格写一次采用相对引用的公式；后续行可自动调整引用，无需逐行计算。
- 完成标志：`B2` 显示一个带一位小数的百分比，且其数值与第 2 行的 `Verified Kits ÷ Planned Kits` 相符。

#### 第 2 步：向下填充所有完成率公式

1. 重新选中 `B2`。
2. 将指针移到选中单元格右下角的小方块，即填充柄。
3. 当指针位于填充柄上时双击。Calc 会依据相邻 C、D 列连续的数据，将公式填充到其余记录行。

- 对应 skills：`51719eea-10bc-4246-a428-ac7c433dd4b3.skill-02`
- 高效操作：对已完成公式的填充柄双击，比拖动到第 25 行更快，也可减少选择错行的风险。
- 完成标志：`B2:B25` 都已填入百分比。单击例如 `B3` 时，编辑栏中的公式应为与该行对应的 `=D3/C3`，而不是仍引用第 2 行。

#### 第 3 步：选择图表数据源

1. 选择包含标题的范围 `A1:B25`。A 列 `Dispatch Date` 将作为横轴类别，B 列 `Completion Rate` 将作为唯一的数据系列。
2. 确认选择范围包含 24 条数据及第 1 行标题，并且 B 列中的计算结果均已显示。

- 对应 skills：无；这是准备或检查步骤。
- 高效操作：图表源区域只选择日期和完成率两列，可避免把计划数量或核验数量误绘制为额外数据线。
- 完成标志：选区覆盖 `Dispatch Date` 和 `Completion Rate` 两个标题，以及从第 2 行到第 25 行的对应数据。

#### 第 4 步：插入无标记折线图

1. 在保持 `A1:B25` 被选中的状态下，点击插入图表的图标以打开图表创建界面。
2. 在图表类型中选择 `Line`。
3. 选择仅显示线条、没有点标记的变体；在此界面中它显示为从右侧数第三个图标。
4. 点击 `Finish` 插入图表。

- 对应 skills：`0a2e43bf-b26c-4631-a966-af9dfa12c9e5.skill-04`
- 高效操作：在完成创建前就选定 `Line` 及无标记的变体，可避免创建后再返回修改图表类型。
- 完成标志：`Dispatch Log` 上出现图表，图中只有一条连续的 Completion Rate 线，没有圆点或其他数据点标记，日期显示为横轴类别。

#### 第 5 步：检查图表和最终结果

1. 检查图表是否清楚显示日期顺序和完成率的上下变化。
2. 如有需要，将图表移动或调整为不会遮挡 `A1:D25` 数据表的可读大小。
3. 抽查图表仅有一个 Completion Rate 系列；不要加入 `Planned Kits` 或 `Verified Kits` 系列。

- 对应 skills：无；这是准备或检查步骤。
- 高效操作：如图表覆盖了表格或文字过小，可拖动图表到空白区域并调整大小，以便同时检查数据表和趋势线。
- 完成标志：数据表与图表可同时辨认：`B2:B25` 为完成率百分比，图表显示 24 个日期对应的一条无标记完成率趋势线。

#### 最终结果检查

- `Dispatch Log` 工作表仍保留 24 条日期连续的派送记录，原始的 `Planned Kits` 和 `Verified Kits` 数据没有被改动。
- `B2:B25` 均显示为一位小数的百分比；抽查任意一行时，该行的 Completion Rate 等于 `Verified Kits ÷ Planned Kits`。
- 工作表中有一个清晰可读的折线图：横轴为 Dispatch Date，只有一条 Completion Rate 数据线，并且线条上没有数据点标记。

## Source-task similarity review

| Measure | Maximum | Most similar source task |
| --- | ---: | --- |
| Lexical sequence similarity | 0.376022 | 0a2e43bf-b26c-4631-a966-af9dfa12c9e5 |
| Semantic cosine similarity | 0.355283 | 3a7c8185-25c1-4941-bd7b-96e823c9f21f |

Similarity scores are reviewer aids, not automatic acceptance thresholds. Inspect the contributing source tasks and their complete ordered actions below.

### Source task `0a2e43bf-b26c-4631-a966-af9dfa12c9e5`

Original instruction:

> Work out the monthly total sales in a new row called "Total" and then create a line chart to show the results (x-axis be Months).

Required skills derived from this source task:

- **Insert a lines-only line chart from selected spreadsheet data** — `0a2e43bf-b26c-4631-a966-af9dfa12c9e5.skill-04`

Complete ordered single-action sequence:

| Action | Related required skill | Original single action |
| ---: | --- | --- |
| 0 |  | <code>`CLICK` on cell A12</code> |
| 1 |  | <code>`TYPING` &#x27;Total&#x27;</code> |
| 2 |  | <code>`PRESS` tab</code> |
| 3 |  | <code>`TYPING` &#x27;=SUM(B2:B11)&#x27;</code> |
| 4 |  | <code>`PRESS` enter</code> |
| 5 |  | <code>`CLICK` cell B12</code> |
| 6 |  | <code>`MOVE_TO bottom right corner of the cell B12`</code> |
| 7 |  | <code>`DRAG_TO` bottom right corner of the cell G12</code> |
| 8 |  | <code>`MOVE_TO` middle of cell A1</code> |
| 9 |  | <code>`DRAG_TO` middle of cell G1</code> |
| 10 |  | <code>`KEY_DOWN` ctrl</code> |
| 11 |  | <code>`CLICK` cell A12</code> |
| 12 |  | <code>`KEY_UP` ctrl</code> |
| 13 |  | <code>`KEY_DOWN` shift</code> |
| 14 |  | <code>`CLICK` cell G12</code> |
| 15 |  | <code>`KEY_UP` shift</code> |
| 16 | <strong>★ Insert a lines-only line chart from selected spreadsheet data</strong><br><code>0a2e43bf-b26c-4631-a966-af9dfa12c9e5.skill-04</code> | <strong><code>`CLICK` chart icon</code></strong> |
| 17 | <strong>★ Insert a lines-only line chart from selected spreadsheet data</strong><br><code>0a2e43bf-b26c-4631-a966-af9dfa12c9e5.skill-04</code> | <strong><code>`CLICK` Line</code></strong> |
| 18 | <strong>★ Insert a lines-only line chart from selected spreadsheet data</strong><br><code>0a2e43bf-b26c-4631-a966-af9dfa12c9e5.skill-04</code> | <strong><code>`CLICK` icon representing lines only (3rd from the right)</code></strong> |
| 19 | <strong>★ Insert a lines-only line chart from selected spreadsheet data</strong><br><code>0a2e43bf-b26c-4631-a966-af9dfa12c9e5.skill-04</code> | <strong><code>`CLICK` Finish</code></strong> |

### Source task `21ab7b40-77c2-4ae6-8321-e00d3a086c73`

Original instruction:

> Please calculate the period rate for my data in a new column with header "Period Rate (%)", convert the results as number type, and highlight the highest result with green (#00ff00) font.

Required skills derived from this source task:

- **Create a row-wise division formula with relative references** — `21ab7b40-77c2-4ae6-8321-e00d3a086c73.skill-01`

Complete ordered single-action sequence:

| Action | Related required skill | Original single action |
| ---: | --- | --- |
| 0 |  | <code>`CLICK` on cell C1</code> |
| 1 |  | <code>`TYPING` &#x27;Period Rate (%)&#x27;</code> |
| 2 |  | <code>`PRESS` enter</code> |
| 3 | <strong>★ Create a row-wise division formula with relative references</strong><br><code>21ab7b40-77c2-4ae6-8321-e00d3a086c73.skill-01</code> | <strong><code>`TYPING` &#x27;=A2/B2&#x27;</code></strong> |
| 4 | <strong>★ Create a row-wise division formula with relative references</strong><br><code>21ab7b40-77c2-4ae6-8321-e00d3a086c73.skill-01</code> | <strong><code>`PRESS` enter</code></strong> |
| 5 |  | <code>`CLICK` cell C2</code> |
| 6 |  | <code>`DOUBLE_CLICK` bottom right corner of the cell C2</code> |
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

### Source task `51719eea-10bc-4246-a428-ac7c433dd4b3`

Original instruction:

> Calculate revenue in a new column according to the Retail Price sheet (consider product price and quantity and discount), and generate a Pivot Table in a new sheet (Sheet2) that summarizes the revenue of each product.

Required skills derived from this source task:

- **Autofill a formula down an adjacent data region** — `51719eea-10bc-4246-a428-ac7c433dd4b3.skill-02`

Complete ordered single-action sequence:

| Action | Related required skill | Original single action |
| ---: | --- | --- |
| 0 |  | <code>`CLICK` cell G1</code> |
| 1 |  | <code>`TYPING` &#x27;Revenue&#x27;</code> |
| 2 |  | <code>`PRESS` enter</code> |
| 3 |  | <code>`CLICK` sheet &#x27;Retail Price&#x27;</code> |
| 4 |  | <code>`CLICK` sheet &#x27;Sheet1&#x27;</code> |
| 5 |  | <code>`TYPING` &#x27;=VLOOKUP(C2,$&#x27;Retail Price&#x27;.$A$2:$B$23,2,FALSE())*E2*(1-F2)&#x27;</code> |
| 6 |  | <code>`PRESS` enter</code> |
| 7 | <strong>★ Autofill a formula down an adjacent data region</strong><br><code>51719eea-10bc-4246-a428-ac7c433dd4b3.skill-02</code> | <strong><code>`CLICK` cell G2</code></strong> |
| 8 | <strong>★ Autofill a formula down an adjacent data region</strong><br><code>51719eea-10bc-4246-a428-ac7c433dd4b3.skill-02</code> | <strong><code>`MOVE_TO` bottom right corner of the cell G2`</code></strong> |
| 9 | <strong>★ Autofill a formula down an adjacent data region</strong><br><code>51719eea-10bc-4246-a428-ac7c433dd4b3.skill-02</code> | <strong><code>`DOUBLE_CLICK`</code></strong> |
| 10 |  | <code>`HOTKEY` ctrl-A</code> |
| 11 |  | <code>`CLICK` pivot table icon</code> |
| 12 |  | <code>`PRESS` enter</code> |
| 13 |  | <code>`MOVE_TO` product in available fields box</code> |
| 14 |  | <code>`DRAG_TO` row fields box</code> |
| 15 |  | <code>`MOVE_TO` revenue in available fields box</code> |
| 16 |  | <code>`DRAG_TO` data fields box</code> |
| 17 |  | <code>`CLICK` ok</code> |
| 18 |  | <code>`DOUBLE_CLICK` Pivot Table Sheet1_1</code> |
| 19 |  | <code>`TYPING` Sheet2</code> |
| 20 |  | <code>`PRESS` enter</code> |

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
