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

## Initial artifact

- Domain: community pollinator habitat survey
- Presentation: [initial_artifact.pptx](artifact/initial_artifact.pptx)
- Blueprint: [artifact_blueprint.json](artifact/artifact_blueprint.json)
- QA report: [artifact_qa.json](artifact/artifact_qa.json)

Initial state:

- Slide 2 contains the exact editable texts “FIELD SNAPSHOT”, “Nesting sites mapped”, “Late-season blooms”, and “Volunteer pairs” in separate text boxes.
- The “FIELD SNAPSHOT” text is initially 14 pt, not 18 pt.
- The three metric captions are initially 16 pt, not 22 pt, and each caption is separate from its metric value.
- Slide 2 contains an existing bee-and-wildflower image at 4.0 cm high, located below the left summary copy rather than in the requested upper-right area.
- The upper-right area of slide 2 is intentionally empty above the metric-card row, providing a clear destination for the image.

Artifact construction requirements:

- Use a clean editorial field-guide aesthetic with a warm off-white background, deep teal typography, pale mint metric cards, and restrained amber details.
- Place the three metric cards as an evenly spaced row across the lower third of slide 2; each card should contain a large value and a caption in a separate editable text object.
- Render the pollinator illustration as a static editable image object with an obvious rectangular selection boundary when selected.
- Initially place the image immediately to the right of the summary text, slightly overlapping the visual balance of that left-side region, while leaving enough empty space in the upper-right for a clear drag destination.
- Use ordinary editable text boxes rather than native placeholders for every text object.

| Slide | Layout | Purpose | Editable objects |
| ---: | --- | --- | --- |
| 1 | title | Introduce the volunteer field-briefing deck. | cover_background_band (shape), cover_main_title (text), cover_subtitle (text), cover_botanical_motif (image) |
| 2 | data_story | Summarize the survey focus and three field metrics for volunteer check-in. | snapshot_section_label (text), snapshot_heading (text), snapshot_summary_copy (text), pollinator_illustration (image), metric_card_nesting (shape), metric_value_nesting (text), metric_caption_nesting (text), metric_card_blooms (shape), metric_value_blooms (text), metric_caption_blooms (text), metric_card_pairs (shape), metric_value_pairs (text), metric_caption_pairs (text) |
| 3 | two_column | Provide concise observation guidance for the walking route. | guidance_title (text), guidance_route_panel (shape), guidance_route_steps (text), guidance_safety_panel (shape), guidance_safety_copy (text), guidance_leaf_marker (image) |

Must remain incomplete before recording:

- Do not change the wording, colors, font family, or font size of the slide title, summary copy, or metric values.
- Do not resize the image by width, crop it, replace it, or alter its aspect ratio.
- Do not move any metric card, text box, or object other than the bee-and-wildflower image.
- Do not edit slides 1 or 3.

Artifact previews:

### contact-sheet

![contact-sheet.png](artifact/previews/contact-sheet.png)

### slide-01

![slide-01.png](artifact/previews/slide-01.png)

### slide-02

![slide-02.png](artifact/previews/slide-02.png)

### slide-03

![slide-03.png](artifact/previews/slide-03.png)

## Operator guide

### Demonstration 1

- Skill: `a434992a-89df-4577-925c-0c58b747f0f4.skill-02`
- Intent: Set the separate “FIELD SNAPSHOT” text box to exactly 18 pt.
- Efficiency: Enter text-editing mode in the label and type the exact value in the Font Size field rather than using incremental size controls.
- Visible success: The teal section label remains unchanged in wording and color but displays visibly larger at 18 pt.

### Demonstration 2

- Skill: `e4ef0baf-4b52-4590-a47e-d4d464cca2d7.skill-02`
- Intent: Set the “Nesting sites mapped”, “Late-season blooms”, and “Volunteer pairs” metric-caption text boxes to exactly 22 pt.
- Efficiency: Select the three caption text boxes together when practical, then enter 22 pt once in the Font Size field; otherwise update each independent caption box in sequence.
- Visible success: All three targeted captions display at the same 22 pt size while their associated metric values remain unchanged.

### Demonstration 3

- Skill: `7ae48c60-f143-4119-b659-15b8f485eb9a.skill-01`
- Intent: Set the bee-and-wildflower image to an exact height of 6.5 cm.
- Efficiency: Use the image Position and Size controls and replace the height measurement directly.
- Visible success: The selected image reports a height of 6.5 cm and retains its original proportions.

### Demonstration 4

- Skill: `ed43c15f-00cb-4054-9c95-62c880865d68.skill-02`
- Intent: Relocate the resized bee-and-wildflower image into the empty upper-right region above the metric cards.
- Efficiency: Drag from the image interior, not a selection handle, to avoid changing its size while positioning it.
- Visible success: The image sits to the right of the summary copy and above the card row without covering text or cards.

Recording start: Open the supplied three-slide deck with slide 2 visible in normal editing view.

Recording end: Slide 2 shows the requested 18 pt label, all three 22 pt metric captions, and the 6.5 cm-high illustration placed in the upper-right.

Allowed variation: Minor final placement variation is acceptable provided the image is clearly in the open upper-right region, above the metric cards, to the right of the summary text, and no overlap occurs.

## Expected incidental operations

- **substantive_prerequisite:** Navigate to slide 2 and select the individual text and image objects needed for the requested edits. Reason: The requested changes are all confined to distinct editable objects on the field-snapshot slide.

## Source-similarity audit

| Measure | Maximum | Most similar source task |
| --- | ---: | --- |
| Lexical sequence similarity | 0.264662 | a53f80cd-4a90-4490-8310-097b011433f6 |
| Semantic cosine similarity | 0.461807 | 8979838c-54a5-4454-a2b8-3d135a1a5c8f |

Scores are reviewer aids, not automatic acceptance thresholds. Compare the task with the source instructions and actions above for solution leakage.

## Review this package

Check that every required skill is necessary and observable, the task is natural and not a source-solution reproduction, incidental operations are limited, the artifact matches its specification, and the guide remains helpful without prescribing one click-by-click trajectory.

1. Inspect the task, required skills, source evidence, artifact, and guide.
2. Fill [review.json](review.json) using `approved`, `revision_requested`, or `rejected`.
3. From the repository root, collect all completed forms:

```bash
python scripts/python/manage_reference_review_packets.py collect
```

Detailed field guidance is in [`reviewer.md`](../../../reviewer.md).

## Start annotation after approval

```bash
python scripts/python/record_reference_task.py \
  --reference-task-id reference-task-impress-full-r01-003
```

The ordinary launcher reads the collected central review file and refuses pending, revision-requested, or rejected tasks.
