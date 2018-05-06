import json
import numpy as np
from matplotlib import pyplot as plt
import textwrap as tw
from inside_polygon import inside_polygon

plt.close("all")

#--------------------------DATA DE VILLE DE QUÉBEC ----------------------------

# LOCATION OF USER
x = -71.220809
y = 46.878230

with open('collecte-des-dechets-qc.geojson') as f:
    data = json.load(f)

plt.figure(1)

for index, feature in enumerate(data['features']):
    size = np.shape(feature['geometry']['coordinates'])
    dim_size = len(size)

    if dim_size == 3:
        if inside_polygon(x, y, np.array(feature['geometry']['coordinates'])[0]):
            for i in range(size[1]):
                plt.plot(np.array(feature['geometry']['coordinates'])[0, i, 0],
                	np.array(feature['geometry']['coordinates'])[0, i, 1], marker='o', markersize=3, color='k')
                
                plt.plot(x,y,marker='o',markersize=3,color='r')
                plt.xlabel('Latitude')
                plt.ylabel('Longitude')
                #msg_fr_wrapped = tw.fill(tw.dedent(feature['properties']['MESSAGE_FR'].rstrip()), width=40)
                #t = plt.text(x-0.02,y-0.01,feature['properties']['MUNICIPALITE'] + "\n" + feature['properties']['TYPE_DECHET'] + "\n" + msg_fr_wrapped)
                #t.set_bbox(dict(boxstyle='round',facecolor='seagreen', edgecolor='seagreen',alpha=0.5))
            
            print('Municipalité : Québec')
            print('\nType déchet : ', feature['properties']['TYPE_COLLECTE'])
            print('\nJours de collecte : ',feature['properties']['JOUR_COLLECTE'])

        #if (index % 5) == 0:
        #   print('index : %i' % index)


plt.show()
