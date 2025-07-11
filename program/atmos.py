import numpy as np
import scipy as sp

class Atmos:

    def __init__ (self, **kwargs):

        stp_size = kwargs['stp_size']

        acc_grav = kwargs['acc_grav']
        gas_cons = kwargs['gas_cons']
        mol_mass = kwargs['mol_mass']
        sea_pres = kwargs['sea_pres']
        sea_temp = kwargs['sea_temp']

        bnd_altd = kwargs['bnd_altd']
        bnd_temp = kwargs['bnd_temp']

        bnd_altd = np.concatenate(([0], bnd_altd))
        bnd_temp = np.concatenate(([sea_temp], bnd_temp))

        idx = np.argsort(bnd_altd)

        bnd_altd = bnd_altd[idx]
        bnd_temp = bnd_temp[idx]

        self._altd = np.arange(bnd_altd[0], bnd_altd[-1], stp_size)
        self._temp = np.array([])
        self._grad = np.array([])

        for altd in self._altd:

            idx = np.clip(np.searchsorted(bnd_altd, altd), 1, np.size(bnd_altd) - 1)

            altd_full_diff = bnd_altd[idx] - bnd_altd[idx - 1]
            temp_full_diff = bnd_temp[idx] - bnd_temp[idx - 1]

            altd_part_diff = altd - bnd_altd[idx - 1]
            temp_part_diff = temp_full_diff * altd_part_diff / altd_full_diff

            temp = temp_part_diff + bnd_temp[idx - 1]
            grad = temp_full_diff / altd_full_diff

            self._temp = np.concatenate((self._temp, [temp]))
            self._grad = np.concatenate((self._grad, [grad]))

        integ = sp.integrate.cumulative_trapezoid((mol_mass * acc_grav + gas_cons * self._grad) / (gas_cons * self._temp), self._altd)
        integ = np.exp(-np.concatenate(([0], integ)))

        self._pres = (sea_pres * self._temp / sea_temp) * integ
        self._dens = (sea_pres * mol_mass) / (sea_temp * gas_cons) * integ

        self._idx = 0

        return

    def getData (self):

        if self._idx == np.size(self._altd):
            return None

        data = self._altd[self._idx], self._temp[self._idx], self._pres[self._idx], self._dens[self._idx]

        self._idx += 1

        return data
