import sys

from . import atmos, config, data

if __name__ == '__main__':

    cfg_path = sys.argv[1]
    dat_path = sys.argv[2]

    cfg = config.Config(path = cfg_path)
    dat = data.Data(path = dat_path)

    stp_size = cfg.getStpSize()
    acc_grav = cfg.getAccGrav()
    gas_cons = cfg.getGasCons()
    mol_mass = cfg.getMolMass()
    sea_pres = cfg.getSeaPres()
    sea_temp = cfg.getSeaTemp()
    bnd_altd = cfg.getBndAltd()
    bnd_temp = cfg.getBndTemp()

    atm = atmos.Atmos(
        stp_size = stp_size,
        acc_grav = acc_grav,
        gas_cons = gas_cons,
        mol_mass = mol_mass,
        sea_pres = sea_pres,
        sea_temp = sea_temp,
        bnd_altd = bnd_altd,
        bnd_temp = bnd_temp
    )

    while True:
        data = atm.getData()
        if data is not None:
            altd, temp, pres, dens = data
            dat.put(altd, temp, pres, dens)
        else:
            break
