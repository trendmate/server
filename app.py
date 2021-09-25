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
import scrapers.scraper as scraper
import server.articles as articles

# firebase
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate(
    './config/trend-mate-firebase-adminsdk-b6xj0-a86d62f4f5.json')
firebase_admin.initialize_app(cred)

global model, filename, IMG_SIZE, db

db = firestore.client()

IMG_SIZE = (160, 160)
filename = 'temp.png'

app = Flask(__name__)


def download_image(image_url):
    r = requests.get(image_url, stream=True)

    if r.status_code == 200:
        r.raw.decode_content = True

        with open(filename, 'wb') as f:
            shutil.copyfileobj(r.raw, f)

        print('Image sucessfully Downloaded: ', filename)
    else:
        print('Image Couldn\'t be retreived')


@app.route('/', methods=['GET'])
def home_page():
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
    return 'Server is On!'


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
    global IMG_SIZE, filename
    scraper.scrape()
    # amazon_df = pd.read_csv('./data/products_data/cloud_scraped_amazon.csv')
    myntra_men_df = pd.read_csv('./data/products_data/myntra_men.csv')
    # myntra_women_df = pd.read__csv('./data/products/myntra_women.csv')
    print(myntra_men_df['image'])
    download_image(myntra_men_df.iloc[0]['image'])

    img = tf.keras.preprocessing.image.load_img(
        filename, target_size=IMG_SIZE
    )
    img_array = tf.keras.preprocessing.image.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0) # Create a batch

    predictions = model.predict(img_array)
    score = tf.nn.softmax(predictions[0])

    print(
        "This image most likely belongs to {} with a {:.2f} percent confidence."
        .format(np.argmax(score), 100 * np.max(score))
    )

    doc_ref = db.collection(u'trending_products').document()
    doc_ref.set({
        u'brand': myntra_men_df.iloc[0]['brand'],
        u'cat': myntra_men_df.iloc[0]['category'],
        u'desc': myntra_men_df.iloc[0]['description'],
        u'image': myntra_men_df.iloc[0]['image'],
        u'name': myntra_men_df.iloc[0]['description'],
        u'price': myntra_men_df.iloc[0]['price'],
        u'rating': myntra_men_df.iloc[0]['rating'],
        u'review': myntra_men_df.iloc[0]['reviews'],
        u'url': myntra_men_df.iloc[0]['url'],
        u'trendiness': np.argmax(score).item(),
    })

def add_articles():
    res = articles.sort_articles()
    print(res)
    for x in range(0,len(res)):
        doc_ref = db.collection(u'trending_articles').document()
        doc_ref.set({
            u'heading': res.iloc[x]['heading'],
            u'author': res.iloc[x]['author'],
            u'datetime': res.iloc[x]['datetime'],
            u'below_title_summary': res.iloc[x]['below_title_summary'],
            u'img': res.iloc[x]['img'],
            u'description': res.iloc[x]['description'],
            u'img2': res.iloc[x]['img2'],
            u'description2': res.iloc[x]['description2'],
            u'trendiness': res.iloc[x]['trendiness'],
        })


def init():
    # global model
    # model = tf.keras.models.load_model('./models/vgg/')
    scraper.init()
    # flow()
    # scheduler = BackgroundScheduler()
    # scheduler.add_job(func=flow, trigger="interval", hours=24)
    # scheduler.start()
    # atexit.register(lambda: scheduler.shutdown())


if __name__ == '__main__':
    init()
    scraper.scrape()
    add_articles()
    app.run()