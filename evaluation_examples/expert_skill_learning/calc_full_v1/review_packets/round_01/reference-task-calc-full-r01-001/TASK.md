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

本任务在 `Funding Plan` 工作表完成两项整理：将六条 `Requested Funding` 记录仅以“百万、保留一位小数、M 前有空格”的显示格式呈现；随后创建一个按 Region 比较请求金额的柱形图，并将标题设为 `Regional Funding Requests`。

#### 启动后的初始状态检查

- 确认当前工作簿只有名为 `Funding Plan` 的工作表，并切换到该表。
- 确认源数据位于 A1:C7：第 1 行是标题行，A 列为 `Region`，B 列为 `Grant Theme`，C 列为 `Requested Funding`。
- 确认 C2:C7 目前显示为普通数值或货币金额，尚未带有 `M` 后缀；并确认从 E2 开始有空白区域可放置图表。
- 确认工作表上尚未存在区域资金比较图，且没有显示 `Regional Funding Requests` 的图表标题。

#### 第 1 步：将请求金额显示为带空格 M 后缀的百万数

1. 在 `Funding Plan` 中选择 C2:C7；不要包含 C1 标题单元格。
2. 右键单击所选区域，选择 `Format Cells...`。
3. 在打开的对话框中切换到 `Numbers` 选项卡。
4. 找到格式代码输入区域，将格式代码设为 `0.0,, \M`，然后按 `Enter` 或确认对话框。
5. 该代码中的两个逗号会将显示值缩放为百万，`0.0` 保留一位小数，反斜杠后的 `M` 作为文字单位显示，前面的空格使单位与数字分开。

- 对应 skills：`21df9241-f8d7-4509-b7f1-37e501a823f7.skill-02`
- 高效操作：先一次选中全部六个金额单元格，能避免逐个单元格重复设置格式。
- 完成标志：C2:C7 中每个金额都显示为类似 `3.6 M` 的形式，均有一位小数且 `M` 前存在可见空格。

#### 第 2 步：创建按区域比较请求金额的柱形图

1. 先选择 A1:A7，其中包括 `Region` 标题和六个区域名称。
2. 按住 `Ctrl`，再选择 C1:C7，其中包括 `Requested Funding` 标题和六个金额。
3. 使用 `Insert` > `Chart...` 开始创建图表。
4. 在图表设置界面选择柱形的列式图表类型；确保区域名称用于分类轴，`Requested Funding` 作为数值系列。若设置界面提供标签选项，保留“第一行作为标签”和“第一列作为标签”的对应设置。
5. 完成图表创建，并将图表放在从 E2 开始的空白区域。

- 对应 skills：无；这是准备或检查步骤。
- 高效操作：使用 `Ctrl` 选择不相邻的 Region 与金额两列，可避免把中间的 `Grant Theme` 文本列作为图表数据。
- 完成标志：工作表空白区域中出现柱形图，每个 Region 对应一个柱，图表反映 C 列的 Requested Funding 金额。

#### 第 3 步：通过图表元素设置图表标题

1. 保持新建图表处于活动状态；如图表未处于编辑状态，双击图表以激活其编辑控件。
2. 打开 `Chart elements`。
3. 点击标题文本框，输入 `Regional Funding Requests`，然后按 `Enter` 应用。
4. 单击图表外的空白工作表区域以结束图表编辑，同时保留图表。

- 对应 skills：`0326d92d-d218-48a8-9ca1-981cd6d064c7.skill-05`
- 高效操作：图表刚创建完成时通常仍处于活动状态，立即设置标题可免去之后重新选中并进入编辑状态。
- 完成标志：图表上方可见且完整显示标题 `Regional Funding Requests`。

#### 第 4 步：核对完成结果并保存

1. 检查 C2:C7，确认六个单元格都使用百万显示格式，而不是只格式化了部分记录。
2. 检查图表分类标签来自 A 列 Region，图中没有把 `Grant Theme` 当作额外的数据系列。
3. 检查标题文字精确为 `Regional Funding Requests`，并确认图表没有遮挡源表数据。
4. 保存工作簿。

- 对应 skills：无；这是准备或检查步骤。
- 高效操作：最后同时检查数值显示、分类标签和标题，可在保存前一次发现范围选择或格式遗漏。
- 完成标志：`Funding Plan` 同时保留完整源表、六个带 `M` 的金额显示，以及标题正确的区域资金柱形比较图。

#### 最终结果检查

- 在 `Funding Plan` 中查看 C2:C7：六个 `Requested Funding` 值均显示为一位小数、数字与 `M` 之间有空格的形式，例如 `3.6 M`；不应显示完整的美元金额。
- 确认工作表上存在按 Region 比较 Requested Funding 的柱形图，且图表可见标题为 `Regional Funding Requests`。
- 单击 C 列中的任一金额并查看编辑栏（或公式输入行）：底层应仍是完整的数值金额，而不是文本 `M` 值。

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
