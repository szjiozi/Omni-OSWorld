# Garden Supply Delivery Register

- Reference task: `reference-task-calc-full-r01-008`
- Application: `libreoffice_calc`
- Review decision: `pending`

## Task instruction

Complete the Line Total calculation for every delivery in the Garden Supply Delivery Register, then add a default-named worksheet and use it to show a Pivot Table summary of total delivery spending for each Garden Zone.

## Required skills

### 1. Create a Pivot Table with a row field and summed data field

Skill ID: `535364ea-05bd-46ea-9937-9f55c68507e8.skill-01`

Procedure:

1. Select the source data range, for example with Ctrl+A when the active sheet contains only the dataset.
2. Click the Pivot Table command and accept the detected source range in the initial dialog.
3. In the Pivot Table Layout dialog, drag the category field from Available Fields to Row Fields. For example, drag a field such as Product or Sales Channel to Row Fields.
4. Drag the numeric measure from Available Fields to Data Fields. For example, drag Revenue to Data Fields; Calc creates an aggregate, normally Sum, for that numeric field.
5. Confirm the layout with OK to generate the Pivot Table. Repeat the same layout pattern with different row fields as needed.

Efficiency tip: Select the entire source range before invoking the Pivot Table command so Calc can detect the source automatically, then drag fields directly into the layout areas rather than opening separate field-setting dialogs.

Source task: `535364ea-05bd-46ea-9937-9f55c68507e8`

Source instruction: Create two pivot tables in a new sheet showing the total revenue for each product and sales channel.

Directly referenced source actions:

- Action 0: <code>`HOTKEY` ctrl-a</code>
- Action 1: <code>`CLICK` pivot table icon</code>
- Action 2: <code>`PRESS` enter</code>
- Action 3: <code>`MOVE_TO` product in available fields box</code>
- Action 4: <code>`DRAG_TO` row fields box</code>
- Action 5: <code>`MOVE_TO` revenue in available fields box</code>
- Action 6: <code>`DRAG_TO` data fields box</code>
- Action 7: <code>`CLICK` ok</code>
- Action 12: <code>`HOTKEY` ctrl-a</code>
- Action 13: <code>`CLICK` pivot table icon</code>
- Action 14: <code>`PRESS` enter</code>
- Action 15: <code>`MOVE_TO` sales channel in available fields box</code>
- Action 16: <code>`DRAG_TO` row fields box</code>
- Action 17: <code>`MOVE_TO` revenue in available fields box</code>
- Action 18: <code>`DRAG_TO` data fields box</code>

### 2. AutoFill a formula down a contiguous data range using the fill handle

Skill ID: `0bf05a7d-b28b-44d2-955a-50b41e24012a.skill-02`

Procedure:

1. Select the cell that contains the formula to propagate.
2. Double-click the small fill handle at the cell’s bottom-right corner.
3. Calc fills the formula down alongside the neighboring contiguous data range, adjusting relative references for each row. For example, `=TEXT(C2,"0000000")` in D2 becomes `=TEXT(C3,"0000000")` in D3.

Efficiency tip: Double-click the fill handle when the adjacent source-data column is contiguous; this is faster and less error-prone than dragging through a long range.

Source task: `0bf05a7d-b28b-44d2-955a-50b41e24012a`

Source instruction: I would like to copy all the numbers in the 'Old ID' column to the 'New 7 Digit Id' column, and pad them with zeros in front, to fill them up to seven digits.

Directly referenced source actions:

- Action 2: <code>`CLICK` cell D2</code>
- Action 3: <code>`DOUBLE_CLICK` the bottom right corner of cell D2</code>

### 3. Insert a new worksheet with the default name

Skill ID: `30e3e107-1cfb-46ee-a755-2cd080d7ba6a.skill-01`

Procedure:

1. Click the plus button beside the worksheet tabs to add a new worksheet.
2. Calc creates the sheet with its next default name, for example, Sheet2; no sheet-tab rename action is needed when that default is desired.

Efficiency tip: Use the plus button when the default generated sheet name is acceptable; this avoids opening a rename workflow.

Source task: `30e3e107-1cfb-46ee-a755-2cd080d7ba6a`

Source instruction: Please create a new sheet. Keep its sheet name as "Sheet2". Merge cells A1:C1 in the new sheet and write "Demographic Profile" with blue (#0000ff) fill and bold white text. Then I want to create three pivot tables to show the percentage of Sex, Civil Status, and Highest Educational Attainment. They should be stacked one by one in Sheet2, each separated with a blank line.

Directly referenced source actions:

- Action 0: <code>`CLICK` on + to left of sheet1</code>

### 4. Create a Pivot Table from the current sheet selection

Skill ID: `1de60575-bb6e-4c3d-9e6a-2fa699f9f197.skill-01`

Procedure:

1. Click inside the source table and press Ctrl+A to select its current data range.
2. Click the toolbar command represented by the Pivot Table insert/edit icon.
3. In the initial Pivot Table dialog, verify that the selected range is the intended source and confirm it. For example, selecting a five-column table with Ctrl+A makes that table the Pivot Table source.

Efficiency tip: Use Ctrl+A when the active sheet contains one contiguous table; it quickly selects the complete source range before opening the Pivot Table command.

Source task: `1de60575-bb6e-4c3d-9e6a-2fa699f9f197`

Source instruction: Summarize the total revenue for each promotion type in a new sheet (Sheet2) with the promotion names as the column headers using the Pivot Table feature.

Directly referenced source actions:

- Action 0: <code>`HOTEKY` &#x27;ctrl-a&#x27;</code>
- Action 1: <code>`CLICK` curved arrow icon in the top bar representing insert or edit pivot table</code>
- Action 2: <code>`CLICK` ok</code>

## Initial state preview

### Delivery Log

![Delivery_Log.png](artifact/previews/Delivery_Log.png)

## Operator guide

### Existing operation-intent guide

#### Demonstration 1

- Skill: `0bf05a7d-b28b-44d2-955a-50b41e24012a.skill-02`
- Intent: Propagate the seeded Line Total calculation from the first delivery row through the remaining contiguous delivery rows.
- Efficiency: Keep the seeded formula cell adjacent to the contiguous Quantity data and double-click its fill handle to extend it through all delivery records efficiently.
- Visible success: Every Line Total cell from E2 through E25 displays a calculated currency amount, with relative row references reflected in the formulas.

#### Demonstration 2

- Skill: `30e3e107-1cfb-46ee-a755-2cd080d7ba6a.skill-01`
- Intent: Insert one blank worksheet and retain its automatically assigned default name.
- Efficiency: Use the sheet-tab plus control rather than a rename workflow, because the required default worksheet name is Sheet2.
- Visible success: A new worksheet tab named Sheet2 is visible alongside Delivery Log.

#### Demonstration 3

- Skill: `1de60575-bb6e-4c3d-9e6a-2fa699f9f197.skill-01`
- Intent: Start Pivot Table creation using the current full delivery-table selection as the source.
- Efficiency: Activate Delivery Log and select its one contiguous table in a single action so Calc detects the entire source range without manual range editing.
- Visible success: The Pivot Table setup flow opens with the Delivery Log table range recognized as the data source.

#### Demonstration 4

- Skill: `535364ea-05bd-46ea-9937-9f55c68507e8.skill-01`
- Intent: Configure and generate a pivot summary on Sheet2 that groups delivery spending by Garden Zone and totals Line Total.
- Efficiency: In the layout dialog, drag Garden Zone directly to Row Fields and Line Total directly to Data Fields; the numeric amount should default to a Sum aggregation.
- Visible success: Sheet2 visibly contains a pivot table with one row per Garden Zone and a summed Line Total amount for each zone, plus the pivot grand total.

Recording start: Delivery Log is the only sheet; its 24-row delivery table has only E2 seeded with the Line Total formula, and no pivot table exists.

Recording end: Delivery Log contains calculated Line Total values for all 24 records, and Sheet2 contains the completed Garden Zone by summed Line Total pivot table.

Allowed variation: The expert may insert Sheet2 before or after filling the line totals, may use menu or toolbar access to Pivot Table, and may choose any clear non-overlapping placement on Sheet2. Equivalent use of keyboard shortcuts is acceptable.

### 中文详细参考方案

> 以下是一个可以参考的操作 guide。标注者可以根据实际 LibreOffice 界面采用等价操作。

完成 Garden Supply Delivery Register：先将 `Line Total` 的种子公式从 `E2` 快速填充到全部 24 条送货记录，再新建默认名称为 `Sheet2` 的工作表，并在其中建立按 `Garden Zone` 汇总 `Line Total` 总支出的 Pivot Table。

#### 启动后的初始状态检查

- 确认当前工作簿只有一个工作表标签 `Delivery Log`；尚未出现 `Sheet2` 或任何 Pivot Table。
- 打开 `Delivery Log`，确认连续数据表位于 `A1:E25`，第 1 行包含标题，`E2` 已有公式 `=C2*D2`，而 `E3:E25` 仍为空。
- 确认 `Quantity` 是整数显示，`Unit Price` 和 `Line Total` 列使用两位小数的货币格式；不要改动原始字段标题。

#### 第 1 步：填充全部 Line Total 公式

1. 在 `Delivery Log` 中单击 `E2`。确认输入行或公式栏显示 `=C2*D2`，而不是手动输入一个固定金额。
2. 将鼠标移到所选单元格右下角的小方块（填充柄）。在相邻的 `Quantity`、`Unit Price` 数据连续到第 25 行的情况下，双击该填充柄。
3. Calc 应沿连续记录自动填充至 `E25`。如果双击后只填充了部分行，或 `E3:E25` 仍有空白，请重新选择 `E2`，拖动填充柄向下直到 `E25`；也可将 `E2` 的公式复制到缺失区域，确保相对引用按行变化。

- 对应 skills：`0bf05a7d-b28b-44d2-955a-50b41e24012a.skill-02`
- 高效操作：先利用已有的种子公式，只需一次双击填充柄即可完成其余 23 行，避免逐行输入公式。
- 完成标志：`E2:E25` 均显示货币金额。单击例如 `E3` 时，公式栏显示 `=C3*D3`，而单击 `E25` 时显示对应第 25 行的相对引用。

#### 第 2 步：插入默认名称的工作表

1. 在底部工作表标签区域，点击 `Delivery Log` 标签旁的加号按钮以插入工作表。
2. 观察新建的工作表标签。预期 Calc 自动命名为 `Sheet2`，此时不需要作任何改名操作。
3. 如果新标签不是 `Sheet2`，说明工作簿中已有同名工作表或新增了额外工作表；返回标签区域确认并使用本任务所需的默认新建工作表作为 Pivot Table 输出页，且不要把 `Delivery Log` 改名。

- 对应 skills：`30e3e107-1cfb-46ee-a755-2cd080d7ba6a.skill-01`
- 高效操作：默认名称正是所需名称时，使用工作表标签旁的加号比通过重命名流程更快。
- 完成标志：底部同时可见 `Delivery Log` 和新标签 `Sheet2`，其中 `Sheet2` 是空白工作表。

#### 第 3 步：选择完整送货登记表并启动 Pivot Table

1. 点击 `Delivery Log` 标签返回源表，并点击表格内任意单元格，例如 `A2`。
2. 按 `Ctrl+A` 选择当前连续数据区域。预期选择范围覆盖标题和所有记录，即 `A1:E25`。
3. 如果可见选择没有覆盖从 `A1` 到 `E25` 的完整表格，请单击 `A1` 后重新按 `Ctrl+A`；若仍未得到该范围，则直接选中 `A1:E25`，不要把空白工作表的大量单元格作为数据源。
4. 打开 `Data` > `Pivot Table` > `Insert or Edit...`。在出现的初始 Pivot Table 来源对话框中，确认检测到的是 `Delivery Log` 的完整表格范围，然后确认进入字段布局对话框。

- 对应 skills：`1de60575-bb6e-4c3d-9e6a-2fa699f9f197.skill-01`
- 高效操作：通过 `Ctrl+A` 一次选中整个连续登记表，让 Calc 自动识别 Pivot Table 的源范围，无须手工逐格指定。
- 完成标志：Pivot Table 字段布局对话框打开，且可用字段中包含 `Garden Zone` 和 `Line Total`；来源是 `Delivery Log` 的完整登记表。

#### 第 4 步：按 Garden Zone 生成 Line Total 汇总

1. 在可用字段列表中，将 `Garden Zone` 拖到 `Row Fields` 区域。
2. 将 `Line Total` 拖到 `Data Fields` 区域。预期该数据字段显示为对 `Line Total` 的 `Sum` 聚合；若已经显示为求和，无需调整。
3. 如果 `Line Total` 在数据区域显示为计数或其他非求和汇总，双击该数据字段，在字段汇总设置中选择 `Sum`，然后确认返回布局。若字段被放到了错误区域，将其从错误区域拖出，再按上述方式放入 `Row Fields` 或 `Data Fields`。
4. 在布局对话框的结果输出位置控件中，将输出位置指定为 `Sheet2` 的空白区域，例如 `Sheet2.A1`（若该控件使用绝对引用格式，则使用 `$Sheet2.$A$1`）。确认输出不会与现有内容重叠后，点击 `OK` 生成结果。

- 对应 skills：`535364ea-05bd-46ea-9937-9f55c68507e8.skill-01`
- 高效操作：在布局对话框中直接拖放字段到对应区域；数值字段通常会自动采用求和，不必先打开额外设置。
- 完成标志：`Sheet2` 出现 Pivot Table：`Garden Zone` 是行标签，每个区域有一个汇总行，数值列为 `Line Total` 的求和，并包含总计。

#### 第 5 步：核对完成结果

1. 回到 `Delivery Log`，检查 `E2`、中间任一行和 `E25` 都是带两位小数的货币结果，并确认没有遗漏的空白 Line Total 单元格。
2. 切换到 `Sheet2`，确认每个 `Garden Zone` 只作为一个行类别出现，数值是支出金额而不是记录数量，并确认存在总计行。
3. 如果 Pivot Table 出现在错误工作表或覆盖了内容，使用 `Data` > `Pivot Table` > `Insert or Edit...` 重新打开其设置，将结果输出位置改为 `Sheet2` 的清晰空白区域，例如 `$Sheet2.$A$1`，然后重新生成。

- 对应 skills：无；这是准备或检查步骤。
- 高效操作：最后只抽查首尾公式和 Pivot Table 的字段角色，即可快速发现填充范围、错误计数或错误输出页等常见问题。
- 完成标志：源表的 24 条记录均有计算后的 `Line Total`，且 `Sheet2` 清晰显示按 `Garden Zone` 汇总的 Line Total 求和 Pivot Table。

#### 最终结果检查

- `Delivery Log` 的 `E2:E25` 都显示货币金额；任选例如 `E3`，公式栏应显示随行号变化的乘法公式，如 `=C3*D3`。
- 工作簿有且仅需新增的默认工作表标签 `Sheet2`，并且没有对该标签进行重命名。
- `Sheet2` 中的 Pivot Table 以 `Garden Zone` 分组，每个 Garden Zone 各有一行；数值列是 `Line Total` 的求和而非计数，并显示总计行。
- 源数据 `Delivery Log!A1:E25` 仍可见，且 Pivot Table 没有覆盖源登记表。

## Source-task similarity review

| Measure | Maximum | Most similar source task |
| --- | ---: | --- |
| Lexical sequence similarity | 0.366762 | 26a8440e-c166-4c50-aef4-bfb77314b46b |
| Semantic cosine similarity | 0.518412 | 51719eea-10bc-4246-a428-ac7c433dd4b3 |

Similarity scores are reviewer aids, not automatic acceptance thresholds. Inspect the contributing source tasks and their complete ordered actions below.

### Source task `0bf05a7d-b28b-44d2-955a-50b41e24012a`

Original instruction:

> I would like to copy all the numbers in the 'Old ID' column to the 'New 7 Digit Id' column, and pad them with zeros in front, to fill them up to seven digits.

Required skills derived from this source task:

- **AutoFill a formula down a contiguous data range using the fill handle** — `0bf05a7d-b28b-44d2-955a-50b41e24012a.skill-02`

Complete ordered single-action sequence:

| Action | Related required skill | Original single action |
| ---: | --- | --- |
| 0 |  | <code>`DOUBLE_CLICK` cell D2</code> |
| 1 |  | <code>`TYPING` &#x27;=TEXT(C2,&quot;0000000&quot;)&#x27; in the formula bar</code> |
| 2 | <strong>★ AutoFill a formula down a contiguous data range using the fill handle</strong><br><code>0bf05a7d-b28b-44d2-955a-50b41e24012a.skill-02</code> | <strong><code>`CLICK` cell D2</code></strong> |
| 3 | <strong>★ AutoFill a formula down a contiguous data range using the fill handle</strong><br><code>0bf05a7d-b28b-44d2-955a-50b41e24012a.skill-02</code> | <strong><code>`DOUBLE_CLICK` the bottom right corner of cell D2</code></strong> |

### Source task `1de60575-bb6e-4c3d-9e6a-2fa699f9f197`

Original instruction:

> Summarize the total revenue for each promotion type in a new sheet (Sheet2) with the promotion names as the column headers using the Pivot Table feature.

Required skills derived from this source task:

- **Create a Pivot Table from the current sheet selection** — `1de60575-bb6e-4c3d-9e6a-2fa699f9f197.skill-01`

Complete ordered single-action sequence:

| Action | Related required skill | Original single action |
| ---: | --- | --- |
| 0 | <strong>★ Create a Pivot Table from the current sheet selection</strong><br><code>1de60575-bb6e-4c3d-9e6a-2fa699f9f197.skill-01</code> | <strong><code>`HOTEKY` &#x27;ctrl-a&#x27;</code></strong> |
| 1 | <strong>★ Create a Pivot Table from the current sheet selection</strong><br><code>1de60575-bb6e-4c3d-9e6a-2fa699f9f197.skill-01</code> | <strong><code>`CLICK` curved arrow icon in the top bar representing insert or edit pivot table</code></strong> |
| 2 | <strong>★ Create a Pivot Table from the current sheet selection</strong><br><code>1de60575-bb6e-4c3d-9e6a-2fa699f9f197.skill-01</code> | <strong><code>`CLICK` ok</code></strong> |
| 3 |  | <code>`MOVE_TO` &#x27;Promotion&#x27; in available fields section</code> |
| 4 |  | <code>`DRAG_TO` &#x27;Column fields&#x27; box</code> |
| 5 |  | <code>`MOVE_TO` &#x27;Revenue&#x27; in available fields section&#x27;</code> |
| 6 |  | <code>`DRAG_TO` &#x27;Data fields&#x27; box</code> |
| 7 |  | <code>`CLICK` ok</code> |
| 8 |  | <code>`DOUBLE_CLICK` on name &#x27;Pivot Table_Sheet1_1&#x27;</code> |
| 9 |  | <code>`TYPING` &#x27;Sheet2&#x27;</code> |
| 10 |  | <code>`PRESS` Enter</code> |

### Source task `30e3e107-1cfb-46ee-a755-2cd080d7ba6a`

Original instruction:

> Please create a new sheet. Keep its sheet name as "Sheet2". Merge cells A1:C1 in the new sheet and write "Demographic Profile" with blue (#0000ff) fill and bold white text. Then I want to create three pivot tables to show the percentage of Sex, Civil Status, and Highest Educational Attainment. They should be stacked one by one in Sheet2, each separated with a blank line.

Required skills derived from this source task:

- **Insert a new worksheet with the default name** — `30e3e107-1cfb-46ee-a755-2cd080d7ba6a.skill-01`

Complete ordered single-action sequence:

| Action | Related required skill | Original single action |
| ---: | --- | --- |
| 0 | <strong>★ Insert a new worksheet with the default name</strong><br><code>30e3e107-1cfb-46ee-a755-2cd080d7ba6a.skill-01</code> | <strong><code>`CLICK` on + to left of sheet1</code></strong> |
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
| 13 |  | <code>`CLICK` font color arrow icon, which is to left of bucket</code> |
| 14 |  | <code>`CLICK` top right color in the color palette (white)</code> |
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
| 26 |  | <code>`CLICK` &#x27;displayed value&#x27; dropdown</code> |
| 27 |  | <code>`CLICK` Normal dropdown next to &#x27;Type&#x27;</code> |
| 28 |  | <code>`CLICK` &#x27;% of total&#x27;</code> |
| 29 |  | <code>`CLICK` ok</code> |
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
| 46 |  | <code>`CLICK` &#x27;displayed value&#x27; dropdown</code> |
| 47 |  | <code>`CLICK` Normal dropdown next to &#x27;Type&#x27;</code> |
| 48 |  | <code>`CLICK` &#x27;% of total&#x27;</code> |
| 49 |  | <code>`PRESS` enter</code> |
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
| 66 |  | <code>`CLICK` &#x27;displayed value&#x27; dropdown</code> |
| 67 |  | <code>`CLICK` Normal dropdown next to &#x27;Type&#x27;</code> |
| 68 |  | <code>`CLICK` &#x27;% of total&#x27;</code> |
| 69 |  | <code>`PRESS` enter</code> |
| 70 |  | <code>`CLICK` source and destination dropdown</code> |
| 71 |  | <code>`CLICK` &#x27;Selection&#x27; under destination</code> |
| 72 |  | <code>`CLICK` text box</code> |
| 73 |  | <code>`TYPING` &#x27;$Sheet2.$A$13&#x27;</code> |
| 74 |  | <code>`CLICK` ok</code> |

### Source task `535364ea-05bd-46ea-9937-9f55c68507e8`

Original instruction:

> Create two pivot tables in a new sheet showing the total revenue for each product and sales channel.

Required skills derived from this source task:

- **Create a Pivot Table with a row field and summed data field** — `535364ea-05bd-46ea-9937-9f55c68507e8.skill-01`

Complete ordered single-action sequence:

| Action | Related required skill | Original single action |
| ---: | --- | --- |
| 0 | <strong>★ Create a Pivot Table with a row field and summed data field</strong><br><code>535364ea-05bd-46ea-9937-9f55c68507e8.skill-01</code> | <strong><code>`HOTKEY` ctrl-a</code></strong> |
| 1 | <strong>★ Create a Pivot Table with a row field and summed data field</strong><br><code>535364ea-05bd-46ea-9937-9f55c68507e8.skill-01</code> | <strong><code>`CLICK` pivot table icon</code></strong> |
| 2 | <strong>★ Create a Pivot Table with a row field and summed data field</strong><br><code>535364ea-05bd-46ea-9937-9f55c68507e8.skill-01</code> | <strong><code>`PRESS` enter</code></strong> |
| 3 | <strong>★ Create a Pivot Table with a row field and summed data field</strong><br><code>535364ea-05bd-46ea-9937-9f55c68507e8.skill-01</code> | <strong><code>`MOVE_TO` product in available fields box</code></strong> |
| 4 | <strong>★ Create a Pivot Table with a row field and summed data field</strong><br><code>535364ea-05bd-46ea-9937-9f55c68507e8.skill-01</code> | <strong><code>`DRAG_TO` row fields box</code></strong> |
| 5 | <strong>★ Create a Pivot Table with a row field and summed data field</strong><br><code>535364ea-05bd-46ea-9937-9f55c68507e8.skill-01</code> | <strong><code>`MOVE_TO` revenue in available fields box</code></strong> |
| 6 | <strong>★ Create a Pivot Table with a row field and summed data field</strong><br><code>535364ea-05bd-46ea-9937-9f55c68507e8.skill-01</code> | <strong><code>`DRAG_TO` data fields box</code></strong> |
| 7 | <strong>★ Create a Pivot Table with a row field and summed data field</strong><br><code>535364ea-05bd-46ea-9937-9f55c68507e8.skill-01</code> | <strong><code>`CLICK` ok</code></strong> |
| 8 |  | <code>`DOUBLE_CLICK` Pivot Table Sheet1_1</code> |
| 9 |  | <code>`TYPING` Sheet2</code> |
| 10 |  | <code>`PRESS` enter</code> |
| 11 |  | <code>`CLICK` sheet &#x27;Sheet1&#x27;</code> |
| 12 | <strong>★ Create a Pivot Table with a row field and summed data field</strong><br><code>535364ea-05bd-46ea-9937-9f55c68507e8.skill-01</code> | <strong><code>`HOTKEY` ctrl-a</code></strong> |
| 13 | <strong>★ Create a Pivot Table with a row field and summed data field</strong><br><code>535364ea-05bd-46ea-9937-9f55c68507e8.skill-01</code> | <strong><code>`CLICK` pivot table icon</code></strong> |
| 14 | <strong>★ Create a Pivot Table with a row field and summed data field</strong><br><code>535364ea-05bd-46ea-9937-9f55c68507e8.skill-01</code> | <strong><code>`PRESS` enter</code></strong> |
| 15 | <strong>★ Create a Pivot Table with a row field and summed data field</strong><br><code>535364ea-05bd-46ea-9937-9f55c68507e8.skill-01</code> | <strong><code>`MOVE_TO` sales channel in available fields box</code></strong> |
| 16 | <strong>★ Create a Pivot Table with a row field and summed data field</strong><br><code>535364ea-05bd-46ea-9937-9f55c68507e8.skill-01</code> | <strong><code>`DRAG_TO` row fields box</code></strong> |
| 17 | <strong>★ Create a Pivot Table with a row field and summed data field</strong><br><code>535364ea-05bd-46ea-9937-9f55c68507e8.skill-01</code> | <strong><code>`MOVE_TO` revenue in available fields box</code></strong> |
| 18 | <strong>★ Create a Pivot Table with a row field and summed data field</strong><br><code>535364ea-05bd-46ea-9937-9f55c68507e8.skill-01</code> | <strong><code>`DRAG_TO` data fields box</code></strong> |
| 19 |  | <code>`CLICK` Source and Destination dropdown</code> |
| 20 |  | <code>`CLICK` &#x27;Selection&#x27; under destination</code> |
| 21 |  | <code>`CLICK` text box</code> |
| 22 |  | <code>`TYPING` &#x27;$Sheet2.$A$15&#x27;</code> |
| 23 |  | <code>`CLICK` ok</code> |

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
