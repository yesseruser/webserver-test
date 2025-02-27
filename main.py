import socket
ws = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ws.bind(('', 80))
ws.listen()

while True:
    conn, addr = ws.accept()
    print(f"connection from: {addr}")
    with open("index.html", "rb") as file:
        content = file.read()
        conn.send("HTTP/3 200 OK\r\n".encode())
        conn.send(f"Content-Lenght: {len(content.decode())}\r\n\r\n".encode())
        conn.send(content)
    conn.shutdown(socket.SHUT_RDWR)
    conn.close()


