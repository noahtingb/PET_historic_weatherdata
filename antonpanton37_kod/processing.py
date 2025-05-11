import time, datetime, biometeo
import biglimp.PET_calculations as b
def covert(strtime="1940-01-01 00:00:00"):
    return datetime.datetime.strptime(strtime,"%Y-%m-%d %H:%M:%S")
def getTmrtPET(params,N=False):
    data={}
    age = int(data.get("age", 35))
    gender = data.get("gender", "man")
    weight = float(data.get("weight", 75))
    place = data.get("location", "Gothenburg")
    height = float(data.get("height", 1.75))
    work = 80 
    if gender.lower() == "man":
        sex = 1
    elif gender.lower() == "kvinna":
        sex = 2
    else:
        sex = 1  # fallback: man

    time_format = covert(params["time"])
    day_of_year = time_format.timetuple().tm_yday
    hour_of_day = time_format.hour+1
    #print("hour_of_day",hour_of_day,hour_of_day)
    lat = params["latitude"]
    lon = params["longitude"]
    sea = params["altitude"]
    Ta = params["Ta"]
    RH = params["RH"]
    Ws = params["Ws"]
    icl = 0.9#0.4

    v1 = biometeo.v1m_cal(Ws, height=10)
    #print(Ta,RH,v1,lon,lat,sea,day_of_year,hour_of_day)
    if N==False:
        alb=0.1
        albhum=0.3
    else:
        alb=0.15
        albhum=0.2
    Tmrt = biometeo.Tmrt_calc(
        Ta=Ta,
        RH=RH,
        v=v1,
        longitude=lon,
        latitude=lat,
        sea_level_height=sea,
        day_of_year=day_of_year,
        hour_of_day=hour_of_day,
        timezone_offset=1,
 #        N=0,G=900,DGratio=0.20,ltf=4.0,
        alb=alb,albhum=albhum,
        RedGChk=False,foglimit=90,bowen=1
    )["Tmrt"]
    #Ta,RH,tmrt,v,mbody,age,ht,work,icl,sex
    PET = b._PET(Ta, RH, Tmrt, v1, weight, age, height, work, icl, sex)
    return Tmrt, PET
