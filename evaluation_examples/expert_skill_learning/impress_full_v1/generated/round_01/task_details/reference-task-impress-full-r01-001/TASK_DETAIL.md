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

## Initial artifact

- Domain: community pollinator-garden volunteer event
- Presentation: [initial_artifact.pptx](artifact/initial_artifact.pptx)
- Blueprint: [artifact_blueprint.json](artifact/artifact_blueprint.json)
- QA report: [artifact_qa.json](artifact/artifact_qa.json)

Initial state:

- Slide 2 contains three evenly spaced schedule cards across the middle of the slide: “9:00 — Check in at Pier Garden,” “9:30 — Plant shoreline natives,” and “11:30 — Return tools and sort compost.”
- The RSVP callout panel and its text box are together in the upper-left area of slide 2, visibly away from the intended footer position beneath the schedule cards.
- The RSVP text reads “Bring water, sun protection, and gloves. Register by Friday to reserve a planting kit.” and is left-aligned in dark gray.
- Within the RSVP text, “Register by Friday” is not underlined and is dark gray rather than teal.
- The footer area centered below the three schedule cards is clear and can accommodate the moved RSVP callout without overlapping other objects.

Artifact construction requirements:

- Use a warm off-white background with dark teal headings, pale sage cards, and teal accent details.
- Build the RSVP message as one editable text object with character-level formatting available for the deadline phrase.
- Keep the RSVP panel and RSVP text as separate editable objects so the text box can be repositioned independently while the panel may remain as contextual visual scaffolding.
- Place the initial RSVP text box clearly in the upper-left quadrant and size it so it can be moved intact to the centered footer region.

| Slide | Layout | Purpose | Editable objects |
| ---: | --- | --- | --- |
| 1 | title | Introduce the volunteer event and establish the botanical harbor theme. | cover_harbor_band (shape), cover_event_title (text), cover_event_subtitle (text), cover_botanical_illustration (image), cover_partner_mark (shape) |
| 2 | process | Present the volunteer schedule and a closing registration callout. | schedule_section_title (text), schedule_intro_caption (text), schedule_card_arrival (shape), schedule_card_planting (shape), schedule_card_cleanup (shape), schedule_arrival_text (text), schedule_planting_text (text), schedule_cleanup_text (text), rsvp_callout_panel (shape), rsvp_closing_callout (text) |

Must remain incomplete before recording:

- Do not move the RSVP callout to the footer beneath the schedule cards.
- Do not center-align the RSVP callout text.
- Do not underline “Register by Friday.”
- Do not change “Register by Friday” to #007C83 teal.
- Do not alter the dark-gray, non-underlined styling of the remaining RSVP text.
- Do not change the wording, card order, slide order, background, or other schedule elements.

Artifact previews:

### contact-sheet

![contact-sheet.png](artifact/previews/contact-sheet.png)

### slide-01

![slide-01.png](artifact/previews/slide-01.png)

### slide-02

![slide-02.png](artifact/previews/slide-02.png)

## Operator guide

### Demonstration 1

- Skill: `15aece23-a215-4579-91b4-69eec72e18da.skill-01`
- Intent: Reposition the RSVP text box from the upper-left area to the centered footer beneath the three schedule cards.
- Efficiency: Select the text box by its border and drag it using the card row and slide-center guide as placement references.
- Visible success: The RSVP text box appears below the card row, centered in the open footer region rather than beside the heading.

### Demonstration 2

- Skill: `4ed5abd0-8b5d-47bd-839f-cacfa15ca37a.skill-02`
- Intent: Underline only the deadline phrase “Register by Friday” within the RSVP callout.
- Efficiency: Keep the deadline phrase selected while applying the underline so no surrounding text is formatted.
- Visible success: Only the deadline words have a visible underline; the surrounding packing-list and reservation text remains unlined.

### Demonstration 3

- Skill: `986fc832-6af2-417c-8845-9272b3a1528b.skill-02`
- Intent: Apply the exact teal #007C83 font color to the selected deadline phrase.
- Efficiency: Apply the teal color while the same deadline phrase remains selected after its underline is set.
- Visible success: “Register by Friday” is teal while all remaining RSVP copy stays dark gray.

### Demonstration 4

- Skill: `05dd4c1d-c489-4c85-8389-a7836c4f0567.skill-01`
- Intent: Center-align every paragraph in the RSVP callout text box.
- Efficiency: Enter text-editing mode in the RSVP callout, select all text in that box, and apply paragraph centering once.
- Visible success: Both sentences in the RSVP message are centered within the relocated callout area.

Recording start: Open the provided two-slide Harbor Pollinator Day presentation in Normal view with slide 2 selected; the RSVP text box is visibly upper-left, left-aligned, and unformatted at the deadline phrase.

Recording end: Slide 2 shows the RSVP text box centered in the footer below the schedule cards, with all callout paragraphs centered and only “Register by Friday” teal (#007C83) and underlined.

Allowed variation: The callout may be placed with minor positional variation as long as it is clearly centered beneath the three schedule cards, does not overlap another object, and the specified text formatting is exact.

## Expected incidental operations

- **scaffolding:** Select slide 2 in the Slides pane before editing the schedule-and-RSVP slide. Reason: The requested callout edits all occur on slide 2.
- **task_specific:** Enter text-editing mode and select the deadline phrase before applying character formatting. Reason: Underline and font color must apply only to “Register by Friday,” not the full RSVP message.

## Source-similarity audit

| Measure | Maximum | Most similar source task |
| --- | ---: | --- |
| Lexical sequence similarity | 0.272727 | 04578141-1d42-4146-b9cf-6fab4ce5fd74 |
| Semantic cosine similarity | 0.423523 | 986fc832-6af2-417c-8845-9272b3a1528b |

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
  --reference-task-id reference-task-impress-full-r01-001
```

The ordinary launcher reads the collected central review file and refuses pending, revision-requested, or rejected tasks.
