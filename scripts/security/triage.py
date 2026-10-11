"""Collate four scanner execution reports without manufacturing PASS labels."""
from datetime import datetime, timezone
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[2]
SOURCES = {
    "sca": ["sca/pip-audit.json", "sca/npm-audit.json"],
    "sast": ["sast/semgrep.json"],
    "dast": ["dast/zap.json"],
    "iac": ["iac/results_json.json"],
}


def main():
    parent = ROOT / "evidence/security"
    result = {"generated_at": datetime.now(timezone.utc).isoformat(), "notice": "Scanner execution evidence; availability is not vulnerability clearance", "scans": {}}
    for category, expected in SOURCES.items():
        files = [parent / path for path in expected]
        present = [str(path.relative_to(ROOT)) for path in files if path.exists() and path.stat().st_size]
        blockers = list((parent / category).glob("*.missing")) + list((parent / category).glob("BLOCKED*"))
        result["scans"][category] = {
            "status": "REPORT_PRESENT_REVIEW_REQUIRED" if present else "UNVERIFIED_OR_BLOCKED",
            "reports": present,
            "blockers": [] if present else [str(p.relative_to(ROOT)) for p in blockers],
        }
    parent.mkdir(parents=True, exist_ok=True)
    (parent / "triage-summary.json").write_text(json.dumps(result, indent=2))
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
