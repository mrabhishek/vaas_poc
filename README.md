# VaaS: Validation-as-a-Service Governance POC

A deterministic governance framework for AI Agents using the **Sidecar Proxy Pattern**. This project demonstrates how to intercept stochastic LLM outputs and enforce safety policies using **Open Policy Agent (OPA)**.

## 🏗 Architecture

The system decouples "Intelligence" (LLM) from "Policy" (Rego/OPA) to ensure that a hallucinating AI cannot bypass security guardrails.

```mermaid
graph TD
    User((User)) -->|Prompt| Agent[LLM Agent: TinyLlama]
    Agent -->|1. Proposed Intent| Proxy[VaaS Proxy: FastAPI]
    Proxy -->|2. Validate| OPA[OPA Engine]
    OPA -->|3. Policy Check| Rego{policy.rego}
    Rego -->|4. Allow/Deny| Proxy
    Proxy -->|5. Execute| Infrastructure[(Protected Resources)]
