import time

def post_content(page, content):
    page.goto("https://www.linkedin.com/feed/")

    time.sleep(5)

    # Click start post
    page.click("text=Start a post")

    time.sleep(3)

    # Enter content
    page.fill("div[role='textbox']", content)

    time.sleep(2)

    # Click post button
    page.click("button:has-text('Post')")

    print("✅ Post published successfully!")

    time.sleep(5)