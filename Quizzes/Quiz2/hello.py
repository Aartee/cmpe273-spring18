# Assignment submitted by Aartee Kasliwal - Student ID:012419004
# Setup
# virtualenv my-venv
# . my-venv/bin/activate
# pip3 install -r requirements.txt

# Run the server as
# FLASK_APP=hello.py flask run
# Send the request as
# curl -i http://127.0.0.1:5000/
# curl -i -X POST http://127.0.0.1:5000/users -d "name=foo"
# curl -i -X GET http://127.0.0.1:5000/users/1
# curl -i -X DELETE http://127.0.0.1:5000/users/1

from flask import Flask, request, json
app = Flask(__name__)

usersList = []
userNumber = 0

@app.route("/")
def hello():
    return "Hello World!"

@app.route('/users', methods=['POST'])
def users():
    name = request.form["name"]
    global userNumber
    userNumber += 1
    user = {
        'id' : userNumber,
        'name' : name
    }
    usersList.append(user) 
    return json.dumps(user, indent=4, separators=(',', ':')), 201

@app.route('/users/<userid>')
def getUsers(userid):
    userName = ''
    for i in range(len(usersList)):
        if(int(usersList[i]['id']) == int(userid)):
            userName = str(usersList[i]['name'])
            user = {
            'id' : userid,
            'name' : userName
            }
        else:
            user = {
                'message' : 'User with given userid is not available'
            }
    return json.dumps(user, indent=4, separators=(',', ':'))

@app.route('/users/<userid>', methods=['DELETE'])
def deleteUsers(userid):
    userName = ''
    for i in range(len(usersList)):
        if(int(usersList[i]['id']) == int(userid)):
            userName = str(usersList[i]['name'])
            user = {
                'id' : userid,
                'name' : userName
            }
            usersList.pop(i)
            break
        else:
            user = {
                'message' : 'User with given userid does not exist to delete'
            }
    return '', 204