from gemini_application.application_abstract import ApplicationAbstract
from gemini_model.reservoir.inflow_performance import IPR
from gemini_model.well.vertical_lift_curve import VLP
from gemini_model.pump.esp import ESP
from gemini_model.fluid.pvt_water_stp import PVTConstantSTP
import numpy as np
from matplotlib import pyplot as plt


class ProductionWellPerformance(ApplicationAbstract):
    """Class for application production well IPR/VLP calculation"""

    def __init__(self):
        super().__init__()

        self.IPR = IPR()
        self.VLP1 = VLP()
        self.VLP2 = VLP()
        self.ESP = ESP()

    def init_parameters(self):
        """Function to initialize model parameters"""
        res_param = dict()

        reservoir_unit = self.unit.from_units[0]
        well_unit = self.unit
        esp_unit = self.unit.to_units[0]

        res_param['reservoir_pressure'] = reservoir_unit.parameters['reservoir_pressure']
        res_param['productivity_index'] = well_unit.parameters['productionwell_productivity_index']
        res_param['type'] = 'production_reservoir'

        self.IPR.update_parameters(res_param)

        esp_param = dict()
        esp_param['no_stages'] = esp_unit.parameters['esp_no_stage']
        esp_param['pump_name'] = esp_unit.parameters['esp_type']
        esp_param['head_coeff'] = np.asarray(
            esp_unit.parameters['esp_head_coeff'].split(';'),
            dtype=np.float32)
        esp_param['power_coeff'] = np.asarray(
            esp_unit.parameters['esp_power_coeff'].split(';'),
            dtype=np.float32)
        esp_param['min_flow'] = esp_unit.parameters['esp_min_flow']
        esp_param['max_flow'] = esp_unit.parameters['esp_max_flow']

        self.ESP.update_parameters(esp_param)

        well_param = dict()

        well_param['diameter'] = np.array(
            [esp_unit.parameters['esp_tubing']])  # well diameter in [m]
        well_param['depth'] = np.array(
            [esp_unit.parameters['esp_depth']])  # well depth in [m]
        well_param['angle'] = np.array([90])  # well angle in [degree]

        self.VLP1.update_parameters(well_param)
        self.VLP1.PVT = PVTConstantSTP()

        well_param = dict()

        well_traj = well_unit.parameters['productionwell_trajectory_table']
        depth = []
        diameter = []
        angle = []
        for ii in range(1, len(well_traj)):
            if well_traj[ii - 1]['MD'] >= esp_unit.parameters['esp_depth']:
                MD = well_traj[ii]['MD'] - well_traj[ii - 1]['MD']
                TVD = well_traj[ii]['TVD'] - well_traj[ii - 1]['TVD']

                depth.append(MD)
                diameter.append(well_traj[ii]['ID'])
                angle.append(np.round(90 - np.arccos(TVD / MD) * 180 / np.pi, 2))

        well_param['diameter'] = np.array(diameter)  # well diameter in [m]
        well_param['depth'] = np.array(depth)  # well depth in [m]
        well_param['angle'] = np.array(angle)  # well angle in [degree]

        self.VLP2.update_parameters(well_param)
        self.VLP2.PVT = PVTConstantSTP()

    def calculate(self):
        """Function to calcaulte IPR, VLP, ESP"""
        flow_array = np.linspace(self.ESP.parameters['min_flow'] * 0.8,
                                 self.ESP.parameters['max_flow'] * 1.1,
                                 100)
        self.inputs['flow'] = flow_array

        self.calculate_dp_top_esp()
        self.calculate_esp()
        self.calculate_dp_esp_bottom()
        self.calculate_pbh_res()

    def calculate_dp_top_esp(self):
        """Function to calculate pressure drop from wellhead to ESP"""
        u = dict()
        x = []

        discharge_pressure = []
        discharge_temperature = []
        for flow in self.inputs['flow']:
            u['pressure_input'] = self.inputs['wellhead_pressure']
            u['temperature_input'] = self.inputs['wellhead_temperature']
            u['mass_flowrate'] = flow
            u['temperature_ambient'] = float(
                self.unit.parameters['productionwell_soil_temperature'])
            u['direction'] = 'down'

            self.VLP1.calculate_output(u, x)

            # ASSERT
            y = self.VLP1.get_output()

            discharge_pressure.append(y['pressure_output'])
            discharge_temperature.append(y['temperature_output'])

        self.outputs['discharge_pressure'] = np.array(discharge_pressure)
        self.outputs['discharge_temperature'] = np.array(discharge_temperature)

    def calculate_dp_esp_bottom(self):
        """Function to calculate pressure drop from ESP to bottomhole"""
        self.outputs['intake_pressure'] = self.outputs['discharge_pressure'] - self.outputs[
            'pump_head']
        self.outputs['intake_temperature'] = self.outputs['discharge_temperature']

        u = dict()
        x = []

        bottomhole_pressure = []
        bottomhole_temperature = []
        ii = 0
        for flow in self.inputs['flow']:
            u['pressure_input'] = self.outputs['intake_pressure'][ii]
            u['temperature_input'] = self.outputs['intake_temperature'][ii]
            u['mass_flowrate'] = flow
            u['temperature_ambient'] = float(
                self.unit.parameters['productionwell_soil_temperature'])
            u['direction'] = 'down'

            self.VLP2.calculate_output(u, x)

            # ASSERT
            y = self.VLP2.get_output()

            bottomhole_pressure.append(y['pressure_output'])
            bottomhole_temperature.append(y['temperature_output'])

            ii = ii + 1

        self.outputs['pbh_well'] = np.array(bottomhole_pressure)
        self.outputs['tbh_well'] = np.array(bottomhole_temperature)

    def calculate_esp(self):
        """Function to calculate ESP output"""
        u = dict()
        x = []

        pump_head = []
        pump_power = []
        pump_eff = []
        for flow in self.inputs['flow']:
            u['pump_freq'] = self.inputs['esp_freq']
            u['pump_flow'] = flow / 3600

            self.ESP.calculate_output(u, x)

            # ASSERT
            y = self.ESP.get_output()
            pump_head.append(y['pump_head'] / 1e5)
            pump_power.append(y['pump_power'])
            pump_eff.append(y['pump_eff'])

        self.outputs['pump_head'] = np.array(pump_head)
        self.outputs['pump_power'] = np.array(pump_power)
        self.outputs['pump_eff'] = np.array(pump_eff)

    def calculate_pbh_res(self):
        """Function to calculate bottomhole pressure from reservoir"""
        u = dict()
        x = []

        pbh_res = []
        p_res = []
        for flow in self.inputs['flow']:
            u['flow'] = flow

            self.IPR.calculate_output(u, x)

            # ASSERT
            y = self.IPR.get_output()
            pbh_res.append(y['pressure_bottomhole'])
            p_res.append(self.IPR.parameters['reservoir_pressure'])

        self.outputs['pbh_res'] = np.array(pbh_res)
        self.inputs['reservoir_pressure'] = np.array(p_res)

    def plot(self):
        """Function to calculate all pressure from reservoir to topside"""
        x = self.inputs['flow']
        y0 = self.inputs['wellhead_pressure'] * np.ones(len(x))
        y1 = self.outputs['discharge_pressure']
        y2 = self.outputs['intake_pressure']
        y3 = self.outputs['pbh_well']
        y4 = self.outputs['pbh_res']
        y5 = self.inputs['reservoir_pressure']

        plt.figure()
        plt.plot(x, y0, label='wellhead pressure')
        plt.plot(x, y1, label='discharge pressure')
        plt.plot(x, y2, label='intake pressure')
        plt.plot(x, y3, label='pbh well')
        plt.plot(x, y4, label='pbh res')
        plt.plot(x, y5, label='reservoir pressure')
        plt.legend()
        plt.show()

    def get_solution(self):

        sol_pbh = np.sqrt(np.power(self.outputs['pbh_well'] - self.outputs['pbh_res'], 2))
        if np.amin(sol_pbh) < 3:
            index = np.where(sol_pbh == np.amin(sol_pbh))
            self.outputs['sol_flow'] = self.inputs['flow'][index]
            self.outputs['sol_pbh'] = self.outputs['pbh_well'][index]
            self.outputs['sol_esp_head'] = self.outputs['pump_head'][index]
            self.outputs['sol_esp_power'] = self.outputs['pump_power'][index]
            self.outputs['sol_esp_eff'] = self.outputs['pump_eff'][index]
            self.outputs['sol_intake_pressure'] = self.outputs['intake_pressure'][index]
            self.outputs['sol_discharge_pressure'] = self.outputs['discharge_pressure'][index]
        else:
            self.outputs['sol_flow'] = 'NaN'
            self.outputs['sol_flow'] = 'NaN'
            self.outputs['sol_pbh'] = 'NaN'
            self.outputs['sol_esp_head'] = 'NaN'
            self.outputs['sol_esp_power'] = 'NaN'
            self.outputs['sol_esp_eff'] = 'NaN'
            self.outputs['sol_intake_pressure'] = 'NaN'
            self.outputs['sol_discharge_pressure'] = 'NaN'
