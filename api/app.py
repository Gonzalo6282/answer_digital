from tkinter.filedialog import test
from flask import Flask, jsonify, request
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS
import create_db
import sqlite3
  
app = Flask(__name__)
CORS(app)

SWAGGER_URL = '/api/docs'
API_URL = '/static/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Python Tech Test API"
    }
)
app.register_blueprint(swaggerui_blueprint)

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

# TODO - you will need to implement the other endpoints
# GET /api/people/{id} - get person with given id
# POST /api/people - create 1 person
# PUT /api/people/{id} - Update a person with the given id
# DELETE /api/people/{id} - Delete a person with a given id

@app.route("/api/people/")
def getall_people():
    conn = sqlite3.connect('test.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    all_people = cur.execute('SELECT * FROM Person;').fetchall()
    return jsonify(all_people)   

#GET PERSON WITH GIVEN ID   
@app.route('/api/people/<id>', methods = ["GET"])
def get_person(id):
    conn = sqlite3.connect('test.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    person = cur.execute(f'SELECT * FROM Person WHERE id = {id};').fetchone()
    return jsonify(person)
    

#CREATE PERSON 
@app.route("/api/people", methods = ["POST"])
def create_person():
    conn = sqlite3.connect('test.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    person = (request.json['id'],
              request.json['firstName'],
              request.json['lastName'],
              request.json['authorised'],
              request.json['enabled'])
    cur.execute('INSERT INTO Person(id, firstName, lastName, authorised, enabled) VALUES(?, ?, ?, ?, ?)', person)
    conn.commit()
    cur.close()
    conn.close()
    return jsonify(person)   
 
#UPDATE PERSON WITH GIVEN ID
@app.route("/api/people/<id>", methods = ["PUT"])
def update_person(id):
    conn = sqlite3.connect('test.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    update_person = (
          request.json['firstName'],
          request.json['lastName'],
          request.json['authorised'],
          request.json['enabled'],
          id
          )
    cur.execute('UPDATE Person SET firstName =  ?, lastName = ?, enabled = ?, authorised = ? WHERE id = ?', update_person)
    conn.commit()
    cur.close()
    conn.close()
    return jsonify(update_person)

#DELETE PERSON WITH GIVEN ID
@app.route("/api/people/<id>", methods = ["DELETE"])
def delete_person(id):
    conn = sqlite3.connect('test.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    cur.execute(f'DELETE FROM Person WHERE id={id};')
    conn.commit()
    cur.close()
    conn.close()
    return "Person deleted"


if __name__ == '__main__':
    app.run()
