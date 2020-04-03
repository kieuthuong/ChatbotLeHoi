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
        'LOC' : [],
        'TIM' : [],
        'ANN' : [],
        'FFT' : [],
        'AC1' : [],
        'AC2' : [],
        'AC3' : [],
        'AC4' : [],
        'AC5' : [],
        'CO1' : [],
        'CO2' : [],
        'CO3' : [],
        'ETH' : [],
        'REL' : [],
        'PER' : [],
        'FAM' : [],
        'CER' : [],
        'REC' : [],
        'ORG' : [],
        'FHC' : '',
        'FIT' : '',
        'FHE' : '',
        'FIL' : '',
        'AHC' : '',
        'FOR' : ''
    }
    for d in fes :  
        if (d.label == "") : continue           
        if ( d.label == "LOC" or 
                d.label == "TIM" or 
                d.label == "ANN" or 
                d.label == "FFT" or
                d.label == "AC1" or
                d.label == "AC2" or
                d.label == "AC3" or
                d.label == "AC4" or 
                d.label == "AC5" or
                d.label == "CO1" or
                d.label == "CO2" or
                d.label == "CO3" or
                d.label == "ETH" or 
                d.label == "REL" or
                d.label == "PER" or
                d.label == "FAM" or
                d.label == "CER" or 
                d.label == "REC" or 
                d.label == "ORG") :
            list[d.label].append(d.text)        
        else : 
            list[d.label] = d.text
    data.append(list) 
# from csv import writer
# from io import StringIO
# import codecs
# import unicodedata
# def append_list_as_row(file_name, list_of_elem):
#   with open(file_name, 'a+', newline='',encoding='utf-8') as write_obj:
#       csv_writer = writer(write_obj)
#       csv_writer.writerow(list_of_elem)

# for x in data:
#     x1=[]
#     x6=[]
#     x1.append(x.get('FES'))
#     x6.append(x.get('AC1'))
#     row_contents = [x1]
#     print(type(row_contents))
#       # print(row_contents)
#     append_list_as_row('students.csv', row_contents)
    # a=[]
    # for x in data :
    #     a += x.get('AC1',[])
    #     a += x.get('AC2',[])
    # a=set(a) #xoa phan tu trung
    # id_dict = {}
    # for index, i in enumerate(a):
    #     id_dict[i] = indexdef setIdForList(dataInput,object,value):#setID của object cho value trong tập dữ liệu dataInput
    a=[]
    for x in dataInput:
        a += x.get(object,[])
        a=set(a) #xoa phan tu trung
        id_dict = {}
        for index, i in enumerate(a):
            id_dict[i] = index
            if i==value:
                return str(index)  
    import csv
    with open('name.csv','w', newline='',encoding='utf-16') as csvfile:
        fieldnames = ["name","action","x7","id"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames,delimiter='\t')
        writer.writeheader()
        for x in data:
            x1=x.get('FES')
            x6=[]
            x7=[]
            # l6=len(x6)
            # l7=len(x7)
            # listLen=[l6,l7]
            
            for j in x.get('AC1',[]):
                    writer.writerow({'name':x1, 'action':j,'x7':"",'id':setIdForList(data,'AC1',j)})
            for j in x.get('AC2',[]):
                    writer.writerow({'name':x1, 'action':"",'x7':j,'id':id_dict[j]})
       

