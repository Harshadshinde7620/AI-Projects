import sys
import json
import requests

def test_llm_connection(payload):
    """
    Tests connectivity to various LLM providers (Ollama, GROQ, Grok).
    Payload shape: {"provider": "...", "endpoint": "...", "api_key": "...", "model": "..."}
    """
    provider = payload.get("provider", "").lower()
    endpoint = payload.get("endpoint")
    api_key = payload.get("api_key")
    model = payload.get("model")

    if not provider:
        return {"status": "error", "message": "No provider specified"}

    try:
        if provider == "ollama":
            # Default Ollama tags endpoint to check availability
            url = f"{endpoint.rstrip('/')}/api/tags" if endpoint else "http://localhost:11434/api/tags"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                return {"status": "success", "message": "Ollama is reachable", "models": response.json().get("models", [])}
            
        elif provider in ["groq", "grok"]:
            if not api_key:
                return {"status": "error", "message": f"API Key required for {provider}"}
            
            # Use a minimal chat completion request to test the key
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            # Placeholder for GROQ/Grok OpenAI-compatible endpoint
            url = endpoint if endpoint else "https://api.groq.com/openai/v1/chat/completions"
            data = {
                "model": model if model else "llama3-8b-8192",
                "messages": [{"role": "user", "content": "ping"}],
                "max_tokens": 1
            }
            response = requests.post(url, headers=headers, json=data, timeout=10)
            if response.status_code == 200:
                return {"status": "success", "message": f"{provider.capitalize()} API is functional"}
            else:
                return {"status": "error", "message": f"{provider.capitalize()} API returned error {response.status_code}", "details": response.text[:200]}

        return {"status": "error", "message": f"Provider '{provider}' not yet supported or configured incorrectly"}

    except Exception as e:
        return {"status": "error", "message": f"LLM Connection failed: {str(e)}"}

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"status": "error", "message": "No input payload provided"}))
        sys.exit(1)
    
    try:
        input_data = json.loads(sys.argv[1])
        result = test_llm_connection(input_data)
        print(json.dumps(result))
    except json.JSONDecodeError:
        print(json.dumps({"status": "error", "message": "Invalid JSON input"}))
