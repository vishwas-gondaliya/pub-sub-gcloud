import random
import time
from google.cloud import pubsub_v1
import os
import json

# Set up Google Pub/Sub client
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "my-project-kubernates-436201-59e5ae40cf92.json"  # Update path
publisher = pubsub_v1.PublisherClient()
topic_path = 'projects/my-project-kubernates-436201/topics/random-message-topic'

def generate_random_message():
    messages = ["Hello World", "Random Message", "This is a Test", "PubSub Rocks"]
    return random.choice(messages)

def publish_message():
    message = generate_random_message()
    data = message.encode('utf-8')
    future = publisher.publish(topic_path, data)
    print(f"Published message: {message}")

if __name__ == "__main__":
    while True:
        publish_message()
        time.sleep(5)  # Sleep for 5 seconds between messages

