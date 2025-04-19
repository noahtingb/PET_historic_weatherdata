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
        hod=(time.hour+1/2+params["longitude"]/15)%24
        Tmrt=biometeo.Tmrt_calc(Ta=params["Ta"][indexforparams], RH=params["RH"][indexforparams], v=0, longitude=params["longitude"], latitude=params["latitude"], sea_level_height=params["altitude"],day_of_year=doy, hour_of_day=hod,timezone_offset=0,alb=0.2, albhum=0.15)
        #params={"year":year,"month":month,"day":day,"hour":hour,"Ta":Ta,"SwR":0.,"RH":RH,"Ws":Ws,"sky":"Clear (100%)","radI":0., "radD":0., "loc":location,"UTC":0}
        return float(Tmrt["Tmrt"])
def getPETBioMeteo(Tmrt,params,indexforparams,funktion=biometeo.PET):
        if type(Tmrt)==type([]):
            Tmrt=Tmrt[indexforparams]
        VP=float(biometeo.VP_RH_exchange(Ta=params["Ta"][indexforparams],RH=params["RH"][indexforparams])["VP"])
        resultPET2=funktion(Ta=params["Ta"][indexforparams],VP=VP,v=(1.1 / 10) ** 0.2 * params["Ws"][indexforparams],Tmrt=Tmrt)["PET_v"]
        return float(resultPET2)

#TODO fixa noahtingb:s kod (~45 min) (faktiskt 27 min)
import noahtingb_kod.petprocessing as noahtingb
def getTmrtNoah(params,indexforparams):
        time=covert(params["time"][indexforparams])
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
#DONE fixa fredrik:s kod ren (~1 h 15 min) (faktiskt 16 min)
import biglimp.flask_app as fkoof
def getTmrtPETFredrik(params,indexforparams):
        timesjustering=covert(params["time"][indexforparams])+datetime.timedelta(hours=params["longitude"]/15)
        form={"Ta":params["Ta"][indexforparams],"RH":params["RH"][indexforparams],"Ws":params["Ws"][indexforparams],"year":timesjustering.year,
              "month":timesjustering.month,"day":timesjustering.day,"hour":timesjustering.hour,
              "longitude":params["longitude"], "latitude":params["latitude"], "altitude":params["altitude"]}
        Tmrt,PET=fkoof.index(form)
        return float(Tmrt),float(PET)
def procentdone(index,total,before=""):
    if ((index-1)*100)//total != ((index)*100)//total:
        print(before+f"{(index*100)//total}%")
#DONE date to index (~30 min)
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
        print(data["time"])
        #data={place:{"latitude":file["latitude"], "longitude":file["longitude"], "elevation":file["elevation"],"time":time,"Ta":data["hourly"]["Tas"][index0:index0+timedif],"RH":data["hourly"]["RHs"][index0:index0+timedif],"Ws":data["hourly"]["Wss"][index0:index0+timedif]}}
        if "Tmrt_B" in funks:
            dictofour=loada("jsons//"+fileour+".json")
            for i in range(timedif):
                procentdone(i,timedif)                
                dictofour[place]["Tmrt_B"][index0+i]=getTmrtBioMeteo(data,i)
            dumpa("jsons//"+filenew+".json",dictofour)
        if "PET_B" in funks:
            dictofour=loada("jsons//"+fileour+".json")
            for i in range(timedif):
                procentdone(i,timedif)
                Tmrt=dictofour[place]["Tmrt_B"][index0+i]
                if Tmrt==-275:
                    Tmrt=getTmrtBioMeteo(data,i)
                dictofour[place]["PET_B"][index0+i]=getPETBioMeteo(Tmrt,data,i)
            dumpa("jsons//"+filenew+".json",dictofour)
        if "mPET_B" in funks:
            dictofour=loada("jsons//"+fileour+".json")
            for i in range(timedif):
                procentdone(i,timedif)
                Tmrt=dictofour[place]["Tmrt_B"][index0+i]
                if Tmrt==-275:
                    Tmrt=getTmrtBioMeteo(data,i)
                dictofour[place]["mPET_B"][index0+i]=getPETBioMeteo(Tmrt,data,i,funktion=biometeo.mPET)
            dumpa("jsons//"+filenew+".json",dictofour)
        if "Tmrt_N" in funks:
            dictofour=loada("jsons//"+fileour+".json")
            for i in range(timedif):
                procentdone(i,timedif)
                dictofour[place]["Tmrt_N"][index0+i]=getTmrtNoah(data,i)
            dumpa("jsons//"+filenew+".json",dictofour)
        if "PET_N" in funks:
            dictofour=loada("jsons//"+fileour+".json")
            for i in range(timedif):
                procentdone(i,timedif)
                Tmrt=dictofour[place]["Tmrt_N"][index0+i]
                if Tmrt==-275:
                    print(f"Error {i}")
                    Tmrt=getTmrtNoah(data,i)
                dictofour[place]["PET_N"][index0+i]=getPETNoah(Tmrt,data,i)
            dumpa("jsons//"+filenew+".json",dictofour)
        if "TmrtPET_F" in funks:
            dictofour=loada("jsons//"+fileour+".json")
            for i in range(timedif):
                procentdone(i,timedif)
                dictofour[place]["Tmrt_F"][index0+i],dictofour[place]["PET_F"][index0+i]=getTmrtPETFredrik(data,i)
            dumpa("jsons//"+filenew+".json",dictofour)
        print("Done mabye")
#? loppa dem (~15 min) (+felsökning ca 1-2 h)

if False: loppa(startstr="2023-12-31 00:00:00",endstr="2025-01-01 23:00:00",funks=["Tmrt_B","PET_B","Tmrt_N","PET_N","TmrtPET_F"],fileour="datareala",filenew="datareala")
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
        for keys in ["Tmrt_N","Tmrt_B","Tmrt_F","PET_N","PET_F","PET_B"]:
            data[keys]=dictofour[keys][index0:index0+timedif]
            dictofour.pop(keys)
        try:
            smalldata=loada("jsons//"+filenew+".json")     
        except:
            smalldata={}
        smalldata[place]=data
        dumpa("jsons//"+filenew+".json",smalldata)   
if False: bigtosmall();

#to reduce the size of the files easy function
def avrundvalues(searchway=[["Gothenburg",["Tmrt_N","Tmrt_B","Tmrt_F","PET_N","PET_F","PET_B"]]],oldfile="oursmall",newfile="oursmaller",decimals=2):
    data=loada("jsons//"+oldfile+".json") 
    for search in searchway:
        place=search[0]
        for key in search[1]:
            data[place][key]=[float(round(i, decimals)) for i in data[place][key]]
    dumpa("jsons//"+newfile+".json",data) 
if False: avrundvalues();

#easy plot to two params
import matplotlib.pyplot as plt
def plota(x,y,title="",xlabel="",ylabel="",karg={}):
    alpha=1 if (karg.get("alpha")==None) else karg["alpha"]
    linewidths=1 if (karg.get("linewidths")==None) else karg["linewidths"]
    print(alpha,linewidths)
    plt.title(title)
    plt.scatter(x=x,y=y,alpha=alpha,linewidths=linewidths)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    if karg.get("linemaxminsomething")==True:
        lista=[min(np.min(np.array(x)),np.min(np.array(y))),min(np.max(np.array(x)),np.max(np.array(y)))]
        plt.plot(lista,lista,linewidth=1,color="orange")
def whattoplot(x_key="Tmrt_F",y_key="Tmrt_N",place="Gothenburg",oldfile="oursmaller"):
    data=loada("jsons//"+oldfile+".json") 
    plota(x=data[place][x_key],y=data[place][y_key],title="Comparsion",xlabel=f"{x_key} [°C]",ylabel=f"{y_key} [°C]",karg={"alpha":0.1,"linewidths":0.1,"linemaxminsomething":True})
    plt.show()
if True: whattoplot();
#DONE importa alla Tmrt och Pet som är relevanta (~1-3 h)
#DONE fixa lopen
#DONE runna allting (~1-3 h) (small)

#TODO plotta sedan dem enlig saker (~1.5 h)
#TODO skriv allt i gruppchatten (~5 min)
#Allt som allt  (~5-9 h (5 kod, 2 väntande, 2 extra logg))


