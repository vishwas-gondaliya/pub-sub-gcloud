import os
from flask import Flask, request, jsonify
import psycopg2
from google.cloud import pubsub_v1
from concurrent.futures import TimeoutError
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_PORT = os.getenv('DB_PORT', '5432')

GCP_PROJECT_ID = os.getenv('GCP_PROJECT_ID')
PUBSUB_SUBSCRIPTION_NAME = os.getenv('PUBSUB_SUBSCRIPTION_NAME')

# Initialize Flask app
app = Flask(__name__)

# Set up Pub/Sub client and subscription
subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(GCP_PROJECT_ID, PUBSUB_SUBSCRIPTION_NAME)

def get_db_connection():
    """Connect to the PostgreSQL database."""
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT
    )

# Pub/Sub callback to process received messages
def callback(message):
    print(f"Received message: {message.data.decode('utf-8')}")
    
    # Store the message in the database
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO data_table (value) VALUES (%s)", (message.data.decode('utf-8'),))
        conn.commit()
        cursor.close()
        conn.close()
        message.ack()
        print("Message stored in database")
    except Exception as e:
        print(f"Failed to store message: {e}")

@app.route("/start_subscriber", methods=["POST"])
def start_subscriber():
    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
    print(f"Listening for messages on {subscription_path}...")

    # Keep the subscriber running in a separate thread
    try:
        streaming_pull_future.result()
    except TimeoutError:
        streaming_pull_future.cancel()

    return jsonify({"status": "Subscriber started"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

