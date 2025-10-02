import socket

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    message = b''

    address = ('www.djxmmx.net', 17)
    
    s.sendto(message, address)

    print(s.recvfrom(2048))

    # data, a = s.recvfrom(1024)

    # print(data.decode())
