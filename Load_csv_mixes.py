# This file is used to process the raw data we have and transform them so that they can be used by our code
# CLEF 24.III.2022

import pandas as pd
import math
import os
import numpy as np
import xlrd

# # BELGIUM (hourly data from 2019 given by electricitymap.org)

# # Importation des données
# # Copie du fichier (pour préserver le fichier original)
# # Suppression de la variable contenant le fichier original (pour libérer la mémoire)

# data_mix_BE_brut = pd.read_csv("BE 2019.csv")
# data_mix_BE = data_mix_BE_brut.copy()
# del data_mix_BE_brut

# # Suppression des colonnes inutiles à notre utilisation du fichier

# data_mix_BE.drop('created_at', axis=1, inplace=True)
# data_mix_BE.drop('updated_at', axis=1, inplace=True)
# data_mix_BE.drop('timestamp', axis=1, inplace=True)
# data_mix_BE.drop('zone_name', axis=1, inplace=True)

# data_mix_BE.drop('carbon_intensity_avg', axis=1, inplace=True)
# data_mix_BE.drop('carbon_intensity_discharge_avg', axis=1, inplace=True)
# data_mix_BE.drop('carbon_intensity_import_avg', axis=1, inplace=True)

# data_mix_BE.drop('total_storage_avg', axis=1, inplace=True)
# data_mix_BE.drop('total_discharge_avg', axis=1, inplace=True)
# data_mix_BE.drop('total_import_avg', axis=1, inplace=True)
# data_mix_BE.drop('total_export_avg', axis=1, inplace=True)
# data_mix_BE.drop('total_consumption_avg', axis=1, inplace=True)

# data_mix_BE.drop('production_sources', axis=1, inplace=True)
# data_mix_BE.drop('power_origin_percent_fossil_avg', axis=1, inplace=True)
# data_mix_BE.drop('power_origin_percent_renewable_avg', axis=1, inplace=True)
# data_mix_BE.drop('power_production_percent_fossil_avg', axis=1, inplace=True)
# data_mix_BE.drop('power_production_percent_renewable_avg',
#                  axis=1, inplace=True)

# data_mix_BE.drop('power_consumption_nuclear_avg', axis=1, inplace=True)
# data_mix_BE.drop('power_consumption_geothermal_avg', axis=1, inplace=True)
# data_mix_BE.drop('power_consumption_biomass_avg', axis=1, inplace=True)
# data_mix_BE.drop('power_consumption_coal_avg', axis=1, inplace=True)
# data_mix_BE.drop('power_consumption_wind_avg', axis=1, inplace=True)

# data_mix_BE.drop('power_consumption_solar_avg', axis=1, inplace=True)
# data_mix_BE.drop('power_consumption_hydro_avg', axis=1, inplace=True)
# data_mix_BE.drop('power_consumption_gas_avg', axis=1, inplace=True)
# data_mix_BE.drop('power_consumption_oil_avg', axis=1, inplace=True)
# data_mix_BE.drop('power_consumption_unknown_avg', axis=1, inplace=True)

# data_mix_BE.drop('power_consumption_battery_discharge_avg',
#                  axis=1, inplace=True)
# data_mix_BE.drop('power_consumption_hydro_discharge_avg', axis=1, inplace=True)
# data_mix_BE.drop('power_net_discharge_battery_avg', axis=1, inplace=True)
# data_mix_BE.drop('power_net_discharge_hydro_avg', axis=1, inplace=True)
# data_mix_BE.drop('power_net_import_DE_avg', axis=1, inplace=True)

# data_mix_BE.drop('carbon_intensity_exchange_DE_avg', axis=1, inplace=True)
# data_mix_BE.drop('power_net_import_FR_avg', axis=1, inplace=True)
# data_mix_BE.drop('carbon_intensity_exchange_FR_avg', axis=1, inplace=True)
# data_mix_BE.drop('power_net_import_GB_avg', axis=1, inplace=True)
# data_mix_BE.drop('carbon_intensity_exchange_GB_avg', axis=1, inplace=True)

# data_mix_BE.drop('power_net_import_LU_avg', axis=1, inplace=True)
# data_mix_BE.drop('carbon_intensity_exchange_LU_avg', axis=1, inplace=True)
# data_mix_BE.drop('power_net_import_NL_avg', axis=1, inplace=True)
# data_mix_BE.drop('carbon_intensity_exchange_NL_avg', axis=1, inplace=True)
# data_mix_BE.drop('latest_forecasted_wind_x_avg', axis=1, inplace=True)

# data_mix_BE.drop('latest_forecasted_wind_y_avg', axis=1, inplace=True)
# data_mix_BE.drop('latest_forecasted_solar_avg', axis=1, inplace=True)
# data_mix_BE.drop('latest_forecasted_temperature_avg', axis=1, inplace=True)
# data_mix_BE.drop('latest_forecasted_dewpoint_avg', axis=1, inplace=True)
# data_mix_BE.drop('latest_forecasted_precipitation_avg', axis=1, inplace=True)

# data_mix_BE.drop('latest_forecasted_price_avg', axis=1, inplace=True)
# data_mix_BE.drop('latest_forecasted_production_avg', axis=1, inplace=True)
# data_mix_BE.drop('latest_forecasted_consumption_avg', axis=1, inplace=True)
# data_mix_BE.drop('latest_forecasted_power_net_import_DE_avg',
#                  axis=1, inplace=True)
# data_mix_BE.drop('latest_forecasted_power_net_import_FR_avg',
#                  axis=1, inplace=True)

# data_mix_BE.drop('latest_forecasted_power_net_import_GB_avg',
#                  axis=1, inplace=True)
# data_mix_BE.drop('latest_forecasted_power_net_import_LU_avg',
#                  axis=1, inplace=True)
# data_mix_BE.drop('latest_forecasted_power_net_import_NL_avg',
#                  axis=1, inplace=True)
# data_mix_BE.drop('latest_forecasted_production_solar_avg',
#                  axis=1, inplace=True)
# data_mix_BE.drop('latest_forecasted_production_wind_avg', axis=1, inplace=True)


# # Renaming the columns

# data_mix_BE.rename(
#     columns={'carbon_intensity_production_avg': 'carbon_intensity'}, inplace=True)
# data_mix_BE.rename(columns={'total_production_avg': 'total'}, inplace=True)
# data_mix_BE.rename(
#     columns={'power_production_nuclear_avg': 'nuclear'}, inplace=True)
# data_mix_BE.rename(
#     columns={'power_production_geothermal_avg': 'geothermal'}, inplace=True)
# data_mix_BE.rename(
#     columns={'power_production_biomass_avg': 'biomass'}, inplace=True)
# data_mix_BE.rename(columns={'power_production_coal_avg': 'coal'}, inplace=True)
# data_mix_BE.rename(columns={'power_production_wind_avg': 'wind'}, inplace=True)
# data_mix_BE.rename(
#     columns={'power_production_solar_avg': 'solar'}, inplace=True)
# data_mix_BE.rename(
#     columns={'power_production_hydro_avg': 'hydraulic'}, inplace=True)
# data_mix_BE.rename(
#     columns={'power_production_gas_avg': 'natural_gas'}, inplace=True)
# data_mix_BE.rename(columns={'power_production_oil_avg': 'oil'}, inplace=True)
# data_mix_BE.rename(
#     columns={'power_production_unknown_avg': 'other'}, inplace=True)

# # Replace NaN values by 0
# data_mix_BE.fillna(0, inplace=True)

# # The columns that are left
# print(data_mix_BE.columns.tolist())

# somme01012019 = 0
# means_production = data_mix_BE.columns.tolist()[3::]

# n = len(means_production)

# for i in range(n):
#     nb = data_mix_BE.iloc[1, i+3]
#     if not math.isnan(nb):
#         somme01012019 += nb

# print(somme01012019)

# print(data_mix_BE.loc[1]["total"])

# biopropane 2020 : 0.074 kgCO2/kWh source ADEME

# path = os.getcwd()

# data_mix_BE.to_excel(str(path) +"\BE_2019_ready.xlsx", index=False)


# Ouverture du fichier Excel

# doc_BE_2019 = xlrd.open_workbook('BE_2019_ready.xlsx')

# feuille1 = doc_BE_2019.sheet_by_index(0)

# print(feuille1.cell_value(2, 70))


# Remplacement des dates

# data_BE_2019 = pd.read_excel(str(os.getcwd())+"\BE_2019.xlsx")

# data_BE_2019["date"] = '14/05/1610'
# data_BE_2019["heure"] = '00:00'

# n = data_BE_2019.shape

# print(data_BE_2019.loc[0, 'datetime'])

# for j in range(n[0]):
#     date_brute = data_BE_2019.loc[j, 'datetime']
#     data_BE_2019.loc[j, 'date'] = date_brute[:10:]
#     data_BE_2019.loc[j, 'heure'] = date_brute[11:16:]


# liste_dates = data_BE_2019['date']
# liste_heures = data_BE_2019['heure']


# print(data_BE_2019.head())

# Save to a new Excel file

# data_BE_2019.to_excel(str(os.getcwd())+"\BE_2019_ready.xlsx", index=False)


useful_columns = ['date',
                  'heure',
                  'carbon_intensity_production_avg',
                  'total_production_avg',
                  'power_production_nuclear_avg',
                  'power_production_geothermal_avg',
                  'power_production_biomass_avg',
                  'power_production_coal_avg',
                  'power_production_wind_avg',
                  'power_production_solar_avg',
                  'power_production_hydro_avg',
                  'power_production_gas_avg',
                  'power_production_oil_avg',
                  'power_production_unknown_avg']

# What to do with the 'other' column ???

# print(1)
# dataX = pd.read_excel(str(os.getcwd())+"\\New Belgique 2019.xlsx")
# print(2)
# dataX["date"] = '14/05/1610'
# print(3)
# dataX["heure"] = '00:00'
# print(4)
# n = dataX.shape
# print(n)

# for j in range(n[0]):
#     date_brute = str(dataX.loc[j, 'Datetime'])
#     dataX.loc[j, 'date'] = date_brute[:10:]
#     dataX.loc[j, 'heure'] = date_brute[11:16:]
#     print(round(j/n[0], 3))

# print(dataX.head())

# dataX.to_excel(str(os.getcwd())+"\BE_2019_opendata.xlsx", index=False)
