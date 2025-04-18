#importa 
import numpy as np
import matplotlib.pyplot as plt
import json
import requests
import pandas as pd
#mappa en karta med latitude och longitude
np.random.seed(314271)
if False:
    size=10000
    longitudes=-np.random.uniform(-180,180,size)
    latitudes=180/np.pi*np.arcsin(np.random.uniform(0,1,size))*np.sign(np.random.uniform(-1,1,size))

#print to se ok
if False:
    plt.scatter(longitudes*np.cos(latitudes*np.pi/180),latitudes,alpha=0.2)
    l1=np.linspace(-90,90,1000)
    plt.plot(180*np.cos(l1/180*np.pi),l1)
    plt.plot(-180*np.cos(l1/180*np.pi),l1)
    plt.show()
#done

#funk to savetojsonfile
def dumpa(name="cords.json",result=None):
    with open(name, 'w') as f:
            json.dump(result,f)
def loada(name="cords"):
    with open(name,"r") as f:
        return json.load(f)
    
#save to jsonfiles
if False:
    dictionary={"longitudes":list(longitudes),"latitudes":list(latitudes)}
    dumpa(name="cords.json",result=dictionary)
#done

#new funktion
def checkwater(lat,lon):
    return requests.get("https://is-on-water.balbona.me/api/v1/get/"+str(lat)+"/"+str(lon)).json()
def createrandomcordinates(lats,lons,startindex=0,listan=[],feature=[]):
    for i in range(startindex,len(lats)):
        response=checkwater(lats[i],lons[i])
        print(response)
        if response["isWater"]:
            listan.append(0)
        else:
            listan.append(1)
        feature.append("feature")
        if i%100==0:
            print(i/(len(lats)-startindex),i)
            dumpa("cordscopy1.json",{"longitudes":list(lons),"latitudes":list(lats),"isLand":listan,"feature":feature})
if False:
    dicta=loada("cords.json")
    print(len(dicta["longitudes"]))
    dicta1=loada("cordscopy.json")
    createrandomcordinates(dicta["latitudes"],dicta["longitudes"],0,[],[])#dicta1["isLand"],feature[])

#plota världskarta
if False:
    dicta=loada("cordscopy1.json")
    y1,x1,y2,x2=[],[],[],[]
    for i,v in enumerate(dicta["isLand"]):
        if v or dicta["feature"]=="LAKE" or dicta["feature"]=="RIVER":
            y1.append(dicta["latitudes"][i])
            x1.append(dicta["longitudes"][i])
        else:
            y2.append(dicta["latitudes"][i])
            x2.append(dicta["longitudes"][i])
    del dicta

    x1,x2,y1,y2=np.array(x1),np.array(x2),np.array(y1),np.array(y2)
    casen=2
    match casen:
        case 1:
            x1=x1*np.cos(y1*np.pi/180)
            x2=x2*np.cos(y2*np.pi/180)
        case 2:
            y1=90*np.sin(y1*np.pi/180)
            y2=90*np.sin(y2*np.pi/180)

    plt.scatter(x2,y2,color="blue",linewidths=10,alpha=1)
    plt.scatter(x1,y1,color="g",linewidths=10,alpha=1)
    plt.scatter(x2,y2,color="blue",linewidths=5,alpha=1)
    plt.scatter(x1,y1,color="g",linewidths=5,alpha=1)
    plt.scatter(x2,y2,color="blue",linewidths=3,alpha=1)
    plt.scatter(x1,y1,color="g",linewidths=3,alpha=1)
    plt.scatter(x2,y2,color="blue",linewidths=1,alpha=1)
    plt.scatter(x1,y1,color="g",linewidths=1,alpha=1)
    plt.xlim(-180,180)
    plt.ylim(-90,90)
    plt.show()
#finish

#read data from gbg from 1940-01-01-00:00 to 2025-01-01-23:00
def exceltojson(place="Gothenburg",fileold="historicweatherdata",filenew="historicweatherdata"):
    file=pd.read_excel("excels//"+fileold+".xlsx",sheet_name=place,index_col=None,header=None)
    #print(file[1][3:])
    latitude, longitude, elevation=file[0][1],file[1][1],file[2][1]
    time=list([str(i) for i in file[0][4:]])
    Ta=list(file[1][4:])
    Ws=list(file[2][4:])
    RH=list(file[3][4:])
    print("working")
    #print(file)
    del file #to reduce size
    data={place:{"latitude":latitude, "longitude":longitude, "elevation":elevation,"hourly":{"time":time,"Ta":Ta,"Ws":Ws,"RH":RH}}}
    del time #to reduce size
    del Ta #to reduce size
    del RH #to reduce size
    del Ws #to reduce size
    dumpa("jsons//"+filenew+".json",data)
#call the function
if False: exceltojson();

#addpetToweatherdata
def exceltojsonEmpty(place="Gothenburg",fileold="historicweatherdata",filenew="ourhistoricweatherdata"):
    data=loada("jsons//"+fileold+".json")
    lenofdata=len(data[place]["hourly"]["time"])
    del data
    dumpa("jsons//"+filenew+".json",{place:{"Tmrt_F":[-275]*lenofdata,"Tmrt_N":[-275]*lenofdata,"Tmrt_B":[-275]*lenofdata,"PET_F":[-275]*lenofdata,"PET_N":[-275]*lenofdata,"PET_B":[-275]*lenofdata}})
#createaempty
if False:exceltojsonEmpty();

#fix Times:
import datetime
def covert(strtime="1940-01-01 00:00:00"):
    return datetime.datetime.strptime(strtime,"%Y-%m-%d %H:%M:%S")
def strtotimes(times_str=[],lower_bound=0,upperbound=1000000):
    return [datetime.datetime.strptime(strtime,"%Y-%m-%d %H:%M:%S") for strtime in times_str[lower_bound,max(lower_bound,min(upperbound,len(times_str)))]]

#DONE date to index (~30 min)
def loppa(startstr="2023-12-31 00:00:00",endstr="2025-01-01 23:00:00",places=["Gothenburg"],fileold="historicweatherdata",funks=[],zerostr="1940-01-01 00:00:00"):
    starttime=datetime.datetime.strptime(startstr)
    endtime=datetime.datetime.strptime(endstr)
    zerotime=datetime.datetime.strptime(zerostr)
    timedif=(endtime.hour-starttime.hour)+1
    index0=(starttime.hour-zerotime.hour)
#DONE loppa för värden (~1 h)
    for place in places:
        data=loada("jsons//"+fileold+".json")[place]
        data["Ta"],data["RH"],data["Ws"],data["time"]=data["hourly"]["Ta"][index0:index0+timedif],data["hourly"]["RHs"][index0:index0+timedif],data["hourly"]["Wss"][index0:index0+timedif],data["hourly"]["time"][index0:index0+timedif]
        data["horly"]=None
        #data={place:{"latitude":file["latitude"], "longitude":file["longitude"], "elevation":file["elevation"],"time":time,"Ta":data["hourly"]["Tas"][index0:index0+timedif],"RH":data["hourly"]["RHs"][index0:index0+timedif],"Ws":data["hourly"]["Wss"][index0:index0+timedif]}}
        for f in funks:
            f(data)
#TODO loppa dem (~15 min)

#TODO importa alla Tmrt och Pet som är relevanta (~1-3 h)
#TODO runna allting (~1-3 h)
#TODO plotta sedan dem enlig saker (~1.5 h)
#TODO skriv allt i gruppchatten (~5 min)
#Allt som allt  (~5-9 h (5 kod, 2 väntande, 2 extra logg))
