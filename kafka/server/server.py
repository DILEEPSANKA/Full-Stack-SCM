import json, random, socket, time
from datetime import datetime  

try:
    server_socket = socket.socket()
    print("Server socket initialized")
    server_socket.bind(('', 12345))
    server_socket.listen(3)
    print("Awaiting incoming connections...")
    client_socket, client_address = server_socket.accept()
    print(f"Connected to client at {client_address}")

    routes_list = ['New York, USA', 'Pune, India', 'Bengaluru, India', 'London, UK', 'Hyderabad, India', 'Louisville, USA']

    while True:
        try:
            device_data_list = []
            for _ in range(2):  
                source_route = random.choice(routes_list)
                destination_route = random.choice(routes_list)

                while source_route == destination_route:
                    destination_route = random.choice(routes_list)

                device_data = {
                    "Battery_Level": round(random.uniform(2.00, 5.00), 2),
                    "Device_Id": random.choice([1819124651, 1819124652, 1819124653]),  
                    "First_Sensor_temperature": round(random.uniform(10.0, 40.0), 1),
                    "Route_From": source_route,
                    "Route_To": destination_route,
                }
                device_data_list.append(device_data)

            encoded_data = (json.dumps(device_data_list) + "\n").encode('utf-8')
            client_socket.send(encoded_data)
            print(f"Transmitted Data: {encoded_data.decode('utf-8')}")
            time.sleep(10)

        except Exception as error:
            print(f"Error encountered: {error}")
            break

finally:
    client_socket.close()
