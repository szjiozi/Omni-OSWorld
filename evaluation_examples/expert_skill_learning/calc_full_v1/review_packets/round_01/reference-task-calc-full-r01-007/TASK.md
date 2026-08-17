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

本指南将在 Shift Log 中计算 12 位现场技术员的 Earned Amount，将 Hourly Rate 和 Earned Amount 以德国式小数显示，为超过 200 的收入添加亮绿色条件格式，并建立技术员收入比较图表，将图表移至新建并命名为 Payment Overview 的工作表。

#### 启动后的初始状态检查

- 确认当前打开的是目标工作簿，且当前工作表标签为 Shift Log。
- 确认第 1 行包含 Technician、Work Order、Service Duration、Hourly Rate 和 Earned Amount 标题，数据位于第 2 至第 13 行。
- 确认 E2:E13 仍为空白，C 列服务时长显示为类似 [HH]:MM 的时长，且工作簿中尚没有 Payment Overview 工作表或图表。

#### 第 1 步：计算全部 Earned Amount

1. 在 Shift Log 工作表中单击 E2。
2. 输入公式 `=D2*(HOUR(C2)+MINUTE(C2)/60)`，然后按 Enter。
3. 该公式将 C2 的时长拆分为完整小时和分钟换算的小时小数，再乘以 D2 中的 Hourly Rate。
4. 再次选中 E2，将单元格右下角的小方块（填充柄）向下拖动到 E13；也可以复制 E2，再选中 E3:E13 并粘贴。

- 对应 skills：`357ef137-7eeb-4c80-a3bb-0951f26a8aff.skill-01`
- 高效操作：先只在 E2 建立正确公式，再使用填充柄或复制粘贴扩展到其余数据行，可避免逐行重复输入。
- 完成标志：E2:E13 都显示数值结果；单击任一结果单元格时，公式栏中的行号会相应变化，例如 E13 使用 C13 和 D13。

#### 第 2 步：将付款数字设为德国式小数显示

1. 拖动选中 D2:E13，其中包括 Hourly Rate 和 Earned Amount 两列的所有数据行。
2. 在选区上右键单击，选择“设置单元格格式”。
3. 在“设置单元格格式”对话框中，找到“语言”下拉列表，输入或选择 `German (aus)`，然后按 Enter 确认该语言选择。
4. 单击“确定”关闭对话框。

- 对应 skills：`a01fbce3-2793-461f-ab86-43680ccbae25.skill-01`
- 高效操作：一次选中 D2:E13 后统一设置语言区域，可确保两列付款数字的显示规则一致，且不会改变实际计算值。
- 完成标志：D2:E13 中带小数的付款数值使用逗号作为小数分隔符，例如显示为类似 35,50；这些单元格仍可参与计算。

#### 第 3 步：突出显示超过 200 的收入

1. 选中 Earned Amount 数据区域 E2:E13。
2. 从“格式”菜单打开“条件格式”，选择用于添加条件的命令，例如“条件…”。
3. 建立一个规则：当单元格值“大于” `200` 时应用格式。
4. 在规则的样式或强调样式下拉列表中选择“新建样式”。
5. 在新样式对话框中打开“字体效果”选项卡，展开字体颜色选择器并选择“自定义颜色”。
6. 在十六进制颜色输入框中输入 `00ff00`，确认颜色选择；然后确认样式对话框和条件格式规则对话框。
7. 如规则列表中尚未显示该规则，确认规则作用范围为 E2:E13 后再保存。

- 对应 skills：`21ab7b40-77c2-4ae6-8321-e00d3a086c73.skill-05`
- 高效操作：通过条件格式的样式选择器新建样式，绿色字体会随规则自动应用，不需要手工逐个修改高收入单元格。
- 完成标志：E2:E13 中至少一个大于 200 的金额立即显示为亮绿色字体（#00FF00）；数值不大于 200 的金额保持非绿色字体。

#### 第 4 步：创建技术员收入比较图表

1. 先选中 A1:A13 以包含 Technician 标题和全部技术员姓名；按住 Ctrl 后，再选中 E1:E13 以同时包含 Earned Amount 标题和全部计算结果。
2. 使用“插入”菜单中的“图表”命令启动图表向导。
3. 选择一种清晰比较各技术员收入的图表类型，例如柱形图；确认数据系列为 Earned Amount，分类标签为 Technician。
4. 完成图表向导。可为图表设置能说明内容的标题，例如 `Technician Earnings`。
5. 确认图表对象仍位于 Shift Log 后，单击图表外框使整个图表对象处于选中状态，而不是只选中图表内部元素。

- 对应 skills：无；这是准备或检查步骤。
- 高效操作：只将 Technician 标签和 Earned Amount 数据作为图表数据源，可避免 Work Order、服务时长或小时费率被误加入比较图。
- 完成标志：Shift Log 上出现图表，图中每位 Technician 对应一项 Earned Amount 比较数据，且整个图表外框可被选中。

#### 第 5 步：将图表移至新工作表

1. 保持整个图表对象被选中，按 Ctrl+X 剪切图表。
2. 单击工作表标签旁的加号，新插入的工作表会成为当前工作表。
3. 在新工作表中按 Ctrl+V 粘贴图表。

- 对应 skills：`12382c62-0cd1-4bf2-bdc8-1d20bf9b2371.skill-03`
- 高效操作：剪切再粘贴已有图表可保留其数据链接、图表类型和标题，无需在新工作表中重新制作。
- 完成标志：新工作表中可见完整图表，切换回 Shift Log 后图表不再显示在源数据表上。

#### 第 6 步：命名图表工作表

1. 在当前新工作表底部的工作表标签上双击，使标签名称进入编辑状态。
2. 输入 `Payment Overview`，然后按 Enter 提交名称。

- 对应 skills：`51719eea-10bc-4246-a428-ac7c433dd4b3.skill-05`
- 高效操作：在新增工作表仍处于活动状态时立刻改名，之后更容易识别图表所在位置。
- 完成标志：底部工作表标签清楚显示 `Payment Overview`，并且该工作表内保留技术员收入图表。

#### 最终结果检查

- 返回 Shift Log，确认 E2:E13 均包含计算结果而非空白；选中任一单元格时，编辑栏中可见以小时费率和服务时长计算的公式。
- 确认 D2:E13 的数值显示使用逗号作为小数分隔符，且服务时长 C2:C13 仍以 [HH]:MM 形式显示。
- 确认 E2:E13 中大于 200 的 Earned Amount 为亮绿色字体（#00FF00），而不大于 200 的金额没有此绿色字体。
- 确认底部存在名为 Payment Overview 的工作表标签。
- 打开 Payment Overview，确认可见比较 Technician 与 Earned Amount 的图表；返回 Shift Log 时不应再看到该图表对象。

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
