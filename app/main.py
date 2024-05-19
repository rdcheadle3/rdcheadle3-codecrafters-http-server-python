# Uncomment this to pass the first stage
import socket


def main():
    # accept connection
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"connection accepted {client_address}")
    
        # read request
        request = client_socket.recv(1024)
        print("request recieved")
        print(request)

        # get path
        request_line = request.splitlines()[0]
        print(f"Request line: {request_line}")
        parts = request_line.split()
        if len(parts) >= 2:
            path = parts[1]
        else:
            path = "/invalid"

        print(f"Extracted path: {path}")

        path = request_line.split()[1]
        print(path)
    
        if path == "/":
            response = "HTTP/1.1 200 OK\r\n\r\n"
        else:
            response = "HTTP/1.1 404 Not Found\r\n\r\n"

        print(f"Response: {response}")

        client_socket.sendall(response.encode("utf-8"))

        client_socket.close()

if __name__ == "__main__":
    main()
