from ollama.client import generate

def review_post(post):
    prompt = f"""
    Review and improve this LinkedIn post:

    {post}

    Fix:
    - Grammar
    - Clarity
    - Tone

    Make it:
    - More engaging
    - More professional
    - Easy to read

    Do not add explanations.
    Return only the improved post.
    """

    response = generate(prompt)

    return response.strip().replace('"', '') if response else post