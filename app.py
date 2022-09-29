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

    def post(self):
        req = request.get_json()

        try:
            new_user = User(name=req['name'], email=req['email'])
            db.session.add(new_user)
            db.session.commit()
            return make_response(201, 'user', new_user.to_json(), 'User created successfully!')
        except Exception as e:
            print(e)
            return make_response(400, 'user', {}, 'Error creating user!')


class UserResource(Resource):
    def get(self, user_id):
        user = User.query.get_or_404(user_id)
        user_json = user.to_json()
        return make_response(200, 'user', user_json)

    def put(self, user_id):
        user = User.query.filter_by(id=user_id).first()
        req = request.get_json()

        try:
            for attr, value in req.items():
                setattr(user, attr, value)

            db.session.add(user)
            db.session.commit()
            return make_response(200, 'user', user.to_json(), 'User successfully updated!')
        except Exception as e:
            print(e)
            return make_response(400, 'user', {}, 'User update error!')


def make_response(status, content_name, content, message=None):
    body = {}
    body[content_name] = content

    if message:
        body['message'] = message

    return Response(json.dumps(body), status=status, mimetype='application/json')


api.add_resource(UsersResource, '/users')
api.add_resource(UserResource, '/user/<int:user_id>')

if __name__ == '__main__':
    app.run(debug=True)
