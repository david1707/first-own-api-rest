from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from config_file import secret_key as secret_key

from resources.user import UserRegister
from resources.dish import Dish, DishList

app = Flask(__name__)
app.secret_key = secret_key  # Define your own 'secret_key' at config_file.py
api = Api(app)

jwt = JWT(app, authenticate, identity)  # /auth endpoint to authenticate

api.add_resource(Dish, '/dish/id/<int:dish_id>')
api.add_resource(DishList, '/dishes')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
