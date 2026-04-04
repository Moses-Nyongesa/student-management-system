from tkinter import *
from utils import load_students, save_students

students = load_students()

def refresh_list():
    name_entry.delete(0, END)
    age_entry.delete(0, END)
    listbox.delete(0, END)
    for student in students:
        listbox.insert(END, f"ID: {student['id']} | {student['name']} ({student['age']})")

def add_student():
    name = name_entry.get()
    age = age_entry.get()

    if not name or not age:
        status_label.config(text="Please enter name and age", fg="red")
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
    status_label.config(text="Student added successfully!")

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
    status_label.config(text="Student deleted successfully!")

def update_student():
    selected = listbox.get(ACTIVE)
    if not selected:
        return

    student_id = int(selected.split("|")[0].split(":")[1])

    for s in students:
        if s["id"] == student_id:
            new_name = name_entry.get()
            new_age = age_entry.get()

            if new_name:
                s["name"] = new_name

            if new_age:
                try:
                    s["age"] = int(new_age)
                except:
                    return
            break

    save_students(students)
    refresh_list()
    status_label.config(text="Student updated successfully!")

# UI
root = Tk()
root.title("Student Management System")

Label(root, text="Name").pack()
name_entry = Entry(root)
name_entry.pack()

Label(root, text="Age").pack()
age_entry = Entry(root)
age_entry.pack()

frame = Frame(root)
frame.pack()

Button(frame, text="Add Student", command=add_student).grid(row=0, column=0)
Button(frame, text="Update Selected", command=update_student).grid(row=0, column=1)
Button(frame, text="Delete Selected", command=delete_student).grid(row=0, column=2)
listbox = Listbox(root, width=50)
listbox.pack()

status_label = Label(root, text="", fg="green")
status_label.pack()

refresh_list()

root.mainloop()