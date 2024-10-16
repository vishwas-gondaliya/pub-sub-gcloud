# Google Cloud Pub/Sub Messaging System with Flask and PostgreSQL

This project demonstrates how to implement a message processing system using Google Cloud Pub/Sub, Flask, and PostgreSQL. A Python script generates random messages and publishes them to a Pub/Sub topic. A Flask application subscribes to the Pub/Sub topic, processes the messages, and stores them in a PostgreSQL database.

## Prerequisites

Before you start, make sure you have the following:

- Google Cloud Platform (GCP) project
- PostgreSQL database (either local or Cloud SQL)
- Python 3.9+
- Google Cloud SDK installed (`gcloud` command-line tool)
- Google Pub/Sub service enabled in your GCP project
- Service account with appropriate permissions.


## Steps to Set Up

###1 Set Up Google Cloud Pub/Sub

1. **Create Pub/Sub Topic:**
    
    gcloud pubsub topics create random-message-topic
    

2. **Create Subscription:**
    
    gcloud pubsub subscriptions create backend-subscription --topic=random-message-topic
   
###2. Set Up the PostgreSQL Database Table

Once connected to the database, create the necessary table for storing the data:


CREATE TABLE data_table (
    id SERIAL PRIMARY KEY,
    value TEXT NOT NULL
);

###3. Create a Service Account and Download Credentials

- In the GCP Console, create a service account and download the JSON key file.
- Add the following roles to the service account:
- Pub/Sub Publisher
- Pub/Sub Subscriber
- Cloud SQL Client

###4. Environment Variables
Create a .env file to configure your environment variables:
DB_HOST=PUBLIC_IP_OF_YOUR_CLOUD_SQL_INSTANCE # IP of DB   
DB_NAME=DBname               # Your Cloud SQL database name  
DB_USER=userDB               # Your Cloud SQL user  
DB_PASSWORD=your-password      # Your Cloud SQL user password  
DB_PORT=5432                  # Default PostgreSQL port  

GCP_PROJECT_ID=project-name  
PUBSUB_SUBSCRIPTION_NAME=backend-subscription  
GOOGLE_APPLICATION_CREDENTIALS=/app/.json  

###5 Install Dependencies
Install the necessary Python dependencies listed in the requirements.txt file:
pip install -r requirements.txt

###6 Running the Flask Application

- Start the Flask app to listen for Pub/Sub messages and process them:

python app.py

- Start the subscriber to process messages:

curl -X POST http://localhost:5000/start_subscriber

- Running the Message Generator

python app2.py

###7 Check if the messages are successfully processed and stored in your Cloud SQL PostgreSQL database. You can query the database to see if the data_table contains the inserted values:

SELECT * FROM data_table;



