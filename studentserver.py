import json
from flask import Flask, jsonify, request, send_from_directory
import redis

studentList = {}
courseList = {}

app = Flask(__name__)
r = redis.Redis(host='localhost', port=6379, db=0)

""" #def studentGet():
    #return jsonify(studentList)

#def studentPost():
    
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
    return "Student added successfully", 201 """

def studentPut():
    # Retrieve JSON data from the request body
    data = request.get_json()
    # Extract the student ID from the JSON data
    student_id = list(data.keys())[0]
    # Extract the student info associated with the ID
    student_info = list(data.values())[0]

    # Check if the student exists in the student list
    if student_id not in studentList:
        return "Student not found", 404

    # Extract student name, major, and courses from student_info or keep existing values
    name = student_info[0].split(": ")[1] if len(student_info) > 0 else studentList[student_id][0].split(": ")[1]
    major = student_info[1].split(": ")[1] if len(student_info) > 1 else studentList[student_id][1].split(": ")[1]
    courses = student_info[2].get("courses", studentList[student_id][2].get("courses", []))

    # Update the student information in the student list
    studentList[student_id] = [f"name: {name}", f"major: {major}", {"courses": courses}]
    return "Student updated successfully", 200

def studentDelete():
    # Retrieve JSON data from the request body
    data = request.get_json()
    # Extract the student ID from the JSON data
    student_id = list(data.keys())[0]

    # Check if the student ID is provided
    if not student_id:
        return "Student ID missing", 400

    # Check if the student exists in the student list and delete
    if student_id in studentList:
        del studentList[student_id]
        return "Student deleted successfully", 200

    return "Student not found", 404

def coursesGet():
    # Get the course name from the query parameters
    course_name = request.args.get("course")
    # Check if the course name is provided
    if not course_name:
        return "Course name not provided", 400

    # Find all students enrolled in the given course
    students_in_course = [
        {"id": student_id, "name": details["name"]}
        for student_id, details in studentList.items()
        if course_name in details.get("courses", [])
    ]
    return jsonify(students_in_course)

def coursesPost():
    # Retrieve JSON data from the request body
    data = request.get_json()
    # Extract student ID and course name from the data
    student_id = data.get("id")
    course_name = data.get("course")

    # Check if student ID or course name is missing
    if not student_id or not course_name:
        return "Student ID or course name missing", 400

    # Check if the student exists in the student list
    if student_id not in studentList:
        return "Student not found", 404

    # Check if the course is already added for the student
    if course_name in studentList[student_id]["courses"]:
        return "Course already added", 400

    # Add the new course to the student's list of courses
    studentList[student_id]["courses"].append(course_name)
    return "Course added successfully", 201

def coursesPut():
    # Retrieve JSON data from the request body
    data = request.get_json()
    # Extract student ID and new courses list
    student_id = data.get("id")
    new_courses = data.get("courses")

    # Check if student ID or new courses are missing
    if not student_id or not new_courses:
        return "Student ID or courses missing", 400

    # Check if the student exists in the student list
    if student_id not in studentList:
        return "Student not found", 404

    # Update the student's courses list with new courses
    studentList[student_id]["courses"] = new_courses
    return "Courses updated successfully", 200

def coursesDelete():
    # Retrieve JSON data from the request body
    data = request.get_json()
    # Extract student ID and course name from the data
    student_id = data.get("id")
    course_name = data.get("course")

    # Check if student ID or course name is missing
    if not student_id or not course_name:
        return "Student ID or course name missing", 400

    # Check if the student exists in the student list
    if student_id not in studentList:
        return "Student not found", 404

    # Retrieve the student's courses list
    courses = studentList[student_id]["courses"]
    # Check if the course exists in the student's courses
    if course_name not in courses:
        return "Course not found for the student", 404

    # Remove the course from the student's courses list
    courses.remove(course_name)
    return "Course removed successfully", 200

@app.route("/student", methods=["GET", "POST", "PUT", "DELETE"])
def student():
    if request.method == "GET":
        # Get all student IDs from Redis
        keys = r.keys("student:*")  # All keys with the prefix 'student:'
        
        students = []
        # Loop through all student keys and fetch their data from Redis
        for key in keys:
            student_data = r.get(key)  # Fetch student data from Redis
            if student_data:
                students.append(json.loads(student_data))  # Convert from JSON string to Python object

        # If no students are found, return a 404 error with a message
        if not students:
            return jsonify({"message": "No students found"}), 404

        # Return the list of students as JSON
        return jsonify({"students": students})

    elif request.method == "POST":
        # Ensure the request has content and it's valid JSON
        if not request.is_json:
            return jsonify({"message": "Invalid content type, must be JSON!"}), 400

        post_data = request.get_json()

        # Check if the data is empty or doesn't have the student ID or expected format
        if not post_data:
            return jsonify({"message": "Post content is missing!"}), 400

        # Check if the data contains a student ID and has valid fields
        student_id = list(post_data.keys())[0]  # Assuming one student is added at a time
        student_info = post_data.get(student_id)

        # Check if student info is valid and has name, major, and courses
        if not student_info or len(student_info) != 3:
            return jsonify({"message": "Invalid student data format!"}), 400
        
        name = student_info[0]
        major = student_info[1]
        courses = student_info[2].get("courses", [])

        # Store student data in Redis with student ID as the key
        student_data = {
            "name": name,
            "major": major,
            "courses": courses
        }

        # Save student data in Redis using student ID as the key
        r.set(f"student:{student_id}", json.dumps(student_data))

        # Return success message after adding the student
        return jsonify({"message": f"Student {student_id} added successfully!"}), 201

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

@app.route("/student/search", methods=["GET"])
def student_search():
    search_type = request.args.get("search_type")  # 'name', 'major', or 'course'
    search_value = request.args.get("search_value")

    if not search_value:
        return jsonify({"message": "Search value is missing!"}), 400

    students = []
    keys = r.keys("student:*")

    for key in keys:
        student_data = r.get(key)
        if student_data:
            student_info = json.loads(student_data)
            if search_type == "name" and search_value.lower() in student_info["name"].lower():
                students.append(student_info)
            elif search_type == "major" and search_value.lower() in student_info["major"].lower():
                students.append(student_info)
            elif search_type == "course" and search_value.lower() in [c.lower() for c in student_info["courses"]]:
                students.append(student_info)

    if not students:
        return jsonify({"message": "No students found matching the search criteria"}), 404

    return jsonify({"students": students})

@app.route("/")
def serve_frontend():
    return send_from_directory("static", "index.html")
# Run the Flask application in debug mode
if __name__ == "__main__":
    app.run(debug=True)
