students = []

def add_student():
    name = input("Enter student name: ")
    age = int(input("Enter student age: "))
    student = {"name": name, "age": age}
    students.append(student)
    print("Student added successfully!\n")

def view_students():
    if not students:
        print("No students found.\n")
        return
    for i, student in enumerate(students):
        print(f"{i + 1}. Name: {student['name']}, Age: {student['age']}")
    print()

def delete_student():
    view_students()
    try:
        index = int(input("Enter student number to delete: ")) - 1
        if 0 <= index < len(students):
            students.pop(index)
            print("Student deleted successfully!\n")
        else:
            print("Invalid number.\n")
    except:
        print("Error occurred.\n") 


def search_student():
    name = input("Enter name to search: ")
    found = False
    for student in students:
        if student["name"].lower() == name.lower():
            print(f"Found: Name: {student['name']}, Age: {student['age']}\n")
            found = True
    if not found:
        print("Student not found.\n")

def menu():
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