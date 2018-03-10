import zmq
import uuid
import select
import sys
import json
import gevent

context = zmq.Context()

socket = context.socket(zmq.SUB)
socket.setsockopt_string(zmq.SUBSCRIBE,"")
socket.connect("tcp://127.0.0.1:5678")

def inpute(client):
    """Non-blocking raw_input."""
    if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
        return sys.stdin.readline()
    else:
        return "1"

def subscriber(connection, sender_id):
    while True:
        while True:
            try:
                data=json.loads(socket.recv_string(zmq.NOBLOCK))
                #print the message coming from all other clients except own
                if data['sender_id'] != sender_id:
                    sys.stdout.write("[%s]: %s" % (data['client'], data['message']))
            except zmq.ZMQError:
                break
        gevent.sleep(0)

def sender(connection,client,sender_id):
    """Takes user input and sends message to server."""
    socket_req = context.socket(zmq.REQ)
    socket_req.connect(connection)
    while True:
        message = str(inpute(client))
        if message != "1" :
            socket_req.send_string(json.dumps({
            'client': client,
            'message': message,
            'sender_id': sender_id,
        }))
            msg_in = str(socket_req.recv_string())
        gevent.sleep(0)

if __name__ == '__main__':
    client = str(sys.argv[1])
    sender_connection = "tcp://127.0.0.1:5680"
    subscriber_connection = "tcp://127.0.0.1:5678"
    # Generate a sender_id
    sender_id = uuid.uuid4().hex
    sender = gevent.spawn(sender, sender_connection, client, sender_id)
    subscriber = gevent.spawn(subscriber, subscriber_connection, sender_id)
    gevent.joinall([sender,subscriber])
