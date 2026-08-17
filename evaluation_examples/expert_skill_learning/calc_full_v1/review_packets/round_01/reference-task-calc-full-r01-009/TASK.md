# Workshop Allocation Review

- Reference task: `reference-task-calc-full-r01-009`
- Application: `libreoffice_calc`
- Review decision: `pending`

## Task instruction

Complete the workshop allocation review: add a standardized two-decimal narrative for every allocation record, make the dark report heading readable with white text, and use the Allocation Summary sheet to show each zone’s share of all completed units.

## Required skills

### 1. Set a cell's font color from the color palette

Skill ID: `30e3e107-1cfb-46ee-a755-2cd080d7ba6a.skill-04`

Procedure:

1. With the target cell or merged cell selected, open the font-color dropdown.
2. Choose the desired palette color; for example, choose white for text that needs contrast against a dark fill.

Efficiency tip: Apply font color while the target cell remains selected after fill formatting, avoiding a separate reselection.

Source task: `30e3e107-1cfb-46ee-a755-2cd080d7ba6a`

Source instruction: Please create a new sheet. Keep its sheet name as "Sheet2". Merge cells A1:C1 in the new sheet and write "Demographic Profile" with blue (#0000ff) fill and bold white text. Then I want to create three pivot tables to show the percentage of Sex, Civil Status, and Highest Educational Attainment. They should be stacked one by one in Sheet2, each separated with a blank line.

Directly referenced source actions:

- Action 13: <code>`CLICK` font color arrow icon, which is to left of bucket</code>
- Action 14: <code>`CLICK` top right color in the color palette (white)</code>

### 2. Build a formatted text-concatenation formula with fixed decimal values

Skill ID: `4de54231-e4b5-49e3-b2ba-61a0bec721c0.skill-02`

Procedure:

1. In the first output-row cell, enter a concatenation formula that joins labels, separators, and formatted cell values. For example: =$A$1&": "&FIXED(A2,2)&", "&$B$1&": "&FIXED(B2,2)&", "&$C$1&": "&FIXED(C2,2)&", "&$D$1&": "&FIXED(D2,2)
2. Use & to join text fragments and cell results. FIXED(A2,2) converts the value in A2 to text with two decimal places; apply the same pattern to each value being joined.
3. In $A$1, the first $ fixes column A and the second $ fixes row 1, so the header reference remains A1 when copied. References such as A2 have no absolute markers, so their row changes when filled downward.

Efficiency tip: Use one concatenation formula with header references rather than manually assembling text row by row. Keep header cells absolute so the labels remain fixed when the formula is filled down.

Source task: `4de54231-e4b5-49e3-b2ba-61a0bec721c0`

Source instruction: I have compute the acceleration in row 2 and I want you to fill out other rows for column B and D. Next concatenate the values from columns A to D, including their headers (the pattern is "Header: cell value, ..., Header: cell value"), into a new column named "Combined Data" for all rows. In the new column, only keep 2 decimal digits.

Directly referenced source actions:

- Action 7: <code>`TYPING` &#x27;=$A$1&amp;&quot;: &quot;&amp;FIXED(A2,2)&amp;&quot;, &quot;&amp;$B$1&amp;&quot;: &quot;&amp;FIXED(B2,2)&amp;&quot;, &quot;&amp;$C$1&amp;&quot;: &quot;&amp;FIXED(C2,2)&amp;&quot;, &quot;&amp;$D$1&amp;&quot;: &quot;&amp;FIXED(D2,2)&#x27;</code>

### 3. Display Pivot Table values as a percentage of the total

Skill ID: `30e3e107-1cfb-46ee-a755-2cd080d7ba6a.skill-09`

Procedure:

1. In the data-field options dialog, open the displayed-value or Show Values As controls.
2. Open the Type dropdown, which may initially show Normal, and choose `% of total`.
3. Confirm the data-field options using OK or Enter. The value field will show each category's share of the overall total.

Efficiency tip: Use the built-in percentage display calculation rather than adding helper formulas outside the Pivot Table.

Source task: `30e3e107-1cfb-46ee-a755-2cd080d7ba6a`

Source instruction: Please create a new sheet. Keep its sheet name as "Sheet2". Merge cells A1:C1 in the new sheet and write "Demographic Profile" with blue (#0000ff) fill and bold white text. Then I want to create three pivot tables to show the percentage of Sex, Civil Status, and Highest Educational Attainment. They should be stacked one by one in Sheet2, each separated with a blank line.

Directly referenced source actions:

- Action 26: <code>`CLICK` &#x27;displayed value&#x27; dropdown</code>
- Action 27: <code>`CLICK` Normal dropdown next to &#x27;Type&#x27;</code>
- Action 28: <code>`CLICK` &#x27;% of total&#x27;</code>
- Action 29: <code>`CLICK` ok</code>
- Action 46: <code>`CLICK` &#x27;displayed value&#x27; dropdown</code>
- Action 47: <code>`CLICK` Normal dropdown next to &#x27;Type&#x27;</code>
- Action 48: <code>`CLICK` &#x27;% of total&#x27;</code>
- Action 49: <code>`PRESS` enter</code>
- Action 66: <code>`CLICK` &#x27;displayed value&#x27; dropdown</code>
- Action 67: <code>`CLICK` Normal dropdown next to &#x27;Type&#x27;</code>
- Action 68: <code>`CLICK` &#x27;% of total&#x27;</code>
- Action 69: <code>`PRESS` enter</code>

## Initial state preview

### Activity Log

![Activity_Log.png](artifact/previews/Activity_Log.png)

### Allocation Summary

![Allocation_Summary.png](artifact/previews/Allocation_Summary.png)

## Operator guide

### Existing operation-intent guide

#### Demonstration 1

- Skill: `4de54231-e4b5-49e3-b2ba-61a0bec721c0.skill-02`
- Intent: In Activity Log!E2, create a reusable concatenation formula that produces a labeled record narrative from Batch Code, Scheduled Units, Completed Units, and Rework Units. The three numeric values must be rendered with exactly two decimal places; copy the formula through E19.
- Efficiency: Use absolute references for the row-1 headers and relative references for the current data row, then fill the formula down in one operation.
- Visible success: Each Record Summary cell contains a readable label-and-value string, such as a batch code followed by the three unit measures, and every numeric measure visibly has two decimal places.

#### Demonstration 2

- Skill: `30e3e107-1cfb-46ee-a755-2cd080d7ba6a.skill-04`
- Intent: Change the font color of the existing dark-filled "Workshop Allocation Share" title in Allocation Summary!A1 to white.
- Efficiency: Apply the color while A1 is selected; the existing dark fill provides immediate contrast feedback.
- Visible success: The A1 title text is visibly white and legible against its dark navy background.

#### Demonstration 3

- Skill: `30e3e107-1cfb-46ee-a755-2cd080d7ba6a.skill-09`
- Intent: Create the native zone-level Pivot Table from Activity Log, summarize Completed Units by Zone, and set its displayed data values to percentage of the overall total.
- Efficiency: Use the data-field display option for percentage of the total instead of calculating shares in cells outside the Pivot Table.
- Visible success: Allocation Summary shows a native Pivot Table with one row per Zone and Completed Units represented as percentages; the category percentages collectively account for the grand total.

Recording start: The workbook has the populated Activity Log source table, a blank Record Summary output column, and a blank Allocation Summary area with a dark-filled, non-white title.

Recording end: Activity Log has completed Record Summary narratives for all 18 records with fixed two-decimal numeric text. Allocation Summary retains its dark-filled white-font title and displays a native Pivot Table that shows each Zone's share of total Completed Units as percentages.

Allowed variation: The expert may use LibreOffice Calc menus, toolbar controls, keyboard shortcuts, or equivalent dialogs. The Pivot Table may be positioned at A3 or another clearly non-overlapping location on Allocation Summary, provided the title remains visible and the resulting zone values are shown as percentages of the overall Completed Units total.

### 中文详细参考方案

> 以下是一个可以参考的操作 guide。标注者可以根据实际 LibreOffice 界面采用等价操作。

本指南完成三项工作：为每条活动记录生成统一的两位小数叙述文字、提高深色报告标题的可读性，以及在“Allocation Summary”中创建按 Zone 汇总 Completed Units 且显示总计占比的原生数据透视表。

#### 启动后的初始状态检查

- 确认工作簿中有“Activity Log”和“Allocation Summary”两个工作表。
- 在“Activity Log”中确认第 1 行为表头、数据记录位于第 2 至第 19 行，且“Record Summary”列当前为空；确认源表中可找到 Zone 和 Completed Units 字段。
- 在“Allocation Summary”中确认 A1 显示“Workshop Allocation Share”，底色为深色，且 A3 起的区域为空。
- 确认尚未存在数据透视表，以免编辑到旧结果。

#### 第 1 步：在第一条记录中建立两位小数叙述公式

1. 打开“Activity Log”工作表并单击 E2，即“Record Summary”标题下的第一条记录。
2. 输入以下公式后按 Enter：=$A$1&": "&A2&", "&$B$1&": "&FIXED(B2,2)&", "&$C$1&": "&FIXED(C2,2)&", "&$D$1&": "&FIXED(D2,2)
3. 其中 $A$1、$B$1、$C$1 和 $D$1 固定引用第 1 行标题；A2:D2 仍是当前记录行。FIXED(B2,2)、FIXED(C2,2) 和 FIXED(D2,2) 会把单位数值转换为恰好两位小数的文本。

- 对应 skills：`4de54231-e4b5-49e3-b2ba-61a0bec721c0.skill-02`
- 高效操作：先只在 E2 写好使用绝对表头引用、相对数据行引用的公式，后续可一次填满所有记录，避免逐行输入。
- 完成标志：E2 显示一段可读的标签和值组合文字，例如包含 Batch Code 以及三个单位字段；三个单位数值都带有两位小数。

#### 第 2 步：将记录叙述填充到全部 18 条记录

1. 再次选中 E2，然后按住 Shift 并选中 E19，使 E2:E19 成为选区。
2. 使用 Ctrl+D 向下填充。若更习惯菜单，可使用用于向下填充单元格的命令。
3. 抽查 E3 和 E19：Batch Code 与单位值应分别对应各自所在行，而字段标签保持不变。

- 对应 skills：无；这是准备或检查步骤。
- 高效操作：选中包含首个公式在内的整个目标区域后使用向下填充，可让相对行号自动从第 2 行变为第 3 至第 19 行。
- 完成标志：E2:E19 均不再为空；每一行都有自己的记录叙述，且 Scheduled Units、Completed Units、Rework Units 均以两位小数显示。

#### 第 3 步：将深色报告标题改为白色文字

1. 切换到“Allocation Summary”工作表并选中 A1，其中包含“Workshop Allocation Share”。
2. 在工具栏打开字体颜色的下拉调色板。
3. 从调色板选择白色。不要更改该单元格原有的深色填充或标题文字。

- 对应 skills：`30e3e107-1cfb-46ee-a755-2cd080d7ba6a.skill-04`
- 高效操作：A1 已有深色填充，保持该单元格处于选中状态即可立即看到白色文字与深色背景的对比。
- 完成标志：A1 中的“Workshop Allocation Share”文字为白色，并清晰显示在原有的深海军蓝背景上。

#### 第 4 步：创建按 Zone 汇总 Completed Units 的原生数据透视表

1. 返回“Activity Log”，在源表内单击任意单元格，然后选中包含所有表头和记录的完整连续源表区域。
2. 选择“数据”菜单中的“数据透视表”创建命令，开始建立数据透视表；在源数据确认界面确认使用当前选中的数据区域。
3. 在数据透视表布局界面，将 Zone 放入“行字段”区域，将 Completed Units 放入“数据字段”区域。确认 Completed Units 的汇总方式为“求和”。
4. 在输出位置设置中选择现有工作表“Allocation Summary”，并指定不覆盖标题的空白起点，例如 A3。确认创建数据透视表。

- 对应 skills：无；这是准备或检查步骤。
- 高效操作：从源表中选择整个连续数据区域而非只选两列，可确保数据透视表正确识别表头和全部记录；将结果放在 A3 可保留标题可见。
- 完成标志：“Allocation Summary”从 A3 或其他未覆盖标题的位置开始显示数据透视表；每个 Zone 各有一行，并显示 Completed Units 的求和结果及总计。

#### 第 5 步：将 Completed Units 显示为总计百分比

1. 在新建的数据透视表中，打开 Completed Units 数据字段的选项；通常可双击该数据字段，或通过字段的右键菜单打开数据字段设置。
2. 在数据字段选项中打开“显示的值”相关控件，将“类型”从 Normal 改为“% of total”。
3. 使用“确定”或 Enter 确认数据字段选项；如仍有数据透视表设置窗口，也确认该窗口以更新结果。
4. 查看每个 Zone 的数据值，确认它们以百分比而非原始单位数显示。

- 对应 skills：`30e3e107-1cfb-46ee-a755-2cd080d7ba6a.skill-09`
- 高效操作：使用数据字段本身的“显示的值”选项计算占总计百分比，避免在透视表外另建公式，也能在源数据更新后保持汇总逻辑一致。
- 完成标志：数据透视表的 Zone 行显示百分比形式的 Completed Units 份额；各类别百分比共同对应总计，Grand Total 为整体总量。

#### 最终结果检查

- 在“Activity Log”中检查 E2:E19：18 条记录均有“Record Summary”文字；每条均包含 Batch Code、Scheduled Units、Completed Units 和 Rework Units 的标签及数值，三个单位数值均显示为两位小数。
- 切换到“Allocation Summary”：A1 的“Workshop Allocation Share”仍使用深海军蓝底色，文字为醒目的白色。
- 确认“Allocation Summary”中存在原生数据透视表，按 Zone 分行，数据字段为 Completed Units；各 Zone 的值以百分比显示，并有总计，类别百分比合计为总计。
- 确认标题没有被透视表覆盖，且没有用工作表辅助公式替代透视表的百分比计算。

## Source-task similarity review

| Measure | Maximum | Most similar source task |
| --- | ---: | --- |
| Lexical sequence similarity | 0.335802 | 1de60575-bb6e-4c3d-9e6a-2fa699f9f197 |
| Semantic cosine similarity | 0.396176 | 04d9aeaf-7bed-4024-bedb-e10e6f00eb7f |

Similarity scores are reviewer aids, not automatic acceptance thresholds. Inspect the contributing source tasks and their complete ordered actions below.

### Source task `30e3e107-1cfb-46ee-a755-2cd080d7ba6a`

Original instruction:

> Please create a new sheet. Keep its sheet name as "Sheet2". Merge cells A1:C1 in the new sheet and write "Demographic Profile" with blue (#0000ff) fill and bold white text. Then I want to create three pivot tables to show the percentage of Sex, Civil Status, and Highest Educational Attainment. They should be stacked one by one in Sheet2, each separated with a blank line.

Required skills derived from this source task:

- **Set a cell's font color from the color palette** — `30e3e107-1cfb-46ee-a755-2cd080d7ba6a.skill-04`
- **Display Pivot Table values as a percentage of the total** — `30e3e107-1cfb-46ee-a755-2cd080d7ba6a.skill-09`

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
| 13 | <strong>★ Set a cell&#x27;s font color from the color palette</strong><br><code>30e3e107-1cfb-46ee-a755-2cd080d7ba6a.skill-04</code> | <strong><code>`CLICK` font color arrow icon, which is to left of bucket</code></strong> |
| 14 | <strong>★ Set a cell&#x27;s font color from the color palette</strong><br><code>30e3e107-1cfb-46ee-a755-2cd080d7ba6a.skill-04</code> | <strong><code>`CLICK` top right color in the color palette (white)</code></strong> |
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
| 26 | <strong>★ Display Pivot Table values as a percentage of the total</strong><br><code>30e3e107-1cfb-46ee-a755-2cd080d7ba6a.skill-09</code> | <strong><code>`CLICK` &#x27;displayed value&#x27; dropdown</code></strong> |
| 27 | <strong>★ Display Pivot Table values as a percentage of the total</strong><br><code>30e3e107-1cfb-46ee-a755-2cd080d7ba6a.skill-09</code> | <strong><code>`CLICK` Normal dropdown next to &#x27;Type&#x27;</code></strong> |
| 28 | <strong>★ Display Pivot Table values as a percentage of the total</strong><br><code>30e3e107-1cfb-46ee-a755-2cd080d7ba6a.skill-09</code> | <strong><code>`CLICK` &#x27;% of total&#x27;</code></strong> |
| 29 | <strong>★ Display Pivot Table values as a percentage of the total</strong><br><code>30e3e107-1cfb-46ee-a755-2cd080d7ba6a.skill-09</code> | <strong><code>`CLICK` ok</code></strong> |
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
| 46 | <strong>★ Display Pivot Table values as a percentage of the total</strong><br><code>30e3e107-1cfb-46ee-a755-2cd080d7ba6a.skill-09</code> | <strong><code>`CLICK` &#x27;displayed value&#x27; dropdown</code></strong> |
| 47 | <strong>★ Display Pivot Table values as a percentage of the total</strong><br><code>30e3e107-1cfb-46ee-a755-2cd080d7ba6a.skill-09</code> | <strong><code>`CLICK` Normal dropdown next to &#x27;Type&#x27;</code></strong> |
| 48 | <strong>★ Display Pivot Table values as a percentage of the total</strong><br><code>30e3e107-1cfb-46ee-a755-2cd080d7ba6a.skill-09</code> | <strong><code>`CLICK` &#x27;% of total&#x27;</code></strong> |
| 49 | <strong>★ Display Pivot Table values as a percentage of the total</strong><br><code>30e3e107-1cfb-46ee-a755-2cd080d7ba6a.skill-09</code> | <strong><code>`PRESS` enter</code></strong> |
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
| 66 | <strong>★ Display Pivot Table values as a percentage of the total</strong><br><code>30e3e107-1cfb-46ee-a755-2cd080d7ba6a.skill-09</code> | <strong><code>`CLICK` &#x27;displayed value&#x27; dropdown</code></strong> |
| 67 | <strong>★ Display Pivot Table values as a percentage of the total</strong><br><code>30e3e107-1cfb-46ee-a755-2cd080d7ba6a.skill-09</code> | <strong><code>`CLICK` Normal dropdown next to &#x27;Type&#x27;</code></strong> |
| 68 | <strong>★ Display Pivot Table values as a percentage of the total</strong><br><code>30e3e107-1cfb-46ee-a755-2cd080d7ba6a.skill-09</code> | <strong><code>`CLICK` &#x27;% of total&#x27;</code></strong> |
| 69 | <strong>★ Display Pivot Table values as a percentage of the total</strong><br><code>30e3e107-1cfb-46ee-a755-2cd080d7ba6a.skill-09</code> | <strong><code>`PRESS` enter</code></strong> |
| 70 |  | <code>`CLICK` source and destination dropdown</code> |
| 71 |  | <code>`CLICK` &#x27;Selection&#x27; under destination</code> |
| 72 |  | <code>`CLICK` text box</code> |
| 73 |  | <code>`TYPING` &#x27;$Sheet2.$A$13&#x27;</code> |
| 74 |  | <code>`CLICK` ok</code> |

### Source task `4de54231-e4b5-49e3-b2ba-61a0bec721c0`

Original instruction:

> I have compute the acceleration in row 2 and I want you to fill out other rows for column B and D. Next concatenate the values from columns A to D, including their headers (the pattern is "Header: cell value, ..., Header: cell value"), into a new column named "Combined Data" for all rows. In the new column, only keep 2 decimal digits.

Required skills derived from this source task:

- **Build a formatted text-concatenation formula with fixed decimal values** — `4de54231-e4b5-49e3-b2ba-61a0bec721c0.skill-02`

Complete ordered single-action sequence:

| Action | Related required skill | Original single action |
| ---: | --- | --- |
| 0 |  | <code>`CLICK` on cell B2</code> |
| 1 |  | <code>`DOUBLE_CLICK` bottom right corner of the cell B2</code> |
| 2 |  | <code>`CLICK` on cell D2</code> |
| 3 |  | <code>`DOUBLE_CLICK` bottom right corner of the cell D2</code> |
| 4 |  | <code>`CLICK` on cell E1</code> |
| 5 |  | <code>`TYPING` &#x27;Combined Data&#x27;</code> |
| 6 |  | <code>`PRESS` enter</code> |
| 7 | <strong>★ Build a formatted text-concatenation formula with fixed decimal values</strong><br><code>4de54231-e4b5-49e3-b2ba-61a0bec721c0.skill-02</code> | <strong><code>`TYPING` &#x27;=$A$1&amp;&quot;: &quot;&amp;FIXED(A2,2)&amp;&quot;, &quot;&amp;$B$1&amp;&quot;: &quot;&amp;FIXED(B2,2)&amp;&quot;, &quot;&amp;$C$1&amp;&quot;: &quot;&amp;FIXED(C2,2)&amp;&quot;, &quot;&amp;$D$1&amp;&quot;: &quot;&amp;FIXED(D2,2)&#x27;</code></strong> |
| 8 |  | <code>`CLICK` on cell E2</code> |
| 9 |  | <code>`DOUBLE_CLICK` bottom right corner of the cell E2</code> |

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
