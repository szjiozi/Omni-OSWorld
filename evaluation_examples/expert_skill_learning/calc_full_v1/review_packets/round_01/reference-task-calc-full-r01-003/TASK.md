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

本指南完成三项服务估算审核整理：将 `Overview` 的纵向检查标签移动并转置为横向标题，在 `Service Requests` 中用 `Rate Card` 的费率生成每条请求的文字估算说明，再将结果向下填满并适度缩小显示比例。

#### 启动后的初始状态检查

- 确认工作簿包含 `Service Requests`、`Rate Card` 和 `Overview` 三个工作表，且最初打开的是 `Service Requests`。
- 在 `Service Requests` 中确认标题位于 `A1:E1`，请求数据连续位于 `A2:D19`，并且 `E2:E19` 仍为空白。
- 在 `Rate Card` 中确认 `A1:B7` 是包含 `Service Code` 和 `Unit Rate` 的完整费率表；不要修改此表。
- 在 `Overview` 中确认四个标签仍纵向位于 `A3:A6`，而目标区域 `B2:E2` 为空白。
- 查看右下角状态栏，确认尚未缩小工作表显示比例。

#### 第 1 步：将审核清单移动并转置为横向标题

1. 切换到 `Overview` 工作表，选中连续源区域 `A3:A6`。
2. 按 `Ctrl+X` 剪切这四个标签。
3. 单击目标左上角单元格 `B2`，右键单击该单元格，打开 `Paste Special`，然后选择 `Transpose`。

- 对应 skills：`26a8440e-c166-4c50-aef4-bfb77314b46b.skill-05`
- 高效操作：先使用剪切而不是复制，转置完成后源区域会自动清空，无需再手动删除旧的纵向标签。
- 完成标志：`B2:E2` 从左到右显示 `Rate verified`、`Adjustment reviewed`、`Estimate prepared`、`Ready to send`；原来的 `A3:A6` 不再包含这些标签。

#### 第 2 步：在首条请求中建立费率查找和估算文字公式

1. 切换到 `Service Requests`，单击第一个输出单元格 `E2`。
2. 输入以下文字结果公式，然后按 `Enter`：`="Estimated total: "&TEXT(VLOOKUP(B2,$'Rate Card'.$A$2:$B$7,2,FALSE())*C2*(1-D2),"$#,##0.00")`。
3. 保持或重新选中 `E2`，查看公式栏：其中 `B2`、`C2`、`D2` 是当前行引用，而 `$'Rate Card'.$A$2:$B$7` 是固定的跨工作表查找区域。

- 对应 skills：`51719eea-10bc-4246-a428-ac7c433dd4b3.skill-01`
- 高效操作：一次写出带绝对查找区域的完整公式；只有当前请求行的引用应随填充改变，费率表范围不应改变。
- 完成标志：`E2` 显示以 `Estimated total:` 开头的文字及货币金额；对于第一条 `DIAG`、2 个单位、0% 调整的请求，金额应反映费率乘以数量后的结果。

#### 第 3 步：将估算说明公式填充到所有请求行

1. 选中含有已验证公式的 `E2`。
2. 找到选中单元格右下角的小方块填充柄，并双击它。
3. 向下检查结果区域，必要时滚动到第 19 行，确认填充已经覆盖全部请求记录。

- 对应 skills：`4de54231-e4b5-49e3-b2ba-61a0bec721c0.skill-03`
- 高效操作：使用填充柄双击可自动识别旁边连续的请求数据并填至最后一行，避免逐行复制公式。
- 完成标志：`E2:E19` 均包含文字估算说明且没有空白；例如选中较低行的结果时，公式中的相对引用会变为该行的 `B`、`C`、`D` 单元格引用，而 `Rate Card` 范围保持固定。

#### 第 4 步：适度缩小工作表显示比例

1. 保持在 `Service Requests` 工作表，以便立即观察表格的可见范围。
2. 在窗口右下角状态栏找到缩放滑块。
3. 单击滑块的左侧或将滑块向左调整一次，使显示比例比初始默认比例略低。

- 对应 skills：`1334ca3e-f9e3-4db8-9ca7-b4c653be7d17.skill-01`
- 高效操作：直接在滑块上选择一个稍低的舒适比例，通常比反复点击缩小端更快，也更容易控制缩放幅度。
- 完成标志：状态栏显示的缩放比例低于开始时的比例，且屏幕上可同时看到更多行或列，同时仍能清楚选择单元格。

#### 第 5 步：完成最终内容与布局核验

1. 在 `Service Requests` 中抽查 `E2`、一个中间结果单元格以及 `E19`，确认它们都是文字结果并包含金额。
2. 选中其中一个非首行结果，确认其公式采用该行的 `B`、`C`、`D` 引用，并仍使用 `$'Rate Card'.$A$2:$B$7`。
3. 返回 `Overview`，确认横向标题仍只在 `B2:E2`，且 `A3:A6` 为空。

- 对应 skills：无；这是准备或检查步骤。
- 高效操作：最终只抽查首行、末行和一个中间行即可有效发现未填充、行引用错误或费率范围被移动等问题，无需逐格重做。
- 完成标志：服务请求的 18 条估算说明完整、审核标签仅保留为横向标题，且缩小后的显示比例仍处于生效状态。

#### 最终结果检查

- 在 `Overview` 中确认 `B2:E2` 依次为 `Rate verified`、`Adjustment reviewed`、`Estimate prepared`、`Ready to send`，而 `A3:A6` 已不再保留这些源标签。
- 切换到 `Service Requests`，确认 `E2:E19` 每一行都有文字形式的估算说明，没有空白单元格；选中任一结果单元格时，公式栏显示该行的服务代码、数量和调整率引用会随行号变化。
- 检查 `Rate Card` 的查找区域仍为 `A2:B7`，且其费率和 `Service Requests!A2:D19` 的原始输入均未被改动。
- 确认底部状态栏的缩放比例低于开始时的默认比例，并且当前视图能比开始时容纳更多工作表内容。

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
