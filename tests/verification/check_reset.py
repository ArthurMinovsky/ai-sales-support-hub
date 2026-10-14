"""Verify disposable Docker data and stale-token rejection on an isolated stack."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import secrets
import subprocess
import time
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

ROOT = Path(__file__).resolve().parents[2]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if not args.project.startswith("saleshub-reset-"):
        parser.error("Use an isolated saleshub-reset-* project; never target a shared stack.")
    compose = ["docker", "compose", "-p", args.project, "-f", "compose.yaml", "-f", "compose.e2e.yaml"]
    commands = []
    report = {"test_ids": ["TEST-010", "TEST-003", "TEST-004", "TEST-020", "TEST-021"],
              "project": args.project, "started_at": datetime.now(timezone.utc).isoformat(),
              "status": "FAIL", "checks": [], "commands": commands}
    def run(tail):
        result = subprocess.run(compose + tail, cwd=ROOT, capture_output=True, text=True)
        commands.append({"command": compose + tail, "exit_code": result.returncode})
        if result.returncode:
            raise RuntimeError("Compose operation failed: " + " ".join(tail) + "\n" + result.stderr[-1500:])
        return result.stdout.strip()
    def ports():
        def port(service, internal):
            return run(["port", "--index", "1", service, str(internal)]).splitlines()[0].rsplit(":", 1)[1]
        return "http://localhost:" + port("api", 8000), "http://localhost:" + port("web", 3000)
    def call(base, path, method="GET", body=None, token=None):
        headers = {}
        if token: headers["Authorization"] = "Bearer " + token
        if body is not None: headers["Content-Type"] = "application/json"
        request = Request(base + path, data=None if body is None else json.dumps(body).encode(), headers=headers, method=method)
        try:
            response = urlopen(request, timeout=5)
            code, data = response.status, response.read()
        except HTTPError as error:
            code, data = error.code, error.read()
        try:
            payload = json.loads(data) if data else None
        except json.JSONDecodeError:
            payload = None  # Readiness also checks HTML endpoints.
        return code, payload
    def ready():
        deadline = time.monotonic() + 180
        while time.monotonic() < deadline:
            try:
                api, web = ports()
                if call(api, "/health")[0] == 200 and call(web, "/login")[0] == 200:
                    assert call(api, "/openapi.json")[0] == 200
                    assert call(api, "/docs")[0] == 200
                    return api, web
            except (URLError, TimeoutError, ConnectionError, RuntimeError):
                pass
            time.sleep(1)
        raise RuntimeError("API/Web readiness timeout")
    def register(api, password):
        code, user = call(api, "/api/auth/register", "POST",
                          {"username": " RESET_PROBE ", "password": password, "confirm_password": password})
        assert code == 201 and set(user) == {"id", "username", "created_at"}
        code, response = call(api, "/api/auth/login", "POST", {"username": "Reset_Probe", "password": password})
        assert code == 200 and response["expires_in"] == 3600
        return user["id"], response["access_token"]
    def core(product):
        return {key: product[key] for key in ("name", "brand", "description", "category", "type", "subtype", "image_url")}
    try:
        run(["restart", "api"])
        api, web = ready()
        container = run(["ps", "-q", "api"])
        inspection = subprocess.run(["docker", "inspect", "--format", "{{json .HostConfig.Tmpfs}}", container], capture_output=True, text=True, check=True)
        options = json.loads(inspection.stdout)["/data"]
        assert all(option in options.split(",") for option in ("size=64m", "uid=10001", "gid=10001", "mode=0700"))
        assert run(["exec", "-T", "api", "id", "-u"]) == "10001"
        report["storage"] = {"mount": "/data", "type": "tmpfs", "options": options, "api_uid": 10001}
        password = secrets.token_urlsafe(24)
        user_id, token = register(api, password)
        assert user_id == 1
        status, baseline = call(api, "/api/products", token=token)
        assert status == 200 and len(baseline) == 10
        assert all(p["brand"] in ("Demo Sensors", "Demo Automation") for p in baseline)
        canonical = [core(p) for p in baseline]
        for operation in ("restart", "recreate"):
            seed = core(baseline[0])
            seed["name"] = "Edited reset probe"
            assert call(api, "/api/products/" + str(baseline[0]["id"]), "PUT", seed, token)[0] == 200
            extra = {**seed, "name": "Temporary reset product"}
            assert call(api, "/api/products", "POST", extra, token)[0] == 201
            assert len(call(api, "/api/products", token=token)[1]) == 11
            previous = token
            previous_password = password
            if operation == "restart":
                run(["restart", "api"])
            else:
                run(["up", "--no-deps", "--force-recreate", "-d", "--wait", "--wait-timeout", "180", "api"])
            api, web = ready()
            assert call(api, "/api/auth/login", "POST", {"username": "reset_probe", "password": previous_password})[0] == 401
            password = secrets.token_urlsafe(24)
            next_id, token = register(api, password)
            assert next_id == user_id
            for route in ("/api/auth/me", "/api/products"):
                assert call(api, route, token=previous)[0] == 401
            assert call(api, "/api/suggestions", "POST", {"query": "gateway"}, previous)[0] == 401
            assert call(api, "/api/auth/me", token=token)[0] == 200
            _, restored = call(api, "/api/products", token=token)
            assert [core(p) for p in restored] == canonical
            report["checks"].append({"operation": operation, "old_login": 401,
                                     "reused_user_id": next_id, "stale_token": 401, "new_token": 200,
                                     "restored_demo_products": len(restored), "api": api, "web": web})
        report["status"] = "PASS"
    except Exception as error:
        report["error"] = str(error)
    report["source_revision"] = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    tracked = subprocess.check_output(["git", "ls-files", "backend", "web/src", "web/package.json",
                                      "web/package-lock.json", "compose.yaml"], cwd=ROOT, text=True).splitlines()
    report["file_hashes"] = {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
                             for name in tracked if (ROOT / name).is_file()}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({key: report[key] for key in ("status", "checks")} , indent=2))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
