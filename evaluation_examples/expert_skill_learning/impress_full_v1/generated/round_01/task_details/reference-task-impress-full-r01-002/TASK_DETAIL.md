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

## Initial artifact

- Domain: municipal night-market planning
- Presentation: [initial_artifact.pptx](artifact/initial_artifact.pptx)
- Blueprint: [artifact_blueprint.json](artifact/artifact_blueprint.json)
- QA report: [artifact_qa.json](artifact/artifact_qa.json)

Initial state:

- All three slides initially use the warm Ivory background F7F3EA.
- Slide 1's opening_headline contains “After-Dark Market Plan,” is left aligned, and uses 32 pt text.
- Slide 3 is intentionally still Ivory rather than Pale Sage.
- Slide 2's schedule_time_list is already 24 pt and should not be edited.

Artifact construction requirements:

- Use editable text boxes and standard editable shapes only; do not use native title or content placeholders.
- Represent Midnight Blue as #1F2A44 and Pale Sage as #C7D5E0.
- The opening headline text box should be wide enough that right alignment is clearly visible after formatting.
- Keep all slide backgrounds initially Ivory #F7F3EA so both requested background edits are visibly outstanding.

| Slide | Layout | Purpose | Editable objects |
| ---: | --- | --- | --- |
| 1 | blank | Opening overview for the council preview | opening_headline (text), opening_subtitle (text), opening_time_badge (shape), opening_streetline (shape) |
| 2 | two_column | Operating schedule overview | schedule_heading (text), schedule_time_list (text), schedule_vendor_note (text), schedule_clock_icon (shape) |
| 3 | blank | Closing action prompt for council coordination | action_heading (text), action_request (text), action_deadline_badge (shape), action_path_marker (shape) |

Must remain incomplete before recording:

- Do not change the background of slide 2.
- Do not alter the wording, font size, or alignment of any text on slide 2.
- Do not change any text other than formatting the opening_headline on slide 1.
- Do not add, remove, reorder, or duplicate slides or objects.

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

- Skill: `841b50aa-df53-47bd-a73a-22d3a9f73160.skill-01`
- Intent: Apply the Midnight Blue background to the opening slide.
- Efficiency: Select slide 1 before opening the background color control so the opening canvas is the target.
- Visible success: Slide 1's full canvas changes from Ivory to Midnight Blue while its objects remain in place.

### Demonstration 2

- Skill: `3161d64e-3120-47b4-aaad-6a764a92493b.skill-01`
- Intent: Change the opening headline’s text size from 32 pt to 42 pt.
- Efficiency: Enter text-editing mode in the headline and type 42 directly into the Font Size box after selecting its paragraph.
- Visible success: “After-Dark Market Plan” is visibly larger, with the Font Size control reporting 42 pt for the formatted headline.

### Demonstration 3

- Skill: `0a211154-fda0-48d0-9274-eaac4ce5486d.skill-01`
- Intent: Apply the Pale Sage background to the closing action slide independently of the opening slide.
- Efficiency: Keep the slide background controls available, select slide 3 in the Slides pane, then choose Pale Sage.
- Visible success: Slide 3's entire canvas changes to Pale Sage, while slides 1 and 2 retain their separate backgrounds.

### Demonstration 4

- Skill: `08aced46-45a2-48d7-993b-ed3fb5b32302.skill-01`
- Intent: Right-align the opening headline paragraph.
- Efficiency: With the cursor anywhere in the single headline paragraph, use Right Align; selecting every character is unnecessary.
- Visible success: The headline’s rightmost characters align to the right edge of its text box on slide 1.

Recording start: Open the supplied three-slide deck in normal editing view with slide 1 selected; all backgrounds are Ivory and the opening headline is left aligned at 32 pt.

Recording end: Slide 1 has a Midnight Blue background and a right-aligned 42 pt opening headline; slide 3 has a Pale Sage background; slide 2 remains unchanged.

Allowed variation: Equivalent static Impress controls may be used, provided slide 1 ends Midnight Blue with its 42 pt headline right aligned, slide 3 ends Pale Sage, and all non-target content remains unchanged.

## Expected incidental operations

- **task_specific:** Select slide 1 and slide 3 in the Slides pane before applying their respective backgrounds. Reason: Each background edit must apply to its intended individual slide.
- **substantive_prerequisite:** Enter text-editing mode in the opening headline before changing paragraph alignment and font size. Reason: The requested text formatting applies to the headline paragraph rather than the text box frame.

## Source-similarity audit

| Measure | Maximum | Most similar source task |
| --- | ---: | --- |
| Lexical sequence similarity | 0.287603 | 9ec204e4-f0a3-42f8-8458-b772a6797cab |
| Semantic cosine similarity | 0.57496 | 8979838c-54a5-4454-a2b8-3d135a1a5c8f |

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
  --reference-task-id reference-task-impress-full-r01-002
```

The ordinary launcher reads the collected central review file and refuses pending, revision-requested, or rejected tasks.
