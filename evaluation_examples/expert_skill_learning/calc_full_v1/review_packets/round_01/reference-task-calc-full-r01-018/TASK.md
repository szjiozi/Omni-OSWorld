# Workshop Attendance Register

- Reference task: `reference-task-calc-full-r01-018`
- Application: `libreoffice_calc`
- Review decision: `pending`

## Task instruction

Prepare the workshop attendance register by assigning each attendee a sequential text check-in tag, then add a Pivot Table report that shows how many attendees are registered in each workshop track.

## Required skills

### 1. Create a row-based text sequence formula

Skill ID: `7efeb4b1-3d19-4762-b163-63328d66303b.skill-01`

Procedure:

1. Select the first output cell in the sequence column, for example B2.
2. Type a concatenation formula such as `="No. " & ROW(B2)-1` and press Enter. `ROW(B2)` returns 2, so subtracting 1 makes the first result `No. 1`.
3. Adjust the referenced starting row or offset when the sequence begins elsewhere; for example, in row 5 use `="No. " & ROW(B5)-4` to begin at `No. 1`.

Efficiency tip: Enter the formula once in the first data row; do not manually type a separate sequence label in every row.

Source task: `7efeb4b1-3d19-4762-b163-63328d66303b`

Source instruction: Fill the Sequence Numbers as "No. #" in the "Seq No." column

Directly referenced source actions:

- Action 0: <code>`CLICK` B2</code>
- Action 1: <code>`TYPING` =&quot;No. &quot; &amp; ROW(B2)-1 </code>
- Action 2: <code>`PRESS` Enter.</code>

### 2. Place a field in Pivot Table row and data areas

Skill ID: `30e3e107-1cfb-46ee-a755-2cd080d7ba6a.skill-07`

Procedure:

1. In the Pivot Table layout dialog, locate a categorical field in Available Fields.
2. Drag the field to Row Fields to list each distinct category as a row.
3. Drag the same field to Data Fields to create a value calculation for those categories. For example, a field can be placed in both areas to show categories and their counts.

Efficiency tip: Drag the same field directly from Available Fields into each required area instead of searching for it again through menus.

Source task: `30e3e107-1cfb-46ee-a755-2cd080d7ba6a`

Source instruction: Please create a new sheet. Keep its sheet name as "Sheet2". Merge cells A1:C1 in the new sheet and write "Demographic Profile" with blue (#0000ff) fill and bold white text. Then I want to create three pivot tables to show the percentage of Sex, Civil Status, and Highest Educational Attainment. They should be stacked one by one in Sheet2, each separated with a blank line.

Directly referenced source actions:

- Action 20: <code>`MOVE_TO` &#x27;Sex&#x27; in available fields</code>
- Action 21: <code>`DRAG_TO` box in row fields</code>
- Action 22: <code>`MOVE_TO` &#x27;Sex&#x27; in available fields</code>
- Action 23: <code>`DRAG_TO` box in data fields</code>
- Action 40: <code>`MOVE_TO` &#x27;Civil Status&#x27; in available fields</code>
- Action 41: <code>`DRAG_TO` box in row fields</code>
- Action 42: <code>`MOVE_TO` &#x27;Civil Status&#x27; in available fields</code>
- Action 43: <code>`DRAG_TO` box in data fields</code>
- Action 60: <code>`MOVE_TO` &#x27;Highest Educational Attainment&#x27; in available fields</code>
- Action 61: <code>`DRAG_TO` box in row fields</code>
- Action 62: <code>`MOVE_TO` &#x27;Highest Educational Attainment&#x27; in available fields</code>
- Action 63: <code>`DRAG_TO` box in data fields</code>

## Initial state preview

### Attendance Log

![Attendance_Log.png](artifact/previews/Attendance_Log.png)

## Operator guide

### Existing operation-intent guide

#### Demonstration 1

- Skill: `7efeb4b1-3d19-4762-b163-63328d66303b.skill-01`
- Intent: Generate sequential text check-in tags beginning at 1 for all attendance records using a row-based concatenation formula.
- Efficiency: Write the formula once in the first Check-in Tag data cell using a ROW-based offset appropriate to row 2, then fill it through the contiguous record range.
- Visible success: Every record in Check-in Tag displays a consecutively numbered text label, beginning with the first record as number 1 and ending with number 24.

#### Demonstration 2

- Skill: `30e3e107-1cfb-46ee-a755-2cd080d7ba6a.skill-07`
- Intent: Create a Pivot Table that lists each Workshop Track and counts its attendance records by placing Workshop Track in both row and data areas.
- Efficiency: Drag Workshop Track from the available fields into both the row area and the data area directly, rather than selecting it once and searching for it again.
- Visible success: The Pivot Table visibly has one row per distinct workshop track and an adjacent count/value column showing the number of records for each track.

Recording start: The workbook contains only the populated Attendance Log source range, with Check-in Tag blank and no Pivot Table.

Recording end: The Attendance Log has formula-generated sequential Check-in Tags for all 24 records, and a visible Pivot Table reports the count for each Workshop Track.

Allowed variation: The expert may create the Pivot Table on a newly inserted sheet or in an unused area, and may use fill-down, a fill handle, or another equivalent Calc method to extend the formula. The displayed count label may follow Calc's automatic wording.

### 中文详细参考方案

> 以下是一个可以参考的操作 guide。标注者可以根据实际 LibreOffice 界面采用等价操作。

本指南将在现有的 `Attendance Log` 工作表中，为 24 条出勤记录生成连续的文字签到标签，并建立一个按 `Workshop Track` 汇总出勤人数的 Pivot Table。

#### 启动后的初始状态检查

- 确认当前打开的工作表是 `Attendance Log`。
- 确认第 1 行是标题行，记录位于第 2 行至第 25 行；`Check-in Tag` 列（D 列）当前为空。
- 确认 `Workshop Track` 列包含重复的类别值，且工作簿中尚未显示任何 Pivot Table。

#### 第 1 步：定位签到标签的起始单元格

1. 查看第 1 行标题，确认 `Check-in Tag` 位于 D 列、第一条记录位于第 2 行，最后一条记录位于第 25 行。
2. 单击单元格 D2；这是连续签到标签的起始单元格。

- 对应 skills：无；这是准备或检查步骤。
- 高效操作：先确认列位置再输入公式，可避免把标签写入 `Workshop Track` 或其他源数据列。
- 完成标志：D2 被选中，名称框或单元格边框显示当前活动单元格为 D2，且该列下方原本为空。

#### 第 2 步：创建首个文字签到标签公式

1. 在 D2 输入公式 `="No. " & ROW(D2)-1`，然后按 `Enter`。
2. 确认 D2 显示为 `No. 1`，而不是显示公式文字。若 D2 显示公式本身，请重新编辑该单元格，确认输入以等号 `=` 开头后再按 `Enter`。

- 对应 skills：`7efeb4b1-3d19-4762-b163-63328d66303b.skill-01`
- 高效操作：只在第一条记录输入一次公式；公式中的 `ROW(D2)-1` 会把第 2 行转换为从 1 开始的编号。
- 完成标志：D2 可见结果为 `No. 1`。

#### 第 3 步：向下填充所有签到标签

1. 选中 D2 到 D25 的连续区域，包含已有公式的 D2 和其下方所有空白签到标签单元格。
2. 按 `Ctrl+D`，将顶部单元格的公式向下填充到选中区域。
3. 查看 D2、D3 和 D25：它们应分别显示 `No. 1`、`No. 2` 和 `No. 24`。如果 D3 或更下方仍为空，重新选中 D2:D25 后再次按 `Ctrl+D`。

- 对应 skills：无；这是准备或检查步骤。
- 高效操作：一次选中 D2:D25 后使用填充命令，比逐行输入 24 个标签更快且能保持公式规律。
- 完成标志：D2:D25 都显示连续的 `No. #` 文本标签，最后一条记录显示 `No. 24`。

#### 第 4 步：创建按工作坊类别计数的 Pivot Table

1. 选中完整源数据区域 A1:E25，必须包含第 1 行的字段标题以及所有记录。
2. 打开 `Data` > `Pivot Table` > `Insert or Edit...`。在出现的来源确认界面中，若当前选择已显示为 A1:E25 或表示使用当前选择，直接确认继续；无需调整。
3. 若来源范围没有包含标题行或没有覆盖到第 25 行，返回工作表重新选中 A1:E25，再打开 `Data` > `Pivot Table` > `Insert or Edit...`。
4. 在 Pivot Table 布局对话框的可用字段列表中，找到 `Workshop Track`。将 `Workshop Track` 从可用字段列表拖到行字段区域，再从可用字段列表将同一字段拖到数据字段区域。
5. 数据字段通常会自动成为 `Count - Workshop Track` 或类似的计数结果；若数据区域显示的是求和、平均值或不是计数，双击数据字段，在其汇总函数设置中选择 `Count`，然后确认。
6. 在布局对话框底部用于指定结果位置的输入区域中，指定工作表的未用位置，例如 `$Attendance Log.$G$1`，再确认创建 Pivot Table。若默认结果位置已经在空白区域且不覆盖 A1:E25，则无需调整。

- 对应 skills：`30e3e107-1cfb-46ee-a755-2cd080d7ba6a.skill-07`
- 高效操作：直接从完整源区域创建 Pivot Table，确保字段标题和全部 24 条记录同时被识别。
- 完成标志：在指定的空白区域出现 Pivot Table；左侧列显示不同的 `Workshop Track` 值，右侧相邻列显示每个类别的数值计数。

#### 第 5 步：复核完成的签到标签和汇总报表

1. 复核 D2:D25 的标签序列：首项为 `No. 1`、末项为 `No. 24`，且编号连续。
2. 复核 Pivot Table：每个不同的 `Workshop Track` 应只出现一行，并有一个相邻的计数值列。
3. 若 Pivot Table 中类别为空、类别未按 `Workshop Track` 分行，或数值列不是记录数量，打开 `Data` > `Pivot Table` > `Insert or Edit...`，在布局中将 `Workshop Track` 同时放入行字段区域和数据字段区域，并将数据字段汇总函数改为 `Count` 后确认。
4. 若报表遮挡源数据，选中 Pivot Table 的外框并将整个报表移到另一块空白区域，使 A1:E25 保持可见。

- 对应 skills：无；这是准备或检查步骤。
- 高效操作：使用首尾标签和 Pivot Table 的类别/数值并排结构进行快速复核，不必逐一手工计数全部记录。
- 完成标志：签到标签完整连续，且 Pivot Table 清楚显示每种 `Workshop Track` 的一行及其对应人数。

#### 最终结果检查

- 在 `Attendance Log` 中，`Check-in Tag` 的数据区域 D2:D25 均为公式生成的文本标签：首项显示 `No. 1`，末项显示 `No. 24`，中间编号连续且没有空白。
- 工作簿中存在一个可见的 Pivot Table 报表；它按 `Workshop Track` 列出每个不同的工作坊类别，并在相邻数值列显示对应的记录计数。
- 确认源数据 A1:E25 仍保留可见，且 Pivot Table 没有覆盖原始出勤记录。

## Source-task similarity review

| Measure | Maximum | Most similar source task |
| --- | ---: | --- |
| Lexical sequence similarity | 0.360856 | 0a2e43bf-b26c-4631-a966-af9dfa12c9e5 |
| Semantic cosine similarity | 0.441439 | 1954cced-e748-45c4-9c26-9855b97fbc5e |

Similarity scores are reviewer aids, not automatic acceptance thresholds. Inspect the contributing source tasks and their complete ordered actions below.

### Source task `30e3e107-1cfb-46ee-a755-2cd080d7ba6a`

Original instruction:

> Please create a new sheet. Keep its sheet name as "Sheet2". Merge cells A1:C1 in the new sheet and write "Demographic Profile" with blue (#0000ff) fill and bold white text. Then I want to create three pivot tables to show the percentage of Sex, Civil Status, and Highest Educational Attainment. They should be stacked one by one in Sheet2, each separated with a blank line.

Required skills derived from this source task:

- **Place a field in Pivot Table row and data areas** — `30e3e107-1cfb-46ee-a755-2cd080d7ba6a.skill-07`

Complete ordered single-action sequence:

| Action | Related required skill | Original single action |
| ---: | --- | --- |
| 0 |  | <code>`CLICK` on + to left of sheet1</code> |
| 1 |  | <code>`KEY_DOWN` shift</code> |
| 2 |  | <code>`CLICK` C1</code> |
| 3 |  | <code>`RIGHT_CLICK` selection</code> |
| 4 |  | <code>`CLICK` merge cells</code> |
| 5 |  | <code>`TYPING` Demographic Profile</code> |
| 6 |  | <code>`PRESS` enter</code> |
| 7 |  | <code>`CLICK` cell A1</code> |
| 8 |  | <code>`CLICK` arrow next to paint button dropdown</code> |
| 9 |  | <code>`CLICK` Custom color</code> |
| 10 |  | <code>`DOUBLE_CLICK` on text inside Hex # box</code> |
| 11 |  | <code>`TYPING` 0000ff</code> |
| 12 |  | <code>`PRESS` enter</code> |
| 13 |  | <code>`CLICK` font color arrow icon, which is to left of bucket</code> |
| 14 |  | <code>`CLICK` top right color in the color palette (white)</code> |
| 15 |  | <code>`CLICK` bold icon</code> |
| 16 |  | <code>`CLICK` Sheet1</code> |
| 17 |  | <code>`CLICK` column B grey cell</code> |
| 18 |  | <code>`CLICK` pivot table icon</code> |
| 19 |  | <code>`PRESS` enter</code> |
| 20 | <strong>★ Place a field in Pivot Table row and data areas</strong><br><code>30e3e107-1cfb-46ee-a755-2cd080d7ba6a.skill-07</code> | <strong><code>`MOVE_TO` &#x27;Sex&#x27; in available fields</code></strong> |
| 21 | <strong>★ Place a field in Pivot Table row and data areas</strong><br><code>30e3e107-1cfb-46ee-a755-2cd080d7ba6a.skill-07</code> | <strong><code>`DRAG_TO` box in row fields</code></strong> |
| 22 | <strong>★ Place a field in Pivot Table row and data areas</strong><br><code>30e3e107-1cfb-46ee-a755-2cd080d7ba6a.skill-07</code> | <strong><code>`MOVE_TO` &#x27;Sex&#x27; in available fields</code></strong> |
| 23 | <strong>★ Place a field in Pivot Table row and data areas</strong><br><code>30e3e107-1cfb-46ee-a755-2cd080d7ba6a.skill-07</code> | <strong><code>`DRAG_TO` box in data fields</code></strong> |
| 24 |  | <code>`DOUBLE_CLICK on sex box in data fields</code> |
| 25 |  | <code>`CLICK` Count</code> |
| 26 |  | <code>`CLICK` &#x27;displayed value&#x27; dropdown</code> |
| 27 |  | <code>`CLICK` Normal dropdown next to &#x27;Type&#x27;</code> |
| 28 |  | <code>`CLICK` &#x27;% of total&#x27;</code> |
| 29 |  | <code>`CLICK` ok</code> |
| 30 |  | <code>`CLICK` source and destination dropdown</code> |
| 31 |  | <code>`CLICK` &#x27;Selection&#x27; under destination</code> |
| 32 |  | <code>`CLICK` text box</code> |
| 33 |  | <code>`TYPING` &#x27;$Sheet2.$A$2&#x27;</code> |
| 34 |  | <code>`CLICK` ok</code> |
| 35 |  | <code>`CLICK` Sheet2</code> |
| 36 |  | <code>`CLICK` Sheet1</code> |
| 37 |  | <code>`CLICK` column C grey cell</code> |
| 38 |  | <code>`CLICK` pivot table icon</code> |
| 39 |  | <code>`PRESS` enter</code> |
| 40 | <strong>★ Place a field in Pivot Table row and data areas</strong><br><code>30e3e107-1cfb-46ee-a755-2cd080d7ba6a.skill-07</code> | <strong><code>`MOVE_TO` &#x27;Civil Status&#x27; in available fields</code></strong> |
| 41 | <strong>★ Place a field in Pivot Table row and data areas</strong><br><code>30e3e107-1cfb-46ee-a755-2cd080d7ba6a.skill-07</code> | <strong><code>`DRAG_TO` box in row fields</code></strong> |
| 42 | <strong>★ Place a field in Pivot Table row and data areas</strong><br><code>30e3e107-1cfb-46ee-a755-2cd080d7ba6a.skill-07</code> | <strong><code>`MOVE_TO` &#x27;Civil Status&#x27; in available fields</code></strong> |
| 43 | <strong>★ Place a field in Pivot Table row and data areas</strong><br><code>30e3e107-1cfb-46ee-a755-2cd080d7ba6a.skill-07</code> | <strong><code>`DRAG_TO` box in data fields</code></strong> |
| 44 |  | <code>`DOUBLE_CLICK on civil status box in data fields</code> |
| 45 |  | <code>`CLICK` Count</code> |
| 46 |  | <code>`CLICK` &#x27;displayed value&#x27; dropdown</code> |
| 47 |  | <code>`CLICK` Normal dropdown next to &#x27;Type&#x27;</code> |
| 48 |  | <code>`CLICK` &#x27;% of total&#x27;</code> |
| 49 |  | <code>`PRESS` enter</code> |
| 50 |  | <code>`CLICK` source and destination dropdown</code> |
| 51 |  | <code>`CLICK` &#x27;Selection&#x27; under destination</code> |
| 52 |  | <code>`CLICK` text box</code> |
| 53 |  | <code>`TYPING` &#x27;$Sheet2.$A$7&#x27;</code> |
| 54 |  | <code>`CLICK` ok</code> |
| 55 |  | <code>`CLICK` Sheet2</code> |
| 56 |  | <code>`CLICK` Sheet1</code> |
| 57 |  | <code>`CLICK` column D grey cell</code> |
| 58 |  | <code>`CLICK` pivot table icon</code> |
| 59 |  | <code>`PRESS` enter</code> |
| 60 | <strong>★ Place a field in Pivot Table row and data areas</strong><br><code>30e3e107-1cfb-46ee-a755-2cd080d7ba6a.skill-07</code> | <strong><code>`MOVE_TO` &#x27;Highest Educational Attainment&#x27; in available fields</code></strong> |
| 61 | <strong>★ Place a field in Pivot Table row and data areas</strong><br><code>30e3e107-1cfb-46ee-a755-2cd080d7ba6a.skill-07</code> | <strong><code>`DRAG_TO` box in row fields</code></strong> |
| 62 | <strong>★ Place a field in Pivot Table row and data areas</strong><br><code>30e3e107-1cfb-46ee-a755-2cd080d7ba6a.skill-07</code> | <strong><code>`MOVE_TO` &#x27;Highest Educational Attainment&#x27; in available fields</code></strong> |
| 63 | <strong>★ Place a field in Pivot Table row and data areas</strong><br><code>30e3e107-1cfb-46ee-a755-2cd080d7ba6a.skill-07</code> | <strong><code>`DRAG_TO` box in data fields</code></strong> |
| 64 |  | <code>`DOUBLE_CLICK on Highest Educational Attainment box in data fields</code> |
| 65 |  | <code>`CLICK` Count</code> |
| 66 |  | <code>`CLICK` &#x27;displayed value&#x27; dropdown</code> |
| 67 |  | <code>`CLICK` Normal dropdown next to &#x27;Type&#x27;</code> |
| 68 |  | <code>`CLICK` &#x27;% of total&#x27;</code> |
| 69 |  | <code>`PRESS` enter</code> |
| 70 |  | <code>`CLICK` source and destination dropdown</code> |
| 71 |  | <code>`CLICK` &#x27;Selection&#x27; under destination</code> |
| 72 |  | <code>`CLICK` text box</code> |
| 73 |  | <code>`TYPING` &#x27;$Sheet2.$A$13&#x27;</code> |
| 74 |  | <code>`CLICK` ok</code> |

### Source task `7efeb4b1-3d19-4762-b163-63328d66303b`

Original instruction:

> Fill the Sequence Numbers as "No. #" in the "Seq No." column

Required skills derived from this source task:

- **Create a row-based text sequence formula** — `7efeb4b1-3d19-4762-b163-63328d66303b.skill-01`

Complete ordered single-action sequence:

| Action | Related required skill | Original single action |
| ---: | --- | --- |
| 0 | <strong>★ Create a row-based text sequence formula</strong><br><code>7efeb4b1-3d19-4762-b163-63328d66303b.skill-01</code> | <strong><code>`CLICK` B2</code></strong> |
| 1 | <strong>★ Create a row-based text sequence formula</strong><br><code>7efeb4b1-3d19-4762-b163-63328d66303b.skill-01</code> | <strong><code>`TYPING` =&quot;No. &quot; &amp; ROW(B2)-1 </code></strong> |
| 2 | <strong>★ Create a row-based text sequence formula</strong><br><code>7efeb4b1-3d19-4762-b163-63328d66303b.skill-01</code> | <strong><code>`PRESS` Enter.</code></strong> |
| 3 |  | <code>`CLICK` B2</code> |
| 4 |  | <code>`DOUBLE_CLICK` bottom right corner of cell</code> |

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
