# -*- coding: utf-8 -*-
import pandas as pd 
import re
from pymystem3 import Mystem
from tqdm import tqdm 
import preprocessor as p #tweeter data preprocessor
from nltk import word_tokenize, pos_tag, ne_chunk
import string
import nltk
import os


 

nltk.download('punkt')
nltk.download("stopwords")
os.system("wget -N https://raw.githubusercontent.com/stopwords-iso/stopwords-ru/master/stopwords-ru.txt")

try:
    name_file = "stopwords-ru.txt" 
    f = open(name_file)
    stopword_file = (f.read()).split("\n")
    f.close()
    print("READ_STOPWORDS_from "+name_file)
except :
    print("Could not read stopword_file")
    from nltk.corpus import stopwords
    main_stopwords = stopword_file+normalisation(stopwords.words('russian')) # нормализуем нлтк шные стоп слова, стакаем в один

def get_stopwords():
    try:
        name_file = "stopwords-ru.txt" 
        f = open(name_file)
        stopword_file = (f.read()).split("\n")
        f.close()
        print("READ_STOPWORDS_from "+name_file)
    except :
        print("Could not read stopword_file")
    from nltk.corpus import stopwords
    return  stopword_file+normalisation(stopwords.words('russian')) # нормализуем нлтк шные стоп слова, стакаем в один

#Если на вход функции main не подать словарь стоп слов то она его будет собирать сама.
# Для быстрого выполнения нужно указать словарь!
def main(data, use_default_dict = True, dict_stopwords=[], norm = True): #Data is pandas object exp -- data['tweets']

#Собираем делее большой словарь из стоп слов
    if use_default_dict:
        try:
            name_file = "stopwords-ru.txt"
            f = open(name_file)
            stopword_file = (f.read()).split("\n")
            f.close()
            print("READ_STOPWORDS_from "+name_file)
        except :
            print("Could not read stopword_file")

        from nltk.corpus import stopwords
        main_stopwords = stopword_file+normalisation(stopwords.words('russian')) # нормализуем нлтк шные стоп слова, стакаем в один
    else:
        main_stopwords  = dict_stopwords

        
    clean_data = []
    for i in tqdm(range(0,len(data))):
        raw_tweet = p.clean(data[i]) # Используем пакет твитера 
        clean_data.append(preprocess_tweet(raw_tweet,main_stopwords_custom = main_stopwords)) # Используем самописную функцию 
    
    #Соединяем все в строку
    new_data = [] 
    for i in range(len(clean_data)):
        sentence = ' '.join(map(str, clean_data[i]))
        if not len(sentence) == 0:
            sentence = sentence.replace("…", "") # Убираем этот странный символ )
            if not len(sentence) == 0:
                new_data.append(sentence)
    
    new_data = cleane_msg(new_data)# Еще раз чистим регуляркой
    if norm == True:
        new_data = normalisation(new_data)

    test_data_filter = []
    trash_box = []
    for part_sentence in new_data: # Удаляю все что меньше или длинну 2 
        new_part_sentence=[]
        for q in part_sentence.split():
            if len(q) <= 2:
                trash_box.append(str(q))    
            else:
                new_part_sentence.append(q)
        test_data_filter.append(new_part_sentence)
   
    print('Удалены слова длинной меньше 3 в количестве'+ str(len(trash_box)))
    new_data = [] 
    for i in range(len(test_data_filter)):
        sentence = ' '.join(map(str, test_data_filter[i]))
        if not len(sentence) == 0:
            new_data.append(sentence)

    print("Количество сообщений  = "+str(len(new_data)))

    df_csv = pd.DataFrame(new_data, columns =['tweets'], dtype = str)

    drop_duplicates_data= df_csv.drop_duplicates()
    
    return  drop_duplicates_data





def normalisation(new_data):
    m = Mystem()
    m.start()
    normalize_data=[]
    data_size=len(new_data)
    count=0
    for i in tqdm(new_data,desc = "normalisation"):
        lemmas = m.lemmatize(i)
        normalize_data.append((''.join(lemmas)).replace("\n",""))
        count=count+1
#         print(count*100/data_size)
    return normalize_data


def preprocess_tweet(text, main_stopwords_custom = None):

    # Check characters to see if they are in punctuation
    nopunc = [char for char in text if char not in string.punctuation]
    # Join the characters again to form the string.
    nopunc = ''.join(nopunc)
    # convert text to lower-case
    nopunc = text.lower()
    # remove URLs
    nopunc = re.sub('((www\.[^\s]+)|(https?://[^\s]+)|(http?://[^\s]+))', '', nopunc)
    nopunc = re.sub(r'http\S+', '', nopunc)
    # remove usernames
    nopunc = re.sub('@[^\s]+', '', nopunc)
    # remove the # in #hashtag
    nopunc = re.sub(r'#([^\s]+)', r'\1', nopunc)
    nopunc = re.sub('"', '', nopunc)
    nopunc = re.sub('\\\\', '', nopunc)
    
    nopunc = re.sub(r'[—/=+-.?!)(,:]', '', nopunc)
    # remove repeated characters
    nopunc = word_tokenize(nopunc)
    # remove stopwords from final word list

    if main_stopwords_custom  == None:
        print("Не заданы стоп-слова!\n СТОП_СЛОВА НЕ УДАЛЯЮТСЯ")
        return nopunc #Возвращаем массив с неудаленными стоп-словами


    if not main_stopwords_custom  == None:# если заданны стоп слова 
        main_stopwords = main_stopwords_custom
        
        return [word for word in nopunc if word not in main_stopwords]

def cleane_msg(msg,len_sentence = 5):
    reg = re.compile('[^а-яА-ЯёЁ ]')
    for i in range(len(msg)):
        msg[i] = re.sub(r'[,.;?!)(]', ' ', msg[i])
        msg[i] = reg.sub('', msg[i])
        msg[i] = msg[i].lower()
    msg = list(filter(lambda x: len(x) > len_sentence, msg))  
    return msg
    

def get_celan_text(text, stop_words, norm =True):
    df_csv = pd.DataFrame([text], columns =['tweets'], dtype = str)
    clean_df = main(df_csv['tweets'],use_default_dict = False, dict_stopwords=stop_words, norm = norm)
    try:
        return [clean_df['tweets'][0]]
    except:
        return ["проблемы с ответом"]
#проблемы с ответом
# def get_stop_words():
#     import os
#     os.system("wget -N https://raw.githubusercontent.com/stopwords-iso/stopwords-ru/master/stopwords-ru.txt")


if __name__ == '__main__':
    data = pd.read_csv("final_df.csv", error_bad_lines = False, encoding = "utf-8")
    # try:
    #     name_file = "stopwords-ru.txt" 
    #     f = open(name_file)
    #     stopword_file = (f.read()).split("\n")
    #     f.close()
    #     print("READ_STOPWORDS_from "+name_file)
    # except :
    #     print("Could not read stopword_file")
    #     from nltk.corpus import stopwords
    #     main_stopwords = stopword_file+normalisation(stopwords.words('russian')) # нормализуем нлтк шные стоп слова, стакаем в один
    main(data["massege"],use_default_dict = False, dict_stopwords=main_stopwords)