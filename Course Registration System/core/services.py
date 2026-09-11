import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MAIN_DIR = ROOT / "main"
JSON_DIR = ROOT / "json"

if str(MAIN_DIR) not in sys.path:
    sys.path.insert(0, str(MAIN_DIR))

from course import Course  # noqa: E402
from student_course import StudentCourse  # noqa: E402
from user import Student, Teacher  # noqa: E402

FILES = {
    "Student": JSON_DIR / "student.json",
    "Teacher": JSON_DIR / "teacher.json",
    "course": JSON_DIR / "course.json",
    "student_course": JSON_DIR / "student_course.json",
}


def load_list(key):
    path = FILES[key]
    if not path.exists():
        return []
    with open(path, "r") as handle:
        data = json.load(handle)
    return data if isinstance(data, list) else []


def save_list(key, data):
    path = FILES[key]
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as handle:
        json.dump(data, handle, indent=4)


def password_rule(password):
    return (
        len(password) >= 6
        and any(char.isdigit() for char in password)
        and any(char.isalpha() for char in password)
        and not any(char.isspace() for char in password)
    )


PASSWORD_RULES_TEXT = (
    "Password must be at least 6 characters, include a letter and a number, "
    "and contain no spaces."
)


def login_user(role_class, username, password):
    username = (username or "").strip()
    password = password or ""
    if not username or not password:
        return None, "Username and password are required."

    data = load_list(role_class.get_name())
    if not data:
        return None, f"No {role_class.get_name().lower()} accounts found."

    for record in data:
        if record.get("username") == username and record.get("password") == password:
            if role_class.get_name() == "Teacher":
                user = role_class(
                    record["full_name"],
                    record["username"],
                    record["email"],
                    record["password"],
                    record["teacher_id"],
                )
            else:
                user = role_class(
                    record["full_name"],
                    record["username"],
                    record["email"],
                    record["password"],
                    record["student_id"],
                )
            return user, f"Logged in as {record['full_name']}."

    return None, f"{role_class.get_name()} login failed. Check your credentials."


def register_user(role_class, full_name, username, email, password, confirm_password):
    full_name = (full_name or "").strip()
    username = (username or "").strip()
    email = (email or "").strip()
    password = password or ""
    confirm_password = confirm_password or ""

    if not all([full_name, username, email, password, confirm_password]):
        return False, "Please fill in every field."
    if not email.endswith("@gmail.com"):
        return False, "Email must end with @gmail.com."
    if not password_rule(password):
        return False, PASSWORD_RULES_TEXT
    if password != confirm_password:
        return False, "Passwords do not match."

    data = load_list(role_class.get_name())
    for record in data:
        if record.get("username") == username:
            return False, "Username already exists. Choose a different one."
        if record.get("email") == email:
            return False, "Email already exists. Choose a different one."

    user = role_class(full_name, username, email, password)
    data.append(user.to_dict())
    save_list(role_class.get_name(), data)
    return True, f"{role_class.get_name()} registered successfully."


def change_password(role_class, user, current_password, new_password, confirm_password):
    if user.password != current_password:
        return False, "Current password is incorrect."
    if not password_rule(new_password):
        return False, PASSWORD_RULES_TEXT
    if new_password != confirm_password:
        return False, "New passwords do not match."

    key = "student_id" if role_class.get_name() == "Student" else "teacher_id"
    user_id = user.student_id if key == "student_id" else user.teacher_id
    data = load_list(role_class.get_name())
    updated = False
    for record in data:
        if record.get(key) == user_id:
            record["password"] = new_password
            updated = True
            break
    if not updated:
        return False, "Account not found."

    save_list(role_class.get_name(), data)
    user.password = new_password
    return True, "Password updated."


def list_teachers():
    return {item["teacher_id"]: item for item in load_list("Teacher")}


def list_students():
    return {item["student_id"]: item for item in load_list("Student")}


def list_courses():
    return load_list("course")


def list_enrollments():
    return load_list("student_course")


def teacher_courses(teacher):
    return [
        course
        for course in list_courses()
        if course.get("teacher") == teacher.teacher_id
    ]


def student_enrollments(student):
    enrolled_ids = {
        item["course_id"]
        for item in list_enrollments()
        if item.get("student_id") == student.student_id
    }
    courses = []
    teachers = list_teachers()
    for course in list_courses():
        if course["course_id"] in enrolled_ids:
            teacher = teachers.get(course.get("teacher"), {})
            courses.append(
                {
                    **course,
                    "teacher_name": teacher.get("full_name", "Unknown"),
                }
            )
    return courses


def available_courses_for_student(student):
    enrolled_ids = {
        item["course_id"]
        for item in list_enrollments()
        if item.get("student_id") == student.student_id
    }
    teachers = list_teachers()
    available = []
    for course in list_courses():
        if course["course_id"] not in enrolled_ids:
            teacher = teachers.get(course.get("teacher"), {})
            available.append(
                {
                    **course,
                    "teacher_name": teacher.get("full_name", "Unknown"),
                }
            )
    return available


def create_course(teacher, course_name):
    course_name = (course_name or "").strip()
    if not course_name:
        return False, "Course name is required."

    data = list_courses()
    for course in data:
        if course["course_name"].lower() == course_name.lower():
            return False, "Course already exists. Choose a different name."

    data.append(Course(course_name, teacher).to_dict())
    save_list("course", data)
    return True, f"Course '{course_name}' created."


def drop_teacher_course(teacher, course_id):
    courses = list_courses()
    target = next(
        (
            course
            for course in courses
            if course["course_id"] == course_id and course["teacher"] == teacher.teacher_id
        ),
        None,
    )
    if not target:
        return False, "Course not found in your list."

    remaining = [course for course in courses if course["course_id"] != course_id]
    save_list("course", remaining)

    enrollments = [
        item for item in list_enrollments() if item.get("course_id") != course_id
    ]
    save_list("student_course", enrollments)
    return True, f"Course '{target['course_name']}' dropped."


def register_student_course(student, course_id):
    courses = list_courses()
    course = next((item for item in courses if item["course_id"] == course_id), None)
    if not course:
        return False, "Course does not exist."

    enrollments = list_enrollments()
    for item in enrollments:
        if item["student_id"] == student.student_id and item["course_id"] == course_id:
            return False, "You are already registered for this course."

    course_obj = Course(course["course_name"], course["teacher"], course["course_id"])
    enrollments.append(StudentCourse(student, course_obj).to_dict())
    save_list("student_course", enrollments)
    return True, f"Registered for '{course['course_name']}'."


def drop_student_course(student, course_id):
    enrollments = list_enrollments()
    remaining = [
        item
        for item in enrollments
        if not (item["student_id"] == student.student_id and item["course_id"] == course_id)
    ]
    if len(remaining) == len(enrollments):
        return False, "You are not registered for that course."

    save_list("student_course", remaining)
    course = next((item for item in list_courses() if item["course_id"] == course_id), None)
    name = course["course_name"] if course else "course"
    return True, f"Dropped '{name}'."


def students_in_course(course_id):
    student_ids = {
        item["student_id"]
        for item in list_enrollments()
        if item.get("course_id") == course_id
    }
    students = list_students()
    return [students[student_id] for student_id in student_ids if student_id in students]
