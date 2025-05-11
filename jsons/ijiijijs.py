import matplotlib.pyplot as plt
import json,datetime
from com.aton import getTmrtPET
import numpy as np
def covert(strtime="1940-01-01 00:00:00"):
    return datetime.datetime.strptime(strtime,"%Y-%m-%d %H:%M:%S")
def dumpa(name="ddddd.json",result=None):
    with open(name, 'w') as f:
            json.dump(result,f)
def procentdone(index,total,before=""):
    if ((index-1)*10)//total != ((index)*10)//total:
        print(before+f"{(index*100)//total}%")
def loada(name="jsons//historicweatherdata.json"):
    with open(name,"r") as f:
        return json.load(f)
def getTmrtPETanton(params,indexforparams,N=False):
        print(params["time"][indexforparams])
        form={"Ta":params["Ta"][indexforparams],"RH":params["RH"][indexforparams],"Ws":params["Ws"][indexforparams],"time":params["time"][indexforparams],
              "longitude":params["longitude"], "latitude":params["latitude"], "altitude":params["altitude"]}
        Tmrt,PET=getTmrtPET(form,N)
        return float(Tmrt),float(PET)
def loopa():
    zerotime=covert("1940-01-01 00:00:00")
    starttime=covert("2024-06-30 23:00:00")
    endtime=covert("2024-07-01 22:00:00")
    timedif=int((endtime-starttime).total_seconds()//3600+1)
    index0=int((starttime-zerotime).total_seconds()//3600)
    print("index0",index0)
    tdata=[-275]*timedif
    pdata=[-275]*timedif
    t1data=[-275]*timedif
    p1data=[-275]*timedif

    dddd=loada()["Gothenburg"]
    dddd["Ta"]=dddd["hourly"]["Ta"][index0:index0+timedif]
    dddd["RH"]=dddd["hourly"]["RH"][index0:index0+timedif]
    dddd["Ws"]=dddd["hourly"]["Ws"][index0:index0+timedif]
    dddd["time"]=dddd["hourly"]["time"][index0:index0+timedif]
    dddd["hourly"]=None
    for i in range(timedif):
        procentdone(i,timedif)
        tdata[i],pdata[i]=getTmrtPETanton(dddd,i,N=False)
        t1data[i],p1data[i]=getTmrtPETanton(dddd,i,N=True)

        print(tdata[i],pdata[i],dddd["Ta"][i])
    plt.plot(np.array(tdata),label="Tmrt")
    plt.plot(np.array(pdata),label="PET")
    plt.plot(dddd["Ta"],label="Ta")
    plt.plot(np.array(t1data),label="Tmrt N")
    plt.plot(np.array(p1data),label="PET N")
    plt.legend()
    return tdata,pdata
y=loopa()
plt.show()
