from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import subprocess
import json
import os

app = FastAPI(title="Test Planner Agent Bridge")

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class JiraPayload(BaseModel):
    url: str
    auth: dict # {"email": "...", "token": "..."}

class LLMPayload(BaseModel):
    provider: str
    endpoint: str | None = None
    api_key: str | None = None
    model: str | None = None

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/api/test-jira")
def test_jira(payload: JiraPayload):
    try:
        cmd = ["python", "tools/test_jira_connection.py", json.dumps(payload.dict())]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            return {"status": "error", "message": result.stderr or "Unknown error"}
        return json.loads(result.stdout)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/test-llm")
def test_llm(payload: LLMPayload):
    try:
        cmd = ["python", "tools/test_llm_connection.py", json.dumps(payload.dict())]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            return {"status": "error", "message": result.stderr or "Unknown error"}
        return json.loads(result.stdout)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class GenerationPayload(BaseModel):
    jira_id: str
    context: str | None = ""
    jira_config: dict
    llm_config: dict

@app.post("/api/generate-plan")
def generate_plan(payload: GenerationPayload):
    """
    Orchestrates the entire test plan generation flow.
    """
    try:
        # 1. Fetch Jira Data
        jira_cmd = ["python", "tools/jira_fetcher.py", json.dumps({"jira_id": payload.jira_id, "config": payload.jira_config})]
        jira_res = subprocess.run(jira_cmd, capture_output=True, text=True)
        jira_data = json.loads(jira_res.stdout)
        
        if jira_data.get("status") == "error":
            return jira_data

        # 2. Generate Test Cases via LLM
        llm_payload = {
            "jira_data": jira_data,
            "context": payload.context,
            "llm_config": payload.llm_config
        }
        llm_cmd = ["python", "tools/llm_processor.py", json.dumps(llm_payload)]
        llm_res = subprocess.run(llm_cmd, capture_output=True, text=True)
        llm_data = json.loads(llm_res.stdout)

        if llm_data.get("status") == "error":
            return llm_data

        # 3. Populate Template (.docx)
        template_name = "Test Plan - Template.docx"
        template_path = os.path.join("Test Plan Templates", template_name)
        output_name = f"TestPlan_{payload.jira_id}.docx"
        output_path = os.path.join("deliverables", output_name)
        
        doc_data = {
            "jira_id": payload.jira_id,
            "summary": jira_data.get("summary"),
            "description": str(jira_data.get("description")),
            "test_cases": llm_data.get("text"),
            "project": jira_data.get("project")
        }
        
        gen_payload = {
            "data": doc_data,
            "template_path": template_path,
            "output_path": output_path
        }
        gen_cmd = ["python", "tools/plan_generator.py", json.dumps(gen_payload)]
        gen_res = subprocess.run(gen_cmd, capture_output=True, text=True)
        
        return json.loads(gen_res.stdout)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
