# HomeAssistant

## [AppDaemon](AppDaemon/README.md) 
LPP_bus: podatki o prihodih mestnih avtobusov na postajo

### ARSO vreme

REST senzor pridobiva podatke iz strani Agencije Republike Slovenije za Okolje https://www.arso.gov.si/ \
Podatki so na strani https://meteo.arso.gov.si/met/sl/service/ v XML obliki, osvežujejo se vsako uro. \
Uporabijo se lahko podatki iz opazovalnih ali samodejnih postaj.
REST senzor se uporablja ker s tem zagotovimo da bo senzor deloval tudi ob dodajanju v XML s strani ponudnika podatkov.

V tem primeru so uporabljeni podatki za postajo Ljubljana Bežigrad. \
https://meteo.arso.gov.si/uploads/probase/www/observ/surface/text/sl/observation_LJUBL-ANA_BEZIGRAD_latest.xml

Dodati je potrebo senzor v configuration.yaml ali v sensor.yaml (odvisno ali so definicije senzorjev v posebni datoteki ali pa v configuration.yaml).
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
Kaj so posamezni atributi lahko ugotovite iz same datoteke in potrebne atribute dodate v listo atributov.
V tem primeru uporabljamo za vrednost atributa "nn_shortText" kar je z besedo opisano trenutno vreme.\
Ostali atributi ki nas zanimajo postanejno atributi stanja ustvarjenega senzorja.\
Nato s template senzorjem poiščemo te atribute in vrednost dodamo novo ustvarjenim senzorjem. \
V primeru so to temperatura, smer vetra, pritisk in vlaga. \
Lahko pa seveda dodamo ali pa zamenjamo poljuben atribut.

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

[Primer sensor.yaml](ARSOvreme/sensor.yaml) 
