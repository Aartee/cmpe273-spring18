import zmq
import json

context = zmq.Context()

socket_rep = context.socket(zmq.REP)
socket_rep.bind("tcp://127.0.0.1:5680")
socket_pub = context.socket(zmq.PUB)
socket_pub.bind("tcp://127.0.0.1:5678")

def respond_all():
    while True:
        msg = socket_rep.recv_string()
        socket_pub.send_string(msg)
        socket_rep.send_string(msg)
        
if __name__ == '__main__':
    respond_all()