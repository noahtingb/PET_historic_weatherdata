import noahtingb_kod.Solweig1D_2020a_calc as so
import noahtingb_kod.PET_calculations as p

def indexflask(form,calcaTmrt=True,calcaPET=True):
        Ta = float(form["Ta"])        
        RH = float(form["RH"])
        if Ta > 60 or Ta < -75:
            print("petresult.html", "Unreasonable air temperature filled in",Ta)
        if RH > 100 or RH < 0:
            print("petresult.html", "Unreasonable relative humidity filled in")
        if calcaTmrt:
            month = int(form["month"])
            day = int(form["day"])
            hour = int(form["hour"])
            year = int(form["year"])
            location = form["loc"]
            if month > 12 or month < 0:
                print("petresult.html","Incorrect month filled in")
            if day > 31 or day < 0:
                print("petresult.html","Incorrect day filled in")
            if hour > 23 or hour < 0:
                print("petresult.html","Incorrect hour filled in")
        if calcaPET:
            Ws = float(form["Ws"])
            if Ws > 100 or Ws < 0:
                print("petresult.html", "Unreasonable Wind speed filled in")
        
 
        # Main calculation
        if Ta is not None and RH is not None:
            if calcaTmrt and calcaPET:
                Tmrt, resultPET = petcalc(Ta, RH, Ws, year, month, day, hour,location)
                return resultPET,Tmrt
            elif calcaTmrt and calcaPET==False:
                return calcTmrt(Ta, RH, year, month, day, hour,location)
            elif calcaTmrt==False and calcaPET==True:
                Tmrt = float(form["Tmrt"])
                if Tmrt > 100 or Tmrt < -75:
                    print("petresult.html", "Unreasonable tmrt filled in",Tmrt)
                return calcPet(Ta, RH, Ws, Tmrt)
            elif calcaTmrt==False and calcaPET==False:
                print("Error 67")
                return None
        print("Error 68")
        return None
def indexflaskPET(form):
        Ta = float(form["Ta"])        
        RH = float(form["RH"])
        Tmrt = float(form["Tmrt"])
        Ws = float(form["Ws"])
        if Ta > 60 or Ta < -75:
            print("petresult.html", "Unreasonable air temperature filled in",Ta)
        if RH > 100 or RH < 0:
            print("petresult.html", "Unreasonable relative humidity filled in")
        if Tmrt > 100 or Tmrt < -75:
                print("petresult.html", "Unreasonable tmrt filled in",Tmrt)
        if Ws > 100 or Ws < 0:
                print("petresult.html", "Unreasonable Wind speed filled in")
        
 
        # Main calculation
        if Ta is not None and RH is not None and Tmrt is not None and Ws is not None:
            return calcPet(Ta, RH, Ws, Tmrt)
        print("Error 68")
        return None
            
def indexflaskaTmrt(form):
        Ta = float(form["Ta"])        
        RH = float(form["RH"])
        if Ta > 60 or Ta < -75:
            print("petresult.html", "Unreasonable air temperature filled in",Ta)
        if RH > 100 or RH < 0:
            print("petresult.html", "Unreasonable relative humidity filled in")
        month = int(form["month"])
        day = int(form["day"])
        hour = int(form["hour"])
        year = int(form["year"])
        location = form["loc"]
        if month > 12 or month < 0:
            print("petresult.html","Incorrect month filled in")
        if day > 31 or day < 0:
            print("petresult.html","Incorrect day filled in")
        if hour > 23 or hour < 0:
            print("petresult.html","Incorrect hour filled in")
 
        # Main calculation
        if Ta is not None and RH is not None:
            return calcTmrt(Ta, RH, year, month, day, hour,location)
def calcTmrt(Ta, RH, year, month, day, hour,location):
    Fside,Fup,Fcyl = 0.22,0.06,0.28 #Ståendes vid Liggande:    Fside,Fup,Fcyl = 0.166666, 0.166666, 0.2
    Tmrt = so.Solweig1D_2020a_calc(Fside, Fup, Fcyl,location,Ta, RH, year, month, day, hour,minu=30)
    return float(Tmrt)
def calcPet(Ta, RH, Ws, Tmrt):
    WsPET = (1.1 / 10) ** 0.2 * Ws #corretion from 10 meters height to 1.1 meters height 
    mbody, ht, clo, age, activity, sex = 75., 1.8, 0.9, 35, 80.,  1#[kg], [m], [1], [years], [W], [m 1/f 2]
    resultPET = p._PET(Ta, RH, Tmrt, WsPET, mbody, age, ht, activity, clo, sex) #get Pet
    return float(resultPET)
def petcalc(Ta, RH, Ws, year, month, day, hour,location):        
    Tmrt = calcTmrt(Ta, RH, year, month, day, hour,location)
    resultPET = calcPet(Ta, RH, Ws, Tmrt)
    return Tmrt, resultPET