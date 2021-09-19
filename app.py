# server
from flask import Flask, request

# AI
import tensorflow as tf
import numpy as np
import pandas as pd

# downloader
import requests
import shutil

# scheduling libs
import time
import atexit
from apscheduler.schedulers.background import BackgroundScheduler

# ours
import scraper

# firebase
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate('./config/trend-mate-firebase-adminsdk-b6xj0-a86d62f4f5.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

global model, filename, IMG_SIZE, db

IMG_SIZE = (160, 160)
filename = 'temp.png'

app = Flask(__name__)

def download_image(image_url):
	r = requests.get(image_url, stream = True)

	if r.status_code == 200:
		r.raw.decode_content = True

		with open(filename,'wb') as f:
			shutil.copyfileobj(r.raw, f)
			
		print('Image sucessfully Downloaded: ',filename)
	else:
		print('Image Couldn\'t be retreived')

@app.route('/status/',methods=['GET'])
def predict():
	# json_data = request.json
	# url = json_data["image_url"]
	# download_image(url)
	# image = tf.keras.preprocessing.image.load_img(
    # 	filename, target_size=IMG_SIZE,
	# )
	# input_arr = tf.keras.preprocessing.image.img_to_array(image)
	# input_arr = np.array([input_arr])
	# predictions = model.predict(input_arr)
	# print(predictions)
	return response	

def delete_collection(coll_ref, batch_size):
    docs = coll_ref.limit(batch_size).stream()
    deleted = 0

    for doc in docs:
        print(f'Deleting doc {doc.id} => {doc.to_dict()}')
        doc.reference.delete()
        deleted = deleted + 1

    if deleted >= batch_size:
        return delete_collection(coll_ref, batch_size)

def flow():
    scraper.scrape()
	amazon_df = pd.read_csv('./data/products_data/cloud_scraped_amazon.csv')
	myntra_df = pd.read__csv('./data/products/myntra_men.csv')
	
	doc_ref = db.collection(u'trending_products').document()
	doc_ref.set({
		u'brand': ,
		u'cat': ,
		u'desc': ,
		u'image': ,
		u'name': ,
		u'price': ,
		u'rating': ,
		u'review': ,
		u'trendiness': 0,
	})



def init():
	model = tf.keras.models.load_model('./models/vgg/')
	scraper.init()
	scheduler = BackgroundScheduler()
	scheduler.add_job(func=flow, trigger="interval", hours=24)
	scheduler.start()
	atexit.register(lambda: scheduler.shutdown())

if __name__ == '__main__':
	init()
    app.run()