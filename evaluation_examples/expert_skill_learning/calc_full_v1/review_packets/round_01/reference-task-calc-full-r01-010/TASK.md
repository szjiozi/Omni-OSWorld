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

本任务要从 `Activity Log` 的志愿服务记录创建一个 Pivot Table。完成后的报告按 `Program` 分行、按 `Quarter` 分列，并在交叉单元格中显示 `Service Hours` 的合计。

#### 启动后的初始状态检查

- 确认当前打开的是 `Garden Volunteer Activity` 工作簿，活动工作表为 `Activity Log`。
- 确认源表从 A1 开始，第一行包含 `Program`、`Quarter`、`Garden Site`、`Activity Type`、`Service Hours`，且数据连续至第 37 行；不要在表内插入空白行或列。
- 确认尚不存在包含该汇总结果的工作表或 Pivot Table。

#### 第 1 步：选择完整的志愿活动记录作为数据源

1. 在 `Activity Log` 中选择完整源范围 A1:E37。可单击名称框并输入 `A1:E37` 后按 Enter，或从 A1 拖动选择到 E37。
2. 打开 `Data` > `Pivot Table` > `Insert or Edit...`。在数据源确认界面中，确认所用范围是 `Activity Log` 中的 A1:E37，然后继续进入 Pivot Table 布局对话框。

- 对应 skills：无；这是准备或检查步骤。
- 高效操作：先在源表内单击任意一个有数据的单元格，再一次性选择整个连续表，可避免把工作表外的空白单元格纳入数据源。
- 完成标志：Pivot Table 布局对话框打开，`Available Fields` 中可见 `Program`、`Quarter`、`Garden Site`、`Activity Type` 和 `Service Hours` 等字段。

#### 第 2 步：用 Program 建立报告行标签

1. 在 `Available Fields` 中找到 `Program`，将它拖入 `Row Fields` 区域。
2. 布局预览中应把 `Program` 作为纵向分组字段。若 `Program` 被误放到其他区域，将该字段从错误区域拖回 `Row Fields`。

- 对应 skills：无；这是准备或检查步骤。
- 高效操作：直接从 `Available Fields` 拖到目标区域，不要先添加后再重新移动字段。
- 完成标志：`Row Fields` 区域中显示 `Program`，这表示输出将按园艺项目逐行汇总。

#### 第 3 步：将 Quarter 放入列字段区域

1. 在 `Available Fields` 中找到 `Quarter`，直接拖入 `Column Fields` 区域。
2. 预期结果是 `Quarter` 将成为横向列分组；如果它已经出现在 `Column Fields` 中则无需调整。若它误出现在 `Row Fields`、`Data Fields` 或其他区域，把该字段拖到 `Column Fields`。

- 对应 skills：`1de60575-bb6e-4c3d-9e6a-2fa699f9f197.skill-02`
- 高效操作：在添加数值度量前先完成行列布局，能更清楚地核对交叉汇总表的结构。
- 完成标志：`Column Fields` 区域中显示 `Quarter`，最终报告会在顶部按季度生成不同列标题。

#### 第 4 步：将 Service Hours 作为汇总数据度量

1. 在 `Available Fields` 中找到数值字段 `Service Hours`，将它拖入 `Data Fields` 区域。
2. 数值字段通常会自动使用合计方式。若布局中已显示为服务时长合计，则无需调整。
3. 如果数据字段名称显示为计数，或完成后数字明显是记录数量而不是小时数，编辑该数据字段的汇总设置并选择 `Sum`，然后确认返回布局对话框。

- 对应 skills：`1de60575-bb6e-4c3d-9e6a-2fa699f9f197.skill-03`
- 高效操作：只添加一次 `Service Hours`，这样最终表中每个项目与季度的交叉位置只会有一个清晰的服务时长汇总值。
- 完成标志：`Data Fields` 区域包含 `Service Hours` 的合计度量，表示 Pivot Table 将聚合小时数而非列出原始记录。

#### 第 5 步：在独立输出位置生成 Pivot Table

1. 在布局对话框的输出位置设置中，选择创建到新工作表的选项；也可以选择任何明确空白、不会覆盖源表的工作表区域。
2. 确认布局：`Program` 位于 `Row Fields`，`Quarter` 位于 `Column Fields`，`Service Hours` 位于 `Data Fields`。然后确认对话框以生成 Pivot Table。
3. 如果生成位置不符合预期或覆盖了已有内容，撤销该次创建，重新打开 `Data` > `Pivot Table` > `Insert or Edit...`，并选择新的空白输出工作表或区域。

- 对应 skills：无；这是准备或检查步骤。
- 高效操作：把结果输出到新工作表可避免覆盖 `Activity Log` 的源数据，也便于一眼区分原始记录和汇总报告。
- 完成标志：Calc 切换到新建的输出工作表或指定空白区域，且可见已经生成的 Pivot Table。

#### 第 6 步：核对交叉汇总的字段方向与数值

1. 查看完成的 Pivot Table：左侧应是各个 `Program` 标签，顶部应是不同的 `Quarter` 标题，表内应是对应的服务时长汇总值。
2. 若 `Quarter` 没有横向显示为列标题，右击 Pivot Table 内任一单元格并选择编辑 Pivot Table 的命令，随后将 `Quarter` 放回 `Column Fields` 并确认更新。
3. 若表内显示单个活动记录或记录数而非小时数合计，编辑 Pivot Table 布局，确认 `Service Hours` 位于 `Data Fields`，并将其汇总方式改为 `Sum` 后更新。

- 对应 skills：无；这是准备或检查步骤。
- 高效操作：优先核对结构和汇总含义，而不是逐个手工重算全部结果；这能更快发现字段放错区域或度量使用计数的问题。
- 完成标志：最终可见的报告按 `Program` 分行、按 `Quarter` 分列，交叉单元格显示聚合后的 `Service Hours` 数值。

#### 最终结果检查

- 应能看到一个原生 Pivot Table，而不是逐条复制的活动记录。
- Pivot Table 的行标签为 `Program`；每个不同的园艺项目各占一行，并可见总计行（其是否显示取决于当前 Pivot Table 默认设置）。
- 顶部横向标题为不同的 `Quarter` 值；每个项目在各季度下显示汇总后的数值。
- 显示的数据度量是 `Service Hours` 的合计：数值应为汇总服务时长，而非记录数或单条活动记录。
- 源工作表 `Activity Log` 仍保留 A1:E37 的原始表格，且新输出工作表或空白输出区域没有遮挡源数据。

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
