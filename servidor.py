import socket
from threading import Thread

SERVER_HOST = '192.168.0.133'
SERVER_PORT = 5002
separador = '<SEP>'

sockets_usuarios = set()

skt = socket.socket()
skt.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
skt.bind((SERVER_HOST, SERVER_PORT))
skt.listen(5)
print(f"[*] Escutando em {SERVER_HOST}:{SERVER_PORT}")

def listening_users(us):
    while True:
        try:
            mensagem = us.recv(1024).decode()
        except Exception as e:
            print(f"[!] Erro: {e}")
            #ativando a exceção, o usuario atual é removido do set
            sockets_usuarios.remove(us)
        else:
            mensagem = mensagem.replace(separador, ": ")

        for socket_usuario in sockets_usuarios:
            socket_usuario.send(mensagem.encode())

while True:
    socket_usuario, endereco_usuario = skt.accept()
    print(f"[+] {endereco_usuario} conectado.")

    sockets_usuarios.add(socket_usuario)

    thread = Thread(target=listening_users, args=(socket_usuario,))
    thread.daemon = True
    thread.start()

for su in socket_usuarios:
    su.close()

skt.close()