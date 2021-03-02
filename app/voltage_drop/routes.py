import pdb
from flask import Blueprint, jsonify, request

from .controller import Controller
from ..models import CableResistance
from .helper import VoltageDropCalc, sanitize_voltage_drop_params as sanitize_vdp

voltage_drop_bp = Blueprint(
    'voltage_drop', __name__, url_prefix="/voltage_drop")

ctrl = Controller()

@voltage_drop_bp.route('/')
def test():
    return "Found"

@voltage_drop_bp.route('/inputs', methods=["POST"])
def inputs():
    return ctrl.get_inputs_from_db()

@voltage_drop_bp.route('/create_resistance_table')
def load_data():
    return ctrl.create_resistance_table()

@voltage_drop_bp.route('/calc', methods=['POST'])
def calc():
    recieved_data = request.json
    response_data = ctrl.calculate_voltage_drop(**recieved_data)
    return jsonify(response_data)



# cable_data_query = CableResistance.query.filter_by(
#     size=recieved_data['size'],
#     conductor_material=recieved_data['conductorMaterial'],
#     conduit_material=recieved_data['conduitMaterial']).first()

# cable_data_json = cable_data_query.to_dict()

# combined_data = {**cable_data_json, **recieved_data}
# voltage_drop = VoltageDropCalc(**sanitize_vdp(**combined_data))
# pdb.set_trace()

# return cable_data_json

# @voltage_drop_bp.route('/send_dummy_data', methods=['GET', 'POST'])
# def send_dummy_data():
#     data = request.json

#     print(data)
#     # data_query = db.session.query(CableResistance).filter_by(size='12').first()
#     data_query = CableResistance.query.filter_by(size='12').first()
#     data_as_json = data_query.serialize()
#     # pdb.set_trace()
#     return data_as_json
