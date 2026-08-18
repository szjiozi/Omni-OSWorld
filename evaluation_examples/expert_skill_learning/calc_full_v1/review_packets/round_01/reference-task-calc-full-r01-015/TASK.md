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

完成 `Dispatch Log` 中 24 条调度记录的油耗估算和总计，然后将空白分析工作表改名为 `Zone Fuel Summary`，并在该工作表创建按 Zone 汇总 Estimated Liters 的 Pivot Table。

#### 启动后的初始状态检查

- 确认当前活动工作表是 `Dispatch Log`，并且源数据表连续位于 A1:E25，首行为字段标题。
- 确认 `E1` 为 `Estimated Liters`，仅 `E2` 已有公式 `=C2*D2`，而 `E3:E25` 仍为空白。
- 确认 `D28` 显示 `Total estimated liters`，`E28` 为空白，且第 26、27 行没有源数据。
- 确认存在一个空白工作表标签 `Analysis`，其中尚未建立报告或 Pivot Table。

#### 第 1 步：向下填充每条路线的预计油耗公式

1. 在 `Dispatch Log` 中单击 E2；该单元格应包含种子公式 `=C2*D2`。
2. 将鼠标移到所选单元格右下角的小方块（填充柄）。当指针适合填充时，双击该小方块。
3. Calc 应将公式向下填充至相邻连续记录的末行，即 E25。若双击后没有填充到 E25，或中途停止，请重新选中 E2，并拖动其右下角填充柄直到 E25；然后检查 A:D 中是否有意外空白行。

- 对应 skills：`4de54231-e4b5-49e3-b2ba-61a0bec721c0.skill-01`
- 高效操作：双击填充柄会利用相邻连续的 A:D 列自动识别最后一条记录，比手动拖到第 25 行更快，也避免漏行。
- 完成标志：E2:E25 都显示数值。单击 E3、E4 等单元格时，公式栏中的引用会对应各自行号，例如 E3 使用 `=C3*D3`。

#### 第 2 步：计算全车队预计油耗总计

1. 单击指定总计结果单元格 E28。
2. 输入公式 `=SUM(E2:E25)`，然后按 `Enter`。
3. 若 E28 没有显示数值而显示公式文本，选中 E28 后使用 `Format` > `Cells...`，在数字格式区域将该单元格改为可计算的常规数值格式，再重新输入 `=SUM(E2:E25)` 并按 `Enter`。

- 对应 skills：`0326d92d-d218-48a8-9ca1-981cd6d064c7.skill-01`
- 高效操作：使用一个 `SUM` 公式一次覆盖完整的估算结果区域，比逐项相加更快且后续数据核对更容易。
- 完成标志：E28 显示一个数值总计，选中 E28 时公式栏显示 `=SUM(E2:E25)`。

#### 第 3 步：重命名空白分析工作表

1. 在窗口底部找到工作表标签 `Analysis`，双击该标签。
2. 输入 `Zone Fuel Summary`，然后按 `Enter`。
3. 若标签文字没有改变，说明可能仍处于编辑状态或名称未提交；再次双击 `Analysis`，完整输入 `Zone Fuel Summary` 后按 `Enter`。

- 对应 skills：`535364ea-05bd-46ea-9937-9f55c68507e8.skill-02`
- 高效操作：先为目标工作表改名，可在后续 Pivot Table 的输出位置中直接辨认正确的报告工作表。
- 完成标志：工作表标签由 `Analysis` 变为 `Zone Fuel Summary`，该工作表仍为空白。

#### 第 4 步：创建按 Zone 汇总预计油耗的 Pivot Table

1. 切换回 `Dispatch Log`，单击源表内任一单元格，例如 A1。
2. 按 `Ctrl+A` 选择当前连续数据区域。选择范围应为 A1:E25，包含标题行且不包含第 28 行总计。若选区包含了其他区域，请单击名称框或直接拖选 A1:E25 以修正。
3. 打开 `Data` > `Pivot Table` > `Insert or Edit...`。在首次创建对话框中，已检测到的源范围应为 A1:E25；若该范围正确，直接确认以进入字段布局对话框。若范围不正确，将源范围改为 `Dispatch Log` 的 A1:E25 后再继续。
4. 在字段布局中，将 `Zone` 放入行分组区域，使每个 Zone 成为一行；将 `Estimated Liters` 放入数据汇总区域。
5. 对于 `Estimated Liters`，Calc 通常会自动采用求和。若布局中已经显示该字段为 Sum，则无需调整。若显示为 Count 或其他汇总方式，打开该数据字段的设置，将汇总函数改为 Sum。
6. 在布局对话框的输出位置区域，选择将结果放到现有工作表，并指定 `Zone Fuel Summary` 的 A1 作为起始位置，然后确认创建 Pivot Table。若结果被放到了新工作表或错误位置，删除该错误 Pivot Table 后重新创建，并在输出位置明确选择 `Zone Fuel Summary` 的 A1。

- 对应 skills：`51719eea-10bc-4246-a428-ac7c433dd4b3.skill-03`
- 高效操作：只选择连续的 A1:E25 源表，不要包含第 28 行的总计；这样 Pivot Table 会将 `Estimated Liters` 识别为可汇总的数据字段。
- 完成标志：`Zone Fuel Summary` 中出现 Pivot Table；Zone 名称各自作为行项，旁边的数值列显示每个 Zone 的 `Estimated Liters` 总和，并通常带有总计行。

#### 第 5 步：核对工作簿中的最终结果

1. 切换到 `Zone Fuel Summary`，确认 Pivot Table 没有遮挡任何源数据，因为源数据仍应保留在 `Dispatch Log`。
2. 确认行项目是 Zone 值，而不是 Route Code；确认数值列对应 `Estimated Liters` 的 Sum。
3. 若行中显示 Route Code、数值列不是 Estimated Liters，或数值不是求和，请在 Pivot Table 内单击任一单元格，使用 `Data` > `Pivot Table` > `Edit Layout...`，将 `Zone` 设为行字段，将 `Estimated Liters` 设为数据字段并设为 Sum，然后确认更新。

- 对应 skills：无；这是准备或检查步骤。
- 高效操作：通过查看 Pivot Table 的行标签和数值字段名称即可快速确认分组字段与汇总方式，无需逐条手工计算。
- 完成标志：`Dispatch Log` 具有完整的 E2:E25 计算结果和 E28 总计，`Zone Fuel Summary` 具有按 Zone 的 Estimated Liters 求和 Pivot Table。

#### 最终结果检查

- 在 `Dispatch Log` 中，`E2:E25` 的每条路线都有计算出的 Estimated Liters 数值；选中其中任一后续单元格（如 E3）时，公式栏应显示随行号变化的乘法公式。
- `E28` 显示一个数值总计；选中它时，公式栏显示 `=SUM(E2:E25)`。
- 原 `Analysis` 工作表标签已改为 `Zone Fuel Summary`。
- `Zone Fuel Summary` 中存在原生 Pivot Table：行标签为各个 Zone，数值列为 Estimated Liters 的求和，并且每个 Zone 只汇总显示一次。

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
