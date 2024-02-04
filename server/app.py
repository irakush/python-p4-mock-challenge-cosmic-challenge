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
            scientists.append(scientist.to_dict())
        body = {"count": len(scientists), "scientists": scientists}
        return make_response(body, 200)
    

    elif request.method == 'POST':
        print('::::: ', request.form.get("name"))
        print('::::: ', request.form.get("field_of_study"))

        new_scientist = Scientist(
            name=request.form.get("name"),
            field_of_study=request.form.get("field_of_study"),
        )

        db.session.add(new_scientist)
        db.session.commit()

        scientist_dict = new_scientist.to_dict()

        response = make_response(
            scientist_dict,
            201
        )

        return response

@app.route('/scientists/<int:id>')
def get_sientist_by_id(id):
    scientist = Scientist.query.filter(Scientist.id == id).first()

    if scientist:
        body = scientist.to_dict()
        status = 200
    else:
        body = {"error": f"Scientist not found"}
        status = 404

    return make_response(body, status)

# @app.route('/scientists')


if __name__ == '__main__':
    app.run(port=5555, debug=True)
