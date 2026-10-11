#!/usr/bin/env bash
# Execute TEST-019 in a new evidence directory; retain actual logs/statuses.
set -uo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"
REPORT_DIR="${SECURITY_EVIDENCE_DIR:-$ROOT/evidence/security/runs/$(date -u +%Y%m%dT%H%M%SZ)}"
CATEGORIES="${SECURITY_CATEGORIES:-sca,sast,iac,dast}"
export SECURITY_EVIDENCE_DIR="$REPORT_DIR"
mkdir -p "$REPORT_DIR"/{sca,sast,dast,iac}
run_report() {
  local category="$1" name="$2"; shift 2
  printf '%q ' "$@" > "$REPORT_DIR/$category/$name-command.txt"
  printf '\n' >> "$REPORT_DIR/$category/$name-command.txt"
  "$@" > "$REPORT_DIR/$category/$name.log" 2>&1
  local status=$?
  printf '%s\n' "$status" > "$REPORT_DIR/$category/$name-exit.txt"
}
requested() { [[ ",$CATEGORIES," == *",$1,"* ]]; }
python3 - <<'PY'
from datetime import datetime, timezone
from pathlib import Path
import hashlib, json, os, platform, subprocess
root = Path.cwd()
paths = subprocess.check_output(["git", "ls-files", "-co", "--exclude-standard"], text=True).splitlines()
files = {p: hashlib.sha256((root / p).read_bytes()).hexdigest() for p in sorted(set(paths)) if (root / p).is_file()}
digest = hashlib.sha256(json.dumps(files, sort_keys=True).encode()).hexdigest()
metadata = {"started_at": datetime.now(timezone.utc).isoformat(), "source_revision": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(), "source_digest": digest, "file_hashes": files, "platform": platform.platform(), "categories": os.environ.get("SECURITY_CATEGORIES", "sca,sast,iac,dast")}
(Path(os.environ["SECURITY_EVIDENCE_DIR"]) / "source.json").write_text(json.dumps(metadata, indent=2) + "\n")
PY
if requested sca; then
  pip-audit --version > "$REPORT_DIR/sca/pip-audit-version.txt" 2>&1
  run_report sca pip-audit pip-audit -f json -o "$REPORT_DIR/sca/pip-audit.json"
  npm --version > "$REPORT_DIR/sca/npm-version.txt" 2>&1
  (cd web && npm audit --json > "$REPORT_DIR/sca/npm-audit.json" 2> "$REPORT_DIR/sca/npm-audit.log")
  printf '%s\n' "$?" > "$REPORT_DIR/sca/npm-audit-exit.txt"
fi
if requested sast; then
  semgrep --version > "$REPORT_DIR/sast/semgrep-version.txt" 2>&1
  run_report sast semgrep semgrep scan --config .semgrep.yml --json --output "$REPORT_DIR/sast/semgrep.json" .
fi
if requested iac; then
  checkov --version > "$REPORT_DIR/iac/checkov-version.txt" 2>&1
  checkov -d . --framework dockerfile,github_actions --output json > "$REPORT_DIR/iac/checkov.json" 2> "$REPORT_DIR/iac/checkov.log"
  printf '%s\n' "$?" > "$REPORT_DIR/iac/checkov-exit.txt"
fi
if requested dast; then
  target="${DAST_TARGET:-}"
  api="${API_BASE_URL:-}"
  if [[ -z "$target" ]]; then
    port="$(docker compose port --index 1 web 3000 | sed -n '1s/.*://p')"
    [[ "$port" =~ ^[0-9]+$ ]] && target="http://localhost:$port"
  fi
  if [[ -z "$api" ]]; then
    port="$(docker compose port --index 1 api 8000 | sed -n '1s/.*://p')"
    [[ "$port" =~ ^[0-9]+$ ]] && api="http://localhost:$port"
  fi
  if [[ -n "$target" && -n "$api" ]] && curl --max-time 5 -fsS "$api/health" > "$REPORT_DIR/dast/api-readiness.json" && curl --max-time 5 -fsS "$target/login" > "$REPORT_DIR/dast/web-readiness.html"; then
    bash scripts/security/run-zap.sh "$REPORT_DIR/dast" "${DAST_DOCKER_TARGET:-$target}" "${DAST_DOCKER_NETWORK:-host}"
    printf '%s\n' "$?" > "$REPORT_DIR/dast/collection-exit.txt"
  else
    echo "DAST target did not pass Web/API readiness" > "$REPORT_DIR/dast/BLOCKED.txt"
  fi
fi
python3 scripts/security/triage.py --evidence-dir "$REPORT_DIR" --categories "$CATEGORIES"
