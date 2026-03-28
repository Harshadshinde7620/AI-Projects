import sys
import json
import requests
from requests.auth import HTTPBasicAuth

def test_jira_connection(payload):
    """
    Verifies Jira API connection using provided URL, email, and API token.
    Payload shape: {"url": "...", "auth": {"email": "...", "token": "..."}}
    """
    url = payload.get("url")
    email = payload.get("auth", {}).get("email")
    token = payload.get("auth", {}).get("token")
    
    if not all([url, email, token]):
        return {"status": "error", "message": "Missing credentials (URL, Email, or Token)"}
    
    # Endpoint to verify connection: Jira Cloud Myself endpoint
    endpoint = f"{url.rstrip('/')}/rest/api/3/myself"
    
    try:
        response = requests.get(
            endpoint,
            auth=HTTPBasicAuth(email, token),
            headers={"Accept": "application/json"},
            timeout=10
        )
        if response.status_code == 200:
            return {
                "status": "success", 
                "message": "Connected to Jira successfully", 
                "user": response.json().get("displayName")
            }
        else:
            return {
                "status": "error", 
                "message": f"Jira returned status code {response.status_code}", 
                "details": response.text[:200]
            }
    except requests.exceptions.RequestException as e:
        return {"status": "error", "message": f"Connection failed: {str(e)}"}

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"status": "error", "message": "No input payload provided"}))
        sys.exit(1)
    
    try:
        input_data = json.loads(sys.argv[1])
        result = test_jira_connection(input_data)
        print(json.dumps(result))
    except json.JSONDecodeError:
        print(json.dumps({"status": "error", "message": "Invalid JSON input"}))
