import json
from flask import Flask, jsonify, request

studentList = {}
courseList = {}

app = Flask(__name__)


def studentGet():
    return jsonify(studentList)

def studentPost():
    data = request.get_json()
    student_id = list(data.keys())[0]
    student_info = list(data.values())[0]
    
    if len(student_info) != 3:
        return "Invalid student data format", 400

    name = student_info[0].split(": ")[1] 
    major = student_info[1].split(": ")[1]  
    courses = student_info[2].get("courses", [])

    if not student_id or not name or not major:
        return "Missing student ID, name, or major", 400

    studentList[student_id] = [f"name: {name}", f"major: {major}", {"courses": courses}]
    return "Student added successfully", 201

def studentPut():
    data = request.get_json()
    student_id = list(data.keys())[0]
    student_info = list(data.values())[0]

    if student_id not in studentList:
        return "Student not found", 404

    name = student_info[0].split(": ")[1] if len(student_info) > 0 else studentList[student_id][0].split(": ")[1]
    major = student_info[1].split(": ")[1] if len(student_info) > 1 else studentList[student_id][1].split(": ")[1]
    courses = student_info[2].get("courses", studentList[student_id][2].get("courses", []))

    studentList[student_id] = [f"name: {name}", f"major: {major}", {"courses": courses}]
    return "Student updated successfully", 200

def studentDelete():
    data = request.get_json()
    student_id = list(data.keys())[0]

    if not student_id:
        return "Student ID missing", 400

    if student_id in studentList:
        del studentList[student_id]
        return "Student deleted successfully", 200

    return "Student not found", 404

def coursesGet():
    course_name = request.args.get("course")
    if not course_name:
        return "Course name not provided", 400

    students_in_course = [
        {"id": student_id, "name": details["name"]}
        for student_id, details in studentList.items()
        if course_name in details.get("courses", [])
    ]
    return jsonify(students_in_course)

def coursesPost():
    data = request.get_json()
    student_id = data.get("id")
    course_name = data.get("course")

    if not student_id or not course_name:
        return "Student ID or course name missing", 400

    if student_id not in studentList:
        return "Student not found", 404

    if course_name in studentList[student_id]["courses"]:
        return "Course already added", 400

    studentList[student_id]["courses"].append(course_name)
    return "Course added successfully", 201

def coursesPut():
    data = request.get_json()
    student_id = data.get("id")
    new_courses = data.get("courses")

    if not student_id or not new_courses:
        return "Student ID or courses missing", 400

    if student_id not in studentList:
        return "Student not found", 404

    studentList[student_id]["courses"] = new_courses
    return "Courses updated successfully", 200

def coursesDelete():
    data = request.get_json()
    student_id = data.get("id")
    course_name = data.get("course")

    if not student_id or not course_name:
        return "Student ID or course name missing", 400

    if student_id not in studentList:
        return "Student not found", 404

    courses = studentList[student_id]["courses"]
    if course_name not in courses:
        return "Course not found for the student", 404

    courses.remove(course_name)
    return "Course removed successfully", 200

@app.route("/student", methods=["GET", "POST", "PUT", "DELETE"])
def student():
    if request.method == "GET":
        return studentGet()
    elif request.method == "POST":
        return studentPost()
    elif request.method == "PUT":
        return studentPut()
    elif request.method == "DELETE":
        return studentDelete()
    return "Bad Request", 400

@app.route("/courses", methods=["GET", "POST", "PUT", "DELETE"])
def courses():
    if request.method == "GET":
        return coursesGet()
    elif request.method == "POST":
        return coursesPost()
    elif request.method == "PUT":
        return coursesPut()
    elif request.method == "DELETE":
        return coursesDelete()
    return "Bad Request", 400

if __name__ == "__main__":
    app.run(debug=True)
