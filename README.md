# Simple Reverse Shell in Python

This project contains two Python scripts that work together to create a simple reverse shell. The two scripts are `socket_client.py` and `socket_server.py`. The server sends commands to the client, which executes them and sends back any output.

    "Disclaimer: Please note that using a reverse shell without explicit permission is illegal and unethical. The following is only for educational purposes or for authorized penetration testing. Unauthorized access to a computer system is a crime in many jurisdictions."

## Client 

The `socket_client.py` script connects back to a specified server and listens for commands. Once it receives a command, it executes the command and sends the output back to the server.

Here's how the client script works:

```Python
class Client:

    def __init__(self, host_ip: str, host_port: str):
        # Constructor for initializing the client
        ...

    def connect_to_server(self):
        # Connect to the server
        ...

    def handle_command(self, command: str):
        # Handle the received command from the server
        ...

    def run(self):
        # Main function to start the client
        ...
```
For more details, please refer to `socket_client.py`.


## Server

The `socket_server.py` script listens for connections and, once a client is connected, sends commands to the client.

Here's how the server script works:
``` Python
class Server:

    def __init__(self, host_ip: str, host_port: str):
        # Constructor for initializing the server
        ...

    def start_server(self):
        # Start the server and listen for connections
        ...

    def handle_client(self, client_sock: socket):
        # Handle the connected client
        ...

    def run(self):
        # Main function to start the server
        ...
```
For more details, please refer to `socket_server.py`.


## How to Run

To run these scripts, you will need Python installed on your machine. Python3 is recommended.

1. Run the `socket_server.py` script on your machine. You will need to specify the IP and port to listen on:


```bash
python socket_server.py 127.0.0.1 9001
```
2. Run the `socket_client.py` script on the target machine. You will need to specify the IP and port of the server:


```bash
python socket_client.py 127.0.0.1 9001
```
Once the client and server are both running, you will be able to send commands from the server to the client.

## Conclusions

This project is a very basic implementation of a reverse shell in Python. It is intended for educational purposes and should not be used for unauthorized access to systems.