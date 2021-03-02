import pdb
from flask import Blueprint, jsonify, request

from .controller import Controller

conduit_fill_bp = Blueprint(
    'conduit_fill', __name__, url_prefix="/conduit_fill")

ctrl = Controller()

@conduit_fill_bp.route('/')
def test():
    return "Found"

@conduit_fill_bp.route('/create_tables')
def create_tables():
    ctrl.create_conduit_data_table()
    ctrl.create_conductor_data_table()
    return "Completed"

@conduit_fill_bp.route('/inputs', methods=["POST"])
def inputs():
    return ctrl.get_inputs_from_db()

@conduit_fill_bp.route('/calc', methods=['POST'])
def calc():
    recieved_data = request.json
    response_data = ctrl.calculate_conduit_fill(**recieved_data)
    return jsonify(response_data)
    