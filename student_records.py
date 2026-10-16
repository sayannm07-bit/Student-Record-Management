import json
from pathlib import Path

DATA_FILE = Path("students.json")


def load_students():
    """Load student records from JSON, or start with an empty dictionary."""
    if not DATA_FILE.exists():
        return {}
    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)
        return data if isinstance(data, dict) else {}
    except (json.JSONDecodeError, OSError):
        print("Warning: saved student data could not be read. Starting empty.")
        return {}


students = load_students()


def save_students():
    """Save all student records to JSON."""
    try:
        with DATA_FILE.open("w", encoding="utf-8") as file:
            json.dump(students, file, indent=4, ensure_ascii=False)
    except OSError as error:
        print(f"Could not save records: {error}")


def ask(prompt):
    """Read input and handle environments that do not provide interactive input."""
    try:
        return input(prompt).strip()
    except EOFError:
        print("\nNo interactive input is available. Run this program in a console.")
        raise SystemExit


def add_student():
    student_id = ask("Student ID: ")
    if not student_id:
        print("ID cannot be empty.")
        return
    if student_id in students:
        print("That ID already exists.")
        return

    name = ask("Name: ")
    course = ask("Course: ")
    if not name or not course:
        print("Name and course are required.")
        return

    try:
        age = int(ask("Age: "))
        marks = float(ask("Marks (0-100): "))
        if age <= 0 or not 0 <= marks <= 100:
            raise ValueError
    except ValueError:
        print("Enter a positive whole-number age and marks from 0 to 100.")
        return

    students[student_id] = {
        "name": name,
        "age": age,
        "course": course,
        "marks": marks
    }
    save_students()
    print("Student added.")


def view_students():
    if not students:
        print("No student records yet.")
        return
    print("\n--- STUDENT RECORDS ---")
    for student_id, student in students.items():
        print(
            f"ID: {student_id} | Name: {student['name']} | "
            f"Age: {student['age']} | Course: {student['course']} | "
            f"Marks: {student['marks']:.2f}"
        )


def search_student():
    student_id = ask("Enter the ID to search: ")
    student = students.get(student_id)
    if student is None:
        print("Student not found.")
        return
    print(f"ID: {student_id}")
    for field, value in student.items():
        print(f"{field.title()}: {value}")


def update_student():
    student_id = ask("Enter the ID to update: ")
    student = students.get(student_id)
    if student is None:
        print("Student not found.")
        return

    print("Press Enter to keep the current value.")
    name = ask(f"Name [{student['name']}]: ")
    course = ask(f"Course [{student['course']}]: ")
    age_text = ask(f"Age [{student['age']}]: ")
    marks_text = ask(f"Marks [{student['marks']}]: ")

    try:
        age = int(age_text) if age_text else student["age"]
        marks = float(marks_text) if marks_text else student["marks"]
        if age <= 0 or not 0 <= marks <= 100:
            raise ValueError
    except ValueError:
        print("Invalid age or marks; no changes were saved.")
        return

    student["name"] = name or student["name"]
    student["course"] = course or student["course"]
    student["age"] = age
    student["marks"] = marks
    save_students()
    print("Student updated.")


def delete_student():
    student_id = ask("Enter the ID to delete: ")
    if student_id not in students:
        print("Student not found.")
        return
    confirm = ask(f"Delete {students[student_id]['name']}? (yes/no): ").lower()
    if confirm == "yes":
        del students[student_id]
        save_students()
        print("Student deleted.")
    else:
        print("Deletion cancelled.")


def main():
    actions = {
        "1": add_student,
        "2": view_students,
        "3": search_student,
        "4": update_student,
        "5": delete_student
    }
    while True:
        print("\n=== STUDENT RECORD MANAGEMENT ===")
        print("1. Add student")
        print("2. View all students")
        print("3. Search by ID")
        print("4. Update student")
        print("5. Delete student")
        print("6. Exit")
        choice = ask("Choose 1-6: ")
        if choice == "6":
            print("Goodbye!")
            break
        action = actions.get(choice)
        if action:
            action()
        else:
            print("Choose a number from 1 to 6.")


if __name__ == "__main__":
    main()
