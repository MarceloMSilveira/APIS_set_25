from flask import Flask, request, abort
from config_db import db
from flask_migrate import Migrate
from flask_cors import CORS, cross_origin

app=Flask(__name__)
app.config.from_object('config')

db.init_app(app)

migrate = Migrate(app,db)

from models import Plant

with app.app_context():
    db.create_all()

cors = CORS(app,
     origins=["127.0.0.1:5000"],
     methods=['GET','POST'],
     supports_credentials=True, 
     )

@app.route("/plants", methods=['GET','POST'])
def get_plants():
    page = request.args.get("page",1,type=int)
    start = (page-1)*5
    end = start + 5

    plants = db.session.execute(db.select(Plant)).scalars().all()

    formatted_plants = [plant.format() for plant in plants]

    return {
        "success": True,
        "plants": formatted_plants[start:end],
        "total_plants": len(formatted_plants)
    }

@app.route("/")
def home():
    return ('home is ok!')

@app.route("/plants/<int:plant_id>")
def get_specific_plant(plant_id):
    try:
        plant = db.get_or_404(Plant,plant_id)
        return {
            "success":True,
            "plant":plant.format()
        }
    except Exception as e:
        abort(404)


@app.errorhandler(404)
def not_found():
    return {
        "success":False,
        "error": 404,
        "message": "Resource not found"
    }, 404
