#-------------------------------POS TAGGING ---------------------------------------
# from pyvi import ViTokenizer, ViPosTagger
# doc = ViTokenizer.tokenize("Lễ hội chọi trâu Đồ Sơn có sự giao thoa giữa những yếu tố văn hoá nông nghiệp đồng bằng với văn hoá cư dân ven biển") #đầu vào là một câu
# sent = ViPosTagger.postagging(doc)
# sentence = []
# for i in range(len(sent[0])):
#     tmp = []
#     tmp.append(sent[0][i])
#     tmp.append(sent[1][i])
#     sentence.append(tmp)
# print(sentence)
#-------------------------------Underthesea ---------------------------------------
from underthesea import pos_tag
import os
import nltk
from nltk import tokenize
name = "test.txt"
path = "../Scrapy/lehoi/76lehoi_maxreading/"
path = os.path.join(path, name)

f = open(path,'r',encoding = 'utf-8')
text=f.read()
f.close()
sents = tokenize.sent_tokenize(text)


for sent in sents:
    sentence = pos_tag(text)

#--------------------------------SET FEATURES-----------------------------------------
import string
import re
def word2features(sent, i):
    word = sent[i][0]     
    postag = sent[i][1]   

    features = {
            'bias': 1.0,
            'word.lower()': word.lower(),
            'word[-3:]': word[-3:],
            'word[-2:]': word[-2:],
            'word.isupper()': word.isupper(),
            'word.istitle()': word.istitle(),
            'word.isdigit()': word.isdigit(),
            'capitalized': word == word.capitalize(),
            'contain_dash': '-' in word,
            'contain_underscore': '_' in word,
            'contain_dot': '.' in word,
            'contain_slash': '\\' in word or '/' in word,
            'is_hashtag': word.startswith('#'),
            'capital_inside': not word[1:] == word[1:].lower(),
            'is_punctuation': word in string.punctuation,
            'contain_spec_chars': len(re.findall(r'[{}]'.format(string.punctuation), word)) > 0,
            'postag': postag,
        }
    if i > 0:
        word1 = sent[i-1][0]
        postag1 = sent[i-1][1]
        features.update({
            '-1:word.lower()': word1.lower(),
            '-1:word.istitle()': word1.istitle(),
            '-1:word.isupper()': word1.isupper(),
            '-1:capitalized': word1 == word1.capitalize(), 
            '-1:postag': postag1,        
            '-1:contain_dash': '-' in word1,   
            '-1:contain_underscore': '_' in word1,
            '-1:contain_dot': '.' in word1,
            '-1:contain_slash': '\\' in word1 or '/' in word1,
            '-1:is_hashtag': word1.startswith('#'),
            '-1:capital_inside': not word1[1:] == word1[1:].lower(),
            '-1:is_punctuation': word1 in string.punctuation,
            '-1:contain_spec_chars': len(re.findall(r'[{}]'.format(string.punctuation), word1)) > 0,
        })
    else:
        features['BOS'] = True

    if i < len(sent)-1:
        word1 = sent[i+1][0]
        postag1 = sent[i+1][1]
        features.update({
            '+1:word.lower()': word1.lower(),
            '+1:word.istitle()': word1.istitle(),
            '+1:word.isupper()': word1.isupper(),
            '+1:capitalized': word1 == word1.capitalize(), 
            '+1:postag': postag1,        
            '+1:contain_dash': '-' in word1,   
            '+1:contain_underscore': '_' in word1,
            '+1:contain_dot': '.' in word1,
            '+1:contain_slash': '\\' in word1 or '/' in word1,
            '+1:is_hashtag': word1.startswith('#'),
            '+1:capital_inside': not word1[1:] == word1[1:].lower(),
            '+1:is_punctuation': word1 in string.punctuation,
            '+1:contain_spec_chars': len(re.findall(r'[{}]'.format(string.punctuation), word1)) > 0,
        })
    else:
        features['EOS'] = True

    return features


def sent2features(sent):
    return [word2features(sent, i) for i in range(len(sent))]

#--------------------------------------------------------------------------------------------
X = sent2features(sentence)
#-----------------------------------
from sklearn_crfsuite import CRF
import pickle
filename = 'crfs_model_vn2.sav'
loaded_model = pickle.load(open(filename, 'rb'))
Y = loaded_model.predict_single(X)

sents_out = []
sentences_out = []

for i in range(len(sentence)):
    sents_out.append(sentence[i][0])
    sents_out.append(sentence[i][1])
    sents_out.append(Y[i])
    sentences_out.append(sents_out)
    sents_out=[]  
#print(sentences_out)

x1 = []
x2 = []
x3 = []
for x in sentences_out: 
    x1.append(x[0])
    x2.append(x[1])
    x3.append(x[2]) 


import pandas as pd
df = pd.DataFrame(None)
df['word'] = x1
df['postagging'] = x2
df['label'] = x3
df.to_csv('datatest.csv', encoding='utf-16',index='true',sep='\t')

