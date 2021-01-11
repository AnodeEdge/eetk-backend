"""Performs voltage drop calculations, sanitizes paramters, and required math operations"""

import numpy as np
# import pdb

def sanitize_voltage_drop_params(**kwargs):
    allowed_keys = ['voltage', 'current', 'resistance', 'reactance', 'length', 'lengthUnit', 'powerfactor', 'parallelSets']
    keys_to_remove = []
    for key in kwargs:
        if (key != "lengthUnit") and (key in allowed_keys):
            kwargs[key] = float(kwargs[key])
        elif key != "lengthUnit":
            keys_to_remove.append(key)
    for key in keys_to_remove:
        kwargs.pop(key)
    return kwargs


class VoltageDropCalc():

    def __init__(self, **kwargs):
        self.voltage = kwargs['voltage']
        self.current = kwargs['current']
        self.length = kwargs['length']
        self.length_unit = kwargs['lengthUnit']
        self.powerfactor = kwargs['powerfactor']
        self.parallel_sets = kwargs['parallelSets']
        self.resistance = self.convert_units(kwargs['resistance'])
        self.reactance = self.convert_units(kwargs['reactance'])
        self.impedance = self.solve_impedance()

    def convert_units(self, unit_to_convert):
        allowed_feet_inputs = ["feet", "ft"]
        unit_to_convert = float(unit_to_convert)
        if self.length_unit in allowed_feet_inputs:
            unit_to_convert = unit_to_convert / 3.28084
        return round(unit_to_convert, 3)

    def solve_impedance(self):
        return((self.resistance * self.powerfactor) + \
            (self.reactance * (np.sin(np.arccos(self.powerfactor)))))

    def single_phase_voltage_drop(self):
        # VD = 2 x I x D x (Z/1000) * (1/parallel sets)
        voltage_drop = 2 * self.current * self.length * \
            (self.impedance / 1000) * (1 / self.parallel_sets)
        voltage_drop_percent = ( voltage_drop / self.voltage ) * 100
        return voltage_drop, voltage_drop_percent

    def three_phase_voltage_drop(self):
        # VD = sqrt(3) x I x D x (Z/1000) * (1/parallel sets)
        voltage_drop = np.sqrt(3) * self.current * self.length * \
            (self.impedance / 1000) * (1 / self.parallel_sets)
        voltage_drop_percent = ( voltage_drop / self.voltage ) * 100
        return voltage_drop, voltage_drop_percent

    
