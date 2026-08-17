# Workshop Grant Reconciliation

- Reference task: `reference-task-r01-002`
- Application: `libreoffice_calc`
- Review decision: `pending`

## Task instruction

Reconcile the workshop grants by calculating each workshop's Net Allocation after reversals, recoveries, and all listed delivery costs, then create a new-sheet Pivot Table that shows the total Net Allocation for each Service Area.

## Required skills

### 1. Build a row formula that subtracts a range total

Skill ID: `035f41ba-6653-43ab-aa63-c86d449d62e5.skill-01`

Procedure:

1. Select the output cell in the row to calculate.
2. Enter and commit a formula that subtracts individual values and a contiguous range total from a starting value. For example, use `=B2-C2-D2-SUM(F2:H2)`.
3. When reused on another table, replace the cell references with the relevant sale, return, adjustment, and expense columns.

Efficiency tip: Use a single SUM range for adjacent expense columns instead of subtracting each expense cell separately.

Source task: `035f41ba-6653-43ab-aa63-c86d449d62e5`

Source instruction: Help me fill in the Gross profit column by subtracting all the available expenses including discounts, allowances, material and labor charges, and overhead from the actual sale, i.e., the sales after deducting the returns. Then under column A named "Year_Profit" in a new sheet, display the Year Column in Sheet 1 as text appended by a "_" with the corresponding integer digits of Gross Profit value.

Directly referenced source actions:

- Action 0: <code>`CLICK` on cell J2</code>
- Action 1: <code>`TYPING` &#x27;=B2-C2-D2-SUM(F2:H2)&#x27;</code>

### 2. Create a Pivot Table from selected worksheet data

Skill ID: `1954cced-e748-45c4-9c26-9855b97fbc5e.skill-01`

Procedure:

1. Select the data to summarize. For example, click a column header to use that entire column as the source when the column contains the needed records.
2. Click the Pivot Table toolbar icon to open the Pivot Table creation workflow.
3. Confirm the detected source selection, for example by pressing Enter when the proposed range is correct.

Efficiency tip: Select the complete contiguous source range before launching the command when possible; this avoids correcting an automatically detected range in the Pivot Table source dialog.

Source task: `1954cced-e748-45c4-9c26-9855b97fbc5e`

Source instruction: Create a Pivot Table in a new sheet (Sheet2) to count how many times each "Invoice No." appears.

Directly referenced source actions:

- Action 0: <code>`CLICK` on grey cell box A for selecting entire column</code>
- Action 1: <code>`CLICK` on pivot table icon</code>
- Action 2: <code>`PRESS` enter</code>

## Initial state preview

### Funding Log

![Funding_Log.png](artifact/previews/Funding_Log.png)

## Operator guide

### Existing operation-intent guide

#### Demonstration 1

- Skill: `035f41ba-6653-43ab-aa63-c86d449d62e5.skill-01`
- Intent: Calculate Net Allocation as the award less the credit reversal, asset recovery, and combined venue-to-facilitator costs for each workshop record.
- Efficiency: Enter the expression once in the first data row using one SUM range for the three adjacent cost columns, then fill it down the populated table.
- Visible success: I2 contains a row-relative formula equivalent to =B2-C2-D2-SUM(F2:H2), and I2:I17 display currency results with references adjusted by row.

#### Demonstration 2

- Skill: `1954cced-e748-45c4-9c26-9855b97fbc5e.skill-01`
- Intent: Create a native Pivot Table on a new worksheet that summarizes the sum of Net Allocation for each Service Area.
- Efficiency: Start from the full contiguous table so the detected Pivot Table source already contains the headers, all records, and the calculated measure.
- Visible success: A separate pivot output sheet visibly lists Northside, Harbor, and Meadow with a summed Net Allocation value for each.

Recording start: The workbook opens to the single Funding Log sheet with the populated source table and a blank Net Allocation column.

Recording end: Funding Log retains all 16 records with completed Net Allocation formulas, and a new worksheet contains a native Pivot Table showing total Net Allocation grouped by Service Area.

Allowed variation: The expert may use formula fill, copy/paste, or another efficient equivalent to populate the calculated column, and may use any suitable native LibreOffice Calc Pivot Table workflow and layout so long as the completed workbook visibly provides the requested summed service-area summary.

### 中文详细参考方案

> 以下是一个可以参考的操作 guide。标注者可以根据实际 LibreOffice 界面采用等价操作。

本任务先在“Funding Log”中计算每个 workshop 的 Net Allocation：从 Award Received 扣除 Credit Reversal、Asset Recovery 以及 Venue Cost 到 Facilitator Cost 的三项连续成本。随后以完整数据表建立原生数据透视表，在新工作表中按 Service Area 汇总 Net Allocation 的总和。

#### 启动后的初始状态检查

- 确认工作簿标题为“Workshop Grant Reconciliation”。
- 确认开始时只有“Funding Log”工作表。
- 确认 Funding Log 中的数据区域为 A1:I17：第 1 行是标题，数据在第 2 至第 17 行，I 列标题为“Net Allocation”，且 I2:I17 为空。
- 确认 A 至 H 列包含 Workshop ID、Award Received、Credit Reversal、Asset Recovery、Service Area、Venue Cost、Materials Cost 和 Facilitator Cost，避免在错误列中输入公式。

#### 第 1 步：在首条记录计算 Net Allocation

1. 打开“Funding Log”工作表，单击输出列的第一个数据单元格 I2。
2. 输入公式 `=B2-C2-D2-SUM(F2:H2)`，然后按 Enter 确认。该公式以 Award Received 为起点，依次扣除 Credit Reversal、Asset Recovery，以及 F 至 H 列的三项成本总额。
3. 检查 I2 显示一个货币结果；再次选中 I2 时，可在输入行看到刚输入的公式。

- 对应 skills：`035f41ba-6653-43ab-aa63-c86d449d62e5.skill-01`
- 高效操作：先只在第一条记录建立公式；将 F2:H2 作为连续区域交给 SUM 一次计算，比逐个减去三项成本更简洁，也更不容易漏列。
- 完成标志：I2 显示货币金额，且其公式为 `=B2-C2-D2-SUM(F2:H2)` 或含义相同的行内公式。

#### 第 2 步：将公式填充到全部 workshop 记录

1. 选中 I2。
2. 将 I2 的公式向下填充到 I17。可拖动选中单元格右下角的填充柄至 I17；也可复制 I2，选中 I3:I17 后粘贴。
3. 选中例如 I3、I10 或 I17 进行抽查，确认公式中的行号已变为对应行号，例如 I3 使用第 3 行引用。

- 对应 skills：无；这是准备或检查步骤。
- 高效操作：使用填充柄或复制到连续目标区域，可以让 Calc 自动调整行号，无需为 16 条记录逐条重输公式。
- 完成标志：I2:I17 全部显示货币结果，没有空白输出；各行公式的引用随行号自动调整。

#### 第 3 步：以完整资金记录作为数据透视表来源

1. 在“Funding Log”中选择完整源数据区域 A1:I17，务必包含标题行、Service Area 列和已完成的 Net Allocation 列。
2. 选择菜单“数据”>“数据透视表”>“插入或编辑…”。在数据源选择界面确认当前选区为 A1:I17，然后继续进入数据透视表布局设置。

- 对应 skills：`1954cced-e748-45c4-9c26-9855b97fbc5e.skill-01`
- 高效操作：从包含标题和计算结果的完整连续区域启动数据透视表，Calc 更容易正确识别字段及全部 16 条记录。
- 完成标志：数据透视表布局窗口显示可用字段，其中包括“Service Area”和“Net Allocation”，并且来源是 Funding Log 的完整表格。

#### 第 4 步：按 Service Area 配置 Net Allocation 求和汇总

1. 在布局设置中，将“Service Area”放入“行字段”区域。
2. 将“Net Allocation”放入“数据字段”区域。若该字段的汇总方式不是求和，双击或打开该数据字段的选项，将函数设为“求和”。
3. 继续到输出位置设置，选择在新工作表中创建数据透视表，然后确认完成。

- 对应 skills：无；这是准备或检查步骤。
- 高效操作：只放置一个行字段和一个数据字段，能得到清晰、便于核对的按区域汇总表。
- 完成标志：Calc 创建一个新的工作表，其中的数据透视表以 Service Area 为行标签，并显示 Net Allocation 的总和列。

#### 第 5 步：核对数据透视表结果和工作簿结构

1. 查看新工作表中的数据透视表，确认行标签包含 Northside、Harbor 和 Meadow。
2. 确认每个 Service Area 对应的是 Net Allocation 的汇总金额，而不是记录计数；如标题显示计数或结果明显为小整数，应返回布局将 Net Allocation 的汇总函数改为“求和”。
3. 保留 Funding Log 源表及新建的数据透视表工作表，不要用手工汇总值替换数据透视表结果。

- 对应 skills：无；这是准备或检查步骤。
- 高效操作：完成后先用三项区域名称和一列总计快速核对结构；这样可立即发现字段放错区域或被计数而非求和的问题。
- 完成标志：新工作表可见 Northside、Harbor、Meadow 三个区域及各自的 Net Allocation 求和金额，同时 Funding Log 的 16 条原始记录和计算列仍完整存在。

#### 最终结果检查

- 返回“Funding Log”工作表，确认 I2:I17 均不再为空，且这些单元格显示为货币金额；单击其中若干单元格时，编辑栏中的公式引用应随所在行变化。
- 确认源数据仍保留在 Funding Log 的 A1:I17，标题行和 16 条记录没有被删除或覆盖。
- 确认存在一个单独的新工作表，其中的原生数据透视表按 Service Area 列出 Northside、Harbor、Meadow，并为每个区域显示 Net Allocation 的求和结果。

## Source-task similarity review

| Measure | Maximum | Most similar source task |
| --- | ---: | --- |
| Lexical sequence similarity | 0.319018 | 1954cced-e748-45c4-9c26-9855b97fbc5e |
| Semantic cosine similarity | 0.437947 | 035f41ba-6653-43ab-aa63-c86d449d62e5 |

Similarity scores are reviewer aids, not automatic acceptance thresholds. Inspect the contributing source tasks and their complete ordered actions below.

### Source task `035f41ba-6653-43ab-aa63-c86d449d62e5`

Original instruction:

> Help me fill in the Gross profit column by subtracting all the available expenses including discounts, allowances, material and labor charges, and overhead from the actual sale, i.e., the sales after deducting the returns. Then under column A named "Year_Profit" in a new sheet, display the Year Column in Sheet 1 as text appended by a "_" with the corresponding integer digits of Gross Profit value.

Required skills derived from this source task:

- **Build a row formula that subtracts a range total** — `035f41ba-6653-43ab-aa63-c86d449d62e5.skill-01`

Complete ordered single-action sequence:

| Action | Related required skill | Original single action |
| ---: | --- | --- |
| 0 | <strong>★ Build a row formula that subtracts a range total</strong><br><code>035f41ba-6653-43ab-aa63-c86d449d62e5.skill-01</code> | <strong><code>`CLICK` on cell J2</code></strong> |
| 1 | <strong>★ Build a row formula that subtracts a range total</strong><br><code>035f41ba-6653-43ab-aa63-c86d449d62e5.skill-01</code> | <strong><code>`TYPING` &#x27;=B2-C2-D2-SUM(F2:H2)&#x27;</code></strong> |
| 2 |  | <code>`CLICK` format as currency icon</code> |
| 3 |  | <code>`MOVE_TO` bottom right corner of the cell J2`</code> |
| 4 |  | <code>`DRAG_TO` bottom right corner of the cell J10</code> |
| 5 |  | <code>`CLICK` on + to left of sheet1</code> |
| 6 |  | <code>`TYPING` &#x27;Year_Profit&#x27;</code> |
| 7 |  | <code>`PRESS` enter</code> |
| 8 |  | <code>`TYPING` &#x27;=$Sheet1.A2&amp;&quot;_&quot;&amp;$Sheet1.J2&#x27;</code> |
| 9 |  | <code>`MOVE_TO` bottom right corner of the cell A2`</code> |
| 10 |  | <code>`DRAG_TO` bottom right corner of the cell A10</code> |

### Source task `1954cced-e748-45c4-9c26-9855b97fbc5e`

Original instruction:

> Create a Pivot Table in a new sheet (Sheet2) to count how many times each "Invoice No." appears.

Required skills derived from this source task:

- **Create a Pivot Table from selected worksheet data** — `1954cced-e748-45c4-9c26-9855b97fbc5e.skill-01`

Complete ordered single-action sequence:

| Action | Related required skill | Original single action |
| ---: | --- | --- |
| 0 | <strong>★ Create a Pivot Table from selected worksheet data</strong><br><code>1954cced-e748-45c4-9c26-9855b97fbc5e.skill-01</code> | <strong><code>`CLICK` on grey cell box A for selecting entire column</code></strong> |
| 1 | <strong>★ Create a Pivot Table from selected worksheet data</strong><br><code>1954cced-e748-45c4-9c26-9855b97fbc5e.skill-01</code> | <strong><code>`CLICK` on pivot table icon</code></strong> |
| 2 | <strong>★ Create a Pivot Table from selected worksheet data</strong><br><code>1954cced-e748-45c4-9c26-9855b97fbc5e.skill-01</code> | <strong><code>`PRESS` enter</code></strong> |
| 3 |  | <code>`MOVE_TO` invoice no. in available fields box</code> |
| 4 |  | <code>`DRAG_TO` row fields box</code> |
| 5 |  | <code>`MOVE_TO` invoice no. in available fields box</code> |
| 6 |  | <code>`DRAG_TO` data fields box</code> |
| 7 |  | <code>`DOUBLE_CLICK on invoice no. box in data fields</code> |
| 8 |  | <code>`CLICK` Count</code> |
| 9 |  | <code>`PRESS` enter</code> |
| 10 |  | <code>`CLICK` ok</code> |
| 11 |  | <code>`DOUBLE_CLICK` Pivot Table Sheet1_1</code> |
| 12 |  | <code>`TYPING` Sheet2</code> |
| 13 |  | <code>`PRESS` enter</code> |

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
