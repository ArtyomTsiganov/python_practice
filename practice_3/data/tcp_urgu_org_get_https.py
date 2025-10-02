import socket
import ssl

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    host = 'urgu.org'
    port = 443
    s.connect((host, port))
    s = ssl.wrap_socket(s, keyfile=None, certfile=None, server_side=False, cert_reqs=ssl.CERT_NONE, ssl_version=ssl.PROTOCOL_SSLv23)
    
    m_str = "GET / HTTP/1.1\r\nHost: {}\r\nConnection: close\r\n\r\n".format(host)
    msg = bytearray(m_str.encode())
    print(msg)

    s.sendall(msg)


    while True:
        answ = s.recv(4096)
        if not answ:
            break

        print(answ)
    