# Dawn Marsh Survey

- Reference task: `reference-task-impress-full-r01-005`
- Application: `libreoffice_impress`
- Review decision: `pending`

## Task instruction

Finalize the “Dawn Marsh Survey” checklist slide for the field-team handoff: give the slide a solid midnight-teal background; convert the three unbulleted readiness statements in the checklist panel into a bulleted list; recolor the full “Launch window: 08:30” line to Yellow; underline every character in the “Carry spare batteries” reminder box; and remove the three pale draft-marker shapes clustered in the upper-right corner with one marquee selection. Keep the rest of the briefing deck unchanged.

## Required skills

### 1. Apply bulleted-list formatting to text in a content placeholder

Skill ID: `f23acfd2-c485-4b7c-a1e7-d4303ddfe864.skill-01`

Procedure:

1. Select the text box or content placeholder that contains the paragraph to format.
2. Open the List control from the Impress toolbar or sidebar and choose the bullet-list option.
3. Impress applies bullet formatting to the current paragraph or selected paragraphs; click in a paragraph before applying the command when no text range is selected.

Efficiency tip: Place the text cursor in the target paragraph before opening the List control, so the bullet style is applied without selecting unrelated text.

Source task: `f23acfd2-c485-4b7c-a1e7-d4303ddfe864`

Source instruction: Add a bullet point to the content of this slide.

Directly referenced source actions:

- Action 0: <code>`CLICK` text box for content</code>
- Action 1: <code>`CLICK` List dropdown</code>
- Action 2: <code>`CLICK` bullet icon</code>

### 2. Set a slide background to a solid color

Skill ID: `9cf05d24-6bd9-4dae-8967-f67d88f5d38a.skill-01`

Procedure:

1. With the target slide active, open the slide background formatting control.
2. Choose the Color background option.
3. Open the color palette and select a desired solid color, for example a green swatch.

Efficiency tip: Select the target slide before opening background formatting so the chosen color is applied directly without revisiting the control.

Source task: `9cf05d24-6bd9-4dae-8967-f67d88f5d38a`

Source instruction: Move to slide 1 and give it a green background color.

Directly referenced source actions:

- Action 0: <code>`CLICK` background dropdown menu</code>
- Action 1: <code>`CLICK` Color</code>
- Action 2: <code>`CLICK` the color dropdown</code>
- Action 3: <code>`CLICK` Green (2nd row, 2nd from right)</code>

### 3. Marquee-select several slide objects and delete them

Skill ID: `a53f80cd-4a90-4490-8310-097b011433f6.skill-03`

Procedure:

1. Open the slide containing the objects to remove.
2. Start in an empty area just outside the upper-left edge of the target object cluster, then drag a selection rectangle to an opposite corner so that all intended objects are enclosed.
3. Press Delete to remove every selected object from the slide.

Efficiency tip: Begin and end the marquee in blank slide space where possible. This reduces the risk of entering text-editing mode or moving an object instead of selecting the group.

Source task: `a53f80cd-4a90-4490-8310-097b011433f6`

Source instruction: Set the font color of the title in slides 2 to 3 as black and bold the title. Also, delete the personal information (including the icons)in slide 4.

Directly referenced source actions:

- Action 9: <code>`CLICK` slide 4</code>
- Action 10: <code>`MOVE_TO` top left corner of the location icon with some padding</code>
- Action 11: <code>`DRAG_TO` where bottom left corner of the pink image is</code>
- Action 12: <code>`PRESS` delete.</code>

### 4. Set selected text color from the font-color palette

Skill ID: `57667013-ea97-417c-9dce-2713091e6e2a.skill-01`

Procedure:

1. Click inside a text box to enter text-editing mode, rather than merely selecting the shape border.
2. Select the text to recolor, for example with Ctrl+A when all text in the active text box should be affected.
3. Open the Font Color drop-down on the formatting toolbar.
4. Choose the desired color swatch from the palette, for example the standard Yellow swatch. The selected text adopts that color.

Efficiency tip: Use Ctrl+A only after the text cursor is active inside the intended text box; otherwise it may select slide objects instead of the box's text.

Source task: `57667013-ea97-417c-9dce-2713091e6e2a`

Source instruction: Navigate to slide 5 and set the font color of all textboxes to yellow. Use exactly 'yellow'—no variations such as light yellow, dark yellow, or any other color.

Directly referenced source actions:

- Action 1: <code>`CLICK` text in &#x27;write an original...&#x27;</code>
- Action 2: <code>`HOTKEY` ctrl-A</code>
- Action 3: <code>`CLICK` font color dropdown.</code>
- Action 4: <code>`CLICK` yellow (2nd row, first from left)</code>

### 5. Underline all text in a text box

Skill ID: `ed43c15f-00cb-4054-9c95-62c880865d68.skill-01`

Procedure:

1. Enter text-editing mode for the text box, for example by double-clicking its text so that a caret appears.
2. Press Ctrl+A to select the text within the active text box. In text-editing mode this selects text rather than all slide objects.
3. Press Ctrl+U to toggle underline formatting for the selected text.
4. Repeat on other text boxes as needed; Ctrl+U applies the same underline technique to each independently selected text range.

Efficiency tip: Use Ctrl+A followed by Ctrl+U while the caret is inside each text box to format its full contents without manually dragging across the text.

Source task: `ed43c15f-00cb-4054-9c95-62c880865d68`

Source instruction: Move the picture on page 2 to slide top. Make textboxes underlined on slide 1 and 2.

Directly referenced source actions:

- Action 0: <code>`HOTKEY` ctrl-a</code>
- Action 1: <code>`HOTKEY` ctrl-U</code>
- Action 3: <code>`HOTKEY` ctrl-a</code>
- Action 4: <code>`HOTKEY` ctrl-U</code>

## Initial artifact

- Domain: wetland field-survey briefing
- Presentation: [initial_artifact.pptx](artifact/initial_artifact.pptx)
- Blueprint: [artifact_blueprint.json](artifact/artifact_blueprint.json)
- QA report: [artifact_qa.json](artifact/artifact_qa.json)

Initial state:

- The deck opens on slide 1, with slide 2 containing every target object in an intentionally unfinished checklist layout.
- Slide 2 has a solid warm off-white background (#F7F4EC), not the requested midnight teal (#0B3D4A).
- The editable readiness_list_text contains three separate unbulleted paragraphs: “Calibrate water meter”, “Pack sample envelopes”, and “Confirm trail access”.
- The full editable launch_time_status text reads “Launch window: 08:30” in the theme's dark teal text color, not Yellow.
- The editable battery_reminder_box reads “Carry spare batteries” with no underline formatting.
- draft_marker_one, draft_marker_two, and draft_marker_three are three small pale circular shapes arranged as a compact upper-right cluster, fully enclosed by a single empty-space marquee without enclosing retained content.
- All other slide 2 objects are positioned outside the removable-marker cluster and should remain unchanged.

Artifact construction requirements:

- Build a clean, editable two-slide PPTX using only text boxes and shapes; do not use native title or content placeholders.
- Use a restrained survey-field visual style: off-white paper base, deep teal headings, pale sage panels, and a Yellow accent reserved for the requested launch-time status.
- On slide 2, place the heading across the upper left, the readiness panel in the left two-thirds, the launch-time status near the lower left, and the battery reminder in a small outlined box below it.
- Place the three removable pale circles in the upper-right quadrant with clear blank margin around their group so a reviewer can perform an unambiguous single marquee deletion.
- The desired final review state is slide 2 with a #0B3D4A solid background, three bullet paragraphs in the readiness list, the entire launch-time line in standard Yellow, a fully underlined battery reminder, and no draft-marker circles.

| Slide | Layout | Purpose | Editable objects |
| ---: | --- | --- | --- |
| 1 | title | Briefing cover that establishes the survey identity and provides context for the checklist slide. | cover_title (text), cover_subtitle (text), cover_horizon_band (shape), cover_location_badge (shape), cover_location_label (text) |
| 2 | two_column | Field-team setup checklist to be finalized before departure. | checklist_heading_band (shape), checklist_slide_heading (text), checklist_intro_panel (shape), checklist_intro_label (text), readiness_list_panel (shape), readiness_list_text (text), launch_time_status (text), battery_reminder_panel (shape), battery_reminder_box (text), route_note_panel (shape), route_note (text), draft_marker_one (shape), draft_marker_two (shape), draft_marker_three (shape) |

Must remain incomplete before recording:

- Do not apply bullet formatting to readiness_list_text before the operator demonstration.
- Do not set slide 2's background to midnight teal before the operator demonstration.
- Do not recolor launch_time_status to Yellow before the operator demonstration.
- Do not underline battery_reminder_box before the operator demonstration.
- Do not delete any of the three draft-marker shapes before the operator demonstration.
- Do not alter slide 1 or delete retained slide 2 content.

Artifact previews:

### contact-sheet

![contact-sheet.png](artifact/previews/contact-sheet.png)

### slide-01

![slide-01.png](artifact/previews/slide-01.png)

### slide-02

![slide-02.png](artifact/previews/slide-02.png)

## Operator guide

### Demonstration 1

- Skill: `f23acfd2-c485-4b7c-a1e7-d4303ddfe864.skill-01`
- Intent: Turn the three readiness statements in the checklist text area into a bulleted list.
- Efficiency: Activate the checklist text area and place the caret in a readiness paragraph before using the bullet-list control; select all three list paragraphs if needed.
- Visible success: Each of the three readiness statements has a visible bullet, with no bullets added to the heading, status line, or reminder.

### Demonstration 2

- Skill: `9cf05d24-6bd9-4dae-8967-f67d88f5d38a.skill-01`
- Intent: Apply the requested solid midnight-teal background to the active checklist slide.
- Efficiency: Select slide 2 before opening the slide-background control so the color is applied only to the checklist slide.
- Visible success: The entire slide canvas behind all objects is a uniform midnight teal (#0B3D4A), while the content objects remain in place.

### Demonstration 3

- Skill: `a53f80cd-4a90-4490-8310-097b011433f6.skill-03`
- Intent: Remove the three obsolete pale draft markers together.
- Efficiency: Drag from blank space just outside the cluster to blank space beyond its opposite edge, ensuring the selection rectangle encloses only the three circles before pressing Delete.
- Visible success: All three upper-right pale circles disappear, while the heading, checklist panel, route note, status line, and reminder remain visible.

### Demonstration 4

- Skill: `57667013-ea97-417c-9dce-2713091e6e2a.skill-01`
- Intent: Set the complete launch-window status line to Yellow.
- Efficiency: Enter text-editing mode in the status line and select its full text before choosing the standard Yellow swatch from the font-color palette.
- Visible success: Every character in “Launch window: 08:30” is Yellow, with no other text recolored by this operation.

### Demonstration 5

- Skill: `ed43c15f-00cb-4054-9c95-62c880865d68.skill-01`
- Intent: Underline the entire battery reminder text box.
- Efficiency: Place a caret inside the reminder text box, select all text within that box, then use the underline shortcut.
- Visible success: Every character in “Carry spare batteries” has an underline; the surrounding outlined box itself is unchanged.

Recording start: Open the supplied two-slide PPTX in LibreOffice Impress with slide 2 available in normal editing view and all described unfinished elements present.

Recording end: Slide 2 shows the midnight-teal background, a three-item bulleted readiness list, Yellow launch-time text, a fully underlined battery reminder, and the former upper-right draft-marker cluster removed.

Allowed variation: Equivalent LibreOffice Impress controls, menus, keyboard shortcuts, or toolbar paths are acceptable as long as the specified final slide state is produced and unrelated objects remain unchanged.

## Expected incidental operations

- **substantive_prerequisite:** Navigate from the cover to slide 2 and make it the active slide before slide-level editing. Reason: All requested changes are confined to the checklist slide.
- **task_specific:** Enter text-editing mode and select only the required text range inside each target text box. Reason: The requested font-color and underline changes apply to text rather than to the text-box border or other objects.
- **scaffolding:** Click an empty area after deleting the marker cluster to verify that no retained object remains selected. Reason: This makes it easy to confirm that only the obsolete shapes were removed.

## Source-similarity audit

| Measure | Maximum | Most similar source task |
| --- | ---: | --- |
| Lexical sequence similarity | 0.270115 | 04578141-1d42-4146-b9cf-6fab4ce5fd74 |
| Semantic cosine similarity | 0.525726 | 04578141-1d42-4146-b9cf-6fab4ce5fd74 |

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
  --reference-task-id reference-task-impress-full-r01-005
```

The ordinary launcher reads the collected central review file and refuses pending, revision-requested, or rejected tasks.
