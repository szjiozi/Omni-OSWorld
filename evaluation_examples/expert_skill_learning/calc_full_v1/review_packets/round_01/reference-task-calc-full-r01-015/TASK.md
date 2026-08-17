# Fleet Fuel Planning

- Reference task: `reference-task-calc-full-r01-015`
- Application: `libreoffice_calc`
- Review decision: `pending`

## Task instruction

Complete the route fuel estimates for every dispatch record and add the overall estimated-liters total. Then rename the blank analysis worksheet to "Zone Fuel Summary" and use a Pivot Table there to report the summed estimated fuel for each zone.

## Required skills

### 1. Enter a range-total formula in a spreadsheet cell

Skill ID: `0326d92d-d218-48a8-9ca1-981cd6d064c7.skill-01`

Procedure:

1. Select the first result cell in the totals row and type a SUM formula covering the source values for that column.
2. For example, enter `=SUM(B2:B11)` and press Enter to calculate the total for column B.

Efficiency tip: Enter the formula once in the first result cell, then use the fill handle separately to propagate it rather than retyping the formula for every column.

Source task: `0326d92d-d218-48a8-9ca1-981cd6d064c7`

Source instruction: Calculate the total sales in an underneath row called "Total" and display the total of each month as bars. Then calculate the month-on-month growth percentage for Feb to Jun in another row called "Growth" and show them in a line chart (Jan should be omitted in the chart as well). Set the chart titles as the two row headers respectively.

Directly referenced source actions:

- Action 3: <code>`TYPING` &#x27;=SUM(B2:B11)&#x27;</code>
- Action 4: <code>`PRESS` enter</code>

### 2. Autofill an existing formula down a column with the fill handle

Skill ID: `4de54231-e4b5-49e3-b2ba-61a0bec721c0.skill-01`

Procedure:

1. Select the cell that already contains the formula to propagate, such as B2.
2. Double-click the small square fill handle at the cell's bottom-right corner. Calc fills the formula downward to the end of the adjacent contiguous data region, adjusting relative references for each row.
3. Repeat the same operation for another formula column when needed, for example select D2 and double-click its fill handle.

Efficiency tip: Double-clicking the fill handle is faster and less error-prone than dragging it through a long data range; verify that an adjacent column contains uninterrupted data so Calc can detect the intended last row.

Source task: `4de54231-e4b5-49e3-b2ba-61a0bec721c0`

Source instruction: I have compute the acceleration in row 2 and I want you to fill out other rows for column B and D. Next concatenate the values from columns A to D, including their headers (the pattern is "Header: cell value, ..., Header: cell value"), into a new column named "Combined Data" for all rows. In the new column, only keep 2 decimal digits.

Directly referenced source actions:

- Action 0: <code>`CLICK` on cell B2</code>
- Action 1: <code>`DOUBLE_CLICK` bottom right corner of the cell B2</code>
- Action 2: <code>`CLICK` on cell D2</code>
- Action 3: <code>`DOUBLE_CLICK` bottom right corner of the cell D2</code>

### 3. Create a Pivot Table from the selected data range

Skill ID: `51719eea-10bc-4246-a428-ac7c433dd4b3.skill-03`

Procedure:

1. Click within the dataset and use `Ctrl+A` to select the current contiguous data range, including its header row.
2. Click the Pivot Table toolbar icon to open the Pivot Table creation flow.
3. Accept the detected selected range, for example by pressing Enter in the initial creation dialog, to open the Pivot Table field-layout dialog.

Efficiency tip: Select the full current data region before creating the Pivot Table so Calc detects the source range automatically and no manual range entry is needed.

Source task: `51719eea-10bc-4246-a428-ac7c433dd4b3`

Source instruction: Calculate revenue in a new column according to the Retail Price sheet (consider product price and quantity and discount), and generate a Pivot Table in a new sheet (Sheet2) that summarizes the revenue of each product.

Directly referenced source actions:

- Action 10: <code>`HOTKEY` ctrl-A</code>
- Action 11: <code>`CLICK` pivot table icon</code>
- Action 12: <code>`PRESS` enter</code>

### 4. Rename a worksheet from its sheet tab

Skill ID: `535364ea-05bd-46ea-9937-9f55c68507e8.skill-02`

Procedure:

1. Double-click the worksheet tab whose name you want to change.
2. Type the new tab name, for example Sheet2, and press Enter to apply it.
3. The tab label updates, and the new name can be used in references such as $Sheet2.$A$15.

Efficiency tip: Rename a newly created sheet immediately after it is inserted so later cross-sheet references and destination selections use a clear, stable sheet name.

Source task: `535364ea-05bd-46ea-9937-9f55c68507e8`

Source instruction: Create two pivot tables in a new sheet showing the total revenue for each product and sales channel.

Directly referenced source actions:

- Action 8: <code>`DOUBLE_CLICK` Pivot Table Sheet1_1</code>
- Action 9: <code>`TYPING` Sheet2</code>
- Action 10: <code>`PRESS` enter</code>

## Initial state preview

### Analysis

![Analysis.png](artifact/previews/Analysis.png)

### Dispatch Log

![Dispatch_Log.png](artifact/previews/Dispatch_Log.png)

## Operator guide

### Existing operation-intent guide

#### Demonstration 1

- Skill: `4de54231-e4b5-49e3-b2ba-61a0bec721c0.skill-01`
- Intent: Propagate the route-level Estimated Liters calculation from the seeded first record through all remaining route records.
- Efficiency: Use the existing formula in E2 as the single source and double-click its fill handle; columns A:D have no gaps, so Calc can infer the final record row reliably.
- Visible success: Every cell from E2 through E25 displays a calculated fuel estimate, with relative row references reflected in the formulas.

#### Demonstration 2

- Skill: `0326d92d-d218-48a8-9ca1-981cd6d064c7.skill-01`
- Intent: Calculate the fleet-wide estimated fuel amount in the designated total cell E28.
- Efficiency: Enter one SUM over the completed Estimated Liters record range rather than adding individual records.
- Visible success: E28 shows a numeric overall total generated by a SUM formula covering the Estimated Liters data rows.

#### Demonstration 3

- Skill: `535364ea-05bd-46ea-9937-9f55c68507e8.skill-02`
- Intent: Rename the blank "Analysis" worksheet to "Zone Fuel Summary".
- Efficiency: Rename the blank destination sheet before configuring Pivot Table placement so its report role is clear in the destination selector.
- Visible success: The worksheet tab formerly labeled "Analysis" is visibly labeled "Zone Fuel Summary".

#### Demonstration 4

- Skill: `51719eea-10bc-4246-a428-ac7c433dd4b3.skill-03`
- Intent: Create the zone-level fuel Pivot Table from the completed Dispatch Log data and place it on the renamed report sheet.
- Efficiency: Start from the contiguous source table including headers so Calc detects the source fields automatically, then assign the grouping and summed measure in the layout dialog.
- Visible success: "Zone Fuel Summary" contains a native Pivot Table listing zones and a sum of Estimated Liters for each zone.

Recording start: "Dispatch Log" is active with the seeded E2 formula, blank E3:E25 and E28, and an empty worksheet tab named "Analysis".

Recording end: The Dispatch Log has formula-derived estimates in E2:E25 and a SUM total in E28; the output tab is named "Zone Fuel Summary" and contains a Pivot Table that sums Estimated Liters by Zone.

Allowed variation: The expert may create the Pivot Table before or after entering the overall total, and may use equivalent Calc commands or keyboard shortcuts. The finished Pivot Table may use a standard Calc-generated layout as long as it groups by Zone and sums Estimated Liters on the renamed output sheet.

### 中文详细参考方案

> 以下是一个可以参考的操作 guide。标注者可以根据实际 LibreOffice 界面采用等价操作。

本指南完成车队路线的预计燃油计算、全表燃油总计，并在重命名后的汇总工作表中建立按 Zone 分组、汇总 Estimated Liters 的 Pivot Table。开始时不要改动原始路线数据列 A:D；只需要利用 E2 中已有的计算公式。

#### 启动后的初始状态检查

- 确认当前打开的是“Dispatch Log”工作表。
- 确认源数据的表头位于 A1:E1，路线记录位于第 2 至第 25 行；A:D 各行均有连续数据。
- 确认 E1 的标题为“Estimated Liters”，E2 已含公式 `=C2*D2`，但 E3:E25 仍为空白。
- 确认第 26、27 行为空，D28 为“Total estimated liters”，E28 为空白。
- 确认存在一个空白工作表标签“Analysis”，且尚未建立任何 Pivot Table。

#### 第 1 步：向下填充每条路线的预计燃油公式

1. 在“Dispatch Log”中单击单元格 E2。查看输入栏，确认其公式为 `=C2*D2`。
2. 将指针移到 E2 选中框右下角的小方块（填充柄）上；当指针可用于填充时，双击该小方块。
3. Calc 会根据相邻的连续路线数据自动向下填充。滚动或单击 E25，确认该列已填充至第 25 行。

- 对应 skills：`4de54231-e4b5-49e3-b2ba-61a0bec721c0.skill-01`
- 高效操作：先确认 E2 是正确的种子公式，再用填充柄一次性向下填充，避免逐行输入公式或复制粘贴。
- 完成标志：E2:E25 都显示数值结果；例如选中 E3 时，公式会变为相对引用形式 `=C3*D3`，而不是所有行都引用第 2 行。

#### 第 2 步：计算全车队预计燃油总计

1. 单击指定总计结果单元格 E28。
2. 输入公式 `=SUM(E2:E25)`。
3. 按 Enter 确认公式。保留 D28 中原有标签“Total estimated liters”。

- 对应 skills：`0326d92d-d218-48a8-9ca1-981cd6d064c7.skill-01`
- 高效操作：使用一个 `SUM` 公式汇总连续区域，比逐个单元格相加更快，也会在路线数变化时更容易检查。
- 完成标志：E28 显示一个数值总计；选中 E28 时，输入栏显示 `=SUM(E2:E25)`。

#### 第 3 步：重命名分析工作表

1. 在窗口底部找到名为“Analysis”的工作表标签。
2. 双击“Analysis”标签，使工作表名称进入编辑状态。
3. 输入 `Zone Fuel Summary`，然后按 Enter。

- 对应 skills：`535364ea-05bd-46ea-9937-9f55c68507e8.skill-02`
- 高效操作：在建立报表前立即重命名空白输出表，可避免在 Pivot Table 的结果位置设置中选错工作表。
- 完成标志：原先显示“Analysis”的工作表标签现在清晰显示为“Zone Fuel Summary”，且该工作表仍为空白。

#### 第 4 步：选择路线数据并打开 Pivot Table 布局

1. 返回“Dispatch Log”工作表，在 A1:E25 中任意单击一个单元格，例如 A1。
2. 按 Ctrl+A 选择当前连续数据区域。确认选区包含表头 A1:E1 和第 2 至第 25 行记录，范围止于 E25。
3. 从菜单选择“数据 > 数据透视表 > 插入或编辑…”。如果出现要求确认数据源范围的对话框，保留当前检测到的选定范围并确认，以打开数据透视表布局对话框。

- 对应 skills：`51719eea-10bc-4246-a428-ac7c433dd4b3.skill-03`
- 高效操作：先只选中连续的源表 A1:E25，不要把空行或第 28 行总计包含进去；这样 Pivot Table 会正确识别字段和记录。
- 完成标志：数据透视表布局窗口打开，字段列表中可见 Zone 和 Estimated Liters 等源表字段。

#### 第 5 步：按 Zone 配置求和 Pivot Table 并放置到汇总表

1. 在 Pivot Table 布局对话框中，将字段 `Zone` 拖到“行字段”区域。
2. 将字段 `Estimated Liters` 拖到“数据字段”区域。
3. 检查数据字段的汇总方式为“Sum（求和）”。如果默认不是求和，可双击该数据字段，在字段设置中选择 Sum，然后确认。
4. 在布局对话框中选择结果位置设置（通常通过“结果”按钮或结果位置选项），选择将结果放在现有工作表，并指定“Zone Fuel Summary”工作表的起始单元格 A1。
5. 确认布局和结果位置，完成创建 Pivot Table。

- 对应 skills：无；这是准备或检查步骤。
- 高效操作：将分组字段放入行区域、数值字段放入数据区域；只放入这两个必需字段可得到简洁且易核对的分区燃油报告。
- 完成标志：“Zone Fuel Summary”中从 A1 附近出现原生 Pivot Table 输出：Zone 显示为行标签，各 Zone 的 Estimated Liters 显示为求和结果，并通常带有总计行。

#### 最终结果检查

- 在“Dispatch Log”中检查 E2:E25：每条路线都有两位小数的 Estimated Liters 计算结果；选中任一如 E3 的单元格时，编辑栏中的公式应按行引用（例如 `=C3*D3`）。
- 检查 D28 仍为“Total estimated liters”，且 E28 显示数值；选中 E28 时，编辑栏应显示 `=SUM(E2:E25)`。
- 确认工作表标签中不再有“Analysis”，而是有“Zone Fuel Summary”。
- 打开“Zone Fuel Summary”，确认其中是 Pivot Table 输出：Zone 为行分类，Estimated Liters 为求和数值字段，并且每个 Zone 有一条汇总结果。
- 可将各 Zone 的 Pivot Table 汇总值与“Dispatch Log”中对应 Zone 的 Estimated Liters 相加结果作抽查比对；各分区合计之和应与 E28 的总计一致。

## Source-task similarity review

| Measure | Maximum | Most similar source task |
| --- | ---: | --- |
| Lexical sequence similarity | 0.325815 | 1de60575-bb6e-4c3d-9e6a-2fa699f9f197 |
| Semantic cosine similarity | 0.410207 | 51719eea-10bc-4246-a428-ac7c433dd4b3 |

Similarity scores are reviewer aids, not automatic acceptance thresholds. Inspect the contributing source tasks and their complete ordered actions below.

### Source task `0326d92d-d218-48a8-9ca1-981cd6d064c7`

Original instruction:

> Calculate the total sales in an underneath row called "Total" and display the total of each month as bars. Then calculate the month-on-month growth percentage for Feb to Jun in another row called "Growth" and show them in a line chart (Jan should be omitted in the chart as well). Set the chart titles as the two row headers respectively.

Required skills derived from this source task:

- **Enter a range-total formula in a spreadsheet cell** — `0326d92d-d218-48a8-9ca1-981cd6d064c7.skill-01`

Complete ordered single-action sequence:

| Action | Related required skill | Original single action |
| ---: | --- | --- |
| 0 |  | <code>`CLICK` on cell A12</code> |
| 1 |  | <code>`TYPING` &#x27;Total&#x27;</code> |
| 2 |  | <code>`PRESS` tab</code> |
| 3 | <strong>★ Enter a range-total formula in a spreadsheet cell</strong><br><code>0326d92d-d218-48a8-9ca1-981cd6d064c7.skill-01</code> | <strong><code>`TYPING` &#x27;=SUM(B2:B11)&#x27;</code></strong> |
| 4 | <strong>★ Enter a range-total formula in a spreadsheet cell</strong><br><code>0326d92d-d218-48a8-9ca1-981cd6d064c7.skill-01</code> | <strong><code>`PRESS` enter</code></strong> |
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

### Source task `4de54231-e4b5-49e3-b2ba-61a0bec721c0`

Original instruction:

> I have compute the acceleration in row 2 and I want you to fill out other rows for column B and D. Next concatenate the values from columns A to D, including their headers (the pattern is "Header: cell value, ..., Header: cell value"), into a new column named "Combined Data" for all rows. In the new column, only keep 2 decimal digits.

Required skills derived from this source task:

- **Autofill an existing formula down a column with the fill handle** — `4de54231-e4b5-49e3-b2ba-61a0bec721c0.skill-01`

Complete ordered single-action sequence:

| Action | Related required skill | Original single action |
| ---: | --- | --- |
| 0 | <strong>★ Autofill an existing formula down a column with the fill handle</strong><br><code>4de54231-e4b5-49e3-b2ba-61a0bec721c0.skill-01</code> | <strong><code>`CLICK` on cell B2</code></strong> |
| 1 | <strong>★ Autofill an existing formula down a column with the fill handle</strong><br><code>4de54231-e4b5-49e3-b2ba-61a0bec721c0.skill-01</code> | <strong><code>`DOUBLE_CLICK` bottom right corner of the cell B2</code></strong> |
| 2 | <strong>★ Autofill an existing formula down a column with the fill handle</strong><br><code>4de54231-e4b5-49e3-b2ba-61a0bec721c0.skill-01</code> | <strong><code>`CLICK` on cell D2</code></strong> |
| 3 | <strong>★ Autofill an existing formula down a column with the fill handle</strong><br><code>4de54231-e4b5-49e3-b2ba-61a0bec721c0.skill-01</code> | <strong><code>`DOUBLE_CLICK` bottom right corner of the cell D2</code></strong> |
| 4 |  | <code>`CLICK` on cell E1</code> |
| 5 |  | <code>`TYPING` &#x27;Combined Data&#x27;</code> |
| 6 |  | <code>`PRESS` enter</code> |
| 7 |  | <code>`TYPING` &#x27;=$A$1&amp;&quot;: &quot;&amp;FIXED(A2,2)&amp;&quot;, &quot;&amp;$B$1&amp;&quot;: &quot;&amp;FIXED(B2,2)&amp;&quot;, &quot;&amp;$C$1&amp;&quot;: &quot;&amp;FIXED(C2,2)&amp;&quot;, &quot;&amp;$D$1&amp;&quot;: &quot;&amp;FIXED(D2,2)&#x27;</code> |
| 8 |  | <code>`CLICK` on cell E2</code> |
| 9 |  | <code>`DOUBLE_CLICK` bottom right corner of the cell E2</code> |

### Source task `51719eea-10bc-4246-a428-ac7c433dd4b3`

Original instruction:

> Calculate revenue in a new column according to the Retail Price sheet (consider product price and quantity and discount), and generate a Pivot Table in a new sheet (Sheet2) that summarizes the revenue of each product.

Required skills derived from this source task:

- **Create a Pivot Table from the selected data range** — `51719eea-10bc-4246-a428-ac7c433dd4b3.skill-03`

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
| 7 |  | <code>`CLICK` cell G2</code> |
| 8 |  | <code>`MOVE_TO` bottom right corner of the cell G2`</code> |
| 9 |  | <code>`DOUBLE_CLICK`</code> |
| 10 | <strong>★ Create a Pivot Table from the selected data range</strong><br><code>51719eea-10bc-4246-a428-ac7c433dd4b3.skill-03</code> | <strong><code>`HOTKEY` ctrl-A</code></strong> |
| 11 | <strong>★ Create a Pivot Table from the selected data range</strong><br><code>51719eea-10bc-4246-a428-ac7c433dd4b3.skill-03</code> | <strong><code>`CLICK` pivot table icon</code></strong> |
| 12 | <strong>★ Create a Pivot Table from the selected data range</strong><br><code>51719eea-10bc-4246-a428-ac7c433dd4b3.skill-03</code> | <strong><code>`PRESS` enter</code></strong> |
| 13 |  | <code>`MOVE_TO` product in available fields box</code> |
| 14 |  | <code>`DRAG_TO` row fields box</code> |
| 15 |  | <code>`MOVE_TO` revenue in available fields box</code> |
| 16 |  | <code>`DRAG_TO` data fields box</code> |
| 17 |  | <code>`CLICK` ok</code> |
| 18 |  | <code>`DOUBLE_CLICK` Pivot Table Sheet1_1</code> |
| 19 |  | <code>`TYPING` Sheet2</code> |
| 20 |  | <code>`PRESS` enter</code> |

### Source task `535364ea-05bd-46ea-9937-9f55c68507e8`

Original instruction:

> Create two pivot tables in a new sheet showing the total revenue for each product and sales channel.

Required skills derived from this source task:

- **Rename a worksheet from its sheet tab** — `535364ea-05bd-46ea-9937-9f55c68507e8.skill-02`

Complete ordered single-action sequence:

| Action | Related required skill | Original single action |
| ---: | --- | --- |
| 0 |  | <code>`HOTKEY` ctrl-a</code> |
| 1 |  | <code>`CLICK` pivot table icon</code> |
| 2 |  | <code>`PRESS` enter</code> |
| 3 |  | <code>`MOVE_TO` product in available fields box</code> |
| 4 |  | <code>`DRAG_TO` row fields box</code> |
| 5 |  | <code>`MOVE_TO` revenue in available fields box</code> |
| 6 |  | <code>`DRAG_TO` data fields box</code> |
| 7 |  | <code>`CLICK` ok</code> |
| 8 | <strong>★ Rename a worksheet from its sheet tab</strong><br><code>535364ea-05bd-46ea-9937-9f55c68507e8.skill-02</code> | <strong><code>`DOUBLE_CLICK` Pivot Table Sheet1_1</code></strong> |
| 9 | <strong>★ Rename a worksheet from its sheet tab</strong><br><code>535364ea-05bd-46ea-9937-9f55c68507e8.skill-02</code> | <strong><code>`TYPING` Sheet2</code></strong> |
| 10 | <strong>★ Rename a worksheet from its sheet tab</strong><br><code>535364ea-05bd-46ea-9937-9f55c68507e8.skill-02</code> | <strong><code>`PRESS` enter</code></strong> |
| 11 |  | <code>`CLICK` sheet &#x27;Sheet1&#x27;</code> |
| 12 |  | <code>`HOTKEY` ctrl-a</code> |
| 13 |  | <code>`CLICK` pivot table icon</code> |
| 14 |  | <code>`PRESS` enter</code> |
| 15 |  | <code>`MOVE_TO` sales channel in available fields box</code> |
| 16 |  | <code>`DRAG_TO` row fields box</code> |
| 17 |  | <code>`MOVE_TO` revenue in available fields box</code> |
| 18 |  | <code>`DRAG_TO` data fields box</code> |
| 19 |  | <code>`CLICK` Source and Destination dropdown</code> |
| 20 |  | <code>`CLICK` &#x27;Selection&#x27; under destination</code> |
| 21 |  | <code>`CLICK` text box</code> |
| 22 |  | <code>`TYPING` &#x27;$Sheet2.$A$15&#x27;</code> |
| 23 |  | <code>`CLICK` ok</code> |

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
