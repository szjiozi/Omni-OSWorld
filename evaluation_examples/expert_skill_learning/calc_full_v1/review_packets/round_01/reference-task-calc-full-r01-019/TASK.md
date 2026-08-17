# Garden Volunteer Activity Tracker

- Reference task: `reference-task-calc-full-r01-019`
- Application: `libreoffice_calc`
- Review decision: `pending`

## Task instruction

Complete the Garden Volunteer Activity tracker by calculating each volunteer’s completed years of service from their enrollment date, presenting attendance as percentages, and standardizing all soil readings to two displayed decimal places.

## Required skills

### 1. Enter a date-difference formula that returns whole years

Skill ID: `4e6fcf72-daf3-439f-a232-c434ce416af6.skill-01`

Procedure:

1. Select the first output cell beside the date column, for example D2.
2. Type a formula such as `=DATEDIF(C2,TODAY(),"Y")` and press Enter. `C2` is a relative reference, so it can adjust to each row when propagated later.
3. The `"Y"` unit returns completed whole years between the date in C2 and the current date.

Efficiency tip: Enter the formula once in the first result cell, then use a propagation command such as the fill handle rather than retyping it for each row.

Source task: `4e6fcf72-daf3-439f-a232-c434ce416af6`

Source instruction: Please calculate the ages of the employees according to their birthday.

Directly referenced source actions:

- Action 0: <code>`CLICK` on the first table cell of the column &#x27;Age&#x27;, D2</code>
- Action 1: <code>`TYPING` the formula `=DATEDIF(C2,TODAY(),&quot;Y&quot;)` where &#x27;C2&#x27; is the column containing the first employee&#x27;s birthdate</code>
- Action 2: <code>`PRESS` &#x27;Enter</code>

### 2. Increase displayed decimal places for an entire column

Skill ID: `6e99a1ad-07d2-4b66-a1ce-ece6d99c20a5.skill-01`

Procedure:

1. Click the column header for the numeric column to select the whole column; for example, click column C.
2. Use the toolbar’s Increase Decimal button to add displayed decimal places. Each activation increases the displayed precision by one decimal place; double-click it when two additional places are needed.
3. For example, a value displayed as 12 can be shown as 12.00 after increasing the decimal places twice. This changes display formatting, not the stored numeric value.

Efficiency tip: Select the entire column first so one formatting command updates all existing values and cells entered later, instead of adjusting decimal places cell by cell.

Source task: `6e99a1ad-07d2-4b66-a1ce-ece6d99c20a5`

Source instruction: Help me format column "spent" by keeping two decimal points. 

Directly referenced source actions:

- Action 0: <code>`CLICK` column C.</code>
- Action 1: <code>`DOUBLE_CLICK` the &#x27;Increase Decimal&#x27; button.</code>

### 3. Apply percentage number formatting to a cell range

Skill ID: `04d9aeaf-7bed-4024-bedb-e10e6f00eb7f.skill-06`

Procedure:

1. Select the cells containing ratio or change results; for example, drag from B2 to D6.
2. Click the Percent (%) button on the formatting toolbar. Calc displays the selected numeric values as percentages while retaining their underlying values.

Efficiency tip: Select the entire result range before applying the format so all existing values use one consistent number format.

Source task: `04d9aeaf-7bed-4024-bedb-e10e6f00eb7f`

Source instruction: In a new sheet with 4 headers "Year", "CA changes", "FA changes", and "OA changes", calculate the percentage annual changes compared to last year in 2015 to 2019 for the Current Assets, Fixed Assets, and Other Assets columns. 

Directly referenced source actions:

- Action 25: <code>`CLICK` cell B2</code>
- Action 26: <code>`DRAG_TO` D6</code>
- Action 27: <code>`CLICK` percent symbol</code>

### 4. Autofill a formula down a contiguous adjacent data range

Skill ID: `a9f325aa-8c05-4e4f-8341-9e4358565f4f.skill-02`

Procedure:

1. Select the cell containing the completed formula, such as C2.
2. Move to the small square at the cell's bottom-right corner (the fill handle) and double-click it.
3. Calc fills the formula downward for the contiguous rows detected in the neighboring data column, adjusting relative references; for example, `B2` becomes `B3`, `B4`, and so on.

Efficiency tip: Double-clicking the fill handle is faster than dragging it through a long contiguous data block; verify that the adjacent source column has no unintended blank rows, because blanks can limit propagation.

Source task: `a9f325aa-8c05-4e4f-8341-9e4358565f4f`

Source instruction: I want to copy the movie titles in 'Garbage Movie Titles' column to the 'Clean Movie Titles' column. But please remove the adundant whitespaces and canonicalize the letter cases by capitalizing the first letter of each words and leave other letters as lower case.

Directly referenced source actions:

- Action 3: <code>`CLICK C2</code>
- Action 4: <code>`DOUBLE_CLICK` bottom right corner of the cell</code>

## Initial state preview

### Volunteer Activity

![Volunteer_Activity.png](artifact/previews/Volunteer_Activity.png)

## Operator guide

### Existing operation-intent guide

#### Demonstration 1

- Skill: `4e6fcf72-daf3-439f-a232-c434ce416af6.skill-01`
- Intent: In the first Completed Years cell, enter a DATEDIF-based formula that calculates completed whole years from that row's Enrollment Date through TODAY().
- Efficiency: Enter the formula only once with a relative reference to the first enrollment date; avoid manually calculating each volunteer's tenure.
- Visible success: The first Completed Years result displays a nonnegative whole-number tenure, while the formula bar shows a date-difference formula using the whole-years unit.

#### Demonstration 2

- Skill: `a9f325aa-8c05-4e4f-8341-9e4358565f4f.skill-02`
- Intent: Propagate the completed-years formula from the first result cell through every populated volunteer record.
- Efficiency: Use the fill handle's double-click behavior or an equivalent fill-down command, because the neighboring records are contiguous.
- Visible success: Every Completed Years cell from row 2 through row 25 contains a result, and row-relative date references are evident when different filled cells are selected.

#### Demonstration 3

- Skill: `04d9aeaf-7bed-4024-bedb-e10e6f00eb7f.skill-06`
- Intent: Display each attendance ratio as a percentage.
- Efficiency: Select all populated Attendance Ratio cells as one range before applying the number format.
- Visible success: Values formerly shown as fractions such as 0.875 visibly display with percent signs, such as 88% or 87.5%, while retaining their values.

#### Demonstration 4

- Skill: `6e99a1ad-07d2-4b66-a1ce-ece6d99c20a5.skill-01`
- Intent: Increase the displayed decimal precision for the Soil Reading column until values consistently show two decimal places.
- Efficiency: Format the entire Soil Reading column in one action sequence rather than modifying individual cells.
- Visible success: All displayed Soil Reading values, including whole-number entries, show two digits after the decimal separator (for example, 8.00 and 7.50).

Recording start: The workbook is open with the 24-row Volunteer Activity table visible; Completed Years is empty, Attendance Ratio is shown as raw decimal fractions, and Soil Reading is in General format.

Recording end: The Volunteer Activity sheet shows calculated whole completed years for every record, percentage-formatted Attendance Ratio cells, and Soil Reading displayed uniformly with two decimal places.

Allowed variation: The expert may use toolbar controls, menu commands, keyboard shortcuts, or another equivalent Calc method. Formula propagation may use a fill handle or an equivalent fill-down command, provided the relative formula is visibly extended through the contiguous records.

### 中文详细参考方案

> 以下是一个可以参考的操作 guide。标注者可以根据实际 LibreOffice 界面采用等价操作。

本指南将在“Volunteer Activity”工作表中完成三项整理：根据 Enrollment Date 自动计算每位志愿者的完整服务年数，将 Attendance Ratio 显示为百分比，并让 Soil Reading 统一显示两位小数。

#### 启动后的初始状态检查

- 确认当前打开的工作表标签是“Volunteer Activity”。
- 确认第 1 行是标题行，数据连续位于第 2 行到第 25 行；中间不应有空白记录。
- 确认 C 列标题为 Enrollment Date，D 列标题为 Completed Years 且 D2:D25 尚为空白。
- 确认 E 列 Attendance Ratio 仍显示为类似 0.875 的小数而非百分比，F 列 Soil Reading 尚未统一显示两位小数。

#### 第 1 步：在首行计算完整服务年数

1. 单击 D2，即 Completed Years 标题正下方的第一个空白单元格。
2. 输入公式 `=DATEDIF(C2,TODAY(),"Y")`，然后按 Enter。
3. 如需确认公式，重新选中 D2 并查看编辑栏；其中 `"Y"` 表示只返回已经完整经过的年数。

- 对应 skills：`4e6fcf72-daf3-439f-a232-c434ce416af6.skill-01`
- 高效操作：只在第一行输入一次公式；公式中的 C2 是相对引用，后续填充时 Calc 会自动改为对应行的日期单元格。
- 完成标志：D2 显示一个非负的整数年数，而不是日期或错误值；编辑栏显示使用 C2、TODAY() 和 "Y" 的 DATEDIF 公式。

#### 第 2 步：将服务年数公式填充到所有志愿者记录

1. 选中含有公式的 D2。
2. 将指针移到选中单元格右下角的小方块，即填充柄。
3. 双击填充柄，让 Calc 自动向下填充相邻连续记录对应的行。
4. 向下查看直到第 25 行，必要时单击任一已填充单元格（例如 D10），确认其公式引用的是同一行的 Enrollment Date，例如 C10。

- 对应 skills：`a9f325aa-8c05-4e4f-8341-9e4358565f4f.skill-02`
- 高效操作：相邻的 Enrollment Date 数据连续至第 25 行时，双击填充柄会比逐行复制或拖动更快。
- 完成标志：D2:D25 均有完成年数结果；选择不同数据行时，公式中的 C 行号会相应变化。

#### 第 3 步：将出勤率显示为百分比

1. 选择 Attendance Ratio 的数据区域 E2:E25；可单击 E2 后拖动到 E25。
2. 在格式工具栏上单击 Percent (%) 按钮。
3. 不要重新输入或乘以 100；百分比格式只改变显示方式，原有小数数值仍会保留。

- 对应 skills：`04d9aeaf-7bed-4024-bedb-e10e6f00eb7f.skill-06`
- 高效操作：先一次选中完整的数据区域再设置格式，可避免遗漏行，并保持全部出勤率显示一致。
- 完成标志：E2:E25 的数值显示 % 符号；例如原来显示为 0.875 的值会显示为约 88% 或 87.5%。

#### 第 4 步：将土壤读数统一显示为两位小数

1. 单击列标 F，选中整个 Soil Reading 列。
2. 在格式工具栏上找到 Increase Decimal（增加小数位数）按钮。
3. 连续单击该按钮两次，使该列的显示精度增加到两位小数。
4. 查看 F 列中的整数和原先带一位小数的数值，确认它们都按两位小数显示。

- 对应 skills：`6e99a1ad-07d2-4b66-a1ce-ece6d99c20a5.skill-01`
- 高效操作：选择整列后再调整小数位，能同时格式化当前土壤读数以及该列以后输入的数值，而无需逐个单元格处理。
- 完成标志：F 列 Soil Reading 的数据均显示两位小数，包括整数显示为类似 8.00、原有一位小数显示为类似 7.50。

#### 最终结果检查

- 确认工作表仍为“Volunteer Activity”，且没有新增工作表、图表或其他无关内容。
- 检查 D2:D25：每一行都有非负整数的 Completed Years 结果。任选如 D10 的单元格查看编辑栏，应能看到随行号变化的公式，例如 =DATEDIF(C10,TODAY(),"Y")。
- 检查 E2:E25：所有 Attendance Ratio 值均以带 % 符号的百分比形式显示，而不是原始小数。
- 检查 Soil Reading 列 F：数据行中的数值均显示两位小数；原先的整数应显示为类似 8.00，带一位小数的值应显示为类似 7.50。
- 保存工作簿，保留这些公式和数字显示格式。

## Source-task similarity review

| Measure | Maximum | Most similar source task |
| --- | ---: | --- |
| Lexical sequence similarity | 0.295699 | 12382c62-0cd1-4bf2-bdc8-1d20bf9b2371 |
| Semantic cosine similarity | 0.370169 | 04d9aeaf-7bed-4024-bedb-e10e6f00eb7f |

Similarity scores are reviewer aids, not automatic acceptance thresholds. Inspect the contributing source tasks and their complete ordered actions below.

### Source task `04d9aeaf-7bed-4024-bedb-e10e6f00eb7f`

Original instruction:

> In a new sheet with 4 headers "Year", "CA changes", "FA changes", and "OA changes", calculate the percentage annual changes compared to last year in 2015 to 2019 for the Current Assets, Fixed Assets, and Other Assets columns. 

Required skills derived from this source task:

- **Apply percentage number formatting to a cell range** — `04d9aeaf-7bed-4024-bedb-e10e6f00eb7f.skill-06`

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
| 16 |  | <code>`CLICK` cell B2</code> |
| 17 |  | <code>`DOUBLE_CLICK` bottom right corner</code> |
| 18 |  | <code>`CLICK` cell B2</code> |
| 19 |  | <code>`MOVE_TO` bottom right corner of the cell B2</code> |
| 20 |  | <code>`DRAG_TO` cell D2</code> |
| 21 |  | <code>`CLICK` cell C2</code> |
| 22 |  | <code>`DOUBLE_CLICK` bottom right corner</code> |
| 23 |  | <code>`MOVE_TO` cell D2</code> |
| 24 |  | <code>`DOUBLE_CLICK` bottom right corner</code> |
| 25 | <strong>★ Apply percentage number formatting to a cell range</strong><br><code>04d9aeaf-7bed-4024-bedb-e10e6f00eb7f.skill-06</code> | <strong><code>`CLICK` cell B2</code></strong> |
| 26 | <strong>★ Apply percentage number formatting to a cell range</strong><br><code>04d9aeaf-7bed-4024-bedb-e10e6f00eb7f.skill-06</code> | <strong><code>`DRAG_TO` D6</code></strong> |
| 27 | <strong>★ Apply percentage number formatting to a cell range</strong><br><code>04d9aeaf-7bed-4024-bedb-e10e6f00eb7f.skill-06</code> | <strong><code>`CLICK` percent symbol</code></strong> |

### Source task `4e6fcf72-daf3-439f-a232-c434ce416af6`

Original instruction:

> Please calculate the ages of the employees according to their birthday.

Required skills derived from this source task:

- **Enter a date-difference formula that returns whole years** — `4e6fcf72-daf3-439f-a232-c434ce416af6.skill-01`

Complete ordered single-action sequence:

| Action | Related required skill | Original single action |
| ---: | --- | --- |
| 0 | <strong>★ Enter a date-difference formula that returns whole years</strong><br><code>4e6fcf72-daf3-439f-a232-c434ce416af6.skill-01</code> | <strong><code>`CLICK` on the first table cell of the column &#x27;Age&#x27;, D2</code></strong> |
| 1 | <strong>★ Enter a date-difference formula that returns whole years</strong><br><code>4e6fcf72-daf3-439f-a232-c434ce416af6.skill-01</code> | <strong><code>`TYPING` the formula `=DATEDIF(C2,TODAY(),&quot;Y&quot;)` where &#x27;C2&#x27; is the column containing the first employee&#x27;s birthdate</code></strong> |
| 2 | <strong>★ Enter a date-difference formula that returns whole years</strong><br><code>4e6fcf72-daf3-439f-a232-c434ce416af6.skill-01</code> | <strong><code>`PRESS` &#x27;Enter</code></strong> |
| 3 |  | <code>`CLICK` cell D2</code> |
| 4 |  | <code>`DOUBLE_CLICK` bottom right corner of cell</code> |

### Source task `6e99a1ad-07d2-4b66-a1ce-ece6d99c20a5`

Original instruction:

> Help me format column "spent" by keeping two decimal points. 

Required skills derived from this source task:

- **Increase displayed decimal places for an entire column** — `6e99a1ad-07d2-4b66-a1ce-ece6d99c20a5.skill-01`

Complete ordered single-action sequence:

| Action | Related required skill | Original single action |
| ---: | --- | --- |
| 0 | <strong>★ Increase displayed decimal places for an entire column</strong><br><code>6e99a1ad-07d2-4b66-a1ce-ece6d99c20a5.skill-01</code> | <strong><code>`CLICK` column C.</code></strong> |
| 1 | <strong>★ Increase displayed decimal places for an entire column</strong><br><code>6e99a1ad-07d2-4b66-a1ce-ece6d99c20a5.skill-01</code> | <strong><code>`DOUBLE_CLICK` the &#x27;Increase Decimal&#x27; button.</code></strong> |

### Source task `a9f325aa-8c05-4e4f-8341-9e4358565f4f`

Original instruction:

> I want to copy the movie titles in 'Garbage Movie Titles' column to the 'Clean Movie Titles' column. But please remove the adundant whitespaces and canonicalize the letter cases by capitalizing the first letter of each words and leave other letters as lower case.

Required skills derived from this source task:

- **Autofill a formula down a contiguous adjacent data range** — `a9f325aa-8c05-4e4f-8341-9e4358565f4f.skill-02`

Complete ordered single-action sequence:

| Action | Related required skill | Original single action |
| ---: | --- | --- |
| 0 |  | <code>`CLICK` C2</code> |
| 1 |  | <code>`TYPING` &#x27;=PROPER(TRIM(B2))&#x27;</code> |
| 2 |  | <code>`PRESS` Enter</code> |
| 3 | <strong>★ Autofill a formula down a contiguous adjacent data range</strong><br><code>a9f325aa-8c05-4e4f-8341-9e4358565f4f.skill-02</code> | <strong><code>`CLICK C2</code></strong> |
| 4 | <strong>★ Autofill a formula down a contiguous adjacent data range</strong><br><code>a9f325aa-8c05-4e4f-8341-9e4358565f4f.skill-02</code> | <strong><code>`DOUBLE_CLICK` bottom right corner of the cell</code></strong> |

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
