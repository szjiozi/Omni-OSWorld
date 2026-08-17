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

在“Dispatch Log”中，先以 Verified Kits ÷ Planned Kits 计算每天的 Completion Rate，再把公式快速填充至全部24条记录，最后用 Dispatch Date 和 Completion Rate 创建无数据点标记的折线图，展示每日完成率变化。

#### 启动后的初始状态检查

- 确认 LibreOffice Calc 已打开工作簿，当前活动工作表名称为“Dispatch Log”。
- 确认第1行显示标题 Dispatch Date、Completion Rate、Planned Kits、Verified Kits，且数据位于第2行至第25行。
- 确认 B2:B25 目前为空白，但该列已经显示为一位小数的百分比格式；C 列和 D 列每一条记录都有数值。
- 确认工作表中尚未存在图表对象。

#### 第 1 步：计算第一天的完成率

1. 单击单元格 B2，这是第一条记录的 Completion Rate 结果位置。
2. 输入公式 `=D2/C2`，其中 D2 是 Verified Kits，C2 是 Planned Kits。
3. 按 Enter 确认公式。由于 B 列已预设为百分比且保留一位小数，结果会自动按百分比显示。

- 对应 skills：`21ab7b40-77c2-4ae6-8321-e00d3a086c73.skill-01`
- 高效操作：先核对列含义再输入公式，可避免把计划数量和已核验数量的除数、被除数写反。
- 完成标志：B2 显示一个一位小数的百分比，而不是空白；其数值与同一行 Verified Kits 除以 Planned Kits 的结果一致。

#### 第 2 步：向下自动填充全部完成率公式

1. 重新选中含有公式的 B2。
2. 将鼠标移到 B2 单元格右下角的小方块（填充柄）。鼠标指针变为适合填充的形状时，双击该填充柄。
3. 确认 Calc 将公式向下复制到与相邻数据区域对应的最后一行，即 B25。
4. 可单击例如 B3 或 B25，在公式栏中检查引用已随行号变化，例如 B3 使用 `=D3/C3`。

- 对应 skills：`51719eea-10bc-4246-a428-ac7c433dd4b3.skill-02`
- 高效操作：使用填充柄双击会自动依据相邻 C、D 列的连续数据向下填充，比逐行输入或长距离拖动更快，也更不容易漏行。
- 完成标志：B2:B25 全部显示百分比结果，且不同日期的结果有变化；后续行公式引用各自所在行的 C 列和 D 列。

#### 第 3 步：创建每日完成率的无标记折线图

1. 选择图表源数据区域 A1:B25，包含 Dispatch Date、Completion Rate 及全部24条数据。
2. 在工具栏中点击插入图表的图标以打开图表创建向导；也可使用菜单“插入”中的图表命令。
3. 在图表类型中选择“折线图”。
4. 在折线图的变体中选择仅显示线条、不带数据点标记的“线条”变体（此界面中为从右侧数第三个图标）。
5. 确认数据范围仍为 A1:B25，且首行作为标签使用；然后点击“完成”插入图表。

- 对应 skills：`0a2e43bf-b26c-4631-a966-af9dfa12c9e5.skill-04`
- 高效操作：一次选中包含标题的两列数据，可让 Calc 自动将 Dispatch Date 识别为类别标签，并将 Completion Rate 识别为唯一的数据系列。
- 完成标志：“Dispatch Log”上出现折线图，横轴按日期显示，图中仅有一条 Completion Rate 折线，并且线条上没有圆点或其他数据点标记。

#### 第 4 步：整理图表并检查结果

1. 查看图表是否完整显示日期趋势和完成率线条。
2. 如图表遮挡了表格，单击图表边框并将其移动或调整为可读的大小，避免覆盖 B2:B25 或源数据标题。
3. 确认图表仍只绘制 Completion Rate，日期仍作为横轴类别。

- 对应 skills：无；这是准备或检查步骤。
- 高效操作：若图表与表格重叠，优先拖动图表边框整体移动到右侧或下方空白处；这样无需改变数据源即可提高可读性。
- 完成标志：源表数据和图表可以同时查看；图表清晰显示随 April 2026 各日期变化的非平坦完成率趋势。

#### 最终结果检查

- “Dispatch Log”工作表仍保留第1行标题和第2至25行的24条每日调度记录，没有新增无关工作表、汇总行或分析列。
- 检查 B2:B25：每个单元格都有结果且以一位小数的百分比显示；例如选中任一结果单元格时，公式栏中的公式应使用该行的 D 列除以 C 列。
- 工作表中存在一个清晰可读的折线图：横轴类别来自 Dispatch Date，只有一个 Completion Rate 数据系列，折线连续且不显示数据点标记。
- 确认图表未遮住需要查看的源数据；必要时可将图表拖到表格右侧或下方的空白区域。

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
