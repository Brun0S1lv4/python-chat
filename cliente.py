import socket
import random
from threading import Thread
from datetime import datetime
from colorama import Fore, init, Back

#usando colorama e random para diferenciar visualmente os usuarios na rede  
init()

colors = [Fore.BLUE, Fore.CYAN, Fore.GREEN, Fore.LIGHTBLACK_EX, 
    Fore.LIGHTBLUE_EX, Fore.LIGHTCYAN_EX, Fore.LIGHTGREEN_EX, 
    Fore.LIGHTMAGENTA_EX, Fore.LIGHTRED_EX, Fore.LIGHTWHITE_EX, 
    Fore.LIGHTYELLOW_EX, Fore.MAGENTA, Fore.RED, Fore.WHITE, Fore.YELLOW
]

usuario_cor = random.choice(colors)

# Definindo Servidor e Porta
SERVER_HOST = "192.168.0.133"
SERVER_PORT = 5002 
#separando o nome do usuario com a mensagem
separador = "<SEP>"

#inicializando o socket
skt = socket.socket()
print(f"[*] Conectando em {SERVER_HOST}:{SERVER_PORT}...")
#conectado
skt.connect((SERVER_HOST, SERVER_PORT))
print("[+] Conectado.")

# pedindo nome do usuario
nome = input("Digite seu nome: ")


def listening_messages():
    
    while True:
        #armazenando o buffer do skt na variavel mensagem
        mensagem = skt.recv(1024).decode()
        #imprimindo para o usuario
        print("\n" + mensagem)

#Criando uma thread que "escuta" as mensagens e as imprime
thread = Thread(target=listening_messages)
thread.daemon = True
thread.start()

#Enviando as mensagens pro Servidor
while True:
    #armazenando o input do usuario em enviar
    enviar = input()
    if enviar.lower() == 'q':
        break
    # adicionando data, nome e cor do usuario
    data = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
    enviar = f"{usuario_cor}[{data}] {nome}{separador}{enviar}{Fore.RESET}"
    # finally, send the message
    skt.send(enviar.encode())

#Fechando o socket
skt.close()