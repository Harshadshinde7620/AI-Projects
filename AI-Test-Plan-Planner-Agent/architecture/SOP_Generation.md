# SOP: Test Plan Generation

## Goal
Transform Jira requirements and UI context into a professional test plan document.

## Workflow
1. **Fetch**: Retrieve User Story from Jira/ADO using `jira_fetcher.py`.
2. **Contextualize**: 
    - Extract text from screenshots (if applicable).
    - Combine with manually provided context.
3. **Reason**: Send the requirements to the selected LLM (Ollama/GROQ/Grok) to generate detailed test cases.
4. **Populate**: Use `plan_generator.py` to inject the generated test cases into the `.docx` template.
5. **Deliver**: Save the output to `deliverables/` using the format `[Filename]_[JiraID].docx`.

## Placeholders
The template should include the following placeholders:
- `{{JIRA_ID}}`
- `{{SUMMARY}}`
- `{{DESCRIPTION}}`
- `{{TEST_CASES}}`
- `{{PROJECT}}`
