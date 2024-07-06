from gemini_model.model_abstract import Model
from gemini_model.well.correlation.frictiondarcyweisbach import frictiondarcyweisbach
import numpy as np


class DPF(Model):
    """ Class of DPF

    Class to calculate pressure drop along the well with multiple sections
    """

    def __init__(self):
        self.parameters = {}
        self.output = {}
        self.PVT = None

    def update_parameters(self, parameters):
        """ To update model parameters

        Parameters
        ----------
        parameters: dict
            parameters dict as defined by the model
        """
        for key, value in parameters.items():
            self.parameters[key] = value

    def initialize_state(self, x):
        """ generate an initial state based on user parameters """
        pass

    def update_state(self, u, x):
        """update the state based on input u and state x"""
        pass

    def calculate_output(self, u, x):
        """calculate output based on input u and state x"""

        # preparing input
        Ngrid = len(self.parameters['depth'])  # Number of grid cells (-)
        Lcel = self.parameters['depth']  # Length of 1 cell
        Dtube = self.parameters['diameter']  # diameter of cells (m)
        Atube = np.pi / 4 * Dtube ** 2  # area of cells (m2)
        Krough = self.parameters['roughness']   # roughness of cells (mm)
        flowRate = u['flowrate']
        Temperature = u['temperature'] + 273.15  # convert to K
        Pressure = u['Pressure'] * 1e5  # convert to K

        krange = range(1, Ngrid + 1)

        rho_g, rho_l, gmf, eta_g, eta_l, cp_g, cp_l, K_g, K_l, sigma = self.PVT.get_pvt(
                Pressure,
                Temperature)

        pressuredrop = 0
        for k in krange:

            if flowRate == 0:
                dp_friction = 0
            else:

                us_l = flowRate / Atube[k - 1]  # superficial gas velocity [m/s]

                dp_friction = frictiondarcyweisbach.calculate_dp(us_l, rho_l, eta_l, Dtube[k - 1],
                                                                 Krough[k - 1],
                                                                 Lcel[k - 1])

            pressuredrop = pressuredrop + dp_friction

        self.output['pressuredrop_output'] = pressuredrop / 1e5

    def get_output(self):
        """get output of the model"""
        return self.output
