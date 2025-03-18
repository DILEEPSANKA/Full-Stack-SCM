from confluent_kafka import Consumer
from dotenv import load_dotenv
import json, os, time
from pymongo import MongoClient
from pymongo.errors import PyMongoError

load_dotenv()

mongo_uri = os.getenv("MONGODB_URI")
db_name = os.getenv("MONGODB_DATABASE")

if not mongo_uri or not db_name:
    raise ValueError("MongoDB URI or database name is not set in .env")

try:
    mongo_client = MongoClient(mongo_uri)
    db_instance = mongo_client[db_name]
    device_data_collection = db_instance["Device_Data_Stream"]
    print("Connected to MongoDB successfully!")
except Exception as mongo_error:
    print(f"Error connecting to MongoDB: {mongo_error}")
    exit(1)

kafka_broker_list = os.getenv("BOOTSTRAP_SERVERS", "kafka:9092")

kafka_consumer_config = {
    'bootstrap.servers': kafka_broker_list,
    'group.id': 'consumer-group-1',
    'auto.offset.reset': 'earliest'
}

MAX_RETRIES = 5
retry_count = 0
while retry_count < MAX_RETRIES:
    try:
        kafka_consumer = Consumer(kafka_consumer_config)
        kafka_consumer.subscribe(['device_data_stream'])
        print("Kafka Consumer started...")
        break
    except Exception as e:
        print(f"Kafka connection attempt {retry_count + 1}/{MAX_RETRIES} failed: {e}")
        retry_count += 1
        time.sleep(5)
else:
    print("Unable to connect to Kafka. Exiting.")
    exit(1)

try:
    while True:
        event_message = kafka_consumer.poll(1.0)
        if event_message is None:
            continue
        if event_message.error():
            print(f"Consumer error: {event_message.error()}")
            continue

        try:
            received_payload = event_message.value().decode('utf-8')
            print(f"Raw data received: {received_payload}")
            parsed_data = json.loads(received_payload)

            if isinstance(parsed_data, str):
                parsed_data = json.loads(parsed_data)

            print(f"Processed data: {parsed_data}")

            if isinstance(parsed_data, list) and parsed_data:
                device_data_collection.insert_many(parsed_data)
                print(f"Inserted {len(parsed_data)} records into MongoDB")
            elif isinstance(parsed_data, dict):
                device_data_collection.insert_one(parsed_data)
                print(f"Inserted single record into MongoDB: {parsed_data}")
            else:
                print(f"Unsupported data format: {parsed_data}")

        except json.JSONDecodeError as json_error:
            print(f"JSON Decode Error: {json_error}")
        except PyMongoError as mongo_error:
            print(f"MongoDB Insertion Error: {mongo_error}")
        except Exception as process_error:
            print(f"Unexpected Error handling message: {str(process_error)}")

except KeyboardInterrupt:
    print("Consumer process interrupted by user.")

finally:
    kafka_consumer.close()
    print("Kafka Consumer closed.")