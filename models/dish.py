import sqlite3
from db import db


class DishModel(db.Model):
    # SQLAlchemy modeling
    __tablename__ = 'dishes'
    dish_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))
    dish_type = db.Column(db.String(80))

    def __init__(self, dish_id, name, price, dish_type):
        self.dish_id = dish_id
        self.name = name
        self.price = price
        self.dish_type = dish_type

    def json(self):
        return {'dish_id': self.dish_id, 'name': self.name, 'price': self.price, 'type': self.dish_type}

    @classmethod
    def find_by_id(cls, dish_id):
        return cls.query.filter_by(dish_id=dish_id).first()  # SELECT * FROM dishes WHERE dish_id = dish_id LIMIT 1

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
