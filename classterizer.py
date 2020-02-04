# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from tqdm import tqdm
import pickle
import os 
from gensim.models.fasttext import FastText

import data_cleaner 

#Сразуй загружаем модель из пикла 

try:
    with open('kmeans_model_2.pickle', 'rb') as f:
        kmeans = pickle.load(f)

except:
    print('Не смог загрузить модель')

try:
    stop_word = data_cleaner.get_stopwords()

except:
    print("Не смог загрузить стоп слова")



while(not os.path.exists("ft_native_300_ru_twitter_nltk_word_tokenize.bin")):
    print("Пытаюсь скачать модель ")
    os.system('wget http://files.deeppavlov.ai/embeddings/ft_native_300_ru_twitter_nltk_word_tokenize.bin')



print("Начинаю загрузку в ОЗУ модели")
import time
start = time.time()
model = FastText.load_fasttext_format("ft_native_300_ru_twitter_nltk_word_tokenize.bin") 
end = time.time()
print('Время  импорта модели ___'+str(int(end - start)//60)+".min")

    




    


    #http://files.deeppavlov.ai/embeddings/ft_native_300_ru_twitter_nltk_word_tokenize.bin


def fit_upload():
    file_with_vectors = "fast_text_MAIN.pickle" # !!!! ПОстоянное название 
    with open(file_with_vectors, 'rb') as f:
        text_vec = pickle.load(f)

    dataset_file_name = "/home/alex/comptech2020/2.1_fast_text_with_NE.csv"
    data = pd.read_csv(dataset_file_name, error_bad_lines = False, encoding = "utf-8")

    number_of_clusters = 20
    kmeans = KMeans(n_clusters=number_of_clusters).fit(text_vec)
    with open("kmeans_model_2.pickle", 'wb') as f:
        pickle.dump(kmeans, f)

def load_predict(text,kmeans=kmeans):
    clean_text = data_cleaner.get_celan_text(text,stop_word)

    #Получаем вектора для сообщения 
    fast_text_vec=[]  
    sentence_vec=np.zeros((100,))  
    for i in clean_text[0].split():  
        sentence_vec+=model[i]  
    fast_text_vec.append(sentence_vec/len(clean_text[0].split())) 
    return kmeans.predict(fast_text_vec)