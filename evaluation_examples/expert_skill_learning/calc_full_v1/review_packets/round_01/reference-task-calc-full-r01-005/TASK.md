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

本指南完成补货审查工作簿：从 `Catalog` 查找每条发运记录的 Supply Group，生成七位 Ticket Code，突出唯一最高的 Restock Cost，在 `Summary` 汇总已发运单位数，并将完整 `Dispatch_Log` 按 SKU 升序排列。

#### 启动后的初始状态检查

- 确认工作簿已打开，并且可见工作表 `Catalog`、`Dispatch_Log` 和 `Summary`。
- 在 `Catalog` 中确认 `A1:B9` 是 SKU 与 Supply Group 的参考表，数据从第 2 行到第 9 行。
- 在 `Dispatch_Log` 中确认第 1 行包含 `Ticket Number`、`SKU`、`Units Dispatched`、`Restock Cost`、`Supply Group`、`Ticket Code`，且 `E2:E19` 与 `F2:F19` 目前为空。
- 确认 `Summary!B2` 为空，且 `Dispatch_Log` 的 SKU 当前尚未按字母顺序排列。

#### 第 1 步：确认发运日志的目标列

1. 切换到 `Dispatch_Log` 工作表，确认数据记录范围是第 2 行到第 19 行。
2. 确认 `SKU` 位于 B 列、空白的 `Supply Group` 位于 E 列、空白的 `Ticket Code` 位于 F 列；`Restock Cost` 位于 D 列。

- 对应 skills：无；这是准备或检查步骤。
- 高效操作：先确认列和行范围，可避免将公式填入标题行或遗漏最后一条记录。
- 完成标志：可以看到 `Dispatch_Log` 的 `E2:E19` 和 `F2:F19` 是待填充区域，且 A 到 D 列已有 18 条发运记录。

#### 第 2 步：用精确匹配查找填充 Supply Group

1. 在 `Dispatch_Log` 中选择单元格 `E2`。
2. 输入精确匹配公式 `=VLOOKUP(B2;$Catalog.$A$2:$B$9;2;FALSE)`，然后按 `Enter`。该公式用本行 SKU 在 `Catalog` 中查找并返回第二列的 Supply Group。
3. 再次选中 `E2`，然后将选择扩展到 `E2:E19`，按 `Ctrl+D` 向下填充公式。
4. 若 `E2` 已显示与 B2 中 SKU 对应的类别，则不需要调整公式。若出现 `#N/A`，检查 B2 的 SKU 是否与 `Catalog!A2:A9` 中的文本完全一致，并确认公式中的查找范围仍是 `$Catalog.$A$2:$B$9`、最后一个参数仍为 `FALSE`。

- 对应 skills：`7e429b8d-a3f0-4ed0-9b58-08957d00b127.skill-01`
- 高效操作：使用绝对引用 `$Catalog.$A$2:$B$9` 固定查找表；随后向下填充时，查找表不会随行号移动。
- 完成标志：`E2:E19` 不再为空，每条记录均显示 Supply Group；相同的 SKU 显示相同分类。

#### 第 3 步：生成七位 Ticket Code

1. 选择 `Dispatch_Log!F2`。
2. 输入公式 `=TEXT(A2;"0000000")`，然后按 `Enter`。该公式将数值 Ticket Number 转换为固定七位的文本显示。
3. 选中 `F2` 并将选择扩展到 `F2:F19`，按 `Ctrl+D` 填充其余记录。
4. 若 `F2` 已显示七个字符的代码，例如 `0004821`，不需要调整。若显示的位数少于七位，双击 `F2` 并确认格式字符串准确为 `"0000000"`，然后重新向下填充。

- 对应 skills：`0bf05a7d-b28b-44d2-955a-50b41e24012a.skill-01`
- 高效操作：只需在第一行输入一次 `TEXT` 公式，再用 `Ctrl+D` 填满整列，可避免逐条手动补零。
- 完成标志：`F2:F19` 均显示七位 Ticket Code；例如 Ticket Number `4821` 显示为 `0004821`，`930` 显示为 `0000930`。

#### 第 4 步：用公式条件格式标记最高 Restock Cost

1. 在 `Dispatch_Log` 中选中范围 `D2:D19`。
2. 打开 `Format` > `Conditional` > `Condition...`。
3. 在条件类型下拉列表中选择 `Formula is`，并输入公式 `$D2=MAX($D$2:$D$19)`。
4. 在该对话框的样式区域选择或创建一个明显可见的高亮样式，然后确认对话框以保存规则。
5. 保存后，若只有 `540.00` 的 Restock Cost 单元格被高亮，则不需要调整。若多个单元格被高亮，重新打开 `Format` > `Conditional` > `Condition...`，确认公式中的当前行引用是 `$D2`，而最大值范围准确为 `$D$2:$D$19`。

- 对应 skills：`21ab7b40-77c2-4ae6-8321-e00d3a086c73.skill-04`
- 高效操作：同一条公式规则应用于完整成本范围即可；`$D2` 固定成本列但保留相对行号，规则会逐行判断。
- 完成标志：在 D2:D19 中，只有数值 `540.00` 的 Restock Cost 单元格具有所选的明显高亮样式。

#### 第 5 步：在 Summary 汇总已发运单位数

1. 切换到 `Summary` 工作表并选择 `B2`，即 `Total Units Dispatched` 标签右侧的空白值单元格。
2. 输入 `=SUM($Dispatch_Log.C2:C19)`，然后按 `Enter`。
3. 若 B2 已显示公式计算出的总数 `649`，不需要调整。若 B2 显示错误或为空，双击 B2，确认公式以 `=` 开头、工作表名称为 `$Dispatch_Log`，并且汇总范围为 `C2:C19`，再按 `Enter`。

- 对应 skills：`26a8440e-c166-4c50-aef4-bfb77314b46b.skill-03`
- 高效操作：用一个跨工作表 `SUM` 公式汇总完整 Units Dispatched 范围，比逐项相加更快且能随源数据更新。
- 完成标志：`Summary!B2` 显示公式结果 `649`，并且选择该单元格时可在输入行看到跨工作表 `SUM` 公式。

#### 第 6 步：按 SKU 升序排序完整 Dispatch_Log

1. 返回 `Dispatch_Log`，选中完整范围 `A1:F19`，包括标题行和所有 18 条记录。
2. 打开 `Data` > `Sort...`。在排序设置中将排序依据设为 `SKU`，选择 `Ascending`，并指定该范围包含列标题后确认。
3. 完成后，若第 1 行仍是原来的标题且 SKU 从 `SKU-104` 逐步排到 `SKU-426`，不需要调整。若标题行被混入数据排序，立即再次选中 `A1:F19`，打开 `Data` > `Sort...`，启用范围包含列标题的设置，再按 `SKU` 的 `Ascending` 重排。
4. 若使用工具栏的 A–Z 升序排序图标而 Calc 询问是否扩展选择，请选择 `Extend selection`，使 A 到 F 列的同一条记录一起移动。

- 对应 skills：`3a7c8185-25c1-4941-bd7b-96e823c9f21f.skill-01`
- 高效操作：先选择完整的 `A1:F19` 连续表格，可使所有字段跟随各自 SKU 的记录一起移动，不会破坏行内关联。
- 完成标志：`Dispatch_Log` 从 `SKU-104` 开始并以 `SKU-426` 结束，所有记录字段仍保持正确的行内对应关系，最高成本的条件格式高亮也随该记录保留。

#### 第 7 步：进行最终核对并保存

1. 检查 `Dispatch_Log`：E 列全部有分类、F 列全部是七位代码，且 D 列仅有一个 `540.00` 高亮。
2. 检查 `Summary!B2` 是否保留公式并显示总计 `649`。
3. 使用 `File` > `Save` 保存完成后的工作簿。

- 对应 skills：无；这是准备或检查步骤。
- 高效操作：最终一次同时检查公式结果、显示格式和排序状态，可在保存前发现遗漏。
- 完成标志：工作簿已保存，发运日志已分类、补零编码、突出最高成本并按 SKU 升序排列，Summary 中已显示总单位数。

#### 最终结果检查

- 在 `Dispatch_Log` 中，`SKU` 已按 A–Z 排列，从 `SKU-104` 到 `SKU-426`；每一行的 Ticket Number、Units Dispatched、Restock Cost、Supply Group 和 Ticket Code 仍与该行 SKU 对应。
- `Dispatch_Log!E2:E19` 都有 Supply Group 分类，重复 SKU 的分类一致；例如 `SKU-104` 对应 `Fasteners`，`SKU-322` 对应 `Electrical`。
- `Dispatch_Log!F2:F19` 都显示七位 Ticket Code，例如 Ticket Number `4821` 显示为 `0004821`，Ticket Number `930` 显示为 `0000930`。
- Restock Cost 中只有数值 `540.00` 的单元格具有所选的明显条件格式高亮，其他 Restock Cost 单元格没有该高亮。
- `Summary!B2` 含有跨工作表的 `SUM` 公式，并显示 Total Units Dispatched 的目标总计 `649`。

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
