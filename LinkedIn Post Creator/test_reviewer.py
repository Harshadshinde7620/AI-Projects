from agents.topic_agent import get_topic
from agents.writer_agent import write_post
from agents.reviewer_agent import review_post

print("STARTING FULL PIPELINE")

topic = get_topic()
print("\nTOPIC:\n", topic)

draft = write_post(topic)
print("\nDRAFT:\n", draft)

final = review_post(draft)
print("\nFINAL POST:\n")
print(final)