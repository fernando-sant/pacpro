import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

"""
Directives (optionnelles) pour la génération de figures avec Python

I. Mise en page

    1.  Ne pas redimensionner une figure sous word/latex/ppt/beamer après création, ça change l'intégration et la taille 
        relative de la police par rapport à celle du document et des autres figures. 

    2.  Privilégier un axe par figure. Car il est toujours possible de composer et mettre en page les figures 
        dans un rapport ou une présentation. Par contre, cette composition doit être connue à l'avance pour ne pas avoir 
        à modifier la taille de la figure (c.f. règle #1). 
        ncols : nombre de colonne (1, ou 2 en général), 
        nrows : nombre de lignes, cet argument n'est pas obligatoire, équivalent à changer le ratio des figures.

        Ne pas tenir compte de cette directive si les légendes d'axes on des hauteurs/largeurs différentes, 
        dans ce cas, il est difficile de bien aligner les axes sous word/latex

    3.  Pas de titres, il vaut mieux utiliser les légendes de word/latex qui sont obligatoires et facilement 
        référençables.

    Rappels : la taille des figures est donnée en inches à pyplot. 
    -   Pour rapport en taille A4, avec des marges de 2cm par exemple, la taille disponible est de 21-4=17cm
        ce qui donne 6.7 inches
    -   L'affichage à votre écran n'a pas la meme taille si plt.rcParams['figure.dpi'] 
        n'est pas bien défini (defaut=100) 

II. Sauvegarde et format

    1.  Pour chaque figures, enregistrer les données avec pickle, csv, excel, etc. 
        pour pouvoir les regénérer. Les figures peuvent aussi être enregistrer avec pickle (ce sont des 
        objets après tout).

    2.  Enregistrer les figures sous format pdf (ou svg), Les formats vectoriels sont à privilégier: pdf, eps, svg, etc. 
        Les formats png et jpeg sont à considérer dans certains cas très lourd (le pdf d'un scatter plot d'un million 
        de points pèse 16 Mo, alors que la sauvegarde en png pèse 250ko en png 600dpi, 150ko en 400dpi). 
        Dans ce cas, préférer 400 dpi (600 sont parfois demandés pour les revues).

    3.  N'hésiter pas à les enregistrer deux ou trois fois par défaut (pour les beamer et les rapports en simple 
        et double colonne) 

    4.  Prévoir un petit script pour regénérer les figures simplement 
        (voire meme un scripts qui lance tous les autres pour les thèses, stages avec beaucoup de résultats. E peut 
        être utile si vous choisissez de changer la police de toutes les figures de votre thèse.


III. Ajustements 

    1.  Des ajustements sur les paramètres suivants sont possibles au cas par cas :
        'figure.subplot.bottom': 0.27,
        'figure.subplot.hspace': 0.2,
        'figure.subplot.left': 0.12,
        'figure.subplot.right': 0.98,
        'figure.subplot.top': 0.92,
        'figure.subplot.wspace': 0.2,

    2.  Les autres options de matplotlib sont modifiables mais doivent etre cohérentes dans tout le document. 
        https://matplotlib.org/stable/tutorials/introductory/customizing.html
        mpl.rcParams pour voir les options utilisées. 

        Pour aider à garder cette cohérence, la fonction rc_param permet de générer automatiquement les paramètres 
        suivant le type de doc, et le nombre de colonnes. Ne pas hésiter à adapter la fonction à vos envies.

    3.  Éviter d'afficher sur les mêmes axes des grandeurs dont les normes sont d'ordre de grandeur très différentes 
        (ou utiliser un second axe y avec `ax_new = ax.twinx()`).

    4.  Si les abcisses sont des dates, d'autres options sont utiles, 
        comme la gestion des graduations majeurs et mineurs : 

        >>> import matplotlib.dates as mdates

        Générer la graduation majeure par mois ou deux mois :
        >>> ax.xaxis.set_major_locator(mdates.MonthLocator()) 
        >>> ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2)) 

        Générer la graduation majeure Automatiquement, pour éviter le recouvrement :
        >>> ax.xaxis.set_major_locator(mdates.AutoDateLocator(minticks=6, maxticks=10)) 

        La gestion des formats : 
        >>> ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))

"""
# size of a ppt:  25.4*19.05

# Définir la largeur de la figure en cm
BEAMER_WIDTH_CM = 20
REPORT_WIDTH_CM = 15
#
inches_per_pt = 1.0 / 72.27  # Convert pt to inch
inches_per_cm = 1 / 2.54  # cm to  inches

BEAMER_WIDTH_PT = BEAMER_WIDTH_CM * inches_per_cm / inches_per_pt
REPORT_WIDTH_PT = REPORT_WIDTH_CM * inches_per_cm / inches_per_pt

# définir le dpi de votre écran pour un affichage à l'échelle (google it)
DPI = 92.5
plt.rcParams['figure.dpi'] = DPI

# exemple de paramètre à utiliser
param_report_1col = {
    "text.usetex": False,  # use LaTeX to write all text
    "font.family": ["serif"],
    "font.serif": ['Times'],  # plt.rcParams['font.sans-serif'] pour avoir les options
    "font.monospace": [],
    "axes.labelsize": 10,  # LaTeX default is 10pt font.
    "axes.grid": True,  # display grid or not
    "axes.grid.axis": 'both',  # which axis the grid should apply to
    "axes.grid.which": 'major',
    "axes.formatter.limits": (-3, 3),
    "font.size": 9,
    "legend.fontsize": 9,  # Make the legend/label fonts a little smaller
    "xtick.labelsize": 14,
    "ytick.labelsize": 14,
    "figure.figsize": (8, 8),  # default fig size of 0.9 textwidth
    'figure.subplot.bottom': 0.12,
    'figure.subplot.hspace': 0.2,
    'figure.subplot.left': 0.08,
    'figure.subplot.right': 0.98,
    'figure.subplot.top': 0.92,
    'figure.subplot.wspace': 0.2,
    'grid.linewidth': 0.5
}


def rc_param(scale=1, nrows=1, ncols=1, document='report', ratio=None):
    """
    Définit les paramètres de matplotlib étant donnée une mise en page, un ratio, et un type de document.

    :param scale: une mise à l'échelle
    :param nrows: nombre de ligne dans la mise en page finale (équivalent à changer le ratio)
    :param ncols: nombre de colonne dans la mise en page finale
    :param document: 'beamer' modifie la largeur du document, défaut: None
    :param ratio: ratio hauteur/largeur, défaut : 0.618
    :return: None
    """
    import matplotlib as mpl

    size = figsize(scale=scale, nrows=nrows, ncols=ncols, document=document, ratio=ratio)
    rc_param = param_report_1col
    rc_param.update({"figure.figsize": size})

    if document == 'beamer':
        # Pour les présentations, les tailles relatives à gauche et en bas doivent être légèrement supérieures
        # pour les légendes et ticks. La police doit être plus grande, les lignes peuvent être aussi plus épaisses.
        rc_param.update(
            {"font.size": 20,
             "legend.fontsize": 16,
             "xtick.labelsize": 18,
             "ytick.labelsize": 18,
             "axes.labelsize": 16,
             'figure.subplot.bottom': 0.12,
             'figure.subplot.left': 0.08,
             'lines.linewidth': 2})

    if ncols == 2:
        # en double colonne les tailles relatives à gauche et en bas doivent être légèrement supérieures
        # pour les légendes et ticks.
        rc_param.update(
            {'figure.subplot.bottom': 0.2,
             'figure.subplot.left': 0.12,
             'figure.subplot.right': 0.98,
             'figure.subplot.top': 0.92})

    if nrows == 2:
        rc_param.update(
            {'figure.subplot.bottom': 0.2,
             'figure.subplot.left': 0.12,
             'figure.subplot.right': 0.98,
             'figure.subplot.top': 0.92,
             'figure.subplot.hspace': 0.1})

    mpl.rcParams.update(rc_param)


def figsize(scale=1, nrows=1, ncols=1, document='report', ratio=None,
            report_width=REPORT_WIDTH_PT,
            beamer_width=BEAMER_WIDTH_PT):
    """
    Calcule la taille d'une figure étant donnée une mise en page, un ratio, et un type de document.

    :param scale: une mise à l'échelle
    :param nrows: nombre de ligne dans la mise en page finale
    :param ncols: nombre de colonne dans la mise en page finale
    :param document: 'beamer' modifie la largeur du document, défaut: None
    :param ratio: ratio hauteur/largeur, défaut : 0.618
    :return: tuple
    """
    if document == 'beamer':
        fig_width_pt = beamer_width
    elif document == 'report':
        fig_width_pt = report_width

    if ratio is None:
        if ncols >= 2:
            ratio = 0.618  # golden number
        else:
            ratio = 0.5  # ratio plus petit dans le cas d'une figure sur une ligne

    inches_per_pt = 1.0 / 72.27  # Convert pt to inch
    inches_per_cm = 1 / 2.54  # cm to  inches
    # default ratio = (np.sqrt(5.0) - 1.0) / 2.0  # Aesthetic golden ratio (you could change this)
    fig_width = fig_width_pt * inches_per_pt * scale / ncols  # / inches_per_cm  # width in inches
    fig_height = nrows * fig_width * ratio  # height in inches
    fig_size = [fig_width, fig_height]
    return fig_size