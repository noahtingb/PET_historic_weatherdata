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
import pickle
def dumpa(name="cords.json",result=None):
    with open(name, 'w') as f:
            json.dump(result,f)
def loada(name="cords"):
    with open(name,"r") as f:
        return json.load(f)
def dumpa1(name="datapkl",result=None):
    with open(name+".pkl", 'wb') as f:
            pickle.dump(result,f)
def loada1(name="datapkl"):
    with open(name+".pkl","rb") as f:
        return pickle.load(f,encoding="UTC-8")    
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
def plotavarldskarta():
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
    casen=1
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
    if casen==1:
        l1=np.linspace(-90,90,1000)
        plt.plot(180*np.cos(l1/180*np.pi),l1)
        plt.plot(-180*np.cos(l1/180*np.pi),l1)
    plt.show()
if False: plotavarldskarta();
#finish

#read data from gbg from 1940-01-01-00:00 to 2025-01-01-23:00
def exceltojson(place="Gothenburg",fileold="historicweatherdata",filenew="historicweatherdata"):
    file=pd.read_excel("excels//"+fileold+".xlsx",sheet_name=place,index_col=None,header=None)
    #print(file[1][3:])
    latitude, longitude, altitude=file[0][1],file[1][1],file[2][1]
    time=list([str(i) for i in file[0][4:]])
    Ta=list(file[1][4:])
    Ws=list(file[3][4:])
    RH=list(file[2][4:])
    print("working")
    #print(file)
    del file #to reduce size
    data={place:{"latitude":latitude, "longitude":longitude, "altitude":altitude,"hourly":{"time":time,"Ta":Ta,"Ws":Ws,"RH":RH}}}
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

#DONE funtions for BIOMETEO (~30 min) (faktiskt 13 min)
import biometeo
def getTmrtBioMeteo(params,indexforparams):
        time=covert(params["time"][indexforparams])
        if (time.year % 4) == 0 and ( ((time.year % 100)==0 and (time.year % 400) == 0) or ((time.year % 100)!=0)):
            dayspermonth = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        else:
            dayspermonth = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        doy= sum(dayspermonth[0:time.month - 1]) + time.day
        hod=(time.hour+1/2)%24
        Tmrt=biometeo.Tmrt_calc(Ta=params["Ta"][indexforparams], RH=params["RH"][indexforparams], v=params["Ws"][indexforparams], longitude=params["longitude"], latitude=params["latitude"], sea_level_height=params["altitude"],day_of_year=doy, hour_of_day=hod,timezone_offset=params["longitude"]/15,alb=0.15, albhum=0.2)
        #params={"year":year,"month":month,"day":day,"hour":hour,"Ta":Ta,"SwR":0.,"RH":RH,"Ws":Ws,"sky":"Clear (100%)","radI":0., "radD":0., "loc":location,"UTC":0}
        return float(Tmrt["Tmrt"])
def getPETBioMeteo(Tmrt,params,indexforparams,funktion=biometeo.PET,pettype="PET_v"):
        if type(Tmrt)==type([]):
            Tmrt=Tmrt[indexforparams]
        VP=float(biometeo.VP_RH_exchange(Ta=params["Ta"][indexforparams],RH=params["RH"][indexforparams])["VP"])
        resultPET2=funktion(Ta=params["Ta"][indexforparams],VP=VP,v=(1.1 / 10) ** 0.2 * params["Ws"][indexforparams],Tmrt=Tmrt)[pettype]
        return float(resultPET2)

#TODO fixa noahtingb:s kod (~45 min) (faktiskt 27 min)
import noahtingb_kod.petprocessing as noahtingb
def getTmrtNoah(params,indexforparams):
        time=covert(params["time"][indexforparams])#+datetime.timedelta(hours=params["longitude"]/15)
        form={"Ta":params["Ta"][indexforparams],"RH":params["RH"][indexforparams],"year":time.year,
              "month":time.month,"day":time.day,"hour":time.hour,
              "loc":{"longitude":params["longitude"], "latitude":params["latitude"], "altitude":params["altitude"]}}
        Tmrt=noahtingb.indexflaskaTmrt(form)
        return float(Tmrt)
def getPETNoah(Tmrt,params,indexforparams):
        if type(Tmrt)==type([]):
            Tmrt=Tmrt[indexforparams]
        form={"Ta":params["Ta"][indexforparams],"RH":params["RH"][indexforparams],"Ws":params["Ws"][indexforparams],"Tmrt":Tmrt}
        resultPET2=noahtingb.indexflaskPET(form)
        return float(resultPET2)
import antonpanton37_kod.processing as apro
def getTmrtPETanton(params,indexforparams):
        form={"Ta":params["Ta"][indexforparams],"RH":params["RH"][indexforparams],"Ws":params["Ws"][indexforparams],"time":params["time"][indexforparams],
              "longitude":params["longitude"], "latitude":params["latitude"], "altitude":params["altitude"]}
        Tmrt,PET=apro.getTmrtPET(form)
        return float(Tmrt),float(PET)


#DONE fixa fredrik:s kod ren (~1 h 15 min) (faktiskt 16 min)
import biglimp.flask_app as fkoof
def getTmrtPETFredrik(params,indexforparams):
        timesjustering=covert(params["time"][indexforparams])+datetime.timedelta(hours=1)
        form={"Ta":params["Ta"][indexforparams],"RH":params["RH"][indexforparams],"Ws":params["Ws"][indexforparams],"year":timesjustering.year,
              "month":timesjustering.month,"day":timesjustering.day,"hour":timesjustering.hour,
              "longitude":params["longitude"], "latitude":params["latitude"], "altitude":params["altitude"]}
        Tmrt,PET=fkoof.index(form)
        return float(Tmrt),float(PET)


def procentdone(index,total,before=""):
    if ((index-1)*100)//total != ((index)*100)//total:
        print(before+f"{(index*100)//total}%")
#DONE date to index (~30 min)
import time
def loppa(startstr="2023-12-31 00:00:00",endstr="2025-01-01 23:00:00",places=["Gothenburg"],fileold="historicweatherdata",fileour="ourhistoricweatherdata",filenew="ourhistoricweatherdata1",funks=[],zerostr="1940-01-01 00:00:00"):
    starttime=covert(startstr)
    endtime=covert(endstr)
    zerotime=covert(zerostr)
    timedif=int((endtime-starttime).total_seconds()//3600+1)
    index0=int((starttime-zerotime).total_seconds()//3600)
#DONE loppa för värden (~1 h)
    for place in places:
        data=loada("jsons//"+fileold+".json")[place]

        data["Ta"],data["RH"],data["Ws"],data["time"]=data["hourly"]["Ta"][index0:index0+timedif],data["hourly"]["RH"][index0:index0+timedif],data["hourly"]["Ws"][index0:index0+timedif],data["hourly"]["time"][index0:index0+timedif]
        print(data["time"][0],data["time"][len(data["time"])-1])
        data["hourly"]=None
        print(data["time"][0],data["time"][len(data["time"])-1])
        #data={place:{"latitude":file["latitude"], "longitude":file["longitude"], "elevation":file["elevation"],"time":time,"Ta":data["hourly"]["Tas"][index0:index0+timedif],"RH":data["hourly"]["RHs"][index0:index0+timedif],"Ws":data["hourly"]["Wss"][index0:index0+timedif]}}
        if "Tmrt_B" in funks:
            dictofour=loada("jsons//"+fileour+".json")
            time1=time.time()
            for i in range(timedif):
                procentdone(i,timedif)                
                dictofour[place]["Tmrt_B"][index0+i]=getTmrtBioMeteo(data,i)
            print(f"Tmrt_B {time.time()-time1}")
            dumpa("jsons//"+filenew+".json",dictofour)
        if "PET_B" in funks:
            dictofour=loada("jsons//"+fileour+".json")
            time1=time.time()
            for i in range(timedif):
                procentdone(i,timedif)
                Tmrt=dictofour[place]["Tmrt_B"][index0+i]
                if Tmrt==-275:
                    Tmrt=getTmrtBioMeteo(data,i)
                dictofour[place]["PET_B"][index0+i]=getPETBioMeteo(Tmrt,data,i)
            print(f"PET_B {time.time()-time1}")
            dumpa("jsons//"+filenew+".json",dictofour)
        if "mPET_B" in funks:
            dictofour=loada("jsons//"+fileour+".json")
            time1=time.time()
            dictofour[place]["mPET_B"]=dictofour[place]["PET_B"].copy()
            for i in range(timedif):
                procentdone(i,timedif)
                Tmrt=dictofour[place]["Tmrt_B"][index0+i]
                if Tmrt==-275:
                    Tmrt=getTmrtBioMeteo(data,i)
                dictofour[place]["mPET_B"][index0+i]=getPETBioMeteo(Tmrt,data,i,funktion=biometeo.mPET,pettype="mPET")
            print(f"mPET_B {time.time()-time1}")
            dumpa("jsons//"+filenew+".json",dictofour)
        if "Tmrt_N" in funks:
            dictofour=loada("jsons//"+fileour+".json")
            time1=time.time()
            for i in range(timedif):
                procentdone(i,timedif)
                dictofour[place]["Tmrt_N"][index0+i]=getTmrtNoah(data,i)
            print(f"Tmrt_N {time.time()-time1}")
            dumpa("jsons//"+filenew+".json",dictofour)
        if "PET_N" in funks:
            dictofour=loada("jsons//"+fileour+".json")
            time1=time.time()
            for i in range(timedif):
                procentdone(i,timedif)
                Tmrt=dictofour[place]["Tmrt_N"][index0+i]
                if Tmrt==-275:
                    print(f"Error {i}")
                    Tmrt=getTmrtNoah(data,i)
                dictofour[place]["PET_N"][index0+i]=getPETNoah(Tmrt,data,i)
            print(f"Pet_N {time.time()-time1}")
            dumpa("jsons//"+filenew+".json",dictofour)
        if "TmrtPET_F" in funks:
            dictofour=loada("jsons//"+fileour+".json")
            time1=time.time()
            for i in range(timedif):
                procentdone(i,timedif)
                dictofour[place]["Tmrt_F"][index0+i],dictofour[place]["PET_F"][index0+i]=getTmrtPETFredrik(data,i)
            print(f"TmrtPET_F {time.time()-time1}")
            dumpa("jsons//"+filenew+".json",dictofour)
        if "TmrtPET_R" in funks:
            dictofour=loada("jsons//"+fileour+".json")
            time1=time.time()
            if dictofour[place].get("Tmrt_R")==None:
                dictofour[place]["Tmrt_R"]=[-275]*len(dictofour[place]["PET_B"])
                dictofour[place]["PET_R"]=[-275]*len(dictofour[place]["PET_B"])
            for i in range(timedif):
                procentdone(i,timedif)
                dictofour[place]["Tmrt_R"][index0+i],dictofour[place]["PET_R"][index0+i]=getTmrtPETanton(data,i)
            dumpa("jsons//"+filenew+".json",dictofour)
        print("Done mabye")
#? loppa dem (~15 min) (+felsökning ca 1-2 h)

if False: loppa(startstr="2023-12-31 00:00:00",endstr="2025-01-01 23:00:00",funks=["TmrtPET_F"],fileour="datareala",filenew="datareala")

#convert into right size data
def bigtosmall(startstr="2023-12-31 00:00:00",endstr="2025-01-01 23:00:00",places=["Gothenburg"],fileold="historicweatherdata",fileour="datareala",filenew="oursmall",zerostr="1940-01-01 00:00:00"):
    starttime=covert(startstr)
    endtime=covert(endstr)
    zerotime=covert(zerostr)
    timedif=int((endtime-starttime).total_seconds()//3600+1)
    index0=int((starttime-zerotime).total_seconds()//3600)
    for place in places:
        data=loada("jsons//"+fileold+".json")[place]
        data["Ta"],data["RH"],data["Ws"],data["time"]=data["hourly"]["Ta"][index0:index0+timedif],data["hourly"]["RH"][index0:index0+timedif],data["hourly"]["Ws"][index0:index0+timedif],data["hourly"]["time"][index0:index0+timedif]
        data.pop("hourly")
        dictofour=loada("jsons//"+fileour+".json")[place]
        for keys in ["Tmrt_N","Tmrt_B","Tmrt_F","mPET_B","PET_N","PET_F","PET_B","Tmrt_R","PET_R"]:
            data[keys]=dictofour[keys][index0:index0+timedif]
            dictofour.pop(keys)
        try:
            smalldata=loada("jsons//"+filenew+".json")     
        except:
            smalldata={}
        smalldata[place]=data
        dumpa("jsons//"+filenew+".json",smalldata)   
#to reduce the size of the files easy function
def avrundvalues(searchway=[["Gothenburg",["Tmrt_N","Tmrt_B","Tmrt_F","mPET_B","PET_N","PET_F","PET_B","Tmrt_R","PET_R"]]],oldfile="oursmall",newfile="oursmaller",decimals=2):
    data=loada("jsons//"+oldfile+".json") 
    for search in searchway:
        place=search[0]
        for key in search[1]:
            data[place][key]=[float(round(i, decimals)) for i in data[place][key]]
    dumpa("jsons//"+newfile+".json",data) 

#2024-01-23
#dumpa1("pkls//historicweatherdata",loada("jsons//historicweatherdata.json"))
#dumpa1("pkls//dataTP2000to2024a",loada("jsons//dataTmrtPETyear2000to2024sa.json"))
dagarb=["2024-02-23","2024-05-16","2024-07-28","2024-11-28"]
dagar=["2024-02-24","2024-05-17","2024-07-29","2024-11-29"]#["Feb 24 2024","Maj 17 2024","Juli 29 2024","November 29 2024"
#print(loada("jsons//dataTmrtPETyear2000to2024.json")["Gothenburg"]["Tmrt_N"][24*(365*60+15)-2:24*(365*60+15)+10])
#print(loada1("pkls//dataTP2000to2024")["Gothenburg"]["Tmrt_N"][24*(365*60+15)-2:24*(365*60+15)+10])

#indexpp=3
for indexpp in range(4):
    dgen=dagarb[indexpp]#"1999-12-31"#dagarb[indexpp]
    dagen=dagar[indexpp]#"2024-12-31"#dagar[indexpp]
    fname="dataTmrtPETana"#+"dataTmrtPETyear2000to2024"# dataTmrtPETBIG2
    fname1="dataTmrtPETyear2000to2024"#fname
    if False:#"Tmrt_B","PET_B","Tmrt_N","PET_N","TmrtPET_F","TmrtPET_R"
        if False: loppa(startstr=dgen+" 23:00:00",endstr=dagen+" 22:00:00",funks=["Tmrt_B","PET_B","TmrtPET_R"],fileour=fname,filenew=fname+"fel")
        if True: bigtosmall(startstr=dgen+" 23:00:00",endstr=dagen+" 22:00:00",fileour=fname1,filenew=fname+f"{indexpp}"+"sm");
        if True: avrundvalues(oldfile=fname+f"{indexpp}"+"sm",newfile=fname+f"{indexpp}"+"sa");
    #Tmrt_B:    26.452080249786377 (25 y)      [s]
    #PET_B:     12.86455512046814 (1 year) 103.19638323783875 (10 years) 46.53330063819885 (5 years) 49.02395462989807 (5 y) 40.123116970062256 (4 y)  [s]
    #Tmrt_N:    48.7991 (1 y)       [s] 
    #PET_N:     211.47069668769836 (25 y)  [s]
    #PETTmrt_F: 114.24778294563293 (1 y) 666.0236203670502 (6 y) 446.3225064277649 (4 y) 1049.415342092514 (5 y) 637.7019832134247 (4 y)   [s]
    #Tmrt_N:    48.7991 (1 y)    [s] 
#easy plot to two params
import matplotlib.pyplot as plt
def plota(x,y,title="",xlabel="",ylabel="",labels=[[""],[""]],karg={}):
    alpha=1 if (karg.get("alpha")==None) else karg["alpha"]
    linewidths=1 if (karg.get("linewidths")==None) else karg["linewidths"]
    if karg.get("color")==None: color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2','#7f7f7f', '#bcbd22', '#17becf']
    elif type(karg.get("color"))!=type([]):  color=[karg.get("color")]
    else: color=karg.get("color")
    viewlegend = True if (karg.get("viewlegend")!=None and karg.get("viewlegend")==True) else False
    scatta = True if (karg.get("scatta")!=None and karg.get("scatta")==True) else False

    #print(alpha,linewidths)
    plt.title(title)
    if type(x[0])==type([]):
        for i,v in enumerate(x):
            if scatta:
                plt.scatter(x=v,y=y[i],alpha=alpha,linewidths=0,s=linewidths,color=color[i%len(color)],label=f"x:{labels[0][i]} y:{labels[1][i]}")
            else:
                plt.plot(v,y[i],alpha=alpha,linewidth=linewidths,color=color[i%len(color)],label=f"x:{labels[0][i]} y:{labels[1][i]}")
    else:
        if scatta:
            plt.scatter(x=x,y=y,alpha=alpha,linewidths=0,s=linewidths,color=color[0],label=f"x:{labels[0][0]} y:{labels[1][0]}")
        else:
            plt.plot(x,y,alpha=alpha,linewidths=linewidths,color=color[0],label=f"x:{labels[0][0]} y:{labels[1][0]}")
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    if karg.get("linemaxminsomething")==True:
        colorline="#ff7f0e" if (karg.get("colorline")==None) else karg["colorline"]
        lista=[min(np.min(np.array(x)),np.min(np.array(y))),min(np.max(np.array(x)),np.max(np.array(y)))]
        plt.plot(lista,lista,linewidth=1,color=colorline,label="stright line")
    if viewlegend: plt.legend();

def whattoplot(x_keys=["time","time","time","time","time"],y_keys=["PET_B","mPET_B","PET_F","PET_N","Ta"],place="Gothenburg",oldfile="oursmaller",unitx="°C",unity="°C",karg={"alpha":1,"linewidths":2,"linemaxminsomething":False,"color":['#1f77b4', '#2ca02c','#d62728', '#9467bd','#8c564b'],"viewlegend":True,"scatta":False}):
    "Tmrt Biometeo","Tmrt Modifierad","Tmrt Solweig"
    """
    This function is used to plot all the data
    
    Created by:
    Noah Tingbratt 2025-04-20, noah.tingbratt@gmail.com,
    Chalmers Tekniska Högskola, Sweden,
    Bachelor Thesis
    
    Input parameters:
     - x_keys: List of what params to campare on the x axis.
     - location: List of what params to campare on the y axis. 
     - place: The place to plot default: "Gothenburg".
     - oldfile: The file with the data default: "oursmaller"
     - unitx: The unit of the x-axis default: "°C"
     - unity: The unit of the x-axis default: "°C"
     - karg: args for the plot as for example "alpha":alpha, "linewidths":width of the scatters, "linemaxminsomething":stright line to compare, "color": list of colors
    
    Output parameters: 
     - None:

    :param x_keys:
    :param location:
    :param place:
    :param oldfile:
    :param unitx:
    :param unity:
    :param karg:        
    :return:
    """
    data=loada("jsons//"+oldfile+".json") 
    #print(data)
    #print(data[place]["longitude"],data[place]["latitude"],data[place]["altitude"])
    #for i in range(24):
    #    print(f'{data[place]["time"][i]} \t mPet: {data[place]["mPET_B"][i]} \t PET: {data[place]["PET_B"][i]} \t PET_N: {data[place]["PET_N"][i]}')
    x=[0]*len(x_keys)
    for i,x_key in enumerate(x_keys):
        if x_key=="time":
            x[i]=[covert("1999-12-31 22:00:00")+datetime.timedelta(hours=i1) for i1 in range(len(data[place][y_keys[0]]))]
            plt.gcf().autofmt_xdate()
        else:
            x[i]=data[place][x_key]
    plota(x=x,y=[data[place][y_key] for y_key in y_keys],title="Title",xlabel=" ".join(x_keys)+f" [{unitx}]",ylabel=" ".join(y_keys)+f" [{unity}]",labels=[x_keys,y_keys],karg=karg)
    plt.show()
#x=np.array([i for i in range(25)])
#for p in [0.15,0.16,0.17,0.175,0.18,0.19,0.2]:
#    plt.plot(x,np.array([i*(1.1/10)**p for i in x]),alpha=0.5,label=f"{p}")
#plt.legend()
#plt.show()

#makeasmallchange



if False:
    if True: whattoplot(oldfile="dataTmrtPETyear2000to2024sa",x_keys=["time"]*5,y_keys=["PET_B","PET_F","PET_N","Ta","PET_R"]);
    if True: whattoplot(x_keys=["time"]*5,y_keys=["Tmrt_B","Tmrt_F","Tmrt_N","Ta","Tmrt_R"],oldfile="dataTmrtPETyear2000to2024sa");

#DONE importa alla Tmrt och Pet som är relevanta (~1-3 h)
#DONE fixa lopen
#DONE runna allting (~1-3 h) (small)

#DONE plotta sedan dem enlig saker (~1.5 h)
#Allt som allt  (~5-9 h (5 kod, 2 väntande, 2 extra logg))
#TODO skriv allt i gruppchatten (~5 min)
#TODO plotta fint (? h)

#   Tmrt Bio,   Pet Bio,    Tmrt Noah,  Pet Fredrik     Tmrt+Pet Fredrik
#[  1.96,       13.86,      37.8,       9.9,            98.2                ] per 8784
def subplots(title="Skillnad mellan dagar",days=[{},{},{},{}],funks=["PET_B","PET_N","PET_F","PET_R","Ta"],labels=["PET Biometeo","PET Modifierad","PET Solweig","PET RunWise","Lufttemperatur"]):
    #fig, axs = plt.subplots(2, 2, figsize=(12, 8))
    #fig.suptitle(title)
    labels1=["Feb 24 2024","Maj 17 2024","Juli 29 2024","November 29 2024"]
    xaxis=[i for i in range(24)]# datetime.datetime.now()+datetime.timedelta(hours=i)
    for i in range(4):
        for j in range(len(funks)):
            if funks[j]=="Ta":
               plt.plot(xaxis,np.array(days[i][funks[j]]), label=labels[j],linestyle="--")
            else:
                plt.plot(xaxis,np.array(days[i][funks[j]]), label=labels[j])#axs[i//2, i%2]
        plt.title(labels1[i],fontsize=10)
        plt.xlabel("Tid [h]",fontsize=10)
        plt.xticks([xaxis[i*2] for i in range(len(xaxis)//2)], labels=[f"{('0'+str(2*i))[len(('0'+str(2*i)))-2:]}:00" for i in range(12)],fontsize=10)
        plt.ylabel("Temperatur [°C]",fontsize=10)
        plt.legend(fontsize=10,loc="upper left")
        plt.grid()
        plt.tight_layout()
        plt.gcf().autofmt_xdate()
        plt.show()
    #plt.tight_layout()
    #plt.gcf().autofmt_xdate()
    #plt.show()
def getcor(listofstums):
    a=[np.array(i) for i in listofstums]
    mean=[np.mean(i) for i in a]
    p1=[(a[i]-mean[i]) for i in range(len(a))]
    sumn2=[np.sqrt(np.sum(p1[i]**2)) for i in range(len(a))]
        #listofstums
    cov=np.array([[np.sum(p1[i]*p1[j]) for i in range(len(a))] for j in range(len(a))])
    reducesize=np.array([[1/sumn2[i]/sumn2[j] for i in range(len(a))]for j in range(len(a))])
    return cov*reducesize
def getVar(listofstums,maxormin=None,months=None):
    a=[np.array(i) for i in listofstums]
    cov=np.array([[np.sum((a[i]-a[j])**2) for i in range(len(a))] for j in range(len(a))])
    print((len(a[0])-2))
    #print(cov)
    return np.sqrt(cov/(len(a[0])-2))
def getVarm(listofstums,maxormin=np.max,months=[0,12]):
    a=[[]]*len(listofstums)    
    dbyy= [0, 366, 731, 1096, 1461, 1827, 2192, 2557, 2922, 3288, 3653, 4018, 4383, 4749, 5114, 5479, 5844, 6210, 6575, 6940, 7305, 7671, 8036, 8401, 8766]
    for il in range(len(listofstums)):        
        for y in range(25):
            if (y % 4) == 0:
                dayspermonth = [0, 31, 60, 91, 121, 152, 182, 213, 244, 274, 305, 335,366]
            else:
                dayspermonth = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334,365]
            d1=(dayspermonth[months[0]]+dbyy[y])
            d2=(dayspermonth[months[1]]+dbyy[y])
            a[il]=a[il]+[maxormin(listofstums[il][(d1+i)*24:24*(d1+i+1)]) for i in range(d2-d1)]

    a=[np.array(i) for i in a]
    cov=np.array([[np.sum((a[i]-a[j])**2) for i in range(len(a))] for j in range(len(a))])
    print((len(a[0])-1))
    #print(cov)
    return np.sqrt(cov/(len(a[0])-1))
def dattaaaa(file="dataTmrtPETyear2000to2024",dt="json",dela="\t"):#dataTmrtPETyear2000to2024, dataTmrtPETd
    data=loada(f"{dt}s//{file}.{dt}")["Gothenburg"]
    listofparams=[data["Tmrt_B"],data["Tmrt_N"],data["Tmrt_F"],data["Tmrt_R"],data["PET_B"],data["PET_N"],data["PET_F"],data["PET_R"],data["Ta"],data["RH"],data["Ws"]]
    labels=["Tmrt_B","Tmrt_N","Tmrt_F","Tmrt_R","PET_B","PET_N","PET_F","PET_R","Ta","RH","Ws"]
    cova=getcor(listofparams)
    print("  "+dela+dela.join(labels)+"\n"+"\n".join([labels[i]+dela+dela.join([f"{jj:.3f}" for jj in j]) for i,j in enumerate(cova)]))
def dattaa2a(file="dataTmrtPETyear2000to2024",dt="json",funk=getVar,maxormin=np.max,months=[0,12],dela="\t"):#dataTmrtPETyear2000to2024, dataTmrtPETd
    data=loada(f"{dt}s//{file}.{dt}")["Gothenburg"]
    listofparams=[data["Tmrt_B"],data["Tmrt_N"],data["Tmrt_F"],data["Tmrt_R"],data["PET_B"],data["PET_N"],data["PET_F"],data["PET_R"],data["Ta"]]
    labels=["Tmrt_B","Tmrt_N","Tmrt_F","Tmrt_R","PET_B","PET_N","PET_F","PET_R","Ta"]
    vara=funk(listofparams,maxormin=maxormin,months=months)
    #print(vara)
    print(f"{months[0]+1},{months[1]}\n  "+dela+dela.join(labels)+"\n"+"\n".join([labels[i]+dela+dela.join([f"{jj:.3f}" for jj in j]) for i,j in enumerate(vara)]))
def makeplotsoffast(paramsdif=["dif"],paramplot="PET", para="Ta"):    
    size=100
    Ta=[20]*size#[0.35*i for i in range(size)]#[20]*size#
    RH=[50]*size#[50]*size#[i+1 for i in range(size)]#[50]*size
    Ws=[0.6]*size#[0.2*i for i in range(size)]#[0.2]*size
    if para=="Ta":    
        Ta=[0.35*i for i in range(size)]#[20]*size#
        xp=Ta
        plt.title(paramplot+" som funktion av lufttemperatur med RH=50% och Ws=0.6 m/s",fontsize=10)
        plt.xlabel("Lufttemperatur [°C]",fontsize=10)
    if para=="RH":
        
        RH=[i+1 for i in range(size)]#[50]*size#[i+1 for i in range(size)]#[50]*size
        xp=RH  
        plt.title(paramplot+" som funktion av luftfuktigheten med Ta=20°C och Ws=0.6 m/s",fontsize=10)
        plt.xlabel("Luftfuktigheten [%]",fontsize=10)        
    if para=="Ws":   
        
        Ws=[0.2*i for i in range(size)]
        xp=Ws     
        plt.title(paramplot+" som funktion av vindhastigheten med Ta=20°C och RH=50%",fontsize=10)
        plt.xlabel("Vindhastigheten [m/s]",fontsize=10)    
    form={"Ta":Ta,"RH":RH,"Ws":Ws,"longitude":12.0259, "latitude":57.6801, "altitude":9,"time":["2024-07-01 12:00:00"]*size}
    
    if para=="Tmrt":
        tmrtN=[20+0.3*i for i in range(size)]
        xp,tmrtB,tmrtF,tmrtR=tmrtN,tmrtN,tmrtN,tmrtN        

        petN=[getPETNoah(tmrtN,form,i) for i in range(size)]
        petB=[getPETBioMeteo(tmrtB,form,i) for i in range(size)]
        petF,petR=petN,petN

        plt.xlabel("Tmrt [°C]",fontsize=10)
        plt.title(paramplot+" som funktion av Tmrt med Ta=20°C, RH=50%, Ws=0.6 m/s",fontsize=10)
    else:
        tmrtN=[getTmrtNoah(form,i) for i in range(size)]
        tmrtB=[getTmrtBioMeteo(form,i) for i in range(size)]
        petN=[getPETNoah(tmrtN,form,i) for i in range(size)]
        petB=[getPETBioMeteo(tmrtB,form,i) for i in range(size)]
        
        tpf=[getTmrtPETFredrik(form,i) for i in range(size)]    
        tpr=[getTmrtPETanton(form,i) for i in range(size)]    
        petF=[i[1] for i in tpf]
        tmrtF=[i[0] for i in tpf]
        petR=[i[1] for i in tpr]
        tmrtR=[i[0] for i in tpr]
    
    if paramplot=="Tmrt":
        plt.plot(np.array(xp),np.array(tmrtB),label="Tmrt Biometeo")  
        plt.plot(np.array(xp),np.array(tmrtN),label="Tmrt Modifierad")
        plt.plot(np.array(xp),np.array(tmrtF),label="Tmrt Solweig")
        plt.plot(np.array(xp),np.array(tmrtR),label="Tmrt Runwise")
    else:
        plt.plot(np.array(xp),np.array(petB),label="PET Biometeo")  
        plt.plot(np.array(xp),np.array(petN),label="PET Modifierad")
        plt.plot(np.array(xp),np.array(petF),label="PET Solweig")
        plt.plot(np.array(xp),np.array(petR),label="PET Runwise")

    plt.ylabel(paramplot+" [°C]",fontsize=10)
    plt.legend(fontsize=10,loc="best")
    plt.tight_layout()
    
    plt.show()
    #    #"Tmrt Biometeo","Tmrt Modifierad","Tmrt Solweig"

#dumpa1("pkls//historicweatherdata",loada("jsons//historicweatherdata.json"))
#dumpa1("pkls//dataTP2000to2024",loada("jsons//dataTmrtPETyear2000to2024.json"))
if False:
    data=loada("jsons//dataTmrtPETyear2000to2024sa.json")["Gothenburg"]
    plt.scatter(data["Ta"],data["PET_B"],alpha=0.01,s=2)
    plt.show()
if True:makeplotsoffast(para="Ta");makeplotsoffast(para="RH");makeplotsoffast(para="Ws");makeplotsoffast(para="Tmrt");
if True: makeplotsoffast(para="RH",paramplot="Tmrt");
#print([sum([31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][:i]) for i in range(12)])
#print([sum([31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][:i]) for i in range(12)])
#print([sum((([366]+[365]*3)*6+[366])[:i]) for i in range(25)])
if True: dattaaaa("dataTmrtPETyear2000to2024sa","json");
if True: dattaa2a("dataTmrtPETyear2000to2024sa","json");
if True: dattaa2a("dataTmrtPETyear2000to2024sa","json",funk=getVarm,maxormin=np.max,months=[3,9]);
if True: dattaa2a("dataTmrtPETyear2000to2024sa","json",funk=getVarm,maxormin=np.min,months=[3,9]);

if True: subplots(days=[loada(f"jsons//dataTmrtPETana{i}sa.json")["Gothenburg"] for i in range(4)]);
if True: subplots(days=[loada(f"jsons//dataTmrtPETana{i}sa.json")["Gothenburg"] for i in range(4)],funks=["Tmrt_B","Tmrt_N","Tmrt_F","Tmrt_R","Ta"],labels=["Tmrt Biometeo","Tmrt Modifierad","Tmrt Solweig","Tmrt RunWise","Lufttemperatur"]);
print(["".join([f"{i:.2f} ms " for i in np.array([  1.96,       13.86,      37.8,       9.9,            98.2                ])/8784*1000])])


