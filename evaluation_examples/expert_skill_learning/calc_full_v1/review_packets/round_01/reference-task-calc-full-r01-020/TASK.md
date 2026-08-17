# Community Garden Supply Budget

- Reference task: `reference-task-calc-full-r01-020`
- Application: `libreoffice_calc`
- Review decision: `pending`

## Task instruction

Finish the Community Garden Supply Plan by giving the title cell A1 a #2F6B4F background and completing the Line Cost calculations for every listed supply item from the existing first calculation.

## Required skills

### 1. Apply a custom cell background color by hexadecimal value

Skill ID: `30e3e107-1cfb-46ee-a755-2cd080d7ba6a.skill-03`

Procedure:

1. Select the target cell or merged range, for example A1:C1 via its merged anchor cell A1.
2. Open the background/fill color dropdown next to the paint-bucket control and choose Custom Color.
3. Select the hexadecimal input, replace its value with an exact color such as `0000ff`, and press Enter to apply the fill.

Efficiency tip: Enter an exact hexadecimal color value in the custom-color dialog instead of approximating the shade from the palette.

Source task: `30e3e107-1cfb-46ee-a755-2cd080d7ba6a`

Source instruction: Please create a new sheet. Keep its sheet name as "Sheet2". Merge cells A1:C1 in the new sheet and write "Demographic Profile" with blue (#0000ff) fill and bold white text. Then I want to create three pivot tables to show the percentage of Sex, Civil Status, and Highest Educational Attainment. They should be stacked one by one in Sheet2, each separated with a blank line.

Directly referenced source actions:

- Action 7: <code>`CLICK` cell A1</code>
- Action 8: <code>`CLICK` arrow next to paint button dropdown</code>
- Action 9: <code>`CLICK` Custom color</code>
- Action 10: <code>`DOUBLE_CLICK` on text inside Hex # box</code>
- Action 11: <code>`TYPING` 0000ff</code>
- Action 12: <code>`PRESS` enter</code>

### 2. AutoFill a formula down by double-clicking the fill handle

Skill ID: `d681960f-7bc3-4286-9913-a8812ba3261a.skill-02`

Procedure:

1. Select the cell that contains the formula to propagate.
2. Point to the small square at the selected cell's bottom-right corner (the fill handle).
3. Double-click the fill handle. Calc copies the formula downward through the rows indicated by the neighboring contiguous data, adjusting relative references for each destination row.

Efficiency tip: Double-clicking the fill handle is faster and less error-prone than dragging across a long list, because Calc extends the formula through the adjacent contiguous data region.

Source task: `d681960f-7bc3-4286-9913-a8812ba3261a`

Source instruction: According to the scale table shown above, calculate and give each student a grade in the table below

Directly referenced source actions:

- Action 3: <code>`CLICK` F10</code>
- Action 4: <code>`DOUBLE_CLICK` bottom right corner of the cell</code>

## Initial state preview

### Supply Plan

![Supply_Plan.png](artifact/previews/Supply_Plan.png)

## Operator guide

### Existing operation-intent guide

#### Demonstration 1

- Skill: `30e3e107-1cfb-46ee-a755-2cd080d7ba6a.skill-03`
- Intent: Apply the requested exact custom background color to the title cell A1.
- Efficiency: Enter the exact hexadecimal value in the custom color control rather than choosing an approximate palette swatch.
- Visible success: A1, containing "Community Garden Supply Plan," visibly displays the specified custom fill color #2F6B4F.

#### Demonstration 2

- Skill: `d681960f-7bc3-4286-9913-a8812ba3261a.skill-02`
- Intent: Propagate the seeded Line Cost formula from D4 through every populated supply-item row.
- Efficiency: Use the formula cell's fill handle and double-click it so Calc follows the neighboring contiguous item data instead of manually dragging to the last row.
- Visible success: D4:D27 contain calculated currency amounts, with no blank Line Cost cells alongside populated rows 4:27.

Recording start: The Supply Plan sheet is open with unfilled title cell A1, populated input columns A:C for rows 4:27, formula only in D4, and blank D5:D27.

Recording end: The title cell A1 has fill #2F6B4F, and Line Cost is calculated in D4:D27 using the propagated relative-reference formula; no unrelated summaries or sheets have been added.

Allowed variation: The expert may use equivalent Calc menus, toolbar controls, keyboard navigation, or selection methods, provided the exact title color and the formula-filled line-cost range are visibly achieved.

### 中文详细参考方案

> 以下是一个可以参考的操作 guide。标注者可以根据实际 LibreOffice 界面采用等价操作。

在“Supply Plan”工作表中，为标题单元格 A1 设置精确的 #2F6B4F 背景色，并利用 D4 中已有的行成本公式快速填充全部供应项目行。

#### 启动后的初始状态检查

- 确认当前打开的工作表名称为“Supply Plan”。
- 确认 A1 显示“Community Garden Supply Plan”，字体较大且加粗，但尚未填充目标背景色。
- 确认第 3 行是表头，A4:C27 均为连续的供应项目、数量和 Unit Cost 数据。
- 确认 D4 已有公式 =B4*C4，且 D5:D27 为空；C 列和 D 列应显示为两位小数的货币格式。

#### 第 1 步：为计划标题应用指定背景色

1. 单击标题单元格 A1；如果标题跨多个合并单元格显示，只需选择合并区域的左上角锚点 A1。
2. 在工具栏中找到油漆桶形状的“背景颜色/填充颜色”控件，打开其下拉菜单并选择“自定义颜色”。
3. 在自定义颜色对话框的十六进制颜色输入框中，将现有值替换为 `2F6B4F`，然后按 Enter 应用颜色。

- 对应 skills：`30e3e107-1cfb-46ee-a755-2cd080d7ba6a.skill-03`
- 高效操作：在自定义颜色框中直接输入十六进制值，可避免从调色板中凭目测选择近似颜色。
- 完成标志：A1 中的“Community Garden Supply Plan”保持可见，并显示精确的深绿色背景 #2F6B4F。

#### 第 2 步：向下自动填充 Line Cost 公式

1. 单击 D4，确认该单元格是已有的 Line Cost 公式单元格，公式栏应显示 `=B4*C4`。
2. 保持 D4 处于选中状态，将指针移到所选单元格右下角的小方块，即填充柄。
3. 双击填充柄。Calc 会沿相邻连续数据区域向下复制公式，直到第 27 行，并自动调整每行的相对引用。
4. 如有需要，单击 D5 和较靠后的一个单元格（例如 D27）进行抽查：它们应分别按本行数量与单价计算。

- 对应 skills：`d681960f-7bc3-4286-9913-a8812ba3261a.skill-02`
- 高效操作：双击填充柄会依据相邻 A:C 列连续的数据自动延伸到最后一个项目行，比手动拖动更快且不易漏行。
- 完成标志：D4:D27 都显示货币金额；D5:D27 不再为空，并且每一行的 Line Cost 对应本行的 Units 与 Unit Cost。

#### 第 3 步：完成最终核对

1. 检查 A1 的背景色和标题文字，确认颜色修改仅应用于标题区域。
2. 检查 D4:D27 的首行、中间行和末行，确认均有金额且仍为货币格式、保留两位小数。
3. 确认没有添加总计行、新工作表、图表、数据透视表或其他额外内容。

- 对应 skills：无；这是准备或检查步骤。
- 高效操作：使用名称框或直接滚动查看首尾行，可快速确认完整范围而无需逐行检查。
- 完成标志：工作表只完成标题配色和全部 24 个供应项目行的 Line Cost 计算，版面中没有无关新增对象。

#### 最终结果检查

- 确认工作簿仍只有“Supply Plan”一个工作表，未新增汇总行、图表、数据透视表或其他无关内容。
- 查看 A1：标题仍为“Community Garden Supply Plan”，且单元格背景为深绿色 #2F6B4F。
- 查看 D4:D27：每个有供应项目的行都有货币格式的 Line Cost 结果，D5:D27 不再有空白单元格。
- 抽查 D5 或 D27，在输入行中确认公式使用本行相对引用，例如 D5 为 =B5*C5、D27 为 =B27*C27。

## Source-task similarity review

| Measure | Maximum | Most similar source task |
| --- | ---: | --- |
| Lexical sequence similarity | 0.388406 | abed40dc-063f-4598-8ba5-9fe749c0615d |
| Semantic cosine similarity | 0.426272 | 01b269ae-2111-4a07-81fd-3fcd711993b0 |

Similarity scores are reviewer aids, not automatic acceptance thresholds. Inspect the contributing source tasks and their complete ordered actions below.

### Source task `30e3e107-1cfb-46ee-a755-2cd080d7ba6a`

Original instruction:

> Please create a new sheet. Keep its sheet name as "Sheet2". Merge cells A1:C1 in the new sheet and write "Demographic Profile" with blue (#0000ff) fill and bold white text. Then I want to create three pivot tables to show the percentage of Sex, Civil Status, and Highest Educational Attainment. They should be stacked one by one in Sheet2, each separated with a blank line.

Required skills derived from this source task:

- **Apply a custom cell background color by hexadecimal value** — `30e3e107-1cfb-46ee-a755-2cd080d7ba6a.skill-03`

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
| 7 | <strong>★ Apply a custom cell background color by hexadecimal value</strong><br><code>30e3e107-1cfb-46ee-a755-2cd080d7ba6a.skill-03</code> | <strong><code>`CLICK` cell A1</code></strong> |
| 8 | <strong>★ Apply a custom cell background color by hexadecimal value</strong><br><code>30e3e107-1cfb-46ee-a755-2cd080d7ba6a.skill-03</code> | <strong><code>`CLICK` arrow next to paint button dropdown</code></strong> |
| 9 | <strong>★ Apply a custom cell background color by hexadecimal value</strong><br><code>30e3e107-1cfb-46ee-a755-2cd080d7ba6a.skill-03</code> | <strong><code>`CLICK` Custom color</code></strong> |
| 10 | <strong>★ Apply a custom cell background color by hexadecimal value</strong><br><code>30e3e107-1cfb-46ee-a755-2cd080d7ba6a.skill-03</code> | <strong><code>`DOUBLE_CLICK` on text inside Hex # box</code></strong> |
| 11 | <strong>★ Apply a custom cell background color by hexadecimal value</strong><br><code>30e3e107-1cfb-46ee-a755-2cd080d7ba6a.skill-03</code> | <strong><code>`TYPING` 0000ff</code></strong> |
| 12 | <strong>★ Apply a custom cell background color by hexadecimal value</strong><br><code>30e3e107-1cfb-46ee-a755-2cd080d7ba6a.skill-03</code> | <strong><code>`PRESS` enter</code></strong> |
| 13 |  | <code>`CLICK` font color arrow icon, which is to left of bucket</code> |
| 14 |  | <code>`CLICK` top right color in the color palette (white)</code> |
| 15 |  | <code>`CLICK` bold icon</code> |
| 16 |  | <code>`CLICK` Sheet1</code> |
| 17 |  | <code>`CLICK` column B grey cell</code> |
| 18 |  | <code>`CLICK` pivot table icon</code> |
| 19 |  | <code>`PRESS` enter</code> |
| 20 |  | <code>`MOVE_TO` &#x27;Sex&#x27; in available fields</code> |
| 21 |  | <code>`DRAG_TO` box in row fields</code> |
| 22 |  | <code>`MOVE_TO` &#x27;Sex&#x27; in available fields</code> |
| 23 |  | <code>`DRAG_TO` box in data fields</code> |
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
| 40 |  | <code>`MOVE_TO` &#x27;Civil Status&#x27; in available fields</code> |
| 41 |  | <code>`DRAG_TO` box in row fields</code> |
| 42 |  | <code>`MOVE_TO` &#x27;Civil Status&#x27; in available fields</code> |
| 43 |  | <code>`DRAG_TO` box in data fields</code> |
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
| 60 |  | <code>`MOVE_TO` &#x27;Highest Educational Attainment&#x27; in available fields</code> |
| 61 |  | <code>`DRAG_TO` box in row fields</code> |
| 62 |  | <code>`MOVE_TO` &#x27;Highest Educational Attainment&#x27; in available fields</code> |
| 63 |  | <code>`DRAG_TO` box in data fields</code> |
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

### Source task `d681960f-7bc3-4286-9913-a8812ba3261a`

Original instruction:

> According to the scale table shown above, calculate and give each student a grade in the table below

Required skills derived from this source task:

- **AutoFill a formula down by double-clicking the fill handle** — `d681960f-7bc3-4286-9913-a8812ba3261a.skill-02`

Complete ordered single-action sequence:

| Action | Related required skill | Original single action |
| ---: | --- | --- |
| 0 |  | <code>`CLICK` F10</code> |
| 1 |  | <code>`TYPING` &#x27;=VLOOKUP(E10, $D$2:$E$7, 2, true)&#x27;</code> |
| 2 |  | <code>`PRESS` Enter</code> |
| 3 | <strong>★ AutoFill a formula down by double-clicking the fill handle</strong><br><code>d681960f-7bc3-4286-9913-a8812ba3261a.skill-02</code> | <strong><code>`CLICK` F10</code></strong> |
| 4 | <strong>★ AutoFill a formula down by double-clicking the fill handle</strong><br><code>d681960f-7bc3-4286-9913-a8812ba3261a.skill-02</code> | <strong><code>`DOUBLE_CLICK` bottom right corner of the cell</code></strong> |

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
