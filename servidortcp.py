import socket
import os

def serve_file(socket, caminho):
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
    else:
        resp = "HTTP/1.1 404 Not Found\r\n\r\n"
        socket.sendall(resp.encode())

def handle_client(socket, diretorio):
    request = socket.recv(1024).decode()
    if request.startswith("GET"):
        caminho = request.split()[1]
        if caminho == "/":
            arquivos = os.listdir(diretorio)
            resp = "HTTP/1.1 200 OK\r\n\r\n"
            resp += "<html><body>"
            resp += "<h1>SERVIDOR</h1></br>"
            for arq in arquivos:
                link = f"<a href='{arq}'>{arq}</a><br>"
                resp += link
            resp += "</body></html>"
            socket.sendall(resp.encode())
        elif caminho == "/HEADER":
            serve_header(socket, request)
        else:
            caminho = caminho[1:]
            serve_file(socket, os.path.join(diretorio, caminho))
    socket.close()

def serve_header(socket, request):
    resp = "HTTP/1.1 200 OK\r\n\r\n"
    resp += f"HTTP Request Header:\n\n{request}\n"
    socket.sendall(resp.encode())




host = "172.30.201.90" # hostname -I 
porta = 8000 
diretorio = "arquivos"  
users = 50

S_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
S_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
S_socket.bind((host, porta))
S_socket.listen(users)
print(f"Server running on http://{host}:{porta}/")
while True:
    socket, addr = S_socket.accept()
    handle_client(socket, diretorio)


