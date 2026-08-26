# Harbor Pollinator Day

- Reference task: `reference-task-impress-full-r01-001`
- Application: `libreoffice_impress`
- Review decision: `pending`

## Task instruction

For the Harbor Pollinator Day volunteer briefing, refine the RSVP message on slide 2 so it works as a centered closing callout: move the RSVP callout from the upper-left area to the footer directly beneath the three schedule cards, center-align all paragraphs in that callout, and emphasize only the words “Register by Friday” with an underline and the exact teal color #007C83. Leave the rest of the RSVP text in its existing dark gray color and without underlining.

## Required skills

### 1. Reposition a text box on a slide

Skill ID: `15aece23-a215-4579-91b4-69eec72e18da.skill-01`

Procedure:

1. In Normal view, select the slide containing the object in the Slides pane.
2. Click the text box border once to select the text box as an object; do not click into the text if you only want to move it.
3. Drag the selected text box to the desired location on the slide, such as nearer the lower edge, and release the mouse.

Efficiency tip: Drag the object by its border rather than entering text-editing mode; use alignment guides or arrow keys afterward if a small positional adjustment is needed.

Source task: `15aece23-a215-4579-91b4-69eec72e18da`

Source instruction: Move the title of page 2 to the bottom of the slide.

Directly referenced source actions:

- Action 0: <code>`CLICK` slide 2</code>
- Action 1: <code>`CLICK` Product Comparison text box</code>
- Action 2: <code>`DRAG_TO` bottom of the slide</code>

### 2. Underline selected text

Skill ID: `4ed5abd0-8b5d-47bd-839f-cacfa15ca37a.skill-02`

Procedure:

1. With text already selected in text-editing mode, click the Underline button on the formatting toolbar.
2. Use the same button again to toggle underlining off for a selected range when needed.

Efficiency tip: Apply underline immediately after another character-formatting change while the text selection is still active, avoiding an extra click into the text box and reselection.

Source task: `4ed5abd0-8b5d-47bd-839f-cacfa15ca37a`

Source instruction: Set the color of titles in slides 2,3,5 as black and underline them.

Directly referenced source actions:

- Action 5: <code>`CLICK` underline icon</code>
- Action 11: <code>`CLICK` underline icon</code>
- Action 17: <code>`CLICK` underline icon</code>

### 3. Apply a font color to selected text

Skill ID: `986fc832-6af2-417c-8845-9272b3a1528b.skill-02`

Procedure:

1. With text already selected in a text-editing context, click the Font Color control on the formatting toolbar.
2. Choose the required color from the color palette to apply it to the current selection.

Efficiency tip: Keep the text selection active while opening the Font Color palette so the chosen color is applied immediately without reselecting the text.

Source task: `986fc832-6af2-417c-8845-9272b3a1528b`

Source instruction: underline the content and make the font color on this slide (including the table) dark red 2.

Directly referenced source actions:

- Action 3: <code>`CLICK` font color icon</code>
- Action 4: <code>`CLICK` dark red 2</code>

### 4. Set paragraph alignment in a text box

Skill ID: `05dd4c1d-c489-4c85-8389-a7836c4f0567.skill-01`

Procedure:

1. Navigate to the slide containing the text box.
2. Click the text in the shape to enter text-editing mode, rather than merely selecting the shape.
3. Press Ctrl+A to select the text in that text box.
4. Click the desired paragraph alignment control, such as Align Right, Center, or Align Left, in the toolbar or Sidebar Paragraph section.
5. For example, choose Center to center all selected text within the text box.

Efficiency tip: After entering text-editing mode, Ctrl+A selects the text in the current text box, allowing one alignment command to format the entire text box without manually dragging over its contents.

Source task: `05dd4c1d-c489-4c85-8389-a7836c4f0567`

Source instruction: Align the first textbox on slide 3 to the right, on slide 4 to the center, and on slide 5 to the left. Ensure that the alignment is applied correctly to each respective slide.

Directly referenced source actions:

- Action 0: <code>`CLICK` Slide 3</code>
- Action 1: <code>`CLICK` &#x27;HELLO&#x27;</code>
- Action 2: <code>`HOTKEY` ctrl-A</code>
- Action 3: <code>`CLICK` right-align icon</code>
- Action 4: <code>`CLICK` Slide 4</code>
- Action 5: <code>`CLICK` &#x27;WRITE&#x27;</code>
- Action 6: <code>`HOTKEY` ctrl-A</code>
- Action 7: <code>`CLICK` center-align icon</code>
- Action 8: <code>`CLICK` Slide 5</code>
- Action 9: <code>`CLICK` &#x27;WRITE&#x27;</code>
- Action 10: <code>`HOTKEY` ctrl-A</code>
- Action 11: <code>`CLICK` left-align icon under paragraph section</code>

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
- Intent: Reposition the RSVP text box from the upper-left area to the centered footer beneath the three schedule cards.
- Efficiency: Select the text box by its border and drag it using the card row and slide-center guide as placement references.
- Visible success: The RSVP text box appears below the card row, centered in the open footer region rather than beside the heading.

#### Demonstration 2

- Skill: `4ed5abd0-8b5d-47bd-839f-cacfa15ca37a.skill-02`
- Intent: Underline only the deadline phrase “Register by Friday” within the RSVP callout.
- Efficiency: Keep the deadline phrase selected while applying the underline so no surrounding text is formatted.
- Visible success: Only the deadline words have a visible underline; the surrounding packing-list and reservation text remains unlined.

#### Demonstration 3

- Skill: `986fc832-6af2-417c-8845-9272b3a1528b.skill-02`
- Intent: Apply the exact teal #007C83 font color to the selected deadline phrase.
- Efficiency: Apply the teal color while the same deadline phrase remains selected after its underline is set.
- Visible success: “Register by Friday” is teal while all remaining RSVP copy stays dark gray.

#### Demonstration 4

- Skill: `05dd4c1d-c489-4c85-8389-a7836c4f0567.skill-01`
- Intent: Center-align every paragraph in the RSVP callout text box.
- Efficiency: Enter text-editing mode in the RSVP callout, select all text in that box, and apply paragraph centering once.
- Visible success: Both sentences in the RSVP message are centered within the relocated callout area.

Recording start: Open the provided two-slide Harbor Pollinator Day presentation in Normal view with slide 2 selected; the RSVP text box is visibly upper-left, left-aligned, and unformatted at the deadline phrase.

Recording end: Slide 2 shows the RSVP text box centered in the footer below the schedule cards, with all callout paragraphs centered and only “Register by Friday” teal (#007C83) and underlined.

Allowed variation: The callout may be placed with minor positional variation as long as it is clearly centered beneath the three schedule cards, does not overlap another object, and the specified text formatting is exact.

### 中文详细参考方案

> 以下是一个可以参考的操作 guide。标注者可以根据实际 LibreOffice 界面采用等价操作。

本指南在 LibreOffice Impress 的 Normal 视图中完成第 2 张幻灯片的 RSVP 收尾信息：仅移动可编辑的 RSVP 文本框到三张日程卡片下方的居中页脚区，将文本框内所有段落居中，并且只把“Register by Friday”设为带下划线的精确青绿色 #007C83。其余 RSVP 文本保持原有深灰色且不加下划线，其他幻灯片和日程内容不作修改。

#### 启动后的初始状态检查

- 确认当前处于 Normal 视图，左侧 Slides 窗格可见两张缩略图；第 2 张缩略图应被选中或可被选中。
- 查看第 2 张：中部应有三张从左至右排列的日程卡片，文字依次为“9:00 — Check in at Pier Garden”、“9:30 — Plant shoreline natives”和“11:30 — Return tools and sort compost.”。
- 确认 RSVP 文字对象显示“Bring water, sun protection, and gloves. Register by Friday to reserve a planting kit.”，位于左上区域、左对齐，且“Register by Friday”当前为深灰色并未加下划线。
- 识别两个独立对象：RSVP 的背景面板是形状，RSVP 文字是可编辑文本框。此任务移动的是文字框；背景面板仍留在原位置是可接受的，无需为了移动文字而选择或移动该面板。

#### 第 1 步：定位第 2 张并确认要编辑的对象

1. 在左侧 Slides 窗格中单击第 2 张的缩略图；这是选择幻灯片，不是选择画布上的对象。
2. 在画布左上区域找到 RSVP 文本。单击文本框的外边框一次，使其出现对象选择边框和控制点；不要双击文字，也不要在句子中单击，否则会进入文字编辑模式。
3. 可接受的初始状态是该文字框在左上区域且没有与其他对象重叠。如果它已经位于三张卡片下方的居中页脚区，则不需要移动；若它仍在左上区域，继续下一步。

- 对应 skills：无；这是准备或检查步骤。
- 高效操作：先以边框选中对象，可避免误把整个文本内容选中或误选到 RSVP 背景面板。
- 完成标志：第 2 张缩略图处于选中状态，且仅 RSVP 文字框有控制点；三个日程卡片、文字和背景面板均未被选中。

#### 第 2 步：将 RSVP 文字框移到卡片下方的居中页脚区

1. 保持 RSVP 文字框以对象边框选中的状态，从边框处拖动文字框到三张日程卡片正下方的空白页脚区，然后松开鼠标。不要通过拖动文字本身进入文字编辑模式。
2. 以中间日程卡片的水平中心和幻灯片中线作为参考，使文本框整体明显位于三张卡片下方并大致居中；不应覆盖任何卡片、标题或其他文字。
3. 若拖动后已清晰地位于卡片行下方且视觉居中，则无需再调整。若位置偏左、偏右或与卡片重叠，重新单击文字框边框后用方向键作小幅调整，或再次从边框拖动；不要移动 `rsvp_callout_panel` 背景形状。

- 对应 skills：`15aece23-a215-4579-91b4-69eec72e18da.skill-01`
- 高效操作：拖动时观察对齐参考线；释放后用方向键微调通常比重复长距离拖动更容易保持居中。
- 完成标志：RSVP 文字框已成为三张日程卡片下方的收尾信息，位于开放的页脚区域并明显居中，且没有遮挡日程内容。

#### 第 3 步：将 RSVP 文本框中的所有段落居中

1. 双击已移动的 RSVP 文字框内的文字，或在文字上单击进入文字编辑模式；此时应能看到插入光标，而非仅看到对象控制点。
2. 按 `Ctrl+A`。在文字编辑模式中，这会选择当前 RSVP 文本框内的全部文本，而不是选择幻灯片上的全部对象。
3. 在格式工具栏单击 `Center` 段落对齐按钮。也可打开右侧 `Properties` 侧边栏，在段落对齐控件中选择 `Center`。
4. 可接受的结果是每个 RSVP 段落都在文本框宽度内居中；若文本原本已居中，则无需改变。若只有部分行居中，重新在该文本框中进入编辑模式，按 `Ctrl+A`，再选择 `Center`。

- 对应 skills：`05dd4c1d-c489-4c85-8389-a7836c4f0567.skill-01`
- 高效操作：使用 `Ctrl+A` 后只执行一次 `Center`，可避免逐行选择造成漏改。
- 完成标志：RSVP 信息的两句文字均以文本框中心为基准居中显示；文字框仍在卡片下方的居中页脚区。

#### 第 4 步：仅对截止日期短语添加下划线和精确青绿色

1. 保持在 RSVP 文本框的文字编辑模式中，用鼠标从“Register by Friday”的第一个字符拖到最后一个字符，精确选中这 18 个字符；不要包含其前面的空格、前一句、后面的“ to reserve a planting kit.”或句点。
2. 在选区仍高亮时，单击格式工具栏的 `Underline`。若所选短语已经显示下划线，则不需要再次单击；若误使周围文字带下划线，选中那些误格式化的字符并再次单击 `Underline` 取消。
3. 保持同一短语仍被选中，打开 `Font Color` 的下拉菜单并选择 `Custom Color...`。在颜色对话框中将 `Hex #` 设为 `007C83`，然后确认。若该对话框没有 `Hex #` 输入项，则在 RGB 输入项中设定 `Red` 为 `0`、`Green` 为 `124`、`Blue` 为 `131`，再确认；这与 #007C83 相同。
4. 可接受的结果是仅“Register by Friday”为 #007C83 且带下划线。如果整段 RSVP 文字意外变成青绿色或被加下划线，先仅选中不应改变的字符，使用 `Font Color` 恢复其原有深灰色，并用 `Underline` 关闭其下划线；然后重新精确选中该截止日期短语并应用所需格式。

- 对应 skills：`4ed5abd0-8b5d-47bd-839f-cacfa15ca37a.skill-02`, `986fc832-6af2-417c-8845-9272b3a1528b.skill-02`
- 高效操作：在同一段文字保持高亮选中时连续完成 `Underline` 和 `Font Color`，可确保字符级格式只作用于该短语，无须重新选择。
- 完成标志：“Register by Friday”清晰显示为青绿色 #007C83 并有下划线；“Bring water, sun protection, and gloves.”以及“to reserve a planting kit.”仍为深灰色且没有下划线。

#### 第 5 步：退出编辑并检查版面关系

1. 单击 RSVP 文本框外侧的空白画布，退出文字编辑模式并取消文字选区，以便检查最终可见效果。
2. 查看对象层次和位置：文字框应完整可读、居中位于卡片下方，且没有遮住三张卡片。若文字框被卡片覆盖或与卡片重叠，单击其边框重新选择对象并向下或横向小幅移动；若其已在清晰的居中页脚区，则无需调整。
3. 不要调整日程卡片、标题、背景、RSVP 背景面板或第 1 张幻灯片中的对象。

- 对应 skills：无；这是准备或检查步骤。
- 高效操作：退出文字编辑模式后再判断居中和重叠，可避免被插入光标、选区高亮或对象控制点干扰视觉判断。
- 完成标志：第 2 张呈现清晰的日程卡片行和下方居中的 RSVP 收尾文字，卡片顺序与其余页面元素保持不变。

#### 最终结果检查

- 在 Slides 窗格检查仍只有两张幻灯片，顺序未改变；第 1 张缩略图的封面内容未被修改。
- 查看第 2 张：三张日程卡片仍从左到右依次显示“9:00 — Check in at Pier Garden”、“9:30 — Plant shoreline natives”和“11:30 — Return tools and sort compost.”，其位置、文字和背景均未改变。
- 确认 RSVP 文字框在三张卡片正下方的页脚开放区域并明显居中，未与任何卡片或其他对象重叠。
- 确认 RSVP 文本框内所有段落均为居中对齐。
- 确认只有“Register by Friday”带下划线并为精确颜色 #007C83；其余 RSVP 文本保持深灰色且不带下划线，且完整文案未被改写。

## Source-task similarity review

| Measure | Maximum | Most similar source task |
| --- | ---: | --- |
| Lexical sequence similarity | 0.272727 | 04578141-1d42-4146-b9cf-6fab4ce5fd74 |
| Semantic cosine similarity | 0.423523 | 986fc832-6af2-417c-8845-9272b3a1528b |

Similarity scores are reviewer aids, not automatic acceptance thresholds. Inspect the contributing source tasks and their complete ordered actions below.

### Source task `05dd4c1d-c489-4c85-8389-a7836c4f0567`

Original instruction:

> Align the first textbox on slide 3 to the right, on slide 4 to the center, and on slide 5 to the left. Ensure that the alignment is applied correctly to each respective slide.

Required skills derived from this source task:

- **Set paragraph alignment in a text box** — `05dd4c1d-c489-4c85-8389-a7836c4f0567.skill-01`

Complete ordered single-action sequence:

| Action | Related required skill | Original single action |
| ---: | --- | --- |
| 0 | <strong>★ Set paragraph alignment in a text box</strong><br><code>05dd4c1d-c489-4c85-8389-a7836c4f0567.skill-01</code> | <strong><code>`CLICK` Slide 3</code></strong> |
| 1 | <strong>★ Set paragraph alignment in a text box</strong><br><code>05dd4c1d-c489-4c85-8389-a7836c4f0567.skill-01</code> | <strong><code>`CLICK` &#x27;HELLO&#x27;</code></strong> |
| 2 | <strong>★ Set paragraph alignment in a text box</strong><br><code>05dd4c1d-c489-4c85-8389-a7836c4f0567.skill-01</code> | <strong><code>`HOTKEY` ctrl-A</code></strong> |
| 3 | <strong>★ Set paragraph alignment in a text box</strong><br><code>05dd4c1d-c489-4c85-8389-a7836c4f0567.skill-01</code> | <strong><code>`CLICK` right-align icon</code></strong> |
| 4 | <strong>★ Set paragraph alignment in a text box</strong><br><code>05dd4c1d-c489-4c85-8389-a7836c4f0567.skill-01</code> | <strong><code>`CLICK` Slide 4</code></strong> |
| 5 | <strong>★ Set paragraph alignment in a text box</strong><br><code>05dd4c1d-c489-4c85-8389-a7836c4f0567.skill-01</code> | <strong><code>`CLICK` &#x27;WRITE&#x27;</code></strong> |
| 6 | <strong>★ Set paragraph alignment in a text box</strong><br><code>05dd4c1d-c489-4c85-8389-a7836c4f0567.skill-01</code> | <strong><code>`HOTKEY` ctrl-A</code></strong> |
| 7 | <strong>★ Set paragraph alignment in a text box</strong><br><code>05dd4c1d-c489-4c85-8389-a7836c4f0567.skill-01</code> | <strong><code>`CLICK` center-align icon</code></strong> |
| 8 | <strong>★ Set paragraph alignment in a text box</strong><br><code>05dd4c1d-c489-4c85-8389-a7836c4f0567.skill-01</code> | <strong><code>`CLICK` Slide 5</code></strong> |
| 9 | <strong>★ Set paragraph alignment in a text box</strong><br><code>05dd4c1d-c489-4c85-8389-a7836c4f0567.skill-01</code> | <strong><code>`CLICK` &#x27;WRITE&#x27;</code></strong> |
| 10 | <strong>★ Set paragraph alignment in a text box</strong><br><code>05dd4c1d-c489-4c85-8389-a7836c4f0567.skill-01</code> | <strong><code>`HOTKEY` ctrl-A</code></strong> |
| 11 | <strong>★ Set paragraph alignment in a text box</strong><br><code>05dd4c1d-c489-4c85-8389-a7836c4f0567.skill-01</code> | <strong><code>`CLICK` left-align icon under paragraph section</code></strong> |

### Source task `15aece23-a215-4579-91b4-69eec72e18da`

Original instruction:

> Move the title of page 2 to the bottom of the slide.

Required skills derived from this source task:

- **Reposition a text box on a slide** — `15aece23-a215-4579-91b4-69eec72e18da.skill-01`

Complete ordered single-action sequence:

| Action | Related required skill | Original single action |
| ---: | --- | --- |
| 0 | <strong>★ Reposition a text box on a slide</strong><br><code>15aece23-a215-4579-91b4-69eec72e18da.skill-01</code> | <strong><code>`CLICK` slide 2</code></strong> |
| 1 | <strong>★ Reposition a text box on a slide</strong><br><code>15aece23-a215-4579-91b4-69eec72e18da.skill-01</code> | <strong><code>`CLICK` Product Comparison text box</code></strong> |
| 2 | <strong>★ Reposition a text box on a slide</strong><br><code>15aece23-a215-4579-91b4-69eec72e18da.skill-01</code> | <strong><code>`DRAG_TO` bottom of the slide</code></strong> |

### Source task `4ed5abd0-8b5d-47bd-839f-cacfa15ca37a`

Original instruction:

> Set the color of titles in slides 2,3,5 as black and underline them.

Required skills derived from this source task:

- **Underline selected text** — `4ed5abd0-8b5d-47bd-839f-cacfa15ca37a.skill-02`

Complete ordered single-action sequence:

| Action | Related required skill | Original single action |
| ---: | --- | --- |
| 0 |  | <code>`CLICK` Slide 2.</code> |
| 1 |  | <code>`CLICK` the title text box</code> |
| 2 |  | <code>`HOTKEY` ctrl-A</code> |
| 3 |  | <code>`CLICK` font color dropdown.</code> |
| 4 |  | <code>`CLICK` black</code> |
| 5 | <strong>★ Underline selected text</strong><br><code>4ed5abd0-8b5d-47bd-839f-cacfa15ca37a.skill-02</code> | <strong><code>`CLICK` underline icon</code></strong> |
| 6 |  | <code>`CLICK` Slide 3.</code> |
| 7 |  | <code>`CLICK` the title text box</code> |
| 8 |  | <code>`HOTKEY` ctrl-A</code> |
| 9 |  | <code>`CLICK` font color dropdown.</code> |
| 10 |  | <code>`CLICK` black</code> |
| 11 | <strong>★ Underline selected text</strong><br><code>4ed5abd0-8b5d-47bd-839f-cacfa15ca37a.skill-02</code> | <strong><code>`CLICK` underline icon</code></strong> |
| 12 |  | <code>`CLICK` Slide 5.</code> |
| 13 |  | <code>`CLICK` the title text box</code> |
| 14 |  | <code>`HOTKEY` ctrl-A</code> |
| 15 |  | <code>`CLICK` font color dropdown.</code> |
| 16 |  | <code>`CLICK` black</code> |
| 17 | <strong>★ Underline selected text</strong><br><code>4ed5abd0-8b5d-47bd-839f-cacfa15ca37a.skill-02</code> | <strong><code>`CLICK` underline icon</code></strong> |

### Source task `986fc832-6af2-417c-8845-9272b3a1528b`

Original instruction:

> underline the content and make the font color on this slide (including the table) dark red 2.

Required skills derived from this source task:

- **Apply a font color to selected text** — `986fc832-6af2-417c-8845-9272b3a1528b.skill-02`

Complete ordered single-action sequence:

| Action | Related required skill | Original single action |
| ---: | --- | --- |
| 0 |  | <code>`CLICK` outline</code> |
| 1 |  | <code>`HOTKEY` ctrl-A</code> |
| 2 |  | <code>`HOTKEY` ctrl-U</code> |
| 3 | <strong>★ Apply a font color to selected text</strong><br><code>986fc832-6af2-417c-8845-9272b3a1528b.skill-02</code> | <strong><code>`CLICK` font color icon</code></strong> |
| 4 | <strong>★ Apply a font color to selected text</strong><br><code>986fc832-6af2-417c-8845-9272b3a1528b.skill-02</code> | <strong><code>`CLICK` dark red 2</code></strong> |
| 5 |  | <code>`CLICK` normal</code> |
| 6 |  | <code>`CLICK` table</code> |
| 7 |  | <code>`CLICK` cursor before &#x27;Model Name&#x27;</code> |
| 8 |  | <code>`DRAG_TO` bottom right corner of table</code> |
| 9 |  | <code>`HOTKEY` ctrl-U</code> |
| 10 |  | <code>`CLICK` font color icon</code> |

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
