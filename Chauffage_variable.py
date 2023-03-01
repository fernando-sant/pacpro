# Implémentation de la demande variable de chauffage sur une année.
# CLEF 13.IV.2022

from Project_NCE_Data_df import *
from Load_csv_mixes import *
import matplotlib.pyplot as plt
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

year = 2019
country = FR
code_pays = 'FR'

# Obtention des demandes globales sur l'année

yearly_space_heating = heating_demands_df.loc[country]['yearly_space_heating']
yearly_water_heating = heating_demands_df.loc[country]['yearly_water_heating']


# Construction des colonnes de la date et de l'heure

creneau = 60  # Durée de l'intervalle de temps en minutes

current_date = datetime(year, 1, 1, 0, 0)

liste_full_dates = [current_date]
# liste_dates = [str(current_date)[:10:]]
# liste_heures = [str(current_date)[11:16:]]

while str(current_date + timedelta(minutes=creneau))[:4:] == str(year):
    current_date = current_date + timedelta(minutes=creneau)
    liste_full_dates.append(current_date)
    # liste_dates.append(str(current_date)[:10:])
    # liste_heures.append(str(current_date)[11:16:])


nombre_creneaux = len(liste_full_dates)


# Création du dataframe de sortie

var_demand = pd.DataFrame()
var_demand['date'] = liste_full_dates


# Demande thermique par créneau de temps


eau_chaude_par_creneau = [yearly_water_heating /
                          nombre_creneaux for n in range(nombre_creneaux)]
chauffage_par_creneau = []
demande_par_creneau = []


# Amplitude du cosinus pour la demande en chauffage spatial
A = yearly_space_heating/(nombre_creneaux*creneau)

# Pour chaque créneau, on calcule la demande avec la formule théorique de l'intégration du cosinus
for n in range(nombre_creneaux):
    chauffage_par_creneau.append(creneau*A*(1 + nombre_creneaux/np.pi*np.cos(
        np.pi*(2*n+1)/nombre_creneaux)*np.sin(np.pi/nombre_creneaux)))
    demande_par_creneau.append(
        chauffage_par_creneau[n] + eau_chaude_par_creneau[n])

# somme_test = 0
# for elt in chauffage_par_creneau:
#     somme_test += elt

# print(somme_test)


# # Plot with dates
# plt.plot(liste_full_dates, demande_par_creneau)
# ax = plt.gca()

# # set dates limits
# ax.set_xlim([liste_full_dates[0], liste_full_dates[-1]])

# # formatters' options
# ax.xaxis.set_major_locator(MonthLocator())
# ax.xaxis.set_minor_locator(MonthLocator(bymonthday=15))
# ax.xaxis.set_major_formatter(NullFormatter())
# ax.xaxis.set_minor_formatter(DateFormatter('%b'))

# plt.plot(eau_chaude_par_creneau)

# y_max = max(demande_par_creneau)*1.1
# plt.ylim(0, y_max)

# plt.ylabel('Demande thermique [kWh/15min]')

# plt.show()


var_demand['heat_demand'] = demande_par_creneau

# Sauvegarde dans un fichier Excel

var_demand.to_excel(str(os.getcwd()) + '\\' + code_pays +
                    '_' + str(year) + '_variable_demand.xlsx', index=False)
