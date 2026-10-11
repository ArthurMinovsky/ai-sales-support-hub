"""Only for isolated CI/E2E; NEVER evidence of real OpenRouter inference."""
from http.server import BaseHTTPRequestHandler, HTTPServer
import json


class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path != "/api/v1/chat/completions":
            self.send_error(404); return
        length = int(self.headers.get("Content-Length", "0"))
        data = json.loads(self.rfile.read(length))
        user_payload = json.loads(data["messages"][1]["content"])
        if "FORCE_PROVIDER_ERROR" in user_payload["customer_needs"]:
            self.send_response(429); self.end_headers(); return
        ids = [item["product_id"] for item in user_payload["candidate_products"]]
        result = {"suggestions": [{"product_id": ids[0], "reason": "Catalog demo fixture matched a requested capability"}]} if ids else {"suggestions": []}
        response = json.dumps({"choices": [{"message": {"content": json.dumps(result)}}]}).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(response)))
        self.end_headers()
        self.wfile.write(response)


if __name__ == "__main__":
    HTTPServer(("0.0.0.0", 9999), Handler).serve_forever()
