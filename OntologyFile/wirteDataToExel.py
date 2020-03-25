class Data:
    def __init__(self, text, label):
        self.text = text
        self.label = label
    
    def toString(self):
        print(self.text + " - " + self.label)

import pandas as pd
df = pd.read_csv('../FesivalData/output/dataFrom26FesivalOfLoca.csv', encoding='utf-16', header=None, sep='\t')
numData = len(df)

listTexts = []
listLabels = []
for row in range(numData):
    listTexts.append(df[0][row])
    listLabels.append(df[2][row])

def check(label, charact):    
    return label[0] == charact
def isEndSen(text): #kết thúc 1 câu
    return isinstance(text,float)
def isEndFes(before, after): #kết thúc 1 lễ hội
    return isEndSen(before) and isEndSen(after)

text = ""
label = ""
datas = []
results = []
for i in range(numData):
    lb = listLabels[i] 
    if ( (i == range(numData)) or isEndFes(listLabels[i], listLabels[i-1]) ) : 
        datas.append(Data(text,label))   
        results.append(datas)
        datas = []
    if (isEndSen(lb)) : continue    
    if (check(lb,"I") and (lb[2:] == label)) :
        text = text + " " + listTexts[i]
    elif (check(lb,"B")) :
        datas.append(Data(text,label))        
        label = lb[2:]
        text = listTexts[i]

data = []
for fes in results:
    list = {
        'FES' : '',
        'EVE' : [],
        'CON' : [],
        'LOC' : [],
        'TIM' : [],
        'ETH' : [],
        'REL' : [],
        'FAM' : '',
        'REC' : [],
        'CER' : [],
        'FFT' : '',
        'ANN' : [],
        'PER' : [],
        'ORG' : '',
        'FHC' : '',
        'FIT' : '',
        'FHE' : '',
        'FIL' : '',
        'AHC' : '',
        'FOR' : ''
    }
    for d in fes :  
        if (d.label == "") : continue           
        if ( d.label == "EVE" or 
                d.label == "CON" or 
                d.label == "LOC" or 
                d.label == "TIM" or 
                d.label == "ETH" or 
                d.label == "REL" or 
                d.label == "REC" or 
                d.label == "CER" or 
                d.label == "ANN" or 
                d.label == "PER") :
            list[d.label].append(d.text)        
        else : 
            list[d.label] = d.text
    data.append(list) 

print(data)