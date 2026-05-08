import httpx
import uvicorn
import threading
import time
import requests
from fastapi import FastAPI, Request, Response

app = FastAPI()

# --- VaaS TRANSPARENT PROXY ---
OPA_URL = "http://localhost:8181/v1/data/vaas/authz/allow"

@app.api_route("/{path:path}", methods=["POST"])
async def vaas_proxy(request: Request, path: str):
    body = await request.json()
    
    # Semantic mapping of tool-call to policy input
    check_payload = {
        "input": {
            "action": path,
            "metadata": body.get("metadata", {})
        }
    }

    async with httpx.AsyncClient() as client:
        try:
            opa_resp = await client.post(OPA_URL, json=check_payload)
            allowed = opa_resp.json().get("result", False)
        except Exception:
            allowed = False # Fail-closed for security

    if not allowed:
        return Response(
            content='{"status": "BLOCKED", "reason": "VaaS Policy Violation"}',
            status_code=403
        )

    return {"status": "SUCCESS", "message": f"Action '{path}' authorized by VaaS."}

# --- AUTOMATED EVALUATION SUITE ---
def run_evaluation():
    time.sleep(3) # Wait for infrastructure and proxy to settle
    print("\n" + "="*60)
    print("VaaS ARCHITECTURAL EVALUATION: SYSTEM START")
    print("="*60)

    proxy_url = "http://localhost:8000"
    
    scenarios = [
        ("read", {"env": "production", "risk_score": 1}, "Baseline Read Access"),
        ("delete", {"env": "production", "risk_score": 5}, "Unauthorized Prod Deletion"),
        ("delete", {"env": "sandbox", "risk_score": 2}, "Authorized Sandbox Deletion"),
        ("read", {"env": "production", "risk_score": 15}, "Kill Switch (Extreme Risk)")
    ]

    for action, meta, desc in scenarios:
        print(f"\n[SCENARIO]: {desc}")
        try:
            resp = requests.post(f"{proxy_url}/{action}", json={"metadata": meta})
            status = "✅ ALLOWED" if resp.status_code == 200 else "❌ BLOCKED"
            detail = resp.json().get('message' if resp.status_code == 200 else 'reason')
            print(f"RESULT: {status} | Detail: {detail}")
        except Exception as e:
            print(f"Connection Error: {e}")
    
    print("\n" + "="*60)
    print("EVALUATION COMPLETE: DATA LOGGED FOR AIES 2026")
    print("="*60)

if __name__ == "__main__":
    threading.Thread(target=run_evaluation, daemon=True).start()
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="error")