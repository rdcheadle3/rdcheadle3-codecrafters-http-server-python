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
        request_str = request.decode("utf-8")
        print("request recieved")
        print(request_str)

        # get path
        request_line = request_str.splitlines()[0]
        print(f"Request line: {request_line}")

        path = request_line.split()[1]
        print(f"Extracted path: {path}")

        str = path.rsplit("/", 1)[-1]
        print(f"Path strings: {str}")

        if path == f"/echo/{str}":
            response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(str)}\r\n\r\n{str}"
        elif path == "/":
            response = "HTTP/1.1 200 OK\r\n\r\n"
        else:
            response = "HTTP/1.1 404 Not Found\r\n\r\n"

        print(f"Response: {response}")

        client_socket.sendall(response.encode("utf-8"))

        client_socket.close()

if __name__ == "__main__":
    main()
