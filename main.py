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
        print(f"connection from: {addr}")
        with open("index.html", "rb") as file:
            content = file.read()
            conn.send("HTTP/3 200 OK\r\n".encode())
            conn.send(f"Content-Lenght: {len(content.decode())}\r\n\r\n".encode())
            conn.send(content)
        conn.shutdown(socket.SHUT_RDWR)
        conn.close()
        dbcur.execute(f"INSERT INTO ips (ip) VALUES (?)", (str(addr[0]),))
        db.commit()


