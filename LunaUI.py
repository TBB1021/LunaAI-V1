from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.uix.colorpicker import ColorPicker
from kivy.uix.popup import Popup
import threading
from datetime import datetime
import time


#creates the main/home screen
class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        #upper layout
        self.Plugin_Dir="plugins"
        screen_layout=BoxLayout(orientation="vertical",padding=10, spacing=10)
        upper_layout=BoxLayout(padding=10, spacing=10,)
        self.time_date_label=Label(text="")
        upper_layout.add_widget(self.time_date_label)
        x=threading.Thread(target=self.TimeDate,args=(1,), daemon=True)
        x.start()
        voice_input = Button(text="Press to Speak",on_press=self.manual_input,background_color=(0,0,0,0.2),size=(100,50)) 
        upper_layout.add_widget(voice_input)
        self.status=Label(text="Inactive")
        upper_layout.add_widget(self.status)
        screen_layout.add_widget(upper_layout)
        #middle Layout
        self.middle_layout=GridLayout(cols=4,spacing=10, size_hint_y=0.7)
        self.load_plugins()
        screen_layout.add_widget(self.middle_layout)
        #lower layout
        lower_layout=BoxLayout(padding=10, spacing=10,)
        settings = Button(text="Settings",on_press=self.open_settings,background_color=(0,0,0,0.2),size=(100,50)) 
        lower_layout.add_widget(settings)
        screen_layout.add_widget(lower_layout)
        self.add_widget(screen_layout)

    #Overides the hotword activation method
    def manual_input(self,ph):
        speech= App.get_running_app().backend
        self.status.text="Listening"
        listen=threading.Thread(target=speech.manual_listen)
        listen.start()
    
    #Is called when a plugin is added or removed
    def reset_plugin(self):
        self.load_plugins()

    #creates a button for every plugin installed
    def load_plugins(self):
        backend = App.get_running_app().backend
        plugin_manager = backend.plugin_manager
        self.middle_layout.clear_widgets()
        for plugin in plugin_manager.plugins:
            button = Button(text=plugin, on_press=lambda x, name=plugin: self.open_plugin(name),background_color=(0,0,0,0.2),size=(100,50))
            self.middle_layout.add_widget(button)
        
    #switches the showed screen to 'plugins'
    #runs the Add_command list before screen switch
    def open_plugin(self,name):
        backend = App.get_running_app().backend
        plugin = backend.plugin_manager.plugins.get(name)
        commands = list(plugin.commands.keys())
        self.manager.get_screen('plugin').add_Commands(name,commands)
        self.manager.current = 'plugin'

    #switches the showed screen to 'settings'
    def open_settings(self,ph):
        self.manager.current = 'settings'
    
    def TimeDate (self,ph):
        while True:
            current_time=datetime.now()
            self.time_date_label.text = current_time.strftime("%H:%M --- %d/%m/%Y")
            time.sleep(1)
    
    def alter_button_colour(self,colour):
        print("here3")
        for widget in self.walk():
            if isinstance(widget, (Label, Button)):
                widget.color = colour

#Creates the setting page
class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        screen_layout=BoxLayout(orientation="vertical",padding=10, spacing=10)
        upper_layout=BoxLayout(padding=10, spacing=10,)
        settingLabel=Label(text="Settings Page")
        upper_layout.add_widget(settingLabel)
        self.status=Label(text="Inactive")
        upper_layout.add_widget(self.status)
        screen_layout.add_widget(upper_layout)
        middle_layout=BoxLayout(padding=10, spacing=10,)
        bg_colour = Button(text="Change background Colour",on_press=lambda x:self.colour_picker("Background"),background_color=(0,0,0,0.2),size=(100,50)) 
        text_colour = Button(text="Change text Colour",on_press=lambda x:self.colour_picker("text"),background_color=(0,0,0,0.2),size=(100,50)) 
        exit = Button(text="Home",on_press=self.open_home,background_color=(0,0,0,0.2),size=(100,50))
        middle_layout.add_widget(bg_colour)
        middle_layout.add_widget(text_colour)
        screen_layout.add_widget(middle_layout)
        screen_layout.add_widget(exit)
        self.add_widget(screen_layout)

    #switches the showed screen to 'main'
    def open_home(self,ph):
        self.manager.current = 'main'

    #opens the colour picker widget 
    def colour_picker(self,type):
        self.type=type
        colour_picker = ColorPicker()
        popup = Popup(title="Select chosen Color", content=colour_picker, size_hint=(None, None), size=(400, 400))
        colour_picker.bind(color=self.selected)
        popup.open()

    #selected colour becomes the primary colour of the background or text based on which button is pressed
    def selected (self, ph, colour_value):
        if self.type =="Background":
            print("here")
            Window.clearcolor = colour_value
        elif self.type == "text":
            print("here2")
            for widget in self.walk():
                if isinstance(widget, (Label, Button)):
                    widget.color = colour_value
            self.manager.get_screen('main').alter_button_colour(colour_value)
            self.manager.get_screen('plugin').alter_button_colour(colour_value)

#Creates the plugin screen
class PluginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        screen_layout = BoxLayout(orientation="vertical",padding=10, spacing=10)
        upper_layout=BoxLayout(padding=10, spacing=10,)
        self.plugin_name = Label(text="")
        self.status=Label(text="Inactive")
        upper_layout.add_widget(self.plugin_name)
        upper_layout.add_widget(self.status)
        screen_layout.add_widget(upper_layout)
        self.command_text = Label(text="")
        self.command_layout = GridLayout(cols=4,spacing=10, size_hint_y=0.7)
        screen_layout.add_widget(self.command_layout)
        lower_layout=BoxLayout(padding=10, spacing=10,)
        back=Button(text="Home",on_press=self.open_home,background_color=(0,0,0,0.2),size=(100,50))
        lower_layout.add_widget(back)
        screen_layout.add_widget(lower_layout)
        self.add_widget(screen_layout)
        
    #switches the showed screen to 'main'
    def open_home(self,ph):
        self.manager.current = 'main'

    #adds the commands of selected plugin to be viewd
    def add_Commands(self,name, commands):
        self.command_layout.clear_widgets()
        self.plugin_name.text = name
        self.command_text.text = f"These are the commands for the {name} plugin:"
        for command in commands:
            self.command_layout.add_widget(Label(text=command, size_hint_y=None, height=30,))
    
    #is called to alter the text colour
    def alter_button_colour(self,colour):
        print("here3")
        for widget in self.walk():
            if isinstance(widget, (Label, Button)):
                widget.color = colour

#Main class
#inits the entire app
class LunaUIApp (App):
    def __init__(self,backend,**kwargs):
        super().__init__(**kwargs)
        self.backend= backend
    def build(self):
        page = ScreenManager()
        Window.clearcolor = (0.2, 0.5, 0.8, 0)
        page.add_widget(MainScreen(name='main'))
        page.add_widget(SettingsScreen(name='settings'))
        page.add_widget(PluginScreen(name='plugin'))
        return page


if __name__ == '__main__':
    LunaUIApp().run()