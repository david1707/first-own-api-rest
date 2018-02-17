import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel


class UserRegister(Resource):
    parse = reqparse.RequestParser()
    parse.add_argument('username',
                       type=str,
                       required=True,
                       help="Name field can not be left blank")
    parse.add_argument('password',
                       type=str,
                       required=True,
                       help="Name field can not be left blank")

    def post(self):
        data = UserRegister.parse.parse_args()

        if UserModel.find_by_username(data['username']):
            return {'message': "A user with that username already exists"}, 400

        connection = sqlite3.connect('marianos.db')
        cursor = connection.cursor()

        query = "INSERT INTO users VALUES (NULL, ?, ?)"
        cursor.execute(query, (data['username'], data['password']))

        connection.commit()
        connection.close()
