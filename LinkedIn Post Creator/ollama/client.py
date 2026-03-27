import requests

def generate(prompt, model="llama3"):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "stream": False
            }
        )

        print("\nSTATUS CODE:", response.status_code)

        data = response.json()

        print("\nFULL RESPONSE JSON:\n", data)

        return data.get("response")

    except Exception as e:
        print("ERROR:", e)
        return None