class Data:
    def __init__(self, text, label):
        self.text = text
        self.label = label
    
    def toString(self):
        print(self.text + " - " + self.label)

import pandas as pd
df = pd.read_csv('../FesivalData/output/DATA.csv', encoding='utf-16', header=None, sep='\t')
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
            if (flag) : list[d.label].append(d.text)   
        elif ( isField(d.label, FIELD_2)) :
            list[d.label].append(d.text)                
    data.append(list) 


print("Có: ",len(data)," lễ hội.")
# for d in data:    
#     print(d['FES'])
#     print(d['REC'])


       

#set id 

def setIdForList(dataInput,object,value):
    a=[]
    for x in dataInput:
        a += x.get(object,[])
    a=set(a) #xoa phan tu trung

    id_dict = {}
    
    for index, i in enumerate(a):
        id_dict[i.lower()] = index
        if i.lower()==value.lower():
            return str(index)  
                
def setIdForStr(dataInput,object,value):
    a=[]
    for x in dataInput:
        a.append(x.get(object,[]))
    a=set(a) #xoa phan tu trung
    id_dict = {}
    for index, i in enumerate(a):
        id_dict[i.lower()] = index
        if i.lower()==value.lower():
            return str(index)

#wirte to csv
#file rec.csv
x1=[]
x2=[]
x3=[]
x4=[]
for x in data:
  z1=x.get('REC',[])
  z2=x.get('ORG',[])
  len1=len(z1)
  len2=len(z2)
  if len1==0:
      x1.append("")
      x2.append("")
      x3.append("")
      x4.append("")
  if len1>0 and len2==0:
      for i in z1:
          x1.append(i)
          x3.append("RE"+setIdForList(data,'REC',i))
          x2.append("")
          x4.append("")
  if len1>0 and len2>0:
      j=len1-len2
      for i in z1:
          x1.append(i)
          x3.append("RE"+setIdForList(data,'REC',i))
      for i in z2:
          x2.append(i)
          x4.append("O"+setIdForList(data,'ORG',i))
      a=1
      while(a<=j):
          x2.append("")
          x4.append("")
          a += 1

import pandas as pd
df = pd.DataFrame(None)
df['REC'] = x1
df['IdREC'] = x3
df['ORG'] = x2
df['IdORG'] = x4
df.to_csv('saveRec.csv', encoding='utf-16',index='true',sep='\t')

#file link lehoi
x5=[]
x6=[]
for x in data:
  x5.append(x.get('FES',[]))
  x6.append('F'+setIdForStr(data,'FES',x.get('FES',[])))
import pandas as pd
df1 = pd.DataFrame(None)
df1['FES'] = x5
df1['IdFES'] = x6
df1.to_csv('savLinkFes.csv', encoding='utf-16',index='true',sep='\t')

#file fesival
import csv
with open('saveAllFes.csv','w', newline='',encoding='utf-16') as csvfile:
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
    for x in data:
        fes = x.get('FES',[])
        for i in x.get('LOC',[]):
            writer.writerow({'Mã lễ hội':"F"+setIdForStr(data,'FES',fes),'Tên lễ hội':fes,'Địa điểm':i,
                                                                    'Mã LOC':"L"+setIdForList(data,'LOC',i),'Thời gian':"",'Tên gọi khác':"",
                                                                    'Lịch sử hình thành':"",'Hoạt động vui chơi':"",'Mã AC1':"",
                                                                    'Hoạt động du lịch':"",'Mã AC2':"",'Hoạt động mang tính lịch sử':"",
                                                                    'Mã AC3':"",'Hoạt động tín ngưỡng':"",'Mã AC4':"",
                                                                    'Hoạt động văn hóa dân gian':"","Mã AC5":"",'Mục đích quảng bá':"",'Mã CO1':"",
                                                                    'Mục đích tâm linh':"",'Mã CO2':"",'Mục đích tưởng nhớ':"","Mã CO3":"",
                                                                    'Dân tộc':"",'Mã ETH':"",'Tôn giáo':"",'Mã REL':"",'Nhân vật':"",'Mã PER':"",
                                                                    'Danh lam':"",'Mã FAM':"",'Đặc điểm danh lam':"",'Danh hiệu':"",
                                                                    'Mã REC':""})
        for i in x.get('TIM',[]):
            writer.writerow({'Mã lễ hội':"F"+setIdForStr(data,'FES',fes),'Tên lễ hội':fes,'Địa điểm':"",
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
            writer.writerow({'Mã lễ hội':"F"+setIdForStr(data,'FES',fes),'Tên lễ hội':fes,'Địa điểm':"",
                                                                    'Mã LOC':"",'Thời gian':"",'Tên gọi khác':i,
                                                                    'Lịch sử hình thành':"",'Hoạt động vui chơi':"",'Mã AC1':"",
                                                                    'Hoạt động du lịch':"",'Mã AC2':"",'Hoạt động mang tính lịch sử':"",
                                                                    'Mã AC3':"",'Hoạt động tín ngưỡng':"",'Mã AC4':"",
                                                                    'Hoạt động văn hóa dân gian':"","Mã AC5":"",'Mục đích quảng bá':"",'Mã CO1':"",
                                                                    'Mục đích tâm linh':"",'Mã CO2':"",'Mục đích tưởng nhớ':"","Mã CO3":"",
                                                                    'Dân tộc':"",'Mã ETH':"",'Tôn giáo':"",'Mã REL':"",'Nhân vật':"",'Mã PER':"",
                                                                    'Danh lam':"",'Mã FAM':"",'Đặc điểm danh lam':"",'Danh hiệu':"",
                                                                    'Mã REC':""})
        for i in x.get('FFT',[]):
            writer.writerow({'Mã lễ hội':"F"+setIdForStr(data,'FES',fes),'Tên lễ hội':fes,'Địa điểm':"",
                                                                    'Mã LOC':"",'Thời gian':"",'Tên gọi khác':"",
                                                                    'Lịch sử hình thành':i,'Hoạt động vui chơi':"",'Mã AC1':"",
                                                                    'Hoạt động du lịch':"",'Mã AC2':"",'Hoạt động mang tính lịch sử':"",
                                                                    'Mã AC3':"",'Hoạt động tín ngưỡng':"",'Mã AC4':"",
                                                                    'Hoạt động văn hóa dân gian':"","Mã AC5":"",'Mục đích quảng bá':"",'Mã CO1':"",
                                                                    'Mục đích tâm linh':"",'Mã CO2':"",'Mục đích tưởng nhớ':"","Mã CO3":"",
                                                                    'Dân tộc':"",'Mã ETH':"",'Tôn giáo':"",'Mã REL':"",'Nhân vật':"",'Mã PER':"",
                                                                    'Danh lam':"",'Mã FAM':"",'Đặc điểm danh lam':"",'Danh hiệu':"",
                                                                    'Mã REC':""})
        for i in x.get('AC1',[]):
            writer.writerow({'Mã lễ hội':"F"+setIdForStr(data,'FES',fes),'Tên lễ hội':fes,'Địa điểm':"",
                                                                    'Mã LOC':"",'Thời gian':"",'Tên gọi khác':"",
                                                                    'Lịch sử hình thành':"",'Hoạt động vui chơi':i,'Mã AC1':'AA'+setIdForList(data,'AC1',i),
                                                                    'Hoạt động du lịch':"",'Mã AC2':"",'Hoạt động mang tính lịch sử':"",
                                                                    'Mã AC3':"",'Hoạt động tín ngưỡng':"",'Mã AC4':"",
                                                                    'Hoạt động văn hóa dân gian':"","Mã AC5":"",'Mục đích quảng bá':"",'Mã CO1':"",
                                                                    'Mục đích tâm linh':"",'Mã CO2':"",'Mục đích tưởng nhớ':"","Mã CO3":"",
                                                                    'Dân tộc':"",'Mã ETH':"",'Tôn giáo':"",'Mã REL':"",'Nhân vật':"",'Mã PER':"",
                                                                    'Danh lam':"",'Mã FAM':"",'Đặc điểm danh lam':"",'Danh hiệu':"",
                                                                    'Mã REC':""})
                                    
        for i in x.get('AC2',[]):
            writer.writerow({'Mã lễ hội':"F"+setIdForStr(data,'FES',fes),'Tên lễ hội':fes,'Địa điểm':"",
                                                                    'Mã LOC':"",'Thời gian':"",'Tên gọi khác':"",
                                                                    'Lịch sử hình thành':"",'Hoạt động vui chơi':"",'Mã AC1':"",
                                                                    'Hoạt động du lịch':i,'Mã AC2':'AB'+setIdForList(data,'AC2',i),'Hoạt động mang tính lịch sử':"",
                                                                    'Mã AC3':"",'Hoạt động tín ngưỡng':"",'Mã AC4':"",
                                                                    'Hoạt động văn hóa dân gian':"","Mã AC5":"",'Mục đích quảng bá':"",'Mã CO1':"",
                                                                    'Mục đích tâm linh':"",'Mã CO2':"",'Mục đích tưởng nhớ':"","Mã CO3":"",
                                                                    'Dân tộc':"",'Mã ETH':"",'Tôn giáo':"",'Mã REL':"",'Nhân vật':"",'Mã PER':"",
                                                                    'Danh lam':"",'Mã FAM':"",'Đặc điểm danh lam':"",'Danh hiệu':"",
                                                                    'Mã REC':""})
        for i in x.get('AC3',[]):
            writer.writerow({'Mã lễ hội':"F"+setIdForStr(data,'FES',fes),'Tên lễ hội':fes,'Địa điểm':"",
                                                                    'Mã LOC':"",'Thời gian':"",'Tên gọi khác':"",
                                                                    'Lịch sử hình thành':"",'Hoạt động vui chơi':"",'Mã AC1':"",
                                                                    'Hoạt động du lịch':"",'Mã AC2':"",'Hoạt động mang tính lịch sử':i,
                                                                    'Mã AC3':'AC'+setIdForList(data,'AC3',i),'Hoạt động tín ngưỡng':"",'Mã AC4':"",
                                                                    'Hoạt động văn hóa dân gian':"","Mã AC5":"",'Mục đích quảng bá':"",'Mã CO1':"",
                                                                    'Mục đích tâm linh':"",'Mã CO2':"",'Mục đích tưởng nhớ':"","Mã CO3":"",
                                                                    'Dân tộc':"",'Mã ETH':"",'Tôn giáo':"",'Mã REL':"",'Nhân vật':"",'Mã PER':"",
                                                                    'Danh lam':"",'Mã FAM':"",'Đặc điểm danh lam':"",'Danh hiệu':"",
                                                                    'Mã REC':""})
        for i in x.get('AC4',[]):
            writer.writerow({'Mã lễ hội':"F"+setIdForStr(data,'FES',fes),'Tên lễ hội':fes,'Địa điểm':"",
                                                                    'Mã LOC':"",'Thời gian':"",'Tên gọi khác':"",
                                                                    'Lịch sử hình thành':"",'Hoạt động vui chơi':"",'Mã AC1':"",
                                                                    'Hoạt động du lịch':"",'Mã AC2':"",'Hoạt động mang tính lịch sử':"",
                                                                    'Mã AC3':"",'Hoạt động tín ngưỡng':i,'Mã AC4':'AD'+setIdForList(data,'AC4',i),
                                                                    'Hoạt động văn hóa dân gian':"","Mã AC5":"",'Mục đích quảng bá':"",'Mã CO1':"",
                                                                    'Mục đích tâm linh':"",'Mã CO2':"",'Mục đích tưởng nhớ':"","Mã CO3":"",
                                                                    'Dân tộc':"",'Mã ETH':"",'Tôn giáo':"",'Mã REL':"",'Nhân vật':"",'Mã PER':"",
                                                                    'Danh lam':"",'Mã FAM':"",'Đặc điểm danh lam':"",'Danh hiệu':"",
                                                                    'Mã REC':""})
        for i in x.get('AC5',[]):
            writer.writerow({'Mã lễ hội':"F"+setIdForStr(data,'FES',fes),'Tên lễ hội':fes,'Địa điểm':"",
                                                                    'Mã LOC':"",'Thời gian':"",'Tên gọi khác':"",
                                                                    'Lịch sử hình thành':"",'Hoạt động vui chơi':"",'Mã AC1':"",
                                                                    'Hoạt động du lịch':"",'Mã AC2':"",'Hoạt động mang tính lịch sử':"",
                                                                    'Mã AC3':"",'Hoạt động tín ngưỡng':"",'Mã AC4':"",
                                                                    'Hoạt động văn hóa dân gian':i,"Mã AC5":'AE'+setIdForList(data,'AC5',i),'Mục đích quảng bá':"",'Mã CO1':"",
                                                                    'Mục đích tâm linh':"",'Mã CO2':"",'Mục đích tưởng nhớ':"","Mã CO3":"",
                                                                    'Dân tộc':"",'Mã ETH':"",'Tôn giáo':"",'Mã REL':"",'Nhân vật':"",'Mã PER':"",
                                                                    'Danh lam':"",'Mã FAM':"",'Đặc điểm danh lam':"",'Danh hiệu':"",
                                                                    'Mã REC':""})
        for i in x.get('CO1',[]):
            writer.writerow({'Mã lễ hội':"F"+setIdForStr(data,'FES',fes),'Tên lễ hội':fes,'Địa điểm':"",
                                                                    'Mã LOC':"",'Thời gian':"",'Tên gọi khác':"",
                                                                    'Lịch sử hình thành':"",'Hoạt động vui chơi':"",'Mã AC1':"",
                                                                    'Hoạt động du lịch':"",'Mã AC2':"",'Hoạt động mang tính lịch sử':"",
                                                                    'Mã AC3':"",'Hoạt động tín ngưỡng':"",'Mã AC4':"",
                                                                    'Hoạt động văn hóa dân gian':"","Mã AC5":"",'Mục đích quảng bá':i,
                                                                    'Mã CO1':'CA'+setIdForList(data,'CO1',i),
                                                                    'Mục đích tâm linh':"",'Mã CO2':"",'Mục đích tưởng nhớ':"","Mã CO3":"",
                                                                    'Dân tộc':"",'Mã ETH':"",'Tôn giáo':"",'Mã REL':"",'Nhân vật':"",'Mã PER':"",
                                                                    'Danh lam':"",'Mã FAM':"",'Đặc điểm danh lam':"",'Danh hiệu':"",
                                                                    'Mã REC':""})
        for i in x.get('CO2',[]):
            writer.writerow({'Mã lễ hội':"F"+setIdForStr(data,'FES',fes),'Tên lễ hội':fes,'Địa điểm':"",
                                                                    'Mã LOC':"",'Thời gian':"",'Tên gọi khác':"",
                                                                    'Lịch sử hình thành':"",'Hoạt động vui chơi':"",'Mã AC1':"",
                                                                    'Hoạt động du lịch':"",'Mã AC2':"",'Hoạt động mang tính lịch sử':"",
                                                                    'Mã AC3':"",'Hoạt động tín ngưỡng':"",'Mã AC4':"",
                                                                    'Hoạt động văn hóa dân gian':"","Mã AC5":"",'Mục đích quảng bá':"",'Mã CO1':"",
                                                                    'Mục đích tâm linh':i,'Mã CO2':'CB'+setIdForList(data,'CO2',i),'Mục đích tưởng nhớ':"","Mã CO3":"",
                                                                    'Dân tộc':"",'Mã ETH':"",'Tôn giáo':"",'Mã REL':"",'Nhân vật':"",'Mã PER':"",
                                                                    'Danh lam':"",'Mã FAM':"",'Đặc điểm danh lam':"",'Danh hiệu':"",
                                                                    'Mã REC':""})
        for i in x.get('CO3',[]):
            writer.writerow({'Mã lễ hội':"F"+setIdForStr(data,'FES',fes),'Tên lễ hội':fes,'Địa điểm':"",
                                                                    'Mã LOC':"",'Thời gian':"",'Tên gọi khác':"",
                                                                    'Lịch sử hình thành':"",'Hoạt động vui chơi':"",'Mã AC1':"",
                                                                    'Hoạt động du lịch':"",'Mã AC2':"",'Hoạt động mang tính lịch sử':"",
                                                                    'Mã AC3':"",'Hoạt động tín ngưỡng':"",'Mã AC4':"",
                                                                    'Hoạt động văn hóa dân gian':"","Mã AC5":"",'Mục đích quảng bá':"",'Mã CO1':"",
                                                                    'Mục đích tâm linh':"",'Mã CO2':"",'Mục đích tưởng nhớ':i,"Mã CO3":'AC'+setIdForList(data,'CO3',i),
                                                                    'Dân tộc':"",'Mã ETH':"",'Tôn giáo':"",'Mã REL':"",'Nhân vật':"",'Mã PER':"",
                                                                    'Danh lam':"",'Mã FAM':"",'Đặc điểm danh lam':"",'Danh hiệu':"",
                                                                    'Mã REC':""})
        for i in x.get('ETH',[]):
            writer.writerow({'Mã lễ hội':"F"+setIdForStr(data,'FES',fes),'Tên lễ hội':fes,'Địa điểm':"",
                                                                    'Mã LOC':"",'Thời gian':"",'Tên gọi khác':"",
                                                                    'Lịch sử hình thành':"",'Hoạt động vui chơi':"",'Mã AC1':"",
                                                                    'Hoạt động du lịch':"",'Mã AC2':"",'Hoạt động mang tính lịch sử':"",
                                                                    'Mã AC3':"",'Hoạt động tín ngưỡng':"",'Mã AC4':"",
                                                                    'Hoạt động văn hóa dân gian':"","Mã AC5":"",'Mục đích quảng bá':"",'Mã CO1':"",
                                                                    'Mục đích tâm linh':"",'Mã CO2':"",'Mục đích tưởng nhớ':"","Mã CO3":"",
                                                                    'Dân tộc':i,'Mã ETH':'E'+setIdForList(data,'ETH',i),'Tôn giáo':"",'Mã REL':"",'Nhân vật':"",'Mã PER':"",
                                                                    'Danh lam':"",'Mã FAM':"",'Đặc điểm danh lam':"",'Danh hiệu':"",
                                                                    'Mã REC':""})
        for i in x.get('REL',[]):
            writer.writerow({'Mã lễ hội':"F"+setIdForStr(data,'FES',fes),'Tên lễ hội':fes,'Địa điểm':"",
                                                                  'Mã LOC':"",'Thời gian':"",'Tên gọi khác':"",
                                                                  'Lịch sử hình thành':"",'Hoạt động vui chơi':"",'Mã AC1':"",
                                                                  'Hoạt động du lịch':"",'Mã AC2':"",'Hoạt động mang tính lịch sử':"",
                                                                  'Mã AC3':"",'Hoạt động tín ngưỡng':"",'Mã AC4':"",
                                                                  'Hoạt động văn hóa dân gian':"","Mã AC5":"",'Mục đích quảng bá':"",'Mã CO1':"",
                                                                  'Mục đích tâm linh':"",'Mã CO2':"",'Mục đích tưởng nhớ':"","Mã CO3":"",
                                                                  'Dân tộc':"",'Mã ETH':"",'Tôn giáo':i,'Mã REL':'R'+setIdForList(data,'REL',i),'Nhân vật':"",'Mã PER':"",
                                                                  'Danh lam':"",'Mã FAM':"",'Đặc điểm danh lam':"",'Danh hiệu':"",
                                                                  'Mã REC':""})
        for i in x.get('PER',[]):
            writer.writerow({'Mã lễ hội':"F"+setIdForStr(data,'FES',fes),'Tên lễ hội':fes,'Địa điểm':"",
                                                                  'Mã LOC':"",'Thời gian':"",'Tên gọi khác':"",
                                                                  'Lịch sử hình thành':"",'Hoạt động vui chơi':"",'Mã AC1':"",
                                                                  'Hoạt động du lịch':"",'Mã AC2':"",'Hoạt động mang tính lịch sử':"",
                                                                  'Mã AC3':"",'Hoạt động tín ngưỡng':"",'Mã AC4':"",
                                                                  'Hoạt động văn hóa dân gian':"","Mã AC5":"",'Mục đích quảng bá':"",'Mã CO1':"",
                                                                  'Mục đích tâm linh':"",'Mã CO2':"",'Mục đích tưởng nhớ':"","Mã CO3":"",
                                                                  'Dân tộc':"",'Mã ETH':"",'Tôn giáo':"",'Mã REL':"",'Nhân vật':i,'Mã PER':'P'+setIdForList(data,'PER',i),
                                                                  'Danh lam':"",'Mã FAM':"",'Đặc điểm danh lam':"",'Danh hiệu':"",
                                                                  'Mã REC':""})
                                    
        for i in x.get('FAM',[]):
            for j in x.get('CER',[]):
                    writer.writerow({'Mã lễ hội':"F"+setIdForStr(data,'FES',fes),'Tên lễ hội':fes,'Địa điểm':"",
                                            'Mã LOC':"",'Thời gian':"",'Tên gọi khác':"",
                                            'Lịch sử hình thành':"",'Hoạt động vui chơi':"",'Mã AC1':"",
                                            'Hoạt động du lịch':"",'Mã AC2':"",'Hoạt động mang tính lịch sử':"",
                                            'Mã AC3':"",'Hoạt động tín ngưỡng':"",'Mã AC4':"",
                                            'Hoạt động văn hóa dân gian':"","Mã AC5":"",'Mục đích quảng bá':"",'Mã CO1':"",
                                            'Mục đích tâm linh':"",'Mã CO2':"",'Mục đích tưởng nhớ':"","Mã CO3":"",
                                            'Dân tộc':"",'Mã ETH':"",'Tôn giáo':"",'Mã REL':"",'Nhân vật':"",'Mã PER':"",
                                            'Danh lam':i,'Mã FAM':'FA'+setIdForList(data,'FAM',i),'Đặc điểm danh lam':j,'Danh hiệu':"",
                                            'Mã REC':""})
        for i in x.get('REC',[]):
            writer.writerow({'Mã lễ hội':"F"+setIdForStr(data,'FES',fes),'Tên lễ hội':fes,'Địa điểm':"",
                                                    'Mã LOC':"",'Thời gian':"",'Tên gọi khác':"",
                                                    'Lịch sử hình thành':"",'Hoạt động vui chơi':"",'Mã AC1':"",
                                                    'Hoạt động du lịch':"",'Mã AC2':"",'Hoạt động mang tính lịch sử':"",
                                                    'Mã AC3':"",'Hoạt động tín ngưỡng':"",'Mã AC4':"",
                                                    'Hoạt động văn hóa dân gian':"","Mã AC5":"",'Mục đích quảng bá':"",'Mã CO1':"",
                                                    'Mục đích tâm linh':"",'Mã CO2':"",'Mục đích tưởng nhớ':"","Mã CO3":"",
                                                    'Dân tộc':"",'Mã ETH':"",'Tôn giáo':"",'Mã REL':"",'Nhân vật':"",'Mã PER':"",
                                                    'Danh lam':"",'Mã FAM':"",'Đặc điểm danh lam':"",'Danh hiệu':i,
                                                    'Mã REC':'RE'+setIdForList(data,'REC',i)})
                                    
