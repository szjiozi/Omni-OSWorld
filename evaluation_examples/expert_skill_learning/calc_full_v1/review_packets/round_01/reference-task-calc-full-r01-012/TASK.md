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

在 `Dispatch Log` 中先以相对引用计算每日 Completion Rate，再快速向下填满 24 条记录，最后以 Dispatch Date 和 Completion Rate 创建无标记的折线图来展示每日完成率趋势。

#### 启动后的初始状态检查

- 确认当前活动工作表为 `Dispatch Log`。
- 确认第 1 行是标题行，数据位于第 2 至第 25 行；`B2:B25` 为空但显示为百分比格式，C 列为 Planned Kits、D 列为 Verified Kits。
- 确认工作表中尚未存在图表对象。

#### 第 1 步：在首行计算完成率

1. 单击第一个结果单元格 `B2`。
2. 输入公式 `=D2/C2`，然后按 `Enter`。这里 D 列的 Verified Kits 是分子，C 列的 Planned Kits 是分母。
3. 观察 `B2` 显示为一位小数的百分比。若显示的是普通小数而不是百分比，选中 `B2`，点击 `Format` > `Format Cells...`，在数字格式中选择百分比并设置为 1 位小数。

- 对应 skills：`21ab7b40-77c2-4ae6-8321-e00d3a086c73.skill-01`
- 高效操作：只输入一次使用相对引用的公式；后续复制时 Calc 会自动按行调整引用，无需逐行计算。
- 完成标志：`B2` 已显示一个百分比结果，且该结果等于第 2 行 `D2` 的 Verified Kits 除以 `C2` 的 Planned Kits。

#### 第 2 步：向下填充所有每日完成率

1. 保持或重新选中 `B2`。
2. 将指针移到 `B2` 选中边框右下角的小方块（填充柄）。当指针表示可填充时，双击该填充柄。
3. Calc 会沿着相邻的连续数据区域向下复制公式，直到第 25 行。
4. 若双击后没有填充到 `B25`，选中 `B2`，复制该单元格，然后选中 `B3:B25` 并粘贴；相对引用会随行号自动变化。

- 对应 skills：`51719eea-10bc-4246-a428-ac7c433dd4b3.skill-02`
- 高效操作：对有相邻连续数据的表格，双击填充柄比拖动或重复输入公式更快，也较不容易漏行。
- 完成标志：`B2:B25` 均显示百分比结果；例如选择 `B25` 时，输入行中的公式为 `=D25/C25`。

#### 第 3 步：创建无标记的完成率折线图

1. 选择图表源数据范围 `A1:B25`，其中 A 列为 Dispatch Date，B 列为已计算的 Completion Rate，且第 1 行标题也要包含在选择中。
2. 打开 `Insert` > `Chart...`。在图表创建窗口中选择 `Line` 图表类型。
3. 在该类型的变体图标中，选择无点标记、仅显示线条的变体（此界面中为从右数第三个图标），然后点击 `Finish`。
4. 完成后查看图表：应以 Dispatch Date 为横轴类别，显示一条 Completion Rate 连线且没有点标记。若已经符合此结果，无需调整。
5. 如果横轴标签不是日期、绘制了错误的列或数值不正确，双击图表进入编辑状态，打开 `Format` > `Data Ranges`，在 `Data Series` 中将 `Categories` 设为 `$'Dispatch Log'.$A$2:$A$25`，并将该系列的 `Y-Values` 设为 `$'Dispatch Log'.$B$2:$B$25`；完成后退出图表编辑状态。

- 对应 skills：`0a2e43bf-b26c-4631-a966-af9dfa12c9e5.skill-04`
- 高效操作：一次选中包含标题的日期和完成率两列，可让 Calc 自动把日期识别为类别、把 Completion Rate 识别为唯一的数据系列。
- 完成标志：工作表上出现一张折线图：日期用作横轴类别，只有一条随日期变化的 Completion Rate 线，并且线上没有圆点或其他数据点标记。

#### 第 4 步：整理图表并完成核对

1. 确认图表没有遮挡 `A1:D25` 的源数据。若图表已在空白区域且源单元格可读，无需调整。
2. 如果图表遮住了数据，单击图表外边框以选中整个对象，然后拖动整个图表到工作表的空白区域，或适度调整其大小，使数据表和图表都清晰可见。
3. 抽查 `B2`、中间任意一行和 `B25`：每个结果都应为百分比，且同一行的完成率应与 Verified Kits ÷ Planned Kits 一致。
4. 最后确认图表没有额外数据系列，横轴仍显示每日日期，且折线趋势不是一条完全水平的线。

- 对应 skills：无；这是准备或检查步骤。
- 高效操作：先核对少量代表性行和图表的系列数量，能快速发现公式未填满、选择范围过大或图表角色识别错误等问题。
- 完成标志：原始表格、所有 24 个完成率和一张可读的无标记单系列折线图同时清晰可见。

#### 最终结果检查

- `Dispatch Log` 工作表仍保留 24 条 2026 年 4 月的原始派送记录，且没有新增不相关的工作表或汇总数据。
- `B2:B25` 均为一位小数的百分比；例如选中任意一行的 B 列单元格，在输入行可看到该行形式为 `=D行号/C行号` 的公式，数值等于 Verified Kits 除以 Planned Kits。
- 图表清晰可见且未遮住源表：横轴为 Dispatch Date 的日期类别，仅有一条 Completion Rate 折线，并且线条没有数据点标记。

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
