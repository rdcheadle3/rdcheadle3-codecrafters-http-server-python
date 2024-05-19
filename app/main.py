# Uncomment this to pass the first stage
import socket


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage
    #
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    server_socket.accept() # wait for client
    client_socket, client_address = server_socket.accept()
    print(f"Accepted connection from {client_address}")

    request = client_socket.recv(1024)
    print("request recieved...")
    print(request.decode("utf-8"))

if __name__ == "__main__":
    main()
