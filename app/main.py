import socket


def main():
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    
    def accept_connection(server_socket):
        client_socket, client_address = server_socket.accept()
        return client_socket, client_address
    
    def read_request(client_socket):
        request = client_socket.recv(1024)
        request_str = request.decode("utf-8")
        return request_str

    def get_headers(request_str):
        headers = {}
        lines = request_str.split("\r\n")
        for line in lines[1:]:
            if ': ' in line:
                k, v = line.split(': ', 1)
                headers[k] = v
        return headers, lines
    
    def get_path(lines):
        request_line = lines[0].split(" ")
        path = request_line[1]
        return path

    def generate_response(path, headers):
        user_agent = headers.get('User-Agent', "Unknown")

        if path == "/user-agent":
           response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(user_agent)}\r\n\r\n{user_agent}"
        
        elif "/echo/" in path:
           parts = path.split("/echo/", 1)
           echo_str = parts[1] if len(parts) > 1 else "No data"
           response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(echo_str)}\r\n\r\n{echo_str}"
        
        elif path == "/":
           response = "HTTP/1.1 200 OK\r\n\r\n"
        
        else:
           response = "HTTP/1.1 404 Not Found\r\n\r\n"
        return response

    def send_response(client_socket, response):
        return client_socket.sendall(response.encode("utf-8"))

    while True:

       client_socket, client_address = accept_connection(server_socket) 
       print(f"Client address: {client_address}")

       request_str = read_request(client_socket)

       headers, lines = get_headers(request_str)

       path = get_path(lines) 

       response = generate_response(path, headers)

       print(f"Response: {response}")

       send_response(client_socket, response)

       client_socket.close()

if __name__ == "__main__":
    main()
