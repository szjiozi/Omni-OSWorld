# Riverside Garden Volunteer Day

- Reference task: `reference-task-impress-full-v2-r01-005`
- Application: `libreoffice_impress`
- Review decision: `pending`

## Task instruction

On the “Join the workday” slide, establish the two color cues for the event: make all text inside the dark-green schedule card use the standard Yellow font-color palette swatch, and recolor only the words “bring work gloves” in the preparation sentence with the Dark Red 2 palette swatch. Leave the rest of the preparation sentence unchanged.

## Required skills

### 1. Apply a font color from the font-color palette

Skill ID: `986fc832-6af2-417c-8845-9272b3a1528b.skill-02`

Procedure:

1. Select the text whose character color should change.
2. Click the Font Color button to open its color palette.
3. Choose the desired palette swatch; for example, select the “Dark Red 2” swatch to apply that color to the selected text.

Efficiency tip: Select the complete text range before opening the palette so a single color choice formats the entire range at once.

Source task: `986fc832-6af2-417c-8845-9272b3a1528b`

Source instruction: underline the content and make the font color on this slide (including the table) dark red 2.

Directly referenced source actions:

- Action 3: <code>`CLICK` font color icon</code>
- Action 4: <code>`CLICK` dark red 2</code>

### 2. Set the font color of all text in a text box using the color palette

Skill ID: `57667013-ea97-417c-9dce-2713091e6e2a.skill-01`

Procedure:

1. Click inside the target text box to enter text-editing mode.
2. Press Ctrl+A to select all text in that text box.
3. Open the Font Color drop-down and choose the required palette color. For example, choose the standard yellow swatch rather than a light or dark variation.

Efficiency tip: Use Ctrl+A only after entering the intended text box; this selects its text without selecting other objects on the slide, allowing the color to be applied in one operation.

Source task: `57667013-ea97-417c-9dce-2713091e6e2a`

Source instruction: Navigate to slide 5 and set the font color of all textboxes to yellow. Use exactly 'yellow'—no variations such as light yellow, dark yellow, or any other color.

Directly referenced source actions:

- Action 1: <code>`CLICK` text in &#x27;write an original...&#x27;</code>
- Action 2: <code>`HOTKEY` ctrl-A</code>
- Action 3: <code>`CLICK` font color dropdown.</code>
- Action 4: <code>`CLICK` yellow (2nd row, first from left)</code>

## Initial artifact

- Domain: community garden volunteer event
- Presentation: [initial_artifact.pptx](artifact/initial_artifact.pptx)
- Blueprint: [artifact_blueprint.json](artifact/artifact_blueprint.json)
- QA report: [artifact_qa.json](artifact/artifact_qa.json)

Initial state:

- The presentation contains three editable wide-format slides with the Riverside Garden Volunteer Day theme already applied.
- On slide 2, the dark-green schedule card and its editable schedule text are present; the schedule text is currently white rather than standard Yellow.
- On slide 2, the editable preparation sentence contains the exact phrase “bring work gloves”; that phrase is currently dark green, matching the other words in the sentence rather than Dark Red 2.
- No requested font-color change has been completed in the initial deck.

Artifact construction requirements:

- Build all listed text as ordinary editable text boxes, not title or content placeholders.
- Keep “bring work gloves” in a single editable paragraph with the rest of the preparation sentence so a character-level font-color change is visibly testable.
- Use a dark-green schedule card with sufficient contrast for the initial white text and the required standard Yellow text.
- Use a light background behind the preparation sentence so Dark Red 2 is visibly distinguishable from the unchanged dark-green text.

| Slide | Layout | Purpose | Editable objects |
| ---: | --- | --- | --- |
| 1 | title | Opening slide introducing the neighborhood garden workday. | cover_background_panel (shape), cover_garden_arc (shape), cover_event_title (text), cover_event_subtitle (text), cover_seedling_icon (shape) |
| 2 | two_column | Volunteer sign-up information requiring the requested text color cues. | signup_background_panel (shape), signup_section_title (text), signup_schedule_card (shape), signup_schedule_text (text), signup_preparation_label (text), signup_preparation_sentence (text), signup_path_marker (shape), signup_signup_footer (text) |
| 3 | title_content | Closing slide with practical next actions for attendees. | next_steps_background_panel (shape), next_steps_title (text), next_steps_checklist (text), next_steps_toolbox_icon (shape), next_steps_thank_you (text) |

Must remain incomplete before recording:

- Do not change any slide background, shape fill, layout, object position, text wording, font family, font size, or text alignment.
- Do not recolor any text other than all text in the schedule callout and only the phrase “bring work gloves” in the preparation sentence.
- Do not apply Dark Red 2 to the entire preparation sentence.
- Do not use a yellow variation other than the standard Yellow palette swatch for the schedule callout.

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

- Skill: `986fc832-6af2-417c-8845-9272b3a1528b.skill-02`
- Intent: Apply Dark Red 2 only to the phrase “bring work gloves” within the preparation sentence on slide 2.
- Efficiency: Enter text-editing mode in the preparation sentence and select exactly the target phrase before opening the Font Color palette.
- Visible success: Only those three words appear in Dark Red 2, while “Please” and “and a refillable bottle.” remain dark green.

### Demonstration 2

- Skill: `57667013-ea97-417c-9dce-2713091e6e2a.skill-01`
- Intent: Apply the standard Yellow palette swatch to every character in the schedule callout on slide 2.
- Efficiency: Click inside the schedule text box first, then use Ctrl+A to select only that text box’s complete text before choosing Yellow from the Font Color palette.
- Visible success: Both lines, “Meet at the tool shed” and “8:30–11:30 a.m.”, display in the same standard Yellow against the dark-green card.

Recording start: Open the supplied presentation in LibreOffice Impress with slide 2 selected or readily accessible; all requested text is still in its initial colors.

Recording end: Slide 2 retains its original layout and wording, the whole schedule callout is standard Yellow, and only “bring work gloves” is Dark Red 2.

Allowed variation: Equivalent efficient selection and palette-opening paths are acceptable if the specified palette colors and exact text scope are preserved.

## Expected incidental operations

- **scaffolding:** Navigate to slide 2 and enter text-editing mode in each specified text box. Reason: The requested character-level and text-box-wide font-color changes target two separate editable text objects on that slide.

## Source-similarity audit

| Measure | Maximum | Most similar source task |
| --- | ---: | --- |
| Lexical sequence similarity | 0.338645 | 57667013-ea97-417c-9dce-2713091e6e2a |
| Semantic cosine similarity | 0.637427 | 04578141-1d42-4146-b9cf-6fab4ce5fd74 |

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
  --reference-task-id reference-task-impress-full-v2-r01-005
```

The ordinary launcher reads the collected central review file and refuses pending, revision-requested, or rejected tasks.
