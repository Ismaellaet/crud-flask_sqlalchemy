import json
from flask import Flask, Response, request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite'

db = SQLAlchemy(app)
api = Api(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email
        }


class UsersResource(Resource):
    def get(self):
        users = User.query.all()
        users_list = [user.to_json() for user in users]
        return make_response(200, 'users', users_list)


def make_response(status, content_name, content, message=None):
    body = {}
    body[content_name] = content

    if message:
        body['message'] = message

    return Response(json.dumps(body), status=status, mimetype='application/json')


api.add_resource(UsersResource, '/users')

if __name__ == '__main__':
    app.run(debug=True)
