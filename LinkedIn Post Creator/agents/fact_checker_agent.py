from ollama.client import generate

def fact_check(post):
    prompt = f"""
    Review this LinkedIn post for factual accuracy:

    {post}

    Tasks:
    - Identify any incorrect or risky claims
    - If needed, rewrite those parts safely
    - Keep the tone professional
    - Do not add explanations

    Return ONLY the corrected post.
    """

    response = generate(prompt)

    return response.strip().replace('"', '') if response else post
    