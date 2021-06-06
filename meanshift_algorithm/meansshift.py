

import matplotlib.pyplot as plt
import numpy as np
from sklearn.datasets.samples_generator import make_blobs#veri üretimi için importladık

x,y=make_blobs(n_samples=40,centers=3,n_features=2)

renkler=10*["g","r","c","b","k"]

class meanshift:
    def __init__(self,yaricap=None,yaricap_norm_adımı=30):
        self.yaricap_norm_adımı=yaricap_norm_adımı
        self.yaricap=yaricap
    
    
    def fit(self,data):#yarıcapi belirledik
       
        if self.yaricap==None:
           ortak_merkez=np.average(data,axis=0)
           
           ortak_norm=np.linalg.norm(ortak_merkez)
          # print("Ortak Merkez Ortak Norm: " ,ortak_merkez,ortak_norm)
           self.yaricap=ortak_norm/self.yaricap_norm_adımı
         #  print("yarıcap:",self.yaricap)
           
        merkezler={}
        for i in range(len(data)):
            merkezler[i]=data[i]#noktaları merkezler dict yapsı iöine aldık
        #print("Merkezler değişkenine alınan datalar: ", merkezler)
        
        while True:
            yeni_merkezler=[]
        
            for i in merkezler:
                
                in_yaricap=[]#yarıçapın içinde mi
                merkez=merkezler[i]
                
                
                agirliklar=[i for i in range(self.yaricap_norm_adımı)][::-1]#yarıçap normadımı indeksleini aldık 0-30aras9
                #count=0
                for futureset in data:
                    #count+=1
                    mesafe=np.linalg.norm(futureset-merkez)
                    #print("mesafe",mesafe)
                    if mesafe==0:
                        mesafe=0.0000001
                    agirlik_index=int(mesafe/self.yaricap)
                    
                    if agirlik_index>=self.yaricap_norm_adımı:
                        agirlik_index=self.yaricap_norm_adımı-1
                        
                    
                    ekle=(agirliklar[agirlik_index]**2)*[futureset]
                    
                    
                    in_yaricap+=ekle
                
                #print("count",count)
                       
                yeni_merkez=np.average(in_yaricap,axis=0)#yeni merkezin kütle merkezini hesapladık
                print("yeni merkez",yeni_merkez)
                #print(yeni_merkez)
                yeni_merkezler.append(tuple(yeni_merkez))
#                print("yeni merkezler",yeni_merkezler)
            #print("in yarıcap kac tane",len(in_yaricap))
            uniques=sorted(list(set(yeni_merkezler)))
            
            
            
            sil=[]
            for i in uniques:# FAZLADAN GELEN MERKEZLERİ SİLİYORUZ
                for j in uniques:
                    if i==j:
                        pass
                    elif np.linalg.norm(np.array(i)-np.array(j))<=self.yaricap:
                        sil.append(j)
                        break
            for i in sil:
                try: 
                    uniques.remove(i)
                except:
                    pass
                    
            
            onceki_merkezler=dict(merkezler)
            #print("kaç tane: ",len(onceki_merkezler))
#            print("önce ki merkezler",onceki_merkezler)
#            print("uniques",uniques)
            merkezler={}
            
            for i in range(len(uniques)):
                merkezler[i]=np.array(uniques[i])
            optimize=True
            #print(merkezler)
            
            for i in merkezler:
                
                if not np.array_equal(merkezler[i],onceki_merkezler[i]):#önce ki merkezler ile yeni merkezleer aynı mı diye kıyasladık değilse for while dçngüsünden çıkmasını engelledik 
                    optimize=False    
            
                if not optimize:
                    break
            
            if  optimize:
                break  
       
        self.merkezler=merkezler
        
        self.sınıflandırma={}
        
        for i in range(len(self.merkezler)):
            self.sınıflandırma[i]=[]
        for futureset in data:
            mesafe=[np.linalg.norm(futureset-self.merkezler[merkez]) for merkez in self.merkezler]
            sınıflandırma=mesafe.index(min(mesafe))
            self.sınıflandırma[sınıflandırma].append(futureset) 
            self.futureset=futureset            
                                
        

    
ms=meanshift()
ms.fit(x)
merkezler=ms.merkezler

for i in ms.sınıflandırma:
    renk=renkler[i]
    for j in ms.sınıflandırma[i]:
        plt.scatter(j[0], j[1], marker='x',color=renk,s=150)
for i in merkezler:
    plt.scatter(merkezler[i][0],merkezler[i][1],color='k',marker='*',s=150)
plt.show()

