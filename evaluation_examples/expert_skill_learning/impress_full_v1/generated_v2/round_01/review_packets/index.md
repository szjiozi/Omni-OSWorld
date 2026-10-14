# Reference task review packets

Open one task directory at a time, read `TASK.md`, and fill only its `review.json` file.

| Task | Artifact | Local review |
| --- | --- | --- |
| [reference-task-impress-full-v2-r01-001](reference-task-impress-full-v2-r01-001/TASK.md) | Harbor Sampling Brief | pending |
| [reference-task-impress-full-v2-r01-002](reference-task-impress-full-v2-r01-002/TASK.md) | Harbor Air Lab: Dawn Sampling Brief | pending |
| [reference-task-impress-full-v2-r01-003](reference-task-impress-full-v2-r01-003/TASK.md) | Neighborhood Repair Café — Host Brief | pending |
| [reference-task-impress-full-v2-r01-004](reference-task-impress-full-v2-r01-004/TASK.md) | Urban Pollinator Pocket Guide | pending |
| [reference-task-impress-full-v2-r01-005](reference-task-impress-full-v2-r01-005/TASK.md) | Riverside Garden Volunteer Day | pending |

After reviewing tasks, run:

```bash
python scripts/python/manage_reference_review_packets.py collect \
  --skill-pool evaluation_examples/expert_skill_learning/impress_full_v1/generated_v2/skill_pool.json \
  --packages evaluation_examples/expert_skill_learning/impress_full_v1/generated_v2/round_01/reference_packages.json \
  --source-tasks evaluation_examples/expert_skill_learning/impress_full_v1/source_tasks.json \
  --reviews evaluation_examples/expert_skill_learning/impress_full_v1/generated_v2/round_01/reference_package_reviews.json \
  --artifact-manifest evaluation_examples/expert_skill_learning/impress_full_v1/generated_v2/round_01/artifacts/artifact_manifest.json \
  --task-config-manifest evaluation_examples/expert_skill_learning/impress_full_v1/generated_v2/round_01/task_config_manifest.json \
  --task-detail-root evaluation_examples/expert_skill_learning/impress_full_v1/generated_v2/round_01/task_details \
  --reviewer-guides evaluation_examples/expert_skill_learning/impress_full_v1/generated_v2/round_01/reviewer_guides.json \
  --coverage evaluation_examples/expert_skill_learning/impress_full_v1/generated_v2/round_01/coverage_state.json \
  --packet-root evaluation_examples/expert_skill_learning/impress_full_v1/generated_v2/round_01/review_packets
```
