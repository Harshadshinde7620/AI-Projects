import sys
import json
import requests

def generate_test_cases(jira_data, context, llm_config):
    """
    Sends requirements to the configured LLM to generate test cases.
    """
    provider = llm_config.get("provider", "").lower()
    model = llm_config.get("model", "llama3:latest")
    api_key = llm_config.get("api_key")
    endpoint = llm_config.get("endpoint")

    prompt = f"""
    Generate a professional test plan with detailed test cases for the following Jira Issue:
    Jira ID: {jira_data.get('jira_id')}
    Summary: {jira_data.get('summary')}
    Description: {jira_data.get('description')}
    
    Additional Context: {context}
    
    Format the output as a clear list of test cases with ID, Description, Expected Result, and Priority.
    Only return the test cases content.
    """

    try:
        if provider == "ollama":
            url = f"{endpoint.rstrip('/')}/api/generate" if endpoint else "http://localhost:11434/api/generate"
            payload = {
                "model": model,
                "prompt": prompt,
                "stream": False
            }
            response = requests.post(url, json=payload, timeout=60)
            if response.status_code == 200:
                return {"status": "success", "text": response.json().get("response")}
                
        elif provider in ["groq", "grok"]:
            url = endpoint if endpoint else "https://api.groq.com/openai/v1/chat/completions"
            headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
            data = {
                "model": model,
                "messages": [{"role": "user", "content": prompt}]
            }
            response = requests.post(url, headers=headers, json=data, timeout=30)
            if response.status_code == 200:
                return {"status": "success", "text": response.json()["choices"][0]["message"]["content"]}
        
        return {"status": "error", "message": f"Provider {provider} failed or not configured"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"status": "error", "message": "No input payload"}))
        sys.exit(1)
        
    try:
        payload = json.loads(sys.argv[1])
        result = generate_test_cases(payload["jira_data"], payload["context"], payload["llm_config"])
        print(json.dumps(result))
    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e)}))
