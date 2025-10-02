import asyncio
import collections
import json
import re
import time
import zlib
import socket
from asyncio import StreamReader, StreamWriter


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
        data_bytes = bytes(json.dumps(data), "utf-8")
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


class Request:
    def __init__(self):
        self.request_protocol: str = "fetch"

    @property
    def headers(self) -> [bytes]:
        return [b"Accept: text/text", ]

    @property
    def body(self) -> bytes:
        return b""

    def build_request(self, addr=b"") -> bytes:
        response = (
                self.request_protocol.encode() +
                addr +
                b"\r\n"
        )
        return response


class Client:
    def __init__(self, port=13000):
        self.host = "10.249.130.26"
        self.port = port

    async def connect(self):
        reader, writer = await asyncio.open_connection(self.host, self.port)
        addresses = collections.deque()
        addresses.append("")
        while len(addresses) > 0:
            addr = addresses.popleft()
            writer.write(f"fetch {addr}\r\n".encode())
            await writer.drain()
            ln = await self.get_len(reader)
            data = await self.recive_data(reader, ln)
            addrs = self.find_addr(data)
            for ad in addrs:
                addresses.append(ad)
            print(*self.find_flags(data))

    async def get_len(self, reader: StreamReader):
        num = b""
        s = await reader.readexactly(1)
        while b"0" <= s <= b"9":
            num += s
            s = await reader.readexactly(1)
        return int(num)

    async def recive_data(self, reader:StreamReader, ln : int):
        mess = await reader.readexactly(ln)
        return mess.decode(errors="ignore")

    def find_addr(self, data: str):
        c = re.compile("\"([a-zA-Z]{8})\"")
        return re.findall(c, data)

    def find_flags(self, data: str):
        c = re.compile("PYTHON_[\d\w]{25}")
        return re.findall(c, data)

if __name__ == "__main__":
    client = Client()
    asyncio.run(client.connect())
