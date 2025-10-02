import socket

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    host = 'time.nist.gov'
    port = 13

    s.connect((host, port))
    s.sendall(b'hi')

    print((s.recv(2)))