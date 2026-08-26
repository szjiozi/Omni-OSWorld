# Neighborhood Night Market

- Reference task: `reference-task-impress-full-r01-002`
- Application: `libreoffice_impress`
- Review decision: `pending`

## Task instruction

Prepare the three-slide “Neighborhood Night Market” briefing for a council preview. Give the opening slide a Midnight Blue background and right-align its headline, “After-Dark Market Plan,” at 42 pt. Set the closing slide background to Pale Sage so it reads as a distinct action slide. Keep the middle slide unchanged; its 24 pt schedule text is included as a readable size reference for the deck’s existing body style.

## Required skills

### 1. Set a slide background color

Skill ID: `841b50aa-df53-47bd-a73a-22d3a9f73160.skill-01`

Procedure:

1. Open the slide background formatting control, such as the Background drop-down in the slide properties area.
2. Choose the color background option, open its color palette, and select a desired color (for example, a purple swatch).
3. The selected color is applied as the background for the current slide.

Efficiency tip: Select the slide before opening background controls so the color applies to the intended slide rather than requiring later correction.

Source task: `841b50aa-df53-47bd-a73a-22d3a9f73160`

Source instruction: Add a note "APP" into the slide and give the slide a purple background color.

Directly referenced source actions:

- Action 0: <code>`CLICK` background dropdown</code>
- Action 1: <code>`CLICK` color</code>
- Action 2: <code>`CLICK` color dropdown</code>
- Action 3: <code>`CLICK` purple (2nd row, 7th from right)</code>

### 2. Set font size for text in a text box

Skill ID: `3161d64e-3120-47b4-aaad-6a764a92493b.skill-01`

Procedure:

1. Click inside the target text box to enter text-editing mode, rather than merely selecting the shape frame.
2. Select the text whose size should change; a triple-click can select the paragraph in a text box when appropriate.
3. Click the Font Size box on the Formatting toolbar, replace its current value with a point size such as 60 pt, and press Enter to apply it.
4. Repeat the same selection-and-Font-Size-box procedure for other text boxes or paragraphs that require different sizes, for example 28 pt.

Efficiency tip: After selecting a paragraph, type the desired point value directly into the Font Size box instead of searching the dropdown list; pressing Enter applies the value immediately.

Source task: `3161d64e-3120-47b4-aaad-6a764a92493b`

Source instruction: Make the first textbox font size 60 pt while the second 28 pt on slide 14.

Directly referenced source actions:

- Action 2: <code>`TRIPLE_CLICK` target audience</code>
- Action 3: <code>`TRIPLE_CLICK` font size text field</code>
- Action 4: <code>`TYPING` 60 pt</code>
- Action 5: <code>`PRESS` enter</code>
- Action 6: <code>`TRIPLE_CLICK` &#x27;Elaborate...&#x27;</code>
- Action 7: <code>`TRIPLE_CLICK` font size dropdown</code>
- Action 8: <code>`TYPING` 28 pt</code>
- Action 9: <code>`PRESS` enter</code>

### 3. Set a slide background color

Skill ID: `0a211154-fda0-48d0-9274-eaac4ce5486d.skill-01`

Procedure:

1. In the Slides pane, select the slide whose background you want to change.
2. In the right Sidebar's slide/background formatting controls, open the background color dropdown.
3. Choose the desired color, for example a yellow swatch. The selected slide's background updates.
4. Repeat the same background-color operation for other applicable slides; each slide can be formatted independently.

Efficiency tip: Keep the Sidebar open while working through several slides, then select each target slide and reuse the same color choice instead of reopening unrelated formatting dialogs.

Source task: `0a211154-fda0-48d0-9274-eaac4ce5486d`

Source instruction: Set the background color to yellow for any slide that contains one or more images of real people, and set the title of slide 2 as "Let's start".

Directly referenced source actions:

- Action 0: <code>`CLICK` Slide 3.</code>
- Action 1: <code>`CLICK` color dropdown in right sidebar</code>
- Action 2: <code>`CLICK` &#x27;yellow&#x27; (second row, first column)</code>
- Action 3: <code>`CLICK` Slide 4.</code>
- Action 4: <code>`CLICK` color dropdown in right sidebar</code>
- Action 5: <code>`CLICK` &#x27;yellow&#x27; (second row, first column)</code>

### 4. Right-align text in a slide text box

Skill ID: `08aced46-45a2-48d7-993b-ed3fb5b32302.skill-01`

Procedure:

1. Select the text box containing the paragraph to format. Click inside the text to enter text-editing mode, rather than only selecting the shape border.
2. Place the cursor in the target paragraph or select its text.
3. Click the Right Align button on the formatting toolbar. This right-aligns the current paragraph; for example, it can align a title paragraph to the right edge of its text box.

Efficiency tip: You do not need to select every character when the text box contains one paragraph: placing the cursor anywhere in that paragraph is sufficient before using Right Align.

Source task: `08aced46-45a2-48d7-993b-ed3fb5b32302`

Source instruction: Give the slide 2 the right aligned title, "Note".

Directly referenced source actions:

- Action 1: <code>`CLICK` the title text box</code>
- Action 3: <code>`CLICK` right align icon.</code>

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

- Skill: `841b50aa-df53-47bd-a73a-22d3a9f73160.skill-01`
- Intent: Apply the Midnight Blue background to the opening slide.
- Efficiency: Select slide 1 before opening the background color control so the opening canvas is the target.
- Visible success: Slide 1's full canvas changes from Ivory to Midnight Blue while its objects remain in place.

#### Demonstration 2

- Skill: `3161d64e-3120-47b4-aaad-6a764a92493b.skill-01`
- Intent: Change the opening headline’s text size from 32 pt to 42 pt.
- Efficiency: Enter text-editing mode in the headline and type 42 directly into the Font Size box after selecting its paragraph.
- Visible success: “After-Dark Market Plan” is visibly larger, with the Font Size control reporting 42 pt for the formatted headline.

#### Demonstration 3

- Skill: `0a211154-fda0-48d0-9274-eaac4ce5486d.skill-01`
- Intent: Apply the Pale Sage background to the closing action slide independently of the opening slide.
- Efficiency: Keep the slide background controls available, select slide 3 in the Slides pane, then choose Pale Sage.
- Visible success: Slide 3's entire canvas changes to Pale Sage, while slides 1 and 2 retain their separate backgrounds.

#### Demonstration 4

- Skill: `08aced46-45a2-48d7-993b-ed3fb5b32302.skill-01`
- Intent: Right-align the opening headline paragraph.
- Efficiency: With the cursor anywhere in the single headline paragraph, use Right Align; selecting every character is unnecessary.
- Visible success: The headline’s rightmost characters align to the right edge of its text box on slide 1.

Recording start: Open the supplied three-slide deck in normal editing view with slide 1 selected; all backgrounds are Ivory and the opening headline is left aligned at 32 pt.

Recording end: Slide 1 has a Midnight Blue background and a right-aligned 42 pt opening headline; slide 3 has a Pale Sage background; slide 2 remains unchanged.

Allowed variation: Equivalent static Impress controls may be used, provided slide 1 ends Midnight Blue with its 42 pt headline right aligned, slide 3 ends Pale Sage, and all non-target content remains unchanged.

### 中文详细参考方案

> 以下是一个可以参考的操作 guide。标注者可以根据实际 LibreOffice 界面采用等价操作。

本指南完成三页“Neighborhood Night Market”简报的指定格式：第 1 页改为 Midnight Blue（#1F2A44），并将标题“After-Dark Market Plan”设为 42 pt、右对齐；第 3 页改为 Pale Sage（#C7D5E0）。第 2 页仅作为现有正文样式参考，必须完全不编辑。

#### 启动后的初始状态检查

- 确认处于普通编辑视图，左侧 `Slides` 窗格中共有 3 张缩略图，且当前选中第 1 张缩略图；选中缩略图表示选择整页，不是选择页面上的某个对象。
- 查看第 1 页：opening_headline 的文字为“After-Dark Market Plan”，初始为左对齐且为 32 pt；不要改写这段文字。
- 查看第 2 页：schedule_time_list 已是 24 pt。此页的背景、文字、对象、顺序和版式都应保持不变，不要在此页点击文字进入编辑状态。
- 查看第 3 页当前仍为 Ivory 背景。全局初始 Ivory 色为 #F7F3EA；如果某页在开始时已显示目标颜色，则该页可不再调整，但仍应核对其他页没有被连带改变。

#### 第 1 步：将第 1 页背景设为 Midnight Blue

1. 在左侧 `Slides` 窗格单击第 1 页缩略图。此操作选择的是幻灯片；不要单击标题文字的边框，也不要进入标题的文字编辑模式。
2. 若右侧边栏未显示属性，打开 `Properties`。在幻灯片的 `Background` 控件中选择 `Color`，然后打开颜色下拉控件。
3. 选择与 Midnight Blue 对应的自定义颜色 #1F2A44。若调色板已有该精确色，可直接选取；如果没有，选择 `Custom Color...`，在 `Hex #` 中输入 `#1F2A44` 后确认。若该颜色对话框只提供 RGB 数值，则设置 Red 为 `31`、Green 为 `42`、Blue 为 `68` 后确认。
4. 可接受的结果是第 1 页整块画布为深蓝色，而标题、副标题、时间徽章和街道线仍处于原位置；若画布已经是 #1F2A44，则无需重复调整。若只有某个形状变蓝而画布仍是 Ivory，说明选中了对象填充而非幻灯片背景：单击第 1 页缩略图重新选择整页，再从 `Background` 进行设置。
5. 不要选择将背景应用到全部幻灯片的选项；本次只应改变当前第 1 页。

- 对应 skills：`841b50aa-df53-47bd-a73a-22d3a9f73160.skill-01`
- 高效操作：先选中第 1 页缩略图再打开 `Background`，可避免把颜色错误应用到其他页面或对象。
- 完成标志：第 1 页缩略图和编辑画布均显示 Midnight Blue（#1F2A44）背景，页面上的既有对象没有移动、删除或新增。

#### 第 2 步：把 opening_headline 设为 42 pt 并右对齐

1. 继续停留在第 1 页。先单击“After-Dark Market Plan”所在文本框的文字区域一次以选择文本框；再在文字中单击，使插入光标出现在标题段落中。第二次操作是进入文字编辑模式，不能只看到文本框外框。
2. 该文本框只有一个标题段落时，可将光标留在该段落内后使用 `Align Right`；也可以先选中整段文字再操作。不要使用拖拽移动文本框，右对齐是段落格式而不是对象位置调整。
3. 在仍处于标题文字编辑模式时，选中标题段落的文字。可在标题段落上三击，或从文字开头拖选至结尾；确认高亮范围仅为“After-Dark Market Plan”，不要选到副标题。
4. 在格式工具栏的 `Font Size` 框中直接输入 `42`，按 `Enter` 应用。随后让光标仍位于该标题段落内，单击 `Align Right`。
5. 可接受的结果是标题字符整体更大，且最右侧字符贴齐该宽文本框的右边界；若 `Font Size` 已显示 `42 pt` 或文字已右对齐，则对应项目无需再次修改。若字号改变了但对齐仍靠左，重新在标题文字内单击以进入编辑模式后点击 `Align Right`。若整个文本框被移动而非文字靠右，请用 `Ctrl+Z` 撤销该移动，再在文字编辑模式使用 `Align Right`。

- 对应 skills：`3161d64e-3120-47b4-aaad-6a764a92493b.skill-01`, `08aced46-45a2-48d7-993b-ed3fb5b32302.skill-01`
- 高效操作：标题只有一个段落时，光标置于段落中即可使用 `Align Right`；字号则在选中标题文字后直接在 `Font Size` 输入 `42`，无需浏览下拉列表。
- 完成标志：“After-Dark Market Plan”文字内容未变，`Font Size` 显示 42 pt，且标题右端在其文本框右侧整齐对齐；副标题和其他对象没有被选中或改写。

#### 第 3 步：将第 3 页背景独立设为 Pale Sage

1. 在左侧 `Slides` 窗格单击第 3 页缩略图。确认编辑画布显示 closing action slide；这是选择整页，不是选中 action_heading、action_request 或徽章形状。
2. 在右侧 `Properties` 的 `Background` 中选择 `Color`，打开颜色选择控件，并选择 Pale Sage 的精确颜色 #C7D5E0。若调色板没有精确色，使用 `Custom Color...`，在 `Hex #` 输入 `#C7D5E0` 并确认；如果只提供 RGB 数值，则设置 Red 为 `199`、Green 为 `213`、Blue 为 `224`。
3. 可接受的结果是仅第 3 页完整画布改为 Pale Sage，action_heading、action_request、action_deadline_badge 和 action_path_marker 均保持原位置。若第 3 页已是 #C7D5E0，则不需要调整。若第 1 页也意外变成 Pale Sage，立即在 `Slides` 中重新选择第 1 页并按步骤 1 恢复 #1F2A44；若第 2 页变色，应把它恢复为 Ivory #F7F3EA。
4. 不要改动第 3 页的文字内容、字号、对齐方式或任何对象；本步只操作整页 `Background`。

- 对应 skills：`0a211154-fda0-48d0-9274-eaac4ce5486d.skill-01`
- 高效操作：保持右侧 `Properties` 边栏打开，只需切换第 3 页缩略图后复用 `Background` 控件即可；这也便于确认颜色确实应用到当前页。
- 完成标志：第 3 页缩略图与画布呈 Pale Sage（#C7D5E0），而第 1 页仍为 Midnight Blue，第 2 页仍为 Ivory。

#### 最终结果检查

- 依次查看三个 `Slides` 缩略图：第 1 页为 Midnight Blue（#1F2A44），第 2 页仍为 Ivory（#F7F3EA），第 3 页为 Pale Sage（#C7D5E0）。幻灯片仍恰好为 3 张，顺序未变。
- 回到第 1 页并进入 opening_headline 的文字编辑模式核对：文字仍精确为“After-Dark Market Plan”，字号为 42 pt，标题段落为右对齐。退出文字编辑模式后，确认没有因格式操作移动文本框或其他对象。
- 查看第 2 页但不要编辑：schedule_time_list 仍为 24 pt，且第 2 页的标题、时间列表、说明文字、图标、背景和布局均与开始时一致。
- 查看第 3 页：仅背景颜色发生变化；action_heading、action_request、action_deadline_badge 和 action_path_marker 的文字、位置及数量均未改变。

## Source-task similarity review

| Measure | Maximum | Most similar source task |
| --- | ---: | --- |
| Lexical sequence similarity | 0.287603 | 9ec204e4-f0a3-42f8-8458-b772a6797cab |
| Semantic cosine similarity | 0.57496 | 8979838c-54a5-4454-a2b8-3d135a1a5c8f |

Similarity scores are reviewer aids, not automatic acceptance thresholds. Inspect the contributing source tasks and their complete ordered actions below.

### Source task `08aced46-45a2-48d7-993b-ed3fb5b32302`

Original instruction:

> Give the slide 2 the right aligned title, "Note".

Required skills derived from this source task:

- **Right-align text in a slide text box** — `08aced46-45a2-48d7-993b-ed3fb5b32302.skill-01`

Complete ordered single-action sequence:

| Action | Related required skill | Original single action |
| ---: | --- | --- |
| 0 |  | <code>`CLICK` Slide 2</code> |
| 1 | <strong>★ Right-align text in a slide text box</strong><br><code>08aced46-45a2-48d7-993b-ed3fb5b32302.skill-01</code> | <strong><code>`CLICK` the title text box</code></strong> |
| 2 |  | <code>`TYPING` &#x27;Note&#x27;</code> |
| 3 | <strong>★ Right-align text in a slide text box</strong><br><code>08aced46-45a2-48d7-993b-ed3fb5b32302.skill-01</code> | <strong><code>`CLICK` right align icon.</code></strong> |

### Source task `0a211154-fda0-48d0-9274-eaac4ce5486d`

Original instruction:

> Set the background color to yellow for any slide that contains one or more images of real people, and set the title of slide 2 as "Let's start".

Required skills derived from this source task:

- **Set a slide background color** — `0a211154-fda0-48d0-9274-eaac4ce5486d.skill-01`

Complete ordered single-action sequence:

| Action | Related required skill | Original single action |
| ---: | --- | --- |
| 0 | <strong>★ Set a slide background color</strong><br><code>0a211154-fda0-48d0-9274-eaac4ce5486d.skill-01</code> | <strong><code>`CLICK` Slide 3.</code></strong> |
| 1 | <strong>★ Set a slide background color</strong><br><code>0a211154-fda0-48d0-9274-eaac4ce5486d.skill-01</code> | <strong><code>`CLICK` color dropdown in right sidebar</code></strong> |
| 2 | <strong>★ Set a slide background color</strong><br><code>0a211154-fda0-48d0-9274-eaac4ce5486d.skill-01</code> | <strong><code>`CLICK` &#x27;yellow&#x27; (second row, first column)</code></strong> |
| 3 | <strong>★ Set a slide background color</strong><br><code>0a211154-fda0-48d0-9274-eaac4ce5486d.skill-01</code> | <strong><code>`CLICK` Slide 4.</code></strong> |
| 4 | <strong>★ Set a slide background color</strong><br><code>0a211154-fda0-48d0-9274-eaac4ce5486d.skill-01</code> | <strong><code>`CLICK` color dropdown in right sidebar</code></strong> |
| 5 | <strong>★ Set a slide background color</strong><br><code>0a211154-fda0-48d0-9274-eaac4ce5486d.skill-01</code> | <strong><code>`CLICK` &#x27;yellow&#x27; (second row, first column)</code></strong> |
| 6 |  | <code>`CLICK` Slide 2</code> |
| 7 |  | <code>`DOUBLE_CLICK` &#x27;Introduction&#x27;.</code> |
| 8 |  | <code>`TYPING` Let&#x27;s start</code> |

### Source task `3161d64e-3120-47b4-aaad-6a764a92493b`

Original instruction:

> Make the first textbox font size 60 pt while the second 28 pt on slide 14.

Required skills derived from this source task:

- **Set font size for text in a text box** — `3161d64e-3120-47b4-aaad-6a764a92493b.skill-01`

Complete ordered single-action sequence:

| Action | Related required skill | Original single action |
| ---: | --- | --- |
| 0 |  | <code>`SCROLL` down to slide 14.</code> |
| 1 |  | <code>`CLICK` slide 14.</code> |
| 2 | <strong>★ Set font size for text in a text box</strong><br><code>3161d64e-3120-47b4-aaad-6a764a92493b.skill-01</code> | <strong><code>`TRIPLE_CLICK` target audience</code></strong> |
| 3 | <strong>★ Set font size for text in a text box</strong><br><code>3161d64e-3120-47b4-aaad-6a764a92493b.skill-01</code> | <strong><code>`TRIPLE_CLICK` font size text field</code></strong> |
| 4 | <strong>★ Set font size for text in a text box</strong><br><code>3161d64e-3120-47b4-aaad-6a764a92493b.skill-01</code> | <strong><code>`TYPING` 60 pt</code></strong> |
| 5 | <strong>★ Set font size for text in a text box</strong><br><code>3161d64e-3120-47b4-aaad-6a764a92493b.skill-01</code> | <strong><code>`PRESS` enter</code></strong> |
| 6 | <strong>★ Set font size for text in a text box</strong><br><code>3161d64e-3120-47b4-aaad-6a764a92493b.skill-01</code> | <strong><code>`TRIPLE_CLICK` &#x27;Elaborate...&#x27;</code></strong> |
| 7 | <strong>★ Set font size for text in a text box</strong><br><code>3161d64e-3120-47b4-aaad-6a764a92493b.skill-01</code> | <strong><code>`TRIPLE_CLICK` font size dropdown</code></strong> |
| 8 | <strong>★ Set font size for text in a text box</strong><br><code>3161d64e-3120-47b4-aaad-6a764a92493b.skill-01</code> | <strong><code>`TYPING` 28 pt</code></strong> |
| 9 | <strong>★ Set font size for text in a text box</strong><br><code>3161d64e-3120-47b4-aaad-6a764a92493b.skill-01</code> | <strong><code>`PRESS` enter</code></strong> |

### Source task `841b50aa-df53-47bd-a73a-22d3a9f73160`

Original instruction:

> Add a note "APP" into the slide and give the slide a purple background color.

Required skills derived from this source task:

- **Set a slide background color** — `841b50aa-df53-47bd-a73a-22d3a9f73160.skill-01`

Complete ordered single-action sequence:

| Action | Related required skill | Original single action |
| ---: | --- | --- |
| 0 | <strong>★ Set a slide background color</strong><br><code>841b50aa-df53-47bd-a73a-22d3a9f73160.skill-01</code> | <strong><code>`CLICK` background dropdown</code></strong> |
| 1 | <strong>★ Set a slide background color</strong><br><code>841b50aa-df53-47bd-a73a-22d3a9f73160.skill-01</code> | <strong><code>`CLICK` color</code></strong> |
| 2 | <strong>★ Set a slide background color</strong><br><code>841b50aa-df53-47bd-a73a-22d3a9f73160.skill-01</code> | <strong><code>`CLICK` color dropdown</code></strong> |
| 3 | <strong>★ Set a slide background color</strong><br><code>841b50aa-df53-47bd-a73a-22d3a9f73160.skill-01</code> | <strong><code>`CLICK` purple (2nd row, 7th from right)</code></strong> |
| 4 |  | <code>`CLICK` View menu</code> |
| 5 |  | <code>`CLICK` Notes</code> |
| 6 |  | <code>`CLICK` &#x27;Click to add notes&#x27;</code> |
| 7 |  | <code>`TYPING` &#x27;APP&#x27;</code> |

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
