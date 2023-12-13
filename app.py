from flask import Flask, render_template, request, json
from flask_mysqldb import MySQL
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
mysql = MySQL(app)

# MySQL configurations
app.config['MYSQL_USER'] = 'A'  # Replace with your MySQL user
app.config['MYSQL_PASSWORD'] = 'B'  # Replace with your MySQL password
app.config['MYSQL_DB'] = 'student'  # Replace with your database name
app.config['MYSQL_HOST'] = 'db.mydomain.ie'  # Replace with your MySQL host

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/add", methods=['GET', 'POST'])  # Add Student
def add():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO students(studentName, email) VALUES(%s, %s)", (name, email))
        mysql.connection.commit()
        cur.close()
        return json.dumps({'message': 'Student added successfully'})
    return render_template("add_student.html")

@app.route("/students")  # Read all students
def students():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM students")
    student_data = cur.fetchall()
    cur.close()
    return render_template("students.html", students=student_data)

# Additional routes for Update and Delete operations can be added here

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
