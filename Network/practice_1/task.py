import socket
import json
import zlib

class Response:
    def __init__(self):
        self.response_protocol: str = "HTTP/1.1 200 OK"

    @property
    def headers(self) -> [bytes]:
        return [b"Content-Type: gzip",
                b"Accept: application/json",
                b"Set-Cookie: name=Artyom; surname=Tsiganov"]

    @property
    def body(self) -> bytes:
        data: dict = {"from": "sage",
                      "content": "Суть всех негативных состояний ума — это автоматическое отторжение того, что есть. "
                                 "Мы не хотим быть там, где мы сейчас, и в нас возникает инстинктивное отталкивание "
                                 "текущей жизненной ситуации. Это отталкивание и переживается нами как страдание."}
        data_bytes =  bytes(json.dumps(data), "utf-8")
        return data_bytes

    def build_response(self) -> bytes:
        response = (
                self.response_protocol.encode() +
                b"\r\n" +
                b"\r\n".join(self.headers) +
                b"\r\n\r\n" +
                self.body
        )

        return response


class Server:
    def __init__(self, port=8080):
        self.host = "0.0.0.0"
        self.port = port

    def connect(self):
        with socket.socket() as s:
            s.bind((self.host, self.port))
            while True:
                s.listen(5)
                conn, addr = s.accept()
                print(f"New connection on {addr}")
                print(f"{conn.recv(65535).decode(errors='ignore')}")

                a = Response()
                conn.sendall(a.build_response())
                print("Отправлено")
                conn.shutdown(1)
                conn.close()


if __name__ == "__main__":
    server = Server()
    server.connect()
