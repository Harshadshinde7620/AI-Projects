import sys
import json
import requests
from requests.auth import HTTPBasicAuth

def fetch_jira_issue(jira_id, config):
    """
    Fetches issue details from Jira.
    """
    url = config.get("url")
    email = config.get("auth", {}).get("email")
    token = config.get("auth", {}).get("token")
    
    if not all([url, email, token, jira_id]):
        return {"status": "error", "message": "Missing credentials or Jira ID"}
    
    endpoint = f"{url.rstrip('/')}/rest/api/3/issue/{jira_id}"
    
    try:
        response = requests.get(
            endpoint,
            auth=HTTPBasicAuth(email, token),
            headers={"Accept": "application/json"},
            timeout=15
        )
        if response.status_code == 200:
            data = response.json()
            fields = data.get("fields", {})
            return {
                "status": "success",
                "jira_id": jira_id,
                "summary": fields.get("summary"),
                "description": fields.get("description"), # Note: Jira API v3 returns ADF (Atlassian Document Format)
                "project": fields.get("project", {}).get("name"),
                "issue_type": fields.get("issuetype", {}).get("name")
            }
        else:
            return {"status": "error", "message": f"Jira error {response.status_code}", "details": response.text[:200]}
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"status": "error", "message": "No input payload"}))
        sys.exit(1)
        
    try:
        payload = json.loads(sys.argv[1])
        jira_id = payload.get("jira_id")
        config = payload.get("config")
        result = fetch_jira_issue(jira_id, config)
        print(json.dumps(result))
    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e)}))
