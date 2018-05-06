
from functions import *
from matplotlib import pyplot as plt

#--------------------------DATA DE VILLE DE MONTRÉAL ----------------------------

# LOCATION OF USER
x = -73.562858
y = 45.494722

filename = 'collecte-des-matieres-recyclables-mtl.geojson'

collecte_mtl(x,y,filename)

plt.show()