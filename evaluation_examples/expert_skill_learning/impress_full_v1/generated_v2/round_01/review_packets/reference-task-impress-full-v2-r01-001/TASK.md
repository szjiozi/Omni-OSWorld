# Harbor Sampling Brief

- Reference task: `reference-task-impress-full-v2-r01-001`
- Application: `libreoffice_impress`
- Review decision: `pending`

## Task instruction

Refresh the “Harbor Sampling Brief” status slide as a field-ready monitoring card: set its slide background to the predefined Light Blue color, move the “Sampling window: 06:00–10:00” status label from the upper-right area to the lower-left area beneath the reading table, and make every character in that label underlined at 18 pt. Keep the table, trend graphic, and advisory badge in their current positions.

## Required skills

### 1. Reposition a text box by dragging

Skill ID: `15aece23-a215-4579-91b4-69eec72e18da.skill-01`

Procedure:

1. In the Slides pane, select the slide containing the text box.
2. Click the text box once to select its outer border rather than entering text-editing mode.
3. Drag the selected text box to the desired location on the slide; for example, drag a title text box downward toward the bottom edge.

Efficiency tip: Use a single click on the object border before dragging, then drag directly to the destination; avoid entering text-editing mode, which can select characters instead of moving the object.

Source task: `15aece23-a215-4579-91b4-69eec72e18da`

Source instruction: Move the title of page 2 to the bottom of the slide.

Directly referenced source actions:

- Action 0: <code>`CLICK` slide 2</code>
- Action 1: <code>`CLICK` Product Comparison text box</code>
- Action 2: <code>`DRAG_TO` bottom of the slide</code>

### 2. Underline all text in a selected text box

Skill ID: `4ed5abd0-8b5d-47bd-839f-cacfa15ca37a.skill-02`

Procedure:

1. After the text in a text box is selected in text-editing mode, click the Underline toolbar icon.
2. For example, select an entire title with Ctrl+A and click Underline once to apply underlining to every selected character.
3. Repeat for each additional text box that needs the same character formatting.

Efficiency tip: Apply underline while the text remains selected after other character formatting, so no extra text selection is required.

Source task: `4ed5abd0-8b5d-47bd-839f-cacfa15ca37a`

Source instruction: Set the color of titles in slides 2,3,5 as black and underline them.

Directly referenced source actions:

- Action 5: <code>`CLICK` underline icon</code>
- Action 11: <code>`CLICK` underline icon</code>
- Action 17: <code>`CLICK` underline icon</code>

### 3. Set the font size of text in a text box

Skill ID: `a434992a-89df-4577-925c-0c58b747f0f4.skill-02`

Procedure:

1. Click the text box containing the text to format.
2. Select the existing value in the font-size field, for example by triple-clicking it.
3. Type the desired point size, such as 12, and press Enter to apply it.

Efficiency tip: Replace the existing size value directly in the toolbar field instead of incrementing or decrementing the size repeatedly.

Source task: `a434992a-89df-4577-925c-0c58b747f0f4`

Source instruction: Change the font size of the content to 12, and change the font color to orange. Change the slide's background to red.

Directly referenced source actions:

- Action 4: <code>`CLICK` the content text box</code>
- Action 5: <code>`TRIPLE_CLICK` the font size text field</code>
- Action 6: <code>`TYPING` 12</code>
- Action 7: <code>`PRESS` enter</code>

### 4. Set a slide background to a predefined color

Skill ID: `70bca0cc-c117-427e-b0be-4df7299ebeb6.skill-02`

Procedure:

1. Select the target slide thumbnail so that formatting applies to the slide rather than an object on the canvas.
2. Open the slide Background menu, choose the background color option, and open its color palette.
3. Click the desired palette swatch. For example, choose a red swatch to make the entire slide background red.

Efficiency tip: Select the slide in the Slides pane before opening Background settings to avoid changing the fill color of a currently selected text box or shape.

Source task: `70bca0cc-c117-427e-b0be-4df7299ebeb6`

Source instruction: Make the background color of slide 2 same as the color of its title.

Directly referenced source actions:

- Action 3: <code>`CLICK` slide 2.</code>
- Action 4: <code>`CLICK` slide 2.</code>
- Action 5: <code>`CLICK` background menu.</code>
- Action 6: <code>`CLICK` color</code>
- Action 7: <code>`CLICK` color menu</code>
- Action 8: <code>`CLICK` red (2nd row, 5th from right)</code>

## Initial state preview

### contact-sheet

![contact-sheet.png](artifact/previews/contact-sheet.png)

### slide-01

![slide-01.png](artifact/previews/slide-01.png)

### slide-02

![slide-02.png](artifact/previews/slide-02.png)

## Operator guide

### Existing operation-intent guide

#### Demonstration 1

- Skill: `15aece23-a215-4579-91b4-69eec72e18da.skill-01`
- Intent: Relocate the sampling-window status text box from the upper-right portion of slide 2 to the designated open lower-left area beneath the table.
- Efficiency: Select the text box border once, then drag the object rather than entering text-editing mode.
- Visible success: The entire “Sampling window: 06:00–10:00” text box appears below the table on the lower-left, while the table and chart have not moved.

#### Demonstration 2

- Skill: `4ed5abd0-8b5d-47bd-839f-cacfa15ca37a.skill-02`
- Intent: Apply underline formatting to every character in the sampling-window status label.
- Efficiency: Select all text in the label before applying Underline so the whole label is formatted in one action.
- Visible success: Both the “Sampling window:” text and the “06:00–10:00” time range have a continuous underline.

#### Demonstration 3

- Skill: `a434992a-89df-4577-925c-0c58b747f0f4.skill-02`
- Intent: Change the sampling-window status label to 18 pt.
- Efficiency: Replace the font-size value directly in the toolbar field rather than stepping through size increments.
- Visible success: The status label is visibly larger than its initial 14 pt appearance and displays as 18 pt when its text is selected.

#### Demonstration 4

- Skill: `70bca0cc-c117-427e-b0be-4df7299ebeb6.skill-02`
- Intent: Apply the predefined Light Blue color to slide 2’s background.
- Efficiency: Select the slide thumbnail before opening Background settings so the color applies to the slide rather than a selected object.
- Visible success: The full slide canvas behind all slide 2 objects is Light Blue, with the objects retaining their own fills and positions.

Recording start: Open the supplied two-slide presentation with slide 2 selected; all requested changes are intentionally incomplete.

Recording end: Slide 2 has a predefined Light Blue background, and its sampling-window label is positioned beneath the table at lower-left, fully underlined, and 18 pt.

Allowed variation: The exact drag path and the sequence used for text formatting may vary, provided the specified final placement, 18 pt size, full underline, and predefined Light Blue slide background are visible.

### 中文详细参考方案

> 以下是一个可以参考的操作 guide。标注者可以根据实际 LibreOffice 界面采用等价操作。

本指南将第 2 张状态页整理为现场可用的监测卡：把整张幻灯片背景改为预定义 `Light Blue`，将“Sampling window: 06:00–10:00”标签移动到读数表下方的左下区域，并把该标签的全部字符设为 18 pt 且带下划线。只编辑该标签和第 2 张的幻灯片背景；读数表、趋势图、提示徽章、来源说明及第 1 张内容均不应改变。

#### 启动后的初始状态检查

- 确认以 Normal 视图打开的是两张幻灯片的演示文稿，且 Slides 窗格中的第 2 张缩略图处于选中状态。若当前不是第 2 张，单击第 2 张缩略图；这是选择幻灯片，不是选择画布上的对象。
- 查看第 2 张：画布背景初始可见为白色；右上区域有可编辑文字“Sampling window: 06:00–10:00”；`station_readings_table` 位于左侧，表格正下方的左下区域留有空位。
- 确认 `station_readings_table`、`turbidity_trend_chart`、`advisory_badge` 和 `source_caption` 已经存在。它们的位置是可接受的，无需调整；如果误选了其中任一对象，按 `Esc` 取消对象选择，再继续操作。
- 初始标签显示为较小的无下划线文本是正常的；后续会将其统一设为 18 pt 并为每个字符加下划线。

#### 第 1 步：将第 2 张幻灯片背景设为 Light Blue

1. 先单击 Slides 窗格中的第 2 张缩略图，使修改目标明确为整张幻灯片，而不是画布上某个文本框或形状。若画布中仍有对象的选择边框，单击第 2 张缩略图后再确认该边框已消失。
2. 打开 `Slide` > `Properties...`，在打开的属性窗口中选择 `Background` 选项卡。将背景填充类型设为 `Color`，然后在颜色选择控件中选择预定义颜色 `Light Blue`，并用 `OK` 应用。
3. 整张画布在所有对象背后呈 `Light Blue` 即为正确，无需再修改背景。若仍是白色，重新确认选中的是第 2 张缩略图而非文本框，然后再次通过 `Slide` > `Properties...` 的 `Background` 选择 `Light Blue`。若只有一个对象变蓝，撤销该对象填充更改或恢复其原填充，并按上述方式从幻灯片缩略图重新设置背景。

- 对应 skills：`70bca0cc-c117-427e-b0be-4df7299ebeb6.skill-02`
- 高效操作：先从 Slides 窗格选中缩略图再打开 `Slide` > `Properties...`，可避免把颜色误应用到当前对象。
- 完成标志：第 2 张的整个背景画布均为 `Light Blue`，而表格、图表、徽章和文字对象本身的填充与位置没有变化。

#### 第 2 步：按对象边框选择并移动 sampling-window 标签

1. 在第 2 张画布右上方找到“Sampling window: 06:00–10:00”。单击其文本框的外边框一次，使文本框出现对象选择边框和控制点。此处是选择对象边框，不是进入文字编辑；若看到闪烁的文字插入光标或选中了字符，按 `Esc`，再单击外边框。
2. 拖动已选中的完整文本框到 `station_readings_table` 正下方的左下空白区域。以标签整体位于表格下方、左侧对齐区域为准，避免覆盖表格、趋势图、来源说明或提示徽章。
3. 标签完全位于读数表下方的左下区域即为可接受的近似位置，无需为了像素级位置反复微调。若标签仍在右上方、压住表格，或与其他对象重叠，先单击标签外边框重新选中该对象，再将整个边框拖到表格正下方的开放区域；不要拖动表格或图表。

- 对应 skills：`15aece23-a215-4579-91b4-69eec72e18da.skill-01`
- 高效操作：一次选中外边框后直接拖动整个对象；这样不会选中或改写标签中的文字。
- 完成标志：“Sampling window: 06:00–10:00”完整地显示在读数表下方的左下区域，表格和趋势图仍在原位置。

#### 第 3 步：进入标签的文字编辑模式并选中全部文字

1. 双击已移到左下方的标签文本框内部，进入文字编辑模式。与上一步的对象选择不同，此时应能看到文本插入光标，且工具栏中的文字格式控件可作用于字符。
2. 按 `Ctrl+A`，选中该文本框内的全部“Sampling window: 06:00–10:00”文字。确认高亮范围同时覆盖“Sampling window:”和“06:00–10:00”，而不是只覆盖其中一段。
3. 若 `Ctrl+A` 选中了幻灯片上的多个对象而非标签中的字符，按 `Esc`，双击标签文字内部以重新进入文字编辑模式，然后再次按 `Ctrl+A`。

- 对应 skills：无；这是准备或检查步骤。
- 高效操作：在同一次全选状态下连续完成字号和下划线设置，避免再次选取文字。
- 完成标志：标签中的整行文本处于字符高亮选中状态，且没有其他画布对象显示选择控制点。

#### 第 4 步：把标签全部文字改为 18 pt

1. 保持标签全部文字处于选中状态，在顶部格式工具栏的字体大小框中选中当前数值，输入 `18`，然后按 `Enter`。字体大小框通常显示当前所选文字的点数。
2. 文字变得比初始 14 pt 更大，且在文字仍被选中时字体大小框显示 `18`，即为正确，无需继续增减。若大小框没有显示 `18`、或只有部分文字变大，重新在文字编辑模式中按 `Ctrl+A` 选中整行，再输入 `18` 并按 `Enter`。

- 对应 skills：`a434992a-89df-4577-925c-0c58b747f0f4.skill-02`
- 高效操作：直接替换字体大小框中的数值，比反复点击增大字号按钮更快且更准确。
- 完成标志：整条“Sampling window: 06:00–10:00”均以 18 pt 显示，且仍处于可继续应用字符格式的全选状态。

#### 第 5 步：为标签的每个字符应用下划线

1. 继续保持整条标签文字被选中，单击格式工具栏中的 `Underline`。不要在未选中文字时单击，以免只影响后续新输入的字符。
2. “Sampling window:”和“06:00–10:00”下方都出现连续下划线即为正确，无需重复点击。若只看到部分文字有下划线，或下划线被关闭，进入该文本框的文字编辑模式，按 `Ctrl+A` 选中全部文字后再单击一次 `Underline`，直到整行都带下划线。
3. 单击画布空白处退出文字编辑模式，以便检查最终外观；这不会改变已应用的 18 pt 和下划线格式。

- 对应 skills：`4ed5abd0-8b5d-47bd-839f-cacfa15ca37a.skill-02`
- 高效操作：字号设置完成后不取消文字选择，立即点击 `Underline`，即可一次格式化整条标签。
- 完成标志：在非编辑状态下，左下方标签的全部字符均为 18 pt 且可见下划线，包括冒号后的完整时间范围。

#### 最终结果检查

- 检查 Slides 窗格：第 1 张仍是原有封面缩略图，第 2 张仍是状态页；没有新增、删除、复制或重排幻灯片。
- 检查第 2 张：整张对象背后的背景为预定义 `Light Blue`，不是白色，也不是仅某个文本框变成蓝色。
- 检查“Sampling window: 06:00–10:00”：它位于 `station_readings_table` 下方的左下开放区域；整条文字均带下划线。双击文字、按 `Ctrl+A` 后，字体大小框应显示 `18`。完成检查后按 `Esc` 或单击空白处退出编辑模式。
- 检查未改动内容：`station_readings_table`、`turbidity_trend_chart`、`advisory_badge` 和 `source_caption` 仍在原位置，未被标签遮挡；第 1 张的标题、字幕、水波段和日期标签保持不变。

## Source-task similarity review

| Measure | Maximum | Most similar source task |
| --- | ---: | --- |
| Lexical sequence similarity | 0.290598 | 05dd4c1d-c489-4c85-8389-a7836c4f0567 |
| Semantic cosine similarity | 0.523926 | 04578141-1d42-4146-b9cf-6fab4ce5fd74 |

Similarity scores are reviewer aids, not automatic acceptance thresholds. Inspect the contributing source tasks and their complete ordered actions below.

### Source task `15aece23-a215-4579-91b4-69eec72e18da`

Original instruction:

> Move the title of page 2 to the bottom of the slide.

Required skills derived from this source task:

- **Reposition a text box by dragging** — `15aece23-a215-4579-91b4-69eec72e18da.skill-01`

Complete ordered single-action sequence:

| Action | Related required skill | Original single action |
| ---: | --- | --- |
| 0 | <strong>★ Reposition a text box by dragging</strong><br><code>15aece23-a215-4579-91b4-69eec72e18da.skill-01</code> | <strong><code>`CLICK` slide 2</code></strong> |
| 1 | <strong>★ Reposition a text box by dragging</strong><br><code>15aece23-a215-4579-91b4-69eec72e18da.skill-01</code> | <strong><code>`CLICK` Product Comparison text box</code></strong> |
| 2 | <strong>★ Reposition a text box by dragging</strong><br><code>15aece23-a215-4579-91b4-69eec72e18da.skill-01</code> | <strong><code>`DRAG_TO` bottom of the slide</code></strong> |

### Source task `4ed5abd0-8b5d-47bd-839f-cacfa15ca37a`

Original instruction:

> Set the color of titles in slides 2,3,5 as black and underline them.

Required skills derived from this source task:

- **Underline all text in a selected text box** — `4ed5abd0-8b5d-47bd-839f-cacfa15ca37a.skill-02`

Complete ordered single-action sequence:

| Action | Related required skill | Original single action |
| ---: | --- | --- |
| 0 |  | <code>`CLICK` Slide 2.</code> |
| 1 |  | <code>`CLICK` the title text box</code> |
| 2 |  | <code>`HOTKEY` ctrl-A</code> |
| 3 |  | <code>`CLICK` font color dropdown.</code> |
| 4 |  | <code>`CLICK` black</code> |
| 5 | <strong>★ Underline all text in a selected text box</strong><br><code>4ed5abd0-8b5d-47bd-839f-cacfa15ca37a.skill-02</code> | <strong><code>`CLICK` underline icon</code></strong> |
| 6 |  | <code>`CLICK` Slide 3.</code> |
| 7 |  | <code>`CLICK` the title text box</code> |
| 8 |  | <code>`HOTKEY` ctrl-A</code> |
| 9 |  | <code>`CLICK` font color dropdown.</code> |
| 10 |  | <code>`CLICK` black</code> |
| 11 | <strong>★ Underline all text in a selected text box</strong><br><code>4ed5abd0-8b5d-47bd-839f-cacfa15ca37a.skill-02</code> | <strong><code>`CLICK` underline icon</code></strong> |
| 12 |  | <code>`CLICK` Slide 5.</code> |
| 13 |  | <code>`CLICK` the title text box</code> |
| 14 |  | <code>`HOTKEY` ctrl-A</code> |
| 15 |  | <code>`CLICK` font color dropdown.</code> |
| 16 |  | <code>`CLICK` black</code> |
| 17 | <strong>★ Underline all text in a selected text box</strong><br><code>4ed5abd0-8b5d-47bd-839f-cacfa15ca37a.skill-02</code> | <strong><code>`CLICK` underline icon</code></strong> |

### Source task `70bca0cc-c117-427e-b0be-4df7299ebeb6`

Original instruction:

> Make the background color of slide 2 same as the color of its title.

Required skills derived from this source task:

- **Set a slide background to a predefined color** — `70bca0cc-c117-427e-b0be-4df7299ebeb6.skill-02`

Complete ordered single-action sequence:

| Action | Related required skill | Original single action |
| ---: | --- | --- |
| 0 |  | <code>`CLICK` slide 2</code> |
| 1 |  | <code>`CLICK &#x27;Our customers love us&#x27; text box</code> |
| 2 |  | <code>`CLICK` font color dropdown</code> |
| 3 | <strong>★ Set a slide background to a predefined color</strong><br><code>70bca0cc-c117-427e-b0be-4df7299ebeb6.skill-02</code> | <strong><code>`CLICK` slide 2.</code></strong> |
| 4 | <strong>★ Set a slide background to a predefined color</strong><br><code>70bca0cc-c117-427e-b0be-4df7299ebeb6.skill-02</code> | <strong><code>`CLICK` slide 2.</code></strong> |
| 5 | <strong>★ Set a slide background to a predefined color</strong><br><code>70bca0cc-c117-427e-b0be-4df7299ebeb6.skill-02</code> | <strong><code>`CLICK` background menu.</code></strong> |
| 6 | <strong>★ Set a slide background to a predefined color</strong><br><code>70bca0cc-c117-427e-b0be-4df7299ebeb6.skill-02</code> | <strong><code>`CLICK` color</code></strong> |
| 7 | <strong>★ Set a slide background to a predefined color</strong><br><code>70bca0cc-c117-427e-b0be-4df7299ebeb6.skill-02</code> | <strong><code>`CLICK` color menu</code></strong> |
| 8 | <strong>★ Set a slide background to a predefined color</strong><br><code>70bca0cc-c117-427e-b0be-4df7299ebeb6.skill-02</code> | <strong><code>`CLICK` red (2nd row, 5th from right)</code></strong> |

### Source task `a434992a-89df-4577-925c-0c58b747f0f4`

Original instruction:

> Change the font size of the content to 12, and change the font color to orange. Change the slide's background to red.

Required skills derived from this source task:

- **Set the font size of text in a text box** — `a434992a-89df-4577-925c-0c58b747f0f4.skill-02`

Complete ordered single-action sequence:

| Action | Related required skill | Original single action |
| ---: | --- | --- |
| 0 |  | <code>`CLICK` background dropdown arrow</code> |
| 1 |  | <code>`CLICK` color</code> |
| 2 |  | <code>`CLICK` color dropdown arrow</code> |
| 3 |  | <code>`CLICK` red (2nd row, 5th from left)</code> |
| 4 | <strong>★ Set the font size of text in a text box</strong><br><code>a434992a-89df-4577-925c-0c58b747f0f4.skill-02</code> | <strong><code>`CLICK` the content text box</code></strong> |
| 5 | <strong>★ Set the font size of text in a text box</strong><br><code>a434992a-89df-4577-925c-0c58b747f0f4.skill-02</code> | <strong><code>`TRIPLE_CLICK` the font size text field</code></strong> |
| 6 | <strong>★ Set the font size of text in a text box</strong><br><code>a434992a-89df-4577-925c-0c58b747f0f4.skill-02</code> | <strong><code>`TYPING` 12</code></strong> |
| 7 | <strong>★ Set the font size of text in a text box</strong><br><code>a434992a-89df-4577-925c-0c58b747f0f4.skill-02</code> | <strong><code>`PRESS` enter</code></strong> |
| 8 |  | <code>`CLICK` the font color dropdown arrow</code> |
| 9 |  | <code>`CLICK` the orange color (2nd row, 3rd from left)</code> |

## Review this package

Before choosing a decision, complete all three checks:

- [ ] **Task naturalness and skill necessity:** Is the reference task a natural Impress task, and is every listed required skill genuinely necessary and observable when solving it?
- [ ] **Initial artifact correctness:** Launch the environment and confirm that the presentation opens correctly, contains the content needed by the instruction, and has not already completed the requested results.
- [ ] **Source-task similarity:** Compare the reference task with the source instructions and complete single-action sequences above. Confirm that it is not merely an entity, field, or value substitution and does not reproduce a source task's complete ordered solution.

Use `approved` when all checks pass. Use `revision_requested` when the package is fixable and provide concrete revision instructions. Use `rejected` when the combination is fundamentally unnatural, infeasible, or too similar to a source task.

Fill [review.json](review.json), then collect completed forms from the repository root:

```bash
python scripts/python/manage_reference_review_packets.py collect \
  --skill-pool evaluation_examples/expert_skill_learning/impress_full_v1/generated_v2/skill_pool.json \
  --packages evaluation_examples/expert_skill_learning/impress_full_v1/generated_v2/round_01/reference_packages.json \
  --source-tasks evaluation_examples/expert_skill_learning/impress_full_v1/source_tasks.json \
  --reviews evaluation_examples/expert_skill_learning/impress_full_v1/generated_v2/round_01/reference_package_reviews.json \
  --artifact-manifest evaluation_examples/expert_skill_learning/impress_full_v1/generated_v2/round_01/artifacts/artifact_manifest.json \
  --task-config-manifest evaluation_examples/expert_skill_learning/impress_full_v1/generated_v2/round_01/task_config_manifest.json \
  --task-detail-root evaluation_examples/expert_skill_learning/impress_full_v1/generated_v2/round_01/task_details \
  --reviewer-guides evaluation_examples/expert_skill_learning/impress_full_v1/generated_v2/round_01/reviewer_guides.json \
  --coverage evaluation_examples/expert_skill_learning/impress_full_v1/generated_v2/round_01/coverage_state.json \
  --packet-root evaluation_examples/expert_skill_learning/impress_full_v1/generated_v2/round_01/review_packets
```

Detailed field guidance is in [`reviewer.md`](../../../../../reviewer.md).
