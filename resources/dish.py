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
    parser.add_argument('type',
                        type=str,
                        required=True,
                        help="Type field can not be left blank")

    def get(self, dish_id):
        dish = DishModel.find_by_id(dish_id)

        if dish:
            return dish.json()
        return {'message': "Dish not found"}, 404

    # @jwt_required()  # Requires to identify before doing this step
    def post(self, dish_id):
        if DishModel.find_by_id(dish_id):
            return {'message': "A dish with id {} already exists".format(dish_id)}

        data = Dish.parser.parse_args()

        dish = DishModel(dish_id,data['name'], data['price'], data['type'])

        try:
            DishModel.insert()
        except:
            return {'message': "An error occurred inserting the item."}, 500
        return dish.json(), 201

    # @jwt_required()
    def delete(self, dish_id):
        connection = sqlite3.connect('marianos.db')
        cursor = connection.cursor()

        query = "DELETE FROM dishes WHERE id=?"
        cursor.execute(query, (dish_id,))

        connection.commit()
        connection.close()
        return {'message': "Item deleted"}, 202

    # @jwt_required()
    def put(self, dish_id):
        data = Dish.parser.parse_args()

        dish = DishModel.find_by_id(dish_id)
        updated_dish = DishModel(dish_id, data['name'], data['price'], data['type'])

        if dish is None:
            try:
                updated_dish.insert()
            except:
                return {'message': "An error occurred inserting the item."}, 500
        else:
            try:
                updated_dish.update()
            except:
                return {'message': "An error occurred updating the item."}, 500
        return updated_dish.json()


class DishList(Resource):
    def get(self):
        connection = sqlite3.connect('marianos.db')
        cursor = connection.cursor()

        query = "SELECT * FROM dishes"
        result = cursor.execute(query)
        dishes = []

        for dish in result:
            dishes.append({'dish id': dish[0], 'name': dish[1], 'price': dish[2], 'type': dish[3]})

        connection.close()
        return {'dishes': dishes}
