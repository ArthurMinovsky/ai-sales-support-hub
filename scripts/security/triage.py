"""Evaluate retained scanner reports; incomplete/tool-error results fail closed."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def evaluate(parent, categories):
    result = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "test_id": "TEST-019",
        "failure_policy": "Missing/invalid reports, tool errors and SCA/SAST/IaC findings fail. DAST high findings fail; lower findings require documented review per TEST.md.",
        "scope": "SCA installed backend/frontend dependencies; configured Python SAST rules; Dockerfile/GitHub Actions IaC; unauthenticated passive ZAP Web scan.",
        "scans": {},
    }

    def read(name):
        path = parent / name
        if not path.is_file() or not path.stat().st_size:
            raise ValueError("Missing or empty report: " + name)
        return json.loads(path.read_text())

    def code(name, allowed=(0,)):
        value = int((parent / name).read_text().strip())
        if value not in allowed:
            raise ValueError("Scanner exit " + str(value) + ": " + name)
        return value

    for category in categories:
        try:
            if category == "sca":
                pip = read("sca/pip-audit.json")
                npm = read("sca/npm-audit.json")
                deps = pip["dependencies"]
                if not deps:
                    raise ValueError("pip-audit did not record any dependency entries")
                skipped = [d.get("name") for d in deps if d.get("skip_reason")]
                vulnerabilities = sum(len(d.get("vulns", [])) for d in deps)
                npm_count = npm["metadata"]["vulnerabilities"]["total"]
                exits = [code("sca/pip-audit-exit.txt"), code("sca/npm-audit-exit.txt")]
                if vulnerabilities or npm_count:
                    raise ValueError("SCA reported dependency vulnerabilities")
                observed = {"dependency_entries": len(deps), "pip_vulnerabilities": vulnerabilities, "npm_advisories": npm_count, "skipped_packages": skipped, "exits": exits}
            elif category == "sast":
                report = read("sast/semgrep.json")
                if report["results"] or report["errors"]:
                    raise ValueError("Semgrep findings or scanner errors require resolution")
                scanned = report.get("paths", {}).get("scanned", [])
                if not scanned:
                    raise ValueError("Semgrep did not scan any source files")
                observed = {"findings": 0, "errors": 0, "scanned_files": len(scanned), "exit": code("sast/semgrep-exit.txt")}
            elif category == "iac":
                report = read("iac/checkov.json")
                reports = report if isinstance(report, list) else [report]
                if not reports:
                    raise ValueError("Empty Checkov result")
                summaries = [r["summary"] for r in reports]
                if any(not s.get("passed") and not s["failed"] for s in summaries):
                    raise ValueError("Checkov did not evaluate any checks")
                if any(s["failed"] or s.get("parsing_errors") for s in summaries):
                    raise ValueError("Checkov findings or parsing errors require resolution")
                observed = {"frameworks": [{"type": r["check_type"], "summary": r["summary"]} for r in reports], "exit": code("iac/checkov-exit.txt")}
            else:
                report = read("dast/zap.json")
                html = parent / "dast/zap.html"
                if not html.is_file() or html.stat().st_size < 100:
                    raise ValueError("Missing or empty ZAP HTML report")
                sites = report["site"]
                if not sites:
                    raise ValueError("ZAP did not record a scanned target")
                alerts = [a for site in sites for a in site.get("alerts", [])]
                severity = {"informational": 0, "low": 0, "medium": 0, "high": 0}
                for alert in alerts:
                    risk = int(alert["riskcode"])
                    if not 0 <= risk <= 3:
                        raise ValueError("Unknown ZAP risk level")
                    severity[["informational", "low", "medium", "high"][risk]] += 1
                exit_code = code("dast/zap-exit.txt", (0, 2))
                if severity["high"]:
                    raise ValueError("High ZAP finding requires resolution or explicit risk acceptance")
                observed = {
                    "severity_by_alert_type": severity,
                    "alerts": [{"id": a.get("pluginid"), "name": a["name"], "risk": a["riskdesc"], "instances": len(a.get("instances", []))} for a in alerts],
                    "exit": exit_code,
                    "target": [s.get("@name") for s in sites],
                    "review_required": bool(alerts),
                }
            result["scans"][category] = {"status": "PASS", "observed": observed}
        except (ValueError, OSError, KeyError, TypeError, json.JSONDecodeError) as error:
            result["scans"][category] = {"status": "FAIL", "reason": str(error)}
    result["status"] = "PASS" if all(s["status"] == "PASS" for s in result["scans"].values()) else "FAIL"
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--evidence-dir", type=Path, default=ROOT / "evidence/security")
    parser.add_argument("--categories", default="sca,sast,iac,dast")
    args = parser.parse_args()
    categories = args.categories.split(",")
    if not categories or any(c not in ("sca", "sast", "iac", "dast") for c in categories):
        parser.error("Use categories sca,sast,iac,dast")
    result = evaluate(args.evidence_dir, categories)
    args.evidence_dir.mkdir(parents=True, exist_ok=True)
    (args.evidence_dir / "triage-summary.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
