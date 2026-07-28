#!/usr/bin/env bash
set -euo pipefail

if [[ -z "${DAYTONA_API_KEY:-}" ]]; then
  echo "DAYTONA_API_KEY is not set" >&2
  exit 2
fi

if [[ -z "${DAYTONA_OSWORLD_SNAPSHOT:-}" ]]; then
  echo "DAYTONA_OSWORLD_SNAPSHOT is not set" >&2
  exit 2
fi

python scripts/python/generate_phase0_fixtures.py
python -m desktop_env.providers.daytona.smoke_test
python -m desktop_env.providers.daytona.soak_test \
  --iterations 10 \
  --report results/daytona_phase0_soak.json
python scripts/python/validate_phase0_tasks.py \
  --daytona \
  --report results/phase0_daytona_tasks.json

echo "Phase 0 Daytona validation passed."
