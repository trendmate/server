import requests
import shutil
import pandas as pd
import os 
from os import path

files = ['myntra.csv',]

file1 = files[0]

directory = "imgs"

img_path = os.path.join(directory) 
if(path.isdir(img_path)==False):
    os.mkdir(img_path)
    print("Directory '% s' created" % directory) 

df1 = pd.read_csv(file1)
df_img_links = df1["img_links"]

for i in range(len(df_img_links)):
    image_url = df_img_links[i]
    filename = str(i)

    r = requests.get(image_url, stream = True)

    if r.status_code == 200:
        r.raw.decode_content = True

        with open(os.path.join(img_path,filename + '.png'),'wb') as f:
            shutil.copyfileobj(r.raw, f)
        
        print('Image sucessfully Downloaded: ',filename)
    else:
        print('Image Couldn\'t be retreived')