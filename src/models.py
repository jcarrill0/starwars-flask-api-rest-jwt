from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(500), nullable=False)
    favorites = db.relationship('Favorite', backref="user", uselist=False, lazy="select")

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "username" : self.username,
            "email": self.email,
            "password" : self.password,
        }

class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True nullable=False)
    birth_year = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(100), nullable=False)
    height = db.Column(db.Integer, nullable=False)
    skin_color = db.Column(db.String(100), nullable=False)
    eye_color = Column(db.String(100), nullable=False)
    favorites = relationship('favorite')

    def __repr__(self):
        return '<People %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name" : self. name,
            "birth_year" : self.birth_year,
            "gender" : self.gender,
            "height" : self.height,
            "skin_color" : self.skin_color,
            "eye_color" : self.eye_color
                    
        }

class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    climate = db.Column(db.String(100), nullable=False)
    population = db.Column(db.Integer, nullable=False)
    orbital_period = db.Column(db.Integer), nullable=False
    rotation_period = db.Column(db.Integer, nullable=False)
    diamater = Column(db.Integer, nullable=False)
    favorites = relationship('favorite')

    def __repr__(self):
        return '<Planet %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name" : self.name,
            "climate" : self.climate,
            "population" : self.population,
            "orbital_period" : self.orbital_period,
            "rotation_period" : self.rotation_period,
            "diamater" : self.diamater
        }

class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('user.id'))
    people_id = db.Column(db.Integer, ForeignKey('people.id'))
    planet_id = db.Column(db.Integer, ForeignKey('planet.id'))

    # def __repr__(self):
    #     return '<Favorite %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "people_id":self.people_id,
            "planet_id":self.planet_id
        }