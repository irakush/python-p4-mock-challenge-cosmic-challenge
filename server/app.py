#!/usr/bin/env python3

from models import db, Scientist, Mission, Planet
from flask_restful import Api, Resource
from flask_migrate import Migrate
from flask import Flask, make_response, jsonify, request
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)


@app.route('/')
def home():
    return ''

class Scientists(Resource):
    def get(self):

        # rules = ("-missions", ) Exclude missions from the object
        scientists = [scientist.to_dict(rules = ("-missions", )) for scientist in Scientist.query.all()]

        return make_response(scientists, 200)
    
api.add_resource(Scientists, "/scientistss") #route

@app.route('/scientists' , methods=['GET', 'POST'])
def scientistst():

    if request.method == 'GET':
        scientists = []  # array to store a dictionary for each scientist
        for scientist in Scientist.query.all():
            scientists.append(scientist.to_dict(rules=("-missions", )))
        # body = {"count": len(scientists), "scientists": scientists}
            body = scientists
        return make_response(body, 200)
    

    elif request.method == 'POST':
        try:
            # print(':::::||:: ', request)
            # [print(i) for i in dir(request.form)]
            # print('::::: ', request.form.get("name"))
            # print('::::: ', request.form.get("field_of_study"))

            form_data = request.get_json()
            # print(form_data)
            # print(form_data['name'])

            new_scientist_obj = Scientist(
                name=form_data['name'], 
                field_of_study=form_data['field_of_study']
                )
            
            db.session.add(new_scientist_obj)
            db.session.commit()

            response = make_response(new_scientist_obj.to_dict(), 201)

            # new_scientist = Scientist(
            #     name=request.form.get("name"),
            #     field_of_study=request.form.get("field_of_study"),
            # )

            # db.session.add(new_scientist)
            # db.session.commit()

            # scientist_dict = new_scientist.to_dict()

            # response = make_response(
            #     scientist_dict,
            #     201
            # )

            # response = make_response(
            #     {},
            #     201
            # )
        except ValueError:
            response = make_response({
                "errors": ["validation errors"]
                }, 400)
    

        return response

@app.route('/scientists/<int:id>', methods = ['GET', 'DELETE', 'PATCH'])
def get_sientist_by_id(id):
    scientist = Scientist.query.filter(Scientist.id == id).first()

    if scientist:
        if request.method == 'GET':
            body = scientist.to_dict()
            status = 200

            response = make_response(body, status)
        elif request.method == 'DELETE':
            assoc_missions = Mission.query.filter(Mission.scientist_id == id).all()

            for assoc_mission in assoc_missions:
                db.session.delete(assoc_mission)

            db.session.delete(scientist)
            db.session.commit()

            response = make_response({}, 204)
        elif request.method == 'PATCH':
            try:
                form_data = request.get_json()

                for attr in form_data:
                    setattr(scientist, attr, form_data[attr])

                db.session.commit()

                response = make_response(
                    scientist.to_dict(),
                    202
                )
            except ValueError:
                response = make_response(
                    {"errors": ["validation errors"]}, 
                    400
                    )
    else:
        response = make_response(
            {"error": "Scientist not found"}, 
            404
            )

    return response

# @app.route('/scientists')

# --------------------- PLANETS ---------------------------

@app.route('/planets', methods=['GET'])
def planets():
    planets = [planet.to_dict(rules = ("-missions", )) for planet in Planet.query.all()]
     
    return make_response(planets, 200)

# --------------------- MISSIONS ---------------------------
@app.route('/missions', methods = ['POST'])
def missions():
    try:
        form_data = request.get_json()
        # print(form_data)
        # print(form_data['name'])

        new_mission_obj = Mission(
            name=form_data['name'], 
            scientist_id=form_data['scientist_id'],
            planet_id=form_data['planet_id']
            )
        
        db.session.add(new_mission_obj)
        db.session.commit()

        response = make_response(new_mission_obj.to_dict(), 201)
    except ValueError:
        response = make_response({"errors": ["validation errors"]}, 400)

    return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)
