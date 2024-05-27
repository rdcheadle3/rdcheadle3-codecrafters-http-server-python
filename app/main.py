from os import read, write
import socket
import sys


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
            if ": " in line:
                k, v = line.split(": ", 1)
                headers[k] = v
        return headers, lines

    def get_path(lines):
        request_line = lines[0].split(" ")
        path = request_line[1]
        return path

    def get_filename(path):
        filename = ""
        parts = path.split("/")
        if len(parts) > 2:
            filename = parts[2]
        return filename

    def get_abs_path():
        if len(sys.argv) >= 3:
            abs_path = sys.argv[2]
        else:
            abs_path = ""
        return abs_path

    def read_file(abs_path, filename):
        file_path = abs_path + filename
        try:
            with open(file_path, "r") as file:
                file_contents = file.read()
        except FileNotFoundError:
            file_contents = ""
        return file_contents

    def write_file(abs_path, filename, data):
        file_path = abs_path + filename
        try:
            with open(file_path, "w") as file:
                file_contents = file.write(data)
        except FileNotFoundError:
            file_contents = ""
        return file_contents

    def generate_response(path, headers, filename, file_contents):
        user_agent = headers.get("User-Agent", "Unknown")

        if request_str.startswith("POST"):
            response = f"HTTP/1.1 201 Created\r\n\r\n"

        elif path == f"/files/{filename}":
            if len(file_contents) > 0:
                response = f"HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length: {len(file_contents)}\r\n\r\n{file_contents}"
            else:
                response = "HTTP/1.1 404 Not Found\r\n\r\n"

        elif path == "/user-agent":
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
        print(f"Request str: {request_str}")

        headers, lines = get_headers(request_str)
        print(f"Headers: {headers}")

        path = get_path(lines)

        filename = get_filename(path)
        print(f"Filename: {filename}")

        abs_path = get_abs_path()
        print(f"Absolut Path: {abs_path}")

        if request_str.startswith("POST"):
            body_index = request_str.index("\r\n\r\n") + 4
            data = request_str[body_index:]
            file_path = write_file(abs_path, filename, data)
            print(f"Full File Path: {file_path}")
            
            file_contents = data
            print(f"File Contents: {file_contents}")
        else :
            file_contents = read_file(abs_path, filename)
            print(f"File Contents: {file_contents}")

        response = generate_response(path, headers, filename, file_contents)

        print(f"Response: {response}")

        send_response(client_socket, response)

        client_socket.close()


if __name__ == "__main__":
    main()
