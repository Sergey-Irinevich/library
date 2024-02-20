import numpy as np
import pandas as pd
import cv2
from keras.applications.xception import Xception
from keras.models import Model

model = Xception(weights='imagenet', include_top=True, classes=1000)
feat_extractor = Model(inputs=model.input, outputs=model.get_layer("avg_pool").output)
feat_extractor.compile()  # нейросеть для выделения признаков

image_array = []
for i in range(1, 1201):
    filename = f'dataset\\{i}.jpg'
    img = cv2.imread(filename)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, feat_extractor.input_shape[1:3])  # подогнать размер картинки под вход нейросети
    image_array.append(img)

image_array = np.array(image_array)
image_array = image_array.astype('float32')
image_array /= 255

features = []
for image in image_array:
    image = np.expand_dims(image, axis=0)
    features.append(feat_extractor.predict(image))
features = np.array(features)

feat_df = pd.DataFrame(features[:, 0, :])
feat_df.to_csv('data.csv', index_label=False)  # признаки записываем в отдельный csv-файл
