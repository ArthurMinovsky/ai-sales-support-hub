"""Regression checks for TEST-019 report and severity evaluation."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[2] / "scripts/security/triage.py"
spec = importlib.util.spec_from_file_location("security_triage", SCRIPT)
triage = importlib.util.module_from_spec(spec)
spec.loader.exec_module(triage)


class SecurityTriageTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.write("sca/pip-audit.json", {"dependencies": [{"name": "example", "vulns": []}]})
        self.write("sca/npm-audit.json", {"metadata": {"vulnerabilities": {"total": 0}}})
        self.write("sast/semgrep.json", {"results": [], "errors": [], "paths": {"scanned": ["example.py"]}})
        self.write("iac/checkov.json", [{"check_type": "dockerfile", "summary": {"passed": 1, "failed": 0, "parsing_errors": 0}}])
        self.write("dast/zap.json", {"site": [{"@name": "http://web:3000", "alerts": []}]})
        self.write_text("dast/zap.html", "<html>" + ("Complete report " * 20) + "</html>")
        for name in ["sca/pip-audit", "sca/npm-audit", "sast/semgrep", "iac/checkov", "dast/zap"]:
            self.write_text(name + "-exit.txt", "0\n")

    def write(self, name, value):
        self.write_text(name, json.dumps(value))

    def write_text(self, name, value):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(value)

    def verdict(self):
        return triage.evaluate(self.root, ["sca", "sast", "iac", "dast"])

    def test_complete_clean_reports_pass(self):
        self.assertEqual(self.verdict()["status"], "PASS")

    def test_missing_html_fails_despite_zero_zap_exit(self):
        (self.root / "dast/zap.html").unlink()
        self.assertEqual(self.verdict()["scans"]["dast"]["status"], "FAIL")

    def test_invalid_json_fails_despite_zero_exit(self):
        self.write_text("sast/semgrep.json", "{invalid")
        self.assertEqual(self.verdict()["scans"]["sast"]["status"], "FAIL")

    def test_scanner_error_fails(self):
        self.write("sast/semgrep.json", {"results": [], "errors": [{"message": "scan failed"}]})
        self.assertEqual(self.verdict()["scans"]["sast"]["status"], "FAIL")

    def test_zero_scanned_files_fails(self):
        self.write("sast/semgrep.json", {"results": [], "errors": [], "paths": {"scanned": []}})
        self.assertEqual(self.verdict()["scans"]["sast"]["status"], "FAIL")

    def test_sca_finding_fails(self):
        self.write("sca/npm-audit.json", {"metadata": {"vulnerabilities": {"total": 1}}})
        self.assertEqual(self.verdict()["scans"]["sca"]["status"], "FAIL")

    def test_nonzero_tool_exit_fails(self):
        self.write_text("sca/pip-audit-exit.txt", "3\n")
        self.assertEqual(self.verdict()["scans"]["sca"]["status"], "FAIL")

    def test_iac_parsing_error_fails(self):
        self.write("iac/checkov.json", [{"check_type": "dockerfile", "summary": {"passed": 1, "failed": 0, "parsing_errors": 1}}])
        self.assertEqual(self.verdict()["scans"]["iac"]["status"], "FAIL")

    def test_high_dast_finding_fails(self):
        self.write("dast/zap.json", {"site": [{"alerts": [{"riskcode": "3", "name": "High test finding", "riskdesc": "High", "instances": []}]}]})
        self.assertEqual(self.verdict()["scans"]["dast"]["status"], "FAIL")

    def test_informational_alert_is_retained_with_review_required(self):
        self.write("dast/zap.json", {"site": [{"alerts": [{"riskcode": "0", "name": "Modern Web Application", "riskdesc": "Informational", "instances": []}]}]})
        self.write_text("dast/zap-exit.txt", "2\n")
        report = self.verdict()["scans"]["dast"]
        self.assertEqual(report["status"], "PASS")
        self.assertTrue(report["observed"]["review_required"])
        self.assertEqual(report["observed"]["severity_by_alert_type"]["informational"], 1)


if __name__ == "__main__":
    unittest.main()

