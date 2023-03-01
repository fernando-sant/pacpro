# This file houses the functions to change the 'field of view' of our data.
# Indeed, it can be useful to compare the results obtained if the heat demand
# and/or the carbon intensity of electricity are hourly/monthly/yearly
# CLEF 11.V.2022

import pandas as pd
import os
from Dynamic_carbon_intensity import moyenne, moyenne_glissante, fenetre_glissante


def convert_country_code(code):
    """
    Small function to pass from a country code to the associated country name.
    """
    dico = {'FR': 'France',
            'BE': 'Belgium',
            'DE': 'Germany',
            'IT': 'Italy',
            'SP': 'Spain',
            'UK': 'Unted Kingdom',
            'UE': 'UE28'}
    return dico[code]


def convert_country_name(name):
    """
    Small function to pass from a country name to the associated country code.
    """
    dico = {'France': 'FR',
            'Belgium': 'BE',
            'Germany': 'DE',
            'Italy': 'IT',
            'Spain': 'SP',
            'Unted Kingdom': 'UK',
            'UE28': 'UE'}
    return dico[name]


def transpose_demand(country, year, fov):
    """
    Cette fonction pour créer des tableaux Excel de demande d'énergie constante sur le mois ou sur l'année.
    Pour moyenner sur les mois, choisissez fov = 'month'.
    Pour moyenner sur l'année, choisissez fov = 'year.
    """
    code_pays = convert_country_name(country)
    demand = pd.read_excel(
        code_pays + '_' + str(year) + '_variable_demand.xlsx')

    liste_full_dates = demand['date']
    demande_par_creneau = demand['heat_demand']
    n = len(liste_full_dates)

    var_demand = pd.DataFrame()
    var_demand['date'] = liste_full_dates

    if fov == 'month':

        mois = {'01': 0, '02': 0, '03': 0, '04': 0, '05': 0, '06': 0,
                '07': 0, '08': 0, '09': 0, '10': 0, '11': 0, '12': 0, }

        cpt_mois = {'01': 0, '02': 0, '03': 0, '04': 0, '05': 0, '06': 0,
                    '07': 0, '08': 0, '09': 0, '10': 0, '11': 0, '12': 0, }

        for i in range(n):
            nb_mois = str(liste_full_dates[i])[5:7:]
            cpt_mois[nb_mois] += 1 #pour compter le nombre de jour dans le mois?
            mois[nb_mois] += demande_par_creneau[i]

        for m in mois:
            mois[m] = mois[m]/cpt_mois[m]

        month_demand = []
        for date in liste_full_dates:
            month_demand.append(mois[str(date)[5:7:]])

        var_demand['heat_demand'] = month_demand

        var_demand.to_excel(str(os.getcwd()) + '\\' + code_pays +
                            '_' + str(year) + '_variable_demand_month.xlsx', index=False)

    elif fov == 'year':
        tot_demand = sum(demande_par_creneau)
        year_demand = [tot_demand/n for date in liste_full_dates]
        var_demand['heat_demand'] = year_demand
        var_demand.to_excel(str(os.getcwd()) + '\\' + code_pays +
                            '_' + str(year) + '_variable_demand_year.xlsx', index=False)


def transpose_carbon(country, year, fov):
    """
    Cette fonction pour créer des tableaux Excel d'intensité carbone constante sur le mois ou sur l'année.
    Pour moyenner sur les mois, choisissez fov = 'month'.
    Pour moyenner sur l'année, choisissez fov = 'year.
    """

    code_pays = convert_country_name(country)
    carbon = pd.read_excel(
        code_pays + '_' + str(year) + '_carbon_intensity.xlsx')

    carbon_exact = carbon['carbon_intensity']
    carbon_rolling = carbon['carbon_intensity_rolling_average']
    liste_full_dates = carbon['date']

    n = len(liste_full_dates)

    new_carbon = pd.DataFrame()
    new_carbon['date'] = liste_full_dates

    if fov == 'month':

        mois_exact = {'01': 0, '02': 0, '03': 0, '04': 0, '05': 0, '06': 0,
                      '07': 0, '08': 0, '09': 0, '10': 0, '11': 0, '12': 0, }

        mois_rolling = {'01': 0, '02': 0, '03': 0, '04': 0, '05': 0, '06': 0,
                        '07': 0, '08': 0, '09': 0, '10': 0, '11': 0, '12': 0, }

        cpt_mois = {'01': 0, '02': 0, '03': 0, '04': 0, '05': 0, '06': 0,
                    '07': 0, '08': 0, '09': 0, '10': 0, '11': 0, '12': 0, }

        for i in range(n):
            nb_mois = str(liste_full_dates[i])[5:7:]
            cpt_mois[nb_mois] += 1
            mois_exact[nb_mois] += carbon_exact[i]
            mois_rolling[nb_mois] += carbon_rolling[i]

        for m in mois_exact:
            mois_exact[m] = mois_exact[m]/cpt_mois[m]
            mois_rolling[m] = mois_rolling[m]/cpt_mois[m]

        month_carbon_exact = []
        month_carbon_rolling = []
        for date in liste_full_dates:
            month_carbon_exact.append(mois_exact[str(date)[5:7:]])
            month_carbon_rolling.append(mois_rolling[str(date)[5:7:]])

        new_carbon['carbon_intensity'] = month_carbon_exact
        new_carbon['carbon_intensity_rolling_average'] = moyenne_glissante(
            month_carbon_exact, fenetre_glissante)

        new_carbon.to_excel(str(os.getcwd()) + '\\' + code_pays +
                            '_' + str(year) + '_carbon_intensity_month.xlsx', index=False)

    elif fov == 'year':

        tot_demand_exact = sum(carbon_exact)
        tot_demand_rolling = sum(carbon_rolling)

        year_carbon_exact = [tot_demand_exact/n for date in liste_full_dates]
        year_carbon_rolling = [tot_demand_rolling /
                               n for date in liste_full_dates]

        new_carbon['carbon_intensity'] = year_carbon_exact
        new_carbon['carbon_intensity_rolling_average'] = year_carbon_rolling

        new_carbon.to_excel(str(os.getcwd()) + '\\' + code_pays +
                            '_' + str(year) + '_carbon_intensity_year.xlsx', index=False)


# transpose_carbon('France', 2019, 'month')
