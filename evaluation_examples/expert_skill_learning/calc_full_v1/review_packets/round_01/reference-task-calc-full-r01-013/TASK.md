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

本操作先使用“Route Snapshot”中的预汇总区域创建按花园分区比较 Delivered Units 的条形图，再返回“Deliveries”并打开其数据源的 Pivot Table 布局对话框。最终保留图表和布局对话框，但不创建 Pivot Table 输出。

#### 启动后的初始状态检查

- 确认工作簿当前只有“Deliveries”和“Route Snapshot”两个普通数据工作表，且尚未插入图表或 Pivot Table。
- 确认“Deliveries”中 A1:G37 是包含字段标题的连续交付记录区域；“Route Snapshot”中 A1:B7 是包含标题的连续汇总区域。
- 如果当前活动单元格为 Deliveries!A1，这是预期的初始状态；不要先创建新工作表或修改现有数据。

#### 第 1 步：选择路线汇总图表数据

1. 单击底部工作表标签“Route Snapshot”切换到路线汇总表。
2. 选中完整图表源区域 A1:B7。可从 A1 拖动到 B7，或先单击名称框、输入 A1:B7 后按 Enter。选区必须包括“Garden Zone”和“Delivered Units”标题行。
3. 确认选区中第一列是 Garden Zone 标签，第二列是 Delivered Units 数值。

- 对应 skills：无；这是准备或检查步骤。
- 高效操作：一次选中 A1:B7（包括标题）可让 Calc 同时识别分类标签和数值系列，避免分别指定标签范围与数值范围。
- 完成标志：“Route Snapshot”中 A1:B7 被高亮选中，且可见两列标题 Garden Zone 与 Delivered Units。

#### 第 2 步：插入 Delivered Units 条形图

1. 在保持 A1:B7 选中的状态下，使用工具栏的图表按钮，或选择“插入”>“图表”。
2. 在图表向导的图表类型中选择“Bar”。如有方向选项，保持条形图的默认方向即可。
3. 检查预览：应按 Garden Zone 显示类别，并以 Delivered Units 的数值显示条形。
4. 完成图表向导以插入图表。不要更改源数据单元格。

- 对应 skills：`0326d92d-d218-48a8-9ca1-981cd6d064c7.skill-04`
- 高效操作：在已选好数据时直接选择 Bar 类型，通常能保留正确的数据区域；不要取消图表向导后重新选择数据。
- 完成标志：“Route Snapshot”工作表上出现一个可见的条形图，含花园分区类别及对应 Delivered Units 条形。

#### 第 3 步：选择交付记录数据源

1. 单击工作表标签“Deliveries”返回交付记录表。
2. 选中完整数据源 A1:G37，包括第 1 行字段标题和所有 36 条记录。可单击 A1 后拖动至 G37，或在名称框中输入 A1:G37 并按 Enter。
3. 核对选区包含 Delivery ID、Delivery Date、Garden Zone、Supply Category、Item、Units Delivered 和 Delivery Cost 七个字段。

- 对应 skills：无；这是准备或检查步骤。
- 高效操作：从连续数据块内任意单元格开始选择时，Calc 通常可以自动识别整个 A1:G37 数据区域；保留标题行有助于正确识别字段。
- 完成标志：Deliveries!A1:G37 被选中，选区内没有遗漏标题行、数据列或记录行。

#### 第 4 步：打开 Deliveries 的 Pivot Table 布局

1. 保持 Deliveries!A1:G37 处于选中状态，单击 Pivot Table 工具栏图标；也可使用“数据”菜单中用于插入或创建 Pivot Table 的命令。
2. 如果 Calc 先显示用于确认源数据范围的提示或对话框，确认显示的是 Deliveries 的 A1:G37 数据范围，然后接受该推断范围（例如按 Enter 或确认）。
3. 等待 Pivot Table Layout 对话框打开。此时不要将 Garden Zone、Units Delivered 或其他字段拖入布局区域，也不要确认创建结果。
4. 保留 Pivot Table Layout 对话框打开，以便数据已准备好进行 garden-zone 分析但尚未输出 Pivot Table。

- 对应 skills：`30e3e107-1cfb-46ee-a755-2cd080d7ba6a.skill-06`
- 高效操作：选中完整连续区域后立即打开 Pivot Table，可直接接受 Calc 推断的数据源，无需手动重建范围。
- 完成标志：Pivot Table Layout 对话框处于打开状态，字段来自 Deliveries 数据源；工作簿中尚未生成 Pivot Table 输出。

#### 最终结果检查

- 在“Route Snapshot”工作表中可以看到已插入的条形图，分类为各 Garden Zone，数据系列表示 Delivered Units。
- “Pivot Table Layout”对话框仍保持打开状态，且其数据源对应 Deliveries 工作表的 A1:G37 连续记录区域。
- 未确认或生成任何数据透视表输出；工作簿中不应出现新的透视表结果工作表或透视表结果区域。

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
