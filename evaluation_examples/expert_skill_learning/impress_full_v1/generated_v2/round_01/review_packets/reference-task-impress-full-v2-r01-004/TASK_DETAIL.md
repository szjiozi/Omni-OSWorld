# Urban Pollinator Pocket Guide

- Reference task: `reference-task-impress-full-v2-r01-004`
- Application: `libreoffice_impress`
- Review decision: `pending`

## Task instruction

Finalize the two-slide “Urban Pollinator Pocket Guide” briefing: remove the unused working slide, give the cover slide a navy blue background, and enlarge its bee photograph proportionally until it fills the existing photo window. On the species checklist slide, underline every entry in the table, from the first header cell through the final status cell, so the checklist reads as a marked reference sheet.

## Required skills

### 1. Resize an image proportionally using corner handles

Skill ID: `5d901039-a89c-4bfb-967b-bf66f4df075e.skill-01`

Procedure:

1. Click the image once to select it and show its resize handles.
2. Drag a corner handle outward to enlarge the image while retaining its aspect ratio; for example, drag the top-left handle toward the page’s top-left area.
3. If more enlargement is needed, drag the opposite corner handle outward, such as the bottom-right handle toward the page’s bottom-right area.

Efficiency tip: Use corner handles rather than side handles when enlarging an image proportionally, and make the largest practical resize first to minimize adjustment drags.

Source task: `5d901039-a89c-4bfb-967b-bf66f4df075e`

Source instruction: I want to turn the rectangular image of Columbus on the first page into a cover page. Could you help me stretch this image to fill the entire page, keeping its proportion and centering the image?

Directly referenced source actions:

- Action 0: <code>`CLICK` on the image</code>
- Action 1: <code>`MOVE_TO` top left corner of the image</code>
- Action 2: <code>`DRAG_TO` increase the size of the image</code>
- Action 3: <code>`MOVE_TO` bottom right corner of the image</code>
- Action 4: <code>`DRAG_TO` increase the size of the image</code>

### 2. Delete the currently selected slide with the keyboard

Skill ID: `bf4e9888-f10f-47af-8dba-76413038b73c.skill-02`

Procedure:

1. Select the slide thumbnail to remove in the Slides pane, then press Delete.
2. For example, after generating image slides, select any extra blank starter slide and press Delete to remove it from the presentation.

Efficiency tip: Delete unwanted slides from the thumbnail pane rather than opening each slide and removing its individual contents.

Source task: `bf4e9888-f10f-47af-8dba-76413038b73c`

Source instruction: I have a series of .png images named pic1.png to pic6.png saved on the Desktop. I want to create a new presentation with six blank slides(which means no textbox or any other stuff on the page), and insert one image per slide in order—pic1.png on the first slide, pic2.png on the second, and so on—following the numerical order. The goal is to prepare a presentation suitable for continuous playback in a kiosk or multimedia show. Could you help me with that?

Directly referenced source actions:

- Action 10: <code>`PRESS` delete</code>

### 3. Change a slide background color

Skill ID: `a434992a-89df-4577-925c-0c58b747f0f4.skill-01`

Procedure:

1. Open the slide background color dropdown.
2. Choose a background fill color from the palette; for example, select a red swatch.
3. The selected color is applied to the current slide background.

Efficiency tip: Choose the background color directly from the palette rather than opening additional formatting dialogs when a solid color is all that is needed.

Source task: `a434992a-89df-4577-925c-0c58b747f0f4`

Source instruction: Change the font size of the content to 12, and change the font color to orange. Change the slide's background to red.

Directly referenced source actions:

- Action 0: <code>`CLICK` background dropdown arrow</code>
- Action 1: <code>`CLICK` color</code>
- Action 2: <code>`CLICK` color dropdown arrow</code>
- Action 3: <code>`CLICK` red (2nd row, 5th from left)</code>

### 4. Select a table text range by dragging from the first cell to the last cell

Skill ID: `986fc832-6af2-417c-8845-9272b3a1528b.skill-03`

Procedure:

1. Click the table to activate it, then click at the beginning of the text in its first cell.
2. Drag from that starting caret position through the last cell, ending at the lower-right end of the table content.
3. With the resulting multi-cell text selection active, apply a character format such as underline or font color.

Efficiency tip: Start at the first character and drag continuously to the final cell rather than formatting cells one at a time.

Source task: `986fc832-6af2-417c-8845-9272b3a1528b`

Source instruction: underline the content and make the font color on this slide (including the table) dark red 2.

Directly referenced source actions:

- Action 6: <code>`CLICK` table</code>
- Action 7: <code>`CLICK` cursor before &#x27;Model Name&#x27;</code>
- Action 8: <code>`DRAG_TO` bottom right corner of table</code>

## Initial artifact

- Domain: Urban pollinator education
- Presentation: [initial_artifact.pptx](artifact/initial_artifact.pptx)
- Blueprint: [artifact_blueprint.json](artifact/artifact_blueprint.json)
- QA report: [artifact_qa.json](artifact/artifact_qa.json)

Initial state:

- The presentation opens with three slides in the order shown; slide 3 is intentionally an unused working slide and must remain present initially.
- Slide 1 has the default light cream background rather than navy blue.
- The bee photograph on slide 1 is already centered over the tall photo window but is intentionally undersized, leaving a visible border of the photo window on all sides.
- Slide 2’s checklist table contains ordinary, non-underlined text in every header and body cell.
- All title, body, table, shape, and image objects are editable.

Artifact construction requirements:

- Use a privacy-safe synthetic bee-and-lavender image for the cover and a separate simple pollinator illustration on slide 2.
- Make the cover photo window and the initial photograph share the same aspect ratio, with the photo materially smaller, so proportional enlargement by a corner handle can visibly fill the window.
- Use navy blue as a standard solid palette color for the requested cover background.
- Keep the slide 2 table large enough that a continuous drag from the first character of the first header cell to the final character of the final status cell is practical and visibly reviewable.

| Slide | Layout | Purpose | Editable objects |
| ---: | --- | --- | --- |
| 1 | blank | Cover for a short urban pollinator field guide | cover_text_panel (shape), cover_heading (text), cover_subheading (text), cover_photo_window (shape), cover_bee_photo (image), cover_footer_tag (shape) |
| 2 | two_column | Quick-reference checklist of pollinator observations | checklist_heading (text), checklist_intro (text), pollinator_observation_table (table), checklist_side_illustration (image), checklist_callout (shape) |
| 3 | blank | Unused internal working slide to be removed before delivery | discarded_working_note (text), discarded_placeholder_block (shape) |

Must remain incomplete before recording:

- Do not delete slide 3 during generation; it is the slide that must be deleted by the operator.
- Do not set slide 1’s background to navy blue during generation.
- Do not resize the cover bee photograph to fill its photo window during generation.
- Do not underline any portion of the checklist table during generation.

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

- Skill: `5d901039-a89c-4bfb-967b-bf66f4df075e.skill-01`
- Intent: Scale the centered cover photograph up without distorting it, until it fills the existing tall photo window.
- Efficiency: Select the image and use a corner handle for the largest practical enlargement rather than using side handles.
- Visible success: The bee photo reaches the photo-window boundaries while retaining its original proportions and without visible side or top/bottom gaps.

### Demonstration 2

- Skill: `bf4e9888-f10f-47af-8dba-76413038b73c.skill-02`
- Intent: Remove the unused internal working slide from the deck.
- Efficiency: Select the third slide’s thumbnail in the Slides pane and press Delete, rather than deleting the slide’s individual objects.
- Visible success: The slide thumbnail list contains only the cover and checklist slides, with no scratch-space slide remaining.

### Demonstration 3

- Skill: `a434992a-89df-4577-925c-0c58b747f0f4.skill-01`
- Intent: Apply the requested solid navy blue background to the cover slide.
- Efficiency: Use the slide background color palette to choose navy blue directly when a solid fill is required.
- Visible success: The entire slide 1 canvas behind its objects displays a uniform navy blue background.

### Demonstration 4

- Skill: `986fc832-6af2-417c-8845-9272b3a1528b.skill-03`
- Intent: Apply underline formatting across the complete checklist table text in one continuous selection.
- Efficiency: Activate the table, begin at the first character in the first header cell, and drag continuously through the final character in the lower-right cell before applying underline.
- Visible success: Every table header and every entry through the final Status cell is underlined, with no unformatted cell text left behind.

Recording start: Open the supplied three-slide presentation in normal editing view with all four requested outcomes visibly incomplete.

Recording end: The deck has two slides; the cover has a navy blue background and a proportionally enlarged photo filling its window; and every character in the checklist table is underlined.

Allowed variation: The exact order of the four edits may vary. Minor handle placement variation is acceptable provided the cover image remains proportional, fills the intended photo window, and remains visually aligned with it.

## Expected incidental operations

- **scaffolding:** Select slide thumbnails to target the cover, checklist, and unused working slide. Reason: Each requested edit applies to a specific slide, and slide 3 must be identified before deletion.
- **task_specific:** Apply underline after the multi-cell table text selection is active. Reason: The task specifically requires the selected table range to become underlined.

## Source-similarity audit

| Measure | Maximum | Most similar source task |
| --- | ---: | --- |
| Lexical sequence similarity | 0.258706 | 5d901039-a89c-4bfb-967b-bf66f4df075e |
| Semantic cosine similarity | 0.528282 | 8979838c-54a5-4454-a2b8-3d135a1a5c8f |

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
  --reference-task-id reference-task-impress-full-v2-r01-004
```

The ordinary launcher reads the collected central review file and refuses pending, revision-requested, or rejected tasks.
