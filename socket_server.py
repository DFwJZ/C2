import socket


def init_server(host_ip, host_port):
    # Create a socket object
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    sock.bind((HOST_IP, HOST_PORT))
    print('[+] Listening on port 2222.....')
    sock.listen()

    remote_target, remote_ip = sock.accept()
    print(f'[+] Connection received from host at IP: {remote_ip[0]}, Port: {remote_ip[1]}')

    try:
        while True:
            msg = input('Message to send >> ')
            if msg.lower() == 'exit':
                remote_target.send(msg.upper().encode())
                break
            remote_target.send(msg.encode())

            response = remote_target.recv(1024).decode()
            if not response: # Client disconnected
                break
            if response.lower() == 'exit':
                print('[-] The client has terminated the session.')
                break
            print(response)

    except KeyboardInterrupt:
        print("User interrupt.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        remote_target.close()


HOST_IP = '127.0.0.1'
HOST_PORT = 2222
init_server(HOST_IP, HOST_PORT)