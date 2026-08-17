# Dispatch Route Review

- Reference task: `reference-task-r01-003`
- Application: `libreoffice_calc`
- Review decision: `pending`

## Task instruction

Build a delivery route review dashboard: add and name a new worksheet "Route Dashboard", create a list of route-and-tracking tags from the Dispatch Log for every dispatch, and include a Pivot Table showing the number of tracking codes handled by each carrier.

## Required skills

### 1. Rename a worksheet tab

Skill ID: `1954cced-e748-45c4-9c26-9855b97fbc5e.skill-05`

Procedure:

1. Double-click the worksheet tab to enter tab-name editing mode.
2. Type the replacement name, for example `Sheet2`, and press Enter to apply it.

Efficiency tip: Rename a newly created sheet immediately while its tab is active, so later formulas and references can use a meaningful sheet name.

Source task: `1954cced-e748-45c4-9c26-9855b97fbc5e`

Source instruction: Create a Pivot Table in a new sheet (Sheet2) to count how many times each "Invoice No." appears.

Directly referenced source actions:

- Action 11: <code>`DOUBLE_CLICK` Pivot Table Sheet1_1</code>
- Action 12: <code>`TYPING` Sheet2</code>
- Action 13: <code>`PRESS` enter</code>

### 2. Insert a new worksheet from the sheet tab bar

Skill ID: `035f41ba-6653-43ab-aa63-c86d449d62e5.skill-04`

Procedure:

1. Click the plus button beside the existing worksheet tabs; for example, use the plus control next to Sheet1 to add a blank sheet.
2. Calc creates and activates a new worksheet, ready for cell entry.

Efficiency tip: Use the sheet-tab plus button to add a worksheet immediately, without opening a worksheet-management dialog.

Source task: `035f41ba-6653-43ab-aa63-c86d449d62e5`

Source instruction: Help me fill in the Gross profit column by subtracting all the available expenses including discounts, allowances, material and labor charges, and overhead from the actual sale, i.e., the sales after deducting the returns. Then under column A named "Year_Profit" in a new sheet, display the Year Column in Sheet 1 as text appended by a "_" with the corresponding integer digits of Gross Profit value.

Directly referenced source actions:

- Action 5: <code>`CLICK` on + to left of sheet1</code>

### 3. Fill a formula down using the fill handle

Skill ID: `035f41ba-6653-43ab-aa63-c86d449d62e5.skill-03`

Procedure:

1. Select the cell containing the formula to propagate, such as J2 or A2.
2. Move to the small square at the selection's bottom-right corner until the fill-handle cursor is available.
3. Drag the handle down to the final target row, for example from row 2 through row 10.
4. Calc copies the formula into each row and adjusts relative row references automatically.

Efficiency tip: Drag the fill handle directly to the last adjacent row of data rather than copying and pasting formulas one row at a time.

Source task: `035f41ba-6653-43ab-aa63-c86d449d62e5`

Source instruction: Help me fill in the Gross profit column by subtracting all the available expenses including discounts, allowances, material and labor charges, and overhead from the actual sale, i.e., the sales after deducting the returns. Then under column A named "Year_Profit" in a new sheet, display the Year Column in Sheet 1 as text appended by a "_" with the corresponding integer digits of Gross Profit value.

Directly referenced source actions:

- Action 3: <code>`MOVE_TO` bottom right corner of the cell J2`</code>
- Action 4: <code>`DRAG_TO` bottom right corner of the cell J10</code>
- Action 9: <code>`MOVE_TO` bottom right corner of the cell A2`</code>
- Action 10: <code>`DRAG_TO` bottom right corner of the cell A10</code>

### 4. Add a field as a Pivot Table value

Skill ID: `1954cced-e748-45c4-9c26-9855b97fbc5e.skill-03`

Procedure:

1. Locate the field in the Available Fields list in the Pivot Table layout dialog.
2. Drag it to the Data Fields area. For example, adding an identifier field as a data field creates a value summary for each row-label group.

Efficiency tip: Use the same source field in both Row Fields and Data Fields when you need a grouped list together with a summary of each group.

Source task: `1954cced-e748-45c4-9c26-9855b97fbc5e`

Source instruction: Create a Pivot Table in a new sheet (Sheet2) to count how many times each "Invoice No." appears.

Directly referenced source actions:

- Action 5: <code>`MOVE_TO` invoice no. in available fields box</code>
- Action 6: <code>`DRAG_TO` data fields box</code>

### 5. Concatenate cross-sheet cell values in a formula

Skill ID: `035f41ba-6653-43ab-aa63-c86d449d62e5.skill-05`

Procedure:

1. In the destination cell, enter a concatenation formula that joins source values with text separators. For example, type `=$Sheet1.A2&"_"&$Sheet1.J2`.
2. The `&` operator joins the two references and the quoted underscore literal into one text result.
3. In `$Sheet1.A2`, the `$` fixes the source sheet name `Sheet1`; column A and row 2 remain relative, so filling downward changes it to `$Sheet1.A3`. The same behavior applies to `$Sheet1.J2`.

Efficiency tip: Reference the source sheet directly in the formula so the result updates automatically when the source values change.

Source task: `035f41ba-6653-43ab-aa63-c86d449d62e5`

Source instruction: Help me fill in the Gross profit column by subtracting all the available expenses including discounts, allowances, material and labor charges, and overhead from the actual sale, i.e., the sales after deducting the returns. Then under column A named "Year_Profit" in a new sheet, display the Year Column in Sheet 1 as text appended by a "_" with the corresponding integer digits of Gross Profit value.

Directly referenced source actions:

- Action 8: <code>`TYPING` &#x27;=$Sheet1.A2&amp;&quot;_&quot;&amp;$Sheet1.J2&#x27;</code>

## Initial state preview

### Dispatch Log

![Dispatch_Log.png](artifact/previews/Dispatch_Log.png)

## Operator guide

### Existing operation-intent guide

#### Demonstration 1

- Skill: `035f41ba-6653-43ab-aa63-c86d449d62e5.skill-04`
- Intent: Insert a blank worksheet to hold the delivery review dashboard.
- Efficiency: Use the plus control at the sheet-tab bar so the blank dashboard sheet is created directly in the workbook.
- Visible success: A new blank worksheet tab is visible and active beside Dispatch Log.

#### Demonstration 2

- Skill: `1954cced-e748-45c4-9c26-9855b97fbc5e.skill-05`
- Intent: Rename the inserted worksheet to "Route Dashboard".
- Efficiency: Rename the newly active tab before creating formulas or reports so the dashboard has a meaningful, stable name.
- Visible success: The active worksheet tab visibly reads "Route Dashboard".

#### Demonstration 3

- Skill: `035f41ba-6653-43ab-aa63-c86d449d62e5.skill-05`
- Intent: Create the first Route Dashboard tag by concatenating the Dispatch Log Route and Tracking Code values with a readable separator, then use the fill handle to extend it through all 30 dispatch rows.
- Efficiency: Use a formula with a fixed source-sheet reference and relative row references, such as joining Route and Tracking Code, so the copied rows update automatically.
- Visible success: The first tag displays both source values as one text label, and the completed tag column contains corresponding route/tracking labels for rows 2 through 31.

#### Demonstration 4

- Skill: `035f41ba-6653-43ab-aa63-c86d449d62e5.skill-03`
- Intent: Propagate the initial cross-sheet tag formula down the full dispatch-record list using the fill handle.
- Efficiency: Drag the first formula cell's fill handle directly to the last adjacent dispatch row instead of copying formulas row by row.
- Visible success: Each filled tag row has adjusted source-row references and no manual repeated formula entry is needed.

#### Demonstration 5

- Skill: `1954cced-e748-45c4-9c26-9855b97fbc5e.skill-03`
- Intent: In the Pivot Table layout, add Tracking Code as a value/data field for the carrier summary.
- Efficiency: After Carrier has been used as the grouping field, add Tracking Code to the data area to produce a count summary for each carrier.
- Visible success: The Pivot Table visibly shows carrier groups with a numeric Tracking Code count/value column.

Recording start: The workbook contains only the populated Dispatch Log source sheet, with no dashboard sheet, Pivot Table, or tag formulas.

Recording end: Route Dashboard is a renamed inserted worksheet containing a filled list of cross-sheet route/tracking tags and a non-overlapping Pivot Table that summarizes Tracking Code counts by Carrier.

Allowed variation: The expert may place the tag list and Pivot Table in any non-overlapping regions of the new worksheet, use an equivalent Calc-supported method to open the Pivot Table layout, and use a semantically equivalent separator in the concatenated tag formula.

### 中文详细参考方案

> 以下是一个可以参考的操作 guide。标注者可以根据实际 LibreOffice 界面采用等价操作。

本指南将现有“Dispatch Log”中的 30 条派送记录整理到新的“Route Dashboard”工作表：先建立路线与追踪码组合标签，再在同一工作表的另一块空白区域创建按 Carrier 汇总 Tracking Code 数量的 Pivot Table。

#### 启动后的初始状态检查

- 确认工作簿已打开，并且底部当前只显示一个名为“Dispatch Log”的工作表标签。
- 切换到“Dispatch Log”，确认源数据位于 A1:E31：第 1 行是表头，第 2 至 31 行为派送记录；应能看到 Carrier、Tracking Code 和 Route 列。
- 确认工作簿中尚未出现“Route Dashboard”工作表，也没有现成的 Pivot Table 或路线/追踪标签列表。

#### 第 1 步：插入仪表板工作表

1. 在窗口底部的工作表标签栏中，点击“Dispatch Log”标签旁的加号（+）。
2. 等待 Calc 创建并自动激活新的空白工作表。

- 对应 skills：`035f41ba-6653-43ab-aa63-c86d449d62e5.skill-04`
- 高效操作：直接使用工作表标签栏的加号可立即新建空白表，无需打开工作表管理窗口。
- 完成标志：底部出现一个新的空白工作表标签，且该标签处于活动状态。

#### 第 2 步：将新工作表命名为 Route Dashboard

1. 双击刚创建的工作表标签，使标签名称进入编辑状态。
2. 输入 Route Dashboard，然后按 Enter 确认。

- 对应 skills：`1954cced-e748-45c4-9c26-9855b97fbc5e.skill-05`
- 高效操作：在新表仍处于活动状态时马上改名，后续设置公式和 Pivot Table 输出位置时更容易识别目标表。
- 完成标志：活动工作表标签清楚显示为“Route Dashboard”。

#### 第 3 步：创建第一条跨工作表路线/追踪标签

1. 保持在“Route Dashboard”工作表中，选择 A1 并输入一个说明性标题，例如 Route / Tracking Tag。
2. 选择 A2，输入公式 `=$'Dispatch Log'.D2&" - "&$'Dispatch Log'.C2`，然后按 Enter。
3. 该公式将 Dispatch Log 的 Route（D 列）和 Tracking Code（C 列）用 ` - ` 连接。工作表名称被固定，而行号会在向下填充时相应变化。

- 对应 skills：`035f41ba-6653-43ab-aa63-c86d449d62e5.skill-05`
- 高效操作：将标签列表放在左侧，例如 A 列，可在右侧预留连续空白区域给 Pivot Table，避免两者重叠。
- 完成标志：A2 显示一条包含路线名称和追踪码的文本标签，而不是公式错误；公式栏显示对“Dispatch Log”的引用。

#### 第 4 步：使用填充柄完成全部标签

1. 选中包含首个公式的 A2 单元格。
2. 将指针移到选区右下角的小方块（填充柄），直到可以拖动填充。
3. 按住并向下拖动填充柄至 A31，然后释放。
4. 如有需要，点击 A31 检查公式：其中的源行应为 31，而不是仍然引用第 2 行。

- 对应 skills：`035f41ba-6653-43ab-aa63-c86d449d62e5.skill-03`
- 高效操作：用填充柄一次拖到最后一条相邻记录，比逐行复制或反复输入公式更快，并能保留相对行引用。
- 完成标志：A2:A31 都有路线/追踪标签；各行显示对应的追踪码，且没有手工重复录入公式的痕迹。

#### 第 5 步：以 Dispatch Log 源表创建 Pivot Table

1. 切换到“Dispatch Log”工作表。
2. 选择完整源表范围 A1:E31，务必包含第 1 行字段标题。
3. 打开“数据”菜单，进入“数据透视表（Pivot Table）”相关命令，并选择用于插入或创建 Pivot Table 的选项。
4. 在确认源数据范围的界面中，确认范围仍为 Dispatch Log 的 A1:E31，然后继续到 Pivot Table 布局界面。

- 对应 skills：无；这是准备或检查步骤。
- 高效操作：先精确选择含表头的完整源范围，可让 Calc 自动识别 Carrier 和 Tracking Code 等字段名称。
- 完成标志：显示 Pivot Table 布局窗口，并在可用字段列表中能看到 Carrier、Tracking Code、Route 等源表字段。

#### 第 6 步：按 Carrier 分组并添加 Tracking Code 计数

1. 在布局窗口的“可用字段”列表中找到 Carrier，并将其拖到“行字段”区域。
2. 在“可用字段”列表中找到 Tracking Code，并将其拖到“数据字段”区域。
3. 如果数据字段设置没有自动使用计数，打开该数据字段的设置，将汇总函数改为 Count（计数）；不要使用 Sum，因为 Tracking Code 是文本标识。

- 对应 skills：`1954cced-e748-45c4-9c26-9855b97fbc5e.skill-03`
- 高效操作：先把 Carrier 放入行字段建立分组，再将 Tracking Code 放入数据字段；同一承运商的多条派送记录会自动合并为一组。
- 完成标志：布局预览或字段区域中，Carrier 位于行字段，Tracking Code 位于数据字段，并显示为计数类型的汇总值。

#### 第 7 步：将 Pivot Table 放置到 Route Dashboard 的非重叠区域

1. 在 Pivot Table 的输出位置或结果位置设置中，选择输出到现有工作表。
2. 将目标设为“Route Dashboard”工作表的 G1（或该表中其他与 A1:A31 标签区域不重叠的空白区域）。
3. 确认布局和输出位置后，点击确定以生成 Pivot Table。

- 对应 skills：无；这是准备或检查步骤。
- 高效操作：选择一个远离 A 列标签清单的起始单元格，例如 Route Dashboard 的 G1，可为 Pivot Table 的扩展行列保留空间。
- 完成标志：切换或查看“Route Dashboard”时，左侧保留路线/追踪标签列表，右侧空白区域出现 Pivot Table，二者没有覆盖。

#### 第 8 步：核对仪表板结果并保存

1. 在“Route Dashboard”中检查标签列表的首行、末行以及中间任意一行，确认标签均含 Route 和 Tracking Code。
2. 检查 Pivot Table 的行标签是 Carrier，并且其数值列是 Tracking Code 的计数。
3. 确认所有 Carrier 的计数相加为 30；这表示全部 30 条 Dispatch Log 记录均被纳入汇总。
4. 保存工作簿。

- 对应 skills：无；这是准备或检查步骤。
- 高效操作：最终同时检查明细标签和汇总表，可及时发现 Pivot Table 输出位置重叠、字段放错区域或填充范围不足的问题。
- 完成标志：Route Dashboard 同时显示完整的 30 条路线/追踪标签和按 Carrier 汇总的 Tracking Code 数量，且 Pivot Table 计数总和为 30。

#### 最终结果检查

- 工作簿中有且只有一个新增的工作表，标签名称为“Route Dashboard”。
- “Route Dashboard”中存在带有说明性标题的路线/追踪标签列表；从第 2 行到第 31 行均显示由 Dispatch Log 中对应行的 Route 与 Tracking Code 组成的文本。
- 标签公式引用 Dispatch Log 工作表，且向下填充后每一行引用对应的源数据行，例如第 31 行对应 Dispatch Log 的第 31 行。
- “Route Dashboard”中存在不与标签列表重叠的 Pivot Table，按 Carrier 分组，并显示每个 Carrier 的 Tracking Code 数量。
- 在 Pivot Table 中，各承运商旁显示数值计数列；30 条源记录应被这些承运商计数完整汇总。

## Source-task similarity review

| Measure | Maximum | Most similar source task |
| --- | ---: | --- |
| Lexical sequence similarity | 0.268041 | 8b1ce5f2-59d2-4dcc-b0b0-666a714b9a14 |
| Semantic cosine similarity | 0.329174 | 1954cced-e748-45c4-9c26-9855b97fbc5e |

Similarity scores are reviewer aids, not automatic acceptance thresholds. Inspect the contributing source tasks and their complete ordered actions below.

### Source task `035f41ba-6653-43ab-aa63-c86d449d62e5`

Original instruction:

> Help me fill in the Gross profit column by subtracting all the available expenses including discounts, allowances, material and labor charges, and overhead from the actual sale, i.e., the sales after deducting the returns. Then under column A named "Year_Profit" in a new sheet, display the Year Column in Sheet 1 as text appended by a "_" with the corresponding integer digits of Gross Profit value.

Required skills derived from this source task:

- **Insert a new worksheet from the sheet tab bar** — `035f41ba-6653-43ab-aa63-c86d449d62e5.skill-04`
- **Fill a formula down using the fill handle** — `035f41ba-6653-43ab-aa63-c86d449d62e5.skill-03`
- **Concatenate cross-sheet cell values in a formula** — `035f41ba-6653-43ab-aa63-c86d449d62e5.skill-05`

Complete ordered single-action sequence:

| Action | Related required skill | Original single action |
| ---: | --- | --- |
| 0 |  | <code>`CLICK` on cell J2</code> |
| 1 |  | <code>`TYPING` &#x27;=B2-C2-D2-SUM(F2:H2)&#x27;</code> |
| 2 |  | <code>`CLICK` format as currency icon</code> |
| 3 | <strong>★ Fill a formula down using the fill handle</strong><br><code>035f41ba-6653-43ab-aa63-c86d449d62e5.skill-03</code> | <strong><code>`MOVE_TO` bottom right corner of the cell J2`</code></strong> |
| 4 | <strong>★ Fill a formula down using the fill handle</strong><br><code>035f41ba-6653-43ab-aa63-c86d449d62e5.skill-03</code> | <strong><code>`DRAG_TO` bottom right corner of the cell J10</code></strong> |
| 5 | <strong>★ Insert a new worksheet from the sheet tab bar</strong><br><code>035f41ba-6653-43ab-aa63-c86d449d62e5.skill-04</code> | <strong><code>`CLICK` on + to left of sheet1</code></strong> |
| 6 |  | <code>`TYPING` &#x27;Year_Profit&#x27;</code> |
| 7 |  | <code>`PRESS` enter</code> |
| 8 | <strong>★ Concatenate cross-sheet cell values in a formula</strong><br><code>035f41ba-6653-43ab-aa63-c86d449d62e5.skill-05</code> | <strong><code>`TYPING` &#x27;=$Sheet1.A2&amp;&quot;_&quot;&amp;$Sheet1.J2&#x27;</code></strong> |
| 9 | <strong>★ Fill a formula down using the fill handle</strong><br><code>035f41ba-6653-43ab-aa63-c86d449d62e5.skill-03</code> | <strong><code>`MOVE_TO` bottom right corner of the cell A2`</code></strong> |
| 10 | <strong>★ Fill a formula down using the fill handle</strong><br><code>035f41ba-6653-43ab-aa63-c86d449d62e5.skill-03</code> | <strong><code>`DRAG_TO` bottom right corner of the cell A10</code></strong> |

### Source task `1954cced-e748-45c4-9c26-9855b97fbc5e`

Original instruction:

> Create a Pivot Table in a new sheet (Sheet2) to count how many times each "Invoice No." appears.

Required skills derived from this source task:

- **Rename a worksheet tab** — `1954cced-e748-45c4-9c26-9855b97fbc5e.skill-05`
- **Add a field as a Pivot Table value** — `1954cced-e748-45c4-9c26-9855b97fbc5e.skill-03`

Complete ordered single-action sequence:

| Action | Related required skill | Original single action |
| ---: | --- | --- |
| 0 |  | <code>`CLICK` on grey cell box A for selecting entire column</code> |
| 1 |  | <code>`CLICK` on pivot table icon</code> |
| 2 |  | <code>`PRESS` enter</code> |
| 3 |  | <code>`MOVE_TO` invoice no. in available fields box</code> |
| 4 |  | <code>`DRAG_TO` row fields box</code> |
| 5 | <strong>★ Add a field as a Pivot Table value</strong><br><code>1954cced-e748-45c4-9c26-9855b97fbc5e.skill-03</code> | <strong><code>`MOVE_TO` invoice no. in available fields box</code></strong> |
| 6 | <strong>★ Add a field as a Pivot Table value</strong><br><code>1954cced-e748-45c4-9c26-9855b97fbc5e.skill-03</code> | <strong><code>`DRAG_TO` data fields box</code></strong> |
| 7 |  | <code>`DOUBLE_CLICK on invoice no. box in data fields</code> |
| 8 |  | <code>`CLICK` Count</code> |
| 9 |  | <code>`PRESS` enter</code> |
| 10 |  | <code>`CLICK` ok</code> |
| 11 | <strong>★ Rename a worksheet tab</strong><br><code>1954cced-e748-45c4-9c26-9855b97fbc5e.skill-05</code> | <strong><code>`DOUBLE_CLICK` Pivot Table Sheet1_1</code></strong> |
| 12 | <strong>★ Rename a worksheet tab</strong><br><code>1954cced-e748-45c4-9c26-9855b97fbc5e.skill-05</code> | <strong><code>`TYPING` Sheet2</code></strong> |
| 13 | <strong>★ Rename a worksheet tab</strong><br><code>1954cced-e748-45c4-9c26-9855b97fbc5e.skill-05</code> | <strong><code>`PRESS` enter</code></strong> |

## Review this package

Before choosing a decision, complete all three checks:

- [ ] **Task naturalness and skill necessity:** Is the reference task a natural Calc task, and is every listed required skill genuinely necessary and observable when solving it?
- [ ] **Initial artifact correctness:** Launch the environment and confirm that the workbook opens correctly, contains the data needed by the instruction, and has not already completed the requested results.
- [ ] **Source-task similarity:** Compare the reference task with the source instructions and complete single-action sequences above. Confirm that it is not merely an entity, field, or value substitution and does not reproduce a source task's complete ordered solution.

Use `approved` when all checks pass. Use `revision_requested` when the package is fixable and provide concrete revision instructions. Use `rejected` when the combination is fundamentally unnatural, infeasible, or too similar to a source task.

Fill [review.json](review.json), then collect completed forms from the repository root:

```bash
python scripts/python/manage_reference_review_packets.py collect
```

Detailed field guidance is in [`reviewer.md`](../../../reviewer.md).
