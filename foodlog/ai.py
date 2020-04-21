#!/usr/bin/python
# -*- coding: UTF-8 -*-

'''
@version:0.1
@author:Cai Qingpeng
@file: ai.py
@time: 2020/2/23 3:04 AM
'''

import os
import numpy as np
from PIL import Image,ImageDraw,ImageFont

from keras.models import Model
from keras.layers import Dense
from keras.preprocessing.image import img_to_array
from keras.applications.xception import Xception

import tensorflow as tf

from models.darknet import darknet

os.environ["CUDA_VISIBLE_DEVICES"] = "2"


def init_models(basic_path):
    print("\n [*]Loading object detection model!\n")

    det_net = darknet.load_net(str.encode(basic_path) + b"darknet/cfg/yolov3-food.cfg", str.encode(basic_path) + b"darknet/backup/food/yolov3-food_final.weights", 0)
    det_meta = darknet.load_meta(str.encode(basic_path) + b"darknet/cfg/food.data")

    print("\n [*]Loading object classficiation model!\n")

    classes = 231

    base_model = Xception(include_top=True, input_shape=(299, 299, 3))
    base_model.layers.pop()
    predictions = Dense(classes, activation='softmax')(base_model.layers[-1].output)
    clf_model = Model(input=base_model.input, output=[predictions])
    clf_model.load_weights(basic_path + "classification/models/xception-0-15-0.82.h5")

    class_dict = {v:k for k,v in np.load(basic_path + "classification/class_index/food231.npy")[()].items()}

    return det_net,det_meta,clf_model,class_dict

def predict(model, img):
    width_height_tuple = (299, 299)
    if(img.size != width_height_tuple):
        img = img.resize(width_height_tuple, Image.NEAREST)
    x = img_to_array(img)
    x /= 255 * 1.
    x = x.reshape((1,) + x.shape)

    with graph.as_default():
        y = model.predict(x)
    return y


config = tf.ConfigProto()
config.gpu_options.allow_growth = True
session = tf.Session(config=config)
global graph
graph = tf.get_default_graph()

basic_path = "/home/qingpeng/website/sift/models/"
