# The content of this file is largely based on:
# https://github.com/pjreddie/darknet/blob/80d9bec20f0a44ab07616215c6eadb2d633492fe/examples/detector-scipy-opencv.py

import sys
import os

# This is added so that the libdarknet.so gets found from this directory
sys.path.append(os.getcwd())

import darknet

def array_to_image(arr):
    arr = arr.transpose(2,0,1)
    c = arr.shape[0]
    h = arr.shape[1]
    w = arr.shape[2]
    arr = (arr/255.0).flatten()
    data = darknet.c_array(darknet.c_float, arr)
    im = darknet.IMAGE(w,h,c,data)
    return im

def detect2(net, meta, image, thresh=.5, hier_thresh=.5, nms=.45):
    boxes = darknet.make_boxes(net)
    probs = darknet.make_probs(net)
    num =   darknet.num_boxes(net)
    darknet.network_detect(net, image, thresh, hier_thresh, nms, boxes, probs)
    res = []
    for j in range(num):
        for i in range(meta.classes):
            if probs[j][i] > 0:
                res.append((meta.names[i], probs[j][i], (boxes[j].x, boxes[j].y, boxes[j].w, boxes[j].h)))
    res = sorted(res, key=lambda x: -x[1])
    darknet.free_ptrs(darknet.cast(probs, darknet.POINTER(darknet.c_void_p)), num)
    return res

class Detector(object):

    def __init__(self):
        # Load darknet
        self.net = darknet.load_net('cfg/yolo.cfg', 'yolo.weights', 0)
        self.meta = darknet.load_meta('cfg/coco.data')

    def detect(self, array):
        image = array_to_image(array)
        darknet.rgbgr_image(image)
        return detect2(self.net, self.meta, image)
