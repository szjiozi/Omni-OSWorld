# Service Estimate Review

- Reference task: `reference-task-calc-full-r01-003`
- Application: `libreoffice_calc`
- Review decision: `pending`

## Task instruction

Prepare the service-estimate review workbook: add readable estimate notes for every service request using the rate card, lay out the Overview checklist as a horizontal heading row instead of its current vertical list, and zoom out the worksheet slightly for easier review.

## Required skills

### 1. Move a cell or range while transposing it

Skill ID: `26a8440e-c166-4c50-aef4-bfb77314b46b.skill-05`

Procedure:

1. Select the source cell or range and press Ctrl+X to cut it.
2. Select the top-left destination cell, right-click it, open Paste Special, and choose Transpose.
3. Calc moves the cut content to the destination while swapping its row and column orientation. For example, cutting a vertical range and transposing it pastes the values horizontally.

Efficiency tip: Use Cut rather than Copy when the original cell should be removed after the transposed placement, avoiding a separate delete step.

Source task: `26a8440e-c166-4c50-aef4-bfb77314b46b`

Source instruction: Create a table with two column headers ("Month" and "Total") in a new sheet named "Sheet2" to show the total sales for all months.

Directly referenced source actions:

- Action 18: <code>`HOTKEY` ctrl+x</code>
- Action 19: <code>`CLICK` on B2</code>
- Action 20: <code>`RIGHT_CLICK`</code>
- Action 21: <code>`MOVE_TO` paste special</code>
- Action 22: <code>`CLICK` transpose</code>

### 2. Propagate a text formula down an output column

Skill ID: `4de54231-e4b5-49e3-b2ba-61a0bec721c0.skill-03`

Procedure:

1. Select the first output cell containing the completed formula, such as E2.
2. Double-click the bottom-right fill handle of that cell.
3. Calc copies the formula down to the last row detected from neighboring continuous data, updating relative references such as A2 to A3, A4, and so on while preserving absolute references such as $A$1.

Efficiency tip: After entering a row formula, reselect its first cell and double-click its fill handle instead of copying and pasting or dragging through every destination row.

Source task: `4de54231-e4b5-49e3-b2ba-61a0bec721c0`

Source instruction: I have compute the acceleration in row 2 and I want you to fill out other rows for column B and D. Next concatenate the values from columns A to D, including their headers (the pattern is "Header: cell value, ..., Header: cell value"), into a new column named "Combined Data" for all rows. In the new column, only keep 2 decimal digits.

Directly referenced source actions:

- Action 8: <code>`CLICK` on cell E2</code>
- Action 9: <code>`DOUBLE_CLICK` bottom right corner of the cell E2</code>

### 3. Decrease worksheet zoom with the status-bar zoom slider

Skill ID: `1334ca3e-f9e3-4db8-9ca7-b4c653be7d17.skill-01`

Procedure:

1. In LibreOffice Calc, locate the zoom slider in the bottom-right status bar.
2. Click on the left/decrease side of the slider to zoom the worksheet out. For example, one click reduces the displayed cell size so more rows and columns fit on screen.
3. Repeat only as needed until cells are comfortably selectable at the desired scale.

Efficiency tip: Use the slider for a quick incremental adjustment; click closer to the desired level rather than repeatedly clicking the decrease end when a larger reduction is needed.

Source task: `1334ca3e-f9e3-4db8-9ca7-b4c653be7d17`

Source instruction: The cells are so big that I can not click on the cell I want, zoom out a little bit.

Directly referenced source actions:

- Action 0: <code>`CLICK` on the left-hand side of the zoom slider at the bottom right corner of the screen</code>

### 4. Build a cross-sheet lookup formula with row arithmetic

Skill ID: `51719eea-10bc-4246-a428-ac7c433dd4b3.skill-01`

Procedure:

1. In the first result cell, enter a formula that looks up a value from another sheet and combines it with values from the current row.
2. For example, enter `=VLOOKUP(C2,$'Retail Price'.$A$2:$B$23,2,FALSE())*E2*(1-F2)` and press Enter. `VLOOKUP` finds the value matching `C2` in the first column of the source range and returns its second column; the remaining multiplication applies the current row's values.
3. In `$'Retail Price'.$A$2:$B$23`, the `$` before the quoted sheet name fixes the source sheet, while `$A$2:$B$23` fixes both columns and rows of the lookup range. The references `C2`, `E2`, and `F2` remain relative, so they adjust when copied to another row.

Efficiency tip: Type the complete formula once in the first result cell, then propagate it rather than rebuilding the lookup and arithmetic separately for every row.

Source task: `51719eea-10bc-4246-a428-ac7c433dd4b3`

Source instruction: Calculate revenue in a new column according to the Retail Price sheet (consider product price and quantity and discount), and generate a Pivot Table in a new sheet (Sheet2) that summarizes the revenue of each product.

Directly referenced source actions:

- Action 5: <code>`TYPING` &#x27;=VLOOKUP(C2,$&#x27;Retail Price&#x27;.$A$2:$B$23,2,FALSE())*E2*(1-F2)&#x27;</code>
- Action 6: <code>`PRESS` enter</code>

## Initial state preview

### Overview

![Overview.png](artifact/previews/Overview.png)

### Rate Card

![Rate_Card.png](artifact/previews/Rate_Card.png)

### Service Requests

![Service_Requests.png](artifact/previews/Service_Requests.png)

## Operator guide

### Existing operation-intent guide

#### Demonstration 1

- Skill: `26a8440e-c166-4c50-aef4-bfb77314b46b.skill-05`
- Intent: On Overview, move the four checklist labels from A3:A6 into the blank B2:E2 heading area while changing their vertical orientation to horizontal.
- Efficiency: Use Cut rather than Copy so the old vertical checklist is cleared automatically after the horizontal placement.
- Visible success: B2:E2 displays the four labels left-to-right in their original top-to-bottom order, and A3:A6 no longer contains those source labels.

#### Demonstration 2

- Skill: `51719eea-10bc-4246-a428-ac7c433dd4b3.skill-01`
- Intent: In the first Estimate Note cell on Service Requests, create a text-producing formula that looks up the unit rate for that row's service code and calculates rate × units × (1 − adjustment), presenting the resulting amount in a readable estimate note.
- Efficiency: Build the full relative-row calculation once, using absolute references for the Rate Card lookup range, rather than constructing separate formulas per request.
- Visible success: E2 shows readable text including a calculated currency estimate, and changing-row references are visible in the formula while the Rate Card table reference remains fixed.

#### Demonstration 3

- Skill: `4de54231-e4b5-49e3-b2ba-61a0bec721c0.skill-03`
- Intent: Propagate the completed Estimate Note formula from E2 down through all 18 request rows.
- Efficiency: After confirming E2, use the fill handle's double-click behavior to extend through the contiguous request records instead of manually copying each result.
- Visible success: Every cell from E2 through E19 contains a text estimate note with row-appropriate calculated values; there are no blank output cells in that range.

#### Demonstration 4

- Skill: `1334ca3e-f9e3-4db8-9ca7-b4c653be7d17.skill-01`
- Intent: Reduce the worksheet display zoom so more of the service-request table is comfortably visible.
- Efficiency: Use the status-bar slider to make one intentional reduction, selecting a comfortable smaller scale instead of many small adjustments.
- Visible success: The status bar indicates a lower zoom than the initial default and visibly more rows or columns fit in the worksheet view.

Recording start: Open the supplied Service Estimate Review workbook in Calc with its three sheets in the described incomplete state.

Recording end: Service Requests has populated text estimate notes in E2:E19 based on the Rate Card and each request row; Overview has the checklist labels only across B2:E2; and worksheet zoom is visibly lower than at the start.

Allowed variation: Equivalent Calc commands, formula syntax accepted by the installed locale, and a different modest zoom-out level are acceptable. The estimate text may use a comparable clear label and currency formatting, provided it remains a text result that uses the Rate Card lookup and the same-row Units and Adjustment arithmetic.

### 中文详细参考方案

> 以下是一个可以参考的操作 guide。标注者可以根据实际 LibreOffice 界面采用等价操作。

本指南完成三个服务估算审阅动作：将 Overview 的纵向检查标签移动并转置为横向标题；利用 Rate Card 中的固定单价为每个服务请求生成文字型估算说明；最后适度缩小工作表显示比例，方便一次审阅更多记录。

#### 启动后的初始状态检查

- 确认工作簿已在 LibreOffice Calc 中打开，并且存在 `Service Requests`、`Rate Card`、`Overview` 三个工作表。
- 在 `Service Requests` 中确认标题位于 A1:E1，数据连续位于 A2:D19，且 `Estimate Note` 列的 E2:E19 仍为空白。
- 在 `Rate Card` 中确认 A1:B7 包含 `Service Code` 与 `Unit Rate` 的固定查找表。
- 在 `Overview` 中确认四个标签仍纵向位于 A3:A6，而 B2:E2 为空。
- 确认当前工作表尚未缩小显示比例。

#### 第 1 步：将 Overview 检查标签移动并转置为横向标题

1. 单击底部工作表标签 `Overview`。
2. 拖动选择范围 A3:A6，其中应依次包含 `Rate verified`、`Adjustment reviewed`、`Estimate prepared`、`Ready to send`。
3. 按 Ctrl+X 剪切该范围。
4. 单击目标区域左上角单元格 B2，然后右键单击 B2。
5. 在右键菜单中打开“选择性粘贴”，选择“转置”。如出现选择性粘贴对话框，启用“转置”选项并确认。

- 对应 skills：`26a8440e-c166-4c50-aef4-bfb77314b46b.skill-05`
- 高效操作：先完成转置移动可立即清空旧位置，不需要之后再手动删除 A3:A6 的内容。
- 完成标志：B2:E2 从左至右显示四个原有标签，顺序与原先 A3:A6 从上至下的顺序一致；A3:A6 已被清空。

#### 第 2 步：在第一条请求中建立文字估算公式

1. 切换到 `Service Requests` 工作表，单击 E2。
2. 输入以下文字型公式，然后按 Enter：`="Estimate: "&TEXT(VLOOKUP(B2,$'Rate Card'.$A$2:$B$7,2,FALSE())*C2*(1-D2),"$#,##0.00")`。
3. 如果本机 Calc 使用分号作为函数参数分隔符，可将公式中的参数逗号改为分号后再确认。
4. 确认公式将 B2 的服务代码到 `Rate Card` 查找单价，乘以当前行 C2 的 Units，并乘以 `(1-D2)` 应用当前行 Adjustment；`TEXT` 会把金额作为文字的一部分显示。

- 对应 skills：`51719eea-10bc-4246-a428-ac7c433dd4b3.skill-01`
- 高效操作：只在第一行写一次完整公式；查找区域使用绝对引用，随后向下填充时不会移动。
- 完成标志：E2 显示以 `Estimate:` 开头并包含货币金额的可读文字。选中 E2 时，公式栏可见相对引用 B2、C2、D2，以及固定的 `$'Rate Card'.$A$2:$B$7` 查找范围。

#### 第 3 步：将估算说明公式填充到所有请求行

1. 保持在 `Service Requests` 工作表，重新单击 E2，确保它是当前选中单元格。
2. 将鼠标移到 E2 选中边框右下角的小方块（填充柄）。
3. 当指针可用于填充时，双击该填充柄。
4. 查看填充结果；相邻的 A:D 列连续有数据，Calc 应将公式自动延伸至 E19。

- 对应 skills：`4de54231-e4b5-49e3-b2ba-61a0bec721c0.skill-03`
- 高效操作：双击填充柄会依据相邻连续数据自动确定终点，比逐行复制或拖动到第 19 行更快。
- 完成标志：E2:E19 每一行均显示文字估算说明，没有空白输出。选择例如 E3 或 E19 时，可见公式中的 B、C、D 行号已相应变为该行行号。

#### 第 4 步：缩小工作表显示比例以便审阅

1. 仍停留在 `Service Requests` 工作表。
2. 在窗口右下角状态栏找到缩放滑块。
3. 单击滑块的左侧（减小）方向，或在当前滑块位置左方选择一个稍小的比例，使工作表适度缩小。
4. 如首次缩小后仍不便于审阅，可再作一次小幅调整；不需要缩小到文字难以辨认。

- 对应 skills：`1334ca3e-f9e3-4db8-9ca7-b4c653be7d17.skill-01`
- 高效操作：可直接在滑块上点击更靠近目标比例的位置，一次完成适度缩小，避免多次点击减小端。
- 完成标志：状态栏显示的缩放百分比低于开始时，且同一屏幕中能舒适地看到更多服务请求行或更多列。

#### 最终结果检查

- 在“Service Requests”中检查 E2:E19：18 个单元格都不为空，均显示可读的文字说明和货币金额；选中其中不同的行时，公式栏中的 B/C/D 行号会随行变化，而 $'Rate Card'.$A$2:$B$7 保持固定。
- 在“Overview”中检查 B2:E2：从左到右依次为 `Rate verified`、`Adjustment reviewed`、`Estimate prepared`、`Ready to send`；A3:A6 已不再保留这些标签。
- 查看“Service Requests”窗口右下角状态栏：缩放比例低于开始时的默认比例，并且屏幕中可见的表格行数或列数增加。
- 确认“Rate Card”的 A1:B7 查找表以及“Service Requests”的 A2:D19 请求输入没有被改动。

## Source-task similarity review

| Measure | Maximum | Most similar source task |
| --- | ---: | --- |
| Lexical sequence similarity | 0.342723 | 42e0a640-4f19-4b28-973d-729602b5a4a7 |
| Semantic cosine similarity | 0.427412 | 51719eea-10bc-4246-a428-ac7c433dd4b3 |

Similarity scores are reviewer aids, not automatic acceptance thresholds. Inspect the contributing source tasks and their complete ordered actions below.

### Source task `1334ca3e-f9e3-4db8-9ca7-b4c653be7d17`

Original instruction:

> The cells are so big that I can not click on the cell I want, zoom out a little bit.

Required skills derived from this source task:

- **Decrease worksheet zoom with the status-bar zoom slider** — `1334ca3e-f9e3-4db8-9ca7-b4c653be7d17.skill-01`

Complete ordered single-action sequence:

| Action | Related required skill | Original single action |
| ---: | --- | --- |
| 0 | <strong>★ Decrease worksheet zoom with the status-bar zoom slider</strong><br><code>1334ca3e-f9e3-4db8-9ca7-b4c653be7d17.skill-01</code> | <strong><code>`CLICK` on the left-hand side of the zoom slider at the bottom right corner of the screen</code></strong> |

### Source task `26a8440e-c166-4c50-aef4-bfb77314b46b`

Original instruction:

> Create a table with two column headers ("Month" and "Total") in a new sheet named "Sheet2" to show the total sales for all months.

Required skills derived from this source task:

- **Move a cell or range while transposing it** — `26a8440e-c166-4c50-aef4-bfb77314b46b.skill-05`

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
| 12 |  | <code>`CLICK` cell B2</code> |
| 13 |  | <code>`TYPING` &#x27;=SUM($Sheet1.B2:B11)&#x27;</code> |
| 14 |  | <code>`PRESS` enter</code> |
| 15 |  | <code>`CLICK` B2</code> |
| 16 |  | <code>`MOVE_TO` bottom right corner of the cell B2</code> |
| 17 |  | <code>`DRAG_TO` G1</code> |
| 18 | <strong>★ Move a cell or range while transposing it</strong><br><code>26a8440e-c166-4c50-aef4-bfb77314b46b.skill-05</code> | <strong><code>`HOTKEY` ctrl+x</code></strong> |
| 19 | <strong>★ Move a cell or range while transposing it</strong><br><code>26a8440e-c166-4c50-aef4-bfb77314b46b.skill-05</code> | <strong><code>`CLICK` on B2</code></strong> |
| 20 | <strong>★ Move a cell or range while transposing it</strong><br><code>26a8440e-c166-4c50-aef4-bfb77314b46b.skill-05</code> | <strong><code>`RIGHT_CLICK`</code></strong> |
| 21 | <strong>★ Move a cell or range while transposing it</strong><br><code>26a8440e-c166-4c50-aef4-bfb77314b46b.skill-05</code> | <strong><code>`MOVE_TO` paste special</code></strong> |
| 22 | <strong>★ Move a cell or range while transposing it</strong><br><code>26a8440e-c166-4c50-aef4-bfb77314b46b.skill-05</code> | <strong><code>`CLICK` transpose</code></strong> |

### Source task `4de54231-e4b5-49e3-b2ba-61a0bec721c0`

Original instruction:

> I have compute the acceleration in row 2 and I want you to fill out other rows for column B and D. Next concatenate the values from columns A to D, including their headers (the pattern is "Header: cell value, ..., Header: cell value"), into a new column named "Combined Data" for all rows. In the new column, only keep 2 decimal digits.

Required skills derived from this source task:

- **Propagate a text formula down an output column** — `4de54231-e4b5-49e3-b2ba-61a0bec721c0.skill-03`

Complete ordered single-action sequence:

| Action | Related required skill | Original single action |
| ---: | --- | --- |
| 0 |  | <code>`CLICK` on cell B2</code> |
| 1 |  | <code>`DOUBLE_CLICK` bottom right corner of the cell B2</code> |
| 2 |  | <code>`CLICK` on cell D2</code> |
| 3 |  | <code>`DOUBLE_CLICK` bottom right corner of the cell D2</code> |
| 4 |  | <code>`CLICK` on cell E1</code> |
| 5 |  | <code>`TYPING` &#x27;Combined Data&#x27;</code> |
| 6 |  | <code>`PRESS` enter</code> |
| 7 |  | <code>`TYPING` &#x27;=$A$1&amp;&quot;: &quot;&amp;FIXED(A2,2)&amp;&quot;, &quot;&amp;$B$1&amp;&quot;: &quot;&amp;FIXED(B2,2)&amp;&quot;, &quot;&amp;$C$1&amp;&quot;: &quot;&amp;FIXED(C2,2)&amp;&quot;, &quot;&amp;$D$1&amp;&quot;: &quot;&amp;FIXED(D2,2)&#x27;</code> |
| 8 | <strong>★ Propagate a text formula down an output column</strong><br><code>4de54231-e4b5-49e3-b2ba-61a0bec721c0.skill-03</code> | <strong><code>`CLICK` on cell E2</code></strong> |
| 9 | <strong>★ Propagate a text formula down an output column</strong><br><code>4de54231-e4b5-49e3-b2ba-61a0bec721c0.skill-03</code> | <strong><code>`DOUBLE_CLICK` bottom right corner of the cell E2</code></strong> |

### Source task `51719eea-10bc-4246-a428-ac7c433dd4b3`

Original instruction:

> Calculate revenue in a new column according to the Retail Price sheet (consider product price and quantity and discount), and generate a Pivot Table in a new sheet (Sheet2) that summarizes the revenue of each product.

Required skills derived from this source task:

- **Build a cross-sheet lookup formula with row arithmetic** — `51719eea-10bc-4246-a428-ac7c433dd4b3.skill-01`

Complete ordered single-action sequence:

| Action | Related required skill | Original single action |
| ---: | --- | --- |
| 0 |  | <code>`CLICK` cell G1</code> |
| 1 |  | <code>`TYPING` &#x27;Revenue&#x27;</code> |
| 2 |  | <code>`PRESS` enter</code> |
| 3 |  | <code>`CLICK` sheet &#x27;Retail Price&#x27;</code> |
| 4 |  | <code>`CLICK` sheet &#x27;Sheet1&#x27;</code> |
| 5 | <strong>★ Build a cross-sheet lookup formula with row arithmetic</strong><br><code>51719eea-10bc-4246-a428-ac7c433dd4b3.skill-01</code> | <strong><code>`TYPING` &#x27;=VLOOKUP(C2,$&#x27;Retail Price&#x27;.$A$2:$B$23,2,FALSE())*E2*(1-F2)&#x27;</code></strong> |
| 6 | <strong>★ Build a cross-sheet lookup formula with row arithmetic</strong><br><code>51719eea-10bc-4246-a428-ac7c433dd4b3.skill-01</code> | <strong><code>`PRESS` enter</code></strong> |
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
| 18 |  | <code>`DOUBLE_CLICK` Pivot Table Sheet1_1</code> |
| 19 |  | <code>`TYPING` Sheet2</code> |
| 20 |  | <code>`PRESS` enter</code> |

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
