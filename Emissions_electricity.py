# Ce code sert à calculer les émissions de CO2 induites sur une année par les chauffages à l'électricité,
# c'est-à-dire le chauffage résistif et les pompes à chaleur.
# CLEF 15.IV.2022

import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from matplotlib.ticker import NullFormatter
from matplotlib.dates import MonthLocator, DateFormatter
from post_processing import rc_param
from Different_fov import transpose_demand, transpose_carbon, convert_country_code, convert_country_name


def electric_heating_emissions(country, year, heating_type, hp_specs, vectors, fov_d, demand_transf_fct, fov_c, carbon_transf_fct):
    '''
    Cette fonction calcule les émissions de CO2 des moyens de chauffage électriques sur une année dans un pays.
    heating_type = 'resistive_heating' or 'ACHP' or 'GCHP
    '''
    country_name = convert_country_code(country)

    # Gestion de FOV pour la demande

    if fov_d == 'hour':
        demand = pd.read_excel(country + '_' +
                               str(year) + '_variable_demand.xlsx')

    elif fov_d in ['month', 'year']:
        demand_transf_fct(country_name, year, fov_d)
        demand = pd.read_excel(country + '_' +
                               str(year) + '_variable_demand_' + fov_d + '.xlsx')

    # Gestion de FOV pour l'intensité carbone

    if fov_c == 'hour':
        carbon_intensity_elec = pd.read_excel(
            country + '_' + str(year) + '_carbon_intensity.xlsx')
    elif fov_c in ['month', 'year']:
        carbon_transf_fct(country_name, year, fov_c)
        carbon_intensity_elec = pd.read_excel(
            country + '_' + str(year) + '_carbon_intensity_' + fov_c + '.xlsx')

    # Importation des données
    heating_vectors = pd.read_csv(vectors).set_index('vector')
    heat_pumps = pd.read_csv(hp_specs).set_index('countries')

    # Définition du rendement pour les moyens de chauffage électriques
    if heating_type == 'resistive_heating':
        efficiency = heating_vectors.loc['resistive_heating', 'yield']
    elif heating_type == 'ACHP':
        efficiency = heat_pumps.loc[convert_country_code(
            country), 'ACHP']
    elif heating_type == 'GCHP':
        efficiency = heat_pumps.loc[convert_country_code(
            country), 'GCHP']

    # Initialisation des résultats
    emissions_exact = 0
    emissions_rolling = 0

    n = demand.shape

    # Application de la formule générale des émissions
    for i in range(n[0]):
        emissions_exact += demand['heat_demand'][i] * \
            carbon_intensity_elec['carbon_intensity'][i]/efficiency
        emissions_rolling += demand['heat_demand'][i] * \
            carbon_intensity_elec['carbon_intensity_rolling_average'][i]/efficiency

    print('Émissions avec facteur exact :', emissions_exact/1000, 'kgCO2')
    print('Émissions avec facteur glissant :', emissions_rolling/1000, 'kgCO2')

    return emissions_exact/1000


# electric_heating_emissions('BE', 2019, 'ACHP', 'HP_efficiencies.csv',
#                            'Heating_vectors.csv', 'hour', transpose_demand, 'hour', transpose_carbon)


def graph_european_electricity_carbon(year):
    """
    To plot the hourly carbon intensity of electricity for the three european countries.
    """

    elec_carbon_FR = pd.read_excel(
        'FR_' + str(year) + '_carbon_intensity.xlsx')
    elec_carbon_DE = pd.read_excel(
        'DE_' + str(year) + '_carbon_intensity.xlsx')
    elec_carbon_BE = pd.read_excel(
        'BE_' + str(year) + '_carbon_intensity.xlsx')

    # plot with dates
    dates = list(elec_carbon_FR['date'])
    plt.plot(dates, elec_carbon_FR['carbon_intensity_rolling_average'],
             label='France')
    plt.plot(dates, elec_carbon_DE['carbon_intensity_rolling_average'],
             label='Germany')
    plt.plot(dates, elec_carbon_BE['carbon_intensity_rolling_average'],
             label='Belgium')
    ax = plt.gca()

    # set dates limits
    ax.set_xlim([dates[0], dates[-1]])

    # formatters' options
    ax.xaxis.set_major_locator(MonthLocator())
    ax.xaxis.set_minor_locator(MonthLocator(bymonthday=15))
    ax.xaxis.set_major_formatter(NullFormatter())
    ax.xaxis.set_minor_formatter(DateFormatter('%b'))

    plt.ylabel('Emission factor of electricity [g/kWh]')
    plt.legend()
    plt.show()

# graph_european_electricity_carbon(2019)


def graph_fov_carbon_intensity(country, year):
    carbon_hour = pd.read_excel(
        country + '_' + str(year) + '_carbon_intensity.xlsx')
    carbon_month = pd.read_excel(
        country + '_' + str(year) + '_carbon_intensity_month.xlsx')
    carbon_year = pd.read_excel(
        country + '_' + str(year) + '_carbon_intensity_year.xlsx')

    plt.plot(carbon_hour['carbon_intensity'], label='HOUR')
    plt.plot(carbon_month['carbon_intensity'], label='MONTH')
    plt.plot(carbon_year['carbon_intensity'], label='YEAR')

    plt.legend()
    plt.title('Carbon intensity throughout the year ' +
              country + ' ' + str(year))

    plt.show()

# graph_fov_carbon_intensity('FR', 2019)


def national_house_heating_dynamic(country_code, year, heating_mix, heating_specs, hp_specs, methode, fov_d, demand_transf_fct, fov_c, carbon_transf_fct):
    """
    Cette fonction calcule les émissions de CO2 pour une maison et une année, en tenant compte de variabilité temporelle de la demande
    et de l'intensité carbone. Trois options sont possibles pour ces deux paramètres : 'hour', 'month' et 'year', selon la période de
    temps sur laquelle on veut moyenner ces paramètres.
    """

    # On récupère la demande variable dans le fichier dédié

    country_name = convert_country_code(country_code)

    if fov_d == 'hour':
        demand = pd.read_excel(country_code + '_' +
                               str(year) + '_variable_demand.xlsx')

    elif fov_d in ['month', 'year']:
        demand_transf_fct(country_name, year, fov_d)
        demand = pd.read_excel(country_code + '_' +
                               str(year) + '_variable_demand_' + fov_d + '.xlsx')

    # Calcul de la demande globale sur l'année
    yearly_energy_demand = sum(list(demand['heat_demand']))

    if fov_c == 'hour':
        carbon_intensity_elec = pd.read_excel(
            country_code + '_' + str(year) + '_carbon_intensity.xlsx')
    elif fov_c in ['month', 'year']:
        carbon_transf_fct(country_name, year, fov_c)
        carbon_intensity_elec = pd.read_excel(
            country_code + '_' + str(year) + '_carbon_intensity_' + fov_c + '.xlsx')

    # Importation des données
    daf = pd.read_csv(heating_specs).set_index('vector').copy()
    daf.rename(index={'wood_closed_hearth': 'wood',
                      'ACHP': 'heat_pump'}, inplace=True)
    heating_mix = pd.read_csv(heating_mix).set_index('countries').copy()
    hp_data = pd.read_csv(hp_specs).set_index('countries').copy()

    # On calcule les émissions pour chaque pas de temps

    # Initialisation des résultats
    emissions_tot = 0
    dynamic_emissions = []

    # Calcul du nombre de pas de temps
    n = len(list(demand['date']))

    # On les parcourt tous
    for i in range(n):

        # Initialisation des émissions du pas de temps
        increment_creneau = 0

        # Obtention de la demande de chaleur pour ce pas de temps
        demande_creneau = demand['heat_demand'][i]

        # On parcourt les moyens de chauffage pour calculer les émissions de chacun sur le pas de temps
        for vector in heating_mix:

            # On distinque d'une part les moyens de chauffage avec facteur d'émission fixe
            if vector not in ['heat_pump', 'resistive_heating']:
                increment_vector = heating_mix.loc[country_name, vector] * daf.loc[vector,
                                                                                   'emission_factor']/daf.loc[vector, 'yield'] * demande_creneau

                increment_creneau += increment_vector

            # D'autre part les moyens de chauffage à l'électricité, à facteur d'émission variable
            else:

                # On regarde quelle colonne d'intensité carbone prendre
                if methode == 'exact':
                    column_used = 'carbon_intensity'
                elif methode == 'rolling':
                    column_used = 'carbon_intensity_rolling_average'

                # On distingue les moyens d'obtenir le rendement entre HP et radiateurs électriques
                if vector == 'heat_pump':
                    efficiency = hp_data.loc[country_name, 'ACHP']
                elif vector == 'resistive_heating':
                    efficiency = daf.loc[vector, 'yield']

                electric_vector_emissions = demande_creneau * \
                    carbon_intensity_elec.loc[i, column_used]/1000 / efficiency
                increment_vector = heating_mix.loc[country_name,
                                                   vector] * electric_vector_emissions

                increment_creneau += increment_vector

        emissions_tot += increment_creneau
        dynamic_emissions.append(increment_creneau)

    return emissions_tot, dynamic_emissions


# res = national_house_heating_dynamic('BE', 2019, 'Heating_mixes.csv',
#                                      'Heating_vectors.csv', 'HP_efficiencies.csv', 'exact',
#                                      'hour', transpose_demand, 'hour', transpose_carbon)
# print(res[0])
# plt.plot(res[1])
# plt.ylabel('CO2 emissions [kgCO2/hour] during the year, BE 2019')
# plt.show()


def barchart_house_emissions_dynamic(year, heating, heat_vectors, hp_specs, method, fct_emissions, vector, fictive_house_fct,  fov_d, demand_transf_fct, fov_c, carbon_transf_fct):
    """
    This function arranges the results of the previous function into a nice barchart.
    """

    # The post-processing function to size the graph correctly
    rc_param(1, 1.3, 1, 'beamer')

    heating_mix = pd.read_csv(heating).set_index('countries').copy()
    n = len(heating_mix.index)
    legend = [heating_mix.index[i] for i in range(n)]

    # Values of the cuurent emissions with thte current heating mix
    values1 = []
    for country in legend:
        country_code = convert_country_name(country)
        values1.append(fictive_house_fct(country_code, year,
                                         heating, heat_vectors, hp_specs, method, fov_d, demand_transf_fct, fov_c, carbon_transf_fct)[0])

    plt.ylabel('Emissions [kgCO2]')
    colors1 = ['orangered', 'green', 'royalblue']
    plt.bar(legend, values1, 0.5, color=colors1)

    # Adding text on top of the bars
    for i, v in enumerate(values1):
        plt.text(i - 0.15, v + 100, str(round(v)),
                 color='black', fontweight='light')

    # Values of the would-be emissions if only HP were used
    values2 = []
    for country in legend:
        country_code = convert_country_name(country)
        values2.append(fct_emissions(country_code, year,
                                     vector, hp_specs, heat_vectors))

    colors2 = ['salmon', 'mediumseagreen', 'cornflowerblue']
    plt.bar(legend, values2, 0.5, color=colors2)

    # Adding text on top of the bars
    for i, v in enumerate(values2):
        plt.text(i - 0.15, v + 100, str(round(v)),
                 color='black', fontweight='light')

    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.show()


# barchart_house_emissions_dynamic(2019, 'Heating_mixes.csv', 'Heating_vectors.csv', 'HP_efficiencies.csv',
#                                  'exact', electric_heating_emissions, 'ACHP', national_house_heating_dynamic,
#                                  'hour', transpose_demand, 'hour', transpose_carbon)
