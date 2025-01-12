from flask import Flask, request

todoList = { "monday": ["Buy groceries", "Clean the house"] }

app = Flask(__name__)

@app.route("/todos", methods=["GET","POST"])
def todos():
  if request.method == "GET":
    return todoList
  elif request.method == "POST":
    data = request.get_json()
    print(str(data))
    return "",200
  return 400
  

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=8000)
