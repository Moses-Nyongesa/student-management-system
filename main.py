import json


def load_students():
    try:
        with open("students.json", "r") as file:
            return json.load(file)
    except:
        return []


students = load_students()


def add_student():
    name = input("Enter student name: ")
    
    try:
        age = int(input("Enter student age: "))
    except:
        print("Invalid age. Must be a number.\n")
        return

    student_id = 1
    if students:
        student_id = max(s["id"] for s in students) + 1
    student = {"id": student_id, "name": name, "age": age}
    students.append(student)
    save_students(students)
    print("Student added successfully!\n")


def save_students(students):
    with open("students.json", "w") as file:
        json.dump(students, file)


def view_students():
    if not students:
        print("No students found.\n")
        return
    for i, student in enumerate(students):
        print(f"ID: {student['id']} | Name: {student['name']} | Age: {student['age']}")
    print()


def delete_student():
    student_id = int(input("Enter student ID to delete: "))

    for student in students:
        if student["id"] == student_id:
            students.remove(student)
            save_students(students)
            print("Student deleted successfully!\n")
            return

    print("Student not found.\n")


def search_student():
    name = input("Enter name to search: ")
    found = False
    for student in students:
        if name.lower() in student["name"].lower():
            print(f"Found: Name: {student['name']}, Age: {student['age']}\n")
            found = True
    if not found:
        print("Student not found.\n")


def menu():
    print("\nWelcome to Student Management System\n")


    while True:
        print("1. Add Student")
        print("2. View Students")
        print("3. Delete Student")
        print("4. Search Student")
        print("5. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            add_student()
        elif choice == "2":
            view_students()
        elif choice == "3":
            delete_student()
        elif choice == "4":
            search_student()
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.\n")

menu()