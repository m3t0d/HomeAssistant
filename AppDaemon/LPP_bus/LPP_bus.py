import appdaemon.plugins.hass.hassapi as hass
import requests
import json
import datetime
#Data from: https://prominfo.projekti.si/web/
#Here you can find stationID, line numbers
#
#
#json location for sttion 600011(Bavarski dvor)
#https://prominfo.projekti.si/lpp_rc/api/600011
#Arguments in apps.yaml
#stationID: station ID from above URL
#refreshinterval: in seconds
#lines:  line nimbers (not numbers at all, but..)
#  - 02
#  - 07
#  - 07L
#

class LPP_bus(hass.Hass):
    def initialize(self):
        self.log("Hello from LPP.py for station " + str(self.args["stationID"]))
        timer = datetime.datetime.now()
        #station ID from parameters
        stationID = self.args["stationID"]
        #url for json data
        url="https://prominfo.projekti.si/lpp_rc/api/"+str(stationID)
        response = requests.get(url)
        if response.status_code != requests.codes.ok:
            #no json data retrieved
            self.log("Something went wrong with internet data ")            
        else:
            stationData=response.json()
            station = stationData['busStationName']
            #station name retrieved and sensor prepared
            self.set_state("sensor.lpp" +str(stationID),state=station,\
                attributes={"friendly_name":"Station"} )

            for line in self.args["lines"]:
                #sensors from argument list prepared with default vaues
                self.set_state("sensor.lpp" + str(stationID) +'bus' + str(line).zfill(2),state=" ",\
                        attributes={"friendly_name" : str(line).zfill(2)} ) 
        
        #initial data retrival
        self.getBusData(self)
        #run refresh every refreshinterval (make no sense less then 60)
        refresh = self.args["refreshinterval"]  
        self.minute = self.run_every(self.getBusData, timer, refresh )
        
    def getBusData(self,kvargs):
        stationID = self.args["stationID"]
        #url for json data
        url="https://prominfo.projekti.si/lpp_rc/api/"+str(stationID)
        response = requests.get(url)
        
        if response.status_code != requests.codes.ok:
            #no json data retrieved
            self.log("Something went wrong with internet data ")
        else: 
            stationData=response.json()
            station = stationData['busStationName']
            sensorsLPP = []
            linesLPP = []
            #prepare list of sensors and lines
        
            for line in self.args["lines"]:
                sensorsLPP.append('sensor.lpp' + str(stationID) + 'bus'+str(line).zfill(2))
                linesLPP.append(str(line).zfill(2))
            #prepare arrivals for bus lines for sensor data
            #format output: first bus in minutes (next bus)   
        
            for i in stationData['arrivals']:
                busID = i['busId']
                busNAME = i['busNameTo']
                first=True
                for j in i['arrivals']:
                    if first:
                        out=str(j['minutes']) 
                        if len(i['arrivals']) != 1:          
                            out=out+' ('
                        first=False
                    else:
                        out=out+str(j['minutes']) + (',')
                if len(i['arrivals']) != 1:          
                    out=out[:-1]+') '
                if str(busID) in linesLPP:
                    self.set_state("sensor.lpp" + str(stationID) +'bus' + str(busID),state=out,\
                        attributes={"friendly_name" : str(busID) + ' '+ busNAME} )
                    linesLPP.remove(str(busID))
     
            #if bus data unavaible set sensor value to N/A  
            #some lines are not 24/7
            for i in linesLPP: 
                old_name=self.get_state("sensor.lpp" + str(stationID) +'bus' + str(i),attribute='friendly_name')
                self.set_state("sensor.lpp" + str(stationID) +'bus' + str(i),state="N/A",\
                        attributes={"friendly_name" : old_name} )          
                
    
