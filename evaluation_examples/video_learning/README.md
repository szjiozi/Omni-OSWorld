# OSWorld Video Learning

Phase 0 contains two Impress and two Calc tasks with deterministic local
fixtures. Generate and validate them from the repository root:

```bash
python scripts/python/generate_phase0_fixtures.py
python scripts/python/validate_phase0_tasks.py
```

The local validator checks task and SkillIR schemas, fixture hashes, video
decoding, and Office task rules. It uses the native OSWorld evaluators when
their optional dependencies are installed; otherwise it reports the explicit
`phase0_compatible` structural fallback used for these four fixtures. Every
initial artifact must fail and every gold artifact must pass.

With a configured Daytona Office snapshot, run the full setup/evaluator path:

```bash
bash scripts/bash/validate_phase0_daytona.sh
```

The Daytona path always exercises the native OSWorld setup and evaluator
pipeline; a local fallback result is not treated as Daytona acceptance.

Record a human demonstration for one task:

```bash
python scripts/python/manual_explore.py \
  --provider_name daytona \
  --headless \
  --task-config evaluation_examples/video_learning/examples/libreoffice_impress/0f4e50c1-0c2c-4f83-9ea9-48f7b67e1001.json
```
