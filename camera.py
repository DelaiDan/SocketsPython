import socket
import pickle
import random

placas = ["MDK3206", "APK6155", "LVZ7440", "LWM5433", "MZS5607", "LWO8576", "JKF7175"]

server_ip = '127.0.0.1'
server_port = 12345

camera_ip = '127.0.0.1'
camera_port = 12346

camera_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    camera_socket.bind((camera_ip, camera_port))
    camera_socket.listen(1)
    print('Camera pronta para receber conexôes')

    while True:
        client_socket, client_address = camera_socket.accept()

        message = client_socket.recv(1024)
        message = pickle.loads(message)
        
        if message[0] == "Proximidade":
            print("Camera Acionada")

            server_socket.connect((server_ip, server_port))

            message = []
            message.append("Camera")
            message.append(random.choice(placas))

            data = pickle.dumps(message)
            server_socket.sendall(data)

except ConnectionRefusedError:
    print("Não foi possível conectar ao servidor.")

finally:
    camera_socket.close()
    server_socket.close()