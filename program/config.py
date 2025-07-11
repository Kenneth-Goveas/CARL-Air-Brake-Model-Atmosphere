import json
import numpy as np

class Config:

    def __init__ (self, **kwargs):

        file = open(kwargs['path'], mode = 'r')
        data = json.load(file)
        file.close()

        self._stp_size = data['step size']
        self._acc_grav = data['gravitational acceleration']
        self._gas_cons = data['ideal gas constant']
        self._mol_mass = data['molar mass']
        self._sea_pres = data['sea level pressure']
        self._sea_temp = data['sea level temperature']
        self._bnd_altd = data['altitude']
        self._bnd_temp = data['temperature']

        return

    def getStpSize (self):
        return self._stp_size

    def getAccGrav (self):
        return self._acc_grav

    def getGasCons (self):
        return self._gas_cons

    def getMolMass (self):
        return self._mol_mass

    def getSeaPres (self):
        return self._sea_pres

    def getSeaTemp (self):
        return self._sea_temp

    def getBndAltd (self):
        return self._bnd_altd

    def getBndTemp (self):
        return self._bnd_temp
