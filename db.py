import sqlite3, random, datetime
from models import Student

def getNewId():
    return random.getrandbits(28)

students = [
]    

def connect():
    conn = sqlite3.connect('students.db')
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS students (id INTEGER PRIMARY KEY, name TEXT, course TEXT, year TEXT)")
    conn.commit()
    conn.close()
    for i in students:
        st = Student(getNewId(), i['name'], i['course'], i['year'])
        insert(st)

def insert(student):
    conn = sqlite3.connect('students.db')
    cur = conn.cursor()
    cur.execute("INSERT INTO students VALUES (?,?,?,?)", (
        student.id,
        student.name,
        student.course,
        student.year
    ))
    conn.commit()
    conn.close()

def view():
    conn = sqlite3.connect('students.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM students")
    rows = cur.fetchall()
    students = []
    for i in rows:
        student = Student(i[0], i[1], i[2], i[3])
        students.append(student)
    conn.close()
    return students

def update(student):
    conn = sqlite3.connect('students.db')
    cur = conn.cursor()
    cur.execute("UPDATE students SET name=?, course=?, year=? WHERE id=?", (student.name, student.course, student.year, student.id))
    conn.commit()
    conn.close()

def delete(theId):
    conn = sqlite3.connect('students.db')
    cur = conn.cursor()
    cur.execute("DELETE FROM students WHERE id=?", (theId,))
    conn.commit()
    conn.close()

def deleteAll():
    conn = sqlite3.connect('students.db')
    cur = conn.cursor()
    cur.execute("DELETE FROM students")
    conn.commit()
    conn.close()