# Workshop Supply Reimbursements

- Reference task: `reference-task-calc-full-r01-016`
- Application: `libreoffice_calc`
- Review decision: `pending`

## Task instruction

Complete the Net Reimbursement calculation for every workshop supply request, keep the internal test requests on rows 6, 13, and 20 out of view without removing them, and show the overall reimbursement total beside the Total Reimbursement label.

## Required skills

### 1. Auto-fill a formula down a contiguous data region

Skill ID: `7e429b8d-a3f0-4ed0-9b58-08957d00b127.skill-02`

Procedure:

1. Select the cell that already contains the formula to propagate.
2. Double-click the small fill handle at the cell's bottom-right corner.
3. Calc fills the formula downward through the contiguous neighboring data rows, adjusting relative references. For example, a formula beginning with `E2` in the selected row becomes `E3`, `E4`, and so on in subsequent rows, while an absolute range such as `$A$2:$B$7` remains fixed.

Efficiency tip: Double-clicking the fill handle is faster than dragging it for long adjacent datasets, but verify that the neighboring column has continuous rows because Calc uses that region to determine the fill length.

Source task: `7e429b8d-a3f0-4ed0-9b58-08957d00b127`

Source instruction: I have a lookup table for the officers of each branch. Please, here is another table in which I need to fill with the officer names according the headoffice (i.e., the branch name). Help me to complete this.

Directly referenced source actions:

- Action 3: <code>`CLICK` F2</code>
- Action 4: <code>`DOUBLE_CLICK` the bottom right corner of cell F2</code>

### 2. Hide multiple non-adjacent rows

Skill ID: `6054afcb-5bab-4702-90a0-b259b5d3217c.skill-01`

Procedure:

1. Click the header of the first row to hide.
2. Hold Ctrl and click each additional row header that should be hidden; for example, select rows 3, 6, 8, and 9 while retaining the earlier selections.
3. Release Ctrl after all target row headers are selected.
4. Right-click any selected row header and choose Hide rows.
5. The selected rows are hidden without deleting their contents; they can later be restored with the corresponding unhide command.

Efficiency tip: Hold Ctrl while selecting all non-adjacent row headers, then use Hide rows once; this is faster and less error-prone than hiding each row individually.

Source task: `6054afcb-5bab-4702-90a0-b259b5d3217c`

Source instruction: Some data are missed by now and are filled by 'N/A' temporarily. Please hide them in the table for now. Do not delete them and filter is no needed.

Directly referenced source actions:

- Action 0: <code>`CLICK` row 3</code>
- Action 1: <code>`KEY_DOWN` Ctrl</code>
- Action 2: <code>`CLICK` row 6</code>
- Action 3: <code>`CLICK` row 8</code>
- Action 4: <code>`CLICK` row 9</code>
- Action 5: <code>`CLICK` row 12</code>
- Action 6: <code>`CLICK` row 14</code>
- Action 7: <code>`CLICK` row 18</code>
- Action 8: <code>`CLICK` row 19</code>
- Action 9: <code>`CLICK` row 20</code>
- Action 10: <code>`CLICK` row 24</code>
- Action 11: <code>`CLICK` row 27</code>
- Action 12: <code>`CLICK` row 32</code>
- Action 13: <code>`CLICK` row 33</code>
- Action 14: <code>`KEY_UP` Ctrl</code>
- Action 15: <code>`RIGHT_CLICK`</code>
- Action 16: <code>`CLICK` Hide rows</code>

### 3. Create a range-total formula in a spreadsheet cell

Skill ID: `0a2e43bf-b26c-4631-a966-af9dfa12c9e5.skill-01`

Procedure:

1. Select the result cell next to the label, type a SUM formula for the cells to total, and confirm it. For example, enter `=SUM(B2:B11)` in B12 to total that column's values from rows 2 through 11.
2. Use relative references when the formula will be copied across columns: `B2:B11` shifts to `C2:C11`, `D2:D11`, and so on when filled right.

Efficiency tip: Enter the formula once in the first result cell; use autofill afterward rather than manually rewriting the formula for each adjacent column.

Source task: `0a2e43bf-b26c-4631-a966-af9dfa12c9e5`

Source instruction: Work out the monthly total sales in a new row called "Total" and then create a line chart to show the results (x-axis be Months).

Directly referenced source actions:

- Action 2: <code>`PRESS` tab</code>
- Action 3: <code>`TYPING` &#x27;=SUM(B2:B11)&#x27;</code>
- Action 4: <code>`PRESS` enter</code>

## Initial state preview

### Reimbursements

![Reimbursements.png](artifact/previews/Reimbursements.png)

## Operator guide

### Existing operation-intent guide

#### Demonstration 1

- Skill: `7e429b8d-a3f0-4ed0-9b58-08957d00b127.skill-02`
- Intent: Propagate the Net Reimbursement formula from the seeded first record through all remaining contiguous reimbursement records.
- Efficiency: Use the seeded formula in G2 and the fill handle’s double-click behavior; the neighboring data columns are continuous through row 25.
- Visible success: G3:G25 display calculated currency results with row-relative formulas, while G2 remains the original seed.

#### Demonstration 2

- Skill: `6054afcb-5bab-4702-90a0-b259b5d3217c.skill-01`
- Intent: Hide the three internal test reimbursement records on rows 6, 13, and 20 without deleting their data.
- Efficiency: Use a single multi-selection of row headers and issue the hide command once rather than hiding records individually.
- Visible success: The row-number sequence visibly skips 6, 13, and 20, and the surrounding records remain in place.

#### Demonstration 3

- Skill: `0a2e43bf-b26c-4631-a966-af9dfa12c9e5.skill-01`
- Intent: Calculate the overall reimbursement amount in G27 next to the Total Reimbursement label.
- Efficiency: Enter one SUM formula referencing the complete Net Reimbursement data range; the blank spacer row prevents accidental inclusion of the total cell.
- Visible success: G27 shows a currency total produced by a range-total formula covering G2:G25.

Recording start: The Reimbursements sheet is visible with populated source records, only G2 containing the seeded formula, and all rows visible.

Recording end: All reimbursement records have calculated net values, rows 6, 13, and 20 are hidden, and G27 contains the range total for G2:G25.

Allowed variation: The expert may calculate and verify the total before or after hiding the specified records, provided all per-record net formulas are filled, the required records are hidden rather than removed, and the total formula covers the complete record range.

### 中文详细参考方案

> 以下是一个可以参考的操作 guide。标注者可以根据实际 LibreOffice 界面采用等价操作。

本指南将在 Reimbursements 工作表中完成每条 workshop supply request 的 Net Reimbursement，隐藏指定的内部测试记录，并在 Total Reimbursement 标签右侧计算全部请求记录的总额。

#### 启动后的初始状态检查

- 确认已打开的工作簿包含名为 Reimbursements 的工作表，并切换到该工作表。
- 确认第 1 行是标题行，记录从第 2 行延续到第 25 行；第 26 行应为空白间隔行，F27 应为 Total Reimbursement，G27 应为空白。
- 确认 G2 已有公式 =D2+E2-F2，而 G3:G25 尚未填入计算结果。
- 确认第 6、13、20 行在开始时均可见；这些行是要隐藏的记录，不应删除或清空。

#### 第 1 步：确认 Net Reimbursement 的公式种子

1. 在 Reimbursements 工作表中单击单元格 G2。
2. 查看输入行或公式栏，确认该单元格的公式为 =D2+E2-F2；如不是该公式，应先停止并重新检查起始工作簿。

- 对应 skills：无；这是准备或检查步骤。
- 高效操作：先利用已有的 G2 公式再自动填充，避免逐行输入相同结构的计算公式。
- 完成标志：G2 被选中，并且公式栏显示 =D2+E2-F2；G3:G25 仍为空。

#### 第 2 步：向下自动填充 Net Reimbursement 公式

1. 保持 G2 处于选中状态。
2. 将指针移到 G2 选框右下角的小方块（填充柄）。
3. 双击填充柄，让 Calc 将公式自动向下填充整个连续记录区。
4. 检查 G3 到 G25 已出现计算结果。

- 对应 skills：`7e429b8d-a3f0-4ed0-9b58-08957d00b127.skill-02`
- 高效操作：双击填充柄比拖到第 25 行更快；由于相邻的记录列在第 2 至 25 行连续有数据，Calc 可据此确定填充终点。
- 完成标志：G3:G25 显示货币计算结果；选中例如 G3 时，公式应按行号自动调整为 =D3+E3-F3，而 G2 保留原公式。

#### 第 3 步：隐藏内部测试请求行

1. 单击左侧的行号 6，选中整行。
2. 按住 Ctrl 键不放，依次单击行号 13 和行号 20，使这三个不相邻行同时处于选中状态。
3. 释放 Ctrl 键。
4. 在任一已选中的行号上右键单击，然后选择 Hide Rows（隐藏行）。

- 对应 skills：`6054afcb-5bab-4702-90a0-b259b5d3217c.skill-01`
- 高效操作：按住 Ctrl 一次选中所有不相邻行，再执行一次隐藏命令，可避免逐行隐藏造成遗漏。
- 完成标志：左侧行号显示 5 后接 7、12 后接 14、19 后接 21；数据没有被删除，只是第 6、13、20 行暂时不可见。

#### 第 4 步：计算总体 reimbursement 总额

1. 单击 Total Reimbursement 标签右侧的单元格 G27。
2. 输入公式 =SUM(G2:G25)。
3. 按 Enter 确认公式。

- 对应 skills：`0a2e43bf-b26c-4631-a966-af9dfa12c9e5.skill-01`
- 高效操作：使用明确的完整数据范围 G2:G25；第 26 行为空白，因此不会把 G27 的总计单元格误包含到汇总范围中。
- 完成标志：G27 显示一个货币总额；选中 G27 时，公式栏显示 =SUM(G2:G25)。

#### 第 5 步：核对最终工作表状态

1. 抽查一个仍可见的 Net Reimbursement 单元格，例如 G10 或 G18，确认它包含本行 D、E、F 列的相对引用公式。
2. 确认 G27 的 SUM 范围是 G2:G25，即使其中部分记录行已隐藏，仍会汇总完整记录范围。
3. 确认 F27 的标签仍为 Total Reimbursement，且第 6、13、20 行没有被删除。

- 对应 skills：无；这是准备或检查步骤。
- 高效操作：通过抽查公式栏和行号跳号即可快速确认计算、隐藏和汇总三项结果，无需逐项修改记录。
- 完成标志：所有记录均已计算、指定三行保持隐藏、G27 已显示完整记录范围的总 reimbursement 金额。

#### 最终结果检查

- 在 Reimbursements 工作表中，G2:G25 的每条请求均显示 Net Reimbursement 计算结果；抽查任一行的公式栏，应符合“材料费 + 运费 - Sponsor Credit”的同一行引用逻辑。
- 左侧行号应出现跳号：5 后直接到 7、12 后直接到 14、19 后直接到 21，表示第 6、13、20 行已隐藏而非删除。
- F27 仍显示标签 Total Reimbursement，G27 显示货币格式的总额；选中 G27 时，公式栏应为 =SUM(G2:G25)。
- 确认记录区域仍包含原有请求：隐藏行前后的可见记录没有被移动、筛选或清除。

## Source-task similarity review

| Measure | Maximum | Most similar source task |
| --- | ---: | --- |
| Lexical sequence similarity | 0.317618 | 0bf05a7d-b28b-44d2-955a-50b41e24012a |
| Semantic cosine similarity | 0.454457 | 035f41ba-6653-43ab-aa63-c86d449d62e5 |

Similarity scores are reviewer aids, not automatic acceptance thresholds. Inspect the contributing source tasks and their complete ordered actions below.

### Source task `0a2e43bf-b26c-4631-a966-af9dfa12c9e5`

Original instruction:

> Work out the monthly total sales in a new row called "Total" and then create a line chart to show the results (x-axis be Months).

Required skills derived from this source task:

- **Create a range-total formula in a spreadsheet cell** — `0a2e43bf-b26c-4631-a966-af9dfa12c9e5.skill-01`

Complete ordered single-action sequence:

| Action | Related required skill | Original single action |
| ---: | --- | --- |
| 0 |  | <code>`CLICK` on cell A12</code> |
| 1 |  | <code>`TYPING` &#x27;Total&#x27;</code> |
| 2 | <strong>★ Create a range-total formula in a spreadsheet cell</strong><br><code>0a2e43bf-b26c-4631-a966-af9dfa12c9e5.skill-01</code> | <strong><code>`PRESS` tab</code></strong> |
| 3 | <strong>★ Create a range-total formula in a spreadsheet cell</strong><br><code>0a2e43bf-b26c-4631-a966-af9dfa12c9e5.skill-01</code> | <strong><code>`TYPING` &#x27;=SUM(B2:B11)&#x27;</code></strong> |
| 4 | <strong>★ Create a range-total formula in a spreadsheet cell</strong><br><code>0a2e43bf-b26c-4631-a966-af9dfa12c9e5.skill-01</code> | <strong><code>`PRESS` enter</code></strong> |
| 5 |  | <code>`CLICK` cell B12</code> |
| 6 |  | <code>`MOVE_TO bottom right corner of the cell B12`</code> |
| 7 |  | <code>`DRAG_TO` bottom right corner of the cell G12</code> |
| 8 |  | <code>`MOVE_TO` middle of cell A1</code> |
| 9 |  | <code>`DRAG_TO` middle of cell G1</code> |
| 10 |  | <code>`KEY_DOWN` ctrl</code> |
| 11 |  | <code>`CLICK` cell A12</code> |
| 12 |  | <code>`KEY_UP` ctrl</code> |
| 13 |  | <code>`KEY_DOWN` shift</code> |
| 14 |  | <code>`CLICK` cell G12</code> |
| 15 |  | <code>`KEY_UP` shift</code> |
| 16 |  | <code>`CLICK` chart icon</code> |
| 17 |  | <code>`CLICK` Line</code> |
| 18 |  | <code>`CLICK` icon representing lines only (3rd from the right)</code> |
| 19 |  | <code>`CLICK` Finish</code> |

### Source task `6054afcb-5bab-4702-90a0-b259b5d3217c`

Original instruction:

> Some data are missed by now and are filled by 'N/A' temporarily. Please hide them in the table for now. Do not delete them and filter is no needed.

Required skills derived from this source task:

- **Hide multiple non-adjacent rows** — `6054afcb-5bab-4702-90a0-b259b5d3217c.skill-01`

Complete ordered single-action sequence:

| Action | Related required skill | Original single action |
| ---: | --- | --- |
| 0 | <strong>★ Hide multiple non-adjacent rows</strong><br><code>6054afcb-5bab-4702-90a0-b259b5d3217c.skill-01</code> | <strong><code>`CLICK` row 3</code></strong> |
| 1 | <strong>★ Hide multiple non-adjacent rows</strong><br><code>6054afcb-5bab-4702-90a0-b259b5d3217c.skill-01</code> | <strong><code>`KEY_DOWN` Ctrl</code></strong> |
| 2 | <strong>★ Hide multiple non-adjacent rows</strong><br><code>6054afcb-5bab-4702-90a0-b259b5d3217c.skill-01</code> | <strong><code>`CLICK` row 6</code></strong> |
| 3 | <strong>★ Hide multiple non-adjacent rows</strong><br><code>6054afcb-5bab-4702-90a0-b259b5d3217c.skill-01</code> | <strong><code>`CLICK` row 8</code></strong> |
| 4 | <strong>★ Hide multiple non-adjacent rows</strong><br><code>6054afcb-5bab-4702-90a0-b259b5d3217c.skill-01</code> | <strong><code>`CLICK` row 9</code></strong> |
| 5 | <strong>★ Hide multiple non-adjacent rows</strong><br><code>6054afcb-5bab-4702-90a0-b259b5d3217c.skill-01</code> | <strong><code>`CLICK` row 12</code></strong> |
| 6 | <strong>★ Hide multiple non-adjacent rows</strong><br><code>6054afcb-5bab-4702-90a0-b259b5d3217c.skill-01</code> | <strong><code>`CLICK` row 14</code></strong> |
| 7 | <strong>★ Hide multiple non-adjacent rows</strong><br><code>6054afcb-5bab-4702-90a0-b259b5d3217c.skill-01</code> | <strong><code>`CLICK` row 18</code></strong> |
| 8 | <strong>★ Hide multiple non-adjacent rows</strong><br><code>6054afcb-5bab-4702-90a0-b259b5d3217c.skill-01</code> | <strong><code>`CLICK` row 19</code></strong> |
| 9 | <strong>★ Hide multiple non-adjacent rows</strong><br><code>6054afcb-5bab-4702-90a0-b259b5d3217c.skill-01</code> | <strong><code>`CLICK` row 20</code></strong> |
| 10 | <strong>★ Hide multiple non-adjacent rows</strong><br><code>6054afcb-5bab-4702-90a0-b259b5d3217c.skill-01</code> | <strong><code>`CLICK` row 24</code></strong> |
| 11 | <strong>★ Hide multiple non-adjacent rows</strong><br><code>6054afcb-5bab-4702-90a0-b259b5d3217c.skill-01</code> | <strong><code>`CLICK` row 27</code></strong> |
| 12 | <strong>★ Hide multiple non-adjacent rows</strong><br><code>6054afcb-5bab-4702-90a0-b259b5d3217c.skill-01</code> | <strong><code>`CLICK` row 32</code></strong> |
| 13 | <strong>★ Hide multiple non-adjacent rows</strong><br><code>6054afcb-5bab-4702-90a0-b259b5d3217c.skill-01</code> | <strong><code>`CLICK` row 33</code></strong> |
| 14 | <strong>★ Hide multiple non-adjacent rows</strong><br><code>6054afcb-5bab-4702-90a0-b259b5d3217c.skill-01</code> | <strong><code>`KEY_UP` Ctrl</code></strong> |
| 15 | <strong>★ Hide multiple non-adjacent rows</strong><br><code>6054afcb-5bab-4702-90a0-b259b5d3217c.skill-01</code> | <strong><code>`RIGHT_CLICK`</code></strong> |
| 16 | <strong>★ Hide multiple non-adjacent rows</strong><br><code>6054afcb-5bab-4702-90a0-b259b5d3217c.skill-01</code> | <strong><code>`CLICK` Hide rows</code></strong> |

### Source task `7e429b8d-a3f0-4ed0-9b58-08957d00b127`

Original instruction:

> I have a lookup table for the officers of each branch. Please, here is another table in which I need to fill with the officer names according the headoffice (i.e., the branch name). Help me to complete this.

Required skills derived from this source task:

- **Auto-fill a formula down a contiguous data region** — `7e429b8d-a3f0-4ed0-9b58-08957d00b127.skill-02`

Complete ordered single-action sequence:

| Action | Related required skill | Original single action |
| ---: | --- | --- |
| 0 |  | <code>`CLICK` F2</code> |
| 1 |  | <code>`TYPING` =VLOOKUP(E2, $A$2:$B$7, 2, FALSE)</code> |
| 2 |  | <code>`PRESS` Enter.</code> |
| 3 | <strong>★ Auto-fill a formula down a contiguous data region</strong><br><code>7e429b8d-a3f0-4ed0-9b58-08957d00b127.skill-02</code> | <strong><code>`CLICK` F2</code></strong> |
| 4 | <strong>★ Auto-fill a formula down a contiguous data region</strong><br><code>7e429b8d-a3f0-4ed0-9b58-08957d00b127.skill-02</code> | <strong><code>`DOUBLE_CLICK` the bottom right corner of cell F2</code></strong> |

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
