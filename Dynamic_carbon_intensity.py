# Ce code sert à calculer et sauvegarder dans un fichier Excel l'intensité carbone de l'électricité, dans un pays et pour une année.
# CLEF 14-15.IV.2022


import xlrd
import numpy as np
import datetime
import matplotlib.pyplot as plt
import pandas as pd
import math
import os
from datetime import datetime, timedelta
from matplotlib.ticker import NullFormatter
from matplotlib.dates import MonthLocator, DateFormatter


# Codes des pays

FR = 'France'
BE = 'Belgium'
DE = 'Germany'
IT = 'Italy'
SP = 'Spain'
UK = 'United Kingdom'
UE = 'UE28'


# Définition du périmètre

country = 'DE'
year = 2019


# Chargement des données

donnees = pd.read_excel(country + '_' + str(year) + "_electric_mix.xlsx")


# Colonnes correspondant à une production d'électricité

electricity_prod_columns = list(donnees.columns)
electricity_prod_columns.remove('date')
electricity_prod_columns.remove('total')


# Contruction du dataframe de sortie

carbon_intensity_df = pd.DataFrame()
carbon_intensity_df['date'] = donnees['date']


# Dictionnaire des facteurs d'émission en fonction du type de production

emissions_electricity_production = {'biomass': 0.032,          # source ADEME, Bois bûches - Combustion en chaudière
                                    'natural_gas': 0.418,      # source ADEME, Electricité - centrale gaz - production
                                    'coal': 1.06,              # source ADEME, Electricité - centrale charbon - production
                                    'oil': 0.73,               # source ADEME, Electricité - centrale fioul - production
                                    'geothermal': 0.045,       # source ADEME, Electricité - géothermie - production
                                    'nuclear': 0.006,          # source ADEME, Electricité - centrale nucléaire - production
                                    'other': 0.7,              # Hypothèse
                                    'other_renewable': 0.02,   # Hypothèse
                                    'solar': 0.0439,           # Source ADEME, Électricité - photovoltaïque - Fabrication Chine
                                    # Source FNADE, (cité dans https://www.actu-environnement.com/ae/news/emissions-co2-recyclage-incineration-37137.php4)
                                    'waste': 0.132,
                                    'wind': 0.0141,            # Source ADEME, Électricité - éolien terrestre - production
                                    'hydro': 0.006}            # Source ADEME, Electricité - hydraulique - production

emissions_factors_ipcc = {'biomass': 0.23,          # source ADEME, Bois bûches - Combustion en chaudière
                          'natural_gas': 0.490,      # source ADEME, Electricité - centrale gaz - production
                          'coal': 0.82,              # source ADEME, Electricité - centrale charbon - production
                          'oil': 0.65,               # source ADEME, Electricité - centrale fioul - production
                          'geothermal': 0.038,       # source ADEME, Electricité - géothermie - production
                          'nuclear': 0.012,          # source ADEME, Electricité - centrale nucléaire - production
                          'other': 0.7,              # Hypothèse
                          'other_renewable': 0.02,   # Hypothèse
                          'solar': 0.045,           # Source ADEME, Électricité - photovoltaïque - Fabrication Chine
                          # Source FNADE, (cité dans https://www.actu-environnement.com/ae/news/emissions-co2-recyclage-incineration-37137.php4)
                          'waste': 0.132,
                          'wind': 0.011,            # Source ADEME, Électricité - éolien terrestre - production
                          'hydro': 0.024}            # Source ADEME, Electricité - hydraulique - production


n = donnees.shape
computed_carbon_intensity = []
computed_ipcc = []

for j in range(n[0]):
    intensity = 0
    dynamic_mix = []
    dynamic_mix2 = []
    for means in electricity_prod_columns:
        contribution = donnees.loc[j, means]
        contribution = contribution / donnees.loc[j, 'total']
        increment = contribution * \
            emissions_electricity_production[str(means)]
        dynamic_mix.append(increment)
        increment2 = contribution * \
            emissions_factors_ipcc[str(means)]
        dynamic_mix2.append(increment2)
    computed_carbon_intensity.append(sum(dynamic_mix)*1000)
    computed_ipcc.append(sum(dynamic_mix2)*1000)

carbon_intensity_df['carbon_intensity'] = computed_carbon_intensity
# carbon_intensity_df['carbon_intensity2'] = computed_ipcc

# # Pour afficher les résultats heure par heure sur l'année :

# plt.plot(carbon_intensity_df['carbon_intensity'], label='Data ADEME')
# plt.plot(carbon_intensity_df['carbon_intensity2'],
#          label='Data Electricity Map')
# plt.legend(fontsize=15)
# plt.show()


# Pour afficher les résultats lissés :

def moyenne(liste):
    return(sum(liste)/len(liste))


def moyenne_glissante(liste, taille_fenetre):
    n = len(liste)
    if n < 2*taille_fenetre+1:
        print('La taille de fenêtre choisie est trop grande pour cette liste')
    else:
        liste_moyennee = []
        for i in range(taille_fenetre):
            elt_moy = moyenne(liste[:i+taille_fenetre+1])
            liste_moyennee.append(elt_moy)
        for i in range(taille_fenetre, n-taille_fenetre):
            elt_moy = moyenne(liste[i-taille_fenetre:i+taille_fenetre+1])
            liste_moyennee.append(elt_moy)
        for i in range(n-taille_fenetre, n):
            elt_moy = moyenne(liste[i-taille_fenetre:])
            liste_moyennee.append(elt_moy)
        return liste_moyennee


fenetre_glissante = 720  # en heures avant et après chaque instant


carbon_intensity_smoothed = moyenne_glissante(
    carbon_intensity_df['carbon_intensity'], fenetre_glissante)
# carbon_intensity_smoothed2 = moyenne_glissante(
#     carbon_intensity_df['carbon_intensity2'], fenetre_glissante)


carbon_intensity_df['carbon_intensity_rolling_average'] = carbon_intensity_smoothed
# carbon_intensity_df['carbon_intensity_rolling_average2'] = carbon_intensity_smoothed2


# Sauvegarde des résultats dans un excel

carbon_intensity_df.to_excel(
    str(os.getcwd()) + "\\" + country + '_' + str(year) + '_carbon_intensity.xlsx', index=False)


# # Pour afficher les résultats lissés sur l'année :

# plt.plot(
#     carbon_intensity_df['carbon_intensity_rolling_average'], label='Data ADEME')
# plt.plot(carbon_intensity_df['carbon_intensity_rolling_average2'],
#          label='Data Electricity Map')
# plt.legend(fontsize=15)
# plt.show()

# # generate list of dates from 01.01.2019 to 31.12.2019 through 1 hour
# dates = list()
# dates.append(datetime.strptime('2019-01-01 00:00', '%Y-%m-%d %H:%M'))
# for i in range(n[0]-1):
#     dates.append(dates[-1] + timedelta(hours=1))

# # plot with dates
# plt.plot(dates, carbon_intensity_smoothed,
#          label='Carbon intensity of electricity')
# ax = plt.gca()

# # set dates limits
# ax.set_xlim([dates[0], dates[-1]])

# # formatters' options
# ax.xaxis.set_major_locator(MonthLocator())
# ax.xaxis.set_minor_locator(MonthLocator(bymonthday=15))
# ax.xaxis.set_major_formatter(NullFormatter())
# ax.xaxis.set_minor_formatter(DateFormatter('%b'))


# plt.ylabel('Emission factor of electricity [g/kWh]')


# plt.show()
