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

此工作簿用于完成补货调度复核：从 `Catalog` 分类全部调度记录，为票号生成七位文本代码，标记唯一最高补货成本，汇总调度单位数，并按 SKU 排序完整日志。开始前不要覆盖已有表头或原始 A–D 列数据。

#### 启动后的初始状态检查

- 确认工作簿中有 `Catalog`、`Dispatch_Log` 和 `Summary` 三个工作表。
- 在 `Catalog` 中确认 `A1:B9` 是 SKU 与 Supply Group 的对照表，数据范围为 `A2:B9`。
- 在 `Dispatch_Log` 中确认 `A1:F19` 有表头，`E2:E19` 和 `F2:F19` 为空，且原始记录尚未按 SKU 排序。
- 确认 `Summary!B2` 为空；`Dispatch_Log` 中尚未出现 Restock Cost 的条件格式高亮。

#### 第 1 步：用 SKU 查找并填充 Supply Group

1. 切换到 `Dispatch_Log` 工作表，单击 `E2`。
2. 输入精确匹配查找公式：`=VLOOKUP(B2,$Catalog.$A$2:$B$9,2,FALSE)`，然后按 `Enter`。如果当前 Calc 设置要求用分号分隔参数，则输入等价公式 `=VLOOKUP(B2;$Catalog.$A$2:$B$9;2;FALSE)`。
3. 再次选中 `E2`，将该公式向下填充到 `E19`。可复制 `E2`，选中 `E3:E19` 后粘贴；也可使用单元格右下角的填充柄向下拖动。

- 对应 skills：`7e429b8d-a3f0-4ed0-9b58-08957d00b127.skill-01`
- 高效操作：先只在第一条记录写公式，再用填充一次性覆盖其余 17 条记录；查找表范围使用绝对引用，向下填充时不会移动。
- 完成标志：`E2:E19` 不再为空。每个 SKU 都显示对应类别，例如 `SKU-305` 显示 `Hand Tools`，相同 SKU 的类别相同。

#### 第 2 步：生成七位 Ticket Code

1. 在仍为 `Dispatch_Log` 的工作表中，单击 `F2`。
2. 输入 `=TEXT(A2,"0000000")`，然后按 `Enter`。该公式把数值票号显示为七位文本，而不改变 A 列原始数值。
3. 选中 `F2`，将公式向下填充至 `F19`，可复制后粘贴到 `F3:F19`，或用填充柄完成。

- 对应 skills：`0bf05a7d-b28b-44d2-955a-50b41e24012a.skill-01`
- 高效操作：`TEXT` 的格式字符串固定为七个零；只建立一次公式并填充，可避免手工输入前导零时遗漏位数。
- 完成标志：`F2:F19` 全部有值，并出现固定七位显示，例如 `0004821`、`0000930` 和 `0017654`。

#### 第 3 步：条件格式标记最高 Restock Cost

1. 在 `Dispatch_Log` 中选择 Restock Cost 数据范围 `D2:D19`，不要包含表头 `D1`。
2. 打开 `Format` > `Conditional` > `Condition`。
3. 在条件类型下拉选项中选择 `Formula is`。
4. 输入公式 `$D2=MAX($D$2:$D$19)`。这里的 `$D2` 会随规则向下检查各行，而 `$D$2:$D$19` 始终比较整段成本数据。
5. 通过此对话框中的样式选择或样式创建控件，为命中的单元格指定明显可见的高亮样式，例如醒目的填充色或字体色，然后确认对话框保存规则。

- 对应 skills：`21ab7b40-77c2-4ae6-8321-e00d3a086c73.skill-04`
- 高效操作：先选择完整成本数据范围，再以当前行相对、最大值范围绝对的公式建立一条规则，即可评估所有 18 条记录。
- 完成标志：在 `D2:D19` 中，只有显示 `540.00` 的单元格具有所选高亮；其余 Restock Cost 单元格保持普通外观。

#### 第 4 步：汇总 Total Units Dispatched

1. 切换到 `Summary` 工作表并单击 `B2`。
2. 输入跨工作表汇总公式 `=SUM($Dispatch_Log.C2:C19)`，然后按 `Enter`。
3. 确认不要把总数作为普通数字手工键入；保留公式，以便结果与 `Dispatch_Log` 的 Units Dispatched 数据保持联动。

- 对应 skills：`26a8440e-c166-4c50-aef4-bfb77314b46b.skill-03`
- 高效操作：直接对完整源范围使用一个 `SUM` 跨表公式，既可避免手工加总，也会在调度单位变化时自动更新。
- 完成标志：`Summary!B2` 显示 `649`；选中该单元格时，输入栏中可见 `=SUM($Dispatch_Log.C2:C19)`。

#### 第 5 步：按 SKU 升序排列完整 Dispatch_Log

1. 返回 `Dispatch_Log`，选中完整日志范围 `A1:F19`，包括表头和所有 18 条记录。
2. 使用工具栏上的升序排序图标（带向下箭头的 A–Z 图标）进行升序排序。若 Calc 显示是否扩展选择的提示，选择 `Extend selection`，使整行数据一起排序。
3. 如果出现排序设置对话框，指定按 `SKU` 升序排序，并将第一行作为表头处理后确认。

- 对应 skills：`3a7c8185-25c1-4941-bd7b-96e823c9f21f.skill-01`
- 高效操作：排序前选中整块连续日志数据，而非只移动 SKU 列；这样所有票号、单位数、成本及派生结果都会跟随所属记录移动。
- 完成标志：日志第一组记录的 SKU 为 `SKU-104`，随后依次为 `SKU-118`、`SKU-203`、`SKU-217`、`SKU-305`、`SKU-322`、`SKU-411`、`SKU-426`；对应的 Supply Group、Ticket Code、单位数和成本均仍与各自记录同行。

#### 第 6 步：完成最终核对并保存

1. 检查 `Dispatch_Log`：确认 `E2:E19` 和 `F2:F19` 均完整填充，`D` 列只有 `540.00` 被高亮，并且 SKU 已升序。
2. 检查 `Summary!B2`：确认结果为 `649` 且它是公式计算结果。
3. 如有未保存的修改，使用 `File` > `Save` 保存工作簿。

- 对应 skills：无；这是准备或检查步骤。
- 高效操作：使用工作表标签逐项检查关键输出，比逐行重新计算更快；尤其要确认排序后公式结果和条件格式仍附着在正确记录上。
- 完成标志：三个工作表均呈现完整结果：分类和代码已填满、最大成本已标记、汇总为 `649`，并且完整调度日志按 SKU 升序排列。

#### 最终结果检查

- `Dispatch_Log` 中的记录按 `SKU` 从 `SKU-104` 到 `SKU-426` 升序排列；每一行的 A–F 列数据仍属于同一条原始记录。
- `Dispatch_Log!E2:E19` 均显示由 `Catalog` 返回的 Supply Group，重复 SKU 的类别一致。
- `Dispatch_Log!F2:F19` 均为七位 Ticket Code 文本；例如票号 `4821` 显示为 `0004821`，票号 `930` 显示为 `0000930`。
- `Dispatch_Log` 的 Restock Cost 数据中，仅数值 `540.00` 具有设置的条件格式高亮。
- `Summary!B2` 显示 `649`，选中该单元格时公式栏显示跨工作表的 `SUM` 公式，而不是手工输入的数字。

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
