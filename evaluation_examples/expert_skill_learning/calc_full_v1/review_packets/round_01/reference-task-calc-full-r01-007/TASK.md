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

本指南完成现场服务付款审核：先把时长换算为十进制小时以计算 `Earned Amount`，再为付款数字应用德国式显示格式，并用条件格式突出超过 200 的金额。最后创建技术员收益比较图，将该图移动到新工作表并命名为 `Payment Overview`。

#### 启动后的初始状态检查

- 确认当前打开的工作簿只有一个工作表标签 `Shift Log`，并且该工作表处于活动状态。
- 确认第 1 行的字段依次包括 `Technician`、`Work Order`、`Service Duration`、`Hourly Rate` 和 `Earned Amount`，数据位于第 2 至第 13 行。
- 确认 `E2:E13` 仍为空白，且工作簿中尚未出现图表对象或名为 `Payment Overview` 的工作表。
- 确认服务时长列显示为时:分形式；这些值是时长，不能直接与费率相乘来得到正确的十进制小时付款。

#### 第 1 步：计算每位技术员的 Earned Amount

1. 在 `Shift Log` 中点击单元格 `E2`。
2. 输入公式 `=D2*(HOUR(C2)+MINUTE(C2)/60)`，然后按 `Enter`。其中 `D2` 是小时费率，`HOUR(C2)` 取完整小时，`MINUTE(C2)/60` 将分钟换算成小时的小数部分。
3. 再次选中 `E2`，使用单元格右下角的填充柄向下拖动到 `E13`，以复制该公式到所有已填数据行。也可以复制 `E2` 后选中 `E3:E13` 并粘贴。

- 对应 skills：`357ef137-7eeb-4c80-a3bb-0951f26a8aff.skill-01`
- 高效操作：将时长到十进制小时的换算直接写进付款公式，不需要添加辅助列。
- 完成标志：`E2:E13` 都显示数值结果；选中任一金额单元格时，编辑栏中的公式会引用同一行的 `C` 列时长和 `D` 列费率。

#### 第 2 步：为付款数值应用德国式小数显示

1. 拖选 `D2:E13`。
2. 在选区上右键，选择 `Format Cells...`。
3. 在对话框中打开 `Numbers` 选项卡，找到 `Language` 下拉列表，选择德国语言区域设置，例如 `German (Austria)`，然后点击 `OK`。
4. 德国区域设置通常会保留已有的小数精度并仅改变显示的小数分隔符。若选区中带小数的数字已经显示为逗号，例如 `28,50`，则无需进一步调整。
5. 如果仍显示小数点，重新打开 `Format Cells...`，在 `Numbers` 中确认 `Language` 确实是所选的德国区域设置，然后点击 `OK`；不要把数值重新输入为文本。

- 对应 skills：`a01fbce3-2793-461f-ab86-43680ccbae25.skill-01`
- 高效操作：一次选中 `D2:E13` 再修改区域设置，可同时格式化费率和计算出的金额，且不会改动公式或底层数值。
- 完成标志：`D2:E13` 中含小数的费率和收益以逗号作为小数分隔符显示，同时 `E2:E13` 仍可作为数值参与计算。

#### 第 3 步：用条件格式突出高额收益

1. 选中 `E2:E13`。
2. 打开 `Format` > `Conditional` > `Condition...`，在条件格式对话框中为第一个条件选择单元格值比较方式，将比较设为大于，并输入阈值 `200`。
3. 在应用样式的下拉列表中选择 `New Style`，为新样式取一个易识别的名称，例如 `High Earned Amount`。
4. 在样式对话框中打开 `Font Effects`，打开 `Font Color` 的颜色选择器并选择 `Custom Color`。在自定义颜色对话框的十六进制输入框中输入 `00FF00`，确认颜色选择；再确认样式和条件格式对话框。
5. 如果金额大于 `200` 的单元格已经显示亮绿色文字，则无需调整。若已知大于 `200` 的金额仍不是绿色，重新打开 `Format` > `Conditional` > `Condition...`，确认规则范围是 `E2:E13`、比较为大于 `200`，且该规则选用了刚创建的自定义样式。

- 对应 skills：`21ab7b40-77c2-4ae6-8321-e00d3a086c73.skill-05`
- 高效操作：通过条件格式中的样式选择器创建自定义样式，规则可自动应用到当前和今后重新计算后符合条件的金额。
- 完成标志：`E2:E13` 中至少一个大于 `200` 的收益显示为 `#00FF00` 的亮绿色字体，而不符合条件的金额保持原有字体颜色。

#### 第 4 步：创建技术员收益比较图

1. 选中包含标题的 `A1:A13`，然后按住 `Ctrl` 并选中包含标题的 `E1:E13`。
2. 选择 `Insert` > `Chart...`，在图表向导中选择适合比较金额的柱形图类型，例如 `Column`，并完成图表插入。
3. 观察完成后的图表：横轴应显示技术员名称，图中应有一个代表 `Earned Amount` 的数值系列。若这两项已正确显示，无需调整。
4. 如果横轴显示金额、技术员名称被当作系列，或图表包含错误数据，双击图表进入编辑状态，打开 `Format` > `Data Ranges`。在 `Data Series` 中将类别范围修正为 `Shift Log.A2:A13`，并将收益系列的 `Y-Values` 修正为 `Shift Log.E2:E13`；完成后退出图表编辑状态。

- 对应 skills：无；这是准备或检查步骤。
- 高效操作：只选择技术员列和收益列，避免把工作单、时长或费率误加入图表；按住 `Ctrl` 可以选择不相邻的数据区域。
- 完成标志：`Shift Log` 上出现一个图表，类别为 12 位技术员，数值系列反映其 `Earned Amount`，而不是服务时长或小时费率。

#### 第 5 步：新建 Payment Overview 工作表并移动图表

1. 单击图表的外边框以选中整个图表对象，然后按 `Ctrl+X` 剪切图表。
2. 点击工作表标签旁的加号按钮以插入新工作表；新工作表会成为活动工作表。
3. 双击新工作表的标签，输入 `Payment Overview`，然后按 `Enter`。
4. 按 `Ctrl+V`，将剪切的图表粘贴到 `Payment Overview`。
5. 如果图表已经位于该新工作表的空白区域且没有遮挡任何需要查看的内容，则无需调整位置。若图表位置不便查看，单击其外边框选中整个对象并拖动，使图表完整可见。

- 对应 skills：`12382c62-0cd1-4bf2-bdc8-1d20bf9b2371.skill-03`, `51719eea-10bc-4246-a428-ac7c433dd4b3.skill-05`
- 高效操作：使用剪切和粘贴移动已完成的图表，可保留图表的数据链接、系列设置和格式，避免在新表中重新建图。
- 完成标志：工作表标签显示 `Payment Overview`，该表上可见技术员收益图；返回 `Shift Log` 时，原图表位置已不再有图表对象。

#### 第 6 步：完成最终核对

1. 切回 `Shift Log`，单击 `E2` 或其他收益单元格，确认编辑栏仍显示按该行引用的收益公式，而非固定输入的数字。
2. 查看 `D2:E13`，确认含小数的付款数值使用逗号显示；查看大于 `200` 的收益，确认其文字为亮绿色。
3. 切换到 `Payment Overview`，确认图表仍显示技术员类别及对应收益，并且图表的数据内容没有因移动而丢失。

- 对应 skills：无；这是准备或检查步骤。
- 高效操作：最终核对时只需抽查一行公式和一个高额金额，就能快速确认计算、格式和条件格式均已覆盖整个目标范围。
- 完成标志：计算列、德国式付款显示、绿色高额强调以及独立的 `Payment Overview` 图表页均同时存在并可见。

#### 最终结果检查

- `Shift Log` 的 `E2:E13` 均含有计算结果而非空白；任一行的金额等于该行 `Hourly Rate` 乘以服务时长换算出的十进制小时数。
- `D2:E13` 的数值显示使用德国式小数逗号，且仍是可用于计算的数字；例如带小数的费率或金额显示为逗号而不是小数点。
- `E2:E13` 中所有大于 `200` 的金额显示为亮绿色字体（`#00FF00`），不大于 `200` 的金额没有该绿色强调。
- 工作表标签中有且只有新建的图表页 `Payment Overview`；图表不再位于 `Shift Log`。
- `Payment Overview` 上的图表以技术员名称为类别，并以 `Earned Amount` 为数值系列，且图表仍显示来自 `Shift Log` 的全部 12 位技术员的收益数据。

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
