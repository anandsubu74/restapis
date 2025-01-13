import json
from flask import Flask, request

todoList = {}

app = Flask(__name__)

@app.route("/todos", methods=["GET","POST", "PUT"])
def todos():
  if request.method == "GET":
    return todoList
  elif request.method == "POST":
    data = request.get_json()
    todoList.update(data)
    print(str(data))
    return "Success",200
  elif request.method == "PUT":
    data = request.get_json()
    todoList.update(data)
    print(str(data))
    return "Updated Successfully", 200
  return 400
  

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=8000)
