# Project Memory: Task Plan

## Phase 1: B - Blueprint 🚧
- [x] Create `deliverables/` folder.
- [ ] Answer Discovery Questions (Wait for User).
- [ ] Define JSON Data Schema for:
    - Jira/ADO Payload (Feature info).
    - LLM Configuration (Ollama, GROQ, Grok).
    - Template Placeholder mapping.
- [ ] Research Jira/ADO API documentation for on-the-fly fetching.
- [ ] Approve Phase 1 Blueprint.

## Phase 2: L - Link 📝
- [ ] Setup `tools/` for Jira/ADO connection testing.
- [ ] Setup `tools/` for LLM connection testing (Ollama/GROQ/Grok).
- [ ] Build "Test Connection" script.

## Phase 3: A - Architect 📝
- [ ] Create `architecture/` SOPs for:
    - On-the-fly Connection Handling.
    - Template Population (Docx manipulation).
    - UI Screenshot context extraction.
- [ ] Build `tools/` Python scripts for:
    - Jira/ADO fetcher.
    - Document generator (`[Filename]_[JiraID].docx`).
    - Context aggregator (Jira + UI + Manual Context).

## Phase 4: S - Stylize 📝
- [ ] Refine Test Plan format for professional delivery.
- [ ] Implement multi-format exports if needed.

## Phase 5: T - Trigger 📝
- [ ] Setup automation triggers (e.g., CLI or Webhook).
- [ ] Finalize Maintenance Log.
