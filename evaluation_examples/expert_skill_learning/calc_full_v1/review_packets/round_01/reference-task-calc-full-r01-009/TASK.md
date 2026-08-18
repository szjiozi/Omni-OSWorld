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

本指南完成三个结果：在 `Activity Log` 中为全部分配记录生成统一的两位小数叙述文字；将 `Allocation Summary` 的深色标题改为白字；并在该汇总表创建原生 Pivot Table，以百分比显示各 `Zone` 占全部 `Completed Units` 的份额。

#### 启动后的初始状态检查

- 确认工作簿已打开，底部可见工作表 `Activity Log` 和 `Allocation Summary`。
- 在 `Activity Log` 中确认第 1 行是表头、已有 18 条数据记录，且 `Record Summary` 输出列的数据单元格目前为空。
- 在 `Allocation Summary` 中确认 `A1` 显示 `Workshop Allocation Share`，具有深色填充，但文字尚不是白色；标题下方的汇总区域为空。
- 确认源表的字段列表中可找到用于分组的 `Zone`，以及用于汇总的 `Completed Units`；创建 Pivot Table 时必须使用这两个字段。

#### 第 1 步：生成所有记录的两位小数叙述

1. 切换到 `Activity Log`，单击 `E2`。不要覆盖 `E1` 中的 `Record Summary` 表头。
2. 在 `E2` 输入以下公式后按 `Enter`：`=$A$1&": "&A2&", "&$B$1&": "&FIXED(B2,2)&", "&$C$1&": "&FIXED(C2,2)&", "&$D$1&": "&FIXED(D2,2)`。其中表头引用含 `$`，复制时会固定；第 2 行的数据引用会随行号改变。
3. 再次选中 `E2`，将选择范围扩展为 `E2:E19`，然后按 `Ctrl+D` 向下填充。

- 对应 skills：`4de54231-e4b5-49e3-b2ba-61a0bec721c0.skill-02`
- 高效操作：先只在 `E2` 完成一次正确公式，再一次性向下填充，可避免逐行输入并保持全部记录的文字格式一致。
- 完成标志：`E2:E19` 均显示由字段名称和数值组成的可读文本；每条记录中的三个单位数值均以两位小数显示，例如 `12.00`。

#### 第 2 步：将报告标题改为白色文字

1. 切换到 `Allocation Summary`，单击深色标题单元格 `A1`。
2. 打开工具栏上的 `Font Color` 下拉颜色面板，选择白色。
3. 保持 `A1` 选中，检查文字与深色填充之间的对比度。

- 对应 skills：`30e3e107-1cfb-46ee-a755-2cd080d7ba6a.skill-04`
- 高效操作：标题单元格保持选中时立刻设置字体颜色，深色背景会即时帮助你判断白字是否已生效。
- 完成标志：`A1` 中的 `Workshop Allocation Share` 显示为白色，并在深海军蓝背景上清晰可读。

#### 第 3 步：创建按 Zone 汇总 Completed Units 的原生 Pivot Table

1. 返回 `Activity Log`，选中包含表头和全部记录的连续源数据区域。选择范围必须包含 `Zone` 和 `Completed Units` 字段；如果表格范围显示为 `A1:E19`，可从 `A1` 拖选到最后一个已使用的单元格。
2. 打开 `Data` > `Pivot Table` > `Insert or Edit...`。在创建对话框中确认当前选择的数据源正确，然后继续进入字段布局设置。
3. 在字段布局中，将 `Zone` 放到行分组区域，使每个 Zone 成为一行；将 `Completed Units` 放到数据区域，并确认其汇总函数为求和。
4. 将结果位置设在 `Allocation Summary` 的标题下方空白区，例如 `A3`，随后确认创建。确保结果不会覆盖 `A1` 标题。

- 对应 skills：无；这是准备或检查步骤。
- 高效操作：直接从完整连续源表建立 Pivot Table，能够让字段名称和所有 18 条记录一次性进入字段布局，避免遗漏记录。
- 完成标志：`Allocation Summary` 的标题下方出现 Pivot Table，其中可见多个 Zone 行和 `Completed Units` 的汇总值；不再只是空白区域。

#### 第 4 步：将 Completed Units 显示为总计百分比

1. 在新建的 Pivot Table 中，打开 `Completed Units` 数据字段的选项或显示值设置。
2. 在显示值设置中打开 `Type` 下拉列表；它可能初始显示 `Normal`。
3. 从 `Type` 中选择 `% of total`，然后用 `OK` 或 `Enter` 确认数据字段选项。
4. 如需退出布局或更新提示，继续确认对话框，并观察 Pivot Table 的数据列显示格式。

- 对应 skills：`30e3e107-1cfb-46ee-a755-2cd080d7ba6a.skill-09`
- 高效操作：使用 Pivot Table 自带的百分比显示计算，可在源数据变化或刷新 Pivot Table 后自动维持正确份额，无需在表外编写辅助公式。
- 完成标志：Pivot Table 中每个 `Zone` 的 `Completed Units` 值显示为百分比，且总计行表示全部 Completed Units 的总份额。

#### 第 5 步：进行最终结果检查

1. 在 `Activity Log` 中查看第一条、中间一条和最后一条 `Record Summary`，确认每项均含 `Batch Code`、`Scheduled Units`、`Completed Units` 和 `Rework Units` 的标签与值，并且数值为两位小数。
2. 在 `Allocation Summary` 中确认 `A1` 标题未被 Pivot Table 覆盖，且仍保持白色文字和深色背景。
3. 检查 Pivot Table：每个 `Zone` 仅作为一个分组行出现，数值列为 `Completed Units` 的百分比显示，并检查总计是否为全部份额。

- 对应 skills：无；这是准备或检查步骤。
- 高效操作：最终检查时先核对结构和格式，再核对数字总计；这样可以同时发现遗漏填充、标题格式错误或透视表显示方式未更新的问题。
- 完成标志：工作簿同时具备完整的 18 条标准化记录叙述、白色可读标题，以及按 Zone 显示 Completed Units 总份额的原生 Pivot Table。

#### 最终结果检查

- 切换到 `Activity Log`，检查 `E2:E19`：18 条记录均已生成 `Record Summary` 文本，且每条中的 `Scheduled Units`、`Completed Units`、`Rework Units` 都显示为恰好两位小数。
- 切换到 `Allocation Summary`，确认 `A1` 仍为深海军蓝填充，`Workshop Allocation Share` 为白色且清晰可读。
- 确认 `Allocation Summary` 的标题下方存在原生 Pivot Table；它按 `Zone` 分行，汇总的是 `Completed Units`，数值显示为百分比而非普通数值，并有总计结果。
- 查看各 Zone 的百分比及 Pivot Table 的总计，确认各类别合计代表全部 `Completed Units` 的 100%份额。

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
