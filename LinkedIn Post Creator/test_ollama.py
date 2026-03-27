from ollama.client import generate

response = generate("Give me one LinkedIn post idea about API testing")

print("\nResponse from Ollama:\n")
print(response)