# Reference task review packets

Open one task directory at a time, read `TASK.md`, and fill only its `review.json` file.

| Task | Workbook | Local review |
| --- | --- | --- |
| [reference-task-calc-full-r01-001](reference-task-calc-full-r01-001/TASK.md) | Regional Community Grant Requests | pending |
| [reference-task-calc-full-r01-002](reference-task-calc-full-r01-002/TASK.md) | Regional Funding Board View | pending |
| [reference-task-calc-full-r01-003](reference-task-calc-full-r01-003/TASK.md) | Service Estimate Review | pending |
| [reference-task-calc-full-r01-004](reference-task-calc-full-r01-004/TASK.md) | Garden Supply Round Reconciliation | pending |
| [reference-task-calc-full-r01-005](reference-task-calc-full-r01-005/TASK.md) | Replenishment Review | pending |
| [reference-task-calc-full-r01-006](reference-task-calc-full-r01-006/TASK.md) | Route Operations Review | pending |
| [reference-task-calc-full-r01-007](reference-task-calc-full-r01-007/TASK.md) | Field Service Payment Review | pending |
| [reference-task-calc-full-r01-008](reference-task-calc-full-r01-008/TASK.md) | Garden Supply Delivery Register | pending |
| [reference-task-calc-full-r01-009](reference-task-calc-full-r01-009/TASK.md) | Workshop Allocation Review | pending |
| [reference-task-calc-full-r01-010](reference-task-calc-full-r01-010/TASK.md) | Garden Volunteer Activity | pending |
| [reference-task-calc-full-r01-011](reference-task-calc-full-r01-011/TASK.md) | Community Workshop Event Finance | pending |
| [reference-task-calc-full-r01-012](reference-task-calc-full-r01-012/TASK.md) | Coastal Lab Dispatch Completion | pending |
| [reference-task-calc-full-r01-013](reference-task-calc-full-r01-013/TASK.md) | Garden Supply Delivery Review | pending |
| [reference-task-calc-full-r01-014](reference-task-calc-full-r01-014/TASK.md) | Repair Fair Handoff | pending |
| [reference-task-calc-full-r01-015](reference-task-calc-full-r01-015/TASK.md) | Fleet Fuel Planning | pending |
| [reference-task-calc-full-r01-016](reference-task-calc-full-r01-016/TASK.md) | Workshop Supply Reimbursements | pending |
| [reference-task-calc-full-r01-017](reference-task-calc-full-r01-017/TASK.md) | Solar Microgrid Review | pending |
| [reference-task-calc-full-r01-018](reference-task-calc-full-r01-018/TASK.md) | Workshop Attendance Register | pending |
| [reference-task-calc-full-r01-019](reference-task-calc-full-r01-019/TASK.md) | Garden Volunteer Activity Tracker | pending |
| [reference-task-calc-full-r01-020](reference-task-calc-full-r01-020/TASK.md) | Community Garden Supply Budget | pending |

After reviewing tasks, run:

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
