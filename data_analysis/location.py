import json
import numpy as np
from matplotlib import pyplot as plt
import textwrap as tw

plt.close("all")

def inside_polygon(x, y, points):
    """
    Return True if a coordinate (x, y) is inside a polygon defined by
    a list of verticies [(x1, y1), (x2, y2), ... , (xN, yN)].

    Reference: http://www.ariel.com.au/a/python-point-int-poly.html
    """
    n = len(points)
    inside = False
    p1x, p1y = points[0]
    for i in range(1, n + 1):
        p2x, p2y = points[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / \
                            (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y
    return inside

#--------------------------DATA DE VILLE DE MONTRÉAL ----------------------------

# LOCATION OF USER
x = -73.569247
y = 45.504907

with open('collecte-des-matieres-recyclables.geojson') as f:
    data = json.load(f)

plt.figure(1)

for index, feature in enumerate(data['features']):
    size = np.shape(feature['geometry']['coordinates'])[1]

    if size != 1 and size != 2:
        if inside_polygon(x, y, np.array(feature['geometry']['coordinates'])[0]):
            for i in range(size):
                plt.plot(np.array(feature['geometry']['coordinates'])[0, i, 0],
                	np.array(feature['geometry']['coordinates'])[0, i, 1], marker='o', markersize=3, color='k')
                
                plt.plot(x,y,marker='o',markersize=3,color='r')
                
                msg_fr_wrapped = tw.fill(tw.dedent(feature['properties']['MESSAGE_FR'].rstrip()), width=40)
                t = plt.text(x-0.02,y-0.01,feature['properties']['MUNICIPALITE'] + "\n" + feature['properties']['TYPE_DECHET'] + "\n" + msg_fr_wrapped)
                t.set_bbox(dict(boxstyle='round',facecolor='seagreen', edgecolor='seagreen',alpha=0.5))
            
            print('Municipalité : ', feature['properties']['MUNICIPALITE'])
            print('\nType déchet : ', feature['properties']['TYPE_DECHET'])
            print('\n',feature['properties']['MESSAGE_FR'])

    #if (index % 5) == 0:
    #    print('index : %i' % index)



plt.show()
