# Neighborhood Repair Café — Host Brief

- Reference task: `reference-task-impress-full-v2-r01-003`
- Application: `libreoffice_impress`
- Review decision: `pending`

## Task instruction

Update the “Neighborhood Repair Café” host brief for the workshop team. First inspect the copper color used by the cover headline and use that verified color for the titles on both activity slides. Select the two activity slides together and give them the shared pale-sage background. On the “Repair Table Flow” slide, set the title to 44 pt using the font-size list, and set the “Tool check-in closes at 09:50” schedule line to an exact 27 pt so it remains a distinct operational cue.

## Required skills

### 1. Multi-select slide thumbnails in the Slides pane

Skill ID: `9ec204e4-f0a3-42f8-8458-b772a6797cab.skill-01`

Procedure:

1. In the Slides pane, click the first slide thumbnail to select it.
2. Hold Ctrl and click another thumbnail to add it to the selection without deselecting the first. For example, select two adjacent ending slides before applying a shared command.
3. Release Ctrl after all intended thumbnails are selected.

Efficiency tip: Use Ctrl-click to build a noncontiguous or multi-slide selection in one pass instead of applying the same command separately to each slide.

Source task: `9ec204e4-f0a3-42f8-8458-b772a6797cab`

Source instruction: Please duplicate the last two slides and insert the copies in alternating order, so the sequence becomes: original slide A, original slide B, then duplicated slide A, duplicated slide B.

Directly referenced source actions:

- Action 1: <code>`CLICK` slide 23</code>
- Action 2: <code>`KEY_DOWN` Ctrl</code>
- Action 3: <code>`CLICK` slide 24</code>
- Action 4: <code>`KEY_UP` Ctrl</code>

### 2. Inspect a text object's current font color

Skill ID: `70bca0cc-c117-427e-b0be-4df7299ebeb6.skill-01`

Procedure:

1. Select the slide containing the text object.
2. Click the text box once to select it, then open the Font Color drop-down on the toolbar.
3. Use the color currently indicated for the selected text as the reference color. For example, inspect a slide title before applying the same color elsewhere.

Efficiency tip: Open the color control only after selecting the text object; otherwise the displayed color may reflect a default or a different selection.

Source task: `70bca0cc-c117-427e-b0be-4df7299ebeb6`

Source instruction: Make the background color of slide 2 same as the color of its title.

Directly referenced source actions:

- Action 0: <code>`CLICK` slide 2</code>
- Action 1: <code>`CLICK &#x27;Our customers love us&#x27; text box</code>
- Action 2: <code>`CLICK` font color dropdown</code>

### 3. Set an exact font size for text in a text box

Skill ID: `3161d64e-3120-47b4-aaad-6a764a92493b.skill-01`

Procedure:

1. Select the slide containing the text box from the Slides pane.
2. Enter text-editing mode in the target text box and select the text whose size should change; for example, triple-click within the text to select its paragraph or text content.
3. Click the font-size field on the formatting toolbar, replace its current value with an exact point size such as 60 pt, and press Enter to apply it.
4. Repeat the same process for any other text object needing a different size, such as entering 28 pt for a second text box.

Efficiency tip: Type the desired point value directly into the font-size field instead of searching the dropdown list; this is faster and supports sizes not shown among preset options.

Source task: `3161d64e-3120-47b4-aaad-6a764a92493b`

Source instruction: Make the first textbox font size 60 pt while the second 28 pt on slide 14.

Directly referenced source actions:

- Action 0: <code>`SCROLL` down to slide 14.</code>
- Action 1: <code>`CLICK` slide 14.</code>
- Action 2: <code>`TRIPLE_CLICK` target audience</code>
- Action 3: <code>`TRIPLE_CLICK` font size text field</code>
- Action 4: <code>`TYPING` 60 pt</code>
- Action 5: <code>`PRESS` enter</code>
- Action 6: <code>`TRIPLE_CLICK` &#x27;Elaborate...&#x27;</code>
- Action 7: <code>`TRIPLE_CLICK` font size dropdown</code>
- Action 8: <code>`TYPING` 28 pt</code>
- Action 9: <code>`PRESS` enter</code>

### 4. Set the font size of selected text

Skill ID: `5c1a6c3d-c1b3-47cb-9b01-8d1b7544ffa1.skill-03`

Procedure:

1. Keep the target text selected in its text object.
2. Open the font-size dropdown on the formatting toolbar.
3. Choose the required point size; for example, select 44 pt to make selected title text 44 points.

Efficiency tip: Set the size on an existing text selection before clicking elsewhere, which preserves the target range and avoids re-entering text-editing mode.

Source task: `5c1a6c3d-c1b3-47cb-9b01-8d1b7544ffa1`

Source instruction: Bold the text on slide 1. Make the title of size 44pt and underline it on slide 1.

Directly referenced source actions:

- Action 4: <code>`CLICK` font size dropdown</code>
- Action 5: <code>`CLICK` 44 pt</code>

## Initial artifact

- Domain: Neighborhood repair café workshop operations
- Presentation: [initial_artifact.pptx](artifact/initial_artifact.pptx)
- Blueprint: [artifact_blueprint.json](artifact/artifact_blueprint.json)
- QA report: [artifact_qa.json](artifact/artifact_qa.json)

Initial state:

- The deck contains three editable wide-format slides using a warm linen cover background and a restrained repair-workshop visual system.
- Slide 1 headline reads “Neighborhood Repair Café” in copper #B85C38 at 40 pt; it is the approved color reference but has not yet been inspected through the font-color control.
- Slide 2 is titled “Repair Table Flow” in dark teal #244653 at 36 pt. It has a light blue-gray background #EFF6F6 and a three-step process diagram.
- Slide 3 is titled “Open the Station” in dark teal #244653 at 36 pt. It has a pale peach background #F8E9DD, a checklist, and the schedule line “Tool check-in closes at 09:50” at 22 pt.
- The activity-slide titles do not yet match the cover headline color, the two activity-slide backgrounds are visibly different, the Slide 2 title is not 44 pt, and the Slide 3 schedule cue is not 27 pt.

Artifact construction requirements:

- Build all listed objects as normal editable text boxes and editable shapes; do not use native placeholders, notes, animations, or external media.
- Use the intended shared activity-slide background color #E3EAD7 after editing; retain the cover background #F7F1E8.
- Place the Slide 2 process steps horizontally across the lower half, and arrange the Slide 3 checklist left of the supplies panel to make both slides visibly related but distinct.
- Use the exact text strings stated in the initial-state descriptions so a reviewer can identify the title and schedule-line targets unambiguously.

| Slide | Layout | Purpose | Editable objects |
| ---: | --- | --- | --- |
| 1 | title | Cover and approved visual-color reference | cover_headline_reference (text), cover_subtitle (text), cover_workbench_illustration (shape), cover_footer_tag (shape) |
| 2 | process | Repair table workflow for volunteer hosts | flow_slide_title (text), flow_intro_text (text), flow_step_intake (shape), flow_step_sort (shape), flow_step_handoff (shape), flow_connector_one (shape), flow_connector_two (shape) |
| 3 | two_column | Opening-station timing and host readiness | timing_slide_title (text), timing_schedule_cue (text), timing_checklist_text (text), timing_supply_panel (shape), timing_supply_list (text), timing_clock_badge (shape) |

Must remain incomplete before recording:

- Do not pre-match the activity-slide title colors to the cover headline.
- Do not pre-apply the shared pale-sage #E3EAD7 background to Slides 2 and 3.
- Do not pre-size the Slide 2 title to 44 pt or the Slide 3 schedule cue to 27 pt.
- Do not alter the cover headline’s copper reference color, body text, workflow wording, or slide order.

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

- Skill: `9ec204e4-f0a3-42f8-8458-b772a6797cab.skill-01`
- Intent: Build a two-slide selection for the related activity slides before applying their shared background treatment.
- Efficiency: Click Slide 2, then Ctrl-click Slide 3 so the common background can be applied as one grouped slide operation.
- Visible success: Slides 2 and 3 are simultaneously highlighted in the Slides pane, and both subsequently show the same pale-sage background.

### Demonstration 2

- Skill: `70bca0cc-c117-427e-b0be-4df7299ebeb6.skill-01`
- Intent: Verify the approved copper title color from the cover headline before using it on the activity-slide titles.
- Efficiency: Select the cover headline itself before opening the font-color control, rather than relying on a toolbar default.
- Visible success: With the cover headline selected, the font-color control indicates the copper reference color; both activity titles later visibly match that hue.

### Demonstration 3

- Skill: `3161d64e-3120-47b4-aaad-6a764a92493b.skill-01`
- Intent: Set the Slide 3 operational schedule line to its non-preset exact size of 27 pt.
- Efficiency: Enter text-editing mode, select the complete schedule line, type 27 in the font-size field, and confirm it.
- Visible success: The full “Tool check-in closes at 09:50” line is visibly larger than its initial state and reports 27 pt when its text is selected.

### Demonstration 4

- Skill: `5c1a6c3d-c1b3-47cb-9b01-8d1b7544ffa1.skill-03`
- Intent: Use the font-size dropdown to promote the Slide 2 workflow title to 44 pt.
- Efficiency: Keep the title text selected while choosing 44 pt from the size list so the formatting applies only to that title.
- Visible success: The selected “Repair Table Flow” title is visibly more prominent and reports 44 pt.

Recording start: Open the generated presentation in normal editing view with all three slide thumbnails visible and no text object selected.

Recording end: Slides 2 and 3 share pale-sage backgrounds and copper titles; the Slide 2 title is 44 pt and the Slide 3 schedule line is 27 pt.

Allowed variation: Minor selection and toolbar-navigation paths may vary, provided the specified objects, colors, font sizes, shared backgrounds, and slide order are preserved.

## Expected incidental operations

- **task_specific:** Apply the inspected copper #B85C38 font color to the titles on Slides 2 and 3. Reason: The task requires the activity-slide titles to match the verified cover-headline color.
- **task_specific:** Apply pale-sage #E3EAD7 as the shared background for the selected activity slides. Reason: This is the visible shared treatment requested for the two related activity slides after their thumbnail multi-selection.

## Source-similarity audit

| Measure | Maximum | Most similar source task |
| --- | ---: | --- |
| Lexical sequence similarity | 0.289121 | 9ec204e4-f0a3-42f8-8458-b772a6797cab |
| Semantic cosine similarity | 0.540673 | a53f80cd-4a90-4490-8310-097b011433f6 |

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
  --reference-task-id reference-task-impress-full-v2-r01-003
```

The ordinary launcher reads the collected central review file and refuses pending, revision-requested, or rejected tasks.
