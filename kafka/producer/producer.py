from confluent_kafka import Producer
import json, os, socket, time
from dotenv import load_dotenv

load_dotenv()

kafka_brokers = os.getenv("BOOTSTRAP_SERVERS", "localhost:9092")
server_address = os.getenv("HOST", "localhost")
server_port = int(os.getenv("PORT", 12345))

if server_address == "host.docker.internal" and os.name != "nt":
    server_address = "172.17.0.1"

kafka_producer = Producer({"bootstrap.servers": kafka_brokers})

def publish_message(topic, data):
    try:
        kafka_producer.produce(topic, value=json.dumps(data))
        kafka_producer.flush()
        print(f"Message published to Kafka topic {topic}: {data}")
    except Exception as e:
        print(f"Error publishing message to Kafka: {e}")

MAX_RETRIES = 5
retry_count = 0
client_socket = None

while retry_count < MAX_RETRIES:
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((server_address, server_port))
        client_socket.settimeout(10)
        print(f"Connected to server at {server_address}:{server_port}")
        break
    except socket.error as e:
        print(f"Connection attempt {retry_count + 1}/{MAX_RETRIES} failed: {e}")
        retry_count += 1
        time.sleep(5)  
else:
    print("Unable to connect to server. Exiting.")
    exit(1)

try:
    while True:
        try:
            received_data = client_socket.recv(1024).decode('utf-8')
            if received_data:
                print(f"Received data from server: {received_data}")
                publish_message("device_data_stream", received_data)
            else:
                print("Received empty data from server")

        except socket.timeout:
            print("No data received in the last 10 seconds.")
        except ConnectionResetError:
            print("Connection reset by server. Exiting.")
            break
        except Exception as e:
            print(f"Unexpected error: {e}")
            break
except KeyboardInterrupt:
    print("Stopping producer...")
finally:
    if client_socket:
        client_socket.close()
    print("Connection closed.")