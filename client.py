import socket
import threading

SERVER_IP = '127.0.0.1' #mudar o ip pra maquina host real
PORT = 12345

def listen_mensage(conection):
    while True:
        try:
            data = conection.recv(1024)
            if not data:
                print("\nConnection closed by the server.");
                break
            
            mensage = data.decode('utf-8')
            print(f"\nServer: {mensage}")
            print("You: ", end='', flush=True)
        except Exception as e:
            print(f"\nError receiving message: {e}")
            break
    
    print("\nClosing connection.")
    conection.close()
    
    
def send_mensage(conection):
    print("\nConnection is ready to send messages.")
    
    while True:
        try:
            mensage = input("You: ")
            
            if not mensage.strip():
                continue
            
            conection.send(mensage.encode('utf-8'))
            
            if mensage.lower() == 'exit':
                break
            
            
        except Exception as e:
            print(f"\nError sending message: {e}")
            break

    print("\nClosing connection.")
    conection.close()
    
def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        print("[Status] Connecting to server at {}:{}".format(SERVER_IP, PORT))
        client.connect((SERVER_IP, PORT))
        print("[Status] Connected to server.")
        
        thread_receiver = threading.Thread(target=listen_mensage, args=(client,),daemon=True)
        sender_thread = threading.Thread(target=send_mensage, args=(client,))
        
        thread_receiver.start()
        sender_thread.start()
    
    except Exception as e:
        print("\n[Error] Failed to connect to server.")
        
if __name__ == "__main__":
    start_client()