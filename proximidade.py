import socket
import pickle

server_ip = '127.0.0.1'
server_port = 12345

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client_socket.connect((server_ip, server_port))

    while True:
        message = []
        message.append("Proximidade")
        message.append(input("Digite uma string: "))

        data = pickle.dumps(message)

        client_socket.sendall(data)

        modified_message = client_socket.recv(1024).decode()
        print("String modificada:", modified_message)

except ConnectionRefusedError:
    print("Não foi possível conectar ao servidor.")

finally:
    client_socket.close()