# pip install -r requirements.txt
# http POST http://localhost:5000/tasks title="Aprender Flask" description="Estudar a criação de APIs"
from flask import Flask
from flask import request, jsonify

app = Flask(__name__)

'''
# exemplo de ja ter uma lista de tarefas já pre definida
tasks = [
    {
        "title": "Aprender Flask e APIs 11111111",
        "description": "Aprofundar nos conceitos 1111111111",
        "id": 1,
        "completed": True
    },
    {
        "title": "Aprender Flask e APIs 222222222",
        "description": "Aprofundar nos conceitos 222222222",
        "id": 2,
        "completed": True
    },
    {
        "title": "Aprender Flask e APIs 333333333333",
        "description": "Aprofundar nos conceitos 3333333333",
        "id": 3,
        "completed": False
    },
]  
'''

tasks = []# Lista para armazenar as tarefas
task_id_control = 1  # Controlador de IDs para garantir unicidade

#página principal
@app.route("/")
def hello():
    return "Hello, World!"

#adicionar 1 na lista (CREATE)
@app.route("/tasks", methods=["POST"])
def create_task():
    global task_id_control
    data = request.get_json()  # Pega os dados enviados no corpo da requisição
    new_task = {
        "id": task_id_control,
        "title": data.get("title"),  # Obtém o título enviado
        "description": data.get("description", ""),  # Descrição opcional
        "completed": False  # Define que a tarefa começa como incompleta
    }
    tasks.append(new_task)  # Adiciona a nova tarefa à lista
    task_id_control += 1  # Incrementa o ID para a próxima tarefa
    return jsonify({"message": "Tarefa criada com sucesso!", "task": new_task}), 201

#lista todos (READ)
@app.route("/tasks", methods=["GET"])
def get_tasks():
    return jsonify({"tasks": tasks, "total": len(tasks)})

#lista um item pelo ID (READ)
@app.route("/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    task = next((t for t in tasks if t["id"] == task_id), None)
    if not task:
        return jsonify({"message":"Tarefa não encontrada"}), 404
    return jsonify(task)

#atualiza um item pelo ID (UPDATE)
@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    task = next((t for t in tasks if t["id"] == task_id), None)
    if not task:
        return jsonify({"message": "Tarefa não encontrada"}), 404
    
    data = request.get_json()
    task["title"] = data.get("title", task["title"])
    task["description"] = data.get("description", task["description"])
    task["completed"] = data.get("completed", task["completed"])
    return jsonify({"message": "Tarefa atualizada com sucesso!", "task": task})

@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    global tasks
    task = next ((t for t in tasks if t["id"] == task_id), None)
    if not task:
        return jsonify({"message": "Tarefa não encontrada"}), 404
    tasks = [t for t in tasks if t["id"] != task_id]
    return jsonify({"message": "Tarefa deletada com sucesso!"})

if __name__ == "__main__":
    app.run(debug=True)