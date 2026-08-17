# Workshop Service Billing

- Reference task: `reference-task-r01-004`
- Application: `libreoffice_calc`
- Review decision: `pending`

## Task instruction

Complete the billed-charge calculation for every workshop service record and present those results as currency. Then create a new Pivot Table summary that lists each coordinator and their total billed charge.

## Required skills

### 1. Apply currency formatting with the toolbar

Skill ID: `035f41ba-6653-43ab-aa63-c86d449d62e5.skill-02`

Procedure:

1. Keep the cell or range containing monetary results selected.
2. Click the toolbar's Format as Currency button to apply the currency number format.
3. For example, after calculating a value in J2, select J2 and use the currency icon so the numeric result displays as an amount.

Efficiency tip: Format the first result cell before filling the formula down so copied results retain the same number format.

Source task: `035f41ba-6653-43ab-aa63-c86d449d62e5`

Source instruction: Help me fill in the Gross profit column by subtracting all the available expenses including discounts, allowances, material and labor charges, and overhead from the actual sale, i.e., the sales after deducting the returns. Then under column A named "Year_Profit" in a new sheet, display the Year Column in Sheet 1 as text appended by a "_" with the corresponding integer digits of Gross Profit value.

Directly referenced source actions:

- Action 2: <code>`CLICK` format as currency icon</code>

### 2. Place a field in Pivot Table row labels

Skill ID: `1954cced-e748-45c4-9c26-9855b97fbc5e.skill-02`

Procedure:

1. In the Pivot Table layout dialog, locate the desired field in the Available Fields list.
2. Drag the field into the Row Fields area. For example, drag an identifier field there to produce one row label per distinct identifier.

Efficiency tip: Drag a field directly from Available Fields to Row Fields rather than adding it elsewhere first and repositioning it afterward.

Source task: `1954cced-e748-45c4-9c26-9855b97fbc5e`

Source instruction: Create a Pivot Table in a new sheet (Sheet2) to count how many times each "Invoice No." appears.

Directly referenced source actions:

- Action 3: <code>`MOVE_TO` invoice no. in available fields box</code>
- Action 4: <code>`DRAG_TO` row fields box</code>

## Initial state preview

### Service Log

![Service_Log.png](artifact/previews/Service_Log.png)

## Operator guide

### Existing operation-intent guide

#### Demonstration 1

- Skill: `035f41ba-6653-43ab-aa63-c86d449d62e5.skill-02`
- Intent: Present every calculated Billed Charge value in the Service Log as a currency amount using Calc's currency toolbar control.
- Efficiency: Format the first calculated result cell with the toolbar before filling the formula down when that workflow preserves the number format; otherwise select the completed result range once and format it together.
- Visible success: The Billed Charge column shows currency symbols and two-decimal monetary displays rather than unformatted numeric products.

#### Demonstration 2

- Skill: `1954cced-e748-45c4-9c26-9855b97fbc5e.skill-02`
- Intent: In the new Pivot Table layout, place Coordinator in the row-label area for a coordinator-level billed-charge summary.
- Efficiency: Move Coordinator directly from the available Pivot Table fields into the Row Fields area, then ensure the billed amount is summarized as a sum.
- Visible success: The resulting Pivot Table displays one row label for each coordinator, with a corresponding total Billed Charge value.

Recording start: The workbook contains only the populated Service Log source sheet; Billed Charge is blank and unformatted, and no Pivot Table exists.

Recording end: Service Log has calculated, currency-formatted Billed Charge values for all 24 records, and a newly created Pivot Table sheet summarizes summed billed charge by Coordinator in row labels.

Allowed variation: The expert may calculate and format the source results before creating the Pivot Table, or use any equivalent Calc workflow that produces the requested source calculations and a new-sheet pivot summary. The destination sheet name and the order of distinct coordinator labels may vary.

### 中文详细参考方案

> 以下是一个可以参考的操作 guide。标注者可以根据实际 LibreOffice 界面采用等价操作。

本指南将在“Service Log”工作表中计算 24 条社区工作坊服务记录的 Billed Charge（Units × Hourly Rate），将结果显示为货币金额，然后在新工作表创建按 Coordinator 汇总 Billed Charge 总额的数据透视表。

#### 启动后的初始状态检查

- 确认工作簿已打开且当前可见“Service Log”工作表。
- 确认第 1 行是标题行，A1:F1 依次包含 Work Order、Coordinator、Service Tier、Units、Hourly Rate、Billed Charge；数据应延续至第 25 行。
- 确认 Billed Charge 列 F2:F25 仍为空白，且当前没有数据透视表汇总工作表。
- 确认 Units 位于 D 列、Hourly Rate 位于 E 列、Billed Charge 位于 F 列，以便使用正确的乘法公式。

#### 第 1 步：计算第一条服务记录的 Billed Charge

1. 在“Service Log”中单击单元格 F2，即第一条服务记录的 Billed Charge 单元格。
2. 输入公式 `=D2*E2`，然后按 Enter。该公式会用本行 Units 乘以本行 Hourly Rate。
3. 确认 F2 显示一个非零数值；选中 F2 时，公式输入栏应显示 `=D2*E2`。

- 对应 skills：无；这是准备或检查步骤。
- 高效操作：先只在第一个结果单元格中建立正确公式，确认无误后再填充，可避免对每一行重复输入公式。
- 完成标志：F2 不再为空白，而是显示 Units 与 Hourly Rate 相乘得到的数值。

#### 第 2 步：将首个计算结果设置为货币格式

1. 保持 F2 处于选中状态。
2. 在 Calc 工具栏上单击“格式化为货币”按钮（货币图标）。
3. 查看 F2 的显示方式：它应改为带货币符号且保留两位小数的金额。

- 对应 skills：`035f41ba-6653-43ab-aa63-c86d449d62e5.skill-02`
- 高效操作：在填充公式前先给 F2 设置货币格式；向下填充时，Calc 通常会同时保留该格式。
- 完成标志：F2 以货币金额显示，而不是普通的小数或常规数字。

#### 第 3 步：向下填充全部 24 条 Billed Charge 公式

1. 再次选中 F2，然后将选区扩展为 F2:F25。可在名称框中输入 `F2:F25` 并按 Enter，或先选中 F2 后按住 Shift 单击 F25。
2. 选择“工作表”菜单中的“填充单元格”→“向下填充”，使 F2 的公式复制到 F3:F25。
3. 检查 F3 和 F25：每行公式应随行号调整，例如 F3 对应 `=D3*E3`，F25 对应 `=D25*E25`。
4. 如果填充后某些单元格未显示货币格式，选中整个 F2:F25，并再次单击工具栏的“格式化为货币”按钮。

- 对应 skills：无；这是准备或检查步骤。
- 高效操作：使用填充柄或“向下填充”可一次把公式和货币格式复制到剩余 23 行，比逐行输入更快。
- 完成标志：F2:F25 全部包含非零计算结果，并以带货币符号和两位小数的格式显示。

#### 第 4 步：以完整服务日志作为数据透视表源

1. 在“Service Log”中选中完整源数据范围 A1:F25，包括标题行和全部 24 条记录。可单击 A1 后按住 Shift 单击 F25。
2. 打开“数据”菜单，选择“数据透视表”中的“插入或编辑”（不同版本可能显示为“插入或创建”），启动数据透视表创建流程。
3. 在数据源确认对话框中，确认使用当前选定区域作为数据源，然后继续进入数据透视表布局对话框。

- 对应 skills：无；这是准备或检查步骤。
- 高效操作：选中包含标题的完整连续数据区域，可让 Calc 自动把第一行识别为数据透视表字段名。
- 完成标志：屏幕显示数据透视表布局界面，并在“可用字段”列表中可看到 Coordinator 和 Billed Charge 等字段。

#### 第 5 步：将 Coordinator 放入数据透视表的行字段

1. 在数据透视表布局对话框的“可用字段”列表中找到 `Coordinator`。
2. 将 `Coordinator` 直接拖入“行字段”区域。
3. 确认 `Coordinator` 已显示在“行字段”区域中，而不是“列字段”或“数据字段”区域。

- 对应 skills：`1954cced-e748-45c4-9c26-9855b97fbc5e.skill-02`
- 高效操作：将字段从“可用字段”直接拖到目标区域，避免先放错位置后再调整。
- 完成标志：布局中的“行字段”区域包含 Coordinator，预示结果会按每位协调员分行显示。

#### 第 6 步：将 Billed Charge 配置为求和数据字段

1. 从“可用字段”列表将 `Billed Charge` 拖入“数据字段”区域。
2. 检查该数据字段的汇总方式是否为“求和”或显示类似“Sum - Billed Charge”。如果显示“计数”，双击或打开该数据字段的选项，将汇总函数改为“求和”。
3. 确认布局只需 Coordinator 作为行字段，Billed Charge 作为数据字段；不需要将其他字段加入列字段。

- 对应 skills：无；这是准备或检查步骤。
- 高效操作：数值金额字段放入“数据字段”后应使用“求和”；若 Calc 自动选择了计数，应在创建前改正。
- 完成标志：“数据字段”区域显示 Billed Charge 的求和汇总，而“行字段”区域仍显示 Coordinator。

#### 第 7 步：在新工作表生成协调员收费汇总

1. 在布局对话框中确认字段设置后，点击“确定”或继续到输出位置设置。
2. 选择将数据透视表输出到“新工作表”，然后确认创建。
3. 切换到新建的数据透视表工作表，必要时可将工作表重命名为易辨识的名称，例如“Coordinator Summary”。

- 对应 skills：无；这是准备或检查步骤。
- 高效操作：选择在新工作表输出可避免覆盖原始服务日志，也便于单独查看汇总结果。
- 完成标志：出现一个新的工作表，其中数据透视表按 Coordinator 显示行标签，并在相邻列显示 Billed Charge 的汇总金额和总计。

#### 最终结果检查

- 回到“Service Log”，确认 F2:F25 的 24 个 Billed Charge 单元格都含有计算结果，且显示为带货币符号和两位小数的金额。
- 确认“Service Log”中的 Billed Charge 结果与同一行的 Units × Hourly Rate 相符；例如可选中任意一行检查公式栏是否为相应的乘法公式。
- 确认工作簿中新建了一个包含数据透视表的工作表；表中应有 Avery Cole、Imani Park、Jules Rowan、Morgan Lee 和 Tessa Vale 等协调员行标签，并且每人旁边有 Billed Charge 的汇总金额。
- 确认数据透视表的金额字段是求和结果，而不是计数；表中通常会有总计行，且总计应对应所有 24 条服务记录的 Billed Charge 总和。

## Source-task similarity review

| Measure | Maximum | Most similar source task |
| --- | ---: | --- |
| Lexical sequence similarity | 0.296053 | 1954cced-e748-45c4-9c26-9855b97fbc5e |
| Semantic cosine similarity | 0.449874 | 1954cced-e748-45c4-9c26-9855b97fbc5e |

Similarity scores are reviewer aids, not automatic acceptance thresholds. Inspect the contributing source tasks and their complete ordered actions below.

### Source task `035f41ba-6653-43ab-aa63-c86d449d62e5`

Original instruction:

> Help me fill in the Gross profit column by subtracting all the available expenses including discounts, allowances, material and labor charges, and overhead from the actual sale, i.e., the sales after deducting the returns. Then under column A named "Year_Profit" in a new sheet, display the Year Column in Sheet 1 as text appended by a "_" with the corresponding integer digits of Gross Profit value.

Required skills derived from this source task:

- **Apply currency formatting with the toolbar** — `035f41ba-6653-43ab-aa63-c86d449d62e5.skill-02`

Complete ordered single-action sequence:

| Action | Related required skill | Original single action |
| ---: | --- | --- |
| 0 |  | <code>`CLICK` on cell J2</code> |
| 1 |  | <code>`TYPING` &#x27;=B2-C2-D2-SUM(F2:H2)&#x27;</code> |
| 2 | <strong>★ Apply currency formatting with the toolbar</strong><br><code>035f41ba-6653-43ab-aa63-c86d449d62e5.skill-02</code> | <strong><code>`CLICK` format as currency icon</code></strong> |
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

- **Place a field in Pivot Table row labels** — `1954cced-e748-45c4-9c26-9855b97fbc5e.skill-02`

Complete ordered single-action sequence:

| Action | Related required skill | Original single action |
| ---: | --- | --- |
| 0 |  | <code>`CLICK` on grey cell box A for selecting entire column</code> |
| 1 |  | <code>`CLICK` on pivot table icon</code> |
| 2 |  | <code>`PRESS` enter</code> |
| 3 | <strong>★ Place a field in Pivot Table row labels</strong><br><code>1954cced-e748-45c4-9c26-9855b97fbc5e.skill-02</code> | <strong><code>`MOVE_TO` invoice no. in available fields box</code></strong> |
| 4 | <strong>★ Place a field in Pivot Table row labels</strong><br><code>1954cced-e748-45c4-9c26-9855b97fbc5e.skill-02</code> | <strong><code>`DRAG_TO` row fields box</code></strong> |
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
