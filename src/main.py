"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""

import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Planet, Favorite

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app) ## inicializo mi base de datos con mi app (db = SQLAlchemy(app))
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET', 'POST'])
def handle_user_all():
    body = request.get_json()

    if request.method == 'POST':
        if body is None:
            return "The request body is null", 400
        if 'username' not in body:
            return 'You need to specify the username', 400
            # raise APIException('You need to specify the username', status_code=400)
        if 'password' not in body:
            return 'You need to specify the password', 400
        if 'email' not in body:
            return 'You need to specify the email', 400
            # raise APIException('You need to specify the email', status_code=400)
        
        user = User()
        user.email = body.email #body['email']
        user.password = body.password #body['password']
        user.username = body.username #body['username']
        
        db.session.add(user)
        db.session.commit()
        return "ok", 200
        # response_body = { "msg": "PURA VIDA" }
        # return jsonify(response_body), 200
    if request.method == 'GET':
        user_query = User.query.all()
        all_user = list(map(lambda x: x.serialize(), user_query))
        
        return jsonify(all_user), 200
    
    return "Invalid Method", 404

# @app.route('/user/<int:user_id>', methods=['GET', 'PUT', 'DELETE'])
# def handle_user_id():
#     user = User.query.get(user_id)
#     if user is not None:
#         if request.method == 'PUT':
#             if 'username' in body:
#                 user.username = body["username"]
#             if 'email' in body:
#                 user.email = body["email"]
#             if 'password' in body:
#                 user.password = body['password']
#             db.session.commit()
#             response_body = { "msg": "Success: User Update" }
#             return jsonify(response_body), 200
#         if request.method == 'DELETE':
#             db.session.delete(user)
#             db.session.commit()
#             response_body = { "msg": "Success: User Delete" }
#             return jsonify(response_body), 200
#             return "ok", 200
#         if request.method == 'GET':
#             return jsonify(user), 200
#     else:
#         raise APIException('User not found', status_code=404)

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
