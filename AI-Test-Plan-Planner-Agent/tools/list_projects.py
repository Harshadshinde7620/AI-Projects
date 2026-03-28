import sys
import json
import requests
from requests.auth import HTTPBasicAuth

def list_projects(config):
    url = config.get("url")
    email = config.get("auth", {}).get("email")
    token = config.get("auth", {}).get("token")
    
    endpoint = f"{url.rstrip('/')}/rest/api/3/project"
    
    try:
        response = requests.get(
            endpoint,
            auth=HTTPBasicAuth(email, token),
            headers={"Accept": "application/json"},
            timeout=10
        )
        if response.status_code == 200:
            return {"status": "success", "projects": [{"key": p["key"], "name": p["name"]} for p in response.json()]}
        else:
            return {"status": "error", "message": f"Jira error {response.status_code}", "details": response.text}
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"status": "error", "message": "No input payload"}))
        sys.exit(1)
        
    try:
        payload = json.loads(sys.argv[1])
        result = list_projects(payload.get("config"))
        print(json.dumps(result))
    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e)}))
