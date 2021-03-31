import numpy as np


class ConduitFillCalc():

    def __init__(self, **kwargs):
        self.conduit_area = kwargs['conduit_data']['area']
        self.conduit_inner_diameter = kwargs['conduit_data']['inner_diameter']
        self.conductor_data = kwargs['conductor_data']

    def solve_conduit_fill(self):
        # sum of ( area of cable * quantity ) for all cables
        if self.conduit_area == 0:
            return "Conduit data for the selected size and type does not exist"
        total_conductor_area = 0
        for conductor in self.conductor_data:
            if conductor['area'] == 0:
                return "Conductor data for type " + conductor['conductor_type'] + " and size " + conductor['conductor_size'] + " does not exist"
            total_conductor_area += conductor['quantity'] * conductor['area']
        conduit_fill_pct = round(total_conductor_area / self.conduit_area * 100, 2)
        return "Fill %: " + str(conduit_fill_pct)

    def solve_jam_ratio(self):
        # 1.05 * inner diameter / largest cable outer diameter
        largest_conductor_diameter = 0
        for conductor in self.conductor_data:
            if conductor['diameter'] == 0:
                return ""
            if conductor['diameter'] > largest_conductor_diameter:
                largest_conductor_diameter = conductor['diameter']
        if largest_conductor_diameter != 0:
            jam_ratio = round(1.05 * self.conduit_inner_diameter / largest_conductor_diameter, 2)
            return "Jam Ratio: " + str(jam_ratio)
        return ""
