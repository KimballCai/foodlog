import os
import numpy as np
from PIL import Image 

from keras import backend as K
from keras.models import Model
from keras.layers import Dense
from keras.preprocessing.image import img_to_array
from keras.models import load_model

from keras.applications.xception import Xception

import tensorflow as tf
import keras.backend.tensorflow_backend as ktf

from darknet import darknet 

config = tf.ConfigProto()
session = tf.Session(config=config)
K.set_session(session)

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
    global k
    k = x
    x = x.reshape((1,) + x.shape)
    y = model.predict(x)
    return y

def analyze_pic(basic_path,pic_path):

    det_net,det_meta,clf_model,class_dict = init_models(basic_path)
    print("\n [*]Starting \n")

    data_path = str.encode(basic_path+pic_path)

    r = darknet.detect(det_net, det_meta,data_path)
    print(r)
    img = Image.open(data_path)
    width = img.size[0]
    height = img.size[1]
    print(img.size)

    result = {}
    result['status'] = "ok"
    result['predictions'] = []

    for index,box in enumerate(r):
        print(str(index) + "\n")
        prob = box[1]
        x,y,w,h = box[2][0],box[2][1],box[2][2],box[2][3]
        left = x-w/2
        upper = y-h/2
        right = x+w/2
        down = y+h/2
        cropped = img.crop((x-w/2,y-h/2,x+w/2,y+h/2))  # (left, upper, right, lower)
        y = predict(clf_model, cropped)

        class_id = np.argsort(y[0])[::-1][0]
        str_class = class_dict[class_id]
        print(str_class,y[0][class_id])

        jbox = {}
        jbox['label_id'] = str(class_id)
        jbox['label'] = str(str_class)
        # y_min,x_min,y_max,x_max
        print(left,right,upper,down)
        print(width,height)

        jbox['detection_box'] = [max(0,upper/height),max(0,left/width),
                                 min(1,down/height),min(1,right/width)]

        result['predictions'].append(jbox)

    print(result)
    return result

if __name__ == "__main__":
    basic_path = "/home/qingpeng/website/sift/models/"
    pic_path = "/000004.jpeg"
    analyze_pic(basic_path,pic_path)

        



        

    
