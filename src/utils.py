from flask import jsonify, url_for
import requests

class APIException(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)

def generate_sitemap(app):
    links = ['/admin/']
    for rule in app.url_map.iter_rules():
        # Filter out rules we can't navigate to in a browser
        # and rules that require parameters
        if "GET" in rule.methods and has_no_empty_params(rule):
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            if "/admin/" not in url:
                links.append(url)

    links_html = "".join(["<li><a href='" + y + "'>" + y + "</a></li>" for y in links])
    return """
        <div style="text-align: center;">
        <img style="max-height: 80px" src='https://ucarecdn.com/3a0e7d8b-25f3-4e2f-add2-016064b04075/rigobaby.jpg' />
        <h1>Rigo welcomes you to your API!!</h1>
        <p>API HOST: <script>document.write('<input style="padding: 5px; width: 300px" type="text" value="'+window.location.href+'" />');</script></p>
        <p>Start working on your proyect by following the <a href="https://github.com/4GeeksAcademy/flask-rest-hello/blob/master/docs/_QUICK_START.md" target="_blank">Quick Start</a></p>
        <p>Remember to specify a real endpoint path like: </p>
        <ul style="text-align: left;">"""+links_html+"</ul></div>"
        
def load_users(User, db):
    users = [
        {"email":"josecarrillo8@gmail.com", "password":"1234", "username":"jcarrillo"},
        {"email":"hangelous29@gmail.com", "password":"1234", "username":"hangelous"}
    ]

    for user in users:
        my_user = User.query.filter_by(email=user['email']).first()
        if my_user is None:
            new_user = User()
            new_user.email = user['email']
            new_user.password = user['password']
            new_user.username = user['username']
            db.session.add(new_user)
            db.session.commit()

def load_people(People, db):
    tb_people = People.query.all()
    
    if tb_people is None:
        res = requests.get('https://swapi.dev/api/people')
        data = res.json()
        
        for idx, people in enumerate(data['results'])):
            new_people = People()
            new_people.id = idx+1
            new_people.name = people['name']
            new_people.birth_year = people['birth_year']
            new_people.gender = people['gender']
            new_people.height = people['height']
            new_people.skin_color = people['skin_color']
            new_people.eye_color = people['eye_color']
            db.session.add(new_people)
            db.session.commit()
            
def load_planets(Planet, db):
    tb_planet = Planet.query.all()
    
    if tb_planet is None:
        res = requests.get('https://swapi.dev/api/planets')
        data = res.json()
        
        for idx, planet in enumerate(data['results']):
            # my_planet = Planet.query.filter_by(id=idx+1).first()
            # if my_planet is None:
            new_planet = Planet()
            new_planet.id = idx+1
            new_planet.name = planet['name']
            new_planet.climate = planet['climate']
            new_planet.population = planet['population']
            new_planet.orbital_period = planet['orbital_period']
            new_planet.rotation_period = planet['rotation_period']
            new_planet.diameter = planet['diameter']
            db.session.add(new_planet)
            db.session.commit()       
