import tensorflow as tf
import numpy as np

# physical_devices = tf.config.list_physical_devices('GPU') 
# for device in physical_devices:
#     tf.config.experimental.set_memory_growth(device, True)

IMG_SIZE = (160, 160)

model = tf.keras.models.load_model('./models/vgg/')
# filename = 'temp.jpg'

# image = tf.keras.preprocessing.image.load_img(
# 	filename, target_size=IMG_SIZE,interpolation='nearest',
# )
# input_arr = tf.keras.preprocessing.image.img_to_array(image)
# # input_arr = tf.keras.applications.vgg16.preprocess_input(input_arr)
# print(input_arr)
# input_arr = np.array([input_arr])

images_ds = tf.keras.preprocessing.image_dataset_from_directory(
  './server/imgs/',
  seed=123,
  image_size=IMG_SIZE,
  batch_size=1)

predictions = model.predict(images_ds)
print(predictions)