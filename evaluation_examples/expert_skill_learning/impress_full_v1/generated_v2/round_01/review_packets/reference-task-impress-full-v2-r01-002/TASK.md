# Harbor Air Lab: Dawn Sampling Brief

- Reference task: `reference-task-impress-full-v2-r01-002`
- Application: `libreoffice_impress`
- Review decision: `pending`

## Task instruction

Finalize the Harbor Air Lab briefing: on the “Field Snapshot” slide, move the coastal landscape illustration from the left panel into the right-side image frame, make the heading “FIELD SNAPSHOT” bold, and right-align the source line beneath the image. On the following “Next Measurement” slide, center the text in the closing callout, “Sampling begins at first light.” Keep all wording and other slide elements unchanged.

## Required skills

### 1. Apply bold formatting to text in a slide text box

Skill ID: `7dbc52a6-11e0-4c9a-a2cb-1e36cfda80d8.skill-01`

Procedure:

1. Select the text box whose text should be formatted, entering text-editing mode if necessary so the formatting applies to its characters rather than the object border.
2. Use Ctrl+B to toggle bold formatting for the selected text or for subsequently entered text. For example, click inside a slide title and press Ctrl+B to make the title bold.

Efficiency tip: Use Ctrl+B rather than opening the formatting toolbar; verify that the text caret or selected text is active so you do not merely select the text box object.

Source task: `7dbc52a6-11e0-4c9a-a2cb-1e36cfda80d8`

Source instruction: On page 2, add a note same to the title into the slide. Make the font of title bold.

Directly referenced source actions:

- Action 1: <code>`CLICK` &#x27;Team Members&#x27; box in the slide.</code>
- Action 2: <code>`HOTKEY` Ctrl-B</code>

### 2. Move a selected image by dragging

Skill ID: `2b94c692-6abb-48ae-ab0b-b3e8a19cb340.skill-01`

Procedure:

1. Select the slide containing the image in the Slides pane, for example Slide 2.
2. Move the pointer over the image and drag it to the desired position on the slide canvas, such as toward the right side.
3. Release the mouse button when the image is positioned correctly.

Efficiency tip: Drag the image by its interior rather than a resize handle, and use alignment guides if they appear to place it accurately in one movement.

Source task: `2b94c692-6abb-48ae-ab0b-b3e8a19cb340`

Source instruction: Move the image to the right side on Slide 2.

Directly referenced source actions:

- Action 0: <code>`CLICK` Slide 2.</code>
- Action 1: <code>`MOVE_TO` the image</code>
- Action 2: <code>`DRAG_TO` the right side of the slide</code>

### 3. Align paragraph text to the right in a text box

Skill ID: `08aced46-45a2-48d7-993b-ed3fb5b32302.skill-01`

Procedure:

1. Enter text-editing mode in the target text box, for example by clicking inside its title text.
2. Click the Right Align toolbar icon to align the current paragraph to the right edge of the text box.

Efficiency tip: Place the text cursor in the intended paragraph before using Right Align; this avoids changing alignment on a different object or paragraph.

Source task: `08aced46-45a2-48d7-993b-ed3fb5b32302`

Source instruction: Give the slide 2 the right aligned title, "Note".

Directly referenced source actions:

- Action 1: <code>`CLICK` the title text box</code>
- Action 3: <code>`CLICK` right align icon.</code>

### 4. Align paragraph text within a selected text box

Skill ID: `05dd4c1d-c489-4c85-8389-a7836c4f0567.skill-01`

Procedure:

1. In the Slides pane, select the slide containing the text box to format.
2. Click inside the text box to enter text-editing mode, then use Ctrl+A to select its text.
3. Click the desired paragraph-alignment control in the toolbar, such as Right Align, Center Align, or Left Align.
4. For example, select the text in a text box and click Center Align to center all selected paragraphs within that box.

Efficiency tip: Select the text directly with Ctrl+A after entering the text box, then apply one alignment command; this avoids changing alignment on the wrong object or only affecting an insertion point.

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

### slide-03

![slide-03.png](artifact/previews/slide-03.png)

## Operator guide

### Existing operation-intent guide

#### Demonstration 1

- Skill: `7dbc52a6-11e0-4c9a-a2cb-1e36cfda80d8.skill-01`
- Intent: Apply bold character formatting to the slide 2 heading only.
- Efficiency: Enter text-editing mode in the heading and use Ctrl+B with the heading text selected or the insertion point in that text.
- Visible success: “FIELD SNAPSHOT” has a visibly heavier weight while its wording, position, and color remain unchanged.

#### Demonstration 2

- Skill: `2b94c692-6abb-48ae-ab0b-b3e8a19cb340.skill-01`
- Intent: Relocate the slide 2 coastal landscape illustration into the outlined destination frame on the right.
- Efficiency: Drag from the image interior rather than a sizing handle; use the visible frame edges as the placement reference.
- Visible success: The coastal landscape illustration occupies the right-side frame area, and the left panel no longer contains the illustration.

#### Demonstration 3

- Skill: `08aced46-45a2-48d7-993b-ed3fb5b32302.skill-01`
- Intent: Right-align the slide 2 source citation paragraph.
- Efficiency: Place the text cursor in the source paragraph before applying Right Align.
- Visible success: The citation’s right edge aligns with the right edge of its text box beneath the image frame.

#### Demonstration 4

- Skill: `05dd4c1d-c489-4c85-8389-a7836c4f0567.skill-01`
- Intent: Center the paragraph in the slide 3 closing callout.
- Efficiency: Enter the callout text box, select its text, and apply Center Align once.
- Visible success: “Sampling begins at first light.” is centered horizontally in the pale-blue callout area.

Recording start: Open the supplied three-slide presentation in normal slide editing view with all specified incomplete states visible.

Recording end: Slide 2 has the image in the right frame, a bold heading, and a right-aligned source line; slide 3 has a centered closing callout.

Allowed variation: Minor differences in the precise image drop point are acceptable if the image is clearly positioned within the right-side outlined frame. The requested text formatting and paragraph alignments must remain exact.

### 中文详细参考方案

> 以下是一个可以参考的操作 guide。标注者可以根据实际 LibreOffice 界面采用等价操作。

本指南完成三页 Harbor Air Lab 简报中的四项局部编辑：在“Field Snapshot”页将海岸插图移入右侧框、将标题加粗并将图源行右对齐；然后在“Next Measurement”页居中结束提示文字。除指定对象的格式或位置外，不修改任何文字、主题颜色、对象或幻灯片顺序。

#### 启动后的初始状态检查

- 确认正在普通编辑视图中打开三页演示文稿，并且左侧 `Slides` 窗格可见三张缩略图。
- 在第 2 张缩略图上单击以选择幻灯片；这只是选择幻灯片，不是选择画布对象。确认可见左侧面板中的海岸景观插图、右侧空的描边图像框、常规字重的“FIELD SNAPSHOT”，以及图框下方左对齐的来源行。
- 在第 3 张缩略图上单击以选择幻灯片，确认浅蓝色提示区域中的“Sampling begins at first light.” 当前在其文本区域内左对齐。随后重新选择第 2 张缩略图开始编辑。
- 如第 2 张中的插图已经清楚地位于右侧描边框内、标题已加粗或来源行已靠右，第 2 张对应部分可不调整；如果与这些可见结果不一致，再按下面相应步骤修复，且不要改动文字内容。

#### 第 1 步：将“FIELD SNAPSHOT”标题设为粗体

1. 保持第 2 张幻灯片缩略图处于选中状态。在画布上单击“FIELD SNAPSHOT”文字的字符内部，进入文本编辑模式；此时应出现文本光标或文字编辑状态，而不只是整个文本框的外框。
2. 按 `Ctrl+A`，仅选中该文本框中的标题字符，然后按 `Ctrl+B`。不要在仅选中对象边框时按快捷键，因为那不会可靠地将字符设为粗体。
3. 单击文本框外的空白画布以退出文本编辑模式并观察字重。标题文字、颜色和位置保持原样即为正确。如果标题仍显得常规字重，重新单击文字内部、用 `Ctrl+A` 选中标题后再按一次 `Ctrl+B`；如果已经是粗体，则不要再次按 `Ctrl+B`，以免切回常规字重。

- 对应 skills：`7dbc52a6-11e0-4c9a-a2cb-1e36cfda80d8.skill-01`
- 高效操作：用 `Ctrl+A` 前务必先在标题字符内部单击；这样选中的是该文本框的文字，而不是幻灯片上的全部对象。
- 完成标志：“FIELD SNAPSHOT”明显比原先更粗，而措辞、颜色、换行和文本框位置均未改变。

#### 第 2 步：把海岸景观插图移至右侧图像框

1. 在第 2 张画布左侧面板中，单击海岸景观插图的可见图像内容一次，使选中的是图片对象：应看到图片自身的选择边框和控制点。这不同于单击左侧的幻灯片缩略图，也不要选中右侧空图框的描边形状。
2. 从图片内部（不要从角部或边缘的缩放控制点）按住鼠标，将图片拖向右侧描边图像框的内部；以该框的边缘为落点参照，松开鼠标。
3. 可接受的结果是插图清楚地占据右侧描边框区域、左侧原位置不再有插图，且插图没有压住标题或下方来源行。如果已经如此，无需移动。若图片只部分落在框外或遮挡了来源行，重新选中图片的边框并从其内部小幅拖动，使其完全清楚地落在右侧框区域。若右侧框的描边意外显示在图片上方或图片被框遮住而影响可见性，在不改变图片位置的前提下，选中相应对象后使用 `Format` > `Arrange` 调整层叠顺序，直到图片在框区域内清楚可见，同时保留框的视觉边界。

- 对应 skills：`2b94c692-6abb-48ae-ab0b-b3e8a19cb340.skill-01`
- 高效操作：拖动时抓住图片中央的图像内容，避免拖到控制点而触发缩放；一次拖到右框中央通常最稳定。
- 完成标志：海岸景观插图位于右侧图像框区域内，左侧面板不再保留该插图，标题和图框下方文字均未被覆盖。

#### 第 3 步：将第 2 张的来源行右对齐

1. 在第 2 张右侧图像框下方，单击来源行文字的字符内部以进入文本编辑模式。此时出现插入光标即可；不要只选中文本框的对象边框。
2. 将光标放在该唯一来源段落中，按 `Ctrl+R`，把当前段落设为右对齐。无需改写、删除或添加任何字符。
3. 退出文本编辑模式后查看来源行：其最右端应与来源文本框的右边界对齐。如果来源行已经满足这个可见结果，不需要重复操作；若仍从左边开始，重新在该行文字内部单击并按 `Ctrl+R`。若误将其他段落或对象改动，可立即按 `Ctrl+Z` 撤销误操作，再只在来源行内执行右对齐。

- 对应 skills：`08aced46-45a2-48d7-993b-ed3fb5b32302.skill-01`
- 高效操作：来源行只有一个段落时，只需在该行放置文本光标后按 `Ctrl+R`，无需拖选整行文字。
- 完成标志：图像框下方来源行的右端贴齐其文本框右侧，文字内容、字体颜色及垂直位置没有变化。

#### 第 4 步：居中第 3 张结束提示的文字

1. 在 `Slides` 窗格单击第 3 张缩略图以切换到“Next Measurement”页；这是选择幻灯片。确认第 2 张缩略图仍显示其已完成的右侧插图布局。
2. 在浅蓝色提示区域内单击“Sampling begins at first light.”的字符，进入该文本框的文本编辑模式，而不是仅选中浅蓝色背景形状或文本框边框。按 `Ctrl+A`，此时只选中该文本框中的这句文字。
3. 按 `Ctrl+E` 将选中段落居中，然后单击画布空白处退出编辑。可接受的结果是这句话在浅蓝色提示区域中水平居中。如果它已经居中，无需调整；若仍偏左或偏右，重新进入该文本框，按 `Ctrl+A` 后再按 `Ctrl+E`。
4. 若发现移动的是提示框背景而不是改变文字对齐，按 `Ctrl+Z` 恢复，然后务必直接单击句子字符进入文本编辑模式，再执行居中。

- 对应 skills：`05dd4c1d-c489-4c85-8389-a7836c4f0567.skill-01`
- 高效操作：先进入文字编辑再用 `Ctrl+A`，可避免选中整张幻灯片或提示框背景；一次 `Ctrl+E` 即可作用于该文本框内选中的段落。
- 完成标志：“Sampling begins at first light.”在浅蓝色 callout 区域内水平居中，句号、措辞、背景形状和其余流程元素均保持不变。

#### 最终结果检查

- 检查 `Slides` 窗格仍只有原来的三张幻灯片，顺序未变化；封面第 1 张没有被编辑。
- 选择第 2 张缩略图，确认海岸景观插图清楚位于右侧描边图像框内，左侧区域没有该插图；“FIELD SNAPSHOT”为粗体；图框下方来源行右对齐。确认上下文文字、状态芯片、主题颜色及其他对象未改变。
- 选择第 3 张缩略图，确认“Sampling begins at first light.”在浅蓝色提示区域内水平居中。确认标题、三个步骤形状、提示背景和所有原有文字均未改动。
- 如某一项不符合，返回对应幻灯片，仅重做该对象的局部操作；不要通过重新创建文本框、替换图片或调整整个幻灯片来修复。

## Source-task similarity review

| Measure | Maximum | Most similar source task |
| --- | ---: | --- |
| Lexical sequence similarity | 0.274583 | a434992a-89df-4577-925c-0c58b747f0f4 |
| Semantic cosine similarity | 0.525306 | 08aced46-45a2-48d7-993b-ed3fb5b32302 |

Similarity scores are reviewer aids, not automatic acceptance thresholds. Inspect the contributing source tasks and their complete ordered actions below.

### Source task `05dd4c1d-c489-4c85-8389-a7836c4f0567`

Original instruction:

> Align the first textbox on slide 3 to the right, on slide 4 to the center, and on slide 5 to the left. Ensure that the alignment is applied correctly to each respective slide.

Required skills derived from this source task:

- **Align paragraph text within a selected text box** — `05dd4c1d-c489-4c85-8389-a7836c4f0567.skill-01`

Complete ordered single-action sequence:

| Action | Related required skill | Original single action |
| ---: | --- | --- |
| 0 | <strong>★ Align paragraph text within a selected text box</strong><br><code>05dd4c1d-c489-4c85-8389-a7836c4f0567.skill-01</code> | <strong><code>`CLICK` Slide 3</code></strong> |
| 1 | <strong>★ Align paragraph text within a selected text box</strong><br><code>05dd4c1d-c489-4c85-8389-a7836c4f0567.skill-01</code> | <strong><code>`CLICK` &#x27;HELLO&#x27;</code></strong> |
| 2 | <strong>★ Align paragraph text within a selected text box</strong><br><code>05dd4c1d-c489-4c85-8389-a7836c4f0567.skill-01</code> | <strong><code>`HOTKEY` ctrl-A</code></strong> |
| 3 | <strong>★ Align paragraph text within a selected text box</strong><br><code>05dd4c1d-c489-4c85-8389-a7836c4f0567.skill-01</code> | <strong><code>`CLICK` right-align icon</code></strong> |
| 4 | <strong>★ Align paragraph text within a selected text box</strong><br><code>05dd4c1d-c489-4c85-8389-a7836c4f0567.skill-01</code> | <strong><code>`CLICK` Slide 4</code></strong> |
| 5 | <strong>★ Align paragraph text within a selected text box</strong><br><code>05dd4c1d-c489-4c85-8389-a7836c4f0567.skill-01</code> | <strong><code>`CLICK` &#x27;WRITE&#x27;</code></strong> |
| 6 | <strong>★ Align paragraph text within a selected text box</strong><br><code>05dd4c1d-c489-4c85-8389-a7836c4f0567.skill-01</code> | <strong><code>`HOTKEY` ctrl-A</code></strong> |
| 7 | <strong>★ Align paragraph text within a selected text box</strong><br><code>05dd4c1d-c489-4c85-8389-a7836c4f0567.skill-01</code> | <strong><code>`CLICK` center-align icon</code></strong> |
| 8 | <strong>★ Align paragraph text within a selected text box</strong><br><code>05dd4c1d-c489-4c85-8389-a7836c4f0567.skill-01</code> | <strong><code>`CLICK` Slide 5</code></strong> |
| 9 | <strong>★ Align paragraph text within a selected text box</strong><br><code>05dd4c1d-c489-4c85-8389-a7836c4f0567.skill-01</code> | <strong><code>`CLICK` &#x27;WRITE&#x27;</code></strong> |
| 10 | <strong>★ Align paragraph text within a selected text box</strong><br><code>05dd4c1d-c489-4c85-8389-a7836c4f0567.skill-01</code> | <strong><code>`HOTKEY` ctrl-A</code></strong> |
| 11 | <strong>★ Align paragraph text within a selected text box</strong><br><code>05dd4c1d-c489-4c85-8389-a7836c4f0567.skill-01</code> | <strong><code>`CLICK` left-align icon under paragraph section</code></strong> |

### Source task `08aced46-45a2-48d7-993b-ed3fb5b32302`

Original instruction:

> Give the slide 2 the right aligned title, "Note".

Required skills derived from this source task:

- **Align paragraph text to the right in a text box** — `08aced46-45a2-48d7-993b-ed3fb5b32302.skill-01`

Complete ordered single-action sequence:

| Action | Related required skill | Original single action |
| ---: | --- | --- |
| 0 |  | <code>`CLICK` Slide 2</code> |
| 1 | <strong>★ Align paragraph text to the right in a text box</strong><br><code>08aced46-45a2-48d7-993b-ed3fb5b32302.skill-01</code> | <strong><code>`CLICK` the title text box</code></strong> |
| 2 |  | <code>`TYPING` &#x27;Note&#x27;</code> |
| 3 | <strong>★ Align paragraph text to the right in a text box</strong><br><code>08aced46-45a2-48d7-993b-ed3fb5b32302.skill-01</code> | <strong><code>`CLICK` right align icon.</code></strong> |

### Source task `2b94c692-6abb-48ae-ab0b-b3e8a19cb340`

Original instruction:

> Move the image to the right side on Slide 2.

Required skills derived from this source task:

- **Move a selected image by dragging** — `2b94c692-6abb-48ae-ab0b-b3e8a19cb340.skill-01`

Complete ordered single-action sequence:

| Action | Related required skill | Original single action |
| ---: | --- | --- |
| 0 | <strong>★ Move a selected image by dragging</strong><br><code>2b94c692-6abb-48ae-ab0b-b3e8a19cb340.skill-01</code> | <strong><code>`CLICK` Slide 2.</code></strong> |
| 1 | <strong>★ Move a selected image by dragging</strong><br><code>2b94c692-6abb-48ae-ab0b-b3e8a19cb340.skill-01</code> | <strong><code>`MOVE_TO` the image</code></strong> |
| 2 | <strong>★ Move a selected image by dragging</strong><br><code>2b94c692-6abb-48ae-ab0b-b3e8a19cb340.skill-01</code> | <strong><code>`DRAG_TO` the right side of the slide</code></strong> |

### Source task `7dbc52a6-11e0-4c9a-a2cb-1e36cfda80d8`

Original instruction:

> On page 2, add a note same to the title into the slide. Make the font of title bold.

Required skills derived from this source task:

- **Apply bold formatting to text in a slide text box** — `7dbc52a6-11e0-4c9a-a2cb-1e36cfda80d8.skill-01`

Complete ordered single-action sequence:

| Action | Related required skill | Original single action |
| ---: | --- | --- |
| 0 |  | <code>`CLICK` Slide 2</code> |
| 1 | <strong>★ Apply bold formatting to text in a slide text box</strong><br><code>7dbc52a6-11e0-4c9a-a2cb-1e36cfda80d8.skill-01</code> | <strong><code>`CLICK` &#x27;Team Members&#x27; box in the slide.</code></strong> |
| 2 | <strong>★ Apply bold formatting to text in a slide text box</strong><br><code>7dbc52a6-11e0-4c9a-a2cb-1e36cfda80d8.skill-01</code> | <strong><code>`HOTKEY` Ctrl-B</code></strong> |
| 3 |  | <code>`CLICK` &#x27;View&#x27; in the menu bar.&#x27;</code> |
| 4 |  | <code>`CLICK` &#x27;Notes&#x27; in the dropdown menu.</code> |
| 5 |  | <code>`CLICK` &#x27;Click to add notes&#x27;</code> |
| 6 |  | <code>`TYPING` &#x27;Team Members&#x27;</code> |

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
