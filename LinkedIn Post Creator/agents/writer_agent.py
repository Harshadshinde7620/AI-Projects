from ollama.client import generate

def write_post(topic):
    prompt = f"""
    Write a LinkedIn post on: {topic}

    Rules:
    - Start with a strong hook (1–2 lines)
    - Add spacing between paragraphs
    - Keep it engaging and professional
    - Add 2–3 relevant emojis
    - End with a question (CTA)
    - DO NOT include phrases like "Here’s a LinkedIn post"

    Length: 100–150 words
    """

    response = generate(prompt)

    if response:
        return response.strip().replace('"', '')
    
    return "No post generated"