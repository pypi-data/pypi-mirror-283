'''
Constants, conversions, and units.
In CGS, unless otherwise noted.

@author:
    Andrew Wetzel <arwetzel@gmail.com>
    Andrew Emerick <aemerick11@gmail.com>
'''

from scipy import constants as scipy_const

import numpy as np


# physical constants -------------------------------------------------------------------------------
grav = scipy_const.gravitational_constant * 1e3  # 6.674e-8 [cm^3 / g / s^2]
speed_light = scipy_const.speed_of_light * 1e2  # [cm / s]
boltzmann = scipy_const.k * 1e7  # [erg / K]
electron_volt = scipy_const.electron_volt * 1e7  # [erg]
proton_mass = scipy_const.proton_mass * 1e3  # [gram]
electron_mass = scipy_const.electron_mass * 1e3  # [gram]
amu_mass = scipy_const.m_u * 1e3  # 1/12 of carbon mass [gram]
hydrogen_mass = 1.0079 * amu_mass


# astrophysical constants --------------------------------------------------------------------------
year = scipy_const.Julian_year  # Julian [sec]
parsec = scipy_const.parsec * 1e2  # 3.0857e18 [cm]
au = scipy_const.astronomical_unit * 1e2  # [cm]

sun_mass = 1.98892e33  # [gram]
sun_luminosity = 3.842e33  # [erg]
sun_magnitude = 4.76  # bolometric (varies with filter but good for sdss r-band)
sun_radius = 6.957e10  # [cm]


# conversions --------------------------------------------------------------------------------------
# metric
micro = 1e-6
milli = 1e-3
centi = 1e-2
kilo = 1e3
mega = 1e6
giga = 1e9

centi_per_kilo = 1e5
kilo_per_centi = 1 / centi_per_kilo

centi_per_mega = 1e8
mega_per_centi = 1 / centi_per_mega

kilo_per_mega = 1e3
mega_per_kilo = 1 / kilo_per_mega

# mass
gram_per_sun = sun_mass
sun_per_gram = 1 / gram_per_sun

gram_per_proton = proton_mass
proton_per_gram = 1 / proton_mass

gram_per_hydrogen = hydrogen_mass
hydrogen_per_gram = 1 / hydrogen_mass

proton_per_sun = sun_mass / proton_mass
sun_per_proton = 1 / proton_per_sun

hydrogen_per_sun = sun_mass / hydrogen_mass
sun_per_hydrogen = 1 / hydrogen_per_sun

# time
sec_per_yr = year
yr_per_sec = 1 / sec_per_yr

sec_per_Gyr = sec_per_yr * 1e9
Gyr_per_sec = 1 / sec_per_Gyr

# length
cm_per_pc = parsec
pc_per_cm = 1 / cm_per_pc

cm_per_kpc = cm_per_pc * 1e3
kpc_per_cm = 1 / cm_per_kpc

cm_per_Mpc = cm_per_pc * 1e6
Mpc_per_cm = 1 / cm_per_Mpc

km_per_pc = cm_per_pc * kilo_per_centi
pc_per_km = 1 / km_per_pc

km_per_kpc = cm_per_pc * 1e-2
kpc_per_km = 1 / km_per_kpc

km_per_Mpc = cm_per_pc * 10
Mpc_per_km = 1 / km_per_Mpc

# energy
erg_per_ev = electron_volt
ev_per_erg = 1 / erg_per_ev

erg_per_kev = erg_per_ev * 1e3
kev_per_erg = 1 / erg_per_kev

kelvin_per_ev = scipy_const.electron_volt / scipy_const.k
ev_per_kelvin = 1 / kelvin_per_ev

# angle
degree_per_radian = 180 / scipy_const.pi
radian_per_degree = 1 / degree_per_radian

arcmin_per_degree = 60
degree_per_arcmin = 1 / arcmin_per_degree

arcsec_per_arcmin = 60
arcmin_per_arcsec = 1 / arcsec_per_arcmin

arcsec_per_degree = arcmin_per_degree * arcsec_per_arcmin
degree_per_arcsec = degree_per_arcmin * arcmin_per_arcsec

arcsec_per_radian = arcsec_per_arcmin * arcmin_per_degree * degree_per_radian
radian_per_arcsec = 1 / arcsec_per_radian

arcmin_per_radian = arcmin_per_degree * degree_per_radian
radian_per_arcmin = 1 / arcmin_per_radian

deg2_per_sky = 4 * scipy_const.pi * degree_per_radian ** 2

# cosmological constant parameters ----------
# hubble parameter = H_0 [h / sec]
hubble_parameter_0 = 100 * Mpc_per_km
# hubble time = 1 / H_0 ~ 9.7779 [Gyr / h]
hubble_time = 1 / 100 * Gyr_per_sec * km_per_Mpc
# hubble distance = c / H_0 ~ 2,997,925 [kpc / h]
hubble_distance = speed_light / 100 * kilo_per_centi * kilo_per_mega
# critical density at z = 0:  3 * H_0 ^ 2 / (8 * pi * G) ~ 277.5 [M_sun/h / (kpc/h)^3]
density_critical_0 = (
    3 * 100 ** 2 / (8 * scipy_const.pi * grav) * centi_per_kilo ** 2 / Mpc_per_cm / sun_mass
) / kilo_per_mega ** 3

# gravitational constant in various units ----------
# [km^3 / M_sun / s^2]
grav_km_msun_sec = grav * kilo_per_centi ** 3 * gram_per_sun
# [pc^3 / M_sun / s^2]
grav_pc_msun_sec = grav * pc_per_cm ** 3 * gram_per_sun
# [pc^3 / M_sun / yr^2]
grav_pc_msun_yr = grav * pc_per_cm ** 3 * gram_per_sun * sec_per_yr ** 2
# [kpc^3 / M_sun / s^2]
grav_kpc_msun_sec = grav * kpc_per_cm ** 3 * gram_per_sun
# [kpc^3 / M_sun / yr^2]
grav_kpc_msun_yr = grav * kpc_per_cm ** 3 * gram_per_sun * sec_per_yr ** 2
# [kpc^3 / M_sun / Gyr^2]
grav_kpc_msun_Gyr = grav * kpc_per_cm ** 3 * gram_per_sun * sec_per_Gyr ** 2


# element properties -------------------------------------------------------------------------------
element = {
    'hydrogen': {'symbol': 'h', 'number': 1, 'weight': 1.0079},
    'helium': {'symbol': 'he', 'number': 2, 'weight': 4.0026},
    'lithium': {'symbol': 'li', 'number': 3, 'weight': 6.941},
    'beryllium': {'symbol': 'be', 'number': 4, 'weight': 9.0122},
    'boron': {'symbol': 'b', 'number': 5, 'weight': 10.811},
    'carbon': {'symbol': 'c', 'number': 6, 'weight': 12.0107},
    'nitrogen': {'symbol': 'n', 'number': 7, 'weight': 14.0067},
    'oxygen': {'symbol': 'o', 'number': 8, 'weight': 15.9994},
    'flourine': {'symbol': 'f', 'number': 9, 'weight': 18.9984},
    'neon': {'symbol': 'ne', 'number': 10, 'weight': 20.1797},
    'sodium': {'symbol': 'na', 'number': 11, 'weight': 22.9897},
    'magnesium': {'symbol': 'mg', 'number': 12, 'weight': 24.305},
    'aluminum': {'symbol': 'al', 'number': 13, 'weight': 26.9815},
    'silicon': {'symbol': 'si', 'number': 14, 'weight': 28.0855},
    'phosphorus': {'symbol': 'p', 'number': 15, 'weight': 30.9738},
    'sulfur': {'symbol': 's', 'number': 16, 'weight': 32.065},
    'chlorine': {'symbol': 'cl', 'number': 17, 'weight': 35.453},
    'argon': {'symbol': 'ar', 'number': 18, 'weight': 39.948},
    'potassium': {'symbol': 'k', 'number': 19, 'weight': 39.098},
    'calcium': {'symbol': 'ca', 'number': 20, 'weight': 40.078},
    'scandium': {'symbol': 'sc', 'number': 21, 'weight': 44.955912},
    'titatium': {'symbol': 'ti', 'number': 22, 'weight': 47.867},
    'vanadium': {'symbol': 'v', 'number': 23, 'weight': 50.9415},
    'chromium': {'symbol': 'cr', 'number': 24, 'weight': 51.9961},
    'manganese': {'symbol': 'mn', 'number': 25, 'weight': 54.938045},
    'iron': {'symbol': 'fe', 'number': 26, 'weight': 55.845},
    'cobalt': {'symbol': 'co', 'number': 27, 'weight': 58.933195},
    'nickel': {'symbol': 'ni', 'number': 28, 'weight': 58.6934},
    'copper': {'symbol': 'cu', 'number': 29, 'weight': 63.546},
    'zinc': {'symbol': 'zn', 'number': 30, 'weight': 65.38},
    'gallium': {'symbol': 'ga', 'number': 31, 'weight': 69.723},
    'germanium': {'symbol': 'ge', 'number': 32, 'weight': 72.64},
    'arsenic': {'symbol': 'as', 'number': 33, 'weight': 74.9216},
    'selenium': {'symbol': 'se', 'number': 34, 'weight': 78.96},
    'bromine': {'symbol': 'be', 'number': 35, 'weight': 79.904},
    'krypton': {'symbol': 'kr', 'number': 36, 'weight': 83.798},
    'rubidium': {'symbol': 'rb', 'number': 37, 'weight': 85.4678},
    'strontium': {'symbol': 'sr', 'number': 38, 'weight': 87.62},
    'yttrium': {'symbol': 'y', 'number': 39, 'weight': 88.90585},
    'zirconium': {'symbol': 'zr', 'number': 40, 'weight': 91.224},
    'niobium': {'symbol': 'nb', 'number': 41, 'weight': 92.90638},
    'molybdenum': {'symbol': 'mo', 'number': 42, 'weight': 95.96},
    'technetium': {'symbol': 'tc', 'number': 43, 'weight': 97.9072},
    'ruthenium': {'symbol': 'ru', 'number': 44, 'weight': 101.07},
    'rhodium': {'symbol': 'rh', 'number': 45, 'weight': 102.90550},
    'palladium': {'symbol': 'pd', 'number': 46, 'weight': 106.42},
    'silver': {'symbol': 'ag', 'number': 47, 'weight': 107.8682},
    'cadmium': {'symbol': 'cd', 'number': 48, 'weight': 112.411},
    'indium': {'symbol': 'in', 'number': 49, 'weight': 114.818},
    'tin': {'symbol': 'sn', 'number': 50, 'weight': 118.710},
    'antimony': {'symbol': 'sb', 'number': 51, 'weight': 121.760},
    'tellurium': {'symbol': 'te', 'number': 52, 'weight': 127.60},
    'iodine': {'symbol': 'i', 'number': 53, 'weight': 126.90447},
    'xenon': {'symbol': 'xe', 'number': 54, 'weight': 131.293},
    'cesium': {'symbol': 'cs', 'number': 55, 'weight': 132.9054519},
    'barium': {'symbol': 'ba', 'number': 56, 'weight': 137.327},
    'lanthanum': {'symbol': 'la', 'number': 57, 'weight': 138.90547},
    'cerium': {'symbol': 'ce', 'number': 58, 'weight': 140.116},
    'praseodymium': {'symbol': 'pr', 'number': 59, 'weight': 140.90765},
    'neodymium': {'symbol': 'nd', 'number': 60, 'weight': 144.242},
    'promethium': {'symbol': 'pm', 'number': 61, 'weight': 145.0},
    'samarium': {'symbol': 'sm', 'number': 62, 'weight': 150.36},
    'europium': {'symbol': 'eu', 'number': 63, 'weight': 151.964},
    'gadolinium': {'symbol': 'gd', 'number': 64, 'weight': 157.25},
    'terbium': {'symbol': 'tb', 'number': 65, 'weight': 158.92535},
    'dysprosium': {'symbol': 'dy', 'number': 66, 'weight': 162.500},
    'holmium': {'symbol': 'ho', 'number': 67, 'weight': 164.93032},
    'erbium': {'symbol': 'er', 'number': 68, 'weight': 167.259},
    'thulium': {'symbol': 'tm', 'number': 69, 'weight': 168.93421},
    'ytterbium': {'symbol': 'yb', 'number': 70, 'weight': 173.054},
    'lutetium': {'symbol': 'lu', 'number': 71, 'weight': 174.9668},
    'hafnium': {'symbol': 'hf', 'number': 72, 'weight': 178.49},
    'tantalum': {'symbol': 'ta', 'number': 73, 'weight': 180.94788},
    'tungsten': {'symbol': 'w', 'number': 74, 'weight': 183.84},
    'rhenium': {'symbol': 're', 'number': 75, 'weight': 186.207},
    'osmium': {'symbol': 'os', 'number': 76, 'weight': 190.23},
    'iridium': {'symbol': 'ir', 'number': 77, 'weight': 192.217},
    'platinum': {'symbol': 'pt', 'number': 78, 'weight': 195.084},
    'gold': {'symbol': 'au', 'number': 79, 'weight': 196.966569},
    'mercury': {'symbol': 'hg', 'number': 80, 'weight': 200.59},
    'thallium': {'symbol': 'tl', 'number': 81, 'weight': 204.3833},
    'lead': {'symbol': 'pb', 'number': 82, 'weight': 207.2},
    'bismuth': {'symbol': 'bi', 'number': 83, 'weight': 208.98040},
    'polonium': {'symbol': 'po', 'number': 84, 'weight': np.nan},
    'astatine': {'symbol': 'at', 'number': 85, 'weight': np.nan},
    'radon': {'symbol': 'rn', 'number': 86, 'weight': np.nan},
    'francium': {'symbol': 'fr', 'number': 87, 'weight': np.nan},
    'radium': {'symbol': 'ra', 'number': 88, 'weight': np.nan},
    'actinium': {'symbol': 'ac', 'number': 89, 'weight': np.nan},
    'thorium': {'symbol': 'th', 'number': 90, 'weight': np.nan},
    'protactinium': {'symbol': 'pa', 'number': 91, 'weight': np.nan},
    'uranium': {'symbol': 'u', 'number': 92, 'weight': np.nan},
}
# add atomic weight [gram]
for element_name in element:
    element[element_name]['mass'] = element[element_name]['weight'] * amu_mass

# conversion dictionaries
element_name_from_symbol = {}
element_symbol_from_name = {}
element_number_from_name = {}
element_name_from_number = {}
element_number_from_symbol = {}
element_symbol_from_number = {}
for element_name in element:
    element_symbol = element[element_name]['symbol']
    element_number = element[element_name]['number']
    element_name_from_symbol[element_symbol] = element_name
    element_symbol_from_name[element_name] = element_symbol
    element_name_from_number[element_number] = element_name
    element_number_from_name[element_name] = element_number
    element_number_from_symbol[element_symbol] = element_number
    element_symbol_from_number[element_number] = element_symbol


# solar element abundances -------------------------------------------------------------------------
# massfraction := element mass / total mass
# abundance := element number / hydrogen number

# Solar abundances from Asplund et al 2009, photosphere
sun_photosphere_metals_mass_fraction = 0.0134
sun_photosphere_helium_mass_fraction = 0.2485
sun_photosphere_hydrogen_mass_fraction = 0.7381

# Solar abundances from Asplund et al 2009, proto-solar (bulk composition) (FIRE-3 default)
sun_protosolar_metals_mass_fraction = 0.0142
sun_protosolar_helium_mass_fraction = 0.2703
sun_protosolar_hydrogen_mass_fraction = 0.7154

# Solar abundances from Anders & Grevesse 1989 (FIRE-2 default)
# sun_metals_mass_fraction = 0.02
# sun_helium_mass_fraction = 0.274
# sun_hydrogen_mass_fraction = 0.706


# Solar abundances from Asplund et al 2009, photosphere (Table 1), up to atomic number 83
sun_photosphere_abundance = {
    1: 12.00,
    2: 10.93,
    3: 1.05,
    4: 1.38,
    5: 2.70,
    6: 8.43,
    7: 7.83,
    8: 8.69,
    9: 4.56,
    10: 7.93,
    11: 6.24,
    12: 7.60,
    13: 6.45,
    14: 7.51,
    15: 5.41,
    16: 7.12,
    17: 5.50,
    18: 6.40,
    19: 5.03,
    20: 6.34,
    21: 3.15,
    22: 4.95,
    23: 3.93,
    24: 5.64,
    25: 5.43,
    26: 7.50,
    27: 4.99,
    28: 6.22,
    29: 4.19,
    30: 4.56,
    31: 3.04,
    32: 3.65,
    33: 2.30,
    34: 3.34,
    35: 2.54,
    36: 3.25,
    37: 2.52,
    38: 2.87,
    39: 2.21,
    40: 2.58,
    41: 1.46,
    42: 1.88,
    43: 0.00,
    44: 1.75,
    45: 0.91,
    46: 1.57,
    47: 0.94,
    48: 1.71,
    49: 0.80,
    50: 2.04,
    51: 1.01,
    52: 2.18,
    53: 1.55,
    54: 2.24,
    55: 1.08,
    56: 2.18,
    57: 1.10,
    58: 1.58,
    59: 0.72,
    60: 1.42,
    61: 0.00,
    62: 0.96,
    63: 0.52,
    64: 1.07,
    65: 0.30,
    66: 1.10,
    67: 0.48,
    68: 0.92,
    69: 0.10,
    70: 0.84,
    71: 0.10,
    72: 0.85,
    73: -0.12,
    74: 0.85,
    75: 0.26,
    76: 1.40,
    77: 1.38,
    78: 1.62,
    79: 0.92,
    80: 1.17,
    81: 0.90,
    82: 1.75,
    83: 0.65,
}
# add element name and symbol as dictionary keys
for element_number in list(sun_photosphere_abundance.keys()):
    element_name = element_name_from_number[element_number]
    sun_photosphere_abundance[element_name] = sun_photosphere_abundance[element_number]
    element_symbol = element_symbol_from_number[element_number]
    sun_photosphere_abundance[element_symbol] = sun_photosphere_abundance[element_number]

    # set the alpha abundance (O + Mg + Si)/3 and convert to table format of log(N_X / N_H) + 12
    # alpha = (10 ** (x['o'] - 12) + 10 ** (x['mg'] - 12) + 10 ** (x['si'] - 12)) / 3
    # sun_photosphere_abundance['alpha.3'] = np.log10(alpha) + 12
    # sun_photosphere_abundance['alpha'] = sun_photosphere_abundance['alpha.3']

    # do again for a 4-species alpha, including now Ca
    # alpha_4 = (alpha * 3 + 10 ** (x['ca'] - 12)) / 4
    # sun_photosphere_abundance['alpha.4'] = np.log10(alpha_4) + 12

    # do again for a 5-species alpha, including now S and Ca
    # alpha_5 = (alpha * 3 + 10 ** (x['s'] - 12) + 10 ** (x['ca'] - 12)) / 5
    # sun_photosphere_abundance['alpha.5'] = np.log10(alpha_5) + 12


# Solar abundances from Asplund et al 2009, proto-solar (Table 5), limited set
sun_protosolar_abundance = {
    'hydrogen': 12.0,
    'helium': 10.98,
    'carbon': 8.47,
    'nitrogen': 7.87,
    'oxygen': 8.73,
    'neon': 7.97,
    'magnesium': 7.64,
    'silicon': 7.55,
    'sulfur': 7.16,
    'argon': 6.44,
    'calcium': 6.38,
    'iron': 7.54,
}
# add element symbol as dictionary key
for element_name in list(sun_protosolar_abundance.keys()):
    element_symbol = element_symbol_from_name[element_name]
    sun_protosolar_abundance[element_symbol] = sun_protosolar_abundance[element_name]
    # element_number = element_number_from_name[element_name]
    # sun_protosolar_abundance[element_number] = sun_protosolar_abundance[element_name]


# default values of Solar abundances and mass fractions ----------
# (the mass fractions below may differ by up to a percent from default values in FIRE-2 or FIRE-3,
# given choices of mean atomic mass)
sun_abundance = {}
sun_massfraction = {}

sun_default = sun_protosolar_abundance

sun_massfraction['metals'] = sun_protosolar_metals_mass_fraction

for element_name in element:
    if element_name in sun_default:
        sun_abundance[element_name] = 10 ** (sun_default[element_name] - sun_default['hydrogen'])
        if element_name == 'hydrogen':
            sun_massfraction[element_name] = sun_protosolar_hydrogen_mass_fraction
        elif element_name == 'helium':
            sun_massfraction[element_name] = sun_protosolar_helium_mass_fraction
        else:
            sun_massfraction[element_name] = (
                sun_abundance[element_name]
                * (element[element_name]['weight'] / element['hydrogen']['weight'])
                * sun_protosolar_hydrogen_mass_fraction
            )
        # store abundances accessible by element symbol as well
        element_symbol = element_symbol_from_name[element_name]
        sun_abundance[element_symbol] = sun_abundance[element_name]
        sun_massfraction[element_symbol] = sun_massfraction[element_name]

# clean namespace
del (sun_default, element_name, element_number, element_symbol)
