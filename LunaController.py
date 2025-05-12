import speech_recognition as speech
from LunaAI import LunaAi
from modular_Framework1 import PluginManager
import time
from pathlib import Path
#import paramiko
import threading


#the Speech Recognition Class
class LunaSpeechRecognition ():
    #Creates a Recogniser and LunaAI Class that will be used in HotWordActivation
    #Dedicates the word "Luna" as the hot word
    #self.termination is a list of words, if spoken will stop outputing the user's speech
    def __init__(self):
        self.recogniser = speech.Recognizer()
        self.hot_word = ("Luna")
        self.termination=("never mind","doesn't matter","forget it","ignore me","ignore it")
        self.plugin_manager=PluginManager()
        self.lunaconnection=LunaAi()
        self.thread_lock=threading.Lock()
        self.ui= None

    #returns recogniser object   
    def return_stt(self):
        return speech.Recognizer()
    
    #returns microphone object
    def return_mic(self):
        return speech.Microphone()
    
        
    #when executed, the program will constantly be listening via the micrphone for the hot word to be spoken
    #Once Luna is spoken the program will remove Luna from the text. if the user spoke in one sentance such as "luna, what is the time"
    #they will move straight to 3b so their action being executed.
    #otherwise the program will wait for either an action to execute or wait for a cancel comand to stop listening
    def HotwordActivation(self):
        while True:
            print("listening")
            with speech.Microphone() as source:
                self.recogniser.adjust_for_ambient_noise(source)
                try:
                    activation = self.recogniser.listen(source)
                    self.prompt = self.recogniser.recognize_google(activation)
                    print("1.",self.prompt)
                    if self.hot_word in self.prompt:
                        self.prompt= self.prompt.split(self.hot_word, 1)[1].strip()
                        if len(self.prompt)==0:
                            self.lunaconnection.TextToSpeech("You may speak")
                            screen=self.ui.root.get_screen(self.ui.root.current)
                            screen.status.text="Listening"
                            time.sleep(2)
                            spoken_audio = self.recogniser.listen(source, timeout=10, phrase_time_limit=15)
                            self.prompt=self.recogniser.recognize_google(spoken_audio)
                            if self.prompt not in self.termination:
                                print("3a.",self.prompt)
                                self.DetermineActions()
                            else:
                                self.lunaconnection.TextToSpeech("Query cancelled")
                        else:
                            print("3b.",self.prompt)
                            self.DetermineActions()
                except speech.UnknownValueError:
                    print("Audio undetected")

    #locks the hotword detection method
    #grabs user prompt
    def manual_listen(self):
        with self.thread_lock:
            print("manual")
            try:
                with speech.Microphone() as source:
                    self.recogniser.adjust_for_ambient_noise(source)
                    spoken_audio = self.recogniser.listen(source, timeout=10, phrase_time_limit=15)
                    self.prompt=self.recogniser.recognize_google(spoken_audio)
                    self.DetermineActions()
            except speech.UnknownValueError:
                print("audio undetected")
                                       
    
    #if the user says add/delete plug-in then the device will ask what is the name of the plug in and will add/delete it via the plugin manager
    #if the prompt doesnt match with the above, the device will then check if any plug-ins are needed
    #otherwise the device will assume that the query should be answered by Luna itself (using OpenAI's gpt model) 
    def DetermineActions(self):
        screen=self.ui.root.get_screen(self.ui.root.current)
        screen.status.text="Executing"
        if self.prompt == "add plug-in":
            self.lunaconnection.TextToSpeech("What is the name of the plug-in you would like to add?")
            time.sleep(1)
            with speech.Microphone() as source:
                self.recogniser.adjust_for_ambient_noise(source)
                plugin = self.recogniser.listen(source,timeout=10, phrase_time_limit=15)
                plugin_name=self.recogniser.recognize_google(plugin)
                self.plugin_manager.Add_Plugin(plugin_name) 
            self.lunaconnection.TextToSpeech(f"I have added the {plugin_name} plugin")         
        elif self.prompt == "delete plug-in":
            self.lunaconnection.TextToSpeech("What is the name of the plug-in you would like to remove")
            time.sleep(1)
            with speech.Microphone() as source:
                self.recogniser.adjust_for_ambient_noise(source)
                plugin = self.recogniser.listen(source,timeout=10, phrase_time_limit=15)
                plugin_name=self.recogniser.recognize_google(plugin)
                self.plugin_manager.Delete_Plugin(self.recogniser.recognize_google(plugin))  
            self.lunaconnection.TextToSpeech(f"I have deletd the {plugin_name} plugin")
        elif self.plugin_manager.Is_Plugin_Needed(self.prompt):
            print("here3")
            self.plugin_manager.Execute_Command(self.prompt)
        else:
            print("chatgpt")
            self.lunaconnection.sendMessage(self.prompt)
            response=self.lunaconnection.RetrieveResponse()
            self.lunaconnection.TextToSpeech(response)
            if self.lunaconnection.file_created == True:
                #self.CheckFile()
                self.lunaconnection.file_created = False
        screen.status.text="Inactive"
    
    #checks to see if a file has been created
    #if it has, an ssh connection is made between the pi and pc
    #file is then transfered and the original is removed
    """ def CheckFile(self):
        file_path=Path(self.lunaconnection.file_name)
        if file_path.is_file():
            connection = paramiko.SSHClient()
            connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            host=os.getenv('host')
            user=os.getenv('user')
            pass=os.getenv('password')
            connection.connect(hostname=host,username=user,password=password)
            ssh=connection.open_sftp()
            ssh.put(str(file_path),f"C:\\path\\To\\desired location\\{file_path.name}")
            ssh.close()
            connection.close()
            self.lunaconnection.TextToSpeech("File transfered")
            os.remove(file_path.name)
 """




        

    