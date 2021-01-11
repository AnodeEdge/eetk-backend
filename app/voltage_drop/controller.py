"""Performs database queries and logical operations for routes"""

import os.path
import csv
import pdb

from flask import Blueprint, jsonify, request
from ..database import db
from ..models import CableResistance
from .helper import VoltageDropCalc, sanitize_voltage_drop_params as sanitize_vdp


class Controller():

    def __init__(self):
        self.app_path = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))

    def get_inputs_from_db(self):
        distinct_sizes_query = db.session.query(
            CableResistance.size.distinct().label('size'))
        distinct_conductor_materials_query = db.session.query(
            CableResistance.conductor_material.distinct().label('conductor_material'))
        distinct_conduit_materials_query = db.session.query(
            CableResistance.conduit_material.distinct().label('conduit_material'))
        distinct_sizes = [row.size for row in distinct_sizes_query.all()]
        distinct_conductor_materials = [
            row.conductor_material for row in distinct_conductor_materials_query.all()]
        distinct_conduit_materials = [
            row.conduit_material for row in distinct_conduit_materials_query.all()]

        table_inputs = {
            "sizes": distinct_sizes,
            "conductorMaterials": distinct_conductor_materials,
            "conduitMaterials": distinct_conduit_materials,
        }
        return jsonify(table_inputs)

    def query_row(self, **recieved_data):
        cable_data_query = CableResistance.query.filter_by(
            size=recieved_data['size'],
            conductor_material=recieved_data['conductorMaterial'],
            conduit_material=recieved_data['conduitMaterial']).first()
        return cable_data_query.to_dict()
        
        # combined_data = {**cable_data_json, **recieved_data}
        # voltage_drop = VoltageDropCalc(**sanitize_vdp(**combined_data))
        # return cable_data_json

    def calculate_voltage_drop(self, **inputs):
        cable_data = self.query_row(**inputs)
        combined_data = {**cable_data, **inputs}
        sanitized_data = sanitize_vdp(**combined_data)
        voltage_drop = VoltageDropCalc(**sanitized_data) 
        # pdb.set_trace()
        if inputs["phase"] == "three":
            result, percent = voltage_drop.three_phase_voltage_drop()
        else:
            result, percent = voltage_drop.single_phase_voltage_drop()
        return {"result": result, "percent": percent}

    def create_resistance_table(self, file_name="assets/voltage_drop/data.csv"):
        file_path = os.path.join(self.app_path, file_name)
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
