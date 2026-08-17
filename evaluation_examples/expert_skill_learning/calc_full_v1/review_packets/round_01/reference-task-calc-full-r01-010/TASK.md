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

在“Activity Log”的连续源数据上创建数据透视表，并将结果放到新的汇总工作表。透视表以 Program 为行、Quarter 为列，并汇总 Service Hours，从而按项目和季度查看志愿服务总小时数。

#### 启动后的初始状态检查

- 确认当前打开的是“Activity Log”工作表，且第1行包含 Program、Quarter、Garden Site、Activity Type、Service Hours 标题。
- 确认数据表是连续区域 A1:E37，中间没有空白行或空白列。
- 确认当前尚未存在数据透视表，也没有预先创建的汇总输出工作表。

#### 第 1 步：检查并选择志愿活动源数据

1. 在“Activity Log”中单击源数据区域内任意单元格，例如标题行或任一记录行。
2. 检查第1行字段名是否包括 Program、Quarter、Garden Site、Activity Type、Service Hours，并确认记录延续到第37行。
3. 如需明确选择数据源，可拖选 A1:E37；不要只选中某一列。

- 对应 skills：无；这是准备或检查步骤。
- 高效操作：先确认源表没有中断；连续区域可让 Calc 自动正确识别整个数据范围，避免漏掉记录或字段。
- 完成标志：“Activity Log”中的 A1:E37 是一块完整的五列数据区域，包含36条活动记录和一行标题。

#### 第 2 步：打开数据透视表布局

1. 保持光标位于源数据区域内，打开菜单“数据”中的“数据透视表”命令，并选择用于插入或创建数据透视表的选项。
2. 在数据源确认界面中，确认使用当前选定区域或当前数据选区作为源；范围应覆盖“Activity Log”中的 A1:E37。
3. 继续进入数据透视表布局对话框。

- 对应 skills：无；这是准备或检查步骤。
- 高效操作：从已选中的源区域启动数据透视表，可减少在设置过程中手动输入范围的需要。
- 完成标志：出现数据透视表布局对话框，Available Fields（可用字段）中可见 Program、Quarter、Garden Site、Activity Type 和 Service Hours。

#### 第 3 步：设置 Program 行和 Quarter 列

1. 在 Available Fields 中找到 Program，将它拖到 Row fields（行字段）区域。
2. 在 Available Fields 中找到 Quarter，将它直接拖到 Column fields（列字段）区域。
3. 检查布局区域：Program 应显示在行字段框中，Quarter 应显示在列字段框中。

- 对应 skills：`1de60575-bb6e-4c3d-9e6a-2fa699f9f197.skill-02`
- 高效操作：直接把字段从 Available Fields 拖入目标区域，避免先添加后再移动字段。先完成分类布局，随后再添加数值字段，结构更容易核对。
- 完成标志：布局对话框的 Row fields 中有 Program，Column fields 中有 Quarter，表示输出将按项目分行、按季度分列。

#### 第 4 步：将 Service Hours 作为汇总值

1. 在 Available Fields 中找到数值字段 Service Hours。
2. 将 Service Hours 拖到 Data fields（数据字段）区域。
3. 确认数据字段显示 Service Hours，汇总函数应为求和；如果 Calc 显示为“Sum - Service Hours”或等效的求和名称，即表示设置正确。
4. 确认布局对话框以应用字段配置。

- 对应 skills：`1de60575-bb6e-4c3d-9e6a-2fa699f9f197.skill-03`
- 高效操作：仅将需要汇总的数值字段放入 Data fields；在行列结构已经确定后添加它，可以立即判断汇总指标是否正确。
- 完成标志：Data fields 区域中显示 Service Hours 的求和汇总，布局已同时包含 Program、Quarter 和该数值指标。

#### 第 5 步：将汇总结果放到新工作表

1. 在输出位置或结果位置设置界面中，选择创建到新的工作表（或选择一个确认为空的工作表位置）。
2. 确认创建数据透视表；如创建了默认名称的新工作表，可按需要将其重命名为清晰的名称，例如“Program Summary”。
3. 不要在“Activity Log”的原始表 A1:E37 内放置输出结果。

- 对应 skills：无；这是准备或检查步骤。
- 高效操作：将透视表放在新工作表可避免覆盖源记录，也便于单独查看和复核汇总结果。
- 完成标志：Calc 切换到新的输出工作表或显示指定的空白输出区域，数据透视表已生成且未覆盖“Activity Log”源数据。

#### 第 6 步：核对并保存数据透视表

1. 查看透视表左侧的行标签，确认显示多个 Program 项目。
2. 查看透视表顶部，确认 Quarter 的不同季度值作为独立列标题显示。
3. 查看 Program 与 Quarter 的交叉单元格，确认其中是 Service Hours 的汇总数值而非原始明细；如有总计行或总计列，也应与汇总结构一致。
4. 保存工作簿以保留新的数据透视表和汇总工作表。

- 对应 skills：无；这是准备或检查步骤。
- 高效操作：用行、列和数值区域同时检查结果，比只检查透视表是否出现更快发现字段放错区域的问题。
- 完成标志：可见的透视表按 Program 分行、按 Quarter 分列，并在交叉位置显示汇总的 Service Hours 数值。

#### 最终结果检查

- 工作簿中有一个新的汇总工作表或明确为空的输出区域，且其中显示原生数据透视表。
- 数据透视表的行标签为 Program；顶部列标题显示 Quarter 的不同季度值。
- 数据区域显示的是 Service Hours 的汇总数值（通常为求和），而不是36条原始活动记录；每个 Program 行在各季度列下都有对应总工时。
- 确认源工作表“Activity Log”仍保留完整的 A1:E37 原始数据表。

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
