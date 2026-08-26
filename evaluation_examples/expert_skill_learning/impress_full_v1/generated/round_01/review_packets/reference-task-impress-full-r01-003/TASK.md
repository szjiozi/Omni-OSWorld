# Riverside Pollinator Walk

- Reference task: `reference-task-impress-full-r01-003`
- Application: `libreoffice_impress`
- Review decision: `pending`

## Task instruction

Update the “Riverside Pollinator Walk” field-brief deck for the volunteer check-in. On slide 2, set the small teal section label “FIELD SNAPSHOT” to 18 pt and set each of the three metric captions (“Nesting sites mapped”, “Late-season blooms”, and “Volunteer pairs”) to 22 pt. Resize the bee-and-wildflower illustration to exactly 6.5 cm high, then move it into the open upper-right area of the slide, above the metric cards and to the right of the summary text. Keep all wording, colors, and other objects unchanged.

## Required skills

### 1. Change text font size in a text box

Skill ID: `a434992a-89df-4577-925c-0c58b747f0f4.skill-02`

Procedure:

1. Select the text box, then select the text whose size should change; clicking a text box is distinct from entering text-editing mode when only part of its text is to be formatted.
2. Select the current value in the font-size field, type the desired point size, such as 12, and press Enter to apply it.

Efficiency tip: Use the font-size field to enter an exact point value instead of repeatedly clicking increase or decrease font-size buttons.

Source task: `a434992a-89df-4577-925c-0c58b747f0f4`

Source instruction: Change the font size of the content to 12, and change the font color to orange. Change the slide's background to red.

Directly referenced source actions:

- Action 4: <code>`CLICK` the content text box</code>
- Action 5: <code>`TRIPLE_CLICK` the font size text field</code>
- Action 6: <code>`TYPING` 12</code>
- Action 7: <code>`PRESS` enter</code>

### 2. Set font size for text in multiple text boxes

Skill ID: `e4ef0baf-4b52-4590-a47e-d4d464cca2d7.skill-02`

Procedure:

1. For each text box, enter text-editing mode and select the text whose size should change. Selecting text inside the shape is different from selecting the shape object itself.
2. Activate the Font Size box on the formatting toolbar, replace its value with the desired point size, for example `40 pt`, and press Enter.
3. Repeat for the remaining independently formatted text boxes on the slide.

Efficiency tip: After applying a size, move directly to the next text box and use the Font Size box again; this avoids opening character-format dialogs for each text box.

Source task: `e4ef0baf-4b52-4590-a47e-d4d464cca2d7`

Source instruction: The height of picture should be 20cm on slide 3 while the font size of all textboxes should be 40pt on slide 6.

Directly referenced source actions:

- Action 8: <code>`TRIPLE_CLICK` text in &#x27;our founder&#x27;.</code>
- Action 9: <code>`TRIPLE_CLICK` font size dropdown</code>
- Action 10: <code>`TYPING` 40pt</code>
- Action 11: <code>`PRESS` enter</code>
- Action 12: <code>`TRIPLE_CLICK` text in &#x27;name surname&#x27;.</code>
- Action 13: <code>`TRIPLE_CLICK` font size dropdown</code>
- Action 14: <code>`TYPING` 40pt</code>
- Action 15: <code>`PRESS` enter</code>
- Action 16: <code>`TRIPLE_CLICK` text in &#x27;presentations are...&#x27;.</code>
- Action 17: <code>`TRIPLE_CLICK` font size dropdown</code>
- Action 18: <code>`TYPING` 40pt</code>
- Action 19: <code>`PRESS` enter</code>

### 3. Set an image's exact height

Skill ID: `7ae48c60-f143-4119-b659-15b8f485eb9a.skill-01`

Procedure:

1. Select the image as an object on the slide; do not enter text-editing mode.
2. Open the image's Position and Size controls if the Height field is not already visible, for example through the Properties sidebar's Position and Size section.
3. Select the entire current value in the Height field, type a measurement with a unit such as `20 cm`, and press Enter to apply the new height.

Efficiency tip: Keep the Properties sidebar open while resizing several images; after selecting each image, replace the Height value directly rather than reopening the full formatting dialog.

Source task: `7ae48c60-f143-4119-b659-15b8f485eb9a`

Source instruction: Change picture's height to 20, 30, 25cm on slide 3, 4, 6 respectively.

Directly referenced source actions:

- Action 1: <code>`CLICK` photo on the right</code>
- Action 2: <code>`SCROLL` down to height text box</code>
- Action 3: <code>`TRIPLE_CLICK` height text box</code>
- Action 4: <code>`TYPING` 20cm</code>
- Action 5: <code>`PRESS` enter</code>
- Action 7: <code>`CLICK` photo on the right</code>
- Action 8: <code>`CLICK` position and size dropdown</code>
- Action 9: <code>`TRIPLE_CLICK` height text box</code>
- Action 10: <code>`TYPING` 30cm</code>
- Action 11: <code>`PRESS` enter</code>
- Action 13: <code>`CLICK` photo</code>
- Action 14: <code>`TRIPLE_CLICK` height text box</code>
- Action 15: <code>`TYPING` 25cm</code>
- Action 16: <code>`PRESS` enter</code>

### 4. Reposition an image by dragging

Skill ID: `ed43c15f-00cb-4054-9c95-62c880865d68.skill-02`

Procedure:

1. Click the image once to select the image object and show its selection handles.
2. Drag the selected image from inside its bounds to the desired location on the slide, then release the mouse button.
3. Avoid dragging a resize handle, which changes the image size instead of its position.

Efficiency tip: Drag from the image interior rather than from an edge or handle to move it cleanly without resizing or cropping.

Source task: `ed43c15f-00cb-4054-9c95-62c880865d68`

Source instruction: Move the picture on page 2 to slide top. Make textboxes underlined on slide 1 and 2.

Directly referenced source actions:

- Action 5: <code>`CLICK` image</code>
- Action 6: <code>`DRAG_TO` top of slide</code>

## Initial state preview

### contact-sheet

![contact-sheet.png](artifact/previews/contact-sheet.png)

### slide-01

![slide-01.png](artifact/previews/slide-01.png)

### slide-02

![slide-02.png](artifact/previews/slide-02.png)

### slide-03

![slide-03.png](artifact/previews/slide-03.png)

## Operator guide

### Existing operation-intent guide

#### Demonstration 1

- Skill: `a434992a-89df-4577-925c-0c58b747f0f4.skill-02`
- Intent: Set the separate “FIELD SNAPSHOT” text box to exactly 18 pt.
- Efficiency: Enter text-editing mode in the label and type the exact value in the Font Size field rather than using incremental size controls.
- Visible success: The teal section label remains unchanged in wording and color but displays visibly larger at 18 pt.

#### Demonstration 2

- Skill: `e4ef0baf-4b52-4590-a47e-d4d464cca2d7.skill-02`
- Intent: Set the “Nesting sites mapped”, “Late-season blooms”, and “Volunteer pairs” metric-caption text boxes to exactly 22 pt.
- Efficiency: Select the three caption text boxes together when practical, then enter 22 pt once in the Font Size field; otherwise update each independent caption box in sequence.
- Visible success: All three targeted captions display at the same 22 pt size while their associated metric values remain unchanged.

#### Demonstration 3

- Skill: `7ae48c60-f143-4119-b659-15b8f485eb9a.skill-01`
- Intent: Set the bee-and-wildflower image to an exact height of 6.5 cm.
- Efficiency: Use the image Position and Size controls and replace the height measurement directly.
- Visible success: The selected image reports a height of 6.5 cm and retains its original proportions.

#### Demonstration 4

- Skill: `ed43c15f-00cb-4054-9c95-62c880865d68.skill-02`
- Intent: Relocate the resized bee-and-wildflower image into the empty upper-right region above the metric cards.
- Efficiency: Drag from the image interior, not a selection handle, to avoid changing its size while positioning it.
- Visible success: The image sits to the right of the summary copy and above the card row without covering text or cards.

Recording start: Open the supplied three-slide deck with slide 2 visible in normal editing view.

Recording end: Slide 2 shows the requested 18 pt label, all three 22 pt metric captions, and the 6.5 cm-high illustration placed in the upper-right.

Allowed variation: Minor final placement variation is acceptable provided the image is clearly in the open upper-right region, above the metric cards, to the right of the summary text, and no overlap occurs.

### 中文详细参考方案

> 以下是一个可以参考的操作 guide。标注者可以根据实际 LibreOffice 界面采用等价操作。

本指南只编辑第 2 张 “Riverside Pollinator Walk” 数据概览页：将 “FIELD SNAPSHOT” 调为 18 pt，将三个独立指标说明调为 22 pt，并把蜜蜂与野花插图等比设为 6.5 cm 高后移到右上方空白区。不要修改任何文字内容、颜色、字体名称、指标数值、卡片或第 1、3 张幻灯片。

#### 启动后的初始状态检查

- 确认演示文稿处于普通编辑视图，左侧缩略图窗格可见 3 张幻灯片；单击第 2 张缩略图以选中幻灯片，而不是在缩略图窗格中拖动它。
- 在第 2 张中确认可见独立文本对象 “FIELD SNAPSHOT”、“Nesting sites mapped”、“Late-season blooms” 和 “Volunteer pairs”；三个说明文字各自位于下方指标卡中，并与较大的指标数值分离。
- 确认蜜蜂与野花插图是可选中的图像对象：单击图像边缘/内部一次应出现矩形选择边框和控制点。它初始较小且不在最终右上目标位置；不要选择或移动指标卡。
- 可接受的初始状态是右上方、指标卡行上方且摘要文字右侧存在明显空白区域。若该区域被其他临时选中对象的边框遮挡，先单击幻灯片空白处取消选择，再辨认该空白目的地。

#### 第 1 步：将 “FIELD SNAPSHOT” 设置为 18 pt

1. 保持第 2 张缩略图被选中。在幻灯片上单击 “FIELD SNAPSHOT” 文本框的边框，使其作为对象被选中；这一步只会显示对象边框，尚未进入文字编辑。
2. 再次双击该文本框内部以进入文字编辑模式，然后用 `Ctrl+A` 仅选中此文本框中的 “FIELD SNAPSHOT” 字符。不要在幻灯片空白处使用 `Ctrl+A`，否则会选中整页对象。
3. 在格式工具栏的 `Font Size` 框中选中原数值，输入 `18 pt` 并按 `Enter`。随后单击文本框外的幻灯片空白处，退出文字编辑并查看结果。
4. 若该标签已经显示为 18 pt、文字仍为 “FIELD SNAPSHOT” 且仍是原来的 teal 颜色，则无需再调整；如果字号未改变，重新进入该文本框的文字编辑模式，确认高亮的是文本字符而不是对象边框，再在 `Font Size` 中输入 `18 pt`。

- 对应 skills：`a434992a-89df-4577-925c-0c58b747f0f4.skill-02`
- 高效操作：直接在 `Font Size` 中输入精确值，比反复使用增大/减小字号按钮更快，也不会误设为相邻字号。
- 完成标志：“FIELD SNAPSHOT” 的措辞和 teal 颜色不变，但视觉上比原来更大；重新选中文本时，`Font Size` 显示 `18 pt`。

#### 第 2 步：同时将三个指标说明设置为 22 pt

1. 先单击 “Nesting sites mapped” 文本框的边框，确认选中的是整个说明文本对象而非卡片形状或大号指标数值。按住 `Shift`，依次单击 “Late-season blooms” 和 “Volunteer pairs” 各自文本框的边框。三者都应显示选择边框；不要把任何 metric card 或 metric value 加入选择。
2. 在三个文本框对象同时选中的状态下，使用工具栏的 `Font Size`，替换数值为 `22 pt`，然后按 `Enter`。这会对这三个独立文本框的全部文字应用相同字号。
3. 单击幻灯片空白处取消多选，逐一目视检查三个卡片说明。若其中某个说明因难以精确多选而没有变为 22 pt，双击该说明文字进入文字编辑，用 `Ctrl+A` 选中该文本框内部文字，在 `Font Size` 输入 `22 pt` 并按 `Enter`；仅修复未正确设置的说明。
4. 若三个说明已同为 22 pt、对应的大号数值仍保持原大小，则无需进一步调整；如果大号数值也意外改变，立即选择该数值所在的独立文本框，恢复其原有字号，而不要修改说明文字或卡片的位置。

- 对应 skills：`e4ef0baf-4b52-4590-a47e-d4d464cca2d7.skill-02`
- 高效操作：通过 `Shift` 选择三个文本框边框后只设置一次 `Font Size`，可避免对三个相同格式对象重复操作；选中边框与双击进入文字编辑是不同状态。
- 完成标志：“Nesting sites mapped”、“Late-season blooms” 和 “Volunteer pairs” 三条说明显示为一致且更大的 22 pt；三个大号指标数值、卡片颜色及位置均未改变。

#### 第 3 步：把蜜蜂与野花图像的高度精确设为 6.5 cm

1. 单击蜜蜂与野花插图一次，选择图像对象并显示其矩形边框和控制点；不要双击图像，也不要进入任何文字编辑状态。
2. 选择 `Format` > `Position and Size...` 打开 `Position and Size` 对话框。找到 `Height` 字段；如有 `Keep ratio` 选项，检查它已启用，以便只改高度时保持原始纵横比。
3. 选中 `Height` 的完整当前值，输入 `6.5 cm`，然后按 `Enter` 或确认对话框中的 `OK` 以应用。不要更改 `Width`，不要使用裁剪控制，也不要替换图像。
4. 若图像高度已显示为 `6.5 cm` 且图像比例自然、没有被拉伸，则无需再调整；如果图像看起来变形或 `Keep ratio` 未启用，启用 `Keep ratio` 后再次在 `Height` 输入 `6.5 cm` 并确认。

- 对应 skills：`7ae48c60-f143-4119-b659-15b8f485eb9a.skill-01`
- 高效操作：使用 `Position and Size...` 的 `Height` 字段输入带单位的精确值，避免拖动控制点造成近似尺寸或意外改变宽度。
- 完成标志：选中插图时可在 `Position and Size` 中读到 `Height` 为 `6.5 cm`；图像仍保持原有蜜蜂与野花内容和正常比例。

#### 第 4 步：将已缩放插图拖到右上方开放区域

1. 保持插图作为对象被选中。将指针放在图像内部、远离边缘和八个控制点的位置，按住鼠标拖动到第 2 张幻灯片右上方的空白区域后释放。目标是位于摘要文字右侧、指标卡行上方。
2. 拖放后检查图像不遮挡 “FIELD SNAPSHOT”、标题、摘要文字，以及任何指标卡、指标数值或说明文字。图像应完全处于上半区域，并与下方卡片行留出可见间隔。
3. 可接受的结果是插图清楚地处于右上空白区、摘要文字右侧且卡片行上方，轻微横向或纵向位置差不需要调整。若图像仍在摘要文字下方、覆盖文字/卡片，或其下边缘进入卡片行，重新从图像内部拖到更靠右或更靠上的空白处；不要拖动控制点。
4. 若拖动时尺寸意外变化，撤销该次操作或重新按第 3 步将 `Height` 设回 `6.5 cm`，再从图像内部进行移动。

- 对应 skills：`ed43c15f-00cb-4054-9c95-62c880865d68.skill-02`
- 高效操作：拖动图像内部而非选择边框或控制点，可仅改变位置，不会触发缩放或裁剪。
- 完成标志：蜜蜂与野花插图位于第 2 张的开放右上区域，明显在指标卡行上方、摘要文字右侧，且没有覆盖任何文本或卡片。

#### 第 5 步：在第 2 张完成局部复核并保存

1. 单击幻灯片空白处取消所有对象选择，以无边框状态检查最终版面。确认 “FIELD SNAPSHOT” 是 18 pt，三个说明均为 22 pt，文字内容和颜色均未改动。
2. 再次单击插图的边框并通过 `Format` > `Position and Size...` 复核 `Height` 为 `6.5 cm`；确认后关闭对话框并取消选择。
3. 使用 `Ctrl+S` 保存演示文稿。

- 对应 skills：无；这是准备或检查步骤。
- 高效操作：在无选择边框的状态下复核，最容易发现图像是否压住文字或卡片；仅在需要读精确高度时再选中图像。
- 完成标志：第 2 张呈现整洁的右上插图与下方三张指标卡布局，且保存操作完成后没有出现未保存修改提示。

#### 最终结果检查

- 检查左侧缩略图顺序仍为原来的第 1、2、3 张；第 2 张仍是数据概览页，没有新增、删除或重排幻灯片。
- 在第 2 张确认仅发生以下编辑：`FIELD SNAPSHOT` 为 18 pt；“Nesting sites mapped”、“Late-season blooms” 和 “Volunteer pairs” 均为 22 pt；原有蜜蜂与野花图像为 6.5 cm 高且在右上空白区。
- 确认第 2 张的标题、摘要文字、三个指标数值、三张 metric card、全部文字措辞、颜色和字体名称均保持不变；没有其他对象被移动。
- 单击第 1 张和第 3 张缩略图进行目视检查：两张幻灯片的标题、图像、形状和文本均与编辑前一致。最后可返回第 2 张，确认最终展示页仍符合版面要求。

## Source-task similarity review

| Measure | Maximum | Most similar source task |
| --- | ---: | --- |
| Lexical sequence similarity | 0.264662 | a53f80cd-4a90-4490-8310-097b011433f6 |
| Semantic cosine similarity | 0.461807 | 8979838c-54a5-4454-a2b8-3d135a1a5c8f |

Similarity scores are reviewer aids, not automatic acceptance thresholds. Inspect the contributing source tasks and their complete ordered actions below.

### Source task `7ae48c60-f143-4119-b659-15b8f485eb9a`

Original instruction:

> Change picture's height to 20, 30, 25cm on slide 3, 4, 6 respectively.

Required skills derived from this source task:

- **Set an image's exact height** — `7ae48c60-f143-4119-b659-15b8f485eb9a.skill-01`

Complete ordered single-action sequence:

| Action | Related required skill | Original single action |
| ---: | --- | --- |
| 0 |  | <code>`CLICK` slide 3</code> |
| 1 | <strong>★ Set an image&#x27;s exact height</strong><br><code>7ae48c60-f143-4119-b659-15b8f485eb9a.skill-01</code> | <strong><code>`CLICK` photo on the right</code></strong> |
| 2 | <strong>★ Set an image&#x27;s exact height</strong><br><code>7ae48c60-f143-4119-b659-15b8f485eb9a.skill-01</code> | <strong><code>`SCROLL` down to height text box</code></strong> |
| 3 | <strong>★ Set an image&#x27;s exact height</strong><br><code>7ae48c60-f143-4119-b659-15b8f485eb9a.skill-01</code> | <strong><code>`TRIPLE_CLICK` height text box</code></strong> |
| 4 | <strong>★ Set an image&#x27;s exact height</strong><br><code>7ae48c60-f143-4119-b659-15b8f485eb9a.skill-01</code> | <strong><code>`TYPING` 20cm</code></strong> |
| 5 | <strong>★ Set an image&#x27;s exact height</strong><br><code>7ae48c60-f143-4119-b659-15b8f485eb9a.skill-01</code> | <strong><code>`PRESS` enter</code></strong> |
| 6 |  | <code>`CLICK` slide 4</code> |
| 7 | <strong>★ Set an image&#x27;s exact height</strong><br><code>7ae48c60-f143-4119-b659-15b8f485eb9a.skill-01</code> | <strong><code>`CLICK` photo on the right</code></strong> |
| 8 | <strong>★ Set an image&#x27;s exact height</strong><br><code>7ae48c60-f143-4119-b659-15b8f485eb9a.skill-01</code> | <strong><code>`CLICK` position and size dropdown</code></strong> |
| 9 | <strong>★ Set an image&#x27;s exact height</strong><br><code>7ae48c60-f143-4119-b659-15b8f485eb9a.skill-01</code> | <strong><code>`TRIPLE_CLICK` height text box</code></strong> |
| 10 | <strong>★ Set an image&#x27;s exact height</strong><br><code>7ae48c60-f143-4119-b659-15b8f485eb9a.skill-01</code> | <strong><code>`TYPING` 30cm</code></strong> |
| 11 | <strong>★ Set an image&#x27;s exact height</strong><br><code>7ae48c60-f143-4119-b659-15b8f485eb9a.skill-01</code> | <strong><code>`PRESS` enter</code></strong> |
| 12 |  | <code>`CLICK` slide 6</code> |
| 13 | <strong>★ Set an image&#x27;s exact height</strong><br><code>7ae48c60-f143-4119-b659-15b8f485eb9a.skill-01</code> | <strong><code>`CLICK` photo</code></strong> |
| 14 | <strong>★ Set an image&#x27;s exact height</strong><br><code>7ae48c60-f143-4119-b659-15b8f485eb9a.skill-01</code> | <strong><code>`TRIPLE_CLICK` height text box</code></strong> |
| 15 | <strong>★ Set an image&#x27;s exact height</strong><br><code>7ae48c60-f143-4119-b659-15b8f485eb9a.skill-01</code> | <strong><code>`TYPING` 25cm</code></strong> |
| 16 | <strong>★ Set an image&#x27;s exact height</strong><br><code>7ae48c60-f143-4119-b659-15b8f485eb9a.skill-01</code> | <strong><code>`PRESS` enter</code></strong> |

### Source task `a434992a-89df-4577-925c-0c58b747f0f4`

Original instruction:

> Change the font size of the content to 12, and change the font color to orange. Change the slide's background to red.

Required skills derived from this source task:

- **Change text font size in a text box** — `a434992a-89df-4577-925c-0c58b747f0f4.skill-02`

Complete ordered single-action sequence:

| Action | Related required skill | Original single action |
| ---: | --- | --- |
| 0 |  | <code>`CLICK` background dropdown arrow</code> |
| 1 |  | <code>`CLICK` color</code> |
| 2 |  | <code>`CLICK` color dropdown arrow</code> |
| 3 |  | <code>`CLICK` red (2nd row, 5th from left)</code> |
| 4 | <strong>★ Change text font size in a text box</strong><br><code>a434992a-89df-4577-925c-0c58b747f0f4.skill-02</code> | <strong><code>`CLICK` the content text box</code></strong> |
| 5 | <strong>★ Change text font size in a text box</strong><br><code>a434992a-89df-4577-925c-0c58b747f0f4.skill-02</code> | <strong><code>`TRIPLE_CLICK` the font size text field</code></strong> |
| 6 | <strong>★ Change text font size in a text box</strong><br><code>a434992a-89df-4577-925c-0c58b747f0f4.skill-02</code> | <strong><code>`TYPING` 12</code></strong> |
| 7 | <strong>★ Change text font size in a text box</strong><br><code>a434992a-89df-4577-925c-0c58b747f0f4.skill-02</code> | <strong><code>`PRESS` enter</code></strong> |
| 8 |  | <code>`CLICK` the font color dropdown arrow</code> |
| 9 |  | <code>`CLICK` the orange color (2nd row, 3rd from left)</code> |

### Source task `e4ef0baf-4b52-4590-a47e-d4d464cca2d7`

Original instruction:

> The height of picture should be 20cm on slide 3 while the font size of all textboxes should be 40pt on slide 6.

Required skills derived from this source task:

- **Set font size for text in multiple text boxes** — `e4ef0baf-4b52-4590-a47e-d4d464cca2d7.skill-02`

Complete ordered single-action sequence:

| Action | Related required skill | Original single action |
| ---: | --- | --- |
| 0 |  | <code>`CLICK` slide 3.</code> |
| 1 |  | <code>`CLICK` image</code> |
| 2 |  | <code>`SCROLL` down to height text box</code> |
| 3 |  | <code>`TRIPLE_CLICK` height text box</code> |
| 4 |  | <code>`HOTKEY` ctrl-a</code> |
| 5 |  | <code>`TYPING` 20cm</code> |
| 6 |  | <code>`PRESS` enter</code> |
| 7 |  | <code>`CLICK` slide 6.</code> |
| 8 | <strong>★ Set font size for text in multiple text boxes</strong><br><code>e4ef0baf-4b52-4590-a47e-d4d464cca2d7.skill-02</code> | <strong><code>`TRIPLE_CLICK` text in &#x27;our founder&#x27;.</code></strong> |
| 9 | <strong>★ Set font size for text in multiple text boxes</strong><br><code>e4ef0baf-4b52-4590-a47e-d4d464cca2d7.skill-02</code> | <strong><code>`TRIPLE_CLICK` font size dropdown</code></strong> |
| 10 | <strong>★ Set font size for text in multiple text boxes</strong><br><code>e4ef0baf-4b52-4590-a47e-d4d464cca2d7.skill-02</code> | <strong><code>`TYPING` 40pt</code></strong> |
| 11 | <strong>★ Set font size for text in multiple text boxes</strong><br><code>e4ef0baf-4b52-4590-a47e-d4d464cca2d7.skill-02</code> | <strong><code>`PRESS` enter</code></strong> |
| 12 | <strong>★ Set font size for text in multiple text boxes</strong><br><code>e4ef0baf-4b52-4590-a47e-d4d464cca2d7.skill-02</code> | <strong><code>`TRIPLE_CLICK` text in &#x27;name surname&#x27;.</code></strong> |
| 13 | <strong>★ Set font size for text in multiple text boxes</strong><br><code>e4ef0baf-4b52-4590-a47e-d4d464cca2d7.skill-02</code> | <strong><code>`TRIPLE_CLICK` font size dropdown</code></strong> |
| 14 | <strong>★ Set font size for text in multiple text boxes</strong><br><code>e4ef0baf-4b52-4590-a47e-d4d464cca2d7.skill-02</code> | <strong><code>`TYPING` 40pt</code></strong> |
| 15 | <strong>★ Set font size for text in multiple text boxes</strong><br><code>e4ef0baf-4b52-4590-a47e-d4d464cca2d7.skill-02</code> | <strong><code>`PRESS` enter</code></strong> |
| 16 | <strong>★ Set font size for text in multiple text boxes</strong><br><code>e4ef0baf-4b52-4590-a47e-d4d464cca2d7.skill-02</code> | <strong><code>`TRIPLE_CLICK` text in &#x27;presentations are...&#x27;.</code></strong> |
| 17 | <strong>★ Set font size for text in multiple text boxes</strong><br><code>e4ef0baf-4b52-4590-a47e-d4d464cca2d7.skill-02</code> | <strong><code>`TRIPLE_CLICK` font size dropdown</code></strong> |
| 18 | <strong>★ Set font size for text in multiple text boxes</strong><br><code>e4ef0baf-4b52-4590-a47e-d4d464cca2d7.skill-02</code> | <strong><code>`TYPING` 40pt</code></strong> |
| 19 | <strong>★ Set font size for text in multiple text boxes</strong><br><code>e4ef0baf-4b52-4590-a47e-d4d464cca2d7.skill-02</code> | <strong><code>`PRESS` enter</code></strong> |

### Source task `ed43c15f-00cb-4054-9c95-62c880865d68`

Original instruction:

> Move the picture on page 2 to slide top. Make textboxes underlined on slide 1 and 2.

Required skills derived from this source task:

- **Reposition an image by dragging** — `ed43c15f-00cb-4054-9c95-62c880865d68.skill-02`

Complete ordered single-action sequence:

| Action | Related required skill | Original single action |
| ---: | --- | --- |
| 0 |  | <code>`HOTKEY` ctrl-a</code> |
| 1 |  | <code>`HOTKEY` ctrl-U</code> |
| 2 |  | <code>`CLICK` slide 2</code> |
| 3 |  | <code>`HOTKEY` ctrl-a</code> |
| 4 |  | <code>`HOTKEY` ctrl-U</code> |
| 5 | <strong>★ Reposition an image by dragging</strong><br><code>ed43c15f-00cb-4054-9c95-62c880865d68.skill-02</code> | <strong><code>`CLICK` image</code></strong> |
| 6 | <strong>★ Reposition an image by dragging</strong><br><code>ed43c15f-00cb-4054-9c95-62c880865d68.skill-02</code> | <strong><code>`DRAG_TO` top of slide</code></strong> |

## Review this package

Before choosing a decision, complete all three checks:

- [ ] **Task naturalness and skill necessity:** Is the reference task a natural Impress task, and is every listed required skill genuinely necessary and observable when solving it?
- [ ] **Initial artifact correctness:** Launch the environment and confirm that the presentation opens correctly, contains the content needed by the instruction, and has not already completed the requested results.
- [ ] **Source-task similarity:** Compare the reference task with the source instructions and complete single-action sequences above. Confirm that it is not merely an entity, field, or value substitution and does not reproduce a source task's complete ordered solution.

Use `approved` when all checks pass. Use `revision_requested` when the package is fixable and provide concrete revision instructions. Use `rejected` when the combination is fundamentally unnatural, infeasible, or too similar to a source task.

Fill [review.json](review.json), then collect completed forms from the repository root:

```bash
python scripts/python/manage_reference_review_packets.py collect \
  --skill-pool evaluation_examples/expert_skill_learning/impress_full_v1/generated/skill_pool.json \
  --packages evaluation_examples/expert_skill_learning/impress_full_v1/generated/round_01/reference_packages.json \
  --source-tasks evaluation_examples/expert_skill_learning/impress_full_v1/source_tasks.json \
  --reviews evaluation_examples/expert_skill_learning/impress_full_v1/generated/round_01/reference_package_reviews.json \
  --artifact-manifest evaluation_examples/expert_skill_learning/impress_full_v1/generated/round_01/artifacts/artifact_manifest.json \
  --task-config-manifest evaluation_examples/expert_skill_learning/impress_full_v1/generated/round_01/task_config_manifest.json \
  --task-detail-root evaluation_examples/expert_skill_learning/impress_full_v1/generated/round_01/task_details \
  --reviewer-guides evaluation_examples/expert_skill_learning/impress_full_v1/generated/round_01/reviewer_guides.json \
  --coverage evaluation_examples/expert_skill_learning/impress_full_v1/generated/round_01/coverage_state.json \
  --packet-root evaluation_examples/expert_skill_learning/impress_full_v1/generated/round_01/review_packets
```

Detailed field guidance is in [`reviewer.md`](../../../../../reviewer.md).
