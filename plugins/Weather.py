import os
import requests
import json
from LunaAI import LunaAi
#creates the weather plugin
class Plugin():
    def __init__(self):
        self.commands = {"what is the weather today in": self.Current_Weather,"what is the forcast for":self.Forecast_Weather}
        self.api=os.getenv("weather_api")
        self.base_location="Ormskirk"
        self.luna=LunaAi()
        self.url="http://api.weatherapi.com/v1"

    #checks to see if any commands are a match
    def Command_Words_Check(self, chosen_command):
        return chosen_command in self.commands

    #executes the given command
    def Execute(self, command, prompt=None):
        if command in self.commands:
            return self.commands[command](prompt)
    #gets the current weather for location x
    # if x isn't provided will assume "Ormskirk"   
    def Current_Weather(self,prompt):
        prompt=prompt.split("in")
        location=prompt[1]
        if location == "":
            location=self.base_location
        curl=self.url+"/current.json"
        parameters = {"key":self.api,"q":location}
        response=requests.get(curl,params=parameters)
        if response.status_code==200:
            data=response.json()
            string_data=json.dumps(data)
            self.luna.sendMessage("Explain this weather json file\n\n"+string_data)
            reply=self.luna.RetrieveResponse()
            self.luna.TextToSpeech(reply)
    #gets the future forecast for location x
    # if x isn't provided will assume "Ormskirk"   
    def Forecast_Weather(self,prompt):
        prompt=prompt.split("in")
        location=prompt[1]
        if location == "":
            location=self.base_location
        curl=self.url+"/forecast.json"
        parameters = {"key":self.api,"q":location,"days":7}
        response=requests.get(curl,params=parameters)
        if response.status_code==200:
            data=response.json()
            string_data=json.dumps(data)
            self.luna.sendMessage("Explain this 7 day weather forecast\n\n"+string_data)
            reply=self.luna.RetrieveResponse()
            self.luna.TextToSpeech(reply)