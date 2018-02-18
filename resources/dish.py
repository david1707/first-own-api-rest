import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.dish import DishModel


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
    parser.add_argument('dish_type',
                        type=str,
                        required=True,
                        help="Type field can not be left blank")

    @jwt_required()  # Requires to identify before doing this step
    def get(self, dish_id):
        dish = DishModel.find_by_id(dish_id)

        if dish:
            return dish.json()
        return {'message': "Dish not found"}, 404

    # @jwt_required()
    def post(self, dish_id):
        if DishModel.find_by_id(dish_id):
            return {'message': "A dish with id {} already exists".format(dish_id)}

        data = Dish.parser.parse_args()
        dish = DishModel(dish_id, **data)

        try:
            dish.save_to_db()

        except:
            return {'message': "An error occurred inserting the item."}, 500
        return dish.json(), 201

    @jwt_required()
    def delete(self, dish_id):
        dish = DishModel.find_by_id(dish_id)

        if dish:
            dish.delete_from_db()
            return {'message': 'Item deleted'}

    @jwt_required()
    def put(self, dish_id):
        data = Dish.parser.parse_args()
        dish = DishModel.find_by_id(dish_id)

        if dish is None:
            dish = DishModel(dish_id, **data)
        else:
            dish.name = data['name']
            dish.price = data['price']
            dish.dish_type = data['dish_type']

        dish.save_to_db()
        return dish.json()


class DishList(Resource):
    def get(self):
        return {'items': [dish.json() for dish in DishModel.query.all()]}
