from socket import *
from pyos import *
from pyos.systemcall import *


def Accept(sock):
    yield ReadWait(sock)
    yield sock.accept()


def Send(sock,buffer):
    while buffer:
        yield WriteWait(sock)
        len = sock.send(buffer)
        buffer = buffer[len:]


def Recv(sock,maxbytes):
    yield ReadWait(sock)
    yield sock.recv(maxbytes)


def handle_client(client,addr):
    print("Connection from", addr)
    while True:
        data = yield Recv(client,65536)
        if not data:
            break
        yield Send(client,data)
    print("Client closed")
    client.close()


def server(port):
    print("Server starting")
    sock = socket(AF_INET,SOCK_STREAM)
    sock.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    sock.bind(("",port))
    sock.listen(5)
    while True:
        client,addr = yield Accept(sock)
        yield NewTask(handle_client(client,addr))


sched = Scheduler()
sched.new(server(45000))
sched.mainloop()