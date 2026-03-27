from agents.topic_agent import get_topic
from agents.writer_agent import write_post

topic = get_topic()
print("\nTOPIC:\n", topic)

post = write_post(topic)
print("\nGENERATED POST:\n")
print(post)