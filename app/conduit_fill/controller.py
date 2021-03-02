
import os.path
import csv
import pandas as pd
import pdb

from flask import jsonify 
from ..database import db
from ..models import ConductorData, ConduitData
from .helper import ConduitFillCalc
# from .helper import ConduitFillCalc, sanitize_voltage_drop_params as sanitize_vdp

class Controller():

    def __init__(self):
        self.app_path = os.path.dirname(
            os.path.abspath(os.path.dirname(__file__)))

    def create_conduit_data_table(self, file_name="assets/conduit_fill/conduit_fill_data.csv"):
        file_path = os.path.join(self.app_path, file_name)
        with open(file_path, newline='') as csvfile:
            db.session.query(ConduitData).delete()
            db.session.commit()
            reader = csv.DictReader(csvfile)
            for data_row in reader:
                row_to_add = ConduitData(**data_row)
                db.session.add(row_to_add)
                db.session.commit()
            return "Completed"
        return 'Could not create table'

    def create_conductor_data_table(self, file_name="assets/conduit_fill/conductor_fill_data.csv"):
        file_path = os.path.join(self.app_path, file_name)
        with open(file_path, newline='') as csvfile:
            db.session.query(ConductorData).delete()
            db.session.commit()
            reader = csv.DictReader(csvfile)
            for data_row in reader:
                row_to_add = ConductorData(**data_row)
                db.session.add(row_to_add)
                db.session.commit()
            return "Completed"
        return 'Could not create table'

    def query_conduit_data(self, data):
        conduit_data_query = ConduitData.query.filter_by(
            trade_size = data['conduitSize'],
            conduit_type = data['conduitType']
        ).first()
        return conduit_data_query.to_dict()

    def query_conductor_data(self, data):
        conductor_data_query = ConductorData.query.filter_by(
            conductor_type = data['wireType'],
            conductor_size = data['wireSize']
        ).first()
        conductor_data_dict = conductor_data_query.to_dict()
        conductor_data_dict['quantity'] = int(data['quantity'])
        return conductor_data_dict 

    def calculate_conduit_fill(self, **inputs):
        conduit_data = self.query_conduit_data(inputs['conduitData'])
        conductor_data = []
        for item in inputs['conductorData']:
            conductor_data.append(self.query_conductor_data(item))
        conduit_fill_data = {"conduit_data": conduit_data,
        "conductor_data": conductor_data}
        conduit_fill_calc = ConduitFillCalc(**conduit_fill_data)
        results = {"fill": conduit_fill_calc.solve_conduit_fill(),
        "jam": conduit_fill_calc.solve_jam_ratio()}
        return results

    def get_inputs_from_db(self):
        # conduit input data
        distinct_conduit_type_query = db.session.query(
            ConduitData.conduit_type.distinct().label('conduit_type'))
        distinct_trade_size_query = db.session.query(
            ConduitData.trade_size.distinct().label('trade_size'))

        # conductor input data
        distinct_conductor_type_query = db.session.query(
            ConductorData.conductor_type.distinct().label('conductor_type'))
        distinct_conductor_size_query = db.session.query(
            ConductorData.conductor_size.distinct().label('conductor_size'))

        #generate input lists for frontend
        distinct_conduit_types = [
            row.conduit_type for row in distinct_conduit_type_query.all()]
        distinct_trade_sizes = [
            row.trade_size for row in distinct_trade_size_query.all()]
        distinct_conductor_types = [
            row.conductor_type for row in distinct_conductor_type_query.all()]
        distinct_conductor_sizes = [
            row.conductor_size for row in distinct_conductor_size_query.all()]

        conduit_fill_inputs = {
            "conduitTypes": distinct_conduit_types,
            "tradeSizes": distinct_trade_sizes,
            "wireTypes": distinct_conductor_types,
            "wireSizes": distinct_conductor_sizes,
        }

        return jsonify(conduit_fill_inputs)



