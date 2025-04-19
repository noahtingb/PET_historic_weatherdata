# PET_historic_weatherdata
För plottande av en lättare graf kontrollera att alla paket är nedladdade annars kommentera ut dem och sätt paketet till None. 
Därefter ska alla if <True|False>: <something>; vara False förutom <whattoplot> som ska vara True.
Välj därefter parametrarna som vill undersökas och du kan ändra karg till andra parametrar.
Filen jsons//oursmaller.json innehåller data för alla parametrar för platsen Göteborg mellan 00:00:00 den 2023-12-31 och 23:00:00 den 2025-01-01.

Jsonfilerna är uppbyggada som: {place1:params,place2:params}

Följande platser är inkluderade: 
- Gothenburg: Göteborg ((57.6801°,12.0259°) 9 möh)

Förklaring av parametrar: 
- PET_F: Fredriks PET     [°C] (list[float] 1e-2) 
- PET_N: Noahs PET        [°C] (list[float] 1e-2) 
- PET_B: BioMeteo:s PET   [°C] (list[float] 1e-2) 
- Tmrt_F: Fredriks Tmrt   [°C] (list[float] 1e-2) 
- Tmrt_N: Noahs Tmrt      [°C] (list[float] 1e-2) 
- Tmrt_B: BioMeteo:s Tmrt [°C] (list[float] 1e-2) 
- Ta: Luft Temperatur [°C] (list[float] 1e-1) 
- RH: Luftfuktighet [%]    (list[int] (0-100))
- Ws: Vindhastighet [m/s]  (list[float] 1e-1) 
- time: tid som list[STRING] på format "Year-month-day Hour:Minute:Second" 
- longitude: longitud (float -180-180) 
- latitude: breddgrad (float -90-90) 
- altitude: höjd över havet (int 0-9000) 
