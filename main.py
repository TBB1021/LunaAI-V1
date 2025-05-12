from LunaController import LunaSpeechRecognition
from LunaUI import LunaUIApp
import threading

#Main executable file. Run this to start the Luna project
class Main():
    def __init__(self):
        self.backend=LunaSpeechRecognition()
        self.frontend=LunaUIApp(self.backend)
        self.backend.ui=self.frontend
        self.start_app()

    #executes and runs the speech recognition, AI and plugin manager as a secondary thread
    #runs the Kivy GUI on the primary thread
    def start_app(self):
        self.listen_thread = threading.Thread(target=self.backend.HotwordActivation)
        self.listen_thread.start()
        self.frontend.run()
        
    

if __name__ == "__main__":
    Main()
