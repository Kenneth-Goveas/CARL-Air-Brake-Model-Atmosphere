# CARL Air Brake Model Atmosphere

This repository contains an atmospheric modelling tool to support the [CARL Air Brake][cab-repo] computer. The CARL Air Brake computer
automatically controls a rocket air brake in flight, so that the vehicle attains an apogee at the desired altitude. The modelling tool
provided here generates the necessary atmospheric data.

## Background

The simulation, control, and estimation algorithms used by the CARL Air Brake computer need atmospheric data in order to run properly. In
particular, a lookup table is required to obtain the atmospheric pressure, temperature, and density, each as a function of altitude. This
modelling tool generates this lookup table from a given temperature-versus-altitude profile.

## Prerequisites

You will need [Python][python] along with the libraries [NumPy][numpy] and [SciPy][scipy] to use this tool. On typical Linux distributions,
Python is usually pre-installed, and the aforementioned libraries can be installed with the following command.

```
pip install numpy scipy
```

## Usage

Create a JSON file in the [models][mod-dir] directory, containing the input parameters to be supplied to the modelling tool (see
[models/example.json][mod-ex-inpt-file] for an illustration). The following is the expected structure of the input JSON file and a
description of the parameters within it.

```
{
  "step size": <number>,
  "gravitational acceleration": <number>,
  "ideal gas constant": <number>,
  "molar mass": <number>,
  "sea level pressure": <number>,
  "sea level temperature": <number>,
  "altitude": [<number1>, <number2> ... <numberN>],
  "temperature": [<number1>, <number2> ... <numberN>]
}
```

| **Parameter**                 | **Description**                                                       |
| ----------------------------- | --------------------------------------------------------------------- |
| `step size`                   | Step size for numerical integration with respect to altitude (in m).  |
| `gravitational acceleration`  | Gravitational acceleration (in m/s²).                                 |
| `ideal gas constant`          | Ideal gas constant (in J/mol.K).                                      |
| `molar mass`                  | Average molar mass of air (in kg/mol).                                |
| `sea level pressure`          | Atmospheric pressure at sea level (in Pa).                            |
| `sea level temperature`       | Atmospheric temperature at sea level (in K).                          |
| `altitude`                    | List of altitudes in temperature-versus-altitude profile (in m).      |
| `temperature`                 | List of temperatures in temperature-versus-altitude profile (in K).   |

The modelling tool uses a piecewise linear temperature-versus-altitude profile. The `altitude` and `temperature` parameters in the above
listing contain an array of altitudes and their corresponding temperatures. The `sea level temperature` parameter specifies one more such
data point at zero altitude. Between any two consecutive altitudes, the temperature is assumed to vary linearly with changing altitude.

After creating the input JSON file, run the following command from the directory where you cloned this repository.

```
python -m program models/<input>.json models/<output>.csv
```

Here, `models/<input>.json` is the path to the input JSON file you created, and `models/<output>.csv` is the path to the output CSV file
that the modelling tool will generate. The output CSV file will have the four columns `Altitude (m)`, `Temperature (K)`, `Pressure (Pa)`,
and `Density (kg/m³)`, and will contain the generated lookup table.

## Working

Assuming air is an ideal gas, the temperature-versus-altitude profile can easily be used to compute the pressure and density as functions of
altitude. We use the following notation in the equations in this section.

| **Symbol**  | **Meaning**                     |
| ----------- | ------------------------------- |
| $h$         | A given arbitrary altitude      |
| $x$         | Dummy altitude for integration  |
| $p$         | Pressure                        |
| $V$         | Volume                          |
| $T$         | Temperature                     |
| $\rho$      | Density                         |
| $m$         | Mass                            |
| $M$         | Molar mass                      |
| $n$         | Number of moles                 |
| $R$         | Ideal gas constant              |
| $g$         | Gravitational acceleration      |
| $p_0$       | Sea level pressure              |
| $T_0$       | Sea level temperature           |
| $\rho_0$    | Sea level density               |

From the parameters in the input JSON file, we know $p_0$, $M$, $R$, $g$, and $T(x)$. Then, given any altitude $h$, we wish to compute the
pressure $p(h)$ and density $\rho(h)$. We start with the ideal gas equation,

$$pV=nRT$$
$$\therefore\ pV=\frac{mRT}{M}$$
$$\therefore\ pM=\rho RT.\quad(1)$$

Now consider an altitude $x$ and an increment $dx$. The corresponding change in pressure $dp$ must be,

$$dp=-\rho gdx.\quad(2)$$

Differentiating $(1)$ and substituting $(2)$, we get,

$$-\rho Mgdx=R\left(\rho dT+Td\rho\right)$$
$$\therefore\ -\rho\left(Mg+RT'\right)dx=RTd\rho$$
$$\therefore\ \frac{d\rho}{\rho}=-\left(\frac{Mg+RT'}{RT}\right)dx.\quad(3)$$

Integrating $(3)$ and using $(1)$ to substitute for $\rho_0$, we get the density $\rho(h)$,

$$\int_{\rho_0}^{\rho\left(h\right)}\frac{d\rho}{\rho}=-\int_0^h\left(\frac{Mg+RT'}{RT}\right)dx$$
$$\therefore\ \ln\left[\frac{\rho\left(h\right)RT_0}{p_0M}\right]=-\int_0^h\left(\frac{Mg+RT'}{RT}\right)dx$$
$$\therefore\ \rho\left(h\right)=\frac{p_0M}{RT_0}\exp\left[-\int_0^h\left(\frac{Mg+RT'}{RT}\right)dx\right].\quad(4)$$

Now substituting $(4)$ in $(1)$, we get the pressure $p(h)$,

$$p\left(h\right)=\frac{p_0T\left(h\right)}{T_0}\exp\left[-\int_0^h\left(\frac{Mg+RT'}{RT}\right)dx\right].\quad(5)$$

The modelling tool uses $(4)$ and $(5)$ to compute the pressure and density for the full range of altitudes in the
temperature-versus-altitude profile. The integral is computed numerically using the step size in the input JSON file.

[mod-dir]:          ./models
[mod-ex-inpt-file]: ./models/example.json

[cab-repo]:         https://github.com/Kenneth-Goveas/CARL-Air-Brake

[python]:           https://www.python.org
[numpy]:            https://www.numpy.org
[scipy]:            https://www.scipy.org
