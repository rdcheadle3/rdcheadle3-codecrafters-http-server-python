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

        # get headers
        headers = {}
        lines = request_str.split("\r\n")
        for line in lines[1:]:
            if ': ' in line:
                key, value = line.split(': ', 1)
                headers[key] = value

        #get user agent header
        user_agent = headers.get('User-Agent', "Uknown")
        print(f"User-Agent: {user_agent}")

        # get path
        request_line = lines[0].split(" ")
        path = request_line[1]
        print(f"Path: {path}")

        if path == "/user-agent":
            response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(user_agent)}\r\n\r\n{user_agent}"
        elif "/echo/" in path:
            parts = path.split("/echo/", 1)
            print(f"Parts: {parts}")
            echo_str = parts[1] if len(parts) > 1 else "No data"
            response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(echo_str)}\r\n\r\n{echo_str}"
        elif path == "/":
            response = "HTTP/1.1 200 OK\r\n\r\n"
        else:
            response = "HTTP/1.1 404 Not Found\r\n\r\n"

        print(f"Response: {response}")

        client_socket.sendall(response.encode("utf-8"))

        client_socket.close()

if __name__ == "__main__":
    main()
