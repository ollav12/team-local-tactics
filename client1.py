from http import client
import socket

clientsocket = socket.socket()

host = "192.168.56.1"
port = 1233

print("waiting for connection")
try:
    clientsocket.connect((host, port))
except socket.error as e:
    print(str(e))


Response = clientsocket.recv(1024)
print(Response.decode("utf-8"))
while True:
    Input = input("Say something ")
    clientsocket.send(str.encode(Input))
    Response = clientsocket.recv(1024)
    print(Response.decode("utf-8"))

clientsocket.close