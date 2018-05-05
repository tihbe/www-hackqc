
import sys
import os
from io import BytesIO
import datetime
import numpy as np
from PIL import Image
from bson import json_util

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


image = np.array(Image.open("test_img.jpg"))
#image = np.array(Image.open(BytesIO(img)))

height, width, _ = image.shape
timestamp = '{:%Y-%b-%d %H:%M:%S}'.format(datetime.datetime.now())
results = model.detect([image])

if len(results) != 1:
    #error
    pass

result = results[0]

# r = results[0]
# visualize.display_instances(image, r['rois'], r['masks'], r['class_ids'], class_names, r['scores'])

result_obj = {
    "timestamp": timestamp,
    "image": {
        "height": height,
        "width": width
    },
    "objects": []
}
object_array = []


for current_id, (class_id, bounding_box) in enumerate(zip(result['class_ids'], result['rois'])):
    object_area = 0 
    current_object = {
        "category_id": int(class_id),
        "bbox": bounding_box.tolist(),
        "category": class_names[class_id],
        "segment": [],
        "id" : current_id,
        "area": object_area
    }
    object_array.append(current_object)


result_obj['objects'] = object_array
to_return = json_util.dumps(result_obj)


print(to_return)