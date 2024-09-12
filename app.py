from flask import Flask, jsonify, request, abort, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Sample data structure
ar = [
    {"id": 1, "name": "betty", "age": 20},
    {"id": 2, "name": "alex", "age": 21},
    {"id": 3, "name": "shadi", "age": 15}
]

# Helper function to find the next available ID
def get_next_id():
    return max(item['id'] for item in ar) + 1 if ar else 1

# Home route to render the front-end
@app.route('/')
def home():
    return render_template('index.html')

# READ: Get all items
@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(ar), 200

# READ: Get a specific item by ID
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = next((item for item in ar if item['id'] == user_id), None)
    if user is None:
        abort(404, "User not found")
    return jsonify(user), 200

# CREATE: Add a new item
@app.route('/users', methods=['POST'])
def add_user():
    if not request.json or not 'name' in request.json or not 'age' in request.json:
        abort(400, "Bad request: 'name' and 'age' are required")
    new_user = {
        "id": get_next_id(),
        "name": request.json['name'],
        "age": request.json['age']
    }
    ar.append(new_user)
    return jsonify(new_user), 201

# UPDATE: Update an existing item by ID
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = next((item for item in ar if item['id'] == user_id), None)
    if user is None:
        abort(404, "User not found")
    if not request.json:
        abort(400, "Bad request: Request body must be JSON")
    if 'name' in request.json and type(request.json['name']) is not str:
        abort(400, "Bad request: 'name' must be a string")
    if 'age' in request.json and type(request.json['age']) is not int:
        abort(400, "Bad request: 'age' must be an integer")

    user['name'] = request.json.get('name', user['name'])
    user['age'] = request.json.get('age', user['age'])
    return jsonify(user), 200

# DELETE: Delete an item by ID
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = next((item for item in ar if item['id'] == user_id), None)
    if user is None:
        abort(404, "User not found")
    ar.remove(user)
    return '', 204

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
