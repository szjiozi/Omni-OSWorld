# Garden Volunteer Activity

- Reference task: `reference-task-calc-full-r01-010`
- Application: `libreoffice_calc`
- Review decision: `pending`

## Task instruction

Create a Pivot Table on a new summary sheet that shows total volunteer service hours for each garden program, with the quarters displayed as column headings.

## Required skills

### 1. Add a numeric field as a Pivot Table data measure

Skill ID: `1de60575-bb6e-4c3d-9e6a-2fa699f9f197.skill-03`

Procedure:

1. Locate the numeric field to summarize in the Available Fields list.
2. Drag it to the Data fields box. For example, dragging “Revenue” to Data fields configures the Pivot Table to aggregate that numeric field.
3. Confirm the Pivot Table layout dialog to create or update the Pivot Table with the configured data measure.

Efficiency tip: Place numeric fields in Data fields only once the row/column layout is set, so it is easier to verify which measure will be summarized.

Source task: `1de60575-bb6e-4c3d-9e6a-2fa699f9f197`

Source instruction: Summarize the total revenue for each promotion type in a new sheet (Sheet2) with the promotion names as the column headers using the Pivot Table feature.

Directly referenced source actions:

- Action 5: <code>`MOVE_TO` &#x27;Revenue&#x27; in available fields section&#x27;</code>
- Action 6: <code>`DRAG_TO` &#x27;Data fields&#x27; box</code>
- Action 7: <code>`CLICK` ok</code>

### 2. Place a field in the Pivot Table column area

Skill ID: `1de60575-bb6e-4c3d-9e6a-2fa699f9f197.skill-02`

Procedure:

1. In the Pivot Table layout dialog, locate the desired categorical field in Available Fields.
2. Drag that field into the Column fields box. For example, dragging a field such as “Promotion” to Column fields creates a separate column heading for each distinct value.

Efficiency tip: Drag fields directly from Available Fields to the desired layout box instead of adding them first and repositioning them afterward.

Source task: `1de60575-bb6e-4c3d-9e6a-2fa699f9f197`

Source instruction: Summarize the total revenue for each promotion type in a new sheet (Sheet2) with the promotion names as the column headers using the Pivot Table feature.

Directly referenced source actions:

- Action 3: <code>`MOVE_TO` &#x27;Promotion&#x27; in available fields section</code>
- Action 4: <code>`DRAG_TO` &#x27;Column fields&#x27; box</code>

## Initial state preview

### Activity Log

![Activity_Log.png](artifact/previews/Activity_Log.png)

## Operator guide

### Existing operation-intent guide

#### Demonstration 1

- Skill: `1de60575-bb6e-4c3d-9e6a-2fa699f9f197.skill-03`
- Intent: In the Pivot Table layout, add the Service Hours numeric field to the Data fields area so the report aggregates volunteer time.
- Efficiency: Set the row and column layout before adding the numeric measure so the intended cross-tab structure is easy to inspect.
- Visible success: The completed Pivot Table displays aggregated Service Hours values rather than individual activity records.

#### Demonstration 2

- Skill: `1de60575-bb6e-4c3d-9e6a-2fa699f9f197.skill-02`
- Intent: In the Pivot Table layout, place Quarter in the column area to split the summary into quarter headings.
- Efficiency: Drag Quarter directly from the available fields into the Column fields area rather than adding and repositioning it.
- Visible success: The completed Pivot Table has distinct Quarter headings across the top, with totals aligned under each heading.

Recording start: The workbook is open on the populated Activity Log source sheet, with no Pivot Table or summary output present.

Recording end: A visible Pivot Table summarizes total Service Hours by Program in rows and Quarter in columns on an empty destination sheet or area.

Allowed variation: The expert may use any equivalent LibreOffice Calc Pivot Table workflow, choose any clear empty output location, and may rename the output sheet. The resulting summary should preserve Program as row labels, Quarter as column headings, and aggregated Service Hours as the displayed values.

### 中文详细参考方案

> 以下是一个可以参考的操作 guide。标注者可以根据实际 LibreOffice 界面采用等价操作。

在 `Activity Log` 的完整活动记录上创建 Pivot Table，并将结果放到新的空白工作表或空白输出区域。布局应为：`Program` 在行、`Quarter` 在列、`Service Hours` 作为数值汇总，以便按园艺项目和季度查看志愿服务总小时数。

#### 启动后的初始状态检查

- 确认当前活动工作表是 `Activity Log`。
- 确认源数据连续覆盖 `A1:E37`：第 1 行包含 `Program`、`Quarter`、`Garden Site`、`Activity Type`、`Service Hours` 标题，且中间没有空白行或空白列。
- 确认工作簿中尚未有 Pivot Table 或预先建立的汇总输出工作表。

#### 第 1 步：选择活动记录并打开 Pivot Table 布局

1. 在 `Activity Log` 中选中完整源表 `A1:E37`，务必包含标题行。
2. 点击 `Data` > `Pivot Table` > `Insert or Edit...`，使用当前选定的数据区域作为 Pivot Table 的源。
3. 继续进入用于摆放字段的 Pivot Table 布局对话框。

- 对应 skills：无；这是准备或检查步骤。
- 高效操作：先在源表内选中任意单元格，再一次性选取完整连续数据区域；这样 Pivot Table 会同时获得字段标题和所有记录。
- 完成标志：Pivot Table 布局对话框出现，并在可用字段列表中能看到 `Program`、`Quarter`、`Garden Site`、`Activity Type` 和 `Service Hours`。

#### 第 2 步：按 Program 建立行标签

1. 在可用字段列表中找到 `Program`。
2. 将 `Program` 拖到 `Row Fields` 区域，使每个园艺项目成为一行标签。
3. 检查 `Program` 已显示在 `Row Fields` 区域内。

- 对应 skills：无；这是准备或检查步骤。
- 高效操作：直接从可用字段列表拖到目标区域，避免先添加字段后再重新定位。
- 完成标志：`Row Fields` 区域中可见 `Program`，说明 Pivot Table 将按项目分行。

#### 第 3 步：将 Quarter 放入列字段区域

1. 在可用字段列表中找到 `Quarter`。
2. 将 `Quarter` 直接拖到 `Column Fields` 区域。
3. 确认 `Quarter` 留在 `Column Fields` 区域中，而非 `Row Fields` 或 `Data Fields`。

- 对应 skills：`1de60575-bb6e-4c3d-9e6a-2fa699f9f197.skill-02`
- 高效操作：将分类字段 `Quarter` 直接拖入列区域；不需要先放入其他区域再移动。
- 完成标志：`Column Fields` 区域中显示 `Quarter`，完成后各季度会横向显示为列标题。

#### 第 4 步：将 Service Hours 作为汇总数值

1. 在可用字段列表中找到数值字段 `Service Hours`。
2. 将 `Service Hours` 拖到 `Data Fields` 区域，且只放置一次。
3. 确认数据字段采用求和汇总；如果布局对话框显示该字段的汇总方式，确保它是 `Sum`，以汇总服务小时数而非计数。

- 对应 skills：`1de60575-bb6e-4c3d-9e6a-2fa699f9f197.skill-03`
- 高效操作：在行、列布局已经清楚后再添加数值字段，可立即确认该数值会按 Program 和 Quarter 交叉汇总。
- 完成标志：`Data Fields` 区域中出现 `Service Hours` 的求和数据项，表示输出将显示聚合小时数。

#### 第 5 步：输出 Pivot Table 到空白汇总位置

1. 在布局对话框中将结果位置指定为新工作表；也可以选择一个没有数据的工作表，并将输出起点设在该表的空白单元格 `A1`。
2. 确认目标位置不会与 `Activity Log` 的源数据重叠。
3. 点击 `OK` 创建 Pivot Table。
4. 如创建的是新工作表，可按需要将该工作表改为便于识别的名称，例如 `Volunteer Summary`。

- 对应 skills：无；这是准备或检查步骤。
- 高效操作：将结果放在新的空白工作表可避免覆盖原始活动记录，也使源数据与汇总报告便于区分。
- 完成标志：出现一个新的 Pivot Table：左侧是 `Program`，顶部横向显示不同的 `Quarter`，内部单元格为汇总后的 `Service Hours` 数值。

#### 第 6 步：核对完成的志愿服务小时汇总

1. 检查行区域：每个 `Program` 应作为单独的行标签。
2. 检查列区域：`Quarter` 的不同值应横向位于表格顶部。
3. 检查数值区域：各交叉单元格应是服务小时数的总和，而不是源表中的单条记录。
4. 如果某字段位置不正确，可返回 Pivot Table 编辑功能调整字段区域，然后再次确认结果。

- 对应 skills：无；这是准备或检查步骤。
- 高效操作：用交叉检查的方式核对布局：先看字段位置，再看数值是否为汇总值，可快速发现字段被放错区域的问题。
- 完成标志：Pivot Table 清晰呈现“Program × Quarter”的交叉汇总，所有可见数据值均为 `Service Hours` 的聚合值。

#### 最终结果检查

- 工作簿中存在一个单独的汇总输出区域或新工作表，且其中显示原生 Pivot Table，而不是手工输入的汇总结果。
- Pivot Table 的左侧行标签为 `Program`，每个 Program 只出现一行汇总。
- 表格顶部有 `Quarter` 的不同季度列标题，且季度下方显示对应 Program 的汇总值。
- 值区域显示的是 `Service Hours` 的聚合结果（通常为 Sum），不是逐条活动记录；行和列总计如自动显示，可保留。

## Source-task similarity review

| Measure | Maximum | Most similar source task |
| --- | ---: | --- |
| Lexical sequence similarity | 0.544747 | 535364ea-05bd-46ea-9937-9f55c68507e8 |
| Semantic cosine similarity | 0.575627 | 535364ea-05bd-46ea-9937-9f55c68507e8 |

Similarity scores are reviewer aids, not automatic acceptance thresholds. Inspect the contributing source tasks and their complete ordered actions below.

### Source task `1de60575-bb6e-4c3d-9e6a-2fa699f9f197`

Original instruction:

> Summarize the total revenue for each promotion type in a new sheet (Sheet2) with the promotion names as the column headers using the Pivot Table feature.

Required skills derived from this source task:

- **Add a numeric field as a Pivot Table data measure** — `1de60575-bb6e-4c3d-9e6a-2fa699f9f197.skill-03`
- **Place a field in the Pivot Table column area** — `1de60575-bb6e-4c3d-9e6a-2fa699f9f197.skill-02`

Complete ordered single-action sequence:

| Action | Related required skill | Original single action |
| ---: | --- | --- |
| 0 |  | <code>`HOTEKY` &#x27;ctrl-a&#x27;</code> |
| 1 |  | <code>`CLICK` curved arrow icon in the top bar representing insert or edit pivot table</code> |
| 2 |  | <code>`CLICK` ok</code> |
| 3 | <strong>★ Place a field in the Pivot Table column area</strong><br><code>1de60575-bb6e-4c3d-9e6a-2fa699f9f197.skill-02</code> | <strong><code>`MOVE_TO` &#x27;Promotion&#x27; in available fields section</code></strong> |
| 4 | <strong>★ Place a field in the Pivot Table column area</strong><br><code>1de60575-bb6e-4c3d-9e6a-2fa699f9f197.skill-02</code> | <strong><code>`DRAG_TO` &#x27;Column fields&#x27; box</code></strong> |
| 5 | <strong>★ Add a numeric field as a Pivot Table data measure</strong><br><code>1de60575-bb6e-4c3d-9e6a-2fa699f9f197.skill-03</code> | <strong><code>`MOVE_TO` &#x27;Revenue&#x27; in available fields section&#x27;</code></strong> |
| 6 | <strong>★ Add a numeric field as a Pivot Table data measure</strong><br><code>1de60575-bb6e-4c3d-9e6a-2fa699f9f197.skill-03</code> | <strong><code>`DRAG_TO` &#x27;Data fields&#x27; box</code></strong> |
| 7 | <strong>★ Add a numeric field as a Pivot Table data measure</strong><br><code>1de60575-bb6e-4c3d-9e6a-2fa699f9f197.skill-03</code> | <strong><code>`CLICK` ok</code></strong> |
| 8 |  | <code>`DOUBLE_CLICK` on name &#x27;Pivot Table_Sheet1_1&#x27;</code> |
| 9 |  | <code>`TYPING` &#x27;Sheet2&#x27;</code> |
| 10 |  | <code>`PRESS` Enter</code> |

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
