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

本任务在现有工作簿中完成三项整理：为每条活动记录生成统一的两位小数文字摘要、将深色报告标题改为白色文字，以及在 `Allocation Summary` 上建立按 `Zone` 汇总 `Completed Units` 总占比的原生数据透视表。

#### 启动后的初始状态检查

- 确认工作簿中有 `Activity Log` 和 `Allocation Summary` 两张工作表。
- 在 `Activity Log` 中确认第 1 行是源表标题、第 2 至第 19 行是 18 条记录，并且 `Record Summary` 列目前没有预填摘要或公式。
- 在 `Allocation Summary` 中确认 `A1` 显示 `Workshop Allocation Share`，具有深色填充，但文字尚不是白色；标题下方应有可放置汇总结果的空白区域。
- 创建区域数据透视表前，确认源数据中存在标题完全为 `Zone` 的区域字段，以及标题为 `Completed Units` 的数值字段。若当前可见源表确实只有 `Batch Code`、`Scheduled Units`、`Completed Units`、`Rework Units` 和 `Record Summary` 而没有 `Zone`，不要根据批次代码自行推断或编造区域；因为缺少分组字段时无法建立所要求的按区域数据透视表，应先补正源工作簿数据后再继续该部分。

#### 第 1 步：在第一条记录中建立标准化摘要公式

1. 打开 `Activity Log`，单击 `E2`，这是第一条记录对应的 `Record Summary` 输出单元格。
2. 输入以下公式后按 `Enter`：`=$A$1&": "&A2&", "&$B$1&": "&FIXED(B2,2)&", "&$C$1&": "&FIXED(C2,2)&", "&$D$1&": "&FIXED(D2,2)`。
3. 公式中的 `$A$1`、`$B$1`、`$C$1`、`$D$1` 固定引用第 1 行标题；`A2`、`B2`、`C2`、`D2` 则会在向下填充时改为当前记录所在行。`FIXED(...,2)` 会把三个单位数值转换成固定两位小数的文本。

- 对应 skills：`4de54231-e4b5-49e3-b2ba-61a0bec721c0.skill-02`
- 高效操作：先只在第一条记录写好公式，再一次性向下填充；绝对引用标题单元格可避免复制后标题引用发生偏移。
- 完成标志：`E2` 显示一段可读文本，包含四个标题和值；其中 `Scheduled Units`、`Completed Units` 和 `Rework Units` 后的数值均显示两位小数。

#### 第 2 步：将摘要公式填充到全部记录

1. 选中范围 `E2:E19`，确保 `E2` 是选区的最上方单元格并保留刚输入的公式。
2. 按 `Ctrl+D` 向下填充公式。
3. 查看 `E3` 和 `E19`，确认引用中的记录值已随行号变化，而标题文字保持不变。

- 对应 skills：`4de54231-e4b5-49e3-b2ba-61a0bec721c0.skill-02`
- 高效操作：使用 `Ctrl+D` 可将选区最上方的公式填入其余所有选中行，避免逐行复制。
- 完成标志：`E2:E19` 都不再为空，每一行都有对应记录的摘要文本，且每个单位数值均带有两位小数。

#### 第 3 步：将报告标题文字改为白色

1. 切换到 `Allocation Summary`，选中 `A1`。
2. 在工具栏打开 `Font Color` 的下拉颜色面板，选择白色。
3. 如果文字已在深色背景上清晰显示为白色，则无需再调整。若文字仍为深色、灰色或与背景对比不足，重新打开 `Font Color` 并选择纯白色样本。

- 对应 skills：`30e3e107-1cfb-46ee-a755-2cd080d7ba6a.skill-04`
- 高效操作：在标题单元格仍被选中时直接设置文字颜色，深色背景会立即帮助判断对比度是否足够。
- 完成标志：`A1` 中的 `Workshop Allocation Share` 为白色粗体文字，并且在深色背景上清楚可读。

#### 第 4 步：创建按区域汇总完成单位的数据透视表

1. 返回 `Activity Log`，选中包含 `Zone`、`Completed Units` 及其所有记录的完整连续源数据区域，并包含第 1 行字段标题。
2. 打开 `Data` > `Pivot Table` > `Insert or Edit...`，以当前选中的源数据建立数据透视表。
3. 在数据透视表布局区域中，将 `Zone` 放入行分组区域，将 `Completed Units` 放入数据字段区域，使其按求和方式汇总。
4. 确认布局后，在结果位置提示中将输出位置设在 `Allocation Summary` 的空白区域，例如选择 `A3`，再确认创建。
5. 如果 Calc 已显示每个区域一行并以 `Completed Units` 的合计作为数值，说明字段角色已正确推断，无需调整。若 `Zone` 出现在数值区、`Completed Units` 出现在行标签区，返回布局设置并将两字段分别移回行分组区域和数据字段区域后重新确认。

- 对应 skills：无；这是准备或检查步骤。
- 高效操作：从包含标题行的连续源表开始创建数据透视表，可让 Calc 自动识别可用字段；不要把目标工作表的空白区域混入源数据选择。
- 完成标志：`Allocation Summary` 的标题下方出现原生数据透视表，其中显示各个 `Zone` 的独立行及对应的 `Completed Units` 汇总值，且没有覆盖 `A1` 标题。

#### 第 5 步：将完成单位汇总值显示为总计百分比

1. 在数据透视表的布局或字段设置中，打开 `Completed Units` 数据字段的数据字段选项。
2. 打开 `Show Values As` 的显示值设置，将 `Type` 下拉选项从普通数值改为 `% of total`，然后用 `OK` 确认。
3. 如果表中的区域值已经显示百分号，并且总计显示为 100% 或等值的全部占比，则无需再调整。若区域值仍显示为原始完成单位数值，重新进入 `Completed Units` 的数据字段选项，确认 `Type` 确实为 `% of total` 后再次用 `OK` 保存。
4. 若百分比表位于空白汇总区且未遮挡标题或源数据，则无需移动。若它遮挡了标题或放置位置不清晰，可选中数据透视表整体并将其移到 `Allocation Summary` 中标题下方的空白区域。

- 对应 skills：`30e3e107-1cfb-46ee-a755-2cd080d7ba6a.skill-09`
- 高效操作：使用数据透视表内建的总计百分比显示方式，可在源数据更新后自动重新计算份额，无需在表外维护辅助公式。
- 完成标志：数据透视表中的每个 `Zone` 对应值带有百分比表示，且这些区域份额共同构成全部 `Completed Units` 的总计。

#### 第 6 步：完成最终核对

1. 回到 `Activity Log`，抽查 `E2`、中间任一摘要单元格和 `E19`，确认每条摘要都包含当前行的批次代码及三个两位小数单位值。
2. 回到 `Allocation Summary`，确认 `A1` 标题仍可见且为白色文字。
3. 确认数据透视表的行标签为 `Zone`，数值字段对应 `Completed Units`，并以百分比而非原始单位数显示。

- 对应 skills：无；这是准备或检查步骤。
- 高效操作：最终抽查首尾记录和数据透视表总计，可以快速发现未填充公式、错误字段或未应用百分比显示的情况。
- 完成标志：两个工作表均呈现完整结果：活动记录已有 18 条统一摘要，汇总表保留可读标题并显示各区域的完成单位总计占比。

#### 最终结果检查

- 在 `Activity Log` 中查看 `E2:E19`：18 个 `Record Summary` 单元格均有文本；每条文本依次包含 `Batch Code`、`Scheduled Units`、`Completed Units` 和 `Rework Units` 的标题与值，三个单位数值均显示为两位小数。
- 在 `Allocation Summary` 中查看 `A1`：`Workshop Allocation Share` 仍保留深色背景，文字为清晰可见的白色。
- 在 `Allocation Summary` 的标题下方查看数据透视表：每个 `Zone` 只出现一行，汇总字段是 `Completed Units`，各区域值以百分比显示，`Grand Total` 应表示全部完成单位的总占比（通常为 100%）。
- 确认数据透视表是通过 Calc 的 `Pivot Table` 功能生成，而不是在普通单元格中手工输入的汇总公式。

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
