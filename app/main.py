# Uncomment this to pass the first stage
import socket


def main():

    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    server_socket.accept() # wait for client
    client_socket, client_address = server_socket.accept()

    request = client_socket.recv(1024)

    response = "HTTP/1.1 200 OK\r\n\r\n"
    client_socket.sendall(response.encode("utf-8"))

    client_socket.close()
    server_socket.close()

if __name__ == "__main__":
    main()
