# Field Service Payment Review

- Reference task: `reference-task-calc-full-r01-007`
- Application: `libreoffice_calc`
- Review decision: `pending`

## Task instruction

Complete the Field Service Payment Review: calculate each technician's earned amount from the hourly rate and logged service duration, display the payment figures using German-style decimal separators, and mark earned amounts above 200 with a custom bright-green font. Then create a chart comparing technician earnings and place it on a newly added worksheet named Payment Overview.

## Required skills

### 1. Move a chart to a newly inserted worksheet

Skill ID: `12382c62-0cd1-4bf2-bdc8-1d20bf9b2371.skill-03`

Procedure:

1. Select the chart object and cut it with Ctrl+X.
2. Click the plus button beside the sheet tabs to insert a new worksheet; the new sheet becomes active.
3. Paste with Ctrl+V to place the cut chart on the new worksheet.

Efficiency tip: Use cut and paste rather than recreating the chart on the destination sheet; this preserves its data links, formatting, and title.

Source task: `12382c62-0cd1-4bf2-bdc8-1d20bf9b2371`

Source instruction: Create a clustered column chart showing the Sales and COGS data for each week in a new sheet. Set the chart title as "Sales & COGS".

Directly referenced source actions:

- Action 7: <code>`CLICK` on chart to select it</code>
- Action 8: <code>`HOTKEY` ctrl-X</code>
- Action 9: <code>`CLICK` on + to left of sheet1</code>
- Action 10: <code>`HOTKEY` ctrl+v</code>

### 2. Rename a worksheet from its sheet tab

Skill ID: `51719eea-10bc-4246-a428-ac7c433dd4b3.skill-05`

Procedure:

1. Double-click the worksheet tab to make its name editable.
2. Type the desired new name, for example `Sheet2`, and press Enter to commit the rename.

Efficiency tip: Rename the sheet tab immediately after creation so later formulas, navigation, and references use a meaningful sheet name.

Source task: `51719eea-10bc-4246-a428-ac7c433dd4b3`

Source instruction: Calculate revenue in a new column according to the Retail Price sheet (consider product price and quantity and discount), and generate a Pivot Table in a new sheet (Sheet2) that summarizes the revenue of each product.

Directly referenced source actions:

- Action 18: <code>`DOUBLE_CLICK` Pivot Table Sheet1_1</code>
- Action 19: <code>`TYPING` Sheet2</code>
- Action 20: <code>`PRESS` enter</code>

### 3. Create a conditional-format style with a custom font color

Skill ID: `21ab7b40-77c2-4ae6-8321-e00d3a086c73.skill-05`

Procedure:

1. From the conditional-formatting style or accent dropdown, choose `New Style` to create a style for cells that meet the rule.
2. Open the style’s Font Effects settings, open the font-color picker, and choose `Custom Color`.
3. Enter a hexadecimal color such as `00ff00`, then confirm the color and the style dialogs. The resulting style applies green font color whenever it is assigned to a conditional-formatting rule.

Efficiency tip: Create a reusable custom style from the conditional-formatting style selector instead of manually changing font color on each matching cell.

Source task: `21ab7b40-77c2-4ae6-8321-e00d3a086c73`

Source instruction: Please calculate the period rate for my data in a new column with header "Period Rate (%)", convert the results as number type, and highlight the highest result with green (#00ff00) font.

Directly referenced source actions:

- Action 15: <code>`CLICK` accent dropdown</code>
- Action 16: <code>`CLICK` new style</code>
- Action 17: <code>`CLICK` font effects</code>
- Action 18: <code>`CLICK` font color dropdown</code>
- Action 19: <code>`CLICK` custom color...</code>
- Action 20: <code>`DOUBLE_CLICK` Hex text box</code>
- Action 21: <code>`TYPING` &#x27;00ff00&#x27;</code>
- Action 22: <code>`PRESS` enter</code>
- Action 23: <code>`CLICK` OK</code>

### 4. Apply a locale-specific number format to a selected cell range

Skill ID: `a01fbce3-2793-461f-ab86-43680ccbae25.skill-01`

Procedure:

1. Select the cells whose displayed numeric separators should follow a different locale; for example, drag from A2 through B20.
2. Right-click the selected range and choose Format Cells.
3. In the Format Cells dialog, open the Language dropdown, type or select the desired locale, such as “German (aus),” and press Enter to apply that selection.
4. Click OK. The selected cells retain their underlying numeric values and decimal precision, while their displayed decimal separator follows the chosen locale (for example, a comma).

Efficiency tip: Select the full target range before opening Format Cells so the locale change is applied in one operation rather than formatting cells individually.

Source task: `a01fbce3-2793-461f-ab86-43680ccbae25`

Source instruction: I need to set the decimal separator as a comma (,) for localized data representation and clarity in visualization. Can you help me to update all the numbers in the sheet? Also please keep the decimal numbers as-is.

Directly referenced source actions:

- Action 0: <code>`MOVE_TO` cell A2</code>
- Action 1: <code>`DRAG_TO` cell B20</code>
- Action 2: <code>`RIGHT_CLICK`</code>
- Action 3: <code>`CLICK` Format Cells.</code>
- Action 4: <code>`CLICK` Language dropdown</code>
- Action 5: <code>`TYPING` German (aus)</code>
- Action 6: <code>`PRESS` enter</code>
- Action 7: <code>`CLICK` OK.</code>

### 5. Multiply a numeric rate by a duration converted to decimal hours

Skill ID: `357ef137-7eeb-4c80-a3bb-0951f26a8aff.skill-01`

Procedure:

1. Select the destination cell where the numeric product should appear.
2. Enter a formula that multiplies the rate by the duration expressed as hours plus minutes divided by 60. For example, use `=F3*(HOUR(D3)+MINUTE(D3)/60)`, where `F3` contains a numeric rate and `D3` contains a time or duration value.
3. Press Enter to calculate the result. `HOUR(D3)` supplies the whole-hour component, while `MINUTE(D3)/60` converts the remaining minutes into a fractional hour before multiplication.

Efficiency tip: Enter the conversion directly within the multiplication formula so Calc calculates a numeric amount in one cell, rather than creating helper cells solely to convert the duration.

Source task: `357ef137-7eeb-4c80-a3bb-0951f26a8aff`

Source instruction: I have calculated the total work hours from the everday hours. And I have an hourly rate. Now I want to multiply the total hours with the hourly rate to get a total earned amount. However, I can't get a correct answer by directly multiply the two cells. Here the "total hours" is of time and "hourly rate" is just a number. How can I get the correct product of them?

Directly referenced source actions:

- Action 0: <code>`CLICK` E3</code>
- Action 1: <code>`TYPING` &#x27;=F3*(HOUR(D3)+MINUTE(D3)/60)&#x27;</code>
- Action 2: <code>`PRESS` Enter</code>

## Initial state preview

### Shift Log

![Shift_Log.png](artifact/previews/Shift_Log.png)

## Operator guide

### Existing operation-intent guide

#### Demonstration 1

- Skill: `357ef137-7eeb-4c80-a3bb-0951f26a8aff.skill-01`
- Intent: Calculate each Earned Amount by multiplying the hourly rate by the service duration converted from hours and minutes to decimal hours.
- Efficiency: Enter the decimal-hour conversion directly in the earnings calculation and fill it down, avoiding helper columns.
- Visible success: Every populated shift row has a numeric Earned Amount consistent with its rate and displayed duration.

#### Demonstration 2

- Skill: `a01fbce3-2793-461f-ab86-43680ccbae25.skill-01`
- Intent: Apply a German locale-specific numeric display format to the Hourly Rate and Earned Amount values while preserving their values and precision.
- Efficiency: Select all target payment cells before opening the formatting dialog so one locale choice updates the full selection.
- Visible success: The targeted payment numbers visibly use comma decimal separators, while calculations remain numeric.

#### Demonstration 3

- Skill: `21ab7b40-77c2-4ae6-8321-e00d3a086c73.skill-05`
- Intent: Add a conditional-format rule that identifies Earned Amount values above 200 and uses a custom font color of #00FF00 for matching cells.
- Efficiency: Create the custom conditional-format style from the rule's style selector so it can be reused rather than manually formatting individual cells.
- Visible success: At least one qualifying Earned Amount is shown in bright green text, and nonqualifying values are not.

#### Demonstration 4

- Skill: `12382c62-0cd1-4bf2-bdc8-1d20bf9b2371.skill-03`
- Intent: Create a technician-versus-earned-amount chart, insert a fresh worksheet, and move the chart object onto that new worksheet.
- Efficiency: Cut and paste the completed chart rather than recreating it, preserving its chart settings and links.
- Visible success: The chart is no longer on Shift Log and is visible on its own newly inserted worksheet with linked earnings data.

#### Demonstration 5

- Skill: `51719eea-10bc-4246-a428-ac7c433dd4b3.skill-05`
- Intent: Rename the newly inserted chart worksheet to Payment Overview.
- Efficiency: Rename the new tab as soon as it is created, before continuing work on the chart sheet.
- Visible success: The workbook tab for the chart sheet visibly reads Payment Overview.

Recording start: One-sheet workbook with the populated Shift Log source table, blank Earned Amount cells, and no chart, conditional formatting, or additional worksheet.

Recording end: Shift Log contains calculated payment values with German-style numeric display and green-font conditional emphasis for earnings above 200; a chart comparing technician earnings is located on a separate worksheet named Payment Overview.

Allowed variation: The expert may use menu commands, dialogs, keyboard shortcuts, autofill, or equivalent Calc workflows. Chart type and threshold may follow the task wording as long as the result clearly compares technician earnings and the specified visual and worksheet outcomes are present.

### 中文详细参考方案

> 以下是一个可以参考的操作 guide。标注者可以根据实际 LibreOffice 界面采用等价操作。

本任务在 `Shift Log` 中完成 12 条现场服务记录的 Earned Amount 计算、德国式数字显示和高额付款的绿色条件格式，然后建立技术员收入比较图，并将该图移动到新建且命名为 `Payment Overview` 的工作表。

#### 启动后的初始状态检查

- 确认当前活动工作表标签为 `Shift Log`，并且只有这一张工作表。
- 确认标题行是 `A1:E1`，其中 `C` 列为 `Service Duration`、`D` 列为 `Hourly Rate`、`E` 列为 `Earned Amount`。
- 确认源数据位于第 `2` 至第 `13` 行，`E2:E13` 仍为空白；此时工作簿中没有图表，也没有名为 `Payment Overview` 的工作表。
- 确认 `Service Duration` 显示为类似 `1:15` 或 `7:45` 的时长，避免把时长当作普通十进制数字直接相乘。

#### 第 1 步：计算全部服务班次的 Earned Amount

1. 在 `Shift Log` 中单击 `E2`，输入公式 `=D2*(HOUR(C2)+MINUTE(C2)/60)`，然后按 `Enter`。其中 `HOUR(C2)` 取完整小时，`MINUTE(C2)/60` 把分钟换成小时的小数部分。
2. 再次选中 `E2` 并复制它。选择目标区域 `E3:E13` 后粘贴，使 Calc 按行自动调整相对引用。
3. 检查 `E2:E13` 中是否均出现计算结果；如某个结果未显示为数字，检查该行的公式是否仍引用同一行的 `C` 列和 `D` 列。

- 对应 skills：`357ef137-7eeb-4c80-a3bb-0951f26a8aff.skill-01`
- 高效操作：先只在第一行写好带时长换算的公式，再一次复制到剩余记录，可避免建立额外的辅助列。
- 完成标志：`E2:E13` 全部填入数值。每一行的 Earned Amount 会随该行的 Hourly Rate 和 Service Duration 而变化。

#### 第 2 步：将付款数字显示为德国式小数分隔符

1. 选择范围 `D2:E13`，右键单击所选区域并选择 `Format Cells...`。
2. 在格式对话框的 `Numbers` 选项卡中，确认数值类别适用于数字显示；如需要统一的金额显示精度，可将 `Decimal places` 设为 `2`。
3. 打开 `Language` 下拉列表，输入或选择 `German (aus)`，按 `Enter` 接受该语言设置，再点击 `OK`。

- 对应 skills：`a01fbce3-2793-461f-ab86-43680ccbae25.skill-01`
- 高效操作：一次选中完整的两列付款数值并统一设置语言区域，能避免逐个单元格修改，也不会改变公式或底层数值。
- 完成标志：`D2:E13` 中的数值显示小数逗号，例如类似 `28,50`；`E` 列的计算结果仍保持为数值而非文本。

#### 第 3 步：用条件格式突出超过 200 的收入

1. 选择 `E2:E13`，通过 `Format` 中的条件格式命令创建一个新的条件格式规则。将规则设为单元格值大于 `200`；数值阈值输入 `200`，不要输入带逗号的文本。
2. 在该规则的样式或强调样式下拉列表中选择 `New Style`。在新样式对话框中打开 `Font Effects`。
3. 打开字体颜色选择器，选择 `Custom Color`，在十六进制颜色输入框中输入 `00FF00`，确认颜色设置。确认新样式对话框，然后确认条件格式规则。
4. 回到工作表后，保留 `E2:E13` 的选择并检查规则是否应用到了完整范围。

- 对应 skills：`21ab7b40-77c2-4ae6-8321-e00d3a086c73.skill-05`
- 高效操作：把自定义绿色保存为条件格式样式，可使所有符合规则的单元格自动同步格式，而无需逐格设置字体颜色。
- 完成标志：至少一个大于 `200` 的 Earned Amount 显示为亮绿色字体；值为 `200` 或更低的金额不变成绿色。

#### 第 4 步：创建技术员收入比较图表

1. 先选择带标题的 `A1:A13`。按住 `Ctrl`，再选择带标题的 `E1:E13`，以同时选择 Technician 和 Earned Amount 数据。
2. 使用 `Insert` > `Chart...` 创建图表。在图表设置中选择能清楚比较各技术员收入的柱形或条形图，并确认类别标签来自 Technician、数据系列来自 Earned Amount。
3. 在图表标题中输入 `Technician Earnings`，完成图表创建。创建后的图表暂时应显示在 `Shift Log` 上。

- 对应 skills：无；这是准备或检查步骤。
- 高效操作：仅把 Technician 和 Earned Amount 作为图表源，可避免 Work Order、时长和费率被误加入图表，令图表更易阅读。
- 完成标志：`Shift Log` 上出现图表，图中能看到技术员名称以及对应的 Earned Amount 比较，不包含不相关的 Work Order 或 Service Duration 系列。

#### 第 5 步：剪切图表并新建图表工作表

1. 单击图表外框，使整个图表对象被选中，而不是只选中图表内部文字或数据系列。
2. 按 `Ctrl+X` 剪切图表对象。
3. 单击工作表标签旁的 `+` 以插入新工作表。确认新工作表已变成当前活动表，并且原图表已不再显示在 `Shift Log` 上。

- 对应 skills：`12382c62-0cd1-4bf2-bdc8-1d20bf9b2371.skill-03`
- 高效操作：剪切现有图表而不是在新表中重新建立，能保留已设置的图表类型、标题和对 `Shift Log` 数据的链接。
- 完成标志：出现一个新的空白工作表标签并处于活动状态；`Shift Log` 上不再保留该图表。

#### 第 6 步：命名新建的图表工作表

1. 双击新工作表的标签，使标签名称进入可编辑状态。
2. 输入 `Payment Overview`，然后按 `Enter` 提交名称。

- 对应 skills：`51719eea-10bc-4246-a428-ac7c433dd4b3.skill-05`
- 高效操作：在粘贴图表前立刻重命名新标签，后续检查图表位置和工作表引用时更清晰。
- 完成标志：当前工作表标签清楚显示为 `Payment Overview`。

#### 第 7 步：将图表粘贴到 Payment Overview

1. 保持在 `Payment Overview` 工作表，按 `Ctrl+V` 粘贴先前剪切的图表。
2. 如图表遮挡了工作表标签或显示区域，可拖动图表外框到该工作表中更合适的位置；不要修改数据系列为静态文本。
3. 单击图表外部以确认图表已放置完成，然后可切换回 `Shift Log` 做一次源数据检查。

- 对应 skills：`12382c62-0cd1-4bf2-bdc8-1d20bf9b2371.skill-03`
- 高效操作：直接粘贴剪切板中的图表即可恢复完整对象，无需重新选择数据范围或重新配置图表。
- 完成标志：图表可见于 `Payment Overview`，而 `Shift Log` 不含图表对象；图表仍显示技术员收入的比较结果。

#### 最终结果检查

- `Shift Log` 中的 `E2:E13` 均为计算所得的数值，而不是空白或手动输入的固定值；抽查任一行，金额应等于该行 Hourly Rate 乘以 Service Duration 换算出的十进制小时。
- `D2:E13` 的数字显示使用德国式小数逗号，且仍保留数值和所需的小数精度。
- `E2:E13` 存在条件格式：仅 Earned Amount 大于 `200` 的单元格显示亮绿色字体（`#00FF00`），不满足条件的金额不显示该绿色。
- 工作簿有且仅新增一个用于图表的工作表，其标签为 `Payment Overview`；技术员与 Earned Amount 的比较图表位于该表，而不再位于 `Shift Log`。
- 图表中的类别为技术员，数据系列为 Earned Amount，且图表仍与 `Shift Log` 的数据链接。

## Source-task similarity review

| Measure | Maximum | Most similar source task |
| --- | ---: | --- |
| Lexical sequence similarity | 0.266667 | 0bf05a7d-b28b-44d2-955a-50b41e24012a |
| Semantic cosine similarity | 0.427664 | 035f41ba-6653-43ab-aa63-c86d449d62e5 |

Similarity scores are reviewer aids, not automatic acceptance thresholds. Inspect the contributing source tasks and their complete ordered actions below.

### Source task `12382c62-0cd1-4bf2-bdc8-1d20bf9b2371`

Original instruction:

> Create a clustered column chart showing the Sales and COGS data for each week in a new sheet. Set the chart title as "Sales & COGS".

Required skills derived from this source task:

- **Move a chart to a newly inserted worksheet** — `12382c62-0cd1-4bf2-bdc8-1d20bf9b2371.skill-03`

Complete ordered single-action sequence:

| Action | Related required skill | Original single action |
| ---: | --- | --- |
| 0 |  | <code>`HOTKEY` ctrl-A</code> |
| 1 |  | <code>`CLICK` insert chart icon</code> |
| 2 |  | <code>`CLICK` chart elements on right sidebar</code> |
| 3 |  | <code>`CLICK` title text box</code> |
| 4 |  | <code>`TYPING` &#x27;Sales &amp; COGS&#x27;</code> |
| 5 |  | <code>`PRESS` enter</code> |
| 6 |  | <code>`CLICK` on cell A1 to cancel out of current menu</code> |
| 7 | <strong>★ Move a chart to a newly inserted worksheet</strong><br><code>12382c62-0cd1-4bf2-bdc8-1d20bf9b2371.skill-03</code> | <strong><code>`CLICK` on chart to select it</code></strong> |
| 8 | <strong>★ Move a chart to a newly inserted worksheet</strong><br><code>12382c62-0cd1-4bf2-bdc8-1d20bf9b2371.skill-03</code> | <strong><code>`HOTKEY` ctrl-X</code></strong> |
| 9 | <strong>★ Move a chart to a newly inserted worksheet</strong><br><code>12382c62-0cd1-4bf2-bdc8-1d20bf9b2371.skill-03</code> | <strong><code>`CLICK` on + to left of sheet1</code></strong> |
| 10 | <strong>★ Move a chart to a newly inserted worksheet</strong><br><code>12382c62-0cd1-4bf2-bdc8-1d20bf9b2371.skill-03</code> | <strong><code>`HOTKEY` ctrl+v</code></strong> |

### Source task `21ab7b40-77c2-4ae6-8321-e00d3a086c73`

Original instruction:

> Please calculate the period rate for my data in a new column with header "Period Rate (%)", convert the results as number type, and highlight the highest result with green (#00ff00) font.

Required skills derived from this source task:

- **Create a conditional-format style with a custom font color** — `21ab7b40-77c2-4ae6-8321-e00d3a086c73.skill-05`

Complete ordered single-action sequence:

| Action | Related required skill | Original single action |
| ---: | --- | --- |
| 0 |  | <code>`CLICK` on cell C1</code> |
| 1 |  | <code>`TYPING` &#x27;Period Rate (%)&#x27;</code> |
| 2 |  | <code>`PRESS` enter</code> |
| 3 |  | <code>`TYPING` &#x27;=A2/B2&#x27;</code> |
| 4 |  | <code>`PRESS` enter</code> |
| 5 |  | <code>`CLICK` cell C2</code> |
| 6 |  | <code>`DOUBLE_CLICK` bottom right corner of the cell C2</code> |
| 7 |  | <code>`CLICK` on the 0.0 icon that converts the cell to number type</code> |
| 8 |  | <code>`CLICK` format</code> |
| 9 |  | <code>`MOVE_TO` &#x27;conditional...&#x27;</code> |
| 10 |  | <code>`CLICK` &#x27;condition&#x27;</code> |
| 11 |  | <code>`CLICK` &#x27;cell value&#x27; dropdown</code> |
| 12 |  | <code>`CLICK` &#x27;Formula is&#x27; option</code> |
| 13 |  | <code>`CLICK` text field</code> |
| 14 |  | <code>`TYPING` $C2=MAX($C$2:$C$25)</code> |
| 15 | <strong>★ Create a conditional-format style with a custom font color</strong><br><code>21ab7b40-77c2-4ae6-8321-e00d3a086c73.skill-05</code> | <strong><code>`CLICK` accent dropdown</code></strong> |
| 16 | <strong>★ Create a conditional-format style with a custom font color</strong><br><code>21ab7b40-77c2-4ae6-8321-e00d3a086c73.skill-05</code> | <strong><code>`CLICK` new style</code></strong> |
| 17 | <strong>★ Create a conditional-format style with a custom font color</strong><br><code>21ab7b40-77c2-4ae6-8321-e00d3a086c73.skill-05</code> | <strong><code>`CLICK` font effects</code></strong> |
| 18 | <strong>★ Create a conditional-format style with a custom font color</strong><br><code>21ab7b40-77c2-4ae6-8321-e00d3a086c73.skill-05</code> | <strong><code>`CLICK` font color dropdown</code></strong> |
| 19 | <strong>★ Create a conditional-format style with a custom font color</strong><br><code>21ab7b40-77c2-4ae6-8321-e00d3a086c73.skill-05</code> | <strong><code>`CLICK` custom color...</code></strong> |
| 20 | <strong>★ Create a conditional-format style with a custom font color</strong><br><code>21ab7b40-77c2-4ae6-8321-e00d3a086c73.skill-05</code> | <strong><code>`DOUBLE_CLICK` Hex text box</code></strong> |
| 21 | <strong>★ Create a conditional-format style with a custom font color</strong><br><code>21ab7b40-77c2-4ae6-8321-e00d3a086c73.skill-05</code> | <strong><code>`TYPING` &#x27;00ff00&#x27;</code></strong> |
| 22 | <strong>★ Create a conditional-format style with a custom font color</strong><br><code>21ab7b40-77c2-4ae6-8321-e00d3a086c73.skill-05</code> | <strong><code>`PRESS` enter</code></strong> |
| 23 | <strong>★ Create a conditional-format style with a custom font color</strong><br><code>21ab7b40-77c2-4ae6-8321-e00d3a086c73.skill-05</code> | <strong><code>`CLICK` OK</code></strong> |
| 24 |  | <code>`CLICK` OK</code> |

### Source task `357ef137-7eeb-4c80-a3bb-0951f26a8aff`

Original instruction:

> I have calculated the total work hours from the everday hours. And I have an hourly rate. Now I want to multiply the total hours with the hourly rate to get a total earned amount. However, I can't get a correct answer by directly multiply the two cells. Here the "total hours" is of time and "hourly rate" is just a number. How can I get the correct product of them?

Required skills derived from this source task:

- **Multiply a numeric rate by a duration converted to decimal hours** — `357ef137-7eeb-4c80-a3bb-0951f26a8aff.skill-01`

Complete ordered single-action sequence:

| Action | Related required skill | Original single action |
| ---: | --- | --- |
| 0 | <strong>★ Multiply a numeric rate by a duration converted to decimal hours</strong><br><code>357ef137-7eeb-4c80-a3bb-0951f26a8aff.skill-01</code> | <strong><code>`CLICK` E3</code></strong> |
| 1 | <strong>★ Multiply a numeric rate by a duration converted to decimal hours</strong><br><code>357ef137-7eeb-4c80-a3bb-0951f26a8aff.skill-01</code> | <strong><code>`TYPING` &#x27;=F3*(HOUR(D3)+MINUTE(D3)/60)&#x27;</code></strong> |
| 2 | <strong>★ Multiply a numeric rate by a duration converted to decimal hours</strong><br><code>357ef137-7eeb-4c80-a3bb-0951f26a8aff.skill-01</code> | <strong><code>`PRESS` Enter</code></strong> |

### Source task `51719eea-10bc-4246-a428-ac7c433dd4b3`

Original instruction:

> Calculate revenue in a new column according to the Retail Price sheet (consider product price and quantity and discount), and generate a Pivot Table in a new sheet (Sheet2) that summarizes the revenue of each product.

Required skills derived from this source task:

- **Rename a worksheet from its sheet tab** — `51719eea-10bc-4246-a428-ac7c433dd4b3.skill-05`

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
| 10 |  | <code>`HOTKEY` ctrl-A</code> |
| 11 |  | <code>`CLICK` pivot table icon</code> |
| 12 |  | <code>`PRESS` enter</code> |
| 13 |  | <code>`MOVE_TO` product in available fields box</code> |
| 14 |  | <code>`DRAG_TO` row fields box</code> |
| 15 |  | <code>`MOVE_TO` revenue in available fields box</code> |
| 16 |  | <code>`DRAG_TO` data fields box</code> |
| 17 |  | <code>`CLICK` ok</code> |
| 18 | <strong>★ Rename a worksheet from its sheet tab</strong><br><code>51719eea-10bc-4246-a428-ac7c433dd4b3.skill-05</code> | <strong><code>`DOUBLE_CLICK` Pivot Table Sheet1_1</code></strong> |
| 19 | <strong>★ Rename a worksheet from its sheet tab</strong><br><code>51719eea-10bc-4246-a428-ac7c433dd4b3.skill-05</code> | <strong><code>`TYPING` Sheet2</code></strong> |
| 20 | <strong>★ Rename a worksheet from its sheet tab</strong><br><code>51719eea-10bc-4246-a428-ac7c433dd4b3.skill-05</code> | <strong><code>`PRESS` enter</code></strong> |

### Source task `a01fbce3-2793-461f-ab86-43680ccbae25`

Original instruction:

> I need to set the decimal separator as a comma (,) for localized data representation and clarity in visualization. Can you help me to update all the numbers in the sheet? Also please keep the decimal numbers as-is.

Required skills derived from this source task:

- **Apply a locale-specific number format to a selected cell range** — `a01fbce3-2793-461f-ab86-43680ccbae25.skill-01`

Complete ordered single-action sequence:

| Action | Related required skill | Original single action |
| ---: | --- | --- |
| 0 | <strong>★ Apply a locale-specific number format to a selected cell range</strong><br><code>a01fbce3-2793-461f-ab86-43680ccbae25.skill-01</code> | <strong><code>`MOVE_TO` cell A2</code></strong> |
| 1 | <strong>★ Apply a locale-specific number format to a selected cell range</strong><br><code>a01fbce3-2793-461f-ab86-43680ccbae25.skill-01</code> | <strong><code>`DRAG_TO` cell B20</code></strong> |
| 2 | <strong>★ Apply a locale-specific number format to a selected cell range</strong><br><code>a01fbce3-2793-461f-ab86-43680ccbae25.skill-01</code> | <strong><code>`RIGHT_CLICK`</code></strong> |
| 3 | <strong>★ Apply a locale-specific number format to a selected cell range</strong><br><code>a01fbce3-2793-461f-ab86-43680ccbae25.skill-01</code> | <strong><code>`CLICK` Format Cells.</code></strong> |
| 4 | <strong>★ Apply a locale-specific number format to a selected cell range</strong><br><code>a01fbce3-2793-461f-ab86-43680ccbae25.skill-01</code> | <strong><code>`CLICK` Language dropdown</code></strong> |
| 5 | <strong>★ Apply a locale-specific number format to a selected cell range</strong><br><code>a01fbce3-2793-461f-ab86-43680ccbae25.skill-01</code> | <strong><code>`TYPING` German (aus)</code></strong> |
| 6 | <strong>★ Apply a locale-specific number format to a selected cell range</strong><br><code>a01fbce3-2793-461f-ab86-43680ccbae25.skill-01</code> | <strong><code>`PRESS` enter</code></strong> |
| 7 | <strong>★ Apply a locale-specific number format to a selected cell range</strong><br><code>a01fbce3-2793-461f-ab86-43680ccbae25.skill-01</code> | <strong><code>`CLICK` OK.</code></strong> |

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
