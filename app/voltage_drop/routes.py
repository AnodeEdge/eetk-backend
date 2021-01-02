from flask import Blueprint, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from ..database import db
# from app import models
from ..models import CableResistance
from flask.json import dumps
import os.path
import csv
import pdb

voltage_drop_bp = Blueprint('voltage_drop', __name__, url_prefix="/voltage_drop")
app_path = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))


@voltage_drop_bp.route('/')
def whatever():
    return "Found"
    
@voltage_drop_bp.route('/calculate_voltage_drop', methods=['POST'])
def calculate_voltage_drop():
    data = request.json
    pdb.set_trace()
    data_query = CableResistance.query.filter_by(
        size=data['size'],
        conductor_material=data['conductor_material'],
        conduit_material=data['conduit_material']).first()
    data_as_json = data_query.serialize()
    return data_as_json

@voltage_drop_bp.route('/create_resistance_table')
def load_data(file_name="assets/voltage_drop/data.csv"):
    file_path = os.path.join(app_path, file_name)
    with open(file_path, newline='') as csvfile:
        db.session.query(CableResistance).delete()
        db.session.commit()
        reader = csv.DictReader(csvfile)
        for data_row in reader:
            row_to_add = CableResistance(**data_row)
            db.session.add(row_to_add)
            db.session.commit()
        return "Completed"
    return 'Cannot find table'

@voltage_drop_bp.route('/send_dummy_data', methods=['GET', 'POST'])
def send_dummy_data():
    data = request.json
    
    print(data)
    # data_query = db.session.query(CableResistance).filter_by(size='12').first()
    data_query = CableResistance.query.filter_by(size='12').first()
    data_as_json = data_query.serialize()
    # pdb.set_trace()
    return data_as_json