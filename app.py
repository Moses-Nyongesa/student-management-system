import os
print(os.listdir("templates"))
print("Static files:", os.listdir("static"))  # ← ADD THIS LINE

from flask import Flask, render_template, request, redirect, session, flash
from utils import load_students, save_students

app = Flask(__name__)
app.secret_key = "secret123"

@app.before_request
def require_login():
    if request.endpoint not in ("login", "static") and "user" not in session:
        return redirect("/login")
    
USERNAME = "admin"
PASSWORD = "1234"  # add this
print("Static folder:", app.static_folder)  # Add this
print("Root path:", app.root_path)           # Add this
students = load_students()

@app.route("/")
def index():
    if "user" not in session:
        return redirect("/login")

    search = request.args.get("search")

    if search:
        filtered_students = [
            s for s in students if search.lower() in s["name"].lower()
        ]
    else:
        filtered_students = students

    total_students = len(students)

    return render_template(
        "index.html",
        students=filtered_students,
        total_students=total_students
    )

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        print("Expected:", USERNAME, PASSWORD)
        print("Entered:", username, password)

        if username == USERNAME and password == PASSWORD:
            session["user"] = username
            flash("Login successful!")
            return redirect("/")
        else:
            flash("Invalid credentials!")

    return render_template("login.html")

@app.route("/add", methods=["POST"])
def add_student():
    if "user" not in session:
        return redirect("/login")
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
    flash("Student added successfully!")

    return redirect("/")
    

@app.route("/delete/<int:id>")
def delete_student(id):
    if "user" not in session:
        return redirect("/login")
    global students
    students = [s for s in students if s["id"] != id]
    save_students(students)
    flash("Student deleted!")
    return redirect("/")
    


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    if "user" not in session:
        return redirect("/login")
    global students
    student = next((s for s in students if s['id'] == id), None)
    if not student:
        return redirect('/')

    if request.method == 'POST':
        student['name'] = request.form['name']
        student['age'] = int(request.form['age'])
        save_students(students)
        flash("Student updated!")
        return redirect('/')

    return render_template('edit.html', student=student)

@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("Logged out!")
    return redirect("/login")
    

app.run(debug=True)