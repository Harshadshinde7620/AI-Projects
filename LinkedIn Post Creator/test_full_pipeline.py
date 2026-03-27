from agents.topic_agent import get_topic
from agents.writer_agent import write_post
from agents.reviewer_agent import review_post
from agents.fact_checker_agent import fact_check

# 🔥 LinkedIn integration
from linkedin.auth import login
from linkedin.poster import post_content

print("🚀 FULL AI PIPELINE STARTED")

# Step 1 — Topic Generation
print("\n➡️ Generating topic...")
topic = get_topic()
print("\n🟢 TOPIC:\n", topic)

# Step 2 — Post Writing
print("\n➡️ Writing post...")
draft = write_post(topic)
print("\n📝 DRAFT:\n", draft)

# Step 3 — Review & Improve
print("\n➡️ Reviewing post...")
reviewed = review_post(draft)
print("\n🔍 REVIEWED:\n", reviewed)

# Step 4 — Fact Checking
print("\n➡️ Fact checking...")
final = fact_check(reviewed)

# Final Output
print("\n✅ FINAL POST:\n")
print(final)

# 🛑 Safety Check Before Posting
input("\n⚠️ Press Enter to continue to approval step...")

# Step 5 — Manual Approval + Posting
confirm = input("\n🚀 Do you want to post this on LinkedIn? (y/n): ")

if confirm.lower() == "y":
    print("\n📤 Posting to LinkedIn...")

    browser, page = login()
    post_content(page, final)

    browser.close()

    print("\n✅ Successfully posted on LinkedIn!")

else:
    print("\n❌ Post skipped.")

print("\n🎯 PIPELINE COMPLETE")