# Route Operations Review

- Reference task: `reference-task-calc-full-r01-006`
- Application: `libreoffice_calc`
- Review decision: `pending`

## Task instruction

Prepare the Route Review for the municipal route-output report. Copy the 12 daily Output Volume values from Daily Metrics into the Working Output column, then calculate the day-over-day percentage change for every day after the first using formulas that keep Daily Metrics as the fixed source sheet. Build a distinct roster of nonblank Service Route names from the source table, preserving the first-seen order, with the result beginning at E5 on Route Review. Add a lines-only chart of Daily Change by Service Date, and export the completed review as /home/oai/share/route_operations_review.pdf.

## Required skills

### 1. Filter a range to copy only unique nonempty records

Skill ID: `abed40dc-063f-4598-8ba5-9fe749c0615d.skill-01`

Procedure:

1. Select the source range, including its header when present; for example, drag from B2 through B17.
2. Open Data > More Filters > Standard Filter.
3. In the filter criteria, set the relevant field/value condition to Not empty so blank records are excluded.
4. Open Options and enable No duplications to retain only the first occurrence of each repeated value in source order.
5. Enable Copy results to, click its destination box, and enter the top-left output cell reference, for example `$Sheet1.D2`. Here `$Sheet1` fixes the destination sheet, while column D and row 2 remain relative.
6. Confirm with OK to place the filtered unique records beginning at the specified destination cell.

Efficiency tip: Select the complete source range before opening the filter dialog so Calc can use it directly; enter the destination as a cell reference rather than copying results manually.

Source task: `abed40dc-063f-4598-8ba5-9fe749c0615d`

Source instruction: Check the names in column "Names with duplicates" and put the unique ones in column "Unique Names". Keep the original order of the first occurrences.

Directly referenced source actions:

- Action 0: <code>`MOVE_TO` B2</code>
- Action 1: <code>`DRAG_TO` B17</code>
- Action 2: <code>`CLICK` &#x27;Data&#x27; menu</code>
- Action 3: <code>`MOVE_TO` &#x27;More Filters&#x27;</code>
- Action 4: <code>`CLICK` &#x27;Standard Filter&#x27;</code>
- Action 5: <code>`CLICK` &#x27;Value dropdown</code>
- Action 6: <code>`CLICK` Not empty</code>
- Action 7: <code>`CLICK` &#x27;Options&#x27;</code>
- Action 8: <code>`CLICK` &#x27;No duplications&#x27;</code>
- Action 9: <code>`CLICK` copy to</code>
- Action 10: <code>`CLICK` text box below</code>
- Action 11: <code>`TYPING` &#x27;$Sheet1.D2</code>
- Action 12: <code>`CLICK` &#x27;OK&#x27;</code>

### 2. Insert a lines-only chart from the selected spreadsheet range

Skill ID: `0326d92d-d218-48a8-9ca1-981cd6d064c7.skill-07`

Procedure:

1. With the source ranges selected, click the chart icon and choose the Line chart category.
2. Choose the lines-only subtype, represented by the line-style icon, to create a chart without point markers.

Efficiency tip: Choose the specific line subtype during chart insertion instead of creating a default chart and changing its subtype afterward.

Source task: `0326d92d-d218-48a8-9ca1-981cd6d064c7`

Source instruction: Calculate the total sales in an underneath row called "Total" and display the total of each month as bars. Then calculate the month-on-month growth percentage for Feb to Jun in another row called "Growth" and show them in a line chart (Jan should be omitted in the chart as well). Set the chart titles as the two row headers respectively.

Directly referenced source actions:

- Action 38: <code>`CLICK` chart icon</code>
- Action 39: <code>`CLICK` Line</code>
- Action 40: <code>`CLICK` icon representing lines only (3rd from the right)</code>

### 3. Copy a contiguous cell range to another column

Skill ID: `37608790-6147-45d0-9f20-1137bb35703d.skill-01`

Procedure:

1. Select the first cell of the source range, then drag to the last cell to select all contiguous cells. For example, select A2 through A22.
2. Press Ctrl+C, click the destination's top cell (for example, B2), and press Ctrl+V.
3. Calc pastes the copied values into the destination range starting at the selected cell.

Efficiency tip: Copy the entire contiguous source range in one drag-and-paste operation rather than copying cells individually; this preserves the original data while creating a working copy.

Source task: `37608790-6147-45d0-9f20-1137bb35703d`

Source instruction: The information are mixed in one field. Help me split them and fill in the columns of First Name, Last Name and Rank

Directly referenced source actions:

- Action 0: <code>`MOVE_TO` A2</code>
- Action 1: <code>`DRAG_TO` A22</code>
- Action 2: <code>`HOTKEY` CTRL-C</code>
- Action 3: <code>`CLICK` on B2</code>
- Action 4: <code>`HOTKEY` CTRL-V</code>

### 4. Create a percentage-change formula using a fixed source sheet

Skill ID: `04d9aeaf-7bed-4024-bedb-e10e6f00eb7f.skill-03`

Procedure:

1. Select the output cell and type a percentage-change formula that subtracts the prior value and divides by that prior value; for example, enter =($Sheet1.B3-$Sheet1.B2)/$Sheet1.B2 in B2, then press Enter.
2. In $Sheet1.B3 and $Sheet1.B2, the $ fixes the source sheet name only. Column B and the row numbers remain relative, so filling the formula downward changes B3/B2 to B4/B3, while the source remains Sheet1.

Efficiency tip: Build the formula once with the intended relative and absolute references before filling it, so propagated formulas adjust correctly without later edits.

Source task: `04d9aeaf-7bed-4024-bedb-e10e6f00eb7f`

Source instruction: In a new sheet with 4 headers "Year", "CA changes", "FA changes", and "OA changes", calculate the percentage annual changes compared to last year in 2015 to 2019 for the Current Assets, Fixed Assets, and Other Assets columns. 

Directly referenced source actions:

- Action 13: <code>`CLICK` cell B2</code>
- Action 14: <code>`TYPING` &#x27;=($Sheet1.B3-$Sheet1.B2)/$Sheet1.B2&#x27;</code>
- Action 15: <code>`PRESS` enter</code>

### 5. Export a spreadsheet as a PDF to a specified path

Skill ID: `aa3a8974-2e85-438b-b29e-a64df44deb4b.skill-02`

Procedure:

1. Open File > Export as PDF.
2. In the file-name field, enter the full output path and PDF filename, such as /home/user/Resize_Cells_Fit_Page.pdf.
3. Click Export to create the PDF at that location.

Efficiency tip: Type the complete destination path and filename directly in the export dialog to avoid navigating folders and to ensure the PDF is saved exactly where required.

Source task: `aa3a8974-2e85-438b-b29e-a64df44deb4b`

Source instruction: I'm working on a project and need to resize cells in a spreadsheet to fit onto one page and export to PDF for efficient presentation. Could you help me on this? Keep the name of PDF the same as the spreadsheet and place it under my home directory.

Directly referenced source actions:

- Action 6: <code>`CLICK` File in the menu bar.</code>
- Action 7: <code>`CLICK` Export as PDF...</code>
- Action 8: <code>`CLICK` file name field</code>
- Action 9: <code>`TYPING` &#x27;/home/user/Resize_Cells_Fit_Page.pdf&#x27;</code>
- Action 10: <code>`CLICK` Export.</code>

## Initial state preview

### Daily Metrics

![Daily_Metrics.png](artifact/previews/Daily_Metrics.png)

### Route Review

![Route_Review.png](artifact/previews/Route_Review.png)

## Operator guide

### Existing operation-intent guide

#### Demonstration 1

- Skill: `abed40dc-063f-4598-8ba5-9fe749c0615d.skill-01`
- Intent: Produce a distinct-route roster from Daily Metrics!D1:D13 that excludes blank route cells, keeps first-occurrence order, and places the copied filter output beginning at Route Review!E5.
- Efficiency: Select the full Service Route source field with its header before opening the filter options, then provide the review-sheet output anchor directly rather than manually copying visible cells.
- Visible success: The roster beginning at E5 contains only North Loop, Harbor Spur, Cedar Link, Ridge Run, Quarry Way, and Canal Point once each (with any copied source header positioned above those results), and no blank roster item appears.

#### Demonstration 2

- Skill: `0326d92d-d218-48a8-9ca1-981cd6d064c7.skill-07`
- Intent: Create a trend chart on Route Review that plots Daily Change by Service Date and uses a line without point markers.
- Efficiency: Select the Service Date categories together with the completed Daily Change series, then choose the lines-only subtype during chart insertion instead of modifying a default chart later.
- Visible success: A chart object is visible on Route Review with dates as its category labels and a single continuous Daily Change line that has no data-point markers.

#### Demonstration 3

- Skill: `37608790-6147-45d0-9f20-1137bb35703d.skill-01`
- Intent: Copy Daily Metrics!B2:B13 into Route Review!B5:B16 while preserving the original source values.
- Efficiency: Copy the entire 12-cell Output Volume source series in one operation and paste it at the first Working Output cell.
- Visible success: Route Review!B5:B16 matches the 12 Output Volume values from Daily Metrics!B2:B13, while the source column remains present and unchanged.

#### Demonstration 4

- Skill: `04d9aeaf-7bed-4024-bedb-e10e6f00eb7f.skill-03`
- Intent: Calculate day-over-day percentage change in Route Review!C6:C16 from consecutive Output Volume values on the fixed Daily Metrics sheet; C5 remains blank because there is no prior day.
- Efficiency: Create the first formula using Daily Metrics as a sheet-fixed reference while leaving the row references relative, then propagate it down the remaining change rows.
- Visible success: C6:C16 displays percentage results, and inspecting formulas shows each uses a fixed Daily Metrics sheet reference while advancing from one source row pair to the next.

#### Demonstration 5

- Skill: `aa3a8974-2e85-438b-b29e-a64df44deb4b.skill-02`
- Intent: Export the completed workbook review as a PDF named route_operations_review.pdf at /home/oai/share/route_operations_review.pdf.
- Efficiency: Enter the complete requested PDF destination and filename in the export dialog to avoid ambiguity about the output location.
- Visible success: A PDF export is completed at the requested path after the review sheet shows the copied series, calculation column, roster, and trend chart.

Recording start: Route Review is active with its date axis prefilled but Working Output, Daily Change, and Distinct Route Roster target areas blank; Daily Metrics contains the intact source table and no chart or PDF exists.

Recording end: Route Review visibly contains the copied 12-row Working Output series, percentage Daily Change formulas from C6 through C16, the nonblank distinct route roster beginning at E5, and a lines-only Daily Change trend chart; the PDF has been exported to /home/oai/share/route_operations_review.pdf.

Allowed variation: The expert may use menus, keyboard shortcuts, or equivalent Calc dialogs, and may perform the independent review-sheet operations in any efficient order. Equivalent selection methods are acceptable, provided the resulting values, formulas, filtered roster, lines-only chart, and PDF are visibly correct.

### 中文详细参考方案

> 以下是一个可以参考的操作 guide。标注者可以根据实际 LibreOffice 界面采用等价操作。

本指南完成 municipal route-output review：从 `Daily Metrics` 复制 12 天的 Output Volume，在 `Route Review` 计算逐日百分比变化，生成非空且不重复的路线名单，制作无标记折线图，并导出指定路径的 PDF。源表 `Daily Metrics` 是固定数据来源，不应在其中输入或修改数据。

#### 启动后的初始状态检查

- 确认当前活动工作表是 `Route Review`，并且日期已在 `A5:A16` 预先填好。
- 确认 `Route Review!B5:B16`、`Route Review!C5:C16` 和 `Route Review!E5:E20` 仍为空；`C` 列已经是带一位小数的百分比格式。
- 切换到 `Daily Metrics`，确认 `A1:D13` 是完整源表，包含 `Service Date`、`Output Volume`、`Crew Hours` 和 `Service Route` 四列。不要编辑这个范围。
- 确认 `Route Review` 上尚没有图表对象。

#### 第 1 步：复制 12 天的 Working Output 数值

1. 切换到 `Daily Metrics` 工作表，选中 `B2:B13`，即 12 天的 `Output Volume` 数据；不要包含标题单元格 `B1`。
2. 按 `Ctrl+C` 复制所选区域。
3. 切换回 `Route Review`，单击 `B5`，然后按 `Ctrl+V`。

- 对应 skills：`37608790-6147-45d0-9f20-1137bb35703d.skill-01`
- 高效操作：一次选中完整的 12 个连续源单元格并粘贴，既快速又不会改变源数据。
- 完成标志：`Route Review!B5:B16` 已连续填入 12 个整数值，并与 `Daily Metrics!B2:B13` 相同；源表的 `Output Volume` 列仍然保留。

#### 第 2 步：计算固定源表的 Daily Change

1. 在 `Route Review` 中单击 `C6`。`C5` 必须保持为空，因为第一天没有前一天可比较。
2. 输入公式 `=($'Daily Metrics'.B3-$'Daily Metrics'.B2)/$'Daily Metrics'.B2`，然后按 `Enter`。其中 `$'Daily Metrics'` 固定的是源工作表名称，`B3` 和 `B2` 的行号仍可在向下填充时变化。
3. 再次选中 `C6`，复制该单元格；选中 `C7:C16` 后粘贴，以将公式填充到其余 10 天。也可以拖动 `C6` 右下角的填充柄直到 `C16`。
4. 单击 `C7` 或更靠下的一个结果单元格查看输入行，确认引用仍是 `Daily Metrics`，且源行号已相应前进。

- 对应 skills：`04d9aeaf-7bed-4024-bedb-e10e6f00eb7f.skill-03`
- 高效操作：先只建立一个正确的固定工作表引用公式，再向下填充，可避免逐行重输公式。
- 完成标志：`C6:C16` 显示百分比结果且保留一位小数，`C5` 为空；例如 `C6` 使用 `Daily Metrics` 的第 3 行和第 2 行，后续公式使用相邻的后续源行。

#### 第 3 步：筛选并复制不重复的非空 Service Route 名单

1. 切换到 `Daily Metrics`，选中包含标题的 `D1:D13`，即 `Service Route` 整列源范围。
2. 打开 `Data` > `More Filters` > `Standard Filter...`。在筛选条件中，将字段设为 `Service Route`，并将条件设为 `Not empty`，以排除空路线单元格。
3. 展开或点击 `Options`，启用 `No duplications`，使每个路线只保留首次出现的一项。
4. 在同一选项区域启用 `Copy results to`，在目标框输入 `$'Route Review'.E5`，然后确认对话框。
5. 返回 `Route Review` 检查输出。若 Calc 同时复制源标题，标题会位于路线结果上方；非空且不重复的路线项目应在其下连续列出。

- 对应 skills：`abed40dc-063f-4598-8ba5-9fe749c0615d.skill-01`
- 高效操作：筛选前先选择完整的单列源范围并直接填写输出锚点，可保留首次出现顺序，免去手动比较和复制。
- 完成标志：`Route Review` 的 E 列输出区域显示每条非空路线一次，顺序为 `North Loop`、`Harbor Spur`、`Cedar Link`、`Ridge Run`、`Quarry Way`、`Canal Point`，且没有空白路线项目。

#### 第 4 步：创建 Daily Change 的无标记折线图

1. 在 `Route Review` 中选择 `A4:A16`，使选择包含 Service Date 标题和全部日期。按住 `Ctrl`，再选择 `C4:C16`，使选择同时包含 `Daily Change` 标题和计算结果。
2. 使用图表按钮，或打开 `Insert` > `Chart...`，开始插入图表。
3. 在图表类型中选择 `Line`，然后选择只显示线条、没有数据点标记的子类型。
4. 在图表向导中确认日期列被用作类别标签、`Daily Change` 是唯一数据序列；如该向导显示数据方向选项，使用按列组织数据，并保留首行作为标签。完成图表插入。
5. 如有需要，拖动图表到 `Route Review` 中不遮挡表格的位置。不要将图表放到 `Daily Metrics` 源表中。

- 对应 skills：`0326d92d-d218-48a8-9ca1-981cd6d064c7.skill-07`
- 高效操作：同时选择日期和完整计算列（包括列标题）后立即选择折线的无标记子类型，比先插入默认图再修改更省时。
- 完成标志：`Route Review` 上出现一个图表对象；它以 Service Date 为横轴类别，只有一条 Daily Change 连续折线，线上没有圆点或其他数据点标记。

#### 第 5 步：导出前检查完成的 Route Review

1. 回到 `Route Review`，检查 `B5:B16`、`C6:C16`、路线名单和图表都可见且完整。
2. 特别确认 `C5` 仍为空，路线名单不含空白项，图表是仅线条样式而不是带标记的线图。
3. 如工作簿中仍显示复制或筛选后的活动虚线边框，可单击空白单元格或按 `Esc` 结束当前复制状态，再进行导出。

- 对应 skills：无；这是准备或检查步骤。
- 高效操作：导出前集中检查所有输出区域，可在生成 PDF 前发现漏填的公式、名单或图表。
- 完成标志：当前 `Route Review` 视图中能看到已填入的 Working Output、Daily Change 百分比、Distinct Route Roster 和折线图，准备导出。

#### 第 6 步：导出 Route Review 为指定 PDF

1. 打开 `File` > `Export as PDF...`；如果该命令位于子菜单中，则在 `File` > `Export As` 中选择 `Export as PDF...`。
2. 在文件名输入框中键入完整路径 `/home/oai/share/route_operations_review.pdf`。
3. 点击 `Export` 完成 PDF 创建。如出现 PDF 选项窗口，保持能够导出当前完成工作簿的设置并继续确认导出。

- 对应 skills：`aa3a8974-2e85-438b-b29e-a64df44deb4b.skill-02`
- 高效操作：在导出窗口中直接输入完整路径和文件名，不必逐层浏览文件夹，也能避免保存到错误位置。
- 完成标志：导出操作完成，文件 `/home/oai/share/route_operations_review.pdf` 已创建。

#### 最终结果检查

- 在 `Route Review` 中确认 `B5:B16` 已填满 12 个 Working Output 数值，且逐项对应 `Daily Metrics!B2:B13`；`Daily Metrics` 的源数据仍保留且没有被改写。
- 确认 `C5` 为空，`C6:C16` 显示一位小数的百分比。逐个抽查例如 `C6` 的公式应为 `=($'Daily Metrics'.B3-$'Daily Metrics'.B2)/$'Daily Metrics'.B2`，向下的公式仍固定引用 `Daily Metrics` 工作表、但行号会递进。
- 确认 Distinct Route Roster 中没有空白项目，并且非空路线按首次出现顺序各出现一次：`North Loop`、`Harbor Spur`、`Cedar Link`、`Ridge Run`、`Quarry Way`、`Canal Point`。
- 确认 `Route Review` 上有图表对象：横轴为 Service Date，只有一个 Daily Change 折线序列，折线没有数据点标记。
- 确认已在 `/home/oai/share/route_operations_review.pdf` 创建 PDF 文件；导出前的工作表视图中应可看到完整的数值、计算结果、路线名单和图表。

## Source-task similarity review

| Measure | Maximum | Most similar source task |
| --- | ---: | --- |
| Lexical sequence similarity | 0.232911 | 347ef137-7eeb-4c80-a3bb-0951f26a8aff |
| Semantic cosine similarity | 0.435233 | 04d9aeaf-7bed-4024-bedb-e10e6f00eb7f |

Similarity scores are reviewer aids, not automatic acceptance thresholds. Inspect the contributing source tasks and their complete ordered actions below.

### Source task `0326d92d-d218-48a8-9ca1-981cd6d064c7`

Original instruction:

> Calculate the total sales in an underneath row called "Total" and display the total of each month as bars. Then calculate the month-on-month growth percentage for Feb to Jun in another row called "Growth" and show them in a line chart (Jan should be omitted in the chart as well). Set the chart titles as the two row headers respectively.

Required skills derived from this source task:

- **Insert a lines-only chart from the selected spreadsheet range** — `0326d92d-d218-48a8-9ca1-981cd6d064c7.skill-07`

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
| 38 | <strong>★ Insert a lines-only chart from the selected spreadsheet range</strong><br><code>0326d92d-d218-48a8-9ca1-981cd6d064c7.skill-07</code> | <strong><code>`CLICK` chart icon</code></strong> |
| 39 | <strong>★ Insert a lines-only chart from the selected spreadsheet range</strong><br><code>0326d92d-d218-48a8-9ca1-981cd6d064c7.skill-07</code> | <strong><code>`CLICK` Line</code></strong> |
| 40 | <strong>★ Insert a lines-only chart from the selected spreadsheet range</strong><br><code>0326d92d-d218-48a8-9ca1-981cd6d064c7.skill-07</code> | <strong><code>`CLICK` icon representing lines only (3rd from the right)</code></strong> |
| 41 |  | <code>`CLICK` Chart elements</code> |
| 42 |  | <code>`CLICK` title text box</code> |
| 43 |  | <code>`TYPING` &#x27;Growth&#x27;</code> |
| 44 |  | <code>`PRESS` enter</code> |

### Source task `04d9aeaf-7bed-4024-bedb-e10e6f00eb7f`

Original instruction:

> In a new sheet with 4 headers "Year", "CA changes", "FA changes", and "OA changes", calculate the percentage annual changes compared to last year in 2015 to 2019 for the Current Assets, Fixed Assets, and Other Assets columns. 

Required skills derived from this source task:

- **Create a percentage-change formula using a fixed source sheet** — `04d9aeaf-7bed-4024-bedb-e10e6f00eb7f.skill-03`

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
| 13 | <strong>★ Create a percentage-change formula using a fixed source sheet</strong><br><code>04d9aeaf-7bed-4024-bedb-e10e6f00eb7f.skill-03</code> | <strong><code>`CLICK` cell B2</code></strong> |
| 14 | <strong>★ Create a percentage-change formula using a fixed source sheet</strong><br><code>04d9aeaf-7bed-4024-bedb-e10e6f00eb7f.skill-03</code> | <strong><code>`TYPING` &#x27;=($Sheet1.B3-$Sheet1.B2)/$Sheet1.B2&#x27;</code></strong> |
| 15 | <strong>★ Create a percentage-change formula using a fixed source sheet</strong><br><code>04d9aeaf-7bed-4024-bedb-e10e6f00eb7f.skill-03</code> | <strong><code>`PRESS` enter</code></strong> |
| 16 |  | <code>`CLICK` cell B2</code> |
| 17 |  | <code>`DOUBLE_CLICK` bottom right corner</code> |
| 18 |  | <code>`CLICK` cell B2</code> |
| 19 |  | <code>`MOVE_TO` bottom right corner of the cell B2</code> |
| 20 |  | <code>`DRAG_TO` cell D2</code> |
| 21 |  | <code>`CLICK` cell C2</code> |
| 22 |  | <code>`DOUBLE_CLICK` bottom right corner</code> |
| 23 |  | <code>`MOVE_TO` cell D2</code> |
| 24 |  | <code>`DOUBLE_CLICK` bottom right corner</code> |
| 25 |  | <code>`CLICK` cell B2</code> |
| 26 |  | <code>`DRAG_TO` D6</code> |
| 27 |  | <code>`CLICK` percent symbol</code> |

### Source task `37608790-6147-45d0-9f20-1137bb35703d`

Original instruction:

> The information are mixed in one field. Help me split them and fill in the columns of First Name, Last Name and Rank

Required skills derived from this source task:

- **Copy a contiguous cell range to another column** — `37608790-6147-45d0-9f20-1137bb35703d.skill-01`

Complete ordered single-action sequence:

| Action | Related required skill | Original single action |
| ---: | --- | --- |
| 0 | <strong>★ Copy a contiguous cell range to another column</strong><br><code>37608790-6147-45d0-9f20-1137bb35703d.skill-01</code> | <strong><code>`MOVE_TO` A2</code></strong> |
| 1 | <strong>★ Copy a contiguous cell range to another column</strong><br><code>37608790-6147-45d0-9f20-1137bb35703d.skill-01</code> | <strong><code>`DRAG_TO` A22</code></strong> |
| 2 | <strong>★ Copy a contiguous cell range to another column</strong><br><code>37608790-6147-45d0-9f20-1137bb35703d.skill-01</code> | <strong><code>`HOTKEY` CTRL-C</code></strong> |
| 3 | <strong>★ Copy a contiguous cell range to another column</strong><br><code>37608790-6147-45d0-9f20-1137bb35703d.skill-01</code> | <strong><code>`CLICK` on B2</code></strong> |
| 4 | <strong>★ Copy a contiguous cell range to another column</strong><br><code>37608790-6147-45d0-9f20-1137bb35703d.skill-01</code> | <strong><code>`HOTKEY` CTRL-V</code></strong> |
| 5 |  | <code>`CLICK` Data</code> |
| 6 |  | <code>`CLICK` Text to Columns</code> |
| 7 |  | <code>`CLICK` tab checkbox to uncheck it</code> |
| 8 |  | <code>`CLICK` Space checkbox to check it</code> |
| 9 |  | <code>`CLICK` OK</code> |

### Source task `aa3a8974-2e85-438b-b29e-a64df44deb4b`

Original instruction:

> I'm working on a project and need to resize cells in a spreadsheet to fit onto one page and export to PDF for efficient presentation. Could you help me on this? Keep the name of PDF the same as the spreadsheet and place it under my home directory.

Required skills derived from this source task:

- **Export a spreadsheet as a PDF to a specified path** — `aa3a8974-2e85-438b-b29e-a64df44deb4b.skill-02`

Complete ordered single-action sequence:

| Action | Related required skill | Original single action |
| ---: | --- | --- |
| 0 |  | <code>`CLICK` Format in the menu bar.</code> |
| 1 |  | <code>`CLICK` Page...</code> |
| 2 |  | <code>`CLICK` the Sheet tab.</code> |
| 3 |  | <code>`CLICK` scale dropdown</code> |
| 4 |  | <code>`CLICK` &#x27;Fit to number of pages&#x27;</code> |
| 5 |  | <code>`CLICK` OK.</code> |
| 6 | <strong>★ Export a spreadsheet as a PDF to a specified path</strong><br><code>aa3a8974-2e85-438b-b29e-a64df44deb4b.skill-02</code> | <strong><code>`CLICK` File in the menu bar.</code></strong> |
| 7 | <strong>★ Export a spreadsheet as a PDF to a specified path</strong><br><code>aa3a8974-2e85-438b-b29e-a64df44deb4b.skill-02</code> | <strong><code>`CLICK` Export as PDF...</code></strong> |
| 8 | <strong>★ Export a spreadsheet as a PDF to a specified path</strong><br><code>aa3a8974-2e85-438b-b29e-a64df44deb4b.skill-02</code> | <strong><code>`CLICK` file name field</code></strong> |
| 9 | <strong>★ Export a spreadsheet as a PDF to a specified path</strong><br><code>aa3a8974-2e85-438b-b29e-a64df44deb4b.skill-02</code> | <strong><code>`TYPING` &#x27;/home/user/Resize_Cells_Fit_Page.pdf&#x27;</code></strong> |
| 10 | <strong>★ Export a spreadsheet as a PDF to a specified path</strong><br><code>aa3a8974-2e85-438b-b29e-a64df44deb4b.skill-02</code> | <strong><code>`CLICK` Export.</code></strong> |

### Source task `abed40dc-063f-4598-8ba5-9fe749c0615d`

Original instruction:

> Check the names in column "Names with duplicates" and put the unique ones in column "Unique Names". Keep the original order of the first occurrences.

Required skills derived from this source task:

- **Filter a range to copy only unique nonempty records** — `abed40dc-063f-4598-8ba5-9fe749c0615d.skill-01`

Complete ordered single-action sequence:

| Action | Related required skill | Original single action |
| ---: | --- | --- |
| 0 | <strong>★ Filter a range to copy only unique nonempty records</strong><br><code>abed40dc-063f-4598-8ba5-9fe749c0615d.skill-01</code> | <strong><code>`MOVE_TO` B2</code></strong> |
| 1 | <strong>★ Filter a range to copy only unique nonempty records</strong><br><code>abed40dc-063f-4598-8ba5-9fe749c0615d.skill-01</code> | <strong><code>`DRAG_TO` B17</code></strong> |
| 2 | <strong>★ Filter a range to copy only unique nonempty records</strong><br><code>abed40dc-063f-4598-8ba5-9fe749c0615d.skill-01</code> | <strong><code>`CLICK` &#x27;Data&#x27; menu</code></strong> |
| 3 | <strong>★ Filter a range to copy only unique nonempty records</strong><br><code>abed40dc-063f-4598-8ba5-9fe749c0615d.skill-01</code> | <strong><code>`MOVE_TO` &#x27;More Filters&#x27;</code></strong> |
| 4 | <strong>★ Filter a range to copy only unique nonempty records</strong><br><code>abed40dc-063f-4598-8ba5-9fe749c0615d.skill-01</code> | <strong><code>`CLICK` &#x27;Standard Filter&#x27;</code></strong> |
| 5 | <strong>★ Filter a range to copy only unique nonempty records</strong><br><code>abed40dc-063f-4598-8ba5-9fe749c0615d.skill-01</code> | <strong><code>`CLICK` &#x27;Value dropdown</code></strong> |
| 6 | <strong>★ Filter a range to copy only unique nonempty records</strong><br><code>abed40dc-063f-4598-8ba5-9fe749c0615d.skill-01</code> | <strong><code>`CLICK` Not empty</code></strong> |
| 7 | <strong>★ Filter a range to copy only unique nonempty records</strong><br><code>abed40dc-063f-4598-8ba5-9fe749c0615d.skill-01</code> | <strong><code>`CLICK` &#x27;Options&#x27;</code></strong> |
| 8 | <strong>★ Filter a range to copy only unique nonempty records</strong><br><code>abed40dc-063f-4598-8ba5-9fe749c0615d.skill-01</code> | <strong><code>`CLICK` &#x27;No duplications&#x27;</code></strong> |
| 9 | <strong>★ Filter a range to copy only unique nonempty records</strong><br><code>abed40dc-063f-4598-8ba5-9fe749c0615d.skill-01</code> | <strong><code>`CLICK` copy to</code></strong> |
| 10 | <strong>★ Filter a range to copy only unique nonempty records</strong><br><code>abed40dc-063f-4598-8ba5-9fe749c0615d.skill-01</code> | <strong><code>`CLICK` text box below</code></strong> |
| 11 | <strong>★ Filter a range to copy only unique nonempty records</strong><br><code>abed40dc-063f-4598-8ba5-9fe749c0615d.skill-01</code> | <strong><code>`TYPING` &#x27;$Sheet1.D2</code></strong> |
| 12 | <strong>★ Filter a range to copy only unique nonempty records</strong><br><code>abed40dc-063f-4598-8ba5-9fe749c0615d.skill-01</code> | <strong><code>`CLICK` &#x27;OK&#x27;</code></strong> |

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
