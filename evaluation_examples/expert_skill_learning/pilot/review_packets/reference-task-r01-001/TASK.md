# Workshop Enrollment Queue

- Reference task: `reference-task-r01-001`
- Application: `libreoffice_calc`
- Review decision: `pending`

## Task instruction

In the Workshop Enrollment Queue, create a new "Program Registration Counts" summary that shows how many enrollment records each Program has, using Participant Code as the registration measure. Also make Review entries in the Enrollment Log's Queue Flag column stand out with a formula-driven custom pale-amber background (#FCE4D6), while leaving Ready and Confirmed entries unhighlighted.

## Required skills

### 1. Set a Pivot Table value aggregation to Count

Skill ID: `1954cced-e748-45c4-9c26-9855b97fbc5e.skill-04`

Procedure:

1. Double-click the field shown in the Data Fields area to open its data-field settings.
2. Choose the Count aggregation option instead of a numeric summary such as Sum.
3. Confirm the aggregation setting, then confirm the Pivot Table layout to create or update the table.

Efficiency tip: Open the data-field settings immediately after placing a field so its aggregation is correct before finalizing the layout.

Source task: `1954cced-e748-45c4-9c26-9855b97fbc5e`

Source instruction: Create a Pivot Table in a new sheet (Sheet2) to count how many times each "Invoice No." appears.

Directly referenced source actions:

- Action 7: <code>`DOUBLE_CLICK on invoice no. box in data fields</code>
- Action 8: <code>`CLICK` Count</code>
- Action 9: <code>`PRESS` enter</code>
- Action 10: <code>`CLICK` ok</code>

### 2. Create a formula-based conditional formatting rule

Skill ID: `8b1ce5f2-59d2-4dcc-b0b0-666a714b9a14.skill-01`

Procedure:

1. Select the cells to evaluate; for example, press Ctrl+A to select the current sheet’s used range or select a specific calendar range.
2. Open Format > Conditional > Condition.
3. In the condition type drop-down, choose Formula is.
4. Enter a formula that returns TRUE for cells to format. For example, `=AND(WEEKDAY(A1,2)>5,NOT(ISBLANK(A1)))` evaluates weekend dates while excluding blank cells.
5. After assigning or creating the desired style, confirm the conditional-formatting dialog to save the rule. The relative reference `A1` is evaluated relative to each cell in the formatted range.

Efficiency tip: Select the entire target range before opening Conditional Formatting so one rule applies to all cells at once; use relative references such as A1 so Calc evaluates the corresponding cell in each position.

Source task: `8b1ce5f2-59d2-4dcc-b0b0-666a714b9a14`

Source instruction: Given a partial calendar, please highlight all the weekends (Satureday & Sunday) by setting the cell background as red (#ff0000).

Directly referenced source actions:

- Action 0: <code>`HOTKEY` ctrl-A</code>
- Action 1: <code>`CLICK` format</code>
- Action 2: <code>`MOVE_TO` conditional...</code>
- Action 3: <code>`CLICK` condition</code>
- Action 4: <code>`CLICK` cell value dropdown</code>
- Action 5: <code>`CLICK` formula is</code>
- Action 6: <code>`CLICK` formula text field</code>
- Action 7: <code>`TYPING` =AND(WEEKDAY(A1,2)&gt;5, NOT(ISBLANK(A1)))</code>
- Action 14: <code>`CLICK` OK</code>

### 3. Create a custom cell style with a background color

Skill ID: `8b1ce5f2-59d2-4dcc-b0b0-666a714b9a14.skill-02`

Procedure:

1. In the conditional-formatting dialog’s Apply Style control, open the style drop-down and choose New Style.
2. In the style dialog, open the Background settings, then open the color chooser.
3. Choose the required background color; for example, select red (`#ff0000`).
4. Confirm the style dialog with OK so the new style is available for assignment to the conditional rule.

Efficiency tip: Create a custom style from the conditional-format dialog rather than manually filling cells; the same style can then be reused by other conditional rules.

Source task: `8b1ce5f2-59d2-4dcc-b0b0-666a714b9a14`

Source instruction: Given a partial calendar, please highlight all the weekends (Satureday & Sunday) by setting the cell background as red (#ff0000).

Directly referenced source actions:

- Action 8: <code>`CLICK` Apply style dropdown</code>
- Action 9: <code>`CLICK` New Style...</code>
- Action 10: <code>`CLICK` Background</code>
- Action 11: <code>`CLICK` Color</code>
- Action 12: <code>`CLICK` red</code>
- Action 13: <code>`CLICK` OK</code>

## Initial state preview

### Enrollment Log

![Enrollment_Log.png](artifact/previews/Enrollment_Log.png)

## Operator guide

### Existing operation-intent guide

#### Demonstration 1

- Skill: `1954cced-e748-45c4-9c26-9855b97fbc5e.skill-04`
- Intent: Build a program-level registration summary on a new sheet, grouping the enrollment records by Program and counting nonblank Participant Code entries rather than totaling any numeric field.
- Efficiency: After adding Participant Code to the pivot values, open its value settings immediately and set the summary type before confirming the pivot layout.
- Visible success: The new summary shows one row for each of the four programs with counts 8, 7, 6, and 7, for a total of 28 registrations.

#### Demonstration 2

- Skill: `8b1ce5f2-59d2-4dcc-b0b0-666a714b9a14.skill-01`
- Intent: Apply one formula-based conditional-formatting rule to Queue Flag cells that evaluates true only when the corresponding flag is Review.
- Efficiency: Select the full Queue Flag data range first and use a row-relative formula such as =G2="Review" so the same rule evaluates each flag cell.
- Visible success: All and only the eight Queue Flag cells containing Review receive the conditional appearance; Ready and Confirmed cells remain unchanged.

#### Demonstration 3

- Skill: `8b1ce5f2-59d2-4dcc-b0b0-666a714b9a14.skill-02`
- Intent: Create and assign a new custom style with a pale amber background (#FCE4D6) for the Review condition.
- Efficiency: Create the style from the conditional-formatting workflow so it can be assigned directly to the formula rule instead of manually coloring individual cells.
- Visible success: The Review cells visibly have the new pale-amber fill, and the assigned formatting is a reusable custom style rather than direct cell formatting.

Recording start: The workbook opens on Enrollment Log with the raw 28-row enrollment table and no pivot table, conditional-formatting rule, or required custom style.

Recording end: A new Program Registration Counts sheet contains a pivot summary that counts Participant Code registrations by Program, and Enrollment Log Queue Flag cells with Review are conditionally filled pale amber using a newly created custom style.

Allowed variation: The operator may create the summary sheet before or during pivot creation and may use any equivalent Calc dialogs or menus. The custom style may be named freely, provided it is newly created for the rule and has the specified pale-amber background.

### 中文详细参考方案

> 以下是一个可以参考的操作 guide。标注者可以根据实际 LibreOffice 界面采用等价操作。

本指南将在 Enrollment Log 的 28 条报名记录上建立按 Program 汇总的注册人数数据透视表，并对 Queue Flag 列中的 Review 状态应用基于公式的淡琥珀色条件格式。

#### 启动后的初始状态检查

- 确认工作簿已打开，当前工作表为 Enrollment Log。
- 确认原始数据表连续位于 A1:G29，第一行是标题行；其中 Program 位于 B 列、Participant Code 位于 D 列、Queue Flag 位于 G 列。
- 确认尚不存在名为 Program Registration Counts 的工作表，且 Queue Flag 列当前没有针对 Review 的淡琥珀色条件格式。

#### 第 1 步：确认原始报名表和目标范围

1. 在 Enrollment Log 中查看第 1 行标题，确认 B1 为 Program、D1 为 Participant Code、G1 为 Queue Flag。
2. 确认数据从第 2 行延续到第 29 行，且 Queue Flag 的数据范围是 G2:G29。
3. 可在 Queue Flag 列中查看 Review、Ready 和 Confirmed 值；此时不要直接给单元格填充颜色。

- 对应 skills：无；这是准备或检查步骤。
- 高效操作：先确认列位置和数据末行，后续可一次性准确选择 A1:G29 与 G2:G29，避免把标题行或空白区域包含进规则。
- 完成标志：可以看到 Enrollment Log 的完整 A1:G29 数据表，并能确定 Program、Participant Code 与 Queue Flag 三个字段。

#### 第 2 步：从报名记录创建数据透视表

1. 在 Enrollment Log 中选中 A1:G29。可先单击 A1，再按住 Shift 单击 G29，确保标题行也被选中。
2. 打开“数据”菜单，选择“数据透视表”中的“插入或编辑”（不同版本的文字可能略有差异）。
3. 在出现的数据源确认界面中，确认当前选择的数据范围为 Enrollment Log 的 A1:G29，然后继续进入数据透视表布局窗口。

- 对应 skills：无；这是准备或检查步骤。
- 高效操作：从包含标题的完整连续数据区域启动数据透视表，Calc 才能正确识别所有字段名称。
- 完成标志：屏幕显示数据透视表布局窗口，字段列表中包含 Program 和 Participant Code。

#### 第 3 步：按 Program 统计非空 Participant Code

1. 在数据透视表布局中，将 Program 字段拖放到“行字段”区域，使每个 Program 成为一行汇总项目。
2. 将 Participant Code 字段拖放到“数据字段”区域。
3. 双击“数据字段”区域中的 Participant Code，打开该数据字段的设置。
4. 在汇总方式中选择 Count，而不是 Sum 或其他数值汇总方式；确认设置。
5. 确认布局中 Program 位于行字段、Participant Code 位于数据字段且汇总方式为 Count，然后确认数据透视表布局。

- 对应 skills：`1954cced-e748-45c4-9c26-9855b97fbc5e.skill-04`
- 高效操作：将 Participant Code 放入数据字段后立刻打开其设置并改为 Count，可避免默认汇总方式不符合“报名记录数”的要求。
- 完成标志：数据字段设置显示 Participant Code 使用 Count（计数）汇总，布局可按 Program 输出计数。

#### 第 4 步：创建并命名 Program Registration Counts 汇总表

1. 在选择结果位置的界面中，选择将数据透视表放到新工作表，然后确认创建。
2. 在新建工作表的标签上右键或双击标签，选择重命名，将工作表名称改为 Program Registration Counts。
3. 检查透视表的 Program 行项目和 Participant Code 计数。若字段标题显示为类似“Count - Participant Code”，这是正常的计数数据字段标题。

- 对应 skills：无；这是准备或检查步骤。
- 高效操作：让透视表输出到新工作表可使原始 Enrollment Log 保持不变，也便于单独检查汇总结果。
- 完成标志：存在名为 Program Registration Counts 的新工作表；表中四个 Program 的计数为 Community Garden 8、Digital Basics 7、First Aid 6、Resume Lab 7，合计为 28。

#### 第 5 步：为 Review 建立公式条件

1. 切换回 Enrollment Log 工作表。
2. 选中 Queue Flag 数据单元格 G2:G29，不要包含标题单元格 G1。
3. 打开“格式”菜单，选择“条件”，再选择“条件…”。
4. 在条件类型下拉列表中选择 Formula is（公式为）。
5. 在公式输入框中输入 =G2="Review"。这里的 G2 是所选范围左上角的相对引用，Calc 会对 G3、G4 等后续单元格分别判断对应行的值。

- 对应 skills：`8b1ce5f2-59d2-4dcc-b0b0-666a714b9a14.skill-01`
- 高效操作：先只选择 G2:G29，再建立一条公式规则；这样公式会逐行相对计算，并且不会影响 Queue Flag 标题或其他列。
- 完成标志：条件格式对话框中已显示 Formula is，且公式框包含 =G2="Review"。

#### 第 6 步：新建淡琥珀色 Review 条件样式

1. 仍在条件格式对话框中，打开 Apply Style（应用样式）下拉列表并选择 New Style（新建样式）。
2. 为新样式输入一个易识别的名称，例如 Review Pale Amber。
3. 在样式设置窗口中打开“背景”设置，再打开颜色选择器。
4. 选择或输入背景颜色 #FCE4D6，并确认颜色选择。
5. 确认样式设置窗口，使新建样式返回到条件格式规则的 Apply Style 列表中并被选中。

- 对应 skills：`8b1ce5f2-59d2-4dcc-b0b0-666a714b9a14.skill-02`
- 高效操作：从条件格式对话框中新建样式，样式会被规则引用；不要使用工具栏的直接填充色，以免所有状态都被永久着色。
- 完成标志：条件格式规则已分配一个新建样式，该样式的背景色为 #FCE4D6。

#### 第 7 步：保存规则并完成核验

1. 确认条件格式对话框以保存规则。
2. 查看 G2:G29：所有内容为 Review 的 Queue Flag 单元格应显示淡琥珀色背景 #FCE4D6。
3. 逐项确认 Ready 和 Confirmed 单元格保持原有外观，没有淡琥珀色背景。
4. 如有必要，重新打开“格式 > 条件 > 条件…”检查应用范围仍是 G2:G29，公式仍是 =G2="Review"，并确认使用的是刚创建的样式。

- 对应 skills：无；这是准备或检查步骤。
- 高效操作：保存后同时检查“匹配的单元格”和“不匹配的单元格”，能快速发现公式引用是否错误或是否把标题行包含在范围内。
- 完成标志：Enrollment Log 中仅 8 个 Review 单元格被淡琥珀色突出显示，Ready 和 Confirmed 单元格未被突出显示。

#### 最终结果检查

- 工作簿中有一个名为 Program Registration Counts 的工作表，其中的数据透视表按 Program 列出 Community Garden、Digital Basics、First Aid、Resume Lab；Participant Code 的计数分别为 8、7、6、7，合计为 28。
- Enrollment Log 的 G2:G29 中，恰好 8 个值为 Review 的单元格显示淡琥珀色背景 #FCE4D6；值为 Ready 或 Confirmed 的单元格没有该背景。
- 选择任一 Review 单元格并检查条件格式时，可看到它来自公式规则和新建的单元格样式，而不是手动填充颜色。

## Source-task similarity review

| Measure | Maximum | Most similar source task |
| --- | ---: | --- |
| Lexical sequence similarity | 0.204633 | 8b1ce5f2-59d2-4dcc-b0b0-666a714b9a14 |
| Semantic cosine similarity | 0.319971 | 8b1ce5f2-59d2-4dcc-b0b0-666a714b9a14 |

Similarity scores are reviewer aids, not automatic acceptance thresholds. Inspect the contributing source tasks and their complete ordered actions below.

### Source task `1954cced-e748-45c4-9c26-9855b97fbc5e`

Original instruction:

> Create a Pivot Table in a new sheet (Sheet2) to count how many times each "Invoice No." appears.

Required skills derived from this source task:

- **Set a Pivot Table value aggregation to Count** — `1954cced-e748-45c4-9c26-9855b97fbc5e.skill-04`

Complete ordered single-action sequence:

| Action | Related required skill | Original single action |
| ---: | --- | --- |
| 0 |  | <code>`CLICK` on grey cell box A for selecting entire column</code> |
| 1 |  | <code>`CLICK` on pivot table icon</code> |
| 2 |  | <code>`PRESS` enter</code> |
| 3 |  | <code>`MOVE_TO` invoice no. in available fields box</code> |
| 4 |  | <code>`DRAG_TO` row fields box</code> |
| 5 |  | <code>`MOVE_TO` invoice no. in available fields box</code> |
| 6 |  | <code>`DRAG_TO` data fields box</code> |
| 7 | <strong>★ Set a Pivot Table value aggregation to Count</strong><br><code>1954cced-e748-45c4-9c26-9855b97fbc5e.skill-04</code> | <strong><code>`DOUBLE_CLICK on invoice no. box in data fields</code></strong> |
| 8 | <strong>★ Set a Pivot Table value aggregation to Count</strong><br><code>1954cced-e748-45c4-9c26-9855b97fbc5e.skill-04</code> | <strong><code>`CLICK` Count</code></strong> |
| 9 | <strong>★ Set a Pivot Table value aggregation to Count</strong><br><code>1954cced-e748-45c4-9c26-9855b97fbc5e.skill-04</code> | <strong><code>`PRESS` enter</code></strong> |
| 10 | <strong>★ Set a Pivot Table value aggregation to Count</strong><br><code>1954cced-e748-45c4-9c26-9855b97fbc5e.skill-04</code> | <strong><code>`CLICK` ok</code></strong> |
| 11 |  | <code>`DOUBLE_CLICK` Pivot Table Sheet1_1</code> |
| 12 |  | <code>`TYPING` Sheet2</code> |
| 13 |  | <code>`PRESS` enter</code> |

### Source task `8b1ce5f2-59d2-4dcc-b0b0-666a714b9a14`

Original instruction:

> Given a partial calendar, please highlight all the weekends (Satureday & Sunday) by setting the cell background as red (#ff0000).

Required skills derived from this source task:

- **Create a formula-based conditional formatting rule** — `8b1ce5f2-59d2-4dcc-b0b0-666a714b9a14.skill-01`
- **Create a custom cell style with a background color** — `8b1ce5f2-59d2-4dcc-b0b0-666a714b9a14.skill-02`

Complete ordered single-action sequence:

| Action | Related required skill | Original single action |
| ---: | --- | --- |
| 0 | <strong>★ Create a formula-based conditional formatting rule</strong><br><code>8b1ce5f2-59d2-4dcc-b0b0-666a714b9a14.skill-01</code> | <strong><code>`HOTKEY` ctrl-A</code></strong> |
| 1 | <strong>★ Create a formula-based conditional formatting rule</strong><br><code>8b1ce5f2-59d2-4dcc-b0b0-666a714b9a14.skill-01</code> | <strong><code>`CLICK` format</code></strong> |
| 2 | <strong>★ Create a formula-based conditional formatting rule</strong><br><code>8b1ce5f2-59d2-4dcc-b0b0-666a714b9a14.skill-01</code> | <strong><code>`MOVE_TO` conditional...</code></strong> |
| 3 | <strong>★ Create a formula-based conditional formatting rule</strong><br><code>8b1ce5f2-59d2-4dcc-b0b0-666a714b9a14.skill-01</code> | <strong><code>`CLICK` condition</code></strong> |
| 4 | <strong>★ Create a formula-based conditional formatting rule</strong><br><code>8b1ce5f2-59d2-4dcc-b0b0-666a714b9a14.skill-01</code> | <strong><code>`CLICK` cell value dropdown</code></strong> |
| 5 | <strong>★ Create a formula-based conditional formatting rule</strong><br><code>8b1ce5f2-59d2-4dcc-b0b0-666a714b9a14.skill-01</code> | <strong><code>`CLICK` formula is</code></strong> |
| 6 | <strong>★ Create a formula-based conditional formatting rule</strong><br><code>8b1ce5f2-59d2-4dcc-b0b0-666a714b9a14.skill-01</code> | <strong><code>`CLICK` formula text field</code></strong> |
| 7 | <strong>★ Create a formula-based conditional formatting rule</strong><br><code>8b1ce5f2-59d2-4dcc-b0b0-666a714b9a14.skill-01</code> | <strong><code>`TYPING` =AND(WEEKDAY(A1,2)&gt;5, NOT(ISBLANK(A1)))</code></strong> |
| 8 | <strong>★ Create a custom cell style with a background color</strong><br><code>8b1ce5f2-59d2-4dcc-b0b0-666a714b9a14.skill-02</code> | <strong><code>`CLICK` Apply style dropdown</code></strong> |
| 9 | <strong>★ Create a custom cell style with a background color</strong><br><code>8b1ce5f2-59d2-4dcc-b0b0-666a714b9a14.skill-02</code> | <strong><code>`CLICK` New Style...</code></strong> |
| 10 | <strong>★ Create a custom cell style with a background color</strong><br><code>8b1ce5f2-59d2-4dcc-b0b0-666a714b9a14.skill-02</code> | <strong><code>`CLICK` Background</code></strong> |
| 11 | <strong>★ Create a custom cell style with a background color</strong><br><code>8b1ce5f2-59d2-4dcc-b0b0-666a714b9a14.skill-02</code> | <strong><code>`CLICK` Color</code></strong> |
| 12 | <strong>★ Create a custom cell style with a background color</strong><br><code>8b1ce5f2-59d2-4dcc-b0b0-666a714b9a14.skill-02</code> | <strong><code>`CLICK` red</code></strong> |
| 13 | <strong>★ Create a custom cell style with a background color</strong><br><code>8b1ce5f2-59d2-4dcc-b0b0-666a714b9a14.skill-02</code> | <strong><code>`CLICK` OK</code></strong> |
| 14 | <strong>★ Create a formula-based conditional formatting rule</strong><br><code>8b1ce5f2-59d2-4dcc-b0b0-666a714b9a14.skill-01</code> | <strong><code>`CLICK` OK</code></strong> |

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
