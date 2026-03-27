from ollama.client import generate

def get_topic():
    prompt = """
    Suggest ONLY ONE LinkedIn post topic.

    Focus:
    - QA Automation
    - Java for automation
    - AI in testing
    - API Testing[Postman/Rest assured]
    - Selenium
    - Automation Framework
    - TestNG
    - Cucumber
    - Software Testing Careers

    Keep it:
    - Short
    - Catchy
    - Professional

    Output should be just the topic, nothing else.
    """

    response = generate(prompt)

    print("DEBUG RESPONSE:", response)   # 👈 ADD THIS

    return response.strip() if response else "No topic generated"