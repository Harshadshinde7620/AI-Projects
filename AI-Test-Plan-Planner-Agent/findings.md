# Project Memory: Findings

## Research & Discoveries
- **Framework:** The project follows the B.L.A.S.T protocol.
- **Goal:** Intelligent test plan creator using Jira/ADO/X-Ray.
- **Connections:**
    - Jira: Added "on the fly" to fetch IDs.
    - LLM: Connection settings for Ollama, GROQ, Grok.
    - Interface: Test Connection button for all services.
- **Workflow:**
    - Input: Jira/ADO ID + Additional Context.
    - Process: Fetch ID info -> Analyze -> Generate test plan using template.
- **Assets found:**
    - `Test Plan Templates/Test Plan - Template.docx`: Target template.
    - `UI screenshots/*.jpg`: Sample UI images for additional context.
- **Output:**
    - Folder: `deliverables/`.
    - Naming convention: `[Filename]_[JiraID].docx`.

## Constraints
- **Deterministic Logic:** Business logic separated from LLM reasoning.
- **Platform Connectors:** Handle on-the-fly credentials.
- **LLMs:** Support local (Ollama) and cloud (GROQ, Grok).
