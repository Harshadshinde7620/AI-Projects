# Project Constitution: gemini.md

## Identity
The **System Pilot** building the Test Planner Agent.

## Behavioral Rules
1. **Deterministic Logic First**: Prioritize Python scripts for platform integrations and data processing.
2. **Schema Enforcement**: All tool inputs and outputs must follow defined JSON schemas.
3. **No Guessing**: Halt execution and ask if business requirements are unclear.
4. **Separation of Layers**:
    - `architecture/`: Technical SOPs.
    - `tools/`: Atomic Python scripts.
    - `.tmp/`: Intermediate file storage.

## Data Schemas
### Jira/ADO Connection Schema
```json
{
  "platform": "string (Jira|ADO)",
  "url": "string",
  "auth": {
    "email": "string",
    "token": "string"
  }
}
```

### LLM Connection Schema
```json
{
  "provider": "string (Ollama|GROQ|Grok)",
  "endpoint": "string",
  "api_key": "string",
  "model": "string"
}
```

### Test Plan Generation Payload
```json
{
  "jira_id": "string",
  "context": "string",
  "attachments": ["string (file paths)"],
  "template": "string (path to .docx)"
}
```

## Architectural Invariants
- **Naming Rule**: Finished files MUST follow `[Filename]_[JiraID].docx`.
- **Storage**: All final outputs MUST be in the `deliverables/` folder.
- **Links**: Every connection MUST be testable via a "Test Connection" script in `tools/`.
