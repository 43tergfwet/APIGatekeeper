from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class ExampleModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(255), nullable=False)

    def __init__(self, content):
        self.content = content

@app.route('/api/items', methods=['GET', 'POST'])
def manage_items():
    if request.method == 'GET':
        items = ExampleModel.query.all()
        return jsonify([{'id': item.id, 'content': item.content} for item in items])
    
    elif request.method == 'POST':
        content_data = request.json
        if not content_data or 'content' not in content_data:
            return jsonify({'error': 'Bad request', 'message': 'Content field is missing'}), 400
        content = content_data['content']
        new_item = ExampleModel(content)
        db.session.add(new_item)
        db.session.commit()
        return jsonify({'message': 'New item added successfully!', 'id': new_item.id, 'content': new_item.content}), 201

@app.route('/api/items/<int:item_id>', methods=['GET', 'PUT', 'DELETE'])
def manage_item_by_id(item_id):
    item = ExampleModel.query.get(item_id)
    
    if not item:
        return jsonify({'error': 'Not found', 'message': f'Item with id {item_id} not found'}), 404

    if request.method == 'GET':
        return jsonify({'id': item.id, 'content': item.content})

    elif request.method == 'PUT':
        content_data = request.json
        if not content_data or 'content' not in content_data:
            return jsonify({'error': 'Bad request', 'message': 'Content field is missing or invalid'}), 400
        item.content = content_data['content']
        db.session.commit()
        return jsonify({'message': 'Item updated successfully!', 'id': item.id, 'content': item.content})

    elif request.method == 'DELETE':
        db.session.delete(item)
        db.session.commit()
        return jsonify({'message': 'Item deleted successfully!'})

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({'error': 'Method not allowed', 'message': 'This method is not allowed for the requested URL'}), 405

@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({'error': 'Internal server error', 'message': "It's not you, it's us. We are looking into it."}), 500

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)