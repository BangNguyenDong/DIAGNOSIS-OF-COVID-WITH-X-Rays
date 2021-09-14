# -*- coding: utf-8 -*-
"""
Created on Sun May 23 01:07:41 2021

@author: ntruo
"""



import tensorflow as tf
import flask
import numpy as np
import cv2
from keras.preprocessing.image import load_img, img_to_array
try:
 from PIL import Image
except ImportError:
 import Image
from flask import Flask, request, Response

app = flask.Flask(__name__)
IMAGE_SIZE = 256
CLASSES = ["COVID", "Normal"]




def load_model():
    global model
    model = tf.keras.models.load_model('covid_dectec.h5')

def prediction(path_to_image):
    img = load_img(path_to_image,target_size=(IMAGE_SIZE, IMAGE_SIZE))
    img_ = img_to_array(img)
    img_ = np.reshape(img, (1, IMAGE_SIZE, IMAGE_SIZE, 3))
    pred = np.argmax(model(img_))
    return CLASSES[pred]

@app.route("/predict", methods=["POST"])
def predict():
    load_model()
    data = {"success": False}
    if flask.request.method == "POST":
        if flask.request.files.get("input_"):
            input_ = flask.request.files["input_"]
            input_ = np.fromstring(input_.read(), np.uint8)
            input_ = cv2.imdecode(input_,cv2.IMREAD_COLOR)
            print(input_.shape)
            img = input_.astype("uint8")
            img = cv2.resize(img, (256,256))
            img_ = np.reshape(img, (1, IMAGE_SIZE, IMAGE_SIZE, 3))
            pred = np.argmax(model(img_))
            pred = CLASSES[pred]
            print(pred)
            data["predictions"] = pred
            data["success"] = True
    return flask.jsonify(data)


if __name__ == "__main__":
	print(("* Loading Keras model and Flask starting server..."
		"please wait until server has fully started"))
	app.run(debug=False)










