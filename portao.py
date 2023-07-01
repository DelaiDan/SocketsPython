import socket
import pickle
import time

placas = []

server_ip = '127.0.0.1'
server_port = 12345

portao_ip = '127.0.0.1'
portao_port = 12347

portao_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    portao_socket.bind((portao_ip, portao_port))
    portao_socket.listen(1)
    print('Portão pronto para receber conexôes')

    while True:
        client_socket, client_address = portao_socket.accept()

        status = client_socket.recv(1024)
        status = pickle.loads(status)
        
        if status[0] == "Status":
            server_socket.connect((server_ip, server_port))

            if status[1] == True:
                print("Placa identificada!")
                print("Portão Aberto")
            else:
                print("Placa NÃO identificada!")
                print("Portão Fechado")

            time.sleep(5)
            print("Portão Fechado")

except ConnectionRefusedError:
    print("Não foi possível conectar ao servidor.")

finally:
    portao_socket.close()
    server_socket.close()