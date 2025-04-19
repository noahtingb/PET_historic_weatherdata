from biglimp.petprocessing import petcalc
from biglimp.petprocessingprognose import petcalcprognose
import numpy as np
import biglimp.Solweig_v2015_metdata_noload as metload
import biglimp.clearnessindex_2013b as ci
import requests
import json
import base64
import pandas as pd

def index(params):
        try:
            month = int(params["month"])
        except:
            month = -999
        try:
            day = int(params["day"])
        except:
            day = -999
        try:
            hour = int(params["hour"])
        except:
            hour = -999
        year = 2019
        minu = 30
        try:
            Ta = float(params["Ta"])
        except:
            Ta = -999
        try:
            RH = float(params["RH"])
        except:
            RH = -999
        try:
            Ws = float(params["Ws"])
        except:
            Ws = -999
        #try:
        #    radG = float(params["radG"])
        #except:
        #    errors += "<p>{!r} is not a number.</p>\n".format(params["radG"])
        sky = "Clear (100%)"#"Semi-cloudy (80%)"
        
        if month > 12 or month < 0:
            print("petresult.html", f"Incorrect month filled in {month}")
        if day > 31 or day < 0:
            print("petresult.html", f"Incorrect day filled in {day}")
        if hour > 23 or hour < 0:
            print("petresult.html", f"Incorrect hour filled in {hour}")
        if Ta > 60 or Ta < -60:
            print("petresult.html", f"Unreasonable air temperature filled in {Ta}")
        if RH > 100 or RH < 0:
            print("petresult.html", f"Unreasonable relative humidity filled in {RH}")
        if Ws > 100 or Ws < 0:
            print("petresult.html", f"Unreasonable Wind speed filled in {Ws}")

        #day of year
        if (year % 4) == 0:
            if (year % 100) == 0:
                if (year % 400) == 0:
                    leapyear = 1
                else:
                    leapyear = 0
            else:
                leapyear = 1
        else:
            leapyear = 0

        if leapyear == 1:
            dayspermonth = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        else:
            dayspermonth = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

        doy = np.sum(dayspermonth[0:month - 1]) + day

        # Currently looked to Gothenburg
        location = {'longitude': params["longitude"], 'latitude': params["latitude"], 'altitude': params["altitude"]}
        UTC = 0

        # Radiation
        P = -999.
        radG = 40.

        metdata = np.zeros((1, 24)) - 999.
        metdata[0, 0] = year
        metdata[0, 1] = doy
        metdata[0, 2] = hour
        metdata[0, 3] = minu
        metdata[0, 11] = Ta
        metdata[0, 10] = RH

        YYYY, altitude, azimuth, zen, jday, leafon, dectime, altmax = metload.Solweig_2015a_metdata_noload(metdata, location, UTC)
        if altitude > 0.:
            I0, _, Kt, _, _ = ci.clearnessindex_2013b(zen, jday, Ta, RH / 100., radG, location, P)

            if sky == "Clear (100%)":
                radG = I0
            elif sky == "Semi-cloudy (80%)":
                radG = I0 * 0.8
            elif sky == "Cloudy (60%)":
                radG = I0 * 0.6
            else:
                radG = I0 * 0.4

            I0, _, Kt, _, _ = ci.clearnessindex_2013b(zen, jday, Ta, RH / 100., radG, location, P)
        else:
            radG = 0.

        # Main calculation
        if Ta is not None and RH is not None and Ws is not None and radG is not None:
            Tmrt, resultPET, _ = petcalc(Ta, RH, Ws, radG, year, month, day, hour, minu,location)
            return Tmrt,resultPET
