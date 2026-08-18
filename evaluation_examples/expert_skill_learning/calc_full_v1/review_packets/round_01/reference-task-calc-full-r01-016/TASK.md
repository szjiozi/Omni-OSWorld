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

本任务在 `Reimbursements` 工作表完成三项工作：利用 `G2` 中已有的 Net Reimbursement 公式快速填充所有记录，隐藏三条内部测试记录但保留其数据，并在 `G27` 计算全部报销记录的总额。

#### 启动后的初始状态检查

- 确认当前打开的工作表是 `Reimbursements`；若不是，点击底部的 `Reimbursements` 工作表标签。
- 确认第 1 行是字段标题，记录位于第 2 至第 25 行；`F27` 显示 `Total Reimbursement`，而 `G27` 仍为空白。
- 选中 `G2`，查看输入行是否为 `=D2+E2-F2`；同时确认 `G3:G25` 尚未填入结果，且行 `6`、`13`、`20` 当前可见。

#### 第 1 步：向下填充 Net Reimbursement 公式

1. 在 `Reimbursements` 工作表中单击 `G2`。该单元格是 Net Reimbursement 列已有公式的种子单元格。
2. 将指针移到 `G2` 选中框右下角的小方块（填充柄），然后双击该小方块。
3. 预期 Calc 会把公式向下填充到连续记录区域的末行 `G25`，并按行调整引用。若 `G3:G25` 已显示计算出的货币值，则无需调整。
4. 如果双击后只填充到较早的行或没有填充到 `G25`，说明 Calc 未正确识别连续区域：重新单击 `G2`，再次双击填充柄；若仍不正确，可选中 `G2`，拖动右下角的填充柄向下至 `G25` 后释放。

- 对应 skills：`7e429b8d-a3f0-4ed0-9b58-08957d00b127.skill-02`
- 高效操作：双击填充柄会根据相邻连续数据区域自动确定终点，比拖动到第 25 行更快；本表相邻输入列从第 2 行连续到第 25 行。
- 完成标志：`G3:G25` 都显示计算结果，且选择例如 `G3` 时可在输入行看到随行变化的公式 `=D3+E3-F3`；`G2` 保留原始公式。

#### 第 2 步：隐藏内部测试请求行

1. 单击左侧行号 `6` 的行标题以选中整行。
2. 按住 `Ctrl` 不放，依次单击行号 `13` 和 `20` 的行标题，然后松开 `Ctrl`。应同时选中这三个不相邻的行标题。
3. 在任一已选中的行标题上右键单击，选择 `Hide Rows`。
4. 预期行号会直接从 `5` 跳到 `7`、从 `12` 跳到 `14`、从 `19` 跳到 `21`，无需额外调整。
5. 如果只有一行被隐藏，或行号未出现这三处跳号，说明多选没有成功：使用 `Ctrl` 重新选择当前仍可见的目标行标题，然后再次右键选择 `Hide Rows`。不要删除行或使用筛选。

- 对应 skills：`6054afcb-5bab-4702-90a0-b259b5d3217c.skill-01`
- 高效操作：一次按住 Ctrl 选中所有不相邻的行标题，再执行一次隐藏命令，可避免逐行隐藏并减少误操作。
- 完成标志：左侧行号序列跳过 `6`、`13` 和 `20`；可见记录仍保持原有顺序，隐藏操作没有移除任何数据。

#### 第 3 步：计算整体报销总额

1. 单击 `G27`，即 `F27` 中 `Total Reimbursement` 标签右侧的空白单元格。
2. 输入公式 `=SUM(G2:G25)`，然后按 `Enter` 确认。
3. 预期 `G27` 显示一个货币总额；即使行 `6`、`13`、`20` 已隐藏，`SUM` 仍会包含这些行的 Net Reimbursement 值，因此无需调整。
4. 如果 `G27` 显示的不是总额，单击 `G27` 并查看输入行：若范围不是 `G2:G25`，重新输入 `=SUM(G2:G25)` 后按 `Enter`；若显示错误值，先确认 `G2:G25` 均已有计算结果，再重新确认该公式。

- 对应 skills：`0a2e43bf-b26c-4631-a966-af9dfa12c9e5.skill-01`
- 高效操作：直接输入一个 `SUM` 公式即可汇总整段 Net Reimbursement 数据；第 26 行是空白间隔，因此总计单元格不会被包含在求和范围中。
- 完成标志：`G27` 显示货币格式的总额；选中该单元格时，输入行显示 `=SUM(G2:G25)`。

#### 第 4 步：完成最终核对

1. 依次抽查一个已填充的 Net Reimbursement 单元格（如 `G3`）和 `G27`，确认输入行分别显示该行的相对公式及 `=SUM(G2:G25)`。
2. 查看左侧行号，确认仅要求隐藏的 `6`、`13`、`20` 不可见，且第 `26` 行仍作为总计上方的空白间隔。

- 对应 skills：无；这是准备或检查步骤。
- 高效操作：通过输入行核对关键公式和左侧行号跳号，比逐项比对所有金额更快。
- 完成标志：所有记录计算完成，指定三行被隐藏但未删除，`G27` 的总计公式覆盖 `G2:G25`。

#### 最终结果检查

- 在 `Reimbursements` 工作表中，`G2:G25` 的每条报销记录都显示货币计算结果；选中例如 `G3` 时，输入行应显示相对行引用的公式（如 `=D3+E3-F3`），而不是空白或固定引用。
- 左侧行号可见跳过 `6`、`13` 和 `20`，表明这些行已隐藏；其余记录仍按原有顺序显示，且并未删除。
- `F27` 仍显示 `Total Reimbursement`，其右侧的 `G27` 显示货币总额。选中 `G27` 后，输入行应显示 `=SUM(G2:G25)`，范围覆盖全部记录行，包括当前隐藏的行。

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
