from flask import Flask

todoList = {}

app = Flask(__name__)

@app.route("/todos", methods=["GET"])
def getlist():
  return todoList
  r

@app.route("/todos", methods=["POST"])
def create():
    return "Create a new todo item"
  

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=8000)
