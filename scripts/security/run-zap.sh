#!/usr/bin/env bash
# Keep ZAP's work directory inside its own container; copy reports after exit.
# This avoids host/runner UID mismatches and does not run the scanner as root.
set -uo pipefail
report_dir="${1:?Provide an absolute report directory}"
target="${2:?Provide the ready test target}"
network="${3:-host}"
image="${ZAP_IMAGE:-ghcr.io/zaproxy/zaproxy:stable}"
scanner="saleshub-zap-$$-${RANDOM}"
created=0
mkdir -p "$report_dir"
cleanup() {
  if [[ "$created" == 1 ]]; then
    docker rm -f "$scanner" > "$report_dir/container-cleanup.log" 2>&1
    printf '%s\n' "$?" > "$report_dir/cleanup-exit.txt"
  fi
}
trap cleanup EXIT
printf '%s\n' "$target" > "$report_dir/target.txt"
date -u +%FT%TZ > "$report_dir/started-at.txt"
docker create --name "$scanner" --network "$network" "$image" \
  sh -c 'mkdir -p /zap/wrk && cd /zap/wrk && zap.sh -version > version.txt && exec zap-baseline.py "$@"' \
  sh -t "$target" -J zap.json -r zap.html > "$report_dir/container-id.txt" 2> "$report_dir/create.log"
create_status=$?
printf '%s\n' "$create_status" > "$report_dir/create-exit.txt"
if [[ "$create_status" != 0 ]]; then exit "$create_status"; fi
created=1
docker inspect "$scanner" --format '{{.Image}}' > "$report_dir/image-id.txt"
docker start -a "$scanner" > "$report_dir/scanner.log" 2>&1
printf '%s\n' "$?" > "$report_dir/start-exit.txt"
docker inspect "$scanner" --format '{{.State.ExitCode}}' > "$report_dir/zap-exit.txt"
docker cp "$scanner:/zap/wrk/." "$report_dir/" > "$report_dir/copy.log" 2>&1
copy_status=$?
printf '%s\n' "$copy_status" > "$report_dir/copy-exit.txt"
date -u +%FT%TZ > "$report_dir/finished-at.txt"
if [[ "$copy_status" != 0 || ! -s "$report_dir/zap.json" || ! -s "$report_dir/zap.html" ]]; then
  echo "ZAP report collection failed; inspect retained scanner/copy logs." >&2
  exit 1
fi
# Collection success is separate from ZAP's exit and findings; triage evaluates both.

