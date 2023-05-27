import socket

def init_client(host_ip: str, host_port: str):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print(f'[+] Connecting to {HOST_IP}.')
    sock.connect((HOST_IP, HOST_PORT))
    print(f'[+] Connected to {HOST_IP}.')

    try:
        while True:
            msg = sock.recv(1024).decode()
            if not msg: # Client disconnected
                break
            if msg.lower() == 'exit':
                print(f'[-] The server has terminated the session.')
                break
            print(msg)

            response = input('Message to reply >> ')
            if response.lower() == 'exit':
                sock.send(response.encode())
                break
            sock.send(response.encode())
            print('Awaiting reponse.....')
    except KeyboardInterrupt as e:
        print("User interrupt.")
    except Exception:
        print(f"An error occurred: {e}")
    finally:
        sock.close()
            





HOST_IP = '127.0.0.1'
HOST_PORT = 2222
init_client(HOST_IP, HOST_PORT)

