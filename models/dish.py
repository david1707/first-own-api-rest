import sqlite3


class DishModel:
    def __init__(self, dish_id, name, price, type):
        self.dish_id = dish_id
        self.name = name
        self.price = price
        self.type = type

    def json(self):
        return {'dish_id': self.dish_id, 'name': self.name, 'price': self.price, 'type': self.type}

    @classmethod
    def find_by_id(cls, dish_id):
        connection = sqlite3.connect('marianos.db')
        cursor = connection.cursor()

        query = "SELECT * FROM dishes WHERE id=?"
        row = cursor.execute(query, (dish_id,)).fetchone()

        connection.close()
        if row:
            return cls(*row)

    def insert(self, dish):
        connection = sqlite3.connect('marianos.db')
        cursor = connection.cursor()

        query = "INSERT INTO dishes VALUES (?, ?, ?, ?)"
        cursor.execute(query, (self.dish_id, self.name, self.price, self.type))

        connection.commit()
        connection.close()

    def update(self, dish):
        connection = sqlite3.connect('marianos.db')
        cursor = connection.cursor()

        query = "UPDATE dishes SET name=?, price=?, type=? WHERE id=?"
        cursor.execute(query, (self.name, self.price, self.type, self.dish_id))

        connection.commit()
        connection.close()
