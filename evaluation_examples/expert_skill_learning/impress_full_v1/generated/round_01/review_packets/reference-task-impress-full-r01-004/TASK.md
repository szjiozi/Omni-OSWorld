# Community Garden Field Brief

- Reference task: `reference-task-impress-full-r01-004`
- Application: `libreoffice_impress`
- Review decision: `pending`

## Task instruction

Prepare the Community Garden Field Brief for the volunteer walk-through. Give the two working slides (Slides 2 and 3) the shared pale-mint background #E5F1E8 by selecting them together. On Slide 2, resize the existing garden-bed illustration to exactly 5.80 cm wide by 3.60 cm high, and set the “Morning Walk Checklist” callout text in the lower-left card to Liberation Sans. On Slide 3, update the four consecutive column labels in the existing table’s header row to “Area”, “Visit time”, “Coordinator”, and “Materials”, moving across the row as each label is replaced. Keep the rest of the brief unchanged.

## Required skills

### 1. Overwrite text in consecutive table cells using Tab

Skill ID: `5cfb9197-e72b-454b-900e-c06b0c802b40.skill-01`

Procedure:

1. Click inside the first table cell whose existing text should be replaced; this places the text cursor in the cell rather than merely selecting the table object.
2. Press Ctrl+A to select the current cell's text, then type the replacement value.
3. Press Tab to move the text cursor to the next cell in the row.
4. Repeat Ctrl+A, typing the replacement value, and Tab navigation for each subsequent cell. Do not press Tab after the final cell unless you intend to continue editing cells.

Efficiency tip: Keep the cursor inside the table and use Tab to advance across cells, avoiding repeated mouse selection of each cell.

Source task: `5cfb9197-e72b-454b-900e-c06b0c802b40`

Source instruction: Change the first row of table to "T1","T2","T3","T4" on slide 4.

Directly referenced source actions:

- Action 1: <code>`CLICK` Table 1</code>
- Action 2: <code>`HOTKEY` ctrl-A</code>
- Action 3: <code>`TYPING` T1</code>
- Action 4: <code>`PRESS` tab</code>
- Action 5: <code>`HOTKEY` ctrl-A</code>
- Action 6: <code>`TYPING` T2</code>
- Action 7: <code>`PRESS` tab</code>
- Action 8: <code>`HOTKEY` ctrl-A</code>
- Action 9: <code>`TYPING` T3</code>
- Action 10: <code>`PRESS` tab</code>
- Action 11: <code>`HOTKEY` ctrl-A</code>
- Action 12: <code>`TYPING` T4</code>

### 2. Set an image to exact width and height

Skill ID: `c82632a4-56b6-4db4-9dd1-3820ee3388e4.skill-02`

Procedure:

1. Select the image object on the slide, then open the Position and Size controls from the object formatting options.
2. Scroll within the controls if necessary until the Width and Height fields are visible.
3. Replace the Width value with a measurement such as 1 cm, press Tab to move to Height, enter the required height such as 1 cm, and press Enter to apply the dimensions.

Efficiency tip: Use Tab after entering Width to reach Height directly; this avoids reopening controls or selecting the object again.

Source task: `c82632a4-56b6-4db4-9dd1-3820ee3388e4`

Source instruction: Add an image "none.png" on the Desktop to slide 2 with 1cm*1cm size.

Directly referenced source actions:

- Action 5: <code>`CLICK` position and size dropdown</code>
- Action 6: <code>`SCROLL` down to width text box</code>
- Action 7: <code>`TRIPLE_CLICK` width text box</code>
- Action 8: <code>`TYPING` 1cm</code>
- Action 9: <code>`PRESS` tab</code>
- Action 10: <code>`TYPING` 1cm</code>
- Action 11: <code>`PRESS` enter</code>

### 3. Change the font family of selected text

Skill ID: `af2d657a-e6b3-4c6a-9f67-9e3ed015974c.skill-01`

Procedure:

1. Enter text-editing mode in a text placeholder or shape, then select the text whose font family you want to change. For example, use Ctrl+A while the text cursor is active to select all text in that text object.
2. Click the font-name box on the formatting toolbar, replace its current value with a font family name such as “Microsoft JhengHei,” and apply the entry.

Efficiency tip: Select the text before changing the font so the font change affects only the intended text object rather than future typing.

Source task: `af2d657a-e6b3-4c6a-9f67-9e3ed015974c`

Source instruction: In the first slide, insert the title "Happy Family" and make the font style "Microsoft JhengHei".

Directly referenced source actions:

- Action 2: <code>`HOTKEY` ctrl-a</code>
- Action 3: <code>`TRIPLE_CLICK` font text field</code>
- Action 4: <code>`TYPING` &#x27;Microsoft JhengHei&#x27;</code>

### 4. Select multiple slides in the Slides pane

Skill ID: `9ec204e4-f0a3-42f8-8458-b772a6797cab.skill-01`

Procedure:

1. In Normal view, locate the target slide thumbnails in the Slides pane.
2. Click the first slide thumbnail.
3. Hold Ctrl and click each additional slide thumbnail to add it to the selection without replacing the existing selection.
4. For example, Ctrl-click a neighboring slide after selecting the first one to prepare both slides for a shared operation.

Efficiency tip: Use Ctrl-click to build a multi-slide selection before applying an operation once, rather than repeating it for each slide.

Source task: `9ec204e4-f0a3-42f8-8458-b772a6797cab`

Source instruction: Please duplicate the last two slides and insert the copies in alternating order, so the sequence becomes: original slide A, original slide B, then duplicated slide A, duplicated slide B.

Directly referenced source actions:

- Action 1: <code>`CLICK` slide 23</code>
- Action 2: <code>`KEY_DOWN` Ctrl</code>
- Action 3: <code>`CLICK` slide 24</code>
- Action 4: <code>`KEY_UP` Ctrl</code>

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

- Skill: `5cfb9197-e72b-454b-900e-c06b0c802b40.skill-01`
- Intent: Replace all four adjacent header labels in the Slide 3 assignment table while retaining the existing table structure.
- Efficiency: Place the text cursor in the first header cell and use Tab to advance through the remaining consecutive header cells after replacing each cell’s text.
- Visible success: The header row reads, from left to right, “Area”, “Visit time”, “Coordinator”, and “Materials”, with the body rows unchanged.

#### Demonstration 2

- Skill: `c82632a4-56b6-4db4-9dd1-3820ee3388e4.skill-02`
- Intent: Set the existing Slide 2 garden-bed illustration to the specified physical dimensions.
- Efficiency: Enter the width and then use Tab to reach the height field in the same size-control interaction.
- Visible success: The selected illustration’s size controls show Width 5.80 cm and Height 3.60 cm.

#### Demonstration 3

- Skill: `af2d657a-e6b3-4c6a-9f67-9e3ed015974c.skill-01`
- Intent: Change only the lower-left Slide 2 checklist callout’s font family to Liberation Sans.
- Efficiency: Enter text-editing mode in the callout and select its full text before entering the requested font family in the font-name control.
- Visible success: “Morning Walk Checklist” displays in Liberation Sans while its neighboring title and checklist items retain their original font formatting.

#### Demonstration 4

- Skill: `9ec204e4-f0a3-42f8-8458-b772a6797cab.skill-01`
- Intent: Prepare the two working slides for one shared background update.
- Efficiency: Select one target thumbnail and Ctrl-click the other target thumbnail so the shared background change can be applied once.
- Visible success: Slides 2 and 3 are simultaneously highlighted in the Slides pane before the pale-mint background is applied, and both slides receive #E5F1E8.

Recording start: Open the supplied three-slide Community Garden Field Brief in Normal view with no multi-slide selection active.

Recording end: Slides 2 and 3 share pale-mint #E5F1E8 backgrounds; the Slide 2 illustration is 5.80 cm by 3.60 cm; the specified Slide 2 callout is Liberation Sans; and the Slide 3 header row contains the four requested labels.

Allowed variation: Equivalent LibreOffice controls and navigation paths are acceptable, provided the specified slide selection, background colors, table text, image dimensions, and isolated font-family change are achieved.

### 中文详细参考方案

> 以下是一个可以参考的操作 guide。标注者可以根据实际 LibreOffice 界面采用等价操作。

本指南在 LibreOffice Impress 的英文界面中完成 Community Garden Field Brief 的四项定向更新：同时为第 2、3 张幻灯片应用浅薄荷色背景；调整第 2 张的既有花坛插图尺寸；仅修改左下角提示文字的字体；以及连续替换第 3 张表格的四个表头。除这些目标外，不修改第 1 张、表格正文、其他文字、形状或对象位置。

#### 启动后的初始状态检查

- 确认演示文稿处于 Normal view，左侧 `Slides` 窗格可见三张缩略图，且开始时没有两张幻灯片同时高亮。
- 查看缩略图：Slide 1、Slide 2、Slide 3 起初均为象牙色背景；Slide 1 是封面，后续操作不应改变它。
- 单击 Slide 2 缩略图只切换当前页面，不要误把它当作对象选择。确认页面中有花坛插图，以及左下角卡片中的文字“Morning Walk Checklist”。
- 单击 Slide 3 缩略图确认有一张任务表；其首行从左至右初始可见“Bed”、“Window”、“Guide”、“Gear”。不要预先改动表格正文。

#### 第 1 步：同时选中两张工作幻灯片并设置共享背景

1. 在左侧 `Slides` 窗格中，先单击 Slide 2 的缩略图；这是选中幻灯片缩略图，不是在画布上选中对象。按住 `Ctrl` 并单击 Slide 3 的缩略图。两张缩略图都呈高亮状态即表示多选成功。
2. 在两张缩略图仍同时高亮时，打开右侧 `Properties` 侧边栏的 `Slide` 区域，并在 `Background` 中选择颜色填充。不同版本中也可使用 `Format` > `Slide Properties...` 打开相应的背景设置；关键是不要在只选中单张幻灯片时应用。
3. 将背景颜色设为 `#E5F1E8`。若颜色选择器提供十六进制输入，则输入 `E5F1E8`；若只提供 RGB 组件，则设为 R `229`、G `241`、B `232`，然后用 `OK` 或 `Apply` 确认。
4. 可接受的结果是：Slide 2 与 Slide 3 都变为同一种淡薄荷绿，而 Slide 1 仍是象牙色，无需再调整。若只有当前页改变，说明多选已丢失：重新在 `Slides` 窗格中先选 Slide 2、再用 `Ctrl` 选 Slide 3，然后重新应用该背景。

- 对应 skills：`9ec204e4-f0a3-42f8-8458-b772a6797cab.skill-01`
- 高效操作：先构建 Slide 2 和 Slide 3 的 `Ctrl` 多选，再一次性应用背景，避免逐页设置而产生颜色不一致。
- 完成标志：左侧 Slide 2、Slide 3 缩略图均显示浅薄荷色 `#E5F1E8` 背景；Slide 1 缩略图仍显示原有象牙色 `#FFFDF7`。

#### 第 2 步：将 Slide 2 花坛插图设为精确尺寸

1. 单击 Slide 2 缩略图，使其成为当前页。然后在画布上单击花坛插图的边缘，直到只出现该插图的选择边框和控制点；这叫选择对象，不要双击进入文字编辑，也不要选中图片旁的说明文字。
2. 可接受的结果是尺寸控件已显示 `Width` 为 `5.80 cm`、`Height` 为 `3.60 cm`，此时无需调整。若尺寸不符，右键已选插图并选择 `Position and Size...`，或在 `Properties` 侧边栏打开 `Position and Size`。
3. 在 `Position and Size` 控制中，如有 `Keep ratio`，先取消勾选它，否则无法同时得到指定的宽和高。只修改 `Width` 与 `Height`，不要修改位置字段。将 `Width` 替换为 `5.80 cm`，按 `Tab` 移至 `Height`，输入 `3.60 cm`，再按 `Enter` 或点击 `OK` 应用。
4. 检查插图仍是同一幅花坛图且没有被裁切、替换或移动到其他区域。若插图的尺寸正确但视觉位置异常，可重新打开 `Position and Size...`，仅恢复原有的 `Position` 数值，不改动已设定的 `Width`、`Height`。

- 对应 skills：`c82632a4-56b6-4db4-9dd1-3820ee3388e4.skill-02`
- 高效操作：在同一个尺寸控件中先填写 `Width`，再用 `Tab` 直接跳到 `Height`；不要通过拖拽控制点猜测厘米值。
- 完成标志：选中 garden-bed illustration 时，其尺寸区域明确显示 `Width` 为 `5.80 cm`、`Height` 为 `3.60 cm`；Slide 2 的其他对象仍保持原有内容。

#### 第 3 步：仅将左下角提示文字改为 Liberation Sans

1. 仍在 Slide 2，定位左下角卡片内的“Morning Walk Checklist”。先单击文字对象的边框可选中整个文本对象；随后再次单击文字，或双击文字，使插入光标出现在文字中。这一步是进入文本编辑模式，不能只停留在对象边框选择状态。
2. 当光标确实在该文字对象内时按 `Ctrl+A`，应只高亮该对象内的“Morning Walk Checklist”。如果 `Ctrl+A` 选中了整张幻灯片或多个对象，先按 `Esc`，再次在该文字上双击并确认有文本光标后再按 `Ctrl+A`。
3. 在格式工具栏的 `Font Name` 输入框中输入 `Liberation Sans`，然后按 `Enter` 应用。不要在没有选中文本时修改该框，因为那样可能只影响之后新输入的文字。
4. 可接受的结果是卡片中的“Morning Walk Checklist”以 Liberation Sans 显示，而相邻标题、卡片外说明和 checklist 条目保持原来的字体，无需再调整。若邻近文字也变成了该字体，立即在邻近对象中进入文本编辑模式，选中其文字并从 `Font Name` 恢复其原有字体；然后只对目标 callout 重新执行本步骤。

- 对应 skills：`af2d657a-e6b3-4c6a-9f67-9e3ed015974c.skill-01`
- 高效操作：先进入目标文字的编辑状态、再用 `Ctrl+A` 选中该对象内全部文字，可避免改变整个卡片或其他文本对象的格式。
- 完成标志：左下角卡片仍显示完全相同的文字“Morning Walk Checklist”，但该文字的字体为 Liberation Sans；邻近标题和列表文字外观未被连带修改。

#### 第 4 步：使用 Tab 连续替换 Slide 3 表头四个单元格

1. 单击 Slide 3 缩略图。单击表格首行最左侧、当前写有“Bed”的单元格内部，使文本插入光标位于该单元格文字中；这不是只选中整张表的对象边框。必要时先单击表格，再单击“Bed”文字以进入单元格的文本编辑模式。
2. 在第一个单元格内按 `Ctrl+A` 选中该单元格当前文字，输入 `Area`。按 `Tab`，让文本光标移动到右侧第二个表头单元格。
3. 在第二个单元格中按 `Ctrl+A`，输入 `Visit time`，再按 `Tab`。在第三个单元格中按 `Ctrl+A`，输入 `Coordinator`，再按 `Tab`。
4. 在第四个单元格中按 `Ctrl+A`，输入 `Materials`。最后一个单元格完成后不要再按 `Tab`，以免继续进入其他单元格或产生不必要的结构变化。
5. 可接受的结果是表头从左到右恰为 `Area`、`Visit time`、`Coordinator`、`Materials`，且表格的行列结构和正文未变，无需调整。若 `Tab` 没有进入相邻表头，而是离开表格，说明光标不在单元格编辑模式：撤销误操作（如有），重新单击首个单元格文字内部，再按上述顺序完成替换。

- 对应 skills：`5cfb9197-e72b-454b-900e-c06b0c802b40.skill-01`
- 高效操作：在第一个表头单元格内保持文本光标，并用 `Tab` 横向前进；这样无需逐个用鼠标重新定位四个相邻单元格。
- 完成标志：Slide 3 表格首行依次显示“Area”、“Visit time”、“Coordinator”、“Materials”；所有表格正文值仍与编辑前一致。

#### 第 5 步：保存前进行页面级核对

1. 依次单击 Slide 1、Slide 2、Slide 3 的缩略图进行查看；这里是选择单张幻灯片缩略图进行核对，不要移动任何缩略图或改变其顺序。
2. 确认 Slide 1 仍为 `#FFFDF7` 象牙背景，封面文字、图形和布局未发生变化。确认 Slide 2 为 `#E5F1E8`，花坛插图尺寸已为 `5.80 cm` × `3.60 cm`，并且只有“Morning Walk Checklist”使用 Liberation Sans。
3. 确认 Slide 3 为 `#E5F1E8`，表头完全符合目标文字且正文行、页脚注释和侧边标记未改动。完成核对后使用 `File` > `Save`，或按 `Ctrl+S` 保存。

- 对应 skills：无；这是准备或检查步骤。
- 高效操作：从缩略图逐页检查能快速发现背景误应用到 Slide 1、表格正文被误选或对象被误移动等问题。
- 完成标志：三张缩略图顺序仍为 Slide 1、Slide 2、Slide 3；只有规定的两页背景、Slide 2 两项对象属性和 Slide 3 四个表头发生变化。

#### 最终结果检查

- Slide 1 仍保持象牙色 `#FFFDF7` 背景，且封面内容未改动。
- Slide 2 和 Slide 3 的背景均为相同的浅薄荷色 `#E5F1E8`；没有其他页面被改成该颜色。
- Slide 2 的 garden-bed illustration 在 `Position and Size` 中为 `Width` `5.80 cm`、`Height` `3.60 cm`；插图仍是原有花坛图。
- Slide 2 左下角文字仍精确为“Morning Walk Checklist”，其字体为 Liberation Sans；邻近标题和 checklist 条目没有被改字体。
- Slide 3 表头从左到右精确为“Area”、“Visit time”、“Coordinator”、“Materials”，表格正文、其他文本、形状和对象位置保持不变。
- 确认 `Slides` 窗格仍只有三张幻灯片，顺序未变化，并已通过 `File` > `Save` 或 `Ctrl+S` 保存。

## Source-task similarity review

| Measure | Maximum | Most similar source task |
| --- | ---: | --- |
| Lexical sequence similarity | 0.222222 | 04578141-1d42-4146-b9cf-6fab4ce5fd74 |
| Semantic cosine similarity | 0.512099 | 9cf05d24-6bd9-4dae-8967-f67d88f5d38a |

Similarity scores are reviewer aids, not automatic acceptance thresholds. Inspect the contributing source tasks and their complete ordered actions below.

### Source task `5cfb9197-e72b-454b-900e-c06b0c802b40`

Original instruction:

> Change the first row of table to "T1","T2","T3","T4" on slide 4.

Required skills derived from this source task:

- **Overwrite text in consecutive table cells using Tab** — `5cfb9197-e72b-454b-900e-c06b0c802b40.skill-01`

Complete ordered single-action sequence:

| Action | Related required skill | Original single action |
| ---: | --- | --- |
| 0 |  | <code>`CLICK` Slide 4</code> |
| 1 | <strong>★ Overwrite text in consecutive table cells using Tab</strong><br><code>5cfb9197-e72b-454b-900e-c06b0c802b40.skill-01</code> | <strong><code>`CLICK` Table 1</code></strong> |
| 2 | <strong>★ Overwrite text in consecutive table cells using Tab</strong><br><code>5cfb9197-e72b-454b-900e-c06b0c802b40.skill-01</code> | <strong><code>`HOTKEY` ctrl-A</code></strong> |
| 3 | <strong>★ Overwrite text in consecutive table cells using Tab</strong><br><code>5cfb9197-e72b-454b-900e-c06b0c802b40.skill-01</code> | <strong><code>`TYPING` T1</code></strong> |
| 4 | <strong>★ Overwrite text in consecutive table cells using Tab</strong><br><code>5cfb9197-e72b-454b-900e-c06b0c802b40.skill-01</code> | <strong><code>`PRESS` tab</code></strong> |
| 5 | <strong>★ Overwrite text in consecutive table cells using Tab</strong><br><code>5cfb9197-e72b-454b-900e-c06b0c802b40.skill-01</code> | <strong><code>`HOTKEY` ctrl-A</code></strong> |
| 6 | <strong>★ Overwrite text in consecutive table cells using Tab</strong><br><code>5cfb9197-e72b-454b-900e-c06b0c802b40.skill-01</code> | <strong><code>`TYPING` T2</code></strong> |
| 7 | <strong>★ Overwrite text in consecutive table cells using Tab</strong><br><code>5cfb9197-e72b-454b-900e-c06b0c802b40.skill-01</code> | <strong><code>`PRESS` tab</code></strong> |
| 8 | <strong>★ Overwrite text in consecutive table cells using Tab</strong><br><code>5cfb9197-e72b-454b-900e-c06b0c802b40.skill-01</code> | <strong><code>`HOTKEY` ctrl-A</code></strong> |
| 9 | <strong>★ Overwrite text in consecutive table cells using Tab</strong><br><code>5cfb9197-e72b-454b-900e-c06b0c802b40.skill-01</code> | <strong><code>`TYPING` T3</code></strong> |
| 10 | <strong>★ Overwrite text in consecutive table cells using Tab</strong><br><code>5cfb9197-e72b-454b-900e-c06b0c802b40.skill-01</code> | <strong><code>`PRESS` tab</code></strong> |
| 11 | <strong>★ Overwrite text in consecutive table cells using Tab</strong><br><code>5cfb9197-e72b-454b-900e-c06b0c802b40.skill-01</code> | <strong><code>`HOTKEY` ctrl-A</code></strong> |
| 12 | <strong>★ Overwrite text in consecutive table cells using Tab</strong><br><code>5cfb9197-e72b-454b-900e-c06b0c802b40.skill-01</code> | <strong><code>`TYPING` T4</code></strong> |

### Source task `9ec204e4-f0a3-42f8-8458-b772a6797cab`

Original instruction:

> Please duplicate the last two slides and insert the copies in alternating order, so the sequence becomes: original slide A, original slide B, then duplicated slide A, duplicated slide B.

Required skills derived from this source task:

- **Select multiple slides in the Slides pane** — `9ec204e4-f0a3-42f8-8458-b772a6797cab.skill-01`

Complete ordered single-action sequence:

| Action | Related required skill | Original single action |
| ---: | --- | --- |
| 0 |  | <code>`SCROLL` down on the slides pane</code> |
| 1 | <strong>★ Select multiple slides in the Slides pane</strong><br><code>9ec204e4-f0a3-42f8-8458-b772a6797cab.skill-01</code> | <strong><code>`CLICK` slide 23</code></strong> |
| 2 | <strong>★ Select multiple slides in the Slides pane</strong><br><code>9ec204e4-f0a3-42f8-8458-b772a6797cab.skill-01</code> | <strong><code>`KEY_DOWN` Ctrl</code></strong> |
| 3 | <strong>★ Select multiple slides in the Slides pane</strong><br><code>9ec204e4-f0a3-42f8-8458-b772a6797cab.skill-01</code> | <strong><code>`CLICK` slide 24</code></strong> |
| 4 | <strong>★ Select multiple slides in the Slides pane</strong><br><code>9ec204e4-f0a3-42f8-8458-b772a6797cab.skill-01</code> | <strong><code>`KEY_UP` Ctrl</code></strong> |
| 5 |  | <code>`RIGHT_CLICK` the selection</code> |
| 6 |  | <code>`CLICK` Duplicate slides</code> |

### Source task `af2d657a-e6b3-4c6a-9f67-9e3ed015974c`

Original instruction:

> In the first slide, insert the title "Happy Family" and make the font style "Microsoft JhengHei".

Required skills derived from this source task:

- **Change the font family of selected text** — `af2d657a-e6b3-4c6a-9f67-9e3ed015974c.skill-01`

Complete ordered single-action sequence:

| Action | Related required skill | Original single action |
| ---: | --- | --- |
| 0 |  | <code>`CLICK` &#x27;Click to add text&#x27;</code> |
| 1 |  | <code>`TYPING` &#x27;Happy Family&#x27;</code> |
| 2 | <strong>★ Change the font family of selected text</strong><br><code>af2d657a-e6b3-4c6a-9f67-9e3ed015974c.skill-01</code> | <strong><code>`HOTKEY` ctrl-a</code></strong> |
| 3 | <strong>★ Change the font family of selected text</strong><br><code>af2d657a-e6b3-4c6a-9f67-9e3ed015974c.skill-01</code> | <strong><code>`TRIPLE_CLICK` font text field</code></strong> |
| 4 | <strong>★ Change the font family of selected text</strong><br><code>af2d657a-e6b3-4c6a-9f67-9e3ed015974c.skill-01</code> | <strong><code>`TYPING` &#x27;Microsoft JhengHei&#x27;</code></strong> |

### Source task `c82632a4-56b6-4db4-9dd1-3820ee3388e4`

Original instruction:

> Add an image "none.png" on the Desktop to slide 2 with 1cm*1cm size.

Required skills derived from this source task:

- **Set an image to exact width and height** — `c82632a4-56b6-4db4-9dd1-3820ee3388e4.skill-02`

Complete ordered single-action sequence:

| Action | Related required skill | Original single action |
| ---: | --- | --- |
| 0 |  | <code>`CLICK` slide 2</code> |
| 1 |  | <code>`CLICK` insert image icon</code> |
| 2 |  | <code>`CLICK` Desktop</code> |
| 3 |  | <code>`CLICK` none.png</code> |
| 4 |  | <code>`PRESS` enter</code> |
| 5 | <strong>★ Set an image to exact width and height</strong><br><code>c82632a4-56b6-4db4-9dd1-3820ee3388e4.skill-02</code> | <strong><code>`CLICK` position and size dropdown</code></strong> |
| 6 | <strong>★ Set an image to exact width and height</strong><br><code>c82632a4-56b6-4db4-9dd1-3820ee3388e4.skill-02</code> | <strong><code>`SCROLL` down to width text box</code></strong> |
| 7 | <strong>★ Set an image to exact width and height</strong><br><code>c82632a4-56b6-4db4-9dd1-3820ee3388e4.skill-02</code> | <strong><code>`TRIPLE_CLICK` width text box</code></strong> |
| 8 | <strong>★ Set an image to exact width and height</strong><br><code>c82632a4-56b6-4db4-9dd1-3820ee3388e4.skill-02</code> | <strong><code>`TYPING` 1cm</code></strong> |
| 9 | <strong>★ Set an image to exact width and height</strong><br><code>c82632a4-56b6-4db4-9dd1-3820ee3388e4.skill-02</code> | <strong><code>`PRESS` tab</code></strong> |
| 10 | <strong>★ Set an image to exact width and height</strong><br><code>c82632a4-56b6-4db4-9dd1-3820ee3388e4.skill-02</code> | <strong><code>`TYPING` 1cm</code></strong> |
| 11 | <strong>★ Set an image to exact width and height</strong><br><code>c82632a4-56b6-4db4-9dd1-3820ee3388e4.skill-02</code> | <strong><code>`PRESS` enter</code></strong> |

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
