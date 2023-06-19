import socket
import os

def handle_client(socket, diretorio):
    request = socket.recv(1024).decode()
    if request.startswith("GET"):
        caminho = request.split()[1]
        if caminho == "/": # lista arquivos e caminhos possiveis
            arquivos = os.listdir(diretorio)
            resp = "HTTP/1.1 200 OK\r\n\r\n"
            resp += "<html><body>"
            resp += "<h1>SERVIDOR</h1></br>"
            for arq in arquivos:
                link = f"<a href='{arq}'>{arq}</a><br>"
                resp += link
            resp += "</body></html>"
            socket.sendall(resp.encode())
        elif caminho == "/HEADER": # header
            resp = "HTTP/1.1 200 OK\r\n\r\n"
            resp += f"HTTP Request Header:\n\n{request}\n"
            socket.sendall(resp.encode())
        else: # retorna o arquivo pedido na requisição
            caminho = caminho[1:]
            caminho = os.path.join(diretorio, caminho)
            dir = os.path.abspath(caminho) 
            if os.path.exists(dir):
                with open(dir, 'rb') as arq:
                    resp = "HTTP/1.1 200 OK\r\n\r\n"
                    socket.sendall(resp.encode())
                    while True:
                        data = arq.read(1024)
                        if not data:
                            break
                        socket.sendall(data)
    socket.close()

host = "localhost"
porta = 8000 
diretorio = "arquivos"  

S_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
S_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
S_socket.bind((host, porta))
S_socket.listen(1)
print(f"Server running on http://{host}:{porta}/")
while True:
    socket, addr = S_socket.accept()
    handle_client(socket, diretorio)


