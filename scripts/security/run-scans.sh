#!/usr/bin/env bash
# Collect TEST-019 reports and preserve each scanner's actual exit status.
set -uo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"
mkdir -p evidence/security/{sca,sast,dast,iac}
# Keep independent results even when one tool exits nonzero.
run_report() {
  local name="$1"; shift
  printf 'Executing %s: %q ' "$name" "$@"; echo
  "$@"; local status=$?
  printf '%s
' "$status" > "evidence/security/$name/exit-code.txt"
  return 0
}

if command -v pip-audit >/dev/null; then
  run_report sca pip-audit --format json --output evidence/security/sca/pip-audit.json
else
  echo 'pip-audit unavailable' | tee evidence/security/sca/pip-audit.missing
fi
if command -v npm >/dev/null; then
  (cd web && npm audit --json > ../evidence/security/sca/npm-audit.json); printf '%s
' "$?" > evidence/security/sca/npm-audit-exit-code.txt
else
  echo 'npm unavailable' > evidence/security/sca/npm-audit.missing
fi
if command -v semgrep >/dev/null; then
  run_report sast semgrep scan --config .semgrep.yml --json --output evidence/security/sast/semgrep.json .
else
  echo 'semgrep unavailable' > evidence/security/sast/semgrep.missing
fi
if command -v checkov >/dev/null; then
  run_report iac checkov -f backend/Dockerfile -f web/Dockerfile -f compose.yaml -f .github/workflows/ci.yml --output json --output-file-path evidence/security/iac
else
  echo 'checkov unavailable' > evidence/security/iac/checkov.missing
fi
# DAST requires an already healthy live target. CI runs this only after readiness.
DAST_TARGET="${DAST_TARGET:-}"
API_BASE_URL="${API_BASE_URL:-}"
if command -v docker >/dev/null; then
  if [[ -z "$DAST_TARGET" ]]; then
    web_port="$(docker compose port --index 1 web 3000 | sed -n '1s/.*://p')"
    [[ "$web_port" =~ ^[0-9]+$ ]] && DAST_TARGET="http://localhost:$web_port"
  fi
  if [[ -z "$API_BASE_URL" ]]; then
    api_port="$(docker compose port --index 1 api 8000 | sed -n '1s/.*://p')"
    [[ "$api_port" =~ ^[0-9]+$ ]] && API_BASE_URL="http://localhost:$api_port"
  fi
fi
if [[ -n "$DAST_TARGET" && -n "$API_BASE_URL" ]] && curl --max-time 5 -fsS "$API_BASE_URL/health" >/dev/null && curl --max-time 5 -fsS "$DAST_TARGET/login" >/dev/null; then
  # On Docker Desktop, use a Compose network and DAST_DOCKER_TARGET=http://web:3000.
  scan_target="${DAST_DOCKER_TARGET:-$DAST_TARGET}"
  printf '%s\n' "$scan_target" > evidence/security/dast/target.txt
  docker run --rm --network "${DAST_DOCKER_NETWORK:-host}" -v "$ROOT/evidence/security/dast:/zap/wrk:rw" ghcr.io/zaproxy/zaproxy:stable zap-baseline.py -t "$scan_target" -J zap.json -r zap.html -I
  printf '%s
' "$?" > evidence/security/dast/exit-code.txt
else
  echo 'DAST prerequisite not ready (Docker or health target)' > evidence/security/dast/BLOCKED.txt
fi
python3 scripts/security/triage.py
