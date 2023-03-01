# Our data put into dataframes
# Each row corresponds to one country

import pandas as pd

# Electrical mixes of the countries
# I have grouped tide and hydraulic, as there is only 0.001 of tide only for France.
electricity_consumption_GWh_df = pd.read_csv("Electrical_mixes.csv", index_col='countries')

# How the residential buildings are heated, proportion
national_heating_df = pd.read_csv("Heating_mixes.csv", index_col='countries')

# Average emission factor of the electricity production, by country, kgCO2/kWh
avg_emissions_df = pd.read_csv("Avg_emissions.csv", index_col='countries')

# The efficiencies of heat pumps in each country
HP_efficiencies_df = pd.read_csv("HP_efficiencies.csv", index_col='countries')

# Specifications of the heating vectors in each country
def heating_vectors_df(country):
    e_f = avg_emissions_df.loc[country]['avg_emission']
    heating_vector_df = pd.read_csv("Heating_vectors.csv", index_col='vector')
    heating_vector_df.loc["ACHP", "emission_factor"] = e_f
    heating_vector_df.loc["GCHP", "emission_factor"] = e_f
    heating_vector_df.loc["resistive_heating", "emission_factor"] = e_f
    heating_vector_df.loc["ACHP", "yield"] = HP_efficiencies_df.loc[country]['ACHP']
    heating_vector_df.loc["GCHP", "yield"] = HP_efficiencies_df.loc[country]['GCHP']
    return heating_vector_df

# Here are the CO2 emissions for the different means of production of electricity
# Until we have the data for different countries, all of it is calculated for France
# (I believe it is not extremely different from one country to the other)
# Expressed in kgCO2/kWh
emissions_electricity_production_df = pd.read_csv("Electricity_prod.csv", index_col='countries')

# The yearly energy demands by country:
heating_demands_df = pd.read_csv("Heating_demands.csv", index_col='countries')