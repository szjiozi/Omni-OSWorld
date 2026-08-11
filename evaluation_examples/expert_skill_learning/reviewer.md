# Reference Package Reviewer Guide

本文档指导人工 reviewer 审核 OSWorld expert-skill benchmark 的 reference packages。
Reviewer 的目标不是判断任务最终是否已经被执行，而是判断这个 package 是否适合交给
human expert 录制 reference video。

## 1. Reviewer 从哪里开始

先打开：

```text
pilot/review_packets/index.md
```

Index 中每个 task 都链接到独立目录：

```text
pilot/review_packets/<reference-task-id>/
├── TASK.md
├── context.json
├── review.json
├── task_config.json
├── manifest.json
└── artifact/
    ├── initial_artifact.xlsx
    ├── artifact_blueprint.json
    ├── artifact_qa.json
    └── previews/
```

正常审核只需要阅读 `TASK.md`、查看 `artifact/`，然后填写同目录下的 `review.json`。
`TASK.md` 已经汇总 task、sampled skills、procedure、efficiency tip、source instruction、直接
引用的 source actions、artifact spec、preview、operator guide 和 similarity audit。
`context.json` 还保留相关 source tasks 的完整 ordered single-action sequence，供需要深入检查
source leakage 时使用。

原来的 `reference_packages.json`、`skill_pool.json`、`source_tasks.json`、artifact manifests
和 task configs 仍然保留为 pipeline 的 canonical 中间交付物。Reviewer 不需要在它们之间
手动跳转，也不应直接编辑这些文件。

如果 packets 尚未生成或上游内容有更新，从仓库根目录运行：

```bash
python scripts/python/manage_reference_review_packets.py export
```

## 2. 每个 package 的推荐审核顺序

对每个 `reference_task_id` 按以下顺序审核。不要只阅读 `task_instruction` 就做决定。

### 2.1 检查 task instruction

确认：

- 任务是自然的结果导向 instruction，而不是 skill 名称列表；
- 任务可以在一个 LibreOffice Calc workbook 内完成；
- 任务不像为了拼接 skills 而人为制造的操作清单；
- instruction 没有直接给出完整 click-by-click golden solution；
- domain、对象名、数值和布局与 source tasks 有实质差异；
- 没有复用 source task 中明显独特的 literals 或完整 ordered solution。

### 2.2 检查 required skills

在 `required_skill_ids` 中找到所有 sampled skills，再到 `skill_pool.json` 查看每个 skill 的：

- `name`；
- `procedure`；
- `efficiency_tip`；
- `source.task_id` 和 `source.action_ids`。

逐个确认：

- 每个 sampled skill 都是完成 task instruction 所必需的；
- 每个 skill 都能在视频中产生可观察的操作过程或结果；
- skill 不是可做可不做的装饰步骤；
- task 没有把两个本应独立的 sampled skills 合并成一个无法分别观察的结果；
- human expert 可以使用对应的高效操作方式完成，而不需要故意绕远路。

Pilot coverage 只计算 `required_skill_ids`。Incidental operations 即使具有实质性，也不会
自动计入 coverage。

### 2.3 检查 incidental operations

查看 `expected_incidental_operations`。每项应属于：

- `scaffolding`：选择区域、确认对话框、输入普通标签等辅助步骤；
- `task_specific`：服务于当前内容、但不是 benchmark 主要 skill 的步骤；
- `substantive_prerequisite`：为了演示 sampled skill 必须完成的应用操作。

确认：

- 所有明显的额外操作都已经声明；
- incidental operations 数量有限；
- 它们不会占据视频的大部分时间；
- 它们没有偷偷组成另一个完整的 substantive task；
- 如果移除某个 prerequisite 后仍能自然完成任务，就不应该强制加入它。

少量 skill 重复是允许的。重点不是让视频只包含 sampled skills，而是让 sampled skills 保持
主要、必要且清晰可学习。

### 2.4 检查 source similarity 和 leakage

`similarity_reference` 提供：

- `lexical.max_sequence_similarity`：字面字符串接近程度；
- `semantic.max_cosine_similarity`：candidate instruction 与 source instructions 的 embedding
  cosine；
- `most_similar_source_task_id`：当前最接近的 source task；
- `source_contribution`：sampled skills 分别来自哪些 source tasks。

这些数值没有自动通过阈值。Reviewer 需要结合内容判断：

- 是否只更换了实体名称，操作结构仍与某个 source task 完全一致；
- 是否复现了同一个 ordered solution；
- 是否复用了 distinctive values、sheet names 或 layout；
- 是否因为多个 sampled skills 来自同一 source，而重建了原任务的大部分内容。

语义相似不等于泄漏；两个 Calc 任务都包含 Pivot Table 时 cosine 较高是正常的。真正需要
拒绝或修改的是 source solution 的实质性复现。

### 2.5 检查 artifact spec

查看 `artifact_spec` 的：

- `domain` 和 `workbook_title`；
- sheets、columns、data types 和 row counts；
- `initial_state`；
- `must_not_be_completed`；
- `generation_notes`。

确认：

- artifact 足以让 expert 完成任务；
- 初始状态不会缺少关键输入数据；
- 应由 expert 演示的公式、格式、Pivot Table、conditional formatting 或结果仍然未完成；
- artifact 没有提前泄露完整操作结果；
- 数据是 synthetic、privacy-safe 的；
- 行数足以清晰演示 skill，但没有无意义地扩大标注工作量；
- spec 中不存在互相冲突的要求。

然后打开实际 `initial_artifact.xlsx` 或查看 preview，确认 materialized workbook 与 spec 一致。

如果 `artifact_spec` 本身设计错误，应对 package 选择 `revision_requested` 或 `rejected`。
如果 spec 正确，但实际 XLSX 因 builder bug、格式导出错误或数据计数错误而不符合 spec，不要
把它误判成 skill combination 问题；停止该 package 的 annotation，并把问题报告给
developer 修复 artifact generation。

### 2.6 检查 operator guide

查看 `operator_guide.recommended_demonstration`，确认：

- 每个 required skill 恰好对应一项；
- `operation_intent` 描述操作目的，不是坐标或逐 click 脚本；
- `visible_success_signal` 可以在视频或 final workbook 中观察；
- `efficiency_tip` 与 skill pool 中的高效方法一致；
- `recording_start_state` 与 artifact 初始状态一致；
- `recording_end_state` 覆盖所有 sampled skills；
- `allowed_variation` 允许 expert 调整顺序或使用等价高效方法。

Guide 可以帮助 expert，但不能退化成 target 的唯一完整 golden trajectory。

## 3. 如何选择 decision

| Decision | 何时使用 | 后续行为 |
| --- | --- | --- |
| `approved` | Task 自然、skills 必要、artifact 可行、leakage 可接受，可以直接进入 annotation | Skills 计入 approved coverage，不重生成 |
| `revision_requested` | Skill combination 有价值，问题可以在保持相同 sampled IDs 的情况下修复 | 使用相同 skill set 和 reviewer feedback 重新生成 |
| `rejected` | Combination 本身不自然、不可行、严重泄漏，或修复需要改变 sampled skills | 当前 exact combination 被屏蔽，uncovered skills 重新采样 |

### 应选择 approved 的最低条件

只有同时满足以下条件才批准：

- 所有 sampled skills 必要且可观察；
- task 是自然且可执行的；
- incidental operations 有限；
- artifact spec 与实际 artifact 足以开始标注；
- 没有明显 source-solution leakage；
- operator guide 有帮助但不过度规定唯一轨迹。

### 应选择 revision_requested 的典型情况

- Task 目标合理，但 instruction 表达不清；
- artifact 太复杂，可以在同一 skill set 下简化；
- incidental operations 过多，但可以减少；
- domain 或 literals 与 source 太接近，但可以更换；
- operator guide 太详细或 success signal 不清楚；
- sampled skills 组合合理，但当前生成版本没有让其中一个 skill 成为必要操作。

Revision instructions 必须给出可执行的修改要求，不能只写 `Improve the task`。

### 应选择 rejected 的典型情况

- Sampled skills 无法组成自然任务；
- 为连接 sampled skills 必须加入大量无关 substantive operations；
- Task 实质上复现某个 source task 的完整解法；
- Artifact 在一个 workbook 内不可合理实现；
- 修复问题必须移除或更换 sampled skill；
- Task 不适合作为简洁、可学习的 reference video。

## 4. Review JSON 每个字段怎么填

每个 task 的 Review 文件位于：

```text
evaluation_examples/expert_skill_learning/pilot/review_packets/
  <reference-task-id>/review.json
```

### `reference_task_id`

- 已由生成器填写；
- 不要修改；
- 必须与 `reference_packages.json` 中的 ID 完全一致。

### `decision`

- Reviewer 必填；
- 未审核时保持空字符串 `""`；
- 审核后只能填写 `approved`、`revision_requested` 或 `rejected`；
- 不要填写 `keep`、`accept`、`pending` 或其他近义词。

### `reason_codes`

- JSON string 数组；
- Approved 时通常为 `[]`；
- Revision 或 rejection 时填写一个或多个标准 code；
- 不要把自然语言长解释写在这里，长解释写入 `notes`。

推荐 codes：

- `too_similar_to_source`：与 source task 实质性相似；
- `unnatural_combination`：sampled skills 组合不自然；
- `missing_skill_coverage`：任务没有真正覆盖某个 required skill；
- `skill_not_necessary`：某个 required skill 对完成任务不是必要的；
- `too_many_incidental_operations`：额外操作过多；
- `artifact_infeasible`：artifact 无法支持任务；
- `artifact_too_complex`：artifact 或任务复杂度不必要地高；
- `operator_guide_too_prescriptive`：guide 过于接近完整 golden steps；
- `unclear_success_signal`：无法明确判断 skill 是否展示成功；
- `other`：其他问题，必须在 notes 解释。

### `revision_instructions`

- 只有 `revision_requested` 可以填写；
- 必须是非空 string 数组；
- 会原样发送给 construction LLM；
- 必须使用英文；
- 每项只描述一个具体修改；
- 不要要求改变 `required_skill_ids`，需要改变组合时应选择 rejected。

Approved 和 rejected 时必须保持 `[]`。

### `reviewer`

- 完成 review 后必填；
- 使用稳定的 reviewer ID，例如 `reviewer-jz`；
- 不建议填写私人邮箱或其他不必要的个人信息；
- Pending 时保持空字符串。

### `notes`

- 对决定的简短解释；
- Approved 时建议说明为什么 task 可以保留；
- Rejected 时，如果 `reason_codes` 已经解释充分，可以简短填写；
- `other` reason code 必须在这里解释；
- 建议使用英文，方便后续审计；
- Pending 时保持空字符串。

重要：当 `decision` 为空时，`reason_codes`、`revision_instructions`、`reviewer` 和 `notes`
也必须保持空。不要一边写 notes 一边把 decision 留空。

## 5. 三种 decision 的填写示例

以下 ID 仅用于展示格式，不代表对当前 packages 的实际建议。

### Approved 示例

```json
{
  "reference_task_id": "reference-task-r01-001",
  "decision": "approved",
  "reason_codes": [],
  "revision_instructions": [],
  "reviewer": "reviewer-jz",
  "notes": "The task is natural, feasible, and sufficiently different from the source tasks. All sampled skills are necessary and visibly demonstrable."
}
```

### Revision 示例

```json
{
  "reference_task_id": "reference-task-r01-002",
  "decision": "revision_requested",
  "reason_codes": [
    "too_many_incidental_operations",
    "artifact_too_complex"
  ],
  "revision_instructions": [
    "Keep the same sampled skills but reduce the task to one source-data sheet.",
    "Remove prerequisite operations that are not necessary to demonstrate the sampled skills.",
    "Use a simpler synthetic domain that remains distinct from every source task."
  ],
  "reviewer": "reviewer-jz",
  "notes": "The skill combination is useful, but the current package requires too much unrelated setup."
}
```

### Rejected 示例

```json
{
  "reference_task_id": "reference-task-r01-003",
  "decision": "rejected",
  "reason_codes": [
    "unnatural_combination"
  ],
  "revision_instructions": [],
  "reviewer": "reviewer-jz",
  "notes": "The sampled skills cannot be combined into a natural single-workbook task without adding several unrelated operations."
}
```

## 6. 保存前检查 JSON 格式

Review 文件必须是合法 JSON：

- 不允许 `// comment`；
- 最后一项后面不能有 trailing comma；
- 字符串必须使用双引号；
- `reason_codes` 和 `revision_instructions` 必须是数组；
- 每个 task ID 最多出现一次；
- `review.json` 本身就是一个 task 的单独 object，不要额外添加 `schema_version` 或
  `reviews` wrapper；
- 除 `review.json` 外，不要修改 packet 内的其他文件；collector 会校验它们的 SHA256。

## 7. 保存后收集 review 并重算 coverage

从仓库根目录运行：

```bash
python scripts/python/manage_reference_review_packets.py collect
```

该命令先验证每个独立表单和 packet 完整性，再合并到 pipeline 使用的中央
`pilot/reference_package_reviews.json`，并自动重算 `pilot/coverage_state.json`。需要只回收
一个 task 时使用：

```bash
python scripts/python/manage_reference_review_packets.py collect \
  --task-id reference-task-r01-001
```

结果解释：

- `Approved skills: 12/12`：Pilot coverage 完成，不需要 round 2；
- 输出仍有 pending IDs：还有 package 没审核；
- 没有 pending、但 approved skills 未覆盖全部 skill：所有旧 package 已审核，可以启动下一轮；
- schema/field 错误：先修正 review JSON，不要启动重生成。

## 8. 什么时候启动下一轮生成

只有满足以下两个条件才启动 round 2：

1. 所有 round-1 packages 都已经填写 decision；
2. `coverage_state.json` 仍有 unresolved skills。

不要仅因为 coverage 尚未完成就直接重跑；先检查是仍有 pending package，还是所有 review
已经完成但 approved coverage 仍不完整。

Round 2 必须使用新的 `generation_round`、seed 和输出目录，不能覆盖 round 1。Revision 会
保持原 sampled skills 并使用 `revision_instructions`；rejected exact combination 不会再次采样。
当前 Pilot 是 coverage-driven：只有至少包含一个 unresolved skill 的 revision 才会重新生成。
如果该 package 的全部 skills 已被其他 approved packages 覆盖，它不会阻塞 coverage，也不会
自动生成替代版本。

## 9. Reviewer 不负责的内容

当前 package reviewer 不需要：

- 实际录制 reference video；
- 评价 human expert 的操作质量；
- 运行 downstream agent；
- 修改 skill pool；
- 给 reference task 编写自动 evaluator；
- 因为个人偏好的操作顺序而拒绝等价的高效方法。

视频录制后的 cross-validation 是另一个阶段。届时 reviewer 将检查视频是否覆盖 required
skills、操作是否正确、是否包含敏感信息，以及录制输出是否完整。

Package 被标记为 `approved` 后，human expert 按 [`annotator.md`](annotator.md) 启动 AWS
环境和录制。普通启动器会拒绝 pending package；`--allow-pending` 只用于工程 smoke。
