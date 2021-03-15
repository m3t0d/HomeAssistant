# HomeAssistant
HomeAssistant stuff.

### ARSO vreme

REST senzor pridobiva podatke iz strani Agencije Republike Slovenije za Okolje https://www.arso.gov.si/ \
Pdatrki so na strani https://meteo.arso.gov.si/met/sl/service/ v XML obliki, osvežujejo se vsako uro. \
Uporabijo se lahko podatki iz opazovalnih ali samodejnih postaj.
REST senzor se uporablja ker s tem zagotovimo da bo senzor deloval tudi ob dodajanju v XML s strnai ponudnika podatkov.

V tem primeru so uporabljeni podatki za postajo Ljubljana Bežigrad. \
https://meteo.arso.gov.si/uploads/probase/www/observ/surface/text/sl/observation_LJUBL-ANA_BEZIGRAD_latest.xml

Dodati je potrebo senzor v configuration.yaml aku v sensor.yaml (odvisno ali so definivije senzorjev v posebni datoteki).
```
- platform: rest
  scan_interval: 3600
  name: arsovremelj
  resource: http://meteo.arso.gov.si/uploads/probase/www/observ/surface/text/sl/observation_LJUBL-ANA_BEZIGRAD_latest.xml
  json_attributes_path: "$.*.metData"
  json_attributes:
    - t
    - nn_shortText
    - dd_longText
    - msl
    - rh
  value_template: '{{ states.sensor.arsovremelj.attributes["nn_shortText"] }}'
```
Kaj so posamezni atributi lahko ugotovite iz sam datoteke in potrebne atribute dodate v listo atributov.
V tem primeru uporabljamo za vrednost "nn_shortText" kar je z besedo opisano trenutno vreme.\
Ostali atributi ki nas zanimajo postajeno atributi stanja ustvarjenega senzorja.\
Nato s template senzorjem poiščemo te atribute in vrednost dodamo novo ustvarjenim senzorjem. \
V primeru so to temperatura, smer vetra, pritisk in vlaga. \
Lahko ap seveda dodamo ai pa zamenjamo poljuben atribut.

```
- platform: template
  sensors:
    arsotemperaturalj:
      value_template: '{{ states.sensor.arsovremelj.attributes["t"] }}'
      device_class: temperature
      unit_of_measurement: "°C"
    arsoveterlj:
      value_template: '{{ states.sensor.arsovremelj.attributes["dd_longText"] }}'
    arsopritisklj:
      value_template: '{{ states.sensor.arsovremelj.attributes["msl"] }}'
      #device_class: humidity
      unit_of_measurement: "hP"
    arsovlagalj:
      value_template: '{{ states.sensor.arsovremelj.attributes["rh"] }}'
      device_class: humidity
      unit_of_measurement: "%"    
```

<br>
[sensor.yaml](apps.yaml) ima naslednje argumente: \
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
senzor za avtobusno postajo:\
`sensor.lppstationID`
 - senzor z IDjem postaje (sensor.lpp600011) 



senzorji za avtobusne linije: \
`sensor.lppstationIDbusNr`
 - senzor za posamezno linijo (sensor.lpp600011bus07) 

 
<br> 
<br> 

 **Za spremljanje več postaj je potrebno v apps.yaml zagnati več instanc skripte z drugimi parametri.**
