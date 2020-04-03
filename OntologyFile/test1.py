class Data:
    def __init__(self, text, label):
        self.text = text
        self.label = label
    
    def toString(self):
        print(self.text + " - " + self.label)

import pandas as pd
df = pd.read_csv('../FesivalData/output/dataFromWiki.csv', encoding='utf-16', header=None, sep='\t')
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
    if ( (i == range(numData)) or isEndFes(listLabels[i], listLabels[i-1])) :         
        datas.append(Data(text,label))   
        results.append(datas)
        label = ""
        datas = []
        continue
    elif (isEndSen(lb)) :         
        if (check(listLabels[i-1],"I")):
            datas.append(Data(text,label))       
        continue
    if (check(lb,"I") and (lb[2:] == label)) :        
        text = text + " " + listTexts[i]
    elif (check(lb,"B")) :
        if (label != "") :
            datas.append(Data(text,label))        
        label = lb[2:]
        text = listTexts[i]


FIELD_1 = ['AC1', 'AC2', 'AC3', 'AC4' , 'AC5' , 'LOC' , 'TIM' , 'CO1' , 'CO2' , 'CO3' , 'PER' , 'ETH' , 'REL' , 'ANN','FFT']
FIELD_2 = ['CER', 'FAM' ,'ORG', 'REC']
def isField(label, field):
    for l in field :
        if ( l == label): return True
    return False

def equal(str1, str2):
    return str1.lower() == str2.lower()

def isContain(str1, str2):
    return (str2.lower() in str1.lower()) 

def isDuplication(text, list):
    for l in list:
        if (isContain(l,text)):
            return True
    return False

data = []
for fes in results:
    list = {
        'FES' : '',
        'AC1' : [],
        'AC2' : [],
        'AC3' : [],
        'AC4' : [],
        'AC5' : [],        
        'LOC' : [],
        'TIM' : [],
        'ORG' : [],
        'CO1' : [],
        'CO2' : [],
        'CO3' : [],
        'PER' : [], 
        'REC' : [],        
        'ETH' : [],
        'REL' : [],
        'ANN' : [],
        'FAM' : [],        
        'CER' : [],
        'FFT' : [],       
    }
    for d in fes :
        # print(type(d.text))  
        if (d.label == "") : continue
        if ( d.label == "FES") :
            list[d.label] = d.text         
        elif ( isField(d.label, FIELD_1)) :
            flag = True #không trùng             
            for i in range(len(list[d.label])) :
                if (isContain(list[d.label][i],d.text)):
                    flag = False                    
                    break                   
                elif (isContain(d.text,list[d.label][i])):                    
                    list[d.label][i] = d.text                    
                    flag = False
                    break         
            if (flag) :
                list[d.label].append(d.text)

        elif ( isField(d.label, FIELD_2)) :
            list[d.label].append(d.text)                
    data.append(list) 
# print("Có: ",len(data)," lễ hội.")
def cleanData(dataInput,object):
    a=[]
    if ( isField(object, FIELD_1)):
       for x in data:
            for y in x.get(object,[]):
                flag = True #không trùng
                for i in range(len(a)) :
                    if (isContain(a[i],y) and len(a[i])-len(y)<19): 
                        a.append(a[i])
                        flag = False
                        break                   
                    elif (isContain(y,a[i]) and len(y)-len(a[i])<10):
                        a[i]=y
                        a.append(y)
                        flag = False
                        break         
                if (flag) : a.append(y) 
    if (isField(object, FIELD_2)):
        for x in data:
            a.append(object,[])
    if (object=='FES'):
        for x in data:
            a = x.get('FES',[])
    return a

def setIdForList(dataInput,object,value):
    a=[]
    if ( isField(object, FIELD_1)):
        for x in dataInput:
            for y in x.get(object,[]):
                flag = True #không trùng
                for i in range(len(a)) :
                    if (isContain(a[i],y) and len(a[i])-len(y)<10): 
                        flag = False
                        break                   
                    elif (isContain(y,a[i]) and len(y)-len(a[i])<10):
                        a[i] = y
                        flag = False
                        break         
                if (flag) : a.append(y)   
        #setID
        a=set(a)
        id_dict = {}
        for index, i in enumerate(a):
            id_dict[i] = index
            if i==value:
                return str(index) 
    if (object=='FES'):
        for x in dataInput:
            a.append(x.get(object,[]))
        a=set(a) #xoa phan tu trung
        id_dict = {}
        for index, i in enumerate(a):
            id_dict[i] = index
            if i==value:
                return str(index) 


       

#set id 

# def setIdForList(dataInput,object,value):
#     a=[]
#     b=[]
  
#     for x in dataInput:
#         for y in x.get(object,[]):
#             flag = True #không trùng
#             for i in range(len(a)) :
#                 if (isContain(a[i],y) and len(a[i])-len(y)<10): 
#                     flag = False
#                     break                   
#                 elif (isContain(y,a[i]) and len(y)-len(a[i])<10):
#                     a[i] = y
#                     flag = False
#                     break         
#             if (flag) : a.append(y)   
#     #setID
#     a=set(a)
#     id_dict = {}
#     for index, i in enumerate(a):
#         id_dict[i] = index
#         if i==value:
#             return str(index)  
# a=[]
# c=[]
# for x in data:
#     c += x.get('LOC',[])
# print(len(c))
# for x in data:
#     for y in x.get('LOC',[]):
#         flag = True #không trùng
#         for i in range(len(a)) :
#             if (isContain(a[i],y) and len(a[i])-len(y)<19): 
#                 a.append(a[i])
#                 flag = False
#                 break                   
#             elif (isContain(y,a[i]) and len(y)-len(a[i])<10):
#                 a[i]=y
#                 a.append(y)
#                 flag = False
#                 break         
#         if (flag) : a.append(y)  
# print(len(a))
# for i in a:
#     b = setIdForList(data,'LOC',i) 
# import csv
# with open('t.csv','w', newline='',encoding='utf-16') as csvfile:
#     fieldnames = ["Mã lễ hội","Tên lễ hội"]
#     writer = csv.DictWriter(csvfile, fieldnames=fieldnames,delimiter='\t')
#     writer.writeheader()
#     fes=[]
    
#     for x in data :
#         fes = x.get('FES',[])
#         for i in x.get('LOC',[]):
#             writer.writerow({'Mã lễ hội':"F"+setIdForList(data,'LOC',i),'Tên lễ hội':i})
import csv

with open('test1.csv','w', newline='',encoding='utf-16') as csvfile:
    fieldnames = ["Mã lễ hội","Tên lễ hội","Địa điểm","Mã LOC","Thời gian","Tên gọi khác",
                "Lịch sử hình thành","Hoạt động vui chơi","Mã AC1","Hoạt động du lịch","Mã AC2",
                "Hoạt động mang tính lịch sử","Mã AC3","Hoạt động tín ngưỡng","Mã AC4",
                "Hoạt động văn hóa dân gian","Mã AC5","Mục đích quảng bá","Mã CO1",
                "Mục đích tâm linh","Mã CO2","Mục đích tưởng nhớ","Mã CO3",
                "Dân tộc","Mã ETH","Tôn giáo","Mã REL","Nhân vật","Mã PER","Danh lam","Mã FAM",
                "Đặc điểm danh lam","Danh hiệu","Mã REC"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames,delimiter='\t')
    writer.writeheader()
    fes=[]
    
    for x in data :
        fes = x.get('FES',[])
        for i in cleanData(data,'LOC'):
            writer.writerow({'Mã lễ hội':"F"+setIdForList(data,'FES',fes),'Tên lễ hội':fes,'Địa điểm':i,
                                                                    'Mã LOC':setIdForList(data,'LOC',i),'Thời gian':"",'Tên gọi khác':"",
                                                                    'Lịch sử hình thành':"",'Hoạt động vui chơi':"",'Mã AC1':"",
                                                                    'Hoạt động du lịch':"",'Mã AC2':"",'Hoạt động mang tính lịch sử':"",
                                                                    'Mã AC3':"",'Hoạt động tín ngưỡng':"",'Mã AC4':"",
                                                                    'Hoạt động văn hóa dân gian':"","Mã AC5":"",'Mục đích quảng bá':"",'Mã CO1':"",
                                                                    'Mục đích tâm linh':"",'Mã CO2':"",'Mục đích tưởng nhớ':"","Mã CO3":"",
                                                                    'Dân tộc':"",'Mã ETH':"",'Tôn giáo':"",'Mã REL':"",'Nhân vật':"",'Mã PER':"",
                                                                    'Danh lam':"",'Mã FAM':"",'Đặc điểm danh lam':"",'Danh hiệu':"",
                                                                    'Mã REC':""})
        for i in cleanData(data,'TIM'):
            writer.writerow({'Mã lễ hội':"F"+setIdForList(data,'FES',fes),'Tên lễ hội':fes,'Địa điểm':"",
                                                                    'Mã LOC':"",'Thời gian':i,'Tên gọi khác':"",
                                                                    'Lịch sử hình thành':"",'Hoạt động vui chơi':"",'Mã AC1':"",
                                                                    'Hoạt động du lịch':"",'Mã AC2':"",'Hoạt động mang tính lịch sử':"",
                                                                    'Mã AC3':"",'Hoạt động tín ngưỡng':"",'Mã AC4':"",
                                                                    'Hoạt động văn hóa dân gian':"","Mã AC5":"",'Mục đích quảng bá':"",'Mã CO1':"",
                                                                    'Mục đích tâm linh':"",'Mã CO2':"",'Mục đích tưởng nhớ':"","Mã CO3":"",
                                                                    'Dân tộc':"",'Mã ETH':"",'Tôn giáo':"",'Mã REL':"",'Nhân vật':"",'Mã PER':"",
                                                                    'Danh lam':"",'Mã FAM':"",'Đặc điểm danh lam':"",'Danh hiệu':"",
                                                                    'Mã REC':""})
        for i in x.get('ANN',[]):
            writer.writerow({'Mã lễ hội':"F"+setIdForList(data,'FES',fes),'Tên lễ hội':fes,'Địa điểm':"",
                                                                    'Mã LOC':"",'Thời gian':"",'Tên gọi khác':i,
                                                                    'Lịch sử hình thành':"",'Hoạt động vui chơi':"",'Mã AC1':"",
                                                                    'Hoạt động du lịch':"",'Mã AC2':"",'Hoạt động mang tính lịch sử':"",
                                                                    'Mã AC3':"",'Hoạt động tín ngưỡng':"",'Mã AC4':"",
                                                                    'Hoạt động văn hóa dân gian':"","Mã AC5":"",'Mục đích quảng bá':"",'Mã CO1':"",
                                                                    'Mục đích tâm linh':"",'Mã CO2':"",'Mục đích tưởng nhớ':"","Mã CO3":"",
                                                                    'Dân tộc':"",'Mã ETH':"",'Tôn giáo':"",'Mã REL':"",'Nhân vật':"",'Mã PER':"",
                                                                    'Danh lam':"",'Mã FAM':"",'Đặc điểm danh lam':"",'Danh hiệu':"",
                                                                    'Mã REC':""})
        # for i in x.get('FFT',[]):
        #     writer.writerow({'Mã lễ hội':"F"+setIdForList(data,'FES',fes),'Tên lễ hội':fes,'Địa điểm':"",
        #                                                             'Mã LOC':"",'Thời gian':"",'Tên gọi khác':"",
        #                                                             'Lịch sử hình thành':i,'Hoạt động vui chơi':"",'Mã AC1':"",
        #                                                             'Hoạt động du lịch':"",'Mã AC2':"",'Hoạt động mang tính lịch sử':"",
        #                                                             'Mã AC3':"",'Hoạt động tín ngưỡng':"",'Mã AC4':"",
        #                                                             'Hoạt động văn hóa dân gian':"","Mã AC5":"",'Mục đích quảng bá':"",'Mã CO1':"",
        #                                                             'Mục đích tâm linh':"",'Mã CO2':"",'Mục đích tưởng nhớ':"","Mã CO3":"",
        #                                                             'Dân tộc':"",'Mã ETH':"",'Tôn giáo':"",'Mã REL':"",'Nhân vật':"",'Mã PER':"",
        #                                                             'Danh lam':"",'Mã FAM':"",'Đặc điểm danh lam':"",'Danh hiệu':"",
        #                                                             'Mã REC':""})
        # for i in x.get('AC1',[]):
        #     writer.writerow({'Mã lễ hội':"F"+setIdForList(data,'FES',fes),'Tên lễ hội':fes,'Địa điểm':"",
        #                                                             'Mã LOC':"",'Thời gian':"",'Tên gọi khác':"",
        #                                                             'Lịch sử hình thành':"",'Hoạt động vui chơi':i,'Mã AC1':'AA'+setIdForList(data,'AC1',i),
        #                                                             'Hoạt động du lịch':"",'Mã AC2':"",'Hoạt động mang tính lịch sử':"",
        #                                                             'Mã AC3':"",'Hoạt động tín ngưỡng':"",'Mã AC4':"",
        #                                                             'Hoạt động văn hóa dân gian':"","Mã AC5":"",'Mục đích quảng bá':"",'Mã CO1':"",
        #                                                             'Mục đích tâm linh':"",'Mã CO2':"",'Mục đích tưởng nhớ':"","Mã CO3":"",
        #                                                             'Dân tộc':"",'Mã ETH':"",'Tôn giáo':"",'Mã REL':"",'Nhân vật':"",'Mã PER':"",
        #                                                             'Danh lam':"",'Mã FAM':"",'Đặc điểm danh lam':"",'Danh hiệu':"",
        #                                                             'Mã REC':""})
                                    
        # for i in x.get('AC2',[]):
        #     writer.writerow({'Mã lễ hội':"F"+setIdForList(data,'FES',fes),'Tên lễ hội':fes,'Địa điểm':"",
        #                                                             'Mã LOC':"",'Thời gian':"",'Tên gọi khác':"",
        #                                                             'Lịch sử hình thành':"",'Hoạt động vui chơi':"",'Mã AC1':"",
        #                                                             'Hoạt động du lịch':i,'Mã AC2':'AB'+setIdForList(data,'AC2',i),'Hoạt động mang tính lịch sử':"",
        #                                                             'Mã AC3':"",'Hoạt động tín ngưỡng':"",'Mã AC4':"",
        #                                                             'Hoạt động văn hóa dân gian':"","Mã AC5":"",'Mục đích quảng bá':"",'Mã CO1':"",
        #                                                             'Mục đích tâm linh':"",'Mã CO2':"",'Mục đích tưởng nhớ':"","Mã CO3":"",
        #                                                             'Dân tộc':"",'Mã ETH':"",'Tôn giáo':"",'Mã REL':"",'Nhân vật':"",'Mã PER':"",
        #                                                             'Danh lam':"",'Mã FAM':"",'Đặc điểm danh lam':"",'Danh hiệu':"",
        #                                                             'Mã REC':""})
        # for i in x.get('AC3',[]):
        #     writer.writerow({'Mã lễ hội':"F"+setIdForList(data,'FES',fes),'Tên lễ hội':fes,'Địa điểm':"",
        #                                                             'Mã LOC':"",'Thời gian':"",'Tên gọi khác':"",
        #                                                             'Lịch sử hình thành':"",'Hoạt động vui chơi':"",'Mã AC1':"",
        #                                                             'Hoạt động du lịch':"",'Mã AC2':"",'Hoạt động mang tính lịch sử':i,
        #                                                             'Mã AC3':'AC'+setIdForList(data,'AC3',i),'Hoạt động tín ngưỡng':"",'Mã AC4':"",
        #                                                             'Hoạt động văn hóa dân gian':"","Mã AC5":"",'Mục đích quảng bá':"",'Mã CO1':"",
        #                                                             'Mục đích tâm linh':"",'Mã CO2':"",'Mục đích tưởng nhớ':"","Mã CO3":"",
        #                                                             'Dân tộc':"",'Mã ETH':"",'Tôn giáo':"",'Mã REL':"",'Nhân vật':"",'Mã PER':"",
        #                                                             'Danh lam':"",'Mã FAM':"",'Đặc điểm danh lam':"",'Danh hiệu':"",
        #                                                             'Mã REC':""})
        # for i in x.get('AC4',[]):
        #     writer.writerow({'Mã lễ hội':"F"+setIdForList(data,'FES',fes),'Tên lễ hội':fes,'Địa điểm':"",
        #                                                             'Mã LOC':"",'Thời gian':"",'Tên gọi khác':"",
        #                                                             'Lịch sử hình thành':"",'Hoạt động vui chơi':"",'Mã AC1':"",
        #                                                             'Hoạt động du lịch':"",'Mã AC2':"",'Hoạt động mang tính lịch sử':"",
        #                                                             'Mã AC3':"",'Hoạt động tín ngưỡng':i,'Mã AC4':'AD'+setIdForList(data,'AC4',i),
        #                                                             'Hoạt động văn hóa dân gian':"","Mã AC5":"",'Mục đích quảng bá':"",'Mã CO1':"",
        #                                                             'Mục đích tâm linh':"",'Mã CO2':"",'Mục đích tưởng nhớ':"","Mã CO3":"",
        #                                                             'Dân tộc':"",'Mã ETH':"",'Tôn giáo':"",'Mã REL':"",'Nhân vật':"",'Mã PER':"",
        #                                                             'Danh lam':"",'Mã FAM':"",'Đặc điểm danh lam':"",'Danh hiệu':"",
        #                                                             'Mã REC':""})
        # for i in x.get('AC5',[]):
        #     writer.writerow({'Mã lễ hội':"F"+setIdForList(data,'FES',fes),'Tên lễ hội':fes,'Địa điểm':"",
        #                                                             'Mã LOC':"",'Thời gian':"",'Tên gọi khác':"",
        #                                                             'Lịch sử hình thành':"",'Hoạt động vui chơi':"",'Mã AC1':"",
        #                                                             'Hoạt động du lịch':"",'Mã AC2':"",'Hoạt động mang tính lịch sử':"",
        #                                                             'Mã AC3':"",'Hoạt động tín ngưỡng':"",'Mã AC4':"",
        #                                                             'Hoạt động văn hóa dân gian':i,"Mã AC5":'AE'+setIdForList(data,'AC5',i),'Mục đích quảng bá':"",'Mã CO1':"",
        #                                                             'Mục đích tâm linh':"",'Mã CO2':"",'Mục đích tưởng nhớ':"","Mã CO3":"",
        #                                                             'Dân tộc':"",'Mã ETH':"",'Tôn giáo':"",'Mã REL':"",'Nhân vật':"",'Mã PER':"",
        #                                                             'Danh lam':"",'Mã FAM':"",'Đặc điểm danh lam':"",'Danh hiệu':"",
        #                                                             'Mã REC':""})
        # for i in x.get('CO1',[]):
        #     writer.writerow({'Mã lễ hội':"F"+setIdForList(data,'FES',fes),'Tên lễ hội':fes,'Địa điểm':"",
        #                                                             'Mã LOC':"",'Thời gian':"",'Tên gọi khác':"",
        #                                                             'Lịch sử hình thành':"",'Hoạt động vui chơi':"",'Mã AC1':"",
        #                                                             'Hoạt động du lịch':"",'Mã AC2':"",'Hoạt động mang tính lịch sử':"",
        #                                                             'Mã AC3':"",'Hoạt động tín ngưỡng':"",'Mã AC4':"",
        #                                                             'Hoạt động văn hóa dân gian':"","Mã AC5":"",'Mục đích quảng bá':i,
        #                                                             'Mã CO1':'CA'+setIdForList(data,'CO1',i),
        #                                                             'Mục đích tâm linh':"",'Mã CO2':"",'Mục đích tưởng nhớ':"","Mã CO3":"",
        #                                                             'Dân tộc':"",'Mã ETH':"",'Tôn giáo':"",'Mã REL':"",'Nhân vật':"",'Mã PER':"",
        #                                                             'Danh lam':"",'Mã FAM':"",'Đặc điểm danh lam':"",'Danh hiệu':"",
        #                                                             'Mã REC':""})
        # for i in x.get('CO2',[]):
        #     writer.writerow({'Mã lễ hội':"F"+setIdForList(data,'FES',fes),'Tên lễ hội':fes,'Địa điểm':"",
        #                                                             'Mã LOC':"",'Thời gian':"",'Tên gọi khác':"",
        #                                                             'Lịch sử hình thành':"",'Hoạt động vui chơi':"",'Mã AC1':"",
        #                                                             'Hoạt động du lịch':"",'Mã AC2':"",'Hoạt động mang tính lịch sử':"",
        #                                                             'Mã AC3':"",'Hoạt động tín ngưỡng':"",'Mã AC4':"",
        #                                                             'Hoạt động văn hóa dân gian':"","Mã AC5":"",'Mục đích quảng bá':"",'Mã CO1':"",
        #                                                             'Mục đích tâm linh':i,'Mã CO2':'CB'+setIdForList(data,'CO2',i),'Mục đích tưởng nhớ':"","Mã CO3":"",
        #                                                             'Dân tộc':"",'Mã ETH':"",'Tôn giáo':"",'Mã REL':"",'Nhân vật':"",'Mã PER':"",
        #                                                             'Danh lam':"",'Mã FAM':"",'Đặc điểm danh lam':"",'Danh hiệu':"",
        #                                                             'Mã REC':""})
        # for i in x.get('CO3',[]):
        #     writer.writerow({'Mã lễ hội':"F"+setIdForList(data,'FES',fes),'Tên lễ hội':fes,'Địa điểm':"",
        #                                                             'Mã LOC':"",'Thời gian':"",'Tên gọi khác':"",
        #                                                             'Lịch sử hình thành':"",'Hoạt động vui chơi':"",'Mã AC1':"",
        #                                                             'Hoạt động du lịch':"",'Mã AC2':"",'Hoạt động mang tính lịch sử':"",
        #                                                             'Mã AC3':"",'Hoạt động tín ngưỡng':"",'Mã AC4':"",
        #                                                             'Hoạt động văn hóa dân gian':"","Mã AC5":"",'Mục đích quảng bá':"",'Mã CO1':"",
        #                                                             'Mục đích tâm linh':"",'Mã CO2':"",'Mục đích tưởng nhớ':i,"Mã CO3":'AC'+setIdForList(data,'CO3',i),
        #                                                             'Dân tộc':"",'Mã ETH':"",'Tôn giáo':"",'Mã REL':"",'Nhân vật':"",'Mã PER':"",
        #                                                             'Danh lam':"",'Mã FAM':"",'Đặc điểm danh lam':"",'Danh hiệu':"",
        #                                                             'Mã REC':""})
        # for i in x.get('ETH',[]):
        #     writer.writerow({'Mã lễ hội':"F"+setIdForList(data,'FES',fes),'Tên lễ hội':fes,'Địa điểm':"",
        #                                                             'Mã LOC':"",'Thời gian':"",'Tên gọi khác':"",
        #                                                             'Lịch sử hình thành':"",'Hoạt động vui chơi':"",'Mã AC1':"",
        #                                                             'Hoạt động du lịch':"",'Mã AC2':"",'Hoạt động mang tính lịch sử':"",
        #                                                             'Mã AC3':"",'Hoạt động tín ngưỡng':"",'Mã AC4':"",
        #                                                             'Hoạt động văn hóa dân gian':"","Mã AC5":"",'Mục đích quảng bá':"",'Mã CO1':"",
        #                                                             'Mục đích tâm linh':"",'Mã CO2':"",'Mục đích tưởng nhớ':"","Mã CO3":"",
        #                                                             'Dân tộc':i,'Mã ETH':'E'+setIdForList(data,'ETH',i),'Tôn giáo':"",'Mã REL':"",'Nhân vật':"",'Mã PER':"",
        #                                                             'Danh lam':"",'Mã FAM':"",'Đặc điểm danh lam':"",'Danh hiệu':"",
        #                                                             'Mã REC':""})
        # for i in x.get('REL',[]):
        #     writer.writerow({'Mã lễ hội':"F"+setIdForList(data,'FES',fes),'Tên lễ hội':fes,'Địa điểm':"",
        #                                                           'Mã LOC':"",'Thời gian':"",'Tên gọi khác':"",
        #                                                           'Lịch sử hình thành':"",'Hoạt động vui chơi':"",'Mã AC1':"",
        #                                                           'Hoạt động du lịch':"",'Mã AC2':"",'Hoạt động mang tính lịch sử':"",
        #                                                           'Mã AC3':"",'Hoạt động tín ngưỡng':"",'Mã AC4':"",
        #                                                           'Hoạt động văn hóa dân gian':"","Mã AC5":"",'Mục đích quảng bá':"",'Mã CO1':"",
        #                                                           'Mục đích tâm linh':"",'Mã CO2':"",'Mục đích tưởng nhớ':"","Mã CO3":"",
        #                                                           'Dân tộc':"",'Mã ETH':"",'Tôn giáo':i,'Mã REL':'R'+setIdForList(data,'REL',i),'Nhân vật':"",'Mã PER':"",
        #                                                           'Danh lam':"",'Mã FAM':"",'Đặc điểm danh lam':"",'Danh hiệu':"",
        #                                                           'Mã REC':""})
        # for i in x.get('PER',[]):
        #     writer.writerow({'Mã lễ hội':"F"+setIdForList(data,'FES',fes),'Tên lễ hội':fes,'Địa điểm':"",
        #                                                           'Mã LOC':"",'Thời gian':"",'Tên gọi khác':"",
        #                                                           'Lịch sử hình thành':"",'Hoạt động vui chơi':"",'Mã AC1':"",
        #                                                           'Hoạt động du lịch':"",'Mã AC2':"",'Hoạt động mang tính lịch sử':"",
        #                                                           'Mã AC3':"",'Hoạt động tín ngưỡng':"",'Mã AC4':"",
        #                                                           'Hoạt động văn hóa dân gian':"","Mã AC5":"",'Mục đích quảng bá':"",'Mã CO1':"",
        #                                                           'Mục đích tâm linh':"",'Mã CO2':"",'Mục đích tưởng nhớ':"","Mã CO3":"",
        #                                                           'Dân tộc':"",'Mã ETH':"",'Tôn giáo':"",'Mã REL':"",'Nhân vật':i,'Mã PER':'P'+setIdForList(data,'PER',i),
        #                                                           'Danh lam':"",'Mã FAM':"",'Đặc điểm danh lam':"",'Danh hiệu':"",
        #                                                           'Mã REC':""})
                                    
        # for i in x.get('FAM',[]):
        #     for j in x.get('CER',[]):
        #             writer.writerow({'Mã lễ hội':"F"+setIdForList(data,'FES',fes),'Tên lễ hội':fes,'Địa điểm':"",
        #                                     'Mã LOC':"",'Thời gian':"",'Tên gọi khác':"",
        #                                     'Lịch sử hình thành':"",'Hoạt động vui chơi':"",'Mã AC1':"",
        #                                     'Hoạt động du lịch':"",'Mã AC2':"",'Hoạt động mang tính lịch sử':"",
        #                                     'Mã AC3':"",'Hoạt động tín ngưỡng':"",'Mã AC4':"",
        #                                     'Hoạt động văn hóa dân gian':"","Mã AC5":"",'Mục đích quảng bá':"",'Mã CO1':"",
        #                                     'Mục đích tâm linh':"",'Mã CO2':"",'Mục đích tưởng nhớ':"","Mã CO3":"",
        #                                     'Dân tộc':"",'Mã ETH':"",'Tôn giáo':"",'Mã REL':"",'Nhân vật':"",'Mã PER':"",
        #                                     'Danh lam':i,'Mã FAM':'FA'+setIdForList(data,'FAM',i),'Đặc điểm danh lam':j,'Danh hiệu':"",
        #                                     'Mã REC':""})
        # for i in x.get('REC',[]):
        #     writer.writerow({'Mã lễ hội':"F"+setIdForList(data,'FES',fes),'Tên lễ hội':fes,'Địa điểm':"",
        #                                             'Mã LOC':"",'Thời gian':"",'Tên gọi khác':"",
        #                                             'Lịch sử hình thành':"",'Hoạt động vui chơi':"",'Mã AC1':"",
        #                                             'Hoạt động du lịch':"",'Mã AC2':"",'Hoạt động mang tính lịch sử':"",
        #                                             'Mã AC3':"",'Hoạt động tín ngưỡng':"",'Mã AC4':"",
        #                                             'Hoạt động văn hóa dân gian':"","Mã AC5":"",'Mục đích quảng bá':"",'Mã CO1':"",
        #                                             'Mục đích tâm linh':"",'Mã CO2':"",'Mục đích tưởng nhớ':"","Mã CO3":"",
        #                                             'Dân tộc':"",'Mã ETH':"",'Tôn giáo':"",'Mã REL':"",'Nhân vật':"",'Mã PER':"",
        #                                             'Danh lam':"",'Mã FAM':"",'Đặc điểm danh lam':"",'Danh hiệu':i,
        #                                             'Mã REC':'RE'+setIdForList(data,'REC',i)})
                                    
