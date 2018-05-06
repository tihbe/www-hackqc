
from functions import *
from matplotlib import pyplot as plt

#--------------------------DATA DE VILLE DE QUÉBEC ----------------------------

#---------- DÉCHETS -----------
# LOCATION OF USER
x = -71.220809
y = 46.878230
filename = 'collecte-des-dechets-qc.geojson'

collecte_qc_dechets(x,y,filename)

#---------- HALOCARBURES -----------
print('HALOOOCARBURE')
x = -71.1927211179615
y = 46.84642400271845 
filename = 'collecte-des-halocarbures-qc.geojson'

collecte_qc_halocarbs(x,y,filename)

plt.show()