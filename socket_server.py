import socket
import sys

class Server:
    """
    Represents a server for remote command execution.
    """
    
    def __init__(self, host_ip: str, host_port: int):
        self.host_ip = host_ip
        self.host_port = host_port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ACK = "ACK"

    def start(self):
        """
        Starts the server.
        """

        self.sock.bind((self.host_ip, self.host_port))
        print(f'[+] Listening on port {self.host_port}.....')
        self.sock.listen()

        self.remote_target, self.remote_ip = self.sock.accept()
        print(f'[+] Connection received from host at IP: {self.remote_ip[0]}, Port: {self.remote_ip[1]}')

    def send_message(self):
        """
        Sends a message to the client.
        """

        msg = input('Message to send >> ')
        if msg.lower() == 'exit':
            self.remote_target.send(msg.upper().encode())
            return False
        self.remote_target.send(msg.encode())
        return True

    def receive_message(self):
        """
        Receives a message from the client.
        """

        response = self.remote_target.recv(1024).decode()
        print(response)
        self.remote_target.send(self.ACK.encode())  # Send an ACK back to the client

        if not response or response.lower() == 'exit':  # Client disconnected or client terminated the session
            return False
        return True

    def run(self):
        """
        Main loop for sending and receiving messages.
        """

        self.start()

        try:
            while True:
                if not self.send_message():
                    break
                if not self.receive_message():
                    break
        except KeyboardInterrupt:
            print("User interrupt.")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            self.remote_target.close()


if __name__ == '__main__':
    HOST_IP = sys.argv[1]
    HOST_PORT = int(sys.argv[2])
    server = Server(HOST_IP, HOST_PORT)
    server.run()
