#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)


class PlantsResource(Resource):

    def get(self):
        plants = [plant.to_dict() for plant in Plant.query.all()]
        return make_response(jsonify(plants), 200)

    def post(self):
        data = request.get_json()

        try:
            new_plant = Plant(
                name=data['name'],
                image=data['image'],
                price=data['price'],
            )

            db.session.add(new_plant)
            db.session.commit()

            return new_plant.to_dict(), 201
        except Exception as e:
            return {"error": str(e)}, 400

            # return make_response(new_plant.to_dict(), 201)




class PlantByIDResource(Resource):

    def get(self, id):
        plant = Plant.query.get(id)
        if not plant:
            return {"error": "Plant not found"}, 404
        return plant.to_dict(), 200
    
    def patch(self, id):
        plant = Plant.query.get(id)
        if not plant:
            return {"error": "Plant not found"}, 404

        data = request.get_json()
        if "is_in_stock" in data:
            plant.is_in_stock = data["is_in_stock"]

        db.session.commit()
        return plant.to_dict(), 200

    def delete(self, id):
        plant = Plant.query.get(id)
        if not plant:
            return {"error": "Plant not found"}, 404

        db.session.delete(plant)
        db.session.commit()
        return '', 204


# Route Registration
api.add_resource(PlantsResource, '/plants')
api.add_resource(PlantByIDResource, '/plants/<int:id>')

# Entry Point 
if __name__ == '__main__':
    app.run(port=5555, debug=True)
