import os
from flask import Flask, render_template, request, redirect, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash

app = Flask(__name__)
app.secret_key = "secret123"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    age = db.Column(db.Integer)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(200))

print(os.listdir("templates"))
print("Static files:", os.listdir("static"))
print("Static folder:", app.static_folder)
print("Root path:", app.root_path)

@app.before_request
def require_login():
    print("Endpoint:", request.endpoint)

    if request.endpoint is None:
        return

    if request.endpoint not in ("login", "static", "logout") and "user" not in session:
        return redirect("/login")

USERNAME = "admin"
PASSWORD = "1234"

with app.app_context():
    db.create_all()

@app.route("/")
def index():
    if "user" not in session:
        return redirect("/login")

    search = request.args.get("search")

    if search:
        students = Student.query.filter(Student.name.contains(search)).all()
    else:
        students = Student.query.all()

    total_students = Student.query.count()

    return render_template("index.html", students=students, total_students=total_students)
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            session["user"] = user.username
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

    new_student = Student(name=name, age=int(age))
    db.session.add(new_student)
    db.session.commit()

    flash("Student added successfully!")
    return redirect("/")
    
    


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    if "user" not in session:
        return redirect("/login")

    student = db.session.get(Student, id)

    if request.method == 'POST':
        student.name = request.form['name']
        student.age = int(request.form['age'])
        db.session.commit()

        flash("Student updated!")
        return redirect('/')

    return render_template('edit.html', student=student)

from werkzeug.security import generate_password_hash

def create_admin():
    with app.app_context():
        # check if admin already exists
        existing = User.query.filter_by(username="admin").first()
        if not existing:
            admin = User(
                username="admin",
                password=generate_password_hash("1234")
            )

            db.session.add(admin)
            db.session.commit()
            print("✅ Admin user created")
        else:
            print("⚠️ Admin already exists")

@app.route("/delete/<int:id>")
def delete_student(id):
    if "user" not in session:
        return redirect("/login")

    student = db.session.get(Student, id)
    if student:
        db.session.delete(student)
        db.session.commit()
        flash("Student deleted!")
    return redirect("/")

@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("Logged out!")
    return redirect("/login")

if __name__ == "__main__":
    create_admin()
    app.run(debug=True, use_reloader=False)