# Regional Community Grant Requests

- Reference task: `reference-task-calc-full-r01-001`
- Application: `libreoffice_calc`
- Review decision: `pending`

## Task instruction

Turn the Funding Plan sheet into a concise regional funding snapshot: display every Requested Funding amount as a rounded one-decimal figure in millions with a separated M suffix, then add a column chart comparing requests by region and title it "Regional Funding Requests".

## Required skills

### 1. Format values as rounded millions with a spaced unit suffix

Skill ID: `21df9241-f8d7-4509-b7f1-37e501a823f7.skill-02`

Procedure:

1. Select the cells to format, then right-click the selection and choose Format Cells.
2. Activate the format-code field and enter a custom numeric format such as `0.0,, \M`, then confirm with Enter.
3. The two trailing commas scale the displayed value by one million, `0.0` displays one decimal place, and the literal space before `\M` separates the number from the M suffix. For example, 12500000 displays as `12.5 M`.

Efficiency tip: Apply the custom format to the full intended range before opening Format Cells when possible, so the format is configured once rather than cell by cell.

Source task: `21df9241-f8d7-4509-b7f1-37e501a823f7`

Source instruction: Change the representation of column "Parameter" to show in Millions (M) in Column B and Billions (B) in Column C. The numbers should be rounded to one decimal place, and half should be rounded up. Then remember to place a white space between the digits and the unit.

Directly referenced source actions:

- Action 5: <code>`RIGHT_CLICK`</code>
- Action 6: <code>`CLICK` &#x27;Format Cells...&#x27;</code>
- Action 7: <code>`DOUBLE_CLICK` format code box</code>
- Action 8: <code>`TYPING` &#x27;0.0,, \M&#x27;</code>
- Action 9: <code>`PRESS` enter</code>

### 2. Set a chart title through the Chart elements control

Skill ID: `0326d92d-d218-48a8-9ca1-981cd6d064c7.skill-05`

Procedure:

1. Activate the chart and open Chart elements.
2. Click the title text box, type the desired title, and press Enter to apply it.
3. For example, type `Total` for one chart or `Growth` for another; use the text appropriate to the chart in a new workbook.

Efficiency tip: Edit the title immediately after creating each chart while it is active, avoiding later selection and formatting steps.

Source task: `0326d92d-d218-48a8-9ca1-981cd6d064c7`

Source instruction: Calculate the total sales in an underneath row called "Total" and display the total of each month as bars. Then calculate the month-on-month growth percentage for Feb to Jun in another row called "Growth" and show them in a line chart (Jan should be omitted in the chart as well). Set the chart titles as the two row headers respectively.

Directly referenced source actions:

- Action 18: <code>`CLICK` Chart elements</code>
- Action 19: <code>`CLICK` title text box</code>
- Action 20: <code>`TYPING` &#x27;Total&#x27;</code>
- Action 21: <code>`PRESS` enter</code>
- Action 41: <code>`CLICK` Chart elements</code>
- Action 42: <code>`CLICK` title text box</code>
- Action 43: <code>`TYPING` &#x27;Growth&#x27;</code>
- Action 44: <code>`PRESS` enter</code>

## Initial state preview

### Funding Plan

![Funding_Plan.png](artifact/previews/Funding_Plan.png)

## Operator guide

### Existing operation-intent guide

#### Demonstration 1

- Skill: `21df9241-f8d7-4509-b7f1-37e501a823f7.skill-02`
- Intent: Format all Requested Funding values to show rounded, one-decimal amounts in millions with a space before the M unit suffix.
- Efficiency: Select the entire numeric funding range before opening cell-format settings so that the custom display is applied once to all six values.
- Visible success: Each funding value in column C is displayed in a form such as 3.6 M while retaining its underlying full-dollar numeric value.

#### Demonstration 2

- Skill: `0326d92d-d218-48a8-9ca1-981cd6d064c7.skill-05`
- Intent: Give the regional funding comparison chart the title Regional Funding Requests through its chart-elements title interface.
- Efficiency: Set the title while the newly created chart is still active, using the chart-elements title control rather than returning to it later.
- Visible success: The visible chart title reads Regional Funding Requests above the chart.

Recording start: Funding Plan shows the unformatted source table with six regional records and a blank chart area; no chart is present.

Recording end: Funding Plan shows all six Requested Funding cells in rounded millions with a spaced M suffix, plus a visible regional comparison chart titled Regional Funding Requests.

Allowed variation: The expert may use an equivalent Calc chart type that clearly compares funding across regions, may place the chart anywhere in the provided blank area, and may use either a selection-first or chart-wizard workflow. The amount display must remain a one-decimal millions representation with a visibly separated M suffix.

### 中文详细参考方案

> 以下是一个可以参考的操作 guide。标注者可以根据实际 LibreOffice 界面采用等价操作。

本指南将“Funding Plan”中的六项 Requested Funding 统一显示为以百万为单位、保留一位小数且带空格 M 后缀的数值，并在右侧空白区域创建按地区比较请求资金的柱形图，最后为图表设置标题。

#### 启动后的初始状态检查

- 确认已打开工作簿，且只有名为“Funding Plan”的工作表需要处理。
- 确认 A1:C7 是连续数据表：第 1 行为表头，A 列为 Region，B 列为 Grant Theme，C 列为 Requested Funding。
- 确认 C2:C7 当前仍显示普通货币或常规完整数值，没有 M 后缀；并确认从 E2 开始有可用于放置图表的空白区域。
- 确认工作表中尚不存在图表，也没有显示“Regional Funding Requests”的图表标题。

#### 第 1 步：将请求资金显示为一位小数的百万金额

1. 在“Funding Plan”工作表中，选择 Requested Funding 的六个数据单元格 C2:C7，不要包含 C1 表头。
2. 右键单击所选区域，选择“Format Cells...”。
3. 在单元格格式对话框中进入可输入数字格式代码的位置；如有类别列表，可选择“User-defined”或自定义格式。
4. 在格式代码框中输入 `0.0,, \M`，然后按 Enter 确认并应用。该代码中的两个逗号会将显示值按百万缩放，`0.0` 保留一位小数，空格和 `\M` 会显示分隔开的 M 后缀。

- 对应 skills：`21df9241-f8d7-4509-b7f1-37e501a823f7.skill-02`
- 高效操作：先一次选中完整的 C2:C7 范围，随后只需设置一次格式，避免逐个单元格重复操作。
- 完成标志：C2:C7 的每个金额都显示为类似“3.6 M”的形式，而不是完整的美元数值；数值与 M 之间清楚可见一个空格。

#### 第 2 步：创建按地区比较请求资金的柱形图

1. 选择图表源数据：先选择 A1:A7（包括 Region 表头和六个地区），然后按住 Ctrl 再选择 C1:C7（包括 Requested Funding 表头和六个金额）。
2. 使用“Insert”菜单中的“Chart...”命令开始插入图表。
3. 在图表向导中选择柱形图或其他清晰比较各地区资金的列式图表；保留地区名称作为分类标签，并将 Requested Funding 作为数据系列。
4. 完成图表创建，将图表放在从 E2 开始的空白区域，避免遮挡 A1:C7 的源数据。

- 对应 skills：无；这是准备或检查步骤。
- 高效操作：由于 A 列和 C 列不相邻，可先选中 A1:A7，再按住 Ctrl 选中 C1:C7；这样可直接将地区作为分类标签、资金作为唯一数值系列。
- 完成标志：工作表中出现一个柱形图，横轴或分类轴显示六个 Region 名称，每个地区对应一根表示 Requested Funding 的柱。

#### 第 3 步：通过图表元素设置图表标题

1. 保持新图表处于选中或编辑状态，打开图表的“Chart elements”控件。
2. 在图表元素中选择标题文本框。
3. 输入标题 `Regional Funding Requests`，然后按 Enter 应用。

- 对应 skills：`0326d92d-d218-48a8-9ca1-981cd6d064c7.skill-05`
- 高效操作：图表刚创建后通常仍处于活动状态，此时立即设置标题，无需之后再重新选择图表。
- 完成标志：图表上方清楚显示标题“Regional Funding Requests”。

#### 第 4 步：完成最终核对

1. 检查 C2:C7：所有六个单元格均应为一位小数的百万显示，并带有与数字分开的 M。
2. 检查图表：它应比较六个地区的 Requested Funding，且没有将 Grant Theme 误作为数值系列。
3. 检查标题拼写和大小写是否恰为 `Regional Funding Requests`。

- 对应 skills：无；这是准备或检查步骤。
- 高效操作：用一次快速目视检查同时确认格式、图表分类和标题，可在结束前及时发现选择范围或标题遗漏。
- 完成标志：格式化金额和标题均可见，图表按地区显示资金比较，且源数据表没有被图表遮挡。

#### 最终结果检查

- “Funding Plan”工作表的 C2:C7 均以类似“3.6 M”的形式显示：保留一位小数，数字与 M 之间有空格；选中任一单元格时，编辑栏中的基础值仍是完整的数值而不是文本。
- 工作表中存在一个按 Region 比较 Requested Funding 的柱形图，且使用六个地区作为分类标签。
- 图表上方可见标题“Regional Funding Requests”。

## Source-task similarity review

| Measure | Maximum | Most similar source task |
| --- | ---: | --- |
| Lexical sequence similarity | 0.30273 | 0a2e43bf-b26c-4631-a966-af9dfa12c9e5 |
| Semantic cosine similarity | 0.418443 | 0326d92d-d218-48a8-9ca1-981cd6d064c7 |

Similarity scores are reviewer aids, not automatic acceptance thresholds. Inspect the contributing source tasks and their complete ordered actions below.

### Source task `0326d92d-d218-48a8-9ca1-981cd6d064c7`

Original instruction:

> Calculate the total sales in an underneath row called "Total" and display the total of each month as bars. Then calculate the month-on-month growth percentage for Feb to Jun in another row called "Growth" and show them in a line chart (Jan should be omitted in the chart as well). Set the chart titles as the two row headers respectively.

Required skills derived from this source task:

- **Set a chart title through the Chart elements control** — `0326d92d-d218-48a8-9ca1-981cd6d064c7.skill-05`

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
| 16 |  | <code>`CLICK` chart icon</code> |
| 17 |  | <code>`CLICK` Bar</code> |
| 18 | <strong>★ Set a chart title through the Chart elements control</strong><br><code>0326d92d-d218-48a8-9ca1-981cd6d064c7.skill-05</code> | <strong><code>`CLICK` Chart elements</code></strong> |
| 19 | <strong>★ Set a chart title through the Chart elements control</strong><br><code>0326d92d-d218-48a8-9ca1-981cd6d064c7.skill-05</code> | <strong><code>`CLICK` title text box</code></strong> |
| 20 | <strong>★ Set a chart title through the Chart elements control</strong><br><code>0326d92d-d218-48a8-9ca1-981cd6d064c7.skill-05</code> | <strong><code>`TYPING` &#x27;Total&#x27;</code></strong> |
| 21 | <strong>★ Set a chart title through the Chart elements control</strong><br><code>0326d92d-d218-48a8-9ca1-981cd6d064c7.skill-05</code> | <strong><code>`PRESS` enter</code></strong> |
| 22 |  | <code>`CLICK` cell A13</code> |
| 23 |  | <code>`TYPING` &#x27;Growth&#x27;</code> |
| 24 |  | <code>`CLICK` cell C13</code> |
| 25 |  | <code>`TYPING` &#x27;=(C12-B12)/B12&#x27;</code> |
| 26 |  | <code>`PRESS` enter</code> |
| 27 |  | <code>`CLICK` cell C13</code> |
| 28 |  | <code>`MOVE_TO bottom right corner of the cell C13`</code> |
| 29 |  | <code>`DRAG_TO` bottom right corner of the cell G13</code> |
| 30 |  | <code>`MOVE_TO` middle of cell C1</code> |
| 31 |  | <code>`DRAG_TO` middle of cell G1</code> |
| 32 |  | <code>`KEY_DOWN` ctrl</code> |
| 33 |  | <code>`CLICK` cell C13</code> |
| 34 |  | <code>`KEY_UP` ctrl</code> |
| 35 |  | <code>`KEY_DOWN` shift</code> |
| 36 |  | <code>`CLICK` cell G13</code> |
| 37 |  | <code>`KEY_UP` shift</code> |
| 38 |  | <code>`CLICK` chart icon</code> |
| 39 |  | <code>`CLICK` Line</code> |
| 40 |  | <code>`CLICK` icon representing lines only (3rd from the right)</code> |
| 41 | <strong>★ Set a chart title through the Chart elements control</strong><br><code>0326d92d-d218-48a8-9ca1-981cd6d064c7.skill-05</code> | <strong><code>`CLICK` Chart elements</code></strong> |
| 42 | <strong>★ Set a chart title through the Chart elements control</strong><br><code>0326d92d-d218-48a8-9ca1-981cd6d064c7.skill-05</code> | <strong><code>`CLICK` title text box</code></strong> |
| 43 | <strong>★ Set a chart title through the Chart elements control</strong><br><code>0326d92d-d218-48a8-9ca1-981cd6d064c7.skill-05</code> | <strong><code>`TYPING` &#x27;Growth&#x27;</code></strong> |
| 44 | <strong>★ Set a chart title through the Chart elements control</strong><br><code>0326d92d-d218-48a8-9ca1-981cd6d064c7.skill-05</code> | <strong><code>`PRESS` enter</code></strong> |

### Source task `21df9241-f8d7-4509-b7f1-37e501a823f7`

Original instruction:

> Change the representation of column "Parameter" to show in Millions (M) in Column B and Billions (B) in Column C. The numbers should be rounded to one decimal place, and half should be rounded up. Then remember to place a white space between the digits and the unit.

Required skills derived from this source task:

- **Format values as rounded millions with a spaced unit suffix** — `21df9241-f8d7-4509-b7f1-37e501a823f7.skill-02`

Complete ordered single-action sequence:

| Action | Related required skill | Original single action |
| ---: | --- | --- |
| 0 |  | <code>`CLICK A2</code> |
| 1 |  | <code>`DRAG_TO A8</code> |
| 2 |  | <code>`HOTKEY` CTRL-C</code> |
| 3 |  | <code>`CLICK` B2</code> |
| 4 |  | <code>`HOTKEY` CTRL-V</code> |
| 5 | <strong>★ Format values as rounded millions with a spaced unit suffix</strong><br><code>21df9241-f8d7-4509-b7f1-37e501a823f7.skill-02</code> | <strong><code>`RIGHT_CLICK`</code></strong> |
| 6 | <strong>★ Format values as rounded millions with a spaced unit suffix</strong><br><code>21df9241-f8d7-4509-b7f1-37e501a823f7.skill-02</code> | <strong><code>`CLICK` &#x27;Format Cells...&#x27;</code></strong> |
| 7 | <strong>★ Format values as rounded millions with a spaced unit suffix</strong><br><code>21df9241-f8d7-4509-b7f1-37e501a823f7.skill-02</code> | <strong><code>`DOUBLE_CLICK` format code box</code></strong> |
| 8 | <strong>★ Format values as rounded millions with a spaced unit suffix</strong><br><code>21df9241-f8d7-4509-b7f1-37e501a823f7.skill-02</code> | <strong><code>`TYPING` &#x27;0.0,, \M&#x27;</code></strong> |
| 9 | <strong>★ Format values as rounded millions with a spaced unit suffix</strong><br><code>21df9241-f8d7-4509-b7f1-37e501a823f7.skill-02</code> | <strong><code>`PRESS` enter</code></strong> |
| 10 |  | <code>`CLICK` C2</code> |
| 11 |  | <code>`HOTKEY` CTRL-V</code> |
| 12 |  | <code>`RIGHT_CLICK`</code> |
| 13 |  | <code>`CLICK` &#x27;Format Cells...&#x27;</code> |
| 14 |  | <code>`DOUBLE_CLICK` format code box</code> |
| 15 |  | <code>`TYPING` &#x27;0.0,,, \B&#x27;</code> |
| 16 |  | <code>`PRESS` enter</code> |

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
