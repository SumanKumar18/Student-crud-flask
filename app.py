from flask import Flask, render_template, request, redirect, url_for
from db_config import get_connection
import os
import sqlite3

# 🔧 Auto-create students.db with students table if it doesn't exist
if not os.path.exists("students.db"):
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER,
            grade TEXT
        )
    ''')
    conn.commit()
    conn.close()


app = Flask(__name__)


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/add", methods=["GET", "POST"])
def add_student():
    if request.method == "POST":
    name = request.form["name"]
    age = int(request.form["age"])
    grade = request.form["grade"]
        
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO students (name,age,grade)VALUES(?,?,?)",(name,age,grade))
    conn.commit()
    conn.close()
    return redirect(url_for("view_students"))
    return render_template("add.html")


@app.route('/view')
def view_students():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    conn.close()
    return render_template('view.html', students=students)

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_student(id):
    conn = get_connection()
    cursor = conn.cursor()
    if request.method == 'POST':
    name = request.form['name']
    age = request.form['age']
    grade = request.form['grade']
    cursor.execute("UPDATE students SET name = ?, age = ?, grade = ? WHERE id = ?", (name, age, grade, id))

    conn.commit()
    conn.close()
    return redirect(url_for('view_students'))
    else:
        cursor.execute("SELECT * FROM students WHERE id=%s", (id,))
        student = cursor.fetchone()
        conn.close()
        return render_template('update.html', student=student)

@app.route('/delete/<int:id>')
def delete_student(id):
    conn = get_connection()
    cursor = conn.cursor()
   cursor.execute("DELETE FROM students WHERE id = ?", (id,))

    conn.commit()
    conn.close()
    return redirect(url_for('view_students'))

if __name__ == '__main__':
    app.run(debug=True)
