from flask import Flask

todoList = { "monday": ["Buy groceries", "Clean the house"] }

app = Flask(__name__)

@app.route("/todos", methods=["GET"])
def getlist():
  return todoList

@app.route("/todos", methods=["POST"])
def create():
    return "Create a new todo item"
  

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=8000)
