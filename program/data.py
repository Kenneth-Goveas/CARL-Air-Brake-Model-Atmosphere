import csv
import numpy as np

class Data:

    def __init__ (self, **kwargs):

        csv.register_dialect(
            'carl', delimiter = ',', lineterminator = '\n', escapechar = '\\', quotechar = '"',
            doublequote = False, quoting = csv.QUOTE_NONE
        )

        self._file = open(kwargs['path'], mode = 'w', newline = '')
        self._writ = csv.DictWriter(
                         self._file,
                         fieldnames = [
                             'Altitude (m)',
                             'Temperature (K)',
                             'Pressure (Pa)',
                             'Density (kg/m³)'
                         ],
                         dialect = 'carl'
                     )

        self._writ.writeheader()

        return

    def __del__ (self):
        self._file.close()
        return

    def put (self, altd, temp, pres, dens):
        self._writ.writerow({
            'Altitude (m)'    : '%+.10e' % altd,
            'Temperature (K)' : '%+.10e' % temp,
            'Pressure (Pa)'   : '%+.10e' % pres,
            'Density (kg/m³)' : '%+.10e' % dens
        })
        return
