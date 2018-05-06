# Thanks to https://technobeans.com/2012/09/17/tornado-file-uploads/ for file upload strategy
# And https://github.com/matterport/Mask_RCNN for object detection

import sys
import os
from io import BytesIO
import datetime
import numpy as np
from PIL import Image
from bson import json_util
import tornado
import tornado.ioloop
import tornado.web

ROOT_DIR = sys.path[0]
COCO_MODEL_PATH = os.path.join(ROOT_DIR, "./mask_rcnn_coco.h5")
MODEL_DIR = os.path.join(ROOT_DIR, "logs")

sys.path.append(os.path.join(sys.path[0], './Mask_RCNN'))
sys.path.append(os.path.join(ROOT_DIR, "Mask_RCNN/samples/coco/"))

from mrcnn import config as Config
import mrcnn.model as modellib
from mrcnn import utils
from mrcnn import visualize
import coco

PORT = 80
THRESHOLD = 0.80

class_names = ['BG', 'personne', 'velo', 'voiture', 'moto', 'avion',
                'bus', 'train', 'camion', 'bateau', 'feu de circulation',
                'borne fontaine', "panneau d'arret", 'parcomètre', 'banc', 'oiseau',
                'chat', 'chien', 'cheval', 'mouton', 'vache', 'elephant', 'ours',
                'zebre', 'giraffe', 'sac a dos', 'parapluie', 'sac a main', 'cravate',
                'valise', 'frisbee', 'skis', 'planche a neige', 'ballon de sport',
                'cerf-volant', 'baton de baseball', 'gant de baseball', 'skateboard',
                'surfboard', 'raquette de tennis', 'bouteille', 'coupe de vin', 'coupe',
                'fourchette', 'couteau', 'cuillere', 'bolle', 'banane', 'pomme',
                'sandwich', 'orange', 'broccoli', 'carrotte', 'hot dog', 'pizza',
                'beigne', 'gateau', 'chaise', 'divan', 'plante', 'lit',
                'table a manger', 'toilette', 'tv', 'portable', 'souris', 'manette',
                'clavier', 'cellulaire', 'micro-ondes', 'four', 'toaster',
                'lavabo', 'refrigirateur', 'livre', 'horloge', 'vase', 'ciseaux',
                'ourse en peluche', 'sechoir', 'brosse a dents']

class  InferenceConfig (coco.CocoConfig):
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1

config = InferenceConfig()

model = modellib.MaskRCNN(mode="inference", model_dir=MODEL_DIR, config=config)
model.load_weights(COCO_MODEL_PATH, by_name=True) 

class Userform(tornado.web.RequestHandler):
    def get(self):
        self.render("fileuploadform.html")

class Index(tornado.web.RequestHandler):
    def get(self):
        self.render("../webpage/sharegreen/w3/index.html")


class Upload(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.set_header('Content-Type', 'application/json')
    def options(self):
        # no body
        self.set_status(204)
        self.finish()
    def post(self):
        fileinfo = self.request.files['filearg'][0]
        lng = self.get_argument("lng", default=None, strip=False)
        lat = self.get_argument("lat", default=None, strip=False)
        if lng is None or lat is None:
            return self.finish(json_util.dumps({"err": "Longitude or latitude missing"}))

        image = np.array(Image.open(BytesIO(fileinfo['body'])))
        height, width, _ = image.shape
        timestamp = '{:%Y-%b-%d %H:%M:%S}'.format(datetime.datetime.now())
        results = model.detect([image])
        if len(results) != 1:
            #error
            pass
        result = results[0]
        result_obj = {
            "timestamp": timestamp,
            "image": {
                "height": height,
                "width": width
            },
            "objects": []
        }
        object_array = []

        for current_id, (class_id, bounding_box, score) in enumerate(zip(result['class_ids'], result['rois'], result['scores'])):
            type_bac = "Recyclage (bac vert)"
            info = u"Saviez-vous que ce genre d'item peut être recyclé en papier journal ?"
            collecte = u"Cet objet peut être mis dans votre bac vert, celui-ci sera ramassé par la ville les mardi et jeudis dans votre quartier"
            
            if class_names[class_id] in ['banane', 'pomme', 'sandwich', 'orange', 'broccoli', 'carrotte', 'beigne', 'gateau']:
                type_bac = "Composte (bac brun)"
                info = u"Saviez-vous que les matières végétales représentent 36 % \du total des déchets produits par les ménages montréalais." 
                collecte = u"Cet objet peut être mis dans votre bac brun, celui-ci sera ramassé par la ville les mardi et jeudis dans votre quartier"
            elif class_names[class_id] in ['bouteille', 'coupe de vin', 'coupe', 'bol', 'livre']:
                type_bac = "Recyclage (bac vert)"
                info = u"Saviez-vous qu'au Québec, 80% \des contenants de verre placés dans les bacs de recyclage résidentiels sont des bouteilles de vin. Or, ce verre n’est pas recyclé! Il est généralement envoyé aux sites d’enfouissement. " 
                collecte = u"Cet objet peut être mis dans votre bac vert, celui-ci sera ramassé par la ville les mardi et jeudis dans votre quartier"
            elif class_names[class_id] in ['tv', 'portable', 'souris', 'manette', 'clavier', 'cellulaire']:
                type_bac = "Écocentre"
                info = u"Saviez-vous que les produits électroniques contiennent beaucoup de matières, comme du verre, du plastique, de l’or, de l’argent, du cuivre et du palladium, qui doivent être récupérées et recyclées." 
                collecte = u"Cet objet doit être emmené dans un écocentre!"
            else:
                continue

            if score < THRESHOLD:
                continue
            
            current_object = {
                #"category_id": int(class_id),
                "bbox": bounding_box.tolist(),
                "category": class_names[class_id],
                #"id" : current_id,
                "type": type_bac,
                "info": info,
                "collecte": collecte
            }
            object_array.append(current_object)


        result_obj['objects'] = object_array
        self.finish(json_util.dumps(result_obj))


application = tornado.web.Application([
        (r"/", Index),
        (r"/api", Upload),
        (r"/upload", Userform),
        (r'/js/(.*)', tornado.web.StaticFileHandler, {'path': '../webpage/sharegreen/w3/js'}),
        (r'/css/(.*)', tornado.web.StaticFileHandler, {'path': '../webpage/sharegreen/w3/css'}),
        (r'/vendor/(.*)', tornado.web.StaticFileHandler, {'path': '../webpage/sharegreen/w3/vendor'}),
        (r'/img/(.*)', tornado.web.StaticFileHandler, {'path': '../webpage/sharegreen/w3/img'}),
        ], debug=False)

if __name__ == "__main__":
    application.listen(PORT)
    print("Server started")
    tornado.ioloop.IOLoop.instance().start()