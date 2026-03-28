# SOP: Link Phase (Connectivity)

## Goal
Verify that all external services (Jira, ADO, X-Ray, LLMs) are reachable and authenticated before moving to logic architecture.

## Tool Logic: `test_jira_connection.py`
- **Input:** JSON object with `url`, `email`, and `token`.
- **Action:** Calls the Jira Cloud `/myself` endpoint.
- **Success:** Status 200 with User Info.
- **Failure:** Any non-200 status or timeout.

## Tool Logic: `test_llm_connection.py`
- **Providers:**
    - **Ollama:** Checks `/api/tags` locally.
    - **GROQ/Grok:** Performs a minimal "ping" chat completion (1 token).
- **Success:** Status 200 from the provider's API.
- **Failure:** Invalid keys, network timeouts, or rate limits.

## Handshake Verification
Every "Test Connection" button in the React UI MUST trigger these scripts via `subprocess` or a backend bridge.
