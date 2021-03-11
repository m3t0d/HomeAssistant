### LPP_bus

AppDaemon skripta pridobiva podatke s spleta, ustvari senzorje in osvežuje podatke o prihodih 
v definiranih intervalih.\
Uporabljajo se podatki s spletne strani https://prominfo.projekti.si/ \
Na tej spletni strani najdete podatke o postaji (stationID) in podatke o avtobusnih linijah na teh postajah.\
Sprotini podatki so na povezavi https://prominfo.projekti.si/lpp_rc/api/stationID \
Primer: \
600011(Bavarski dvor), stationID je 600011\
https://prominfo.projekti.si/lpp_rc/api/600011 \
<br>
[apps.yaml](apps.yaml) ima naslednje argumente: \
stationID: station ID, pridobljen iz zgornje lokacije
```
stationID: 600011
```
refreshinterval: in seconds, osvežitev podatkov, nesmiselno je uporabljati manj kot 60, podatki se osvežujejo na minuto
```
refreshinterval: 180 
```
lines:  številke avtobusnih linij (niso samo številke...) 
```
lines:
  - 02
  - 07
  - 07L
```
<br> 

[V skripti](LPP_bus.py) so ustvarjeni senzorji: \
sensor.lppstationID
 - senzor z IDjem postaje (sensor.lpp600011) 
<br> 

senzorji za avtobusne linije:
sensor.lppstationIDbusNr
 - senzor za posamezno linijo (sensor.lpp600011bus07) 

 
<br> 
<br> 

 **Za spremljanje več postaj je potrebno v apps.yaml zagnati več instanc skripte z drugimi parametri.**
