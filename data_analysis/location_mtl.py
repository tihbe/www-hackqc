
from functions import *
from matplotlib import pyplot as plt

#--------------------------DATA DE VILLE DE MONTRÉAL ----------------------------
# SOURCE : https://www.donneesquebec.ca/recherche/fr/dataset/vmtl-info-collectes/resource/08165e1d-581a-4e7c-8fba-6148ad0b1761


# LOCATION OF ETS
#x = -73.562858
#y = 45.494722

#LOCATION OF MY HOME
x = -73.612488
y = 45.550321
filename = 'collecte-des-matieres-recyclables-mtl.geojson'

collecte_mtl(x,y,filename)

plt.show()