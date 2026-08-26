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

## Initial artifact

- Domain: community garden volunteer coordination
- Presentation: [initial_artifact.pptx](artifact/initial_artifact.pptx)
- Blueprint: [artifact_blueprint.json](artifact/artifact_blueprint.json)
- QA report: [artifact_qa.json](artifact/artifact_qa.json)

Initial state:

- The presentation has three slides in the stated order and begins with an ivory #FFFDF7 background on every slide.
- Slides 2 and 3 are not selected together; each is an independent slide thumbnail in the Slides pane.
- Slide 2 contains the existing garden-bed illustration at 4.20 cm wide by 2.70 cm high, not at the requested dimensions.
- The lower-left Slide 2 callout reads “Morning Walk Checklist” and is formatted in Liberation Serif rather than Liberation Sans.
- Slide 3 contains the assignment table. Its consecutive header-row cells currently read “Bed”, “Window”, “Guide”, and “Gear” from left to right.
- All other visible text, shapes, table body values, and object placements are already final and should remain unchanged.

Artifact construction requirements:

- Use a clean editorial garden-notebook visual style: ivory base, deep green text, restrained terracotta rules, and mustard accents.
- Create a privacy-safe synthetic vector-style garden-bed illustration directly in the deck as the existing image asset; no external files are needed.
- The final intended backgrounds for Slides 2 and 3 are pale mint #E5F1E8, while Slide 1 remains ivory #FFFDF7.
- Set the initial table header values and image dimensions exactly as described so the requested edits are visibly reviewable.
- Keep the callout text as a separate editable text object inside its card so its font family can be changed without altering nearby copy.

| Slide | Layout | Purpose | Editable objects |
| ---: | --- | --- | --- |
| 1 | title | Brief cover that establishes the volunteer walk-through context | cover_top_rule (shape), cover_title (text), cover_subtitle (text), cover_seedling_motif (image) |
| 2 | two_column | Working-slide checklist with a garden-bed visual reference | checklist_section_label (text), checklist_title (text), garden_bed_illustration (image), garden_bed_caption (text), checklist_callout_card (shape), checklist_callout_text (text), checklist_item_one (text), checklist_item_two (text) |
| 3 | data_story | Working-slide assignment grid for the garden walk | assignment_section_label (text), assignment_title (text), assignment_intro (text), assignment_table (table), assignment_footer_note (text), assignment_side_marker (shape) |

Must remain incomplete before recording:

- Do not apply the pale-mint #E5F1E8 background to Slides 2 and 3 before the task is performed.
- Do not resize the Slide 2 garden-bed illustration to 5.80 cm by 3.60 cm before the task is performed.
- Do not format the Slide 2 “Morning Walk Checklist” callout in Liberation Sans before the task is performed.
- Do not replace the Slide 3 table header row with “Area”, “Visit time”, “Coordinator”, and “Materials” before the task is performed.

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

- Skill: `5cfb9197-e72b-454b-900e-c06b0c802b40.skill-01`
- Intent: Replace all four adjacent header labels in the Slide 3 assignment table while retaining the existing table structure.
- Efficiency: Place the text cursor in the first header cell and use Tab to advance through the remaining consecutive header cells after replacing each cell’s text.
- Visible success: The header row reads, from left to right, “Area”, “Visit time”, “Coordinator”, and “Materials”, with the body rows unchanged.

### Demonstration 2

- Skill: `c82632a4-56b6-4db4-9dd1-3820ee3388e4.skill-02`
- Intent: Set the existing Slide 2 garden-bed illustration to the specified physical dimensions.
- Efficiency: Enter the width and then use Tab to reach the height field in the same size-control interaction.
- Visible success: The selected illustration’s size controls show Width 5.80 cm and Height 3.60 cm.

### Demonstration 3

- Skill: `af2d657a-e6b3-4c6a-9f67-9e3ed015974c.skill-01`
- Intent: Change only the lower-left Slide 2 checklist callout’s font family to Liberation Sans.
- Efficiency: Enter text-editing mode in the callout and select its full text before entering the requested font family in the font-name control.
- Visible success: “Morning Walk Checklist” displays in Liberation Sans while its neighboring title and checklist items retain their original font formatting.

### Demonstration 4

- Skill: `9ec204e4-f0a3-42f8-8458-b772a6797cab.skill-01`
- Intent: Prepare the two working slides for one shared background update.
- Efficiency: Select one target thumbnail and Ctrl-click the other target thumbnail so the shared background change can be applied once.
- Visible success: Slides 2 and 3 are simultaneously highlighted in the Slides pane before the pale-mint background is applied, and both slides receive #E5F1E8.

Recording start: Open the supplied three-slide Community Garden Field Brief in Normal view with no multi-slide selection active.

Recording end: Slides 2 and 3 share pale-mint #E5F1E8 backgrounds; the Slide 2 illustration is 5.80 cm by 3.60 cm; the specified Slide 2 callout is Liberation Sans; and the Slide 3 header row contains the four requested labels.

Allowed variation: Equivalent LibreOffice controls and navigation paths are acceptable, provided the specified slide selection, background colors, table text, image dimensions, and isolated font-family change are achieved.

## Expected incidental operations

- **task_specific:** Apply the pale-mint #E5F1E8 slide background after Slides 2 and 3 have been selected together. Reason: This is the shared visible outcome that makes the multi-slide selection meaningful within the coordinated brief update.
- **scaffolding:** Select the intended image, callout text object, and table header cells before performing their requested edits. Reason: Target selection is necessary scaffolding to restrict each formatting or text change to the specified object.

## Source-similarity audit

| Measure | Maximum | Most similar source task |
| --- | ---: | --- |
| Lexical sequence similarity | 0.222222 | 04578141-1d42-4146-b9cf-6fab4ce5fd74 |
| Semantic cosine similarity | 0.512099 | 9cf05d24-6bd9-4dae-8967-f67d88f5d38a |

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
  --reference-task-id reference-task-impress-full-r01-004
```

The ordinary launcher reads the collected central review file and refuses pending, revision-requested, or rejected tasks.
