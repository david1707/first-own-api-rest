from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

from security import authenticate, identity
from config_file import secret_key as secret_key

app = Flask(__name__)
app.secret_key = secret_key  # Define your own 'secret_key' at config_file.py
api = Api(app)

jwt = JWT(app, authenticate, identity)  # /auth endpoint to authenticate

dishes = []


class Dish(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        type=str,
                        required=True,
                        help="Name field can not be left blank")
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="Price field can not be left blank")
    parser.add_argument('type',
                        type=str,
                        required=True,
                        help="Type field can not be left blank")

    def get(self, dish_id):
        dish = [dish for dish in dishes if dish['dish_id'] == dish_id]
        if dish:
            return dish, 200
        return {'message': "Dish not found"}, 404

    @jwt_required()  # Requires to identify before doing this step
    def post(self, dish_id):
        data = Dish.parser.parse_args()

        dish = {'dish_id': dish_id, 'name': data['name'], "price": data['price'], "type": data['type']}
        dishes.append(dish)
        return dish, 201

    @jwt_required()
    def delete(self, dish_id):
        global dishes
        dishes = list(filter(lambda x: x['dish_id'] != dish_id, dishes))
        return {'message': "Item deleted"}, 202

    @jwt_required()
    def put(self, dish_id):
        data = Dish.parser.parse_args()

        dish = next(filter(lambda x: x['dish_id'] == dish_id, dishes), None)
        if dish is None:
            dish = {'dish_id': dish_id, 'name': data['name'], "price": data['price'], "type": data['type']}
            dishes.append(dish)
        else:
            dish.update(data)

        return dish


class DishList(Resource):
    def get(self):
        return {'dishes': dishes}


api.add_resource(Dish, '/dish/id/<int:dish_id>')
api.add_resource(DishList, '/dishes')


if __name__ == '__main__':
    app.run(debug=True, port=5000)
