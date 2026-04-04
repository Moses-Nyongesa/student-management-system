from tkinter import *
from utils import load_students, save_students

students = load_students()

def refresh_list():
    listbox.delete(0, END)
    for student in students:
        listbox.insert(END, f"ID: {student['id']} | {student['name']} ({student['age']})")

def add_student():
    name = name_entry.get()
    age = age_entry.get()

    if not name or not age:
        return

    try:
        age = int(age)
    except:
        return

    student_id = 1
    if students:
        student_id = max(s["id"] for s in students) + 1

    students.append({"id": student_id, "name": name, "age": age})
    save_students(students)
    refresh_list()

def delete_student():
    selected = listbox.get(ACTIVE)
    if not selected:
        return

    student_id = int(selected.split("|")[0].split(":")[1])

    for s in students:
        if s["id"] == student_id:
            students.remove(s)
            break

    save_students(students)
    refresh_list()

# UI
root = Tk()
root.title("Student Management System")

Label(root, text="Name").pack()
name_entry = Entry(root)
name_entry.pack()

Label(root, text="Age").pack()
age_entry = Entry(root)
age_entry.pack()

Button(root, text="Add Student", command=add_student).pack()
Button(root, text="Delete Selected", command=delete_student).pack()

listbox = Listbox(root, width=50)
listbox.pack()

refresh_list()

root.mainloop()