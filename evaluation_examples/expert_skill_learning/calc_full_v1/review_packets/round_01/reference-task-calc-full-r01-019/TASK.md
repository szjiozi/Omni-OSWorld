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

本指南将在 `Volunteer Activity` 工作表中为每位园艺志愿者计算截至今天的完整服务年数，将出勤比率显示为百分比，并把土壤读数统一显示为两位小数。操作使用相对引用公式和整段/整列格式化，可避免逐行重复处理。

#### 启动后的初始状态检查

- 确认当前打开的是 `Volunteer Activity` 工作表，且第 1 行包含 `Volunteer Code`、`Garden Zone`、`Enrollment Date`、`Completed Years`、`Attendance Ratio` 和 `Soil Reading` 表头。
- 确认数据记录连续位于第 2 至 25 行：`Completed Years` 列为空，`Attendance Ratio` 仍显示为类似 `0.875` 的小数，`Soil Reading` 尚未统一显示两位小数。
- 确认 `Enrollment Date` 位于 C 列并紧邻 D 列的 `Completed Years`，这样填充公式时 Calc 可以识别连续数据范围。

#### 第 1 步：在首行输入完整服务年数公式

1. 点击 `D2`，即 `Completed Years` 表头下的第一个空白单元格。
2. 输入公式 `=DATEDIF(C2,TODAY(),"Y")`，然后按 `Enter`。其中 `C2` 是同一行的 Enrollment Date，`"Y"` 表示只返回已完成的整年数。
3. 观察 `D2` 的结果。应显示非负整数；再次选中 `D2` 时，公式栏应显示刚输入的 `DATEDIF` 公式。

- 对应 skills：`4e6fcf72-daf3-439f-a232-c434ce416af6.skill-01`
- 高效操作：只在首个结果单元格建立一次相对引用公式；随后填充时无需逐位志愿者重复输入。
- 完成标志：`D2` 不再为空，显示一个非负的整年数，且公式栏显示 `=DATEDIF(C2,TODAY(),"Y")`。

#### 第 2 步：向下填充所有志愿者的服务年数

1. 选中含有公式的 `D2`。
2. 将指针移到选中单元格右下角的小方块，即填充柄；当指针可用于填充时，双击该小方块。
3. 预期 Calc 会沿着相邻 C 列的连续记录向下填充，`D2:D25` 都会出现结果，因此无需调整。
4. 如果填充没有到达 `D25`，或在某个较早行停止，先查看 C 列对应位置是否有意外空白；随后选中从 `D2` 到 `D25` 的范围，使用 `Sheet` > `Fill Cells` > `Down`，将首行公式填至选中范围。

- 对应 skills：`a9f325aa-8c05-4e4f-8341-9e4358565f4f.skill-02`
- 高效操作：双击填充柄比把公式手动复制到 24 行更快；相邻的 Enrollment Date 记录连续时，Calc 会自动停止在最后一条记录。
- 完成标志：`D2:D25` 的每个数据行都有整数结果；选中不同的已填充单元格时，公式中的 C 列行号会相应变化。

#### 第 3 步：将出勤比率显示为百分比

1. 拖动选择 `E2:E25`，即全部 `Attendance Ratio` 数据单元格，不要选入表头。
2. 在格式工具栏上点击 Percent (%) 按钮。
3. 预期原先类似 `0.875` 的数值会显示为类似 `88%` 或 `87.5%`，并保留百分号；若已经如此显示，无需调整。
4. 如果选中范围中的值仍显示为原始小数，确认选中的是 `E2:E25`，然后再次点击格式工具栏的 Percent (%) 按钮。

- 对应 skills：`04d9aeaf-7bed-4024-bedb-e10e6f00eb7f.skill-06`
- 高效操作：一次选中整个结果区域并设置格式，能让所有出勤记录保持一致，且不改变原有小数数值。
- 完成标志：`E2:E25` 显示百分号，例如原先的 `0.875` 显示为 `88%` 或带小数的百分比。

#### 第 4 步：将土壤读数统一显示为两位小数

1. 点击 F 列列标，选中整个 `Soil Reading` 列。
2. 在格式工具栏上使用 `Increase Decimal` 两次，每次增加一个显示小数位。
3. 预期 F 列的土壤读数会统一显示两位小数，例如 `8` 显示为 `8.00`、`7.5` 显示为 `7.50`；若已全部显示两位小数，无需调整。
4. 如果仍有读数少于两位小数，再点击 `Increase Decimal`，直到读数显示两位；如果超过两位小数，则使用相邻的减少显示小数位控制，直至显示为两位。

- 对应 skills：`6e99a1ad-07d2-4b66-a1ce-ece6d99c20a5.skill-01`
- 高效操作：选中整列后再增加小数位，可一次作用于所有现有土壤读数及该列后续输入的数值，无需逐单元格处理。
- 完成标志：F 列的 Soil Reading 数值均显示恰好两位小数，整数读数也带有 `.00`。

#### 最终结果检查

- 在 `Volunteer Activity` 工作表中，`D2:D25` 都显示非负整数；分别选中例如 `D2` 和 `D3` 时，公式栏可见其引用会随行号变化，例如 `=DATEDIF(C2,TODAY(),"Y")` 与 `=DATEDIF(C3,TODAY(),"Y")`。
- `E2:E25` 的数值均以百分比显示并带有 `%` 符号，而不是原始小数形式；这些单元格仍是数值而非文本。
- `F2:F25` 的 Soil Reading 显示均有两位小数，包含原本为整数的值也显示类似 `8.00`，一位小数的值显示类似 `7.50`。
- 表中原有的 24 条记录仍连续位于第 2 至 25 行，表头及其他源数据没有被覆盖或删除。

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
