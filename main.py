import socket
import sqlite3

ws = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ws.bind(('', 80))
ws.listen()

with sqlite3.connect("ips.db") as db:
    dbcur = db.cursor()
    dbcur.execute("CREATE TABLE IF NOT EXISTS ips (ip TEXT)")

    while True:
        conn, addr = ws.accept()
        request = conn.recv(1024).decode()
        print(f"connection from: {addr}")
        location = "/"
        lines = request.split("\r\n")
        if len(lines) != 0:
            header_args = lines[0].split(" ")
            if len(header_args) == 3:
                location = header_args[1]
        if location == "/ips":
            content = ""
            ips = dbcur.execute("SELECT ip FROM ips").fetchall()
            ip_dict = {}
            for ip in ips:
                if ip not in ip_dict:
                    ip_dict[ip] = 1
                else:
                    ip_dict[ip] += 1

            for ip, count in ip_dict.items():
                content += f"{ip[0]}: {count}\r\n"
            response = "HTTP/3 200 OK\r\n"
            response += f"Content-Lenght: {len(content)}\r\n\r\n"
            response += content
            conn.send(response.encode())
        else:
            with open("index.html", "rt") as file:
                content = file.read()
                response = "HTTP/3 200 OK\r\n"
                response += f"Content-Lenght: {str(len(content))}\r\n\r\n"
                response += content
                conn.send(response.encode())
        conn.shutdown(socket.SHUT_RDWR)
        conn.close()
        dbcur.execute(f"INSERT INTO ips (ip) VALUES (?)", (str(addr[0]),))
        db.commit()


