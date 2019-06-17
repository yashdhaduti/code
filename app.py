from flask import Flask, jsonify
import sqlite3
app = Flask(__name__)

valuelist = []


@app.route('/increment/<string:userkey>', methods=['POST'])
def increment(userkey):
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    for index in valuelist:
        if index == userkey:
            query = "UPDATE valuetable SET uservalue=uservalue+1 WHERE userkey=?"
            cursor.execute(query, (userkey,))

            connection.commit()
            connection.close()

            return get_value(userkey)
    return "Key not found"


@app.route('/decrement/<string:userkey>', methods=['POST'])
def decrement(userkey):
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    for index in valuelist:
        if index == userkey:
            query = "UPDATE valuetable SET uservalue=uservalue-1 WHERE userkey=?"
            cursor.execute(query, (userkey,))

            connection.commit()
            connection.close()

            return get_value(userkey)
    return "Key not found"


@app.route('/insert_value/<string:userkey>/<string:uservalue>', methods=['PUT'])
def insert_value(userkey, uservalue):
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    for index in valuelist:
        if index == userkey:
            return "Key already exists"
    valuelist.append(userkey)
    query = "INSERT INTO valuetable VALUES (?, ?)"
    cursor.execute(query, (userkey, uservalue))

    connection.commit()
    connection.close()
    return jsonify(uservalue)


@app.route('/get_value/<string:userkey>', methods=['GET'])
def get_value(userkey):

    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    query = "SELECT uservalue FROM valuetable WHERE userkey=?"
    result = (cursor.execute(query, (userkey,)))
    row = result.fetchone()
    connection.close()
    if row:
        return jsonify(row[0])
    return "Key Not found"


@app.route('/delete/<string:userkey>', methods=['DELETE'])
def delete(userkey):
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    query = "DELETE FROM valuetable WHERE userkey=?"
    cursor.execute(query, (userkey,))
    for index in valuelist:
        if index == userkey:
            valuelist.remove(userkey)
            connection.commit()
            connection.close()
            return "Key deleted"

    connection.commit()
    connection.close()
    return "There is no key to delete"


app.run(port=5001, debug=True)



