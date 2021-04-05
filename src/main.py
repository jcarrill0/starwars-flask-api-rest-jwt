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
        if 'password' not in body:
            return 'You need to specify the password', 400
        if 'email' not in body:
            return 'You need to specify the email', 400

        user = User()
        user.email = body['email']
        user.password = body['password']
        user.username = body['username']
        db.session.add(user)
        db.session.commit()
        return "ok", 200
    if request.method == 'GET':
        all_user = list(map(lambda x: x.serialize(), User.query.all()))
        # all_user = [ user.serialize() for user in User.query.all() ] 
        if len(all_user) > 0:
            return jsonify(all_user), 200
        else:
            return  jsonify({ "msg": "No existing Users" }), 200     
    
    return "Invalid Method", 404

@app.route('/user/<int:user_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_user_id(user_id):
    user = User.query.get(user_id) # User.query.filter_by(id=user_id).first()
    if user is not None:
        if request.method == 'PUT':
            body = request.get_json()
            if 'username' in body:
                user.username = body["username"]
            if 'email' in body:
                user.email = body["email"]
            if 'password' in body:
                user.password = body['password']
            db.session.commit()
            return jsonify({ "msg": "Success: User Update" }), 200
        if request.method == 'DELETE':
            db.session.delete(user)
            db.session.commit()
            return jsonify({ "msg": "Success: User Delete" }), 200
        if request.method == 'GET':
            return jsonify(user.serialize()), 200   
    else:
        raise APIException('User does not exist', status_code=404)

@app.route('/people', methods=['GET', 'POST'])
def handle_people_all():
    body = request.get_json()

    if request.method == 'POST':
        if body is None:
            return "The request body is null", 400
        if 'name' not in body:
            return 'You need to specify the name', 400
        if 'birth_year' not in body:
            return 'You need to specify the birth_year', 400
        if 'gender' not in body:
            return 'You need to specify the gender', 400
        if 'height' not in body:
            return 'You need to specify the height', 400
        if 'skin_color' not in body:
            return 'You need to specify the skin_color', 400
        if 'eye_color' not in body:
            return 'You need to specify the eye_color', 400

        people = People()
        people.name = body['name']
        people.birth_year = body['birth_year']
        people.gender = body['gender']
        people.height = body['height']
        people.skin_color = body['skin_color']
        people.eye_color = body['eye_color']
        db.session.add(people)
        db.session.commit()
        return "ok", 200
    if request.method == 'GET':
        all_people = list(map(lambda x: x.serialize(), People.query.all()))
        # all_people = [ people.serialize() for people in People.query.all() ] 
        if len(all_people) > 0:
            return jsonify(all_people), 200
        else:
            return  jsonify({ "msg": "No existing Peoples" }), 200     
    
    return "Invalid Method", 404


@app.route('/people/<int:people_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_people_id(people_id):
    people = People.query.get(people_id) # People.query.filter_by(id=people_id).first()
    if user is not None:
        if request.method == 'PUT':
            body = request.get_json()
            if 'name' in body:
                people.name = body['name']
            if 'birth_year' in body:
                people.birth_year = body['birth_year']
            if 'gender' in body:
                people.gender = body['gender']
            if 'height' in body:
                people.height = body['height']
            if 'skin_color' in body:
                people.skin_color = body['skin_color']
            if 'eye_color' in body:
                people.eye_color = body['eye_color']
            db.session.commit()
            return jsonify({ "msg": "Success: People Update" }), 200
        if request.method == 'DELETE':
            db.session.delete(people)
            db.session.commit()
            return jsonify({ "msg": "Success: People Delete" }), 200
        if request.method == 'GET':
            return jsonify(people.serialize()), 200   
    else:
        raise APIException('People does not exist', status_code=404)

@app.route('/planet', methods=['GET', 'POST'])

@app.route('/planet/<int:planeta_id>', methods=['GET', 'PUT', 'DELETE'])

@app.route('/favorite', methods=['GET', 'POST'])

@app.route('/favorite/<int:favorite_id>', methods=['GET', 'PUT', 'DELETE'])




# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
