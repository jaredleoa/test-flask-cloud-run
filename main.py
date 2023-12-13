import os
from flask import Flask, jsonify, Response, render_template, request 
from flask_cors import CORS
import os, re, datetime
import db
from models import Student

# def create_app():
app = Flask(__name__)
CORS(app)
# Error 404 handler
@app.errorhandler(404)
def resource_not_found(e):
  return jsonify(error=str(e)), 404
# Error 405 handler
@app.errorhandler(405)
def resource_not_found(e):
  return jsonify(error=str(e)), 405

if not os.path.isfile('students.db'):
  db.connect()

@app.route("/")
def hello_world():
    return render_template("index.html")

@app.route('/read', methods=['GET'])
def getRequest():
    sts = [s.serialize() for s in db.view()]
    print('students in lib: ', sts)
    return jsonify({
            'res': sts,
            'status': '200',
            'msg': 'Success getting all students.'
        })

@app.route("/write", methods=['POST'])
def postRequest():
    req_data = request.get_json()
    course = req_data['course']
    name = req_data['name']
    year = req_data['year']

    st = Student(db.getNewId(), name, course, year)

    db.insert(st)
    new_sts = [s.serialize() for s in db.view()]
    print('students in lib: ', new_sts)
    
    return jsonify({
                # 'error': '',
                'res': st.serialize(),
                'status': '200',
                'msg': 'Success adding new student.'
            })

@app.route('/readStudent/', methods=['GET'])
def getRequestId():
    sts = [s.serialize() for s in db.view()]

    for s in sts:
        if s['id'] == int(request.args.get('id')):
            return jsonify({
                # 'error': '',
                'res': s,
                'status': '200',
                'msg': 'Success getting student by ID.'
            })
            
    return jsonify({
        'error': f"Error. Student with id '{request.args.get('id')}' was not found.",
        'res': '',
        'status': '404'
    })

@app.route("/update", methods=['POST'])
def putRequest():
    req_data = request.get_json()
    the_id = req_data['id']
    name = req_data['name']
    course = req_data['course']
    year = req_data['year']

    sts = [s.serialize() for s in db.view()]
    for s in sts:
        if s['id'] == int(the_id):
            st = Student(
                the_id, 
                name, 
                course, 
                year
            )
            print('new student: ', st.serialize())
            db.update(st)
            new_sts = [s.serialize() for s in db.view()]
            print('students in lib: ', new_sts)
            return jsonify({
                # 'error': '',
                'res': st.serialize(),
                'status': '200',
                'msg': f'Success updating the student named: {name}.'
            })     
    return jsonify({
                # 'error': '',
                'msg': f'Error: Failed to update Student with named: {name}.',
                'status': '404'
            })

    
@app.route('/delete/', methods=['GET'])
def deleteRequest():
    sts = [s.serialize() for s in db.view()]
    for s in sts:
        if s['id'] == int(request.args.get('id')):
            db.delete(s['id'])
            updated_sts = [s.serialize() for s in db.view()]
            print('updated_sts: ', updated_sts)
            return jsonify({
                'res': updated_sts,
                'status': '200',
                'msg': 'Success deleting student by ID.',
                'updated_no_of_students': len(updated_sts)
            })
    return jsonify({
                'status': '400',
                'msg': f'No student with id ${request.args.get("id")} was found.'
            })

if __name__ == "__main__":
  #    app = create_app()
  print(" Starting app...")
  app.run(host="0.0.0.0", port=8080)