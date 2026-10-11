#!/usr/bin/env bash
# Print the live Web / API / Swagger URLs and health for the running stack.
# Docker allocates free host ports automatically (API_PORT=0, WEB_PORT=0), so
# always run this to find the current URLs instead of guessing a fixed port.
set -uo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

# The running verification/hosting project. Override for the E2E fixture:
#   COMPOSE_PROJECT_NAME=saleshub-e2e scripts/status.sh
PROJECT="${COMPOSE_PROJECT_NAME:-saleshub-implementation-check}"

web_port="$(docker compose -p "$PROJECT" port --index 1 web 3000 2>/dev/null | sed -n '1s/.*://p')"
api_port="$(docker compose -p "$PROJECT" port --index 1 api 8000 2>/dev/null | sed -n '1s/.*://p')"

if [[ -z "$web_port" || -z "$api_port" ]]; then
  echo "Stack '$PROJECT' is not running." >&2
  echo "Start it with:  docker compose -p $PROJECT up -d --build" >&2
  exit 1
fi

web="http://localhost:$web_port"
api="http://localhost:$api_port"

health="$(curl -s -o /dev/null -w '%{http_code}' "$api/health" 2>/dev/null)"
login="$(curl -s -o /dev/null -w '%{http_code}' "$web/login" 2>/dev/null)"

printf 'Web:     %s\n' "$web"
printf 'API:     %s/health\n' "$api"
printf 'Swagger: %s/docs\n' "$api"
printf 'Checks:  health=%s login=%s\n' "${health:-—}" "${login:-—}"

if [[ "$health" != "200" ]]; then
  echo "Warning: API health did not return 200; containers may still be starting." >&2
  exit 2
fi