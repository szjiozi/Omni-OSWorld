# Garden Supply Delivery Review

- Reference task: `reference-task-calc-full-r01-013`
- Application: `libreoffice_calc`
- Review decision: `pending`

## Task instruction

Prepare the garden supply delivery review by creating a bar chart that compares delivered units across the garden zones in the Route Snapshot sheet, then open the Pivot Table layout for the Deliveries records so the delivery data is ready for a garden-zone analysis. Leave the Pivot Table layout open rather than creating its output.

## Required skills

### 1. Open the Pivot Table layout from a selected data range

Skill ID: `30e3e107-1cfb-46ee-a755-2cd080d7ba6a.skill-06`

Procedure:

1. Switch to the worksheet containing the source data and select the relevant source range or column; for example, click a column header to select that column.
2. Click the Pivot Table toolbar icon.
3. Accept the inferred source selection, for example by pressing Enter, to open the Pivot Table layout dialog.

Efficiency tip: Select the intended source column before invoking Pivot Table so Calc can infer the source selection immediately.

Source task: `30e3e107-1cfb-46ee-a755-2cd080d7ba6a`

Source instruction: Please create a new sheet. Keep its sheet name as "Sheet2". Merge cells A1:C1 in the new sheet and write "Demographic Profile" with blue (#0000ff) fill and bold white text. Then I want to create three pivot tables to show the percentage of Sex, Civil Status, and Highest Educational Attainment. They should be stacked one by one in Sheet2, each separated with a blank line.

Directly referenced source actions:

- Action 16: <code>`CLICK` Sheet1</code>
- Action 17: <code>`CLICK` column B grey cell</code>
- Action 18: <code>`CLICK` pivot table icon</code>
- Action 19: <code>`PRESS` enter</code>
- Action 36: <code>`CLICK` Sheet1</code>
- Action 37: <code>`CLICK` column C grey cell</code>
- Action 38: <code>`CLICK` pivot table icon</code>
- Action 39: <code>`PRESS` enter</code>
- Action 56: <code>`CLICK` Sheet1</code>
- Action 57: <code>`CLICK` column D grey cell</code>
- Action 58: <code>`CLICK` pivot table icon</code>
- Action 59: <code>`PRESS` enter</code>

### 2. Insert a bar chart from the selected spreadsheet range

Skill ID: `0326d92d-d218-48a8-9ca1-981cd6d064c7.skill-04`

Procedure:

1. With the chart source ranges selected, click the chart icon in the spreadsheet interface.
2. Choose the Bar chart type to create a bar chart from the selected labels and values.

Efficiency tip: Select the intended source ranges first, then choose the chart type directly from the chart control so the chart is created with the correct data and type in one pass.

Source task: `0326d92d-d218-48a8-9ca1-981cd6d064c7`

Source instruction: Calculate the total sales in an underneath row called "Total" and display the total of each month as bars. Then calculate the month-on-month growth percentage for Feb to Jun in another row called "Growth" and show them in a line chart (Jan should be omitted in the chart as well). Set the chart titles as the two row headers respectively.

Directly referenced source actions:

- Action 16: <code>`CLICK` chart icon</code>
- Action 17: <code>`CLICK` Bar</code>

## Initial state preview

### Deliveries

![Deliveries.png](artifact/previews/Deliveries.png)

### Route Snapshot

![Route_Snapshot.png](artifact/previews/Route_Snapshot.png)

## Operator guide

### Existing operation-intent guide

#### Demonstration 1

- Skill: `30e3e107-1cfb-46ee-a755-2cd080d7ba6a.skill-06`
- Intent: Open the Pivot Table layout using the selected delivery-record source range, ready for a garden-zone delivery analysis.
- Efficiency: Use the contiguous data block on Deliveries so Calc can infer the full source immediately; confirm the inferred range rather than manually rebuilding it.
- Visible success: The Calc Pivot Table Layout dialog is open and its source corresponds to the Deliveries data range.

#### Demonstration 2

- Skill: `0326d92d-d218-48a8-9ca1-981cd6d064c7.skill-04`
- Intent: Create a bar chart that compares delivered units across garden zones from the Route Snapshot summary.
- Efficiency: Select both columns of the compact Route Snapshot range, including headers, before launching chart creation so zone labels and delivered-unit values are detected together.
- Visible success: A bar chart is visibly inserted on Route Snapshot, with garden-zone categories and bars representing Delivered Units.

Recording start: The workbook is open on Deliveries with only the two ordinary data sheets and no charts or Pivot Tables.

Recording end: A bar chart based on Route Snapshot is visible in the workbook, and the Pivot Table Layout dialog for Deliveries is open without a Pivot Table output having been created.

Allowed variation: The demonstrator may create the chart before or after opening the Pivot Table layout, may select source ranges by dragging or through the name box, and may use menus, toolbar controls, or equivalent keyboard commands. The final recording should show the completed bar chart and the Pivot Table layout dialog open for the delivery source.

### 中文详细参考方案

> 以下是一个可以参考的操作 guide。标注者可以根据实际 LibreOffice 界面采用等价操作。

本指南先利用 `Route Snapshot` 中已准备好的区域汇总数据插入横向条形图，再返回 `Deliveries`，以完整配送记录作为来源打开 Pivot Table Layout。最后停留在布局对话框，不创建 Pivot Table。

#### 启动后的初始状态检查

- 确认工作簿已打开，起始工作表为 `Deliveries`，活动单元格是 `A1`。
- 确认 `Deliveries` 的数据连续位于 `A1:G37`，首行包含字段标题，范围内部没有空行或空列。
- 确认存在 `Route Snapshot` 工作表，其图表源数据连续位于 `A1:B7`，包括 `Garden Zone` 和 `Delivered Units` 标题。
- 确认目前没有已插入的图表，也没有 Pivot Table 结果。

#### 第 1 步：选择花园区域汇总数据并启动图表创建

1. 点击工作表标签 `Route Snapshot`。
2. 选中完整图表源范围 `A1:B7`，其中应包括标题行 `Garden Zone`、`Delivered Units` 以及全部六个区域数据行。
3. 点击工具栏中的图表图标以启动图表创建；如果通过菜单启动，可使用 `Insert` > `Chart...`。

- 对应 skills：`0326d92d-d218-48a8-9ca1-981cd6d064c7.skill-04`
- 高效操作：先选中包含标题的两个完整列，图表向导通常能同时识别类别标签和数值系列，无需随后逐项指定数据。
- 完成标志：出现图表创建向导或图表编辑界面，且数据来源对应 `Route Snapshot` 的 `A1:B7`。

#### 第 2 步：创建 Delivered Units 横向条形图

1. 在图表类型选择处选择 `Bar`。
2. 检查预览：应显示以花园区域为类别的横向条形，并以 `Delivered Units` 作为数值。
3. 确认图表创建；如向导提供 `Finish`，点击 `Finish`。
4. 完成后单击工作表中的空白单元格，确保图表对象已插入并且在 `Route Snapshot` 上可见。

- 对应 skills：`0326d92d-d218-48a8-9ca1-981cd6d064c7.skill-04`
- 高效操作：在图表类型列表中直接选择 `Bar`，而不是先创建其他类型再转换，可减少后续设置。
- 完成标志：`Route Snapshot` 上可见条形图，包含花园区域类别及对应的 `Delivered Units` 条形。

#### 第 3 步：选择完整配送记录作为 Pivot Table 来源

1. 点击工作表标签 `Deliveries`。
2. 选中完整配送记录范围 `A1:G37`，包括字段标题行和全部记录。可点击 `A1` 后拖动到 `G37`，也可在名称框中输入 `A1:G37` 并按 Enter。
3. 确认选区首行包括 `Delivery ID`、`Delivery Date`、`Garden Zone`、`Supply Category`、`Item`、`Units Delivered` 和 `Delivery Cost`。

- 对应 skills：无；这是准备或检查步骤。
- 高效操作：使用完整连续数据块 `A1:G37` 作为选择，可让 Calc 自动推断所有配送字段，避免遗漏 `Garden Zone` 或 `Units Delivered` 等分析字段。
- 完成标志：`Deliveries` 中的 `A1:G37` 被高亮选中，选区覆盖全部七个字段及全部配送记录。

#### 第 4 步：打开 Deliveries 的 Pivot Table Layout

1. 在保持 `A1:G37` 被选中的情况下，打开 `Data` > `Pivot Table` > `Insert or Edit...`；也可以使用 Pivot Table 工具栏图标。
2. 如果出现来源选择或确认窗口，接受当前推断的选区 `A1:G37`，可直接按 Enter 继续。
3. 等待 Pivot Table Layout 对话框打开后停止，不要拖放字段，也不要选择输出位置或确认创建。

- 对应 skills：`30e3e107-1cfb-46ee-a755-2cd080d7ba6a.skill-06`
- 高效操作：保持数据范围处于选中状态再调用 Pivot Table 命令，随后接受 Calc 推断的来源范围即可，不必手动重新输入范围。
- 完成标志：Pivot Table Layout 对话框保持打开，其来源对应 `Deliveries` 的配送记录范围；工作簿中尚未生成 Pivot Table 输出。

#### 最终结果检查

- `Route Snapshot` 工作表中可见一个横向条形图，类别来自花园区域，条形表示 `Delivered Units`。
- 当前仍显示 `Deliveries` 数据的 Pivot Table Layout 对话框；尚未确认创建任何 Pivot Table 输出。
- 工作簿仍只有原有数据工作表，未因 Pivot Table 操作新增结果表或结果数据区域。

## Source-task similarity review

| Measure | Maximum | Most similar source task |
| --- | ---: | --- |
| Lexical sequence similarity | 0.307054 | abed40dc-063f-4598-8ba5-9fe749c0615d |
| Semantic cosine similarity | 0.47598 | 51719eea-10bc-4246-a428-ac7c433dd4b3 |

Similarity scores are reviewer aids, not automatic acceptance thresholds. Inspect the contributing source tasks and their complete ordered actions below.

### Source task `0326d92d-d218-48a8-9ca1-981cd6d064c7`

Original instruction:

> Calculate the total sales in an underneath row called "Total" and display the total of each month as bars. Then calculate the month-on-month growth percentage for Feb to Jun in another row called "Growth" and show them in a line chart (Jan should be omitted in the chart as well). Set the chart titles as the two row headers respectively.

Required skills derived from this source task:

- **Insert a bar chart from the selected spreadsheet range** — `0326d92d-d218-48a8-9ca1-981cd6d064c7.skill-04`

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
| 16 | <strong>★ Insert a bar chart from the selected spreadsheet range</strong><br><code>0326d92d-d218-48a8-9ca1-981cd6d064c7.skill-04</code> | <strong><code>`CLICK` chart icon</code></strong> |
| 17 | <strong>★ Insert a bar chart from the selected spreadsheet range</strong><br><code>0326d92d-d218-48a8-9ca1-981cd6d064c7.skill-04</code> | <strong><code>`CLICK` Bar</code></strong> |
| 18 |  | <code>`CLICK` Chart elements</code> |
| 19 |  | <code>`CLICK` title text box</code> |
| 20 |  | <code>`TYPING` &#x27;Total&#x27;</code> |
| 21 |  | <code>`PRESS` enter</code> |
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
| 41 |  | <code>`CLICK` Chart elements</code> |
| 42 |  | <code>`CLICK` title text box</code> |
| 43 |  | <code>`TYPING` &#x27;Growth&#x27;</code> |
| 44 |  | <code>`PRESS` enter</code> |

### Source task `30e3e107-1cfb-46ee-a755-2cd080d7ba6a`

Original instruction:

> Please create a new sheet. Keep its sheet name as "Sheet2". Merge cells A1:C1 in the new sheet and write "Demographic Profile" with blue (#0000ff) fill and bold white text. Then I want to create three pivot tables to show the percentage of Sex, Civil Status, and Highest Educational Attainment. They should be stacked one by one in Sheet2, each separated with a blank line.

Required skills derived from this source task:

- **Open the Pivot Table layout from a selected data range** — `30e3e107-1cfb-46ee-a755-2cd080d7ba6a.skill-06`

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
| 16 | <strong>★ Open the Pivot Table layout from a selected data range</strong><br><code>30e3e107-1cfb-46ee-a755-2cd080d7ba6a.skill-06</code> | <strong><code>`CLICK` Sheet1</code></strong> |
| 17 | <strong>★ Open the Pivot Table layout from a selected data range</strong><br><code>30e3e107-1cfb-46ee-a755-2cd080d7ba6a.skill-06</code> | <strong><code>`CLICK` column B grey cell</code></strong> |
| 18 | <strong>★ Open the Pivot Table layout from a selected data range</strong><br><code>30e3e107-1cfb-46ee-a755-2cd080d7ba6a.skill-06</code> | <strong><code>`CLICK` pivot table icon</code></strong> |
| 19 | <strong>★ Open the Pivot Table layout from a selected data range</strong><br><code>30e3e107-1cfb-46ee-a755-2cd080d7ba6a.skill-06</code> | <strong><code>`PRESS` enter</code></strong> |
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
| 36 | <strong>★ Open the Pivot Table layout from a selected data range</strong><br><code>30e3e107-1cfb-46ee-a755-2cd080d7ba6a.skill-06</code> | <strong><code>`CLICK` Sheet1</code></strong> |
| 37 | <strong>★ Open the Pivot Table layout from a selected data range</strong><br><code>30e3e107-1cfb-46ee-a755-2cd080d7ba6a.skill-06</code> | <strong><code>`CLICK` column C grey cell</code></strong> |
| 38 | <strong>★ Open the Pivot Table layout from a selected data range</strong><br><code>30e3e107-1cfb-46ee-a755-2cd080d7ba6a.skill-06</code> | <strong><code>`CLICK` pivot table icon</code></strong> |
| 39 | <strong>★ Open the Pivot Table layout from a selected data range</strong><br><code>30e3e107-1cfb-46ee-a755-2cd080d7ba6a.skill-06</code> | <strong><code>`PRESS` enter</code></strong> |
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
| 56 | <strong>★ Open the Pivot Table layout from a selected data range</strong><br><code>30e3e107-1cfb-46ee-a755-2cd080d7ba6a.skill-06</code> | <strong><code>`CLICK` Sheet1</code></strong> |
| 57 | <strong>★ Open the Pivot Table layout from a selected data range</strong><br><code>30e3e107-1cfb-46ee-a755-2cd080d7ba6a.skill-06</code> | <strong><code>`CLICK` column D grey cell</code></strong> |
| 58 | <strong>★ Open the Pivot Table layout from a selected data range</strong><br><code>30e3e107-1cfb-46ee-a755-2cd080d7ba6a.skill-06</code> | <strong><code>`CLICK` pivot table icon</code></strong> |
| 59 | <strong>★ Open the Pivot Table layout from a selected data range</strong><br><code>30e3e107-1cfb-46ee-a755-2cd080d7ba6a.skill-06</code> | <strong><code>`PRESS` enter</code></strong> |
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
