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
THRESHOLD = 0.75

class_names = ['BG', 'person', 'bicycle', 'car', 'motorcycle', 'airplane',
                'bus', 'train', 'truck', 'boat', 'traffic light',
                'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird',
                'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear',
                'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie',
                'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball',
                'kite', 'baseball bat', 'baseball glove', 'skateboard',
                'surfboard', 'tennis racket', 'bottle', 'wine glass', 'cup',
                'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple',
                'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza',
                'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed',
                'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote',
                'keyboard', 'cell phone', 'microwave', 'oven', 'toaster',
                'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors',
                'teddy bear', 'hair drier', 'toothbrush']

class  InferenceConfig (coco.CocoConfig):
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1

config = InferenceConfig()

model = modellib.MaskRCNN(mode="inference", model_dir=MODEL_DIR, config=config)
model.load_weights(COCO_MODEL_PATH, by_name=True) 

class Userform(tornado.web.RequestHandler):
    def get(self):
        self.render("fileuploadform.html")


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
            if score < THRESHOLD:
                continue
            if class_names[class_id] in ["person", "traffic light", "stop sign", "parking meter", "bird", "cat", "dog", "horse", "sheep", "cow", "elephant", "bear", 'zebra', 'giraffe']:
                continue

            current_object = {
                #"category_id": int(class_id),
                "bbox": bounding_box.tolist(),
                "category": class_names[class_id],
                #"id" : current_id,
                "type": "Recyclage (bac vert)",
                "info": u"Saviez-vous que ce genre d'item peut être recyclé en papier journal ?",
                "collecte": u"Cet objet peut être mis dans votre bac vert, celui-ci sera ramassé par la ville les mardi et jeudis dans votre quartier"
            }
            object_array.append(current_object)


        result_obj['objects'] = object_array
        self.finish(json_util.dumps(result_obj))


application = tornado.web.Application([
        (r"/", Upload),
        (r"/upload", Userform),
        ], debug=False)

if __name__ == "__main__":
    application.listen(PORT)
    print("Server started")
    tornado.ioloop.IOLoop.instance().start()