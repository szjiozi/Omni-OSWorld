# Replenishment Review

- Reference task: `reference-task-calc-full-r01-005`
- Application: `libreoffice_calc`
- Review decision: `pending`

## Task instruction

Prepare the replenishment review workbook for management: classify every dispatch record from the SKU catalog, create seven-digit ticket-code displays, flag the single largest restock cost, sort the complete dispatch log by SKU from A to Z, and show the total units dispatched on the Summary sheet.

## Required skills

### 1. Enter an exact-match VLOOKUP formula

Skill ID: `7e429b8d-a3f0-4ed0-9b58-08957d00b127.skill-01`

Procedure:

1. Select the destination cell where the lookup result should appear.
2. Type a VLOOKUP formula that uses a lookup key, a table range, the return-column number, and `FALSE` for an exact match. For example, enter `=VLOOKUP(E2,$A$2:$B$7,2,FALSE)` to find the value from E2 in the first column of the fixed A2:B7 table and return the matching value from its second column.
3. Press Enter to commit the formula. In `$A$2:$B$7`, the `$` before each column and row fixes both columns and rows when the formula is filled.

Efficiency tip: Use absolute references such as `$A$2:$B$7` for a fixed lookup table so the table range does not shift when the formula is copied to other rows.

Source task: `7e429b8d-a3f0-4ed0-9b58-08957d00b127`

Source instruction: I have a lookup table for the officers of each branch. Please, here is another table in which I need to fill with the officer names according the headoffice (i.e., the branch name). Help me to complete this.

Directly referenced source actions:

- Action 0: <code>`CLICK` F2</code>
- Action 1: <code>`TYPING` =VLOOKUP(E2, $A$2:$B$7, 2, FALSE)</code>
- Action 2: <code>`PRESS` Enter.</code>

### 2. Configure a formula-based conditional formatting rule

Skill ID: `21ab7b40-77c2-4ae6-8321-e00d3a086c73.skill-04`

Procedure:

1. With the intended result range active, open Format > Conditional > Condition.
2. Change the condition type from a cell-value comparison to `Formula is`.
3. Enter a Boolean formula that tests the current row. For example, use `$C2=MAX($C$2:$C$25)` to test whether each cell in column C equals the maximum of C2:C25.
4. In this example, `$C2` fixes column C but leaves row 2 relative, so the row changes as the rule is evaluated down the range. `$C$2:$C$25` fixes both the column and rows for the maximum range.
5. After choosing or creating the desired style, confirm the conditional-formatting dialog to save the rule.

Efficiency tip: Use a relative row reference in the condition formula so one rule can evaluate every row in the selected range, rather than creating a separate rule per cell.

Source task: `21ab7b40-77c2-4ae6-8321-e00d3a086c73`

Source instruction: Please calculate the period rate for my data in a new column with header "Period Rate (%)", convert the results as number type, and highlight the highest result with green (#00ff00) font.

Directly referenced source actions:

- Action 8: <code>`CLICK` format</code>
- Action 9: <code>`MOVE_TO` &#x27;conditional...&#x27;</code>
- Action 10: <code>`CLICK` &#x27;condition&#x27;</code>
- Action 11: <code>`CLICK` &#x27;cell value&#x27; dropdown</code>
- Action 12: <code>`CLICK` &#x27;Formula is&#x27; option</code>
- Action 13: <code>`CLICK` text field</code>
- Action 14: <code>`TYPING` $C2=MAX($C$2:$C$25)</code>
- Action 24: <code>`CLICK` OK</code>

### 3. Format a numeric cell value as fixed-width text with leading zeros

Skill ID: `0bf05a7d-b28b-44d2-955a-50b41e24012a.skill-01`

Procedure:

1. Select the destination cell and enter a TEXT formula that references the source cell with a zero-only number format.
2. For example, enter `=TEXT(C2,"0000000")` in D2 to display the value from C2 as seven digits, adding leading zeros when necessary.
3. The result is text, so use this method when a fixed-width identifier-like display is needed rather than a numeric value for later arithmetic.

Efficiency tip: Enter the formula once in the first destination cell, then propagate it rather than manually editing each value.

Source task: `0bf05a7d-b28b-44d2-955a-50b41e24012a`

Source instruction: I would like to copy all the numbers in the 'Old ID' column to the 'New 7 Digit Id' column, and pad them with zeros in front, to fill them up to seven digits.

Directly referenced source actions:

- Action 0: <code>`DOUBLE_CLICK` cell D2</code>
- Action 1: <code>`TYPING` &#x27;=TEXT(C2,&quot;0000000&quot;)&#x27; in the formula bar</code>

### 4. Build a cross-sheet range-total formula

Skill ID: `26a8440e-c166-4c50-aef4-bfb77314b46b.skill-03`

Procedure:

1. Select the destination cell and type a formula that totals a range on another worksheet, for example `=SUM($Sheet1.B2:B11)`, then press Enter.
2. In `$Sheet1.B2:B11`, the `$` before `Sheet1` fixes the source sheet only. Column B and rows 2 through 11 remain relative, so they can adjust when the formula is filled to another location.
3. Use the same pattern with any source sheet and source range, such as `=SUM($Data.C2:C20)`.

Efficiency tip: Enter the formula once in the first result cell, then use autofill separately to propagate the relative references instead of manually editing equivalent formulas.

Source task: `26a8440e-c166-4c50-aef4-bfb77314b46b`

Source instruction: Create a table with two column headers ("Month" and "Total") in a new sheet named "Sheet2" to show the total sales for all months.

Directly referenced source actions:

- Action 12: <code>`CLICK` cell B2</code>
- Action 13: <code>`TYPING` &#x27;=SUM($Sheet1.B2:B11)&#x27;</code>
- Action 14: <code>`PRESS` enter</code>

### 5. Sort a full table by a column in ascending order

Skill ID: `3a7c8185-25c1-4941-bd7b-96e823c9f21f.skill-01`

Procedure:

1. Click the header of the column that should control the ordering, such as column A, to select the entire column.
2. Click the ascending-sort toolbar icon (A–Z with a downward arrow).
3. If Calc asks whether to extend the selection, choose “Extend selection” so values in adjacent columns move together with their original rows.

Efficiency tip: Select a cell or the full key column before using the toolbar sort button; when Calc offers to extend the selection, choose it so every row stays intact rather than sorting just one column.

Source task: `3a7c8185-25c1-4941-bd7b-96e823c9f21f`

Source instruction: Sort the data according to column A in an ascending order and then create a line chart with the "Date Time" column on the X-axis and quantity on the Y-axis.

Directly referenced source actions:

- Action 0: <code>`CLICK` on the A grey cell to select the entire column</code>
- Action 1: <code>`CLICK` the ascending sort icon az with the down arrow</code>
- Action 2: <code>`CLICK` extend selection</code>

## Initial state preview

### Catalog

![Catalog.png](artifact/previews/Catalog.png)

### Dispatch Log

![Dispatch_Log.png](artifact/previews/Dispatch_Log.png)

### Summary

![Summary.png](artifact/previews/Summary.png)

## Operator guide

### Existing operation-intent guide

#### Demonstration 1

- Skill: `7e429b8d-a3f0-4ed0-9b58-08957d00b127.skill-01`
- Intent: Classify every Dispatch_Log record by looking up its SKU in Catalog and returning the corresponding Supply Group with an exact-match VLOOKUP.
- Efficiency: Enter the first lookup with an absolute Catalog table range, then fill it down the Supply Group column so the fixed reference does not drift.
- Visible success: Every previously blank Supply Group cell contains the appropriate category, including repeated SKUs returning the same category.

#### Demonstration 2

- Skill: `21ab7b40-77c2-4ae6-8321-e00d3a086c73.skill-04`
- Intent: Create a formula-based conditional-formatting rule on Dispatch_Log Restock Cost values that visibly flags the unique highest cost in the log.
- Efficiency: Apply one rule to the entire Restock Cost data range and use a relative current-row reference with an absolute maximum range.
- Visible success: Only the row/cell containing the 540.00 Restock Cost receives the chosen highlight style.

#### Demonstration 3

- Skill: `0bf05a7d-b28b-44d2-955a-50b41e24012a.skill-01`
- Intent: Generate seven-character, leading-zero Ticket Code text values for all dispatch records from their numeric ticket numbers.
- Efficiency: Create the TEXT formula once from the numeric Ticket Number and fill it down rather than editing codes individually.
- Visible success: Ticket Code displays values such as 0004821 and 0000930 as fixed-width text for every record.

#### Demonstration 4

- Skill: `26a8440e-c166-4c50-aef4-bfb77314b46b.skill-03`
- Intent: Calculate the Total Units Dispatched metric in Summary from the Units Dispatched range on Dispatch_Log using a cross-sheet range-total formula.
- Efficiency: Use one SUM formula that references the Units Dispatched range on Dispatch_Log rather than manually adding values.
- Visible success: Summary!B2 shows the aggregate dispatched-unit total, 649, and it is formula-derived.

#### Demonstration 5

- Skill: `3a7c8185-25c1-4941-bd7b-96e823c9f21f.skill-01`
- Intent: Order the complete Dispatch_Log table by SKU in ascending alphabetical order.
- Efficiency: Sort the whole contiguous log, or extend the selection when prompted, so ticket details, costs, and generated values travel with their SKU rows.
- Visible success: Dispatch_Log records are in ascending SKU order from SKU-104 through SKU-426 with intact row associations.

Recording start: Open the supplied Replenishment Review workbook with the Catalog reference data, unsorted Dispatch_Log inputs, blank derived columns, and blank Summary total.

Recording end: The dispatch log is SKU-ascending, fully classified and assigned seven-digit text ticket codes, its unique largest restock cost is visibly formula-highlighted, and Summary shows the cross-sheet total of 649 units.

Allowed variation: The expert may perform the sort before or after filling formulas and may use equivalent range-selection or autofill methods. Use LibreOffice Calc-compatible argument separators and an equivalent visible conditional style, while retaining an exact-match lookup and a formula-based maximum test.

### 中文详细参考方案

> 以下是一个可以参考的操作 guide。标注者可以根据实际 LibreOffice 界面采用等价操作。

本指南完成 Replenishment Review 工作簿的管理复核：从 Catalog 查找每条调度记录的 Supply Group，生成七位 Ticket Code，突出显示唯一最高的 Restock Cost，将完整 Dispatch_Log 按 SKU 升序排列，并在 Summary 汇总已调度单位数。

#### 启动后的初始状态检查

- 打开 Replenishment Review 工作簿，确认底部有 Catalog、Dispatch_Log 和 Summary 三个工作表。
- 在 Catalog 中确认 A1:B9 是 SKU 与 Supply Group 的参考表，且第 2 至第 9 行有八个 SKU 记录。
- 在 Dispatch_Log 中确认标题位于第 1 行，A:D 列已有 18 条记录，E2:E19（Supply Group）和 F2:F19（Ticket Code）仍为空；当前记录尚未按 SKU 排序。
- 在 Summary 中确认 A2 为 Total Units Dispatched，且 B2 为空、没有预先存在的公式。

#### 第 1 步：按 SKU 查找 Supply Group

1. 切换到 Dispatch_Log 工作表，单击 E2。
2. 输入精确匹配查找公式：`=VLOOKUP(B2;$Catalog.$A$2:$B$9;2;FALSE)`，然后按 Enter。此公式用本行 B 列的 SKU 到 Catalog 的固定 A2:B9 表中查找，并返回第 2 列 Supply Group。
3. 再次选中 E2，将选择范围扩展至 E2:E19，然后使用“工作表 > 填充单元格 > 向下填充”，或按 Ctrl+D，把公式填充到所有调度记录。若 Calc 的公式参数分隔符显示为逗号，可使用该环境接受的逗号分隔符，引用结构和 `FALSE` 保持不变。

- 对应 skills：`7e429b8d-a3f0-4ed0-9b58-08957d00b127.skill-01`
- 高效操作：先在首个数据行建立公式，再把该公式填充到整段区域；这样可避免逐行输入并减少引用错误。
- 完成标志：Dispatch_Log 的 E2:E19 都有分类文本；例如 SKU-305 对应 Hand Tools，重复出现的同一 SKU 显示相同分类。

#### 第 2 步：生成七位 Ticket Code

1. 在 Dispatch_Log 中单击 F2。
2. 输入公式 `=TEXT(A2;"0000000")`，然后按 Enter。A2 是本行的 Ticket Number；七个 0 要求显示结果固定为七位。
3. 选中 F2，并将范围扩展为 F2:F19；使用“工作表 > 填充单元格 > 向下填充”或 Ctrl+D 填满该列。

- 对应 skills：`0bf05a7d-b28b-44d2-955a-50b41e24012a.skill-01`
- 高效操作：用 TEXT 公式保留原始票号的数值来源，同时得到适合标识符显示的固定七位文本，不必手工添加前导零。
- 完成标志：F2:F19 均显示七位代码；例如 F2 显示 0004821，而票号为 930 的记录显示 0000930。

#### 第 3 步：突出显示最高 Restock Cost

1. 选中 Dispatch_Log 中的 Restock Cost 数据区域 D2:D19，不要包含标题 D1。
2. 打开“格式 > 条件 > 条件”。在条件类型下拉列表中选择 `Formula is`。
3. 输入公式 `$D2=MAX($D$2:$D$19)`。其中 `$D2` 会随规则检查的行而变化，`$D$2:$D$19` 始终是完整成本范围。
4. 为条件选择或新建一个清晰可见的样式。例如新建样式后，在字体颜色中设置绿色 `#00FF00`，也可同时选择易辨认的填充色；确认样式和条件格式对话框以保存规则。

- 对应 skills：`21ab7b40-77c2-4ae6-8321-e00d3a086c73.skill-04`
- 高效操作：让一个条件格式规则覆盖整个成本数据区域；公式中锁定列和最大值范围、保留行号相对变化，便可逐行判断。
- 完成标志：D2:D19 中仅金额 540.00 的一个单元格显示所选的突出样式，其他成本单元格保持普通样式。

#### 第 4 步：在 Summary 汇总已调度单位数

1. 切换到 Summary 工作表并单击 B2。
2. 输入公式 `=SUM($Dispatch_Log.C2:C19)`，然后按 Enter。该公式汇总 Dispatch_Log 工作表 C2:C19 中的 Units Dispatched。
3. 保持 B2 为公式单元格，不要将结果值覆盖为手工输入的数字。

- 对应 skills：`26a8440e-c166-4c50-aef4-bfb77314b46b.skill-03`
- 高效操作：使用跨工作表 SUM 公式可在原始记录变化时自动更新汇总，无需手工相加。
- 完成标志：Summary!B2 显示 649；选中 B2 时，编辑栏中可见以 `=SUM(` 开头且引用 Dispatch_Log 的公式。

#### 第 5 步：按 SKU 对完整 Dispatch_Log 升序排序

1. 回到 Dispatch_Log。单击 SKU 列中任意一个数据单元格，例如 B2；也可以单击列标题 B 选择该列。
2. 单击工具栏上的升序排序按钮（A–Z 和向下箭头）。
3. 如果出现排序范围提示，选择“扩展选择”，使 A:F 的完整记录同行移动。若打开了排序设置对话框，选择按 SKU 列升序排序，并确认数据包含标题行。

- 对应 skills：`3a7c8185-25c1-4941-bd7b-96e823c9f21f.skill-01`
- 高效操作：排序时让 Calc 扩展选择范围，确保每条记录的所有字段一起移动，而不会只重排 SKU 列。
- 完成标志：Dispatch_Log 的数据从 SKU-104 开始并以 SKU-426 结束；每条记录的 Supply Group、Ticket Code、Units Dispatched 和 Restock Cost 仍与本行票号对应。

#### 第 6 步：完成最终检查

1. 在 Dispatch_Log 检查 E、F 两列均覆盖至第 19 行，并确认高亮仍跟随金额 540.00 所在记录。
2. 检查 Dispatch_Log 的 SKU 顺序为从小到大的字母数字顺序，且没有拆散任一行的记录内容。
3. 在 Summary 选中 B2，确认显示结果为 649，并在编辑栏确认它仍是 `=SUM($Dispatch_Log.C2:C19)` 公式。

- 对应 skills：无；这是准备或检查步骤。
- 高效操作：最后在两个工作表各抽查一个公式结果和一个异常标记，可快速发现填充范围、排序范围或引用范围遗漏。
- 完成标志：三个目标均可见：完整分类和七位代码、唯一最高成本突出显示、SKU 升序日志，以及 Summary 中公式得出的 649。

#### 最终结果检查

- 在 Dispatch_Log 中检查数据行已按 SKU 升序排列：先是 SKU-104，随后依次为 SKU-118、SKU-203、SKU-217、SKU-305、SKU-322、SKU-411，最后为 SKU-426；同一行的票号、数量、成本、分类和代码仍相互对应。
- 确认 Dispatch_Log!E2:E19 均不再为空，且 SKU 相同的记录得到相同的 Supply Group 分类。
- 确认 Dispatch_Log!F2:F19 都显示七位 Ticket Code；例如票号 4821 显示为 0004821，票号 930 显示为 0000930。
- 确认 Restock Cost 中只有数值 540.00 的单元格具有所选的条件格式突出显示。
- 切换到 Summary，确认 B2 显示 649；选中 B2 后，编辑栏显示跨工作表的 SUM 公式，而不是手工输入的常数。

## Source-task similarity review

| Measure | Maximum | Most similar source task |
| --- | ---: | --- |
| Lexical sequence similarity | 0.299766 | 0a2e43bf-b26c-4631-a966-af9dfa12c9e5 |
| Semantic cosine similarity | 0.434468 | 51719eea-10bc-4246-a428-ac7c433dd4b3 |

Similarity scores are reviewer aids, not automatic acceptance thresholds. Inspect the contributing source tasks and their complete ordered actions below.

### Source task `0bf05a7d-b28b-44d2-955a-50b41e24012a`

Original instruction:

> I would like to copy all the numbers in the 'Old ID' column to the 'New 7 Digit Id' column, and pad them with zeros in front, to fill them up to seven digits.

Required skills derived from this source task:

- **Format a numeric cell value as fixed-width text with leading zeros** — `0bf05a7d-b28b-44d2-955a-50b41e24012a.skill-01`

Complete ordered single-action sequence:

| Action | Related required skill | Original single action |
| ---: | --- | --- |
| 0 | <strong>★ Format a numeric cell value as fixed-width text with leading zeros</strong><br><code>0bf05a7d-b28b-44d2-955a-50b41e24012a.skill-01</code> | <strong><code>`DOUBLE_CLICK` cell D2</code></strong> |
| 1 | <strong>★ Format a numeric cell value as fixed-width text with leading zeros</strong><br><code>0bf05a7d-b28b-44d2-955a-50b41e24012a.skill-01</code> | <strong><code>`TYPING` &#x27;=TEXT(C2,&quot;0000000&quot;)&#x27; in the formula bar</code></strong> |
| 2 |  | <code>`CLICK` cell D2</code> |
| 3 |  | <code>`DOUBLE_CLICK` the bottom right corner of cell D2</code> |

### Source task `21ab7b40-77c2-4ae6-8321-e00d3a086c73`

Original instruction:

> Please calculate the period rate for my data in a new column with header "Period Rate (%)", convert the results as number type, and highlight the highest result with green (#00ff00) font.

Required skills derived from this source task:

- **Configure a formula-based conditional formatting rule** — `21ab7b40-77c2-4ae6-8321-e00d3a086c73.skill-04`

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
| 8 | <strong>★ Configure a formula-based conditional formatting rule</strong><br><code>21ab7b40-77c2-4ae6-8321-e00d3a086c73.skill-04</code> | <strong><code>`CLICK` format</code></strong> |
| 9 | <strong>★ Configure a formula-based conditional formatting rule</strong><br><code>21ab7b40-77c2-4ae6-8321-e00d3a086c73.skill-04</code> | <strong><code>`MOVE_TO` &#x27;conditional...&#x27;</code></strong> |
| 10 | <strong>★ Configure a formula-based conditional formatting rule</strong><br><code>21ab7b40-77c2-4ae6-8321-e00d3a086c73.skill-04</code> | <strong><code>`CLICK` &#x27;condition&#x27;</code></strong> |
| 11 | <strong>★ Configure a formula-based conditional formatting rule</strong><br><code>21ab7b40-77c2-4ae6-8321-e00d3a086c73.skill-04</code> | <strong><code>`CLICK` &#x27;cell value&#x27; dropdown</code></strong> |
| 12 | <strong>★ Configure a formula-based conditional formatting rule</strong><br><code>21ab7b40-77c2-4ae6-8321-e00d3a086c73.skill-04</code> | <strong><code>`CLICK` &#x27;Formula is&#x27; option</code></strong> |
| 13 | <strong>★ Configure a formula-based conditional formatting rule</strong><br><code>21ab7b40-77c2-4ae6-8321-e00d3a086c73.skill-04</code> | <strong><code>`CLICK` text field</code></strong> |
| 14 | <strong>★ Configure a formula-based conditional formatting rule</strong><br><code>21ab7b40-77c2-4ae6-8321-e00d3a086c73.skill-04</code> | <strong><code>`TYPING` $C2=MAX($C$2:$C$25)</code></strong> |
| 15 |  | <code>`CLICK` accent dropdown</code> |
| 16 |  | <code>`CLICK` new style</code> |
| 17 |  | <code>`CLICK` font effects</code> |
| 18 |  | <code>`CLICK` font color dropdown</code> |
| 19 |  | <code>`CLICK` custom color...</code> |
| 20 |  | <code>`DOUBLE_CLICK` Hex text box</code> |
| 21 |  | <code>`TYPING` &#x27;00ff00&#x27;</code> |
| 22 |  | <code>`PRESS` enter</code> |
| 23 |  | <code>`CLICK` OK</code> |
| 24 | <strong>★ Configure a formula-based conditional formatting rule</strong><br><code>21ab7b40-77c2-4ae6-8321-e00d3a086c73.skill-04</code> | <strong><code>`CLICK` OK</code></strong> |

### Source task `26a8440e-c166-4c50-aef4-bfb77314b46b`

Original instruction:

> Create a table with two column headers ("Month" and "Total") in a new sheet named "Sheet2" to show the total sales for all months.

Required skills derived from this source task:

- **Build a cross-sheet range-total formula** — `26a8440e-c166-4c50-aef4-bfb77314b46b.skill-03`

Complete ordered single-action sequence:

| Action | Related required skill | Original single action |
| ---: | --- | --- |
| 0 |  | <code>`CLICK` on cell B1</code> |
| 1 |  | <code>`DRAG_TO` cell G1</code> |
| 2 |  | <code>`HOTKEY` ctrl+c</code> |
| 3 |  | <code>`CLICK` on the + button next to Sheet1 to add a new sheet</code> |
| 4 |  | <code>`TYPING` &#x27;Month&#x27;</code> |
| 5 |  | <code>`PRESS` tab</code> |
| 6 |  | <code>`TYPING` &#x27;Total&#x27;</code> |
| 7 |  | <code>`PRESS` enter</code> |
| 8 |  | <code>`MOVE_TO` cell A2</code> |
| 9 |  | <code>`RIGHT_CLICK`</code> |
| 10 |  | <code>`MOVE_TO` paste special</code> |
| 11 |  | <code>`CLICK` transpose</code> |
| 12 | <strong>★ Build a cross-sheet range-total formula</strong><br><code>26a8440e-c166-4c50-aef4-bfb77314b46b.skill-03</code> | <strong><code>`CLICK` cell B2</code></strong> |
| 13 | <strong>★ Build a cross-sheet range-total formula</strong><br><code>26a8440e-c166-4c50-aef4-bfb77314b46b.skill-03</code> | <strong><code>`TYPING` &#x27;=SUM($Sheet1.B2:B11)&#x27;</code></strong> |
| 14 | <strong>★ Build a cross-sheet range-total formula</strong><br><code>26a8440e-c166-4c50-aef4-bfb77314b46b.skill-03</code> | <strong><code>`PRESS` enter</code></strong> |
| 15 |  | <code>`CLICK` B2</code> |
| 16 |  | <code>`MOVE_TO` bottom right corner of the cell B2</code> |
| 17 |  | <code>`DRAG_TO` G1</code> |
| 18 |  | <code>`HOTKEY` ctrl+x</code> |
| 19 |  | <code>`CLICK` on B2</code> |
| 20 |  | <code>`RIGHT_CLICK`</code> |
| 21 |  | <code>`MOVE_TO` paste special</code> |
| 22 |  | <code>`CLICK` transpose</code> |

### Source task `3a7c8185-25c1-4941-bd7b-96e823c9f21f`

Original instruction:

> Sort the data according to column A in an ascending order and then create a line chart with the "Date Time" column on the X-axis and quantity on the Y-axis.

Required skills derived from this source task:

- **Sort a full table by a column in ascending order** — `3a7c8185-25c1-4941-bd7b-96e823c9f21f.skill-01`

Complete ordered single-action sequence:

| Action | Related required skill | Original single action |
| ---: | --- | --- |
| 0 | <strong>★ Sort a full table by a column in ascending order</strong><br><code>3a7c8185-25c1-4941-bd7b-96e823c9f21f.skill-01</code> | <strong><code>`CLICK` on the A grey cell to select the entire column</code></strong> |
| 1 | <strong>★ Sort a full table by a column in ascending order</strong><br><code>3a7c8185-25c1-4941-bd7b-96e823c9f21f.skill-01</code> | <strong><code>`CLICK` the ascending sort icon az with the down arrow</code></strong> |
| 2 | <strong>★ Sort a full table by a column in ascending order</strong><br><code>3a7c8185-25c1-4941-bd7b-96e823c9f21f.skill-01</code> | <strong><code>`CLICK` extend selection</code></strong> |
| 3 |  | <code>`CLICK` on the A cell to select the entire column</code> |
| 4 |  | <code>`KEY_DOWN` ctrl</code> |
| 5 |  | <code>`CLICK` on the E cell to select the entire column</code> |
| 6 |  | <code>`CLICK` on the insert chart icon (3 bars)</code> |
| 7 |  | <code>`CLICK` line</code> |
| 8 |  | <code>`CLICK` the line only chart icon (3rd from the right)</code> |
| 9 |  | <code>`PRESS` enter</code> |

### Source task `7e429b8d-a3f0-4ed0-9b58-08957d00b127`

Original instruction:

> I have a lookup table for the officers of each branch. Please, here is another table in which I need to fill with the officer names according the headoffice (i.e., the branch name). Help me to complete this.

Required skills derived from this source task:

- **Enter an exact-match VLOOKUP formula** — `7e429b8d-a3f0-4ed0-9b58-08957d00b127.skill-01`

Complete ordered single-action sequence:

| Action | Related required skill | Original single action |
| ---: | --- | --- |
| 0 | <strong>★ Enter an exact-match VLOOKUP formula</strong><br><code>7e429b8d-a3f0-4ed0-9b58-08957d00b127.skill-01</code> | <strong><code>`CLICK` F2</code></strong> |
| 1 | <strong>★ Enter an exact-match VLOOKUP formula</strong><br><code>7e429b8d-a3f0-4ed0-9b58-08957d00b127.skill-01</code> | <strong><code>`TYPING` =VLOOKUP(E2, $A$2:$B$7, 2, FALSE)</code></strong> |
| 2 | <strong>★ Enter an exact-match VLOOKUP formula</strong><br><code>7e429b8d-a3f0-4ed0-9b58-08957d00b127.skill-01</code> | <strong><code>`PRESS` Enter.</code></strong> |
| 3 |  | <code>`CLICK` F2</code> |
| 4 |  | <code>`DOUBLE_CLICK` the bottom right corner of cell F2</code> |

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
