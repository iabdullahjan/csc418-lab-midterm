import json
import os
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer

PORT = 5050
OUT_FILE = "test-report.json"


class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path != "/report":
            self.send_response(404)
            self.end_headers()
            return
        body = self.rfile.read(int(self.headers.get("Content-Length", 0)))
        try:
            report = json.loads(body)
        except json.JSONDecodeError:
            self.send_response(400)
            self.end_headers()
            return
        with open(OUT_FILE, "w") as f:
            json.dump(report, f, indent=2)
        os.makedirs("reports", exist_ok=True)
        with open(f"reports/report-{report.get('pipeline_run_id')}.json", "w") as f:
            json.dump(report, f, indent=2)
        print(f"[{datetime.now():%H:%M:%S}] saved {OUT_FILE}: "
              f"{report.get('overall_status')} (commit {str(report.get('commit_sha'))[:7]})", flush=True)
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"saved")


print(f"Receiver listening on http://localhost:{PORT}/report", flush=True)
HTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
