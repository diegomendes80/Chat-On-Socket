import socket
import threading

HOST = '0.0.0.0'
PORT = 12345

def listen_mensage(conection):
    while True:
        try:
            data = conection.recv(1024)
            if not data:
                print("\nConnection closed by the client.");
                break
           
            mensage = data.decode('utf-8')
            print(f"\nCliente: {mensage}")
        except Exception as e:
            print(f"\nError receiving message: {e}")
            break
    
    print("\nClosing connection.")
    conection.close()
    
def send_mensage(conection):
    print("\nConnection is ready to send messages.")
    
    while True:
        try:
            print("\nEnter a message to send (or 'exit' to quit): ")
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
    
    
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    server.bind((HOST, PORT))
    server.listen()
    print("\n[Status] Server is listening on {}:{}".format(HOST, PORT))
    
    conection, address = server.accept()
    
    print(f"[Status] Client connected from {address}")
    
    receiver_thread = threading.Thread(target=listen_mensage, args=(conection,), daemon=True)
    sender_thread = threading.Thread(target=send_mensage, args=(conection,))
    
    receiver_thread.start()
    sender_thread.start()
    
if __name__ == "__main__":
    start_server()