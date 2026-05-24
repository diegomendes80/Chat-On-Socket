import socket #conexão entre processos
import threading #multiplas tarefas simultaneamente

HOST = '0.0.0.0' #aceita conexões de qualquer endereço
PORT = 12345 #porta escolhida 


#Função que faz o server ficar ouvindo continuamente mensagens do cleinte
#Recv(1024) recebe os bytes que vem do client, tendo buffer maximo de 1024 bytes 1Kb por leitura, e armazena em data. Se data for vazio, significa que o cliente fechou a conexão, e o loop é interrompido. Caso contrário, a mensagem é decodificada de bytes para string usando UTF-8 e exibida no console. Se ocorrer algum erro durante o recebimento da mensagem, ele é capturado e exibido, e o loop é interrompido. No final, a conexão é fechada.
def listen_mensage(conection):
    while True:
        try:
            data = conection.recv(1024)
            if not data:
                print("\nConnection closed by the client.");
                break
           
            mensage = data.decode('utf-8') #conversão de bytes -> string
            print(f"\nCliente: {mensage}") #imprime a string recebida do cliente
            print("You: ", end='', flush=True) #imprime "You: " sem quebra de linha e força a exibição imediata
        except Exception as e:
            print(f"\nError receiving message: {e}")
            break
    
    print("\nClosing connection.")
    conection.close()
    
    
    
#Função que permite ao servidor enviar mensagens para o cliente. O servidor solicita ao usuário que digite uma mensagem para enviar ao cliente. Se a mensagem for vazia, o loop continua solicitando uma nova mensagem. Se a mensagem for "exit", o loop é interrompido e a conexão é fechada. Caso contrário, a mensagem é codificada em bytes usando UTF-8 e enviada para o cliente. Se ocorrer algum erro durante o envio da mensagem, ele é capturado e exibido, e o loop é interrompido. No final, a conexão é fechada.    
def send_mensage(conection):
    print("\nConnection is ready to send messages.")
    
    while True:
        try:
       
            mensage = input("\nYou: ")
            
            if not mensage.strip():
                continue
            
            if mensage.lower() == 'exit':
                break
            
            conection.send(mensage.encode('utf-8'))
            
        except Exception as e:
            print(f"\nError sending message: {e}")
            break

    print("\nClosing connection.")
    conection.close()
    

#Função principal que inicia o servidor. O servidor é configurado para aceitar conexões de clientes e, quando um cliente se conecta, ele cria duas threads: uma para ouvir mensagens do cliente e outra para enviar mensagens ao cliente. O servidor continua a aceitar conexões e a criar threads para cada cliente conectado. O servidor é configurado para ouvir na porta especificada e aceitar conexões de qualquer endereço IP.
def start_server():
    #AF_INET indica que a familia de endereções é IPv4, e SOCK_STREAM indica que o tipo de socket é TCP
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #serve pra liberar a porta assim que fechar a conexão
    
    server.bind((HOST, PORT)) #configura o pacote socket: endereço ip + porta - o servidor vai escutar nesse ip e porta
    server.listen() #coloca em modo escuta
    print("\n[Status] Server is listening on {}:{}".format(HOST, PORT))
    
    #segura a execução do programa até um cliente se conectar. Quando um cliente se conectar cria o socket de fato e da start as threads de envio e recebimento
    conection, address = server.accept()
    
    print(f"[Status] Client connected from {address}")
    
    #thread de recebimento e envio. Elas vão estar em concorrência, ou seja, ao mesmo tempo
    receiver_thread = threading.Thread(target=listen_mensage, args=(conection,), daemon=True)
    sender_thread = threading.Thread(target=send_mensage, args=(conection,))
    
    #incia as duas
    receiver_thread.start()
    sender_thread.start()
    
if __name__ == "__main__":
    start_server()