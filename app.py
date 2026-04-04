import os
print(os.listdir("templates"))
print("Static files:", os.listdir("static"))  # ← ADD THIS LINE

from flask import Flask, render_template, request, redirect
from utils import load_students, save_students

app = Flask(__name__)
print("Static folder:", app.static_folder)  # Add this
print("Root path:", app.root_path)           # Add this
students = load_students()

@app.route("/")
def index():
    return render_template("index.html", students=students)

@app.route("/add", methods=["POST"])
def add_student():
    name = request.form.get("name")
    age = request.form.get("age")

    if not name or not age:
        return redirect("/")

    try:
        age = int(age)
    except:
        return redirect("/")

    student_id = 1
    if students:
        student_id = max(s["id"] for s in students) + 1

    students.append({"id": student_id, "name": name, "age": age})
    save_students(students)

    return redirect("/")

@app.route("/delete/<int:id>")
def delete_student(id):
    global students
    students = [s for s in students if s["id"] != id]
    save_students(students)
    return redirect("/")

app.run(debug=True)