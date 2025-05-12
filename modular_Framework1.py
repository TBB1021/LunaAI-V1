import importlib
from pathlib import Path
import spacy
import json
import glob
import shutil
import os

#Plugin Manager Class
class PluginManager:
    #Stores the paths of the config file and plugins folder
    def __init__(self):
        self.plugins = {}
        self.nlp = spacy.load("en_core_web_md")
        self.Plugin_Dir=Path("plugins")
        self.config_Dir=Path("config.json")
        self.best_command=""
        self.Load_Config()

    #loads and installs the plugins via importlib
    def Load_Config(self):
        """ Load enabled plugins from config.json """
        if os.path.exists(self.config_Dir):
            with open(self.config_Dir, "r") as file:
                all_plugins = json.load(file).get("plugin_names", [])
                print(all_plugins)
            for plugin in all_plugins:
                if plugin not in self.plugins:
                    module=importlib.import_module(f"{self.Plugin_Dir}.{plugin}")
                    self.plugins[plugin] = module.Plugin()

    #The user will have said the name of the plugin they want to delete.
    #the program will delete the name of the plugin from its current list, the config file and the plugin file itself.
    def Delete_Plugin (self,plugin_name):
        plugin_path=self.Plugin_Dir/f"{plugin_name}.py"
        self.plugins.pop(plugin_name)
        if os.path.exists(plugin_path):
            os.remove(plugin_path)
            with open(self.config_Dir, "w") as file:
                json.dump({"plugin_names": list(self.plugins.keys())}, file, indent=4)

    #This plugin will ad a plugin.
    #This is done by retrieving the name of the plugin and searching the all drives on the device untill an identical match is found.
    # This plugin is them move to the plugins directory ant the config file is updated.
    # The Load_Config file is then executed again to import the module  
    def Add_Plugin (self,plugin_name):
        drive_list=os.listdrives()
        plugin_path=""
        for driver in drive_list:
            files = glob.glob(driver+"/*.py")
            for file in files:
                if plugin_name in file:
                    plugin_path=file
        if len(plugin_path) !=0:
            print(plugin_path)
            print("usb found and plugin located")
            relocation_path=f"{self.Plugin_Dir}/{plugin_name}.py"
            shutil.move(plugin_path,relocation_path)
            with open(self.config_Dir, "w") as file:
                json.dump({"plugin_names": list(self.plugins.keys())}, file, indent=4)
            self.Load_Config()
        else:
            print("usb not found")

            
    #This function is called in DetermineAction function.
    #It uses Spacy to check for similarities between the users prompt and the command words of each plugin.
    #it does this by comparing the scores of each comparisons with the higher score being stored in best_score
    #if best score isn't bigger then 0.70 (70%) then the function returns False meaning a plugin isnt needed.
    #if True is returned the Speech rec program will then run the execute command function.
    def Is_Plugin_Needed (self,prompt):
        best_score=0
        input=self.nlp(prompt)
        for plugin in self.plugins.values():
            for command,_ in plugin.commands.items():
                command_check=input.similarity(self.nlp(command))
                print(command_check,command)
                if command_check > best_score:
                    best_score=command_check
                    self.best_command=command
        if best_score > 0.75:
            return True
        else:
            return False
    
    #The program will check to see which plugin the query matches and executes the corresponding command
    #Retrieves the best command variable.
    def Execute_Command(self,prompt):
        for plugin in self.plugins.values():
            if  plugin.Command_Words_Check(self.best_command):
                return plugin.Execute(self.best_command,prompt)
            

    