from flask import Flask, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_restful import Api, Resource
from dotenv import load_dotenv
from os import environ
from marshmallow import post_load

load_dotenv()

# Create App instance
app = Flask(__name__)

# Add DB URI from .env
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('SQLALCHEMY_DATABASE_URI')

# Registering App w/ Services
db = SQLAlchemy(app)
ma = Marshmallow(app)
api = Api(app)
CORS(app)
Migrate(app, db)

# Models
class Car(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    make = db.Column(db.String(255), nullable = False)
    model = db.Column(db.String(255), nullable = False)
    year = db.Column(db.Integer)    

    def __repr__(self):
        return f'{self.year} {self.make} {self.model}'

# Schemas
class CarSchema(ma.Schema):
    @post_load
    def create(self, data, **kwargs):
        return Car(**data)
    
    class Meta:
        fields = ("id","make","model","year")

car_schema = CarSchema()
cars_schema = CarSchema(many = True)


# Resources
class CarListResources(Resource):
    def get(self):
        all_cars = Car.query.all()
        return cars_schema.dump(all_cars)
    
    def post(self):
        data = request.get_json()
        new_car = car_schema.load(data)
        db.session.add(new_car)
        db.session.commit()
        return car_schema.dump(new_car)
    

class CarResource(Resource):
    def get(self,car_id):
        print(car_id)
        pass


# Routes
api.add_resource(CarListResources,'/api/cars')
api.add_resource(CarResource, '/api/cars/<int:car_id>')
