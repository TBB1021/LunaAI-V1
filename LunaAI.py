from audioplayer import AudioPlayer
from openai import OpenAI
import os
import time
#LunaAI class                
class LunaAi():
    #grabs the api keys for OpenAI and Luna Assistant via a .env file and created the OpenAI object
    def __init__(self):
        aikey=os.getenv('OAkey')
        self.lkey=os.getenv('LunaKey')
        self.client=OpenAI(api_key=aikey)
        self.file_created=False
    
    #Creates a connection to the Assistant API and sends the user's prompt through
    #The program will then loop till the query is completed returning a answer.
    #This response is then pushed to the TextToSpeech function
    def sendMessage (self,prompt):          
        self.luna=self.client.beta.assistants.retrieve(self.lkey)
        self.thread=self.client.beta.threads.create()
        self.client.beta.threads.messages.create(self.thread.id,role="user",content=prompt,)
        
    #retrieves the response after message is sent.
    # if the message contains a file then the file is created and stored for the check file method.    
    def RetrieveResponse (self):    
        runned=self.client.beta.threads.runs.create(thread_id=self.thread.id,assistant_id=self.luna.id)
        while self.client.beta.threads.runs.retrieve(thread_id=self.thread.id,run_id=runned.id).status !="completed":
            time.sleep(1)
        messages=self.client.beta.threads.messages.list(self.thread.id)
        try:
            file_id=messages.data[0].content[0].text.annotations[0].file_path.file_id
            file=self.client.files.content(file_id)
            file_bytes = file.read()
            self.file_name = (messages.data[0].content[0].text.annotations[0].text).split("/")[-1]
            with open(self.file_name, "wb") as file:
                file.write(file_bytes)
            self.file_created=True
            return messages.data[0].content[0].text.value
        except:
            return messages.data[0].content[0].text.value
        
    #Use OpenAI to translate text to speech for the AI to converse
    #removes audio file after played
    def TextToSpeech (self,prompt):
        tts = self.client.audio.speech.create(model="tts-1", voice="nova",input=prompt,)
        tts.write_to_file("speech.mp3")
        print("speaking")
        AudioPlayer("speech.mp3").play(block=True)
        print("stopped speaking")
        os.remove("speech.mp3")

        