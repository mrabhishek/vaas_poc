import httpx
import uvicorn
import os
from fastapi import FastAPI, Request, Response

app = FastAPI()
OPA_URL = os.getenv("OPA_URL", "http://opa:8181/v1/data/vaas/authz/allow")

@app.api_route("/{path:path}", methods=["POST"])
async def vaas_proxy(request: Request, path: str):
    body = await request.json()
    check_payload = {"input": {"action": path, "metadata": body.get("metadata", {})}}
    
    async with httpx.AsyncClient() as client:
        opa_resp = await client.post(OPA_URL, json=check_payload)
        allowed = opa_resp.json().get("result", False)

    if not allowed:
        return Response(content='{"status": "BLOCKED"}', status_code=403)
    return {"status": "SUCCESS"}