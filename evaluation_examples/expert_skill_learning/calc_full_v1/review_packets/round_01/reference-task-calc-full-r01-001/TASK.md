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

本指南将 `Funding Plan` 的六笔 Requested Funding 金额统一显示为以百万为单位的一位小数，并在右侧空白区域创建按 Region 比较请求金额的柱形图，再设置标题为 `Regional Funding Requests`。

#### 启动后的初始状态检查

- 确认当前打开的工作表标签是 `Funding Plan`，并能看到 A1:C7 的连续数据表。
- 确认第 1 行包含 `Region`、`Grant Theme` 和 `Requested Funding` 标题，C2:C7 目前仍显示为普通金额或未缩放的数值，而不是带 `M` 的数值。
- 确认从 E2 开始的区域没有现成图表，足以放置新图表。

#### 第 1 步：将请求金额显示为一位小数的百万数

1. 在 `Funding Plan` 中选中 Requested Funding 的数据区域 C2:C7；不要选中标题 C1。
2. 在选区上右键，选择 `Format Cells...`。
3. 在数字格式设置中找到 `Format Code` 输入框，输入 `0.0,, \M`，然后按 `Enter` 确认。该格式中的两个逗号会按百万缩放，`0.0` 保留一位小数，反斜杠后的 `M` 会作为文字显示，前面的空格会使单位与数字分开。

- 对应 skills：`21df9241-f8d7-4509-b7f1-37e501a823f7.skill-02`
- 高效操作：先一次选中全部六个金额单元格，只需设置一次格式即可，避免逐格处理。
- 完成标志：C2:C7 中的六个单元格都显示为类似 `3.6 M` 的形式：数字只有一位小数，数字与 `M` 之间有可见空格；单元格仍是数值而非文本。

#### 第 2 步：创建按地区比较请求金额的柱形图

1. 先选中 A1:A7，其中包括 `Region` 表头和六个地区名称；然后按住 `Ctrl`，再选中 C1:C7，其中包括 `Requested Funding` 表头和六个已格式化的金额。
2. 打开 `Insert` > `Chart...`。
3. 在图表向导中选择一种 column 风格的图表，用柱形清晰比较各地区的请求金额；完成向导以插入图表。
4. 图表生成后，预期横轴会显示六个 Region，柱形高度对应 Requested Funding。如果已经如此显示，无需调整。
5. 如果横轴显示的不是 Region，或图中没有正确的请求金额系列，双击图表进入编辑状态，打开 `Format` > `Data Ranges`。在 `Data Series` 中将 `Categories` 指向 `Funding Plan` 的 A2:A7，并将该数值系列的 `Y-Values` 指向 C2:C7；确认后退出编辑状态。

- 对应 skills：无；这是准备或检查步骤。
- 高效操作：选择包含表头的 Region 与 Requested Funding 两列，可让 Calc 更容易把表头识别为名称、把 Region 识别为类别标签。
- 完成标志：工作表出现柱形比较图，六个 Region 作为类别标签，图中有一组表示 Requested Funding 的柱形。

#### 第 3 步：通过图表元素设置图表标题

1. 图表仍处于活动状态时，使用 `Chart elements` 打开图表元素控制。
2. 点击标题文字框，输入 `Regional Funding Requests`，然后按 `Enter` 应用。
3. 预期标题会显示在图表上方；如果标题没有出现或文字仍不正确，再次激活图表并打开 `Chart elements`，选择标题文字框后重新输入完全相同的 `Regional Funding Requests` 并按 `Enter`。

- 对应 skills：`0326d92d-d218-48a8-9ca1-981cd6d064c7.skill-05`
- 高效操作：新图表保持活动状态时立即设置标题，省去之后重新选中和进入图表编辑模式的步骤。
- 完成标志：图表上方可见完整标题 `Regional Funding Requests`。

#### 第 4 步：整理图表位置并核对结果

1. 查看图表是否位于从 E2 开始的空白区域，并且没有遮住 A1:C7 的源数据。如果已经位于该区域且源数据完整可见，无需调整。
2. 如果图表遮住了源数据或不在右侧空白区，单击图表的外边框以选中整个图表对象，再拖动整个图表，使其左上角靠近 E2，并保持 A1:C7 可见。
3. 最后查看 C2:C7、图表类别标签、柱形和标题，确认它们均仍可见。

- 对应 skills：无；这是准备或检查步骤。
- 高效操作：只在图表位置影响源数据可见性时移动图表，避免无意义的重复调整。
- 完成标志：数据表在左侧完整可见，图表位于右侧空白区域，标题、地区类别和柱形比较均清楚可读。

#### 最终结果检查

- `Funding Plan` 工作表仍保留原有的 A1:C7 数据表，且 C2:C7 的底层数据仍是数值；显示内容均为一位小数、空格和 `M` 后缀，例如 `3.6 M`，而不是完整美元金额。
- 工作表中有一张清晰比较六个 Region 请求金额的柱形图；Region 是横轴类别，Requested Funding 是唯一的数值系列。
- 图表标题在图表上方清晰显示为 `Regional Funding Requests`，且源数据表没有被图表遮挡。

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
