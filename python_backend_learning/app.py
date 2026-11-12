from flask import Flask, request, jsonify
import json
from datetime import datetime

app = Flask(__name__)

# In-memory storage (in real apps, use a database)
tasks = [
    {"id": 1, "title": "Learn Python", "completed": False, "created_at": "2026-01-01"}
]

# GET all tasks
@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks)

# GET a single task by ID
@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = next((t for t in tasks if t['id'] == task_id), None)
    if not task:
        return jsonify({"error": "Task not found"}), 404
    return jsonify(task)

# POST - create a new task
@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()

    # Validate input
    if not data or 'title' not in data:
        return jsonify({"error": "Title is required"}), 400

    # Create new task
    new_task = {
        "id": max([t['id'] for t in tasks]) + 1 if tasks else 1,
        "title": data['title'],
        "completed": False,
        "created_at": datetime.now().isoformat()
    }

    tasks.append(new_task)
    return jsonify(new_task), 201

# PUT - update a task
@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = next((t for t in tasks if t['id'] == task_id), None)
    if not task:
        return jsonify({"error": "Task not found"}), 404

    data = request.get_json()
    task['title'] = data.get('title', task['title'])
    task['completed'] = data.get('completed', task['completed'])

    return jsonify(task)

# DELETE a task
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    global tasks
    task = next((t for t in tasks if t['id'] == task_id), None)
    if not task:
        return jsonify({"error": "Task not found"}), 404

    tasks = [t for t in tasks if t['id'] != task_id]
    return jsonify({"message": "Task deleted"})

# Health check endpoint
@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
