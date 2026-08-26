# Reference task review packets

Open one task directory at a time, read `TASK.md`, and fill only its `review.json` file.

| Task | Artifact | Local review |
| --- | --- | --- |
| [reference-task-impress-full-r01-001](reference-task-impress-full-r01-001/TASK.md) | Harbor Pollinator Day | pending |
| [reference-task-impress-full-r01-002](reference-task-impress-full-r01-002/TASK.md) | Neighborhood Night Market | pending |
| [reference-task-impress-full-r01-003](reference-task-impress-full-r01-003/TASK.md) | Riverside Pollinator Walk | pending |
| [reference-task-impress-full-r01-004](reference-task-impress-full-r01-004/TASK.md) | Community Garden Field Brief | pending |
| [reference-task-impress-full-r01-005](reference-task-impress-full-r01-005/TASK.md) | Dawn Marsh Survey | pending |

After reviewing tasks, run:

```bash
python scripts/python/manage_reference_review_packets.py collect \
  --skill-pool evaluation_examples/expert_skill_learning/impress_full_v1/generated/skill_pool.json \
  --packages evaluation_examples/expert_skill_learning/impress_full_v1/generated/round_01/reference_packages.json \
  --source-tasks evaluation_examples/expert_skill_learning/impress_full_v1/source_tasks.json \
  --reviews evaluation_examples/expert_skill_learning/impress_full_v1/generated/round_01/reference_package_reviews.json \
  --artifact-manifest evaluation_examples/expert_skill_learning/impress_full_v1/generated/round_01/artifacts/artifact_manifest.json \
  --task-config-manifest evaluation_examples/expert_skill_learning/impress_full_v1/generated/round_01/task_config_manifest.json \
  --task-detail-root evaluation_examples/expert_skill_learning/impress_full_v1/generated/round_01/task_details \
  --reviewer-guides evaluation_examples/expert_skill_learning/impress_full_v1/generated/round_01/reviewer_guides.json \
  --coverage evaluation_examples/expert_skill_learning/impress_full_v1/generated/round_01/coverage_state.json \
  --packet-root evaluation_examples/expert_skill_learning/impress_full_v1/generated/round_01/review_packets
```
