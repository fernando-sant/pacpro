# P17 NCE S7 Project
# CO2 Emissions savings with Installation of a Heat Pump
# Albert, Darrobers, David, Grimme, Hippolite, Lurion

import matplotlib.pyplot as plt
from Project_NCE_functions import *
from Project_NCE_Data_df import *

# Abbreviations for countries :
FR = "France"
DE = "Germany"
BE = "Belgium"

# Thermal heating energy demand (space and water heating) per year for one house of 102.2 m² in kWh:
demand_FR = 15402
demand_DE = 15494
demand_BE = 20440

########################################################################################################################
# To compare the emission factors of electricity with their computed values, please uncomment section below:

# data_efe_FR = avg_emissions_df.loc[FR]['avg_emission']
# data_efe_DE = avg_emissions_df.loc[DE]['avg_emission']
# data_efe_BE = avg_emissions_df.loc[BE]['avg_emission']
#
# comp_efe_FR = round(compute_avg_electricity_emissions(FR,
#                     electricity_consumption_GWh_df, emissions_electricity_production_df), 3)
# comp_efe_DE = round(compute_avg_electricity_emissions(DE,
#                     electricity_consumption_GWh_df, emissions_electricity_production_df), 3)
# comp_efe_BE = round(compute_avg_electricity_emissions(BE,
#                     electricity_consumption_GWh_df, emissions_electricity_production_df), 3)
#
# print("France emits " + str(data_efe_FR) + " kgCO2/kWh for electricity production.\n"
#       "Computed value is " + str(comp_efe_FR) + " kgCO2/kWh.\n")
# print("Germany emits " + str(data_efe_DE) + " kgCO2/kWh for electricity production.\n"
#       "Computed value is " + str(comp_efe_DE) + " kgCO2/kWh.\n")
# print("Belgium emits " + str(data_efe_BE) + " kgCO2/kWh for electricity production.\n"
#       "Computed value is " + str(comp_efe_BE) + " kgCO2/kWh.\n")

########################################################################################################################
# To know what the fictive houses emit in each country, please uncomment section below:

# house_emissions_BE = national_house_heating(BE, heating_demands_df, national_heating_df, heating_vectors_df(BE))
# house_emissions_FR = national_house_heating(FR, heating_demands_df, national_heating_df, heating_vectors_df(FR))
# house_emissions_DE = national_house_heating(DE, heating_demands_df, national_heating_df, heating_vectors_df(DE))
# print("The Belgian fictive house emits " + str(round(house_emissions_BE)) + " kgCO2 per year.")
# print("The French fictive house emits " + str(round(house_emissions_FR)) + " kgCO2 per year.")
# print("The German fictive house emits " + str(round(house_emissions_DE)) + " kgCO2 per year.")

########################################################################################################################
# To see the electrical mix of a country, please uncomment section below:

# country = DE
# piechart_mix(country, electricity_consumption_GWh_df)

########################################################################################################################
# To see what the emissions with each heating system are in a country, please uncomment section below:

# country = DE
# barchart_emissions(country, heating_demands_df, heating_vectors_df)

########################################################################################################################
# To see the emissions of all the heating systems compared by country, please uncomment section below:

# barchart_emissions3(heating_demands_df, heating_vectors_df, avg_emissions_df)

########################################################################################################################
# To create a legend for the barchart_emissions and barchart_emissions3 graphs, please uncomment section below:

# legend_creator(compute_emissions('Belgium', heating_demands_df, heating_vectors_df))

########################################################################################################################
# To see the comparison between the fictive houses' emissions and the emissions of a heat pump (ACHP), please
# uncomment section below:

# barchart_house_emissions(heating_demands_df, national_heating_df, heating_vectors_df,
#                          compute_emissions, 'ACHP', national_house_heating)
