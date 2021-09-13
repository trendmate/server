from flask import Flask, render_template, request
from scipy.misc import imsave, imread, imresize
import numpy as np
import keras.models
import re
import sys 
import os
import base64
sys.path.append(os.path.abspath("./model"))
from server.load import * 

global graph, model

app = Flask(__name__)

model, graph = init()


@app.route('/predict/',methods=['GET'])
def predict():
	x = []

	with graph.as_default():
		out = model.predict(x)
		response = np.array_str(np.argmax(out,axis=1))
		return response	


if __name__ == '__main__':
    app.run(debug=True, port=8000)