import socket
import pickle

#Placas Cadastradas
placas = ["MDK3206", "JKF7175"]

#Servidor
server_ip = '127.0.0.1'
server_port = 12345

#Camera
camera_ip = '127.0.0.1'
camera_port = 12346

#Portao
portao_ip = '127.0.0.1'
portao_port = 12347

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
camera_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
portao_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    server_socket.bind((server_ip, server_port))
    server_socket.listen(1)
    print('Servidor pronto para receber conexôes')

    while True:
        client_socket, client_address = server_socket.accept()
        print("Conexão com: ", client_address)

        message = client_socket.recv(1024)
        message = pickle.loads(message)

        #Recebe do Sensor de Proximidade e manda sinal para a Câmera
        if message[0] == "Proximidade":
            camera_socket.connect((camera_ip, camera_port))

            message = []
            message.append("Proximidade")

            data = pickle.dumps(message)
            camera_socket.sendall(data)

            print("Sensor apontou proximidade")
            return_message = "Sinal OK"
            client_socket.send(return_message.encode())


        #Recebe da Câmera o sinal e a placa capturada e manda sinal para o Portão
        if message[0] == "Camera":
            print("Camera Capturou a placa: ", message[1])

            portao_socket.connect((portao_ip, portao_port))

            data = []
            data.append("Status")

            if message[1] in placas:
                print("Placa encontrada!")
                data.append(True)
            else:
                print("Placa não encontrada!")
                data.append(False)

            data = pickle.dumps(data)
            portao_socket.sendall(data)

        client_socket.close()
        break

finally:
    server_socket.close()
    camera_socket.close()
    portao_socket.close()