import requests
import json

OPA_URL = "http://localhost:8181/v1/data/vaas/authz/allow"

def v_as_a_service_proxy(action, env, risk):
    payload = {
        "input": {
            "action": action,
            "metadata": {
                "env": env,
                "risk_score": risk
            }
        }
    }
    try:
        response = requests.post(OPA_URL, json=payload)
        return response.json().get("result", False)
    except Exception as e:
        print(f"Connection Error: {e}")
        return False

# POC Scenarios
scenarios = [
    {"action": "read", "env": "production", "risk": 1, "desc": "Standard Read Access"},
    {"action": "delete", "env": "production", "risk": 5, "desc": "UNAUTHORIZED Production Delete"},
    {"action": "delete", "env": "sandbox", "risk": 2, "desc": "AUTHORIZED Sandbox Delete"},
    {"action": "read", "env": "production", "risk": 15, "desc": "KILL SWITCH TRIGGERED (High Risk)"}
]

print("--- VaaS POC: Sidecar Policy Enforcement Results ---")
for s in scenarios:
    permitted = v_as_a_service_proxy(s['action'], s['env'], s['risk'])
    status = "✅ ALLOWED" if permitted else "❌ BLOCKED"
    print(f"Scenario: {s['desc']} -> {status}")