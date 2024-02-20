import numpy as np
import pandas as pd

from keras.applications.xception import Xception
from keras.models import Model

from sklearn.neighbors import NearestNeighbors

from PIL import ImageTk, Image

import tkinter as tk
import tkinter.filedialog as fd


class Root(tk.Tk):
    def __init__(self):
        super().__init__()

        self.canvas1 = tk.Canvas(width=600, height=600, bg='white')
        self.canvas1.grid(row=0, column=0, padx=5, pady=5)

        self.canvas2 = tk.Canvas(width=400, height=600, bg='white')
        self.canvas2.grid(row=0, column=1, padx=5, pady=5)

        self.button_load = tk.Button(text='Загрузить', font='Times 18', command=self.load_image)
        self.button_load.grid(row=1, column=0, padx=5, pady=5)

        self.button_compare = tk.Button(text='Найти', font='Times 18', command=self.find_similar_ones)
        self.button_compare.grid(row=1, column=1, padx=5, pady=5)

    def load_image(self):
        filename = fd.askopenfilename(filetypes=[('All files', '*.*')])
        self.img = Image.open(filename)
        self.img = self.img.resize((self.canvas1.winfo_width(), self.canvas1.winfo_width()))
        self.img_tk = ImageTk.PhotoImage(self.img)
        self.canvas1.create_image(0, 0, image=self.img_tk, anchor=tk.NW)

    def find_similar_ones(self):
        model = Xception(weights='imagenet', include_top=True, classes=1000)
        feat_extractor = Model(inputs=model.input, outputs=model.get_layer("avg_pool").output)
        feat_extractor.compile()  # нейросеть для выделения признаков

        img1 = self.img.resize(feat_extractor.input_shape[1:3])
        img1 = np.array(img1)
        img1 = np.expand_dims(img1, axis=0)
        img1 = img1.astype('float32')
        img1 /= 255

        features1 = feat_extractor.predict(img1)
        features1 = np.array(features1)

        features2 = pd.read_csv('data.csv').values  # загружаем признаки из csv-файла

        nei_clf = NearestNeighbors(metric='minkowski')  # сравниваем признаки как векторы методом ближайшего соседа
        nei_clf.fit(features2)
        (_, ), (idx, ) = nei_clf.kneighbors(features1, n_neighbors=1)

        filename = 'dataset\\' + str(idx[0] + 1) + '.jpg'
        self.img2 = Image.open(filename)  # загружаем найденную картинку
        self.img2_tk = ImageTk.PhotoImage(self.img2)
        self.canvas2.create_image(0, 0, image=self.img2_tk, anchor=tk.NW)


window = Root()
window.title('Image Comparison')

window.mainloop()
