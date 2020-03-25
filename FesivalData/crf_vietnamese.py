file = open('data.txt','r',encoding='utf-8')

def getWord(wordFeature):
    n = len(wordFeature)
    result = []
    if (n>=3):    
        result.append( " ".join(wordFeature[:-2]))
        result.append(wordFeature[n-2])
        result.append(wordFeature[n-1])
    return(result)

sentences = []
sent = []
for f in file:
    word = getWord( f.split())     
    if (word):        
        sent.append(word)        
    else :
        if (sent):
            sentences.append(sent)             
        sent = []        
file.close()

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

def sent2labels(sent):    
    return [label for token, postag, label in sent]

def sent2tokens(sent):
    return [token for token, postag, label in sent]

X = [sent2features(s) for s in sentences]
y = [sent2labels(s) for s in sentences]
   
    
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=0)

from sklearn_crfsuite import CRF

crf = CRF(algorithm='lbfgs',
          c1=0.1,
          c2=0.1,
          max_iterations=100,
          all_possible_transitions=False)

crf.fit(X_train, y_train)

#-------------------------------------------------------------#
labels = list(crf.classes_)
labels.remove('O')

from sklearn import metrics
from sklearn.metrics import classification_report
from sklearn_crfsuite import scorers
from sklearn_crfsuite import metrics
from collections import Counter

print("Train Predict")
y_pred = crf.predict(X_train)
print(metrics.flat_classification_report(y_train, y_pred, labels = labels))

print("Test Predict")
y_pred = crf.predict(X_test)
print(metrics.flat_classification_report(y_test, y_pred, labels = labels))

#-------------------------------------------------------------#

# save the model to disk
import pickle
filename = 'crfs_model_vn2.sav'
pickle.dump(crf, open(filename, 'wb'))
 
