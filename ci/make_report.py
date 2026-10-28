import json
import os
import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

xml_file = sys.argv[1] if len(sys.argv) > 1 else "results.xml"
tests = []
if os.path.exists(xml_file):
    for case in ET.parse(xml_file).getroot().iter("testcase"):
        problem = case.find("failure")
        if problem is None:
            problem = case.find("error")
        tests.append({
            "name": case.get("name"),
            "result": "failed" if problem is not None else "passed",
            "failure_message": problem.get("message") if problem is not None else None,
        })

passed = sum(t["result"] == "passed" for t in tests)
failed = len(tests) - passed
report = {
    "repository": os.getenv("GITHUB_REPOSITORY", "local"),
    "branch": os.getenv("GITHUB_REF_NAME", "local"),
    "commit_sha": os.getenv("GITHUB_SHA", "local"),
    "pipeline_run_id": os.getenv("GITHUB_RUN_ID", "local"),
    "run_number": os.getenv("GITHUB_RUN_NUMBER", "local"),
    "timestamp": datetime.now(timezone.utc).isoformat(),
    "tests": tests,
    "summary": {"total": len(tests), "passed": passed, "failed": failed},
    "overall_status": "passed" if tests and failed == 0 else "failed",
}
with open("test-report.json", "w") as f:
    json.dump(report, f, indent=2)
print(json.dumps(report, indent=2))
