from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import safe_str_cmp  
import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), nullable=False)
    password = db.Column(db.Text, unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=True)    
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())
    favorites = db.relationship("Favorite", backref="user", uselist=False, lazy="select")

    def __repr__(self):
        return '<User %r>' % self.username
        # return f'<User {self.name}>'

    def check_password(self, password):
        return safe_str_cmp(password, self.password)
    
    def serialize(self):
        return {
            "id": self.id,
            "username" : self.username,
            "email": self.email,
            "create" : self.created_at
        }

class People(db.Model):
    idx = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.Integer, unique=True, nullable=False)
    name = db.Column(db.String(80), unique=True, nullable=False)
    birth_year = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(50), nullable=False)
    height = db.Column(db.Integer, nullable=False)
    skin_color = db.Column(db.String(50), nullable=False)
    eye_color = db.Column(db.String(50), nullable=False)
    favorites = db.relationship('Favorite', backref='people', lazy=True)

    def __repr__(self):
        return '<People %r>' % self.name
        # return f'<People {self.name}>'

    def serialize(self):
        return {
            "id": self.id,
            "name" : self. name,
            "birth_year" : self.birth_year,
            "gender" : self.gender,
            "height" : self.height,
            "skin_color" : self.skin_color,
            "eye_color" : self.eye_color
            # "favorites" : list(map(lambda x: x.serialize(), self.favorites))
                    
        }

class Planet(db.Model):
    idx = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.Integer, unique=True, nullable=False)
    name = db.Column(db.String(80), nullable=False)
    climate = db.Column(db.String(50), nullable=False)
    population = db.Column(db.String(20), nullable=False)
    orbital_period = db.Column(db.Integer, nullable=False)
    rotation_period = db.Column(db.Integer, nullable=False)
    diameter = db.Column(db.Integer, nullable=False)
    favorites = db.relationship('Favorite', backref='planet', lazy=True)

    def __repr__(self):
        return '<Planet %r>' % self.name
        # return f'<Planet {self.name}>'

    def serialize(self):
        return {
            "id": self.id,
            "name" : self.name,
            "climate" : self.climate,
            "population" : self.population,
            "orbital_period" : self.orbital_period,
            "rotation_period" : self.rotation_period,
            "diameter" : self.diameter
            # "favorites" : list(map(lambda x: x.serialize(), self.favorites))
        }

class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    people_id = db.Column(db.Integer, db.ForeignKey('people.id'))
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'))

    # def __repr__(self):
    #     return '<Favorite %r>' % self.username
    #     return f'<Favorite {self.name}>'

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "people_id":self.people_id,
            "planet_id":self.planet_id
        }