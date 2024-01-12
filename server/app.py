from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=['GET', 'POST'])
def messages():
    if request.method == 'GET':
        chatter_messages = [message.to_dict() for message in Message.query.order_by('created_at').all()]

        return make_response(jsonify(chatter_messages), 200)
    
    elif request.method == 'POST':
        data = request.get_json()
        new_message = Message(
            body=data['body'],
            username=data['username']
        )
        db.session.add(new_message)
        db.session.commit()

        return make_response(jsonify(new_message.to_dict()), 201)

@app.route('/messages/<int:id>', methods=['PATCH', 'DELETE'])
def messages_by_id(id):
    message_by_id = Message.query.filter_by(id=id).first()
    
    if request.method == 'PATCH':
        data = request.get_json()
        for attr in data:
            setattr(message_by_id, attr, data[attr])

        db.session.add(message_by_id)
        db.session.commit()

        return make_response(message_by_id.to_dict(), 200)
    
    elif request.method == 'DELETE':
        db.session.delete(message_by_id)
        db.session.commit()

        response_body={
            'message':'Message deleted.'
        }

        return make_response(response_body, 200)

if __name__ == '__main__':
    app.run(port=8000,debug=True)
