# Dawn Marsh Survey

- Reference task: `reference-task-impress-full-r01-005`
- Application: `libreoffice_impress`
- Review decision: `pending`

## Task instruction

Finalize the “Dawn Marsh Survey” checklist slide for the field-team handoff: give the slide a solid midnight-teal background; convert the three unbulleted readiness statements in the checklist panel into a bulleted list; recolor the full “Launch window: 08:30” line to Yellow; underline every character in the “Carry spare batteries” reminder box; and remove the three pale draft-marker shapes clustered in the upper-right corner with one marquee selection. Keep the rest of the briefing deck unchanged.

## Required skills

### 1. Apply bulleted-list formatting to text in a content placeholder

Skill ID: `f23acfd2-c485-4b7c-a1e7-d4303ddfe864.skill-01`

Procedure:

1. Select the text box or content placeholder that contains the paragraph to format.
2. Open the List control from the Impress toolbar or sidebar and choose the bullet-list option.
3. Impress applies bullet formatting to the current paragraph or selected paragraphs; click in a paragraph before applying the command when no text range is selected.

Efficiency tip: Place the text cursor in the target paragraph before opening the List control, so the bullet style is applied without selecting unrelated text.

Source task: `f23acfd2-c485-4b7c-a1e7-d4303ddfe864`

Source instruction: Add a bullet point to the content of this slide.

Directly referenced source actions:

- Action 0: <code>`CLICK` text box for content</code>
- Action 1: <code>`CLICK` List dropdown</code>
- Action 2: <code>`CLICK` bullet icon</code>

### 2. Set a slide background to a solid color

Skill ID: `9cf05d24-6bd9-4dae-8967-f67d88f5d38a.skill-01`

Procedure:

1. With the target slide active, open the slide background formatting control.
2. Choose the Color background option.
3. Open the color palette and select a desired solid color, for example a green swatch.

Efficiency tip: Select the target slide before opening background formatting so the chosen color is applied directly without revisiting the control.

Source task: `9cf05d24-6bd9-4dae-8967-f67d88f5d38a`

Source instruction: Move to slide 1 and give it a green background color.

Directly referenced source actions:

- Action 0: <code>`CLICK` background dropdown menu</code>
- Action 1: <code>`CLICK` Color</code>
- Action 2: <code>`CLICK` the color dropdown</code>
- Action 3: <code>`CLICK` Green (2nd row, 2nd from right)</code>

### 3. Marquee-select several slide objects and delete them

Skill ID: `a53f80cd-4a90-4490-8310-097b011433f6.skill-03`

Procedure:

1. Open the slide containing the objects to remove.
2. Start in an empty area just outside the upper-left edge of the target object cluster, then drag a selection rectangle to an opposite corner so that all intended objects are enclosed.
3. Press Delete to remove every selected object from the slide.

Efficiency tip: Begin and end the marquee in blank slide space where possible. This reduces the risk of entering text-editing mode or moving an object instead of selecting the group.

Source task: `a53f80cd-4a90-4490-8310-097b011433f6`

Source instruction: Set the font color of the title in slides 2 to 3 as black and bold the title. Also, delete the personal information (including the icons)in slide 4.

Directly referenced source actions:

- Action 9: <code>`CLICK` slide 4</code>
- Action 10: <code>`MOVE_TO` top left corner of the location icon with some padding</code>
- Action 11: <code>`DRAG_TO` where bottom left corner of the pink image is</code>
- Action 12: <code>`PRESS` delete.</code>

### 4. Set selected text color from the font-color palette

Skill ID: `57667013-ea97-417c-9dce-2713091e6e2a.skill-01`

Procedure:

1. Click inside a text box to enter text-editing mode, rather than merely selecting the shape border.
2. Select the text to recolor, for example with Ctrl+A when all text in the active text box should be affected.
3. Open the Font Color drop-down on the formatting toolbar.
4. Choose the desired color swatch from the palette, for example the standard Yellow swatch. The selected text adopts that color.

Efficiency tip: Use Ctrl+A only after the text cursor is active inside the intended text box; otherwise it may select slide objects instead of the box's text.

Source task: `57667013-ea97-417c-9dce-2713091e6e2a`

Source instruction: Navigate to slide 5 and set the font color of all textboxes to yellow. Use exactly 'yellow'—no variations such as light yellow, dark yellow, or any other color.

Directly referenced source actions:

- Action 1: <code>`CLICK` text in &#x27;write an original...&#x27;</code>
- Action 2: <code>`HOTKEY` ctrl-A</code>
- Action 3: <code>`CLICK` font color dropdown.</code>
- Action 4: <code>`CLICK` yellow (2nd row, first from left)</code>

### 5. Underline all text in a text box

Skill ID: `ed43c15f-00cb-4054-9c95-62c880865d68.skill-01`

Procedure:

1. Enter text-editing mode for the text box, for example by double-clicking its text so that a caret appears.
2. Press Ctrl+A to select the text within the active text box. In text-editing mode this selects text rather than all slide objects.
3. Press Ctrl+U to toggle underline formatting for the selected text.
4. Repeat on other text boxes as needed; Ctrl+U applies the same underline technique to each independently selected text range.

Efficiency tip: Use Ctrl+A followed by Ctrl+U while the caret is inside each text box to format its full contents without manually dragging across the text.

Source task: `ed43c15f-00cb-4054-9c95-62c880865d68`

Source instruction: Move the picture on page 2 to slide top. Make textboxes underlined on slide 1 and 2.

Directly referenced source actions:

- Action 0: <code>`HOTKEY` ctrl-a</code>
- Action 1: <code>`HOTKEY` ctrl-U</code>
- Action 3: <code>`HOTKEY` ctrl-a</code>
- Action 4: <code>`HOTKEY` ctrl-U</code>

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

- Skill: `f23acfd2-c485-4b7c-a1e7-d4303ddfe864.skill-01`
- Intent: Turn the three readiness statements in the checklist text area into a bulleted list.
- Efficiency: Activate the checklist text area and place the caret in a readiness paragraph before using the bullet-list control; select all three list paragraphs if needed.
- Visible success: Each of the three readiness statements has a visible bullet, with no bullets added to the heading, status line, or reminder.

#### Demonstration 2

- Skill: `9cf05d24-6bd9-4dae-8967-f67d88f5d38a.skill-01`
- Intent: Apply the requested solid midnight-teal background to the active checklist slide.
- Efficiency: Select slide 2 before opening the slide-background control so the color is applied only to the checklist slide.
- Visible success: The entire slide canvas behind all objects is a uniform midnight teal (#0B3D4A), while the content objects remain in place.

#### Demonstration 3

- Skill: `a53f80cd-4a90-4490-8310-097b011433f6.skill-03`
- Intent: Remove the three obsolete pale draft markers together.
- Efficiency: Drag from blank space just outside the cluster to blank space beyond its opposite edge, ensuring the selection rectangle encloses only the three circles before pressing Delete.
- Visible success: All three upper-right pale circles disappear, while the heading, checklist panel, route note, status line, and reminder remain visible.

#### Demonstration 4

- Skill: `57667013-ea97-417c-9dce-2713091e6e2a.skill-01`
- Intent: Set the complete launch-window status line to Yellow.
- Efficiency: Enter text-editing mode in the status line and select its full text before choosing the standard Yellow swatch from the font-color palette.
- Visible success: Every character in “Launch window: 08:30” is Yellow, with no other text recolored by this operation.

#### Demonstration 5

- Skill: `ed43c15f-00cb-4054-9c95-62c880865d68.skill-01`
- Intent: Underline the entire battery reminder text box.
- Efficiency: Place a caret inside the reminder text box, select all text within that box, then use the underline shortcut.
- Visible success: Every character in “Carry spare batteries” has an underline; the surrounding outlined box itself is unchanged.

Recording start: Open the supplied two-slide PPTX in LibreOffice Impress with slide 2 available in normal editing view and all described unfinished elements present.

Recording end: Slide 2 shows the midnight-teal background, a three-item bulleted readiness list, Yellow launch-time text, a fully underlined battery reminder, and the former upper-right draft-marker cluster removed.

Allowed variation: Equivalent LibreOffice Impress controls, menus, keyboard shortcuts, or toolbar paths are acceptable as long as the specified final slide state is produced and unrelated objects remain unchanged.

### 中文详细参考方案

> 以下是一个可以参考的操作 guide。标注者可以根据实际 LibreOffice 界面采用等价操作。

本指南完成“Dawn Marsh Survey”中的第 2 张检查清单页：将页面背景设为纯色午夜青绿（#0B3D4A）、把三条准备事项变为项目符号列表、将完整状态行设为标准 Yellow、给电池提醒全文加下划线，并通过一次框选删除右上角的三个浅色圆形草稿标记。所有操作均应只影响第 2 张；第 1 张封面及第 2 张其余内容必须保留。

#### 启动后的初始状态检查

- 确认演示文稿在 LibreOffice Impress 的普通编辑视图中打开，左侧缩略图窗格应显示共两张幻灯片。
- 查看第 2 张缩略图并单击它，使其成为活动幻灯片；这是“选择幻灯片缩略图”，不是选择画布上的对象。画布应显示左侧准备事项面板、下方的“Launch window: 08:30”和“Carry spare batteries”，以及右上角紧凑的三个浅色圆形标记。
- 初始状态中，第 2 张背景应为暖白色而非 #0B3D4A；准备事项三行没有项目符号；状态行不是 Yellow；提醒文字没有下划线。若打开的文件已经显示某项所需结果，可不重复改变该项，但仍应核对该项仅作用于指定对象。
- 不要通过单击文字边缘的方式误把文字框当作文本来编辑：单击一次对象外框是“选择对象”，双击文字或在文字中单击至出现插入光标才是“进入文本编辑模式”。

#### 第 1 步：激活并确认第 2 张检查清单页

1. 在左侧缩略图窗格中单击第 2 张缩略图。画布中出现第 2 张后，先单击画布空白处，避免任何文字框或形状仍被选中。
2. 核对需要保留的内容：左上标题和浅色面板、左侧准备事项区、左下状态行和提醒框、右侧路线说明均存在；只有右上角三个浅色圆形是后续要删除的对象。
3. 如果单击后仍看到某个对象的选择手柄，单击不含对象的画布空白位置取消选择；不要按 `Delete`。

- 对应 skills：无；这是准备或检查步骤。
- 高效操作：先固定在第 2 张再进行所有页面级与对象级修改，可避免把背景或文字格式错误应用到封面。
- 完成标志：第 2 张缩略图处于选中状态，画布没有非目标对象被意外选中，且右上角仍可见三个浅色圆形标记。

#### 第 2 步：将三条准备事项改为项目符号列表

1. 在左侧准备事项面板内的“Calibrate water meter”文字上双击，直到出现文本插入光标；此时是进入 `readiness_list_text` 的文本编辑模式，而不是仅选中其文字框边框。
2. 按 `Ctrl+A`。确认高亮范围仅覆盖三段“Calibrate water meter”、“Pack sample envelopes”和“Confirm trail access”，而不包括标题、状态行或提醒文字。
3. 打开 `Format` > `Bullets and Numbering...`，在对话框中打开 `Bullets` 选项卡，选择普通圆点项目符号样式后点击 `OK`。
4. 如果只有一段出现项目符号，说明选区未覆盖三段：再次在该文字框中双击，按 `Ctrl+A` 仅选中框内文字，并重复 `Format` > `Bullets and Numbering...`。

- 对应 skills：`f23acfd2-c485-4b7c-a1e7-d4303ddfe864.skill-01`
- 高效操作：在目标文字框已经出现插入光标后再按 `Ctrl+A`，这样选择的是框内三段文本，不会选择整页对象。
- 完成标志：准备事项区的三条陈述各自带有一个可见项目符号；标题、状态行和电池提醒均未新增项目符号。

#### 第 3 步：设置第 2 张为纯色午夜青绿背景

1. 先单击左侧第 2 张缩略图，确保仍是第 2 张页面级选择，而不是某个文本框的文本编辑状态。
2. 选择 `Format` > `Slide Properties...`，在打开的对话框中选择 `Background` 选项卡。将 `Fill` 设置为 `Color`。
3. 打开 `Color` 的颜色选择器；若预设色板没有精确颜色，使用 `Custom Color...` 打开 `Color Picker`，将 `Hex #` 设为 `0B3D4A`，确认后以 `OK` 关闭颜色选择器及幻灯片属性对话框。
4. 如果背景没有变化，重新确认选择的是第 2 张缩略图，再打开 `Format` > `Slide Properties...` 检查 `Fill` 是否为 `Color`、颜色是否为 #0B3D4A；不要修改第 1 张缩略图。

- 对应 skills：`9cf05d24-6bd9-4dae-8967-f67d88f5d38a.skill-01`
- 高效操作：此操作前选择缩略图而不是单击某个面板，可使背景设置直接作用于整张检查清单页。
- 完成标志：第 2 张所有内容对象后方的整个幻灯片画布为均匀纯色 #0B3D4A；标题、面板、路线说明和文字框的位置没有移动。

#### 第 4 步：把完整启动时间状态行设为 Yellow

1. 在下方左侧的“Launch window: 08:30”文字上双击，确认文字中出现插入光标。这是文本编辑模式；若只看到文本框边界和控制点，需再双击文字本身。
2. 按 `Ctrl+A`，确认选择范围是该文本框中的完整“Launch window: 08:30”，包括“Launch window:”、空格和“08:30”。
3. 在格式工具栏打开 `Font Color` 的下拉菜单，选择标准色块 `Yellow`。
4. 如果仅部分字符变黄，或附近文字也被改变，撤销或重新在状态行内进入文本编辑模式，按 `Ctrl+A` 重新选中该框内全文后再选择 `Yellow`。

- 对应 skills：`57667013-ea97-417c-9dce-2713091e6e2a.skill-01`
- 高效操作：不要在对象仅显示边框时按 `Ctrl+A`；必须先看到插入光标，否则快捷键可能选择整页对象。
- 完成标志：“Launch window: 08:30”的每一个字符均为标准 `Yellow`，而准备事项、路线说明和其他文字颜色未改变。

#### 第 5 步：给电池提醒全文添加下划线

1. 在小型描边提醒框内的“Carry spare batteries”文字上双击，直到出现文本插入光标；不要只单击提醒框的边线，因为那只是选择对象。
2. 按 `Ctrl+A`，使该文本框内的“Carry spare batteries”全部被选中，然后按 `Ctrl+U`。
3. 单击画布空白处查看格式。如果文字已全部带下划线，则无需再调整。若只有部分文字带下划线，重新进入该提醒文字框的文本编辑模式，按 `Ctrl+A` 后再次按 `Ctrl+U`；若已有下划线却被切换取消，可立即再按一次 `Ctrl+U` 恢复。

- 对应 skills：`ed43c15f-00cb-4054-9c95-62c880865d68.skill-01`
- 高效操作：在插入光标位于提醒框内时使用 `Ctrl+A`、`Ctrl+U`，比手动拖选整句更不易遗漏首尾字符。
- 完成标志：“Carry spare batteries”的全部字符均有下划线，而其外侧的描边提醒框形状、大小和位置均保持不变。

#### 第 6 步：用一次框选删除右上角三个草稿标记

1. 单击画布空白处，退出任何文本编辑模式。不要先逐个单击圆形，也不要按住 `Shift` 逐个添加选择；本步骤需要一次矩形框选。
2. 在右上角圆形簇左上方的空白画布处按住鼠标左键，向该簇右下方的空白位置拖动，形成选择矩形。选择矩形必须完整包围三个浅色圆形 `draft_marker_one`、`draft_marker_two` 和 `draft_marker_three`，且不能碰入标题、面板、路线说明或其他保留对象。
3. 松开鼠标后，确认仅三个圆形显示为选中对象，然后按 `Delete` 一次。最后单击画布空白处取消选择。
4. 如果选择手柄显示在任何保留对象上，先单击空白处取消本次选择，再从更靠近圆形簇的空白边缘重新拖出更小的框选矩形；只有确认恰好选中三个圆形时才按 `Delete`。

- 对应 skills：`a53f80cd-4a90-4490-8310-097b011433f6.skill-03`
- 高效操作：从空白处开始并在空白处结束拖动，可避免进入文字编辑模式、移动对象，或把相邻保留内容加入选择。
- 完成标志：右上角三个浅色圆形全部消失；标题、清单面板、路线说明、启动时间和提醒框仍完整可见。

#### 最终结果检查

- 查看第 2 张：背景为无渐变、无图案的统一 #0B3D4A 纯色；内容对象仍位于原有布局中。
- 确认准备事项区恰有三条带项目符号的段落，文字分别为“Calibrate water meter”、“Pack sample envelopes”和“Confirm trail access”。
- 确认完整“Launch window: 08:30”为标准 `Yellow`，并且完整“Carry spare batteries”带下划线；提醒框的外框没有被删除或改变。
- 确认右上角没有残留任何一个浅色圆形草稿标记，且删除操作没有移除标题、面板、路线说明或其他第 2 张内容。
- 单击第 1 张缩略图进行检查：封面标题、副标题、地平线带和位置徽章仍存在且未改动。再返回第 2 张缩略图，确认最终页面仍显示上述五项要求。

## Source-task similarity review

| Measure | Maximum | Most similar source task |
| --- | ---: | --- |
| Lexical sequence similarity | 0.270115 | 04578141-1d42-4146-b9cf-6fab4ce5fd74 |
| Semantic cosine similarity | 0.525726 | 04578141-1d42-4146-b9cf-6fab4ce5fd74 |

Similarity scores are reviewer aids, not automatic acceptance thresholds. Inspect the contributing source tasks and their complete ordered actions below.

### Source task `57667013-ea97-417c-9dce-2713091e6e2a`

Original instruction:

> Navigate to slide 5 and set the font color of all textboxes to yellow. Use exactly 'yellow'—no variations such as light yellow, dark yellow, or any other color.

Required skills derived from this source task:

- **Set selected text color from the font-color palette** — `57667013-ea97-417c-9dce-2713091e6e2a.skill-01`

Complete ordered single-action sequence:

| Action | Related required skill | Original single action |
| ---: | --- | --- |
| 0 |  | <code>`CLICK` slide 5</code> |
| 1 | <strong>★ Set selected text color from the font-color palette</strong><br><code>57667013-ea97-417c-9dce-2713091e6e2a.skill-01</code> | <strong><code>`CLICK` text in &#x27;write an original...&#x27;</code></strong> |
| 2 | <strong>★ Set selected text color from the font-color palette</strong><br><code>57667013-ea97-417c-9dce-2713091e6e2a.skill-01</code> | <strong><code>`HOTKEY` ctrl-A</code></strong> |
| 3 | <strong>★ Set selected text color from the font-color palette</strong><br><code>57667013-ea97-417c-9dce-2713091e6e2a.skill-01</code> | <strong><code>`CLICK` font color dropdown.</code></strong> |
| 4 | <strong>★ Set selected text color from the font-color palette</strong><br><code>57667013-ea97-417c-9dce-2713091e6e2a.skill-01</code> | <strong><code>`CLICK` yellow (2nd row, first from left)</code></strong> |
| 5 |  | <code>`TRIPLE_CLICK` text in &#x27;Include a credit&#x27;...</code> |
| 6 |  | <code>`CLICK` font color.</code> |

### Source task `9cf05d24-6bd9-4dae-8967-f67d88f5d38a`

Original instruction:

> Move to slide 1 and give it a green background color.

Required skills derived from this source task:

- **Set a slide background to a solid color** — `9cf05d24-6bd9-4dae-8967-f67d88f5d38a.skill-01`

Complete ordered single-action sequence:

| Action | Related required skill | Original single action |
| ---: | --- | --- |
| 0 | <strong>★ Set a slide background to a solid color</strong><br><code>9cf05d24-6bd9-4dae-8967-f67d88f5d38a.skill-01</code> | <strong><code>`CLICK` background dropdown menu</code></strong> |
| 1 | <strong>★ Set a slide background to a solid color</strong><br><code>9cf05d24-6bd9-4dae-8967-f67d88f5d38a.skill-01</code> | <strong><code>`CLICK` Color</code></strong> |
| 2 | <strong>★ Set a slide background to a solid color</strong><br><code>9cf05d24-6bd9-4dae-8967-f67d88f5d38a.skill-01</code> | <strong><code>`CLICK` the color dropdown</code></strong> |
| 3 | <strong>★ Set a slide background to a solid color</strong><br><code>9cf05d24-6bd9-4dae-8967-f67d88f5d38a.skill-01</code> | <strong><code>`CLICK` Green (2nd row, 2nd from right)</code></strong> |

### Source task `a53f80cd-4a90-4490-8310-097b011433f6`

Original instruction:

> Set the font color of the title in slides 2 to 3 as black and bold the title. Also, delete the personal information (including the icons)in slide 4.

Required skills derived from this source task:

- **Marquee-select several slide objects and delete them** — `a53f80cd-4a90-4490-8310-097b011433f6.skill-03`

Complete ordered single-action sequence:

| Action | Related required skill | Original single action |
| ---: | --- | --- |
| 0 |  | <code>`CLICK` slide 2</code> |
| 1 |  | <code>`TRIPLE_CLICK` title text</code> |
| 2 |  | <code>`CLICK` font color dropdown.</code> |
| 3 |  | <code>`CLICK` black (1st row, first from left)</code> |
| 4 |  | <code>`CLICK` bold icon</code> |
| 5 |  | <code>`CLICK` slide 3</code> |
| 6 |  | <code>`TRIPLE_CLICK` title text</code> |
| 7 |  | <code>`CLICK` font color icon</code> |
| 8 |  | <code>`CLICK` bold icon</code> |
| 9 | <strong>★ Marquee-select several slide objects and delete them</strong><br><code>a53f80cd-4a90-4490-8310-097b011433f6.skill-03</code> | <strong><code>`CLICK` slide 4</code></strong> |
| 10 | <strong>★ Marquee-select several slide objects and delete them</strong><br><code>a53f80cd-4a90-4490-8310-097b011433f6.skill-03</code> | <strong><code>`MOVE_TO` top left corner of the location icon with some padding</code></strong> |
| 11 | <strong>★ Marquee-select several slide objects and delete them</strong><br><code>a53f80cd-4a90-4490-8310-097b011433f6.skill-03</code> | <strong><code>`DRAG_TO` where bottom left corner of the pink image is</code></strong> |
| 12 | <strong>★ Marquee-select several slide objects and delete them</strong><br><code>a53f80cd-4a90-4490-8310-097b011433f6.skill-03</code> | <strong><code>`PRESS` delete.</code></strong> |

### Source task `ed43c15f-00cb-4054-9c95-62c880865d68`

Original instruction:

> Move the picture on page 2 to slide top. Make textboxes underlined on slide 1 and 2.

Required skills derived from this source task:

- **Underline all text in a text box** — `ed43c15f-00cb-4054-9c95-62c880865d68.skill-01`

Complete ordered single-action sequence:

| Action | Related required skill | Original single action |
| ---: | --- | --- |
| 0 | <strong>★ Underline all text in a text box</strong><br><code>ed43c15f-00cb-4054-9c95-62c880865d68.skill-01</code> | <strong><code>`HOTKEY` ctrl-a</code></strong> |
| 1 | <strong>★ Underline all text in a text box</strong><br><code>ed43c15f-00cb-4054-9c95-62c880865d68.skill-01</code> | <strong><code>`HOTKEY` ctrl-U</code></strong> |
| 2 |  | <code>`CLICK` slide 2</code> |
| 3 | <strong>★ Underline all text in a text box</strong><br><code>ed43c15f-00cb-4054-9c95-62c880865d68.skill-01</code> | <strong><code>`HOTKEY` ctrl-a</code></strong> |
| 4 | <strong>★ Underline all text in a text box</strong><br><code>ed43c15f-00cb-4054-9c95-62c880865d68.skill-01</code> | <strong><code>`HOTKEY` ctrl-U</code></strong> |
| 5 |  | <code>`CLICK` image</code> |
| 6 |  | <code>`DRAG_TO` top of slide</code> |

### Source task `f23acfd2-c485-4b7c-a1e7-d4303ddfe864`

Original instruction:

> Add a bullet point to the content of this slide.

Required skills derived from this source task:

- **Apply bulleted-list formatting to text in a content placeholder** — `f23acfd2-c485-4b7c-a1e7-d4303ddfe864.skill-01`

Complete ordered single-action sequence:

| Action | Related required skill | Original single action |
| ---: | --- | --- |
| 0 | <strong>★ Apply bulleted-list formatting to text in a content placeholder</strong><br><code>f23acfd2-c485-4b7c-a1e7-d4303ddfe864.skill-01</code> | <strong><code>`CLICK` text box for content</code></strong> |
| 1 | <strong>★ Apply bulleted-list formatting to text in a content placeholder</strong><br><code>f23acfd2-c485-4b7c-a1e7-d4303ddfe864.skill-01</code> | <strong><code>`CLICK` List dropdown</code></strong> |
| 2 | <strong>★ Apply bulleted-list formatting to text in a content placeholder</strong><br><code>f23acfd2-c485-4b7c-a1e7-d4303ddfe864.skill-01</code> | <strong><code>`CLICK` bullet icon</code></strong> |

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
