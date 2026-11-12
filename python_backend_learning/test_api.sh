#!/bin/bash

# Simple API Testing Examples
# Run these after starting the Flask app with: python app.py

BASE_URL="http://localhost:5000"

echo "=== Testing Flask Task API ==="

echo -e "\n1. GET all tasks"
curl -X GET $BASE_URL/tasks | python -m json.tool

echo -e "\n2. GET a single task (ID 1)"
curl -X GET $BASE_URL/tasks/1 | python -m json.tool

echo -e "\n3. POST - Create a new task"
curl -X POST $BASE_URL/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Learn Flask"}' | python -m json.tool

echo -e "\n4. PUT - Update a task"
curl -X PUT $BASE_URL/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"title": "Learn Python Backend", "completed": true}' | python -m json.tool

echo -e "\n5. DELETE - Remove a task"
curl -X DELETE $BASE_URL/tasks/2 | python -m json.tool

echo -e "\n6. Health check"
curl -X GET $BASE_URL/health | python -m json.tool
