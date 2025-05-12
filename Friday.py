
class Plugin():
    def __init__(self):
        self.commands = {"test": self.Testfunction}
        

    #checks to see if any commands are a match
    def Command_Words_Check(self, chosen_command):
        return chosen_command in self.commands

    #executes the given command
    def Execute(self, command, prompt=None):
        if command in self.commands:
            return self.commands[command](prompt)
    
    def Testfunction(self):
        print("test")