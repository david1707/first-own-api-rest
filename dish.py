import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required


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
        dish = self.find_by_id(dish_id)

        if dish:
            return dish
        return {'message': "Dish not found"}, 404

    # @jwt_required()  # Requires to identify before doing this step
    def post(self, dish_id):
        if self.find_by_id(dish_id):
            return {'message': "A dish with id {} already exists".format(dish_id)}

        data = Dish.parser.parse_args()

        dish = {'dish_id': dish_id, 'name': data['name'], "price": data['price'], "type": data['type']}

        try:
            self.insert(dish)
        except:
            return {'message': "An error occurred inserting the item."}, 500
        return dish, 201

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

        dish = self.find_by_id(dish_id)
        updated_dish = {'dish_id': dish_id, 'name': data['name'], "price": data['price'], "type": data['type']}

        if dish is None:
            try:
                self.insert(updated_dish)
            except:
                return {'message': "An error occurred inserting the item."}, 500
        else:
            try:
                self.update(updated_dish)
            except:
                return {'message': "An error occurred updating the item."}, 500
        return updated_dish

    @classmethod
    def find_by_id(cls, dish_id):
        connection = sqlite3.connect('marianos.db')
        cursor = connection.cursor()

        query = "SELECT * FROM dishes WHERE id=?"
        row = cursor.execute(query, (dish_id,)).fetchone()

        connection.close()
        if row:
            return {'item': {'dish id': row[0], 'name': row[1], 'price': row[2], 'type': row[3]}}

    @classmethod
    def insert(cls, dish):
        connection = sqlite3.connect('marianos.db')
        cursor = connection.cursor()

        query = "INSERT INTO dishes VALUES (?, ?, ?, ?)"
        cursor.execute(query, (dish['dish_id'], dish['name'], dish['price'], dish['type']))

        connection.commit()
        connection.close()

    @classmethod
    def update(cls, dish):
        connection = sqlite3.connect('marianos.db')
        cursor = connection.cursor()

        query = "UPDATE dishes SET name=?, price=?, type=? WHERE id=?"
        cursor.execute(query, (dish['name'], dish['price'], dish['type'], dish['dish_id']))

        connection.commit()
        connection.close()


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
