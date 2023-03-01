from Project_NCE_Data_df import *
import matplotlib.pyplot as plt
import numpy as np
from post_processing import rc_param


def piechart_mix(country, national_mixes):
    n = len(national_mixes.keys())
    labels = [national_mixes.keys()[i] for i in range(1, n)]
    total = [national_mixes.loc[country][label] for label in labels]
    rc_param(1, 1, 1, 'beamer')
    pie = plt.pie(total, startangle=0, radius=1.5, normalize=True)
    labels_legend = labels
    for i in range(len(labels_legend)):
        labels_legend[i] = labels_legend[i] + ' ' + str(round(total[i]*100, 1)) + '%'
    plt.legend(pie[0], labels_legend, bbox_to_anchor=(0.87, 0.5), loc="center right",
               bbox_transform=plt.gcf().transFigure)
    plt.subplots_adjust(left=0.2, bottom=0.1, right=0.45)
    plt.show()


def compute_avg_electricity_emissions(country, electrical_mix, electricity_emissions):
    """
    This function computes the average CO2 intensity of electricity in a given country.
    :param country: Country for which the CO2 intensity of electricity is wanted.
    :param electrical_mix: dataframe in which each each row gives the electrical mix of a given country
    :param electricity_emissions: dataframe in which each row gives the CO2 intensity of the means of electricity
    production in a given country
    :return: the value of the emissions of electricity, in kgCO2/kWh
    """
    emissions = 0
    n = len(electrical_mix.keys())
    mix = [electrical_mix.keys()[i] for i in range(1, n)]
    for source in mix:
        emissions += electrical_mix.loc[country][source] * electricity_emissions.loc[country][source]
    return emissions


def compute_emissions(country, yearly_energy_demand, heating_mix):
    """
    This function computes the emissions of CO2 for a year of heating for one building and for different heating vectors
    """
    emissions = {}
    daf = heating_mix(country)
    vectors = daf.index
    for vector in vectors:
        emissions[vector] = yearly_energy_demand.loc[country]["yearly_energy_demand"] * daf.loc[vector]["emission_factor"]/daf.loc[vector]["yield"]
    return emissions


def barchart_emissions(country, yearly_energy_demand, heating_mix):
    """
    This function arranges the results of the previous function into a nice barchart.
    """
    rc_param(1, 1, 1, 'beamer')
    emissions = compute_emissions(country, yearly_energy_demand, heating_mix)
    values = []
    legend = []
    for elt in emissions:
        values.append(emissions[elt])
        legend.append(str(elt))
    plt.ylabel('Emissions (kgCO2)')
    colors = ['peru', 'sienna', 'darkgoldenrod', 'darkorange', 'darkorchid',
              'olive', 'forestgreen', 'limegreen', 'steelblue',
              'crimson', 'cyan']
    bar_width = 0.9
    plt.bar([i for i in range(len(legend))], values, bar_width, color=colors)
    plt.xticks(rotation=270)
    plt.xticks(color='w')
    plt.tight_layout()
    plt.show()


def barchart_emissions3(yearly_energy_demand, heating, df_countries):
    """
    Another version of the previous function
    Which makes only one chart for all the countries
    """
    rc_param(1, 1, 1, 'beamer')
    values = {}
    legend = []
    n = len(df_countries.index)
    countries = [df_countries.index[i] for i in range(n)]
    for country in countries:
        emissions = compute_emissions(country, yearly_energy_demand, heating)
        values[country] = []
        for elt in emissions:
            values[country].append(round(emissions[elt]))
            if str(elt) not in legend:
                legend.append(str(elt))
    m = len(legend)
    plt.ylabel('Emissions (kgCO2)')
    colors = ['peru', 'sienna', 'darkgoldenrod', 'darkorange', 'darkorchid',
              'olive', 'forestgreen', 'limegreen', 'steelblue',
              'crimson', 'cyan']
    bar_width = 0.9/n
    indices = [i for i in range(m)]
    for k in range(len(countries)):
        plt.bar([j + k * bar_width for j in indices], values[countries[k]], bar_width, color=colors, edgecolor='black')
    plt.xticks(rotation=270)
    plt.xticks(color='w')
    plt.tight_layout()
    plt.show()

# Now we compute the emissions of a fictive house, heated by the national heating mix.


def national_house_heating(country, yearly_energy_demand, heating_mix, heating_specs):
    emissions = 0
    daf = heating_specs.copy()
    daf.rename(index={'wood_closed_hearth': 'wood', 'ACHP': 'heat_pump'}, inplace=True)
    for vector in heating_mix:
        emissions += heating_mix.loc[country, vector] * daf.loc[vector, 'emission_factor']/daf.loc[vector, 'yield']
    return emissions * yearly_energy_demand.loc[country]["yearly_energy_demand"]


def barchart_house_emissions(yearly_energy_demand, heating, heat_vectors, fct_emissions, vector, fictive_house_fct):
    """This function arranges the results of the previous function into a nice barchart."""
    rc_param(1, 1.3, 1, 'beamer')
    n = len(heating.index)
    legend = [heating.index[i] for i in range(n)]
    values1 = [fictive_house_fct(country, yearly_energy_demand,
               heating, heat_vectors(country)) for country in legend]
    plt.ylabel('Emissions [kgCO2]')
    colors1 = ['orangered', 'green', 'royalblue']
    plt.bar(legend, values1, 0.5, color=colors1)
    for i, v in enumerate(values1):
        plt.text(i - 0.15, v + 100, str(round(v)),
                 color='black', fontweight='light')
    values2 = [fct_emissions(country, yearly_energy_demand,
               heat_vectors)[vector] for country in legend]
    colors2 = ['salmon', 'mediumseagreen', 'cornflowerblue']
    plt.bar(legend, values2, 0.5, color=colors2)
    for i, v in enumerate(values2):
        plt.text(i - 0.15, v + 100, str(round(v)),
                 color='black', fontweight='light')
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.show()



def legend_creator(emissions):
    rc_param(1, 1, 1, 'beamer')
    colors = ['peru', 'sienna', 'darkgoldenrod', 'darkorange', 'darkorchid',
              'olive', 'forestgreen', 'limegreen', 'steelblue',
              'crimson', 'cyan']
    n = len(colors)
    legend = []
    for elt in emissions:
        legend.append(str(elt))
    total = [1 for i in range(n)]
    pie = plt.pie(total, startangle=0, radius=0, normalize=True, colors=colors)
    labels_legend = legend
    plt.legend(pie[0], labels_legend, bbox_to_anchor=(0.87, 0.5), loc="center right",
               bbox_transform=plt.gcf().transFigure)
    plt.subplots_adjust(left=0.2, bottom=0.1, right=0.45)
    plt.show()
