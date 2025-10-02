import socket

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    host = 'urgu.org'
    # host = 'example.com'
    port = 80
    s.connect((host, port))
    
    m_str = "GET / HTTP/1.1\r\nHost: {}\r\nConnection: close\r\n\r\n".format(host)
    msg = bytearray(m_str.encode())
    print(msg)

    s.sendall(msg)

    # answ = s.recv(4)
    # print(answ.decode('utf8'))
    
    
    
    
    
    
    
    
    while True:
        answ = s.recv(4096)
        if not answ:
            break
        print(answ.decode('utf8'))
    
    # answ = s.recv(1024)
    # print(answ.decode('utf8'))
    
    #'10.241.130.73'