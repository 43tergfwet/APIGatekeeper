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
        content = request.json['content']
        new_item = ExampleModel(content)
        db.session.add(new_item)
        db.session.commit()
        return jsonify({'message': 'New item added successfully!', 'id': new_item.id, 'content': new_item.content}), 201

@app.route('/api/items/<int:item_id>', methods=['GET', 'PUT', 'DELETE'])
def manage_item_by_id(item_id):
    item = ExampleModel.query.get_or_404(item_id)

    if request.method == 'GET':
        return jsonify({'id': item.id, 'content': item.content})

    elif request.method == 'PUT':
        item.content = request.json['content']
        db.session.commit()
        return jsonify({'message': 'Item updated successfully!', 'id': item.id, 'content': item.content})

    elif request.method == 'DELETE':
        db.session.delete(item)
        db.session.commit()
        return jsonify({'message': 'Item deleted successfully!'})

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)