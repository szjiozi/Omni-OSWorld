# Regional Funding Board View

- Reference task: `reference-task-calc-full-r01-002`
- Application: `libreoffice_calc`
- Review decision: `pending`

## Task instruction

Prepare the board-ready funding view by duplicating each initiative's planned allocation into the blank Board View column and displaying those copied amounts as rounded billions with one decimal place and a spaced B suffix.

## Required skills

### 1. Paste copied cells into a different column

Skill ID: `21df9241-f8d7-4509-b7f1-37e501a823f7.skill-03`

Procedure:

1. With copied cells still on the clipboard, click the top destination cell in another column, for example C2.
2. Press Ctrl+V to paste the copied range beginning at that cell.

Efficiency tip: After copying, use Ctrl+V immediately in the target cell; this is faster and less error-prone than reselecting and duplicating content manually.

Source task: `21df9241-f8d7-4509-b7f1-37e501a823f7`

Source instruction: Change the representation of column "Parameter" to show in Millions (M) in Column B and Billions (B) in Column C. The numbers should be rounded to one decimal place, and half should be rounded up. Then remember to place a white space between the digits and the unit.

Directly referenced source actions:

- Action 10: <code>`CLICK` C2</code>
- Action 11: <code>`HOTKEY` CTRL-V</code>

### 2. Format values as rounded billions with a spaced unit suffix

Skill ID: `21df9241-f8d7-4509-b7f1-37e501a823f7.skill-04`

Procedure:

1. Select the cells to format, right-click, and choose Format Cells.
2. Activate the format-code field and enter `0.0,,, \B`, then confirm with Enter.
3. The three trailing commas scale the display by one billion, `0.0` shows one decimal place, and the literal space before `\B` leaves a space before the B suffix. For example, 12500000000 displays as `12.5 B`.

Efficiency tip: Use comma scaling in a custom format instead of changing underlying values, so calculations retain their original precision and magnitude.

Source task: `21df9241-f8d7-4509-b7f1-37e501a823f7`

Source instruction: Change the representation of column "Parameter" to show in Millions (M) in Column B and Billions (B) in Column C. The numbers should be rounded to one decimal place, and half should be rounded up. Then remember to place a white space between the digits and the unit.

Directly referenced source actions:

- Action 12: <code>`RIGHT_CLICK`</code>
- Action 13: <code>`CLICK` &#x27;Format Cells...&#x27;</code>
- Action 14: <code>`DOUBLE_CLICK` format code box</code>
- Action 15: <code>`TYPING` &#x27;0.0,,, \B&#x27;</code>
- Action 16: <code>`PRESS` enter</code>

## Initial state preview

### Funding Plan

![Funding_Plan.png](artifact/previews/Funding_Plan.png)

## Operator guide

### Existing operation-intent guide

#### Demonstration 1

- Skill: `21df9241-f8d7-4509-b7f1-37e501a823f7.skill-03`
- Intent: Paste the copied planned-allocation values into the blank Board View column beginning at C2.
- Efficiency: Copy the contiguous source range once, then paste starting at the top destination cell so Calc fills the matching range in one action.
- Visible success: C2:C11 are populated with the same underlying numeric amounts as B2:B11, while the Initiative and source columns remain unchanged.

#### Demonstration 2

- Skill: `21df9241-f8d7-4509-b7f1-37e501a823f7.skill-04`
- Intent: Format the populated Board View values as rounded billions with one decimal place and a space before the B unit suffix.
- Efficiency: Apply a comma-scaled custom number format to the whole Board View range rather than changing the underlying amounts; use a one-decimal billions format with a literal spaced B suffix (for example, `0.0,,, \B`).
- Visible success: The Board View column shows values such as 12.5 B, 8.8 B, and 3.6 B, while the formula/input line retains the full raw amounts.

Recording start: The Funding Plan sheet is open with populated source values in B2:B11 and a blank Board View destination range C2:C11.

Recording end: The Funding Plan sheet has B2:B11 copied into C2:C11, and every Board View entry displays as a one-decimal rounded number of billions followed by a spaced B suffix.

Allowed variation: The expert may use keyboard shortcuts, menus, the format dialog, or another equivalent LibreOffice Calc method. The pasted values must remain numeric and the Board View display must visibly use a single decimal place, a space, and the B suffix.

### 中文详细参考方案

> 以下是一个可以参考的操作 guide。标注者可以根据实际 LibreOffice 界面采用等价操作。

本指南将把 `Funding Plan` 中的 Planned Allocation 金额复制到空白的 Board View 列，然后只通过自定义数字格式把该列显示为“十亿、保留一位小数、空格加 B 后缀”的董事会视图。底层金额将保持原始数值，方便后续计算。

#### 启动后的初始状态检查

- 确认当前打开的工作表是 `Funding Plan`。
- 确认第 1 行是标题行，`B2:B11` 含有数值金额，且 `C2:C11` 的 Board View 区域仍为空白。
- 确认列 B 的金额是可计算的数值而非文本；选择例如 B2 时，输入行/公式栏应显示完整金额。
- 确认 Board View 列尚未显示类似 `12.5 B` 的十亿缩放格式。

#### 第 1 步：复制 Planned Allocation 金额

1. 选中源金额区域 `B2:B11`，不要包含标题单元格 B1。
2. 按 `Ctrl+C` 复制所选金额。此时可见移动边框，表示该区域仍在剪贴板中可供粘贴。

- 对应 skills：无；这是准备或检查步骤。
- 高效操作：一次选中完整连续区域并复制，可避免逐行复制时漏掉项目或错位。
- 完成标志：`B2:B11` 周围出现复制边框，且 Board View 的 `C2:C11` 仍为空白。

#### 第 2 步：将复制的金额粘贴到 Board View

1. 在复制边框仍存在时，单击目标起始单元格 C2。
2. 按 `Ctrl+V`，将复制的范围从 C2 开始粘贴到 Board View 列。
3. 确认粘贴覆盖的是 `C2:C11`，不要修改 A 列 Initiative 或 B 列源金额。

- 对应 skills：`21df9241-f8d7-4509-b7f1-37e501a823f7.skill-03`
- 高效操作：复制后立即从目标区域的第一个单元格粘贴，Calc 会自动将整段连续数据按相同行数填入，无需逐项处理。
- 完成标志：`C2:C11` 已全部填入，并与对应的 `B2:B11` 具有相同的底层金额；例如 C2 包含 `12450000000`。

#### 第 3 步：将 Board View 格式化为十亿显示

1. 选中刚粘贴的区域 `C2:C11`。
2. 在所选区域上右键单击，选择 `Format Cells...`。
3. 在打开的对话框中找到用于输入自定义格式代码的输入框，激活或选中其中现有的格式代码。
4. 输入 `0.0,,, \B`，然后按 `Enter` 确认并应用格式。三个逗号会按十亿缩放显示，`0.0` 保留一位小数，反斜杠后的 `B` 作为带前置空格的文字后缀显示。

- 对应 skills：`21df9241-f8d7-4509-b7f1-37e501a823f7.skill-04`
- 高效操作：使用自定义数字格式缩放显示，而不是用公式或除法改写数值；这样能保留完整原始金额并一次格式化整列目标区域。
- 完成标志：`C2:C11` 显示为一位小数加空格和 `B`，例如 C2 显示 `12.5 B`、C3 显示 `8.8 B`、C4 显示 `3.6 B`。

#### 最终结果检查

- 在 `Funding Plan` 工作表中，`C2:C11` 均已填入数值，且 `B2:B11` 的原始金额和 Initiative 列没有被改动。
- Board View 显示为带一位小数、数字与单位间有空格的十亿单位，例如 `12.5 B`、`8.8 B`、`3.6 B`。
- 单击任一 Board View 单元格（例如 C2）时，输入行/公式栏显示完整的底层金额 `12450000000`，而不是已缩放的 `12.5`；这确认仅改变显示格式，未改变数值。
- 检查 C2:C11 的所有条目均使用相同的十亿显示格式，并保留一位小数和 `B` 后缀。

## Source-task similarity review

| Measure | Maximum | Most similar source task |
| --- | ---: | --- |
| Lexical sequence similarity | 0.382979 | 1de60575-bb6e-4c3d-9e6a-2fa699f9f197 |
| Semantic cosine similarity | 0.474372 | 21df9241-f8d7-4509-b7f1-37e501a823f7 |

Similarity scores are reviewer aids, not automatic acceptance thresholds. Inspect the contributing source tasks and their complete ordered actions below.

### Source task `21df9241-f8d7-4509-b7f1-37e501a823f7`

Original instruction:

> Change the representation of column "Parameter" to show in Millions (M) in Column B and Billions (B) in Column C. The numbers should be rounded to one decimal place, and half should be rounded up. Then remember to place a white space between the digits and the unit.

Required skills derived from this source task:

- **Paste copied cells into a different column** — `21df9241-f8d7-4509-b7f1-37e501a823f7.skill-03`
- **Format values as rounded billions with a spaced unit suffix** — `21df9241-f8d7-4509-b7f1-37e501a823f7.skill-04`

Complete ordered single-action sequence:

| Action | Related required skill | Original single action |
| ---: | --- | --- |
| 0 |  | <code>`CLICK A2</code> |
| 1 |  | <code>`DRAG_TO A8</code> |
| 2 |  | <code>`HOTKEY` CTRL-C</code> |
| 3 |  | <code>`CLICK` B2</code> |
| 4 |  | <code>`HOTKEY` CTRL-V</code> |
| 5 |  | <code>`RIGHT_CLICK`</code> |
| 6 |  | <code>`CLICK` &#x27;Format Cells...&#x27;</code> |
| 7 |  | <code>`DOUBLE_CLICK` format code box</code> |
| 8 |  | <code>`TYPING` &#x27;0.0,, \M&#x27;</code> |
| 9 |  | <code>`PRESS` enter</code> |
| 10 | <strong>★ Paste copied cells into a different column</strong><br><code>21df9241-f8d7-4509-b7f1-37e501a823f7.skill-03</code> | <strong><code>`CLICK` C2</code></strong> |
| 11 | <strong>★ Paste copied cells into a different column</strong><br><code>21df9241-f8d7-4509-b7f1-37e501a823f7.skill-03</code> | <strong><code>`HOTKEY` CTRL-V</code></strong> |
| 12 | <strong>★ Format values as rounded billions with a spaced unit suffix</strong><br><code>21df9241-f8d7-4509-b7f1-37e501a823f7.skill-04</code> | <strong><code>`RIGHT_CLICK`</code></strong> |
| 13 | <strong>★ Format values as rounded billions with a spaced unit suffix</strong><br><code>21df9241-f8d7-4509-b7f1-37e501a823f7.skill-04</code> | <strong><code>`CLICK` &#x27;Format Cells...&#x27;</code></strong> |
| 14 | <strong>★ Format values as rounded billions with a spaced unit suffix</strong><br><code>21df9241-f8d7-4509-b7f1-37e501a823f7.skill-04</code> | <strong><code>`DOUBLE_CLICK` format code box</code></strong> |
| 15 | <strong>★ Format values as rounded billions with a spaced unit suffix</strong><br><code>21df9241-f8d7-4509-b7f1-37e501a823f7.skill-04</code> | <strong><code>`TYPING` &#x27;0.0,,, \B&#x27;</code></strong> |
| 16 | <strong>★ Format values as rounded billions with a spaced unit suffix</strong><br><code>21df9241-f8d7-4509-b7f1-37e501a823f7.skill-04</code> | <strong><code>`PRESS` enter</code></strong> |

## Review this package

Before choosing a decision, complete all three checks:

- [ ] **Task naturalness and skill necessity:** Is the reference task a natural Calc task, and is every listed required skill genuinely necessary and observable when solving it?
- [ ] **Initial artifact correctness:** Launch the environment and confirm that the workbook opens correctly, contains the data needed by the instruction, and has not already completed the requested results.
- [ ] **Source-task similarity:** Compare the reference task with the source instructions and complete single-action sequences above. Confirm that it is not merely an entity, field, or value substitution and does not reproduce a source task's complete ordered solution.

Use `approved` when all checks pass. Use `revision_requested` when the package is fixable and provide concrete revision instructions. Use `rejected` when the combination is fundamentally unnatural, infeasible, or too similar to a source task.

Fill [review.json](review.json), then collect completed forms from the repository root:

```bash
python scripts/python/manage_reference_review_packets.py collect \
  --skill-pool evaluation_examples/expert_skill_learning/calc_full_v1/generated/skill_pool.json \
  --packages evaluation_examples/expert_skill_learning/calc_full_v1/generated/round_01/reference_packages.json \
  --source-tasks evaluation_examples/expert_skill_learning/calc_full_v1/source_tasks.json \
  --reviews evaluation_examples/expert_skill_learning/calc_full_v1/generated/round_01/reference_package_reviews.json \
  --artifact-manifest evaluation_examples/expert_skill_learning/calc_full_v1/generated/round_01/artifacts/artifact_manifest.json \
  --task-config-manifest evaluation_examples/expert_skill_learning/calc_full_v1/generated/round_01/task_config_manifest.json \
  --task-detail-root evaluation_examples/expert_skill_learning/calc_full_v1/generated/round_01/task_details \
  --reviewer-guides evaluation_examples/expert_skill_learning/calc_full_v1/generated/round_01/reviewer_guides.json \
  --coverage evaluation_examples/expert_skill_learning/calc_full_v1/generated/round_01/coverage_state.json \
  --packet-root evaluation_examples/expert_skill_learning/calc_full_v1/review_packets/round_01
```

Detailed field guidance is in [`reviewer.md`](../../../../reviewer.md).
