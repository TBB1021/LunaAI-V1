import json
import os
from LunaAI import LunaAi
#creates the notes plugins
class Plugin():
    def __init__(self):
        self.commands = {"create a note titled": self.create_note,"read note": self.read_note,"delete note": self.delete_note,"tell me my notes":self.list_notes}
        self.notes_file = "local_notes.json"
        self.luna = LunaAi()
        if not os.path.exists(self.notes_file):
            with open(self.notes_file, 'w') as f:
                json.dump({}, f)

    #checks to see if any commands are a match
    def Command_Words_Check(self, chosen_command):
        return chosen_command in self.commands

    #executes the given command
    def Execute(self, command, prompt=None):
        if command in self.commands:
            return self.commands[command](prompt)
    #loads the local_notes.json file
    def load_notes(self):
        with open(self.notes_file, 'r') as f:
            return json.load(f)
    #writes to the file
    def save_notes(self, notes):
        with open(self.notes_file, 'w') as f:
            json.dump(notes, f, indent=4)
    #creates a new entry
    def create_note(self, prompt):
        title = prompt.replace("create a note titled", "").strip()
        notes = self.load_notes()
        if title in notes:
            self.luna.TextToSpeech(f"A note titled {title} already exists.")
        else:
            notes[title] = []
            self.save_notes(notes)
            self.luna.TextToSpeech(f"Note {title} created.")
    #reads the notes using TTS
    def read_note(self, prompt):
        title = prompt.replace("read note", "").strip()
        notes = self.load_notes()
        if title in notes:
            content = "\n".join(notes[title])
            self.luna.TextToSpeech(f"Note {title} contains: {content}")
        else:
            self.luna.TextToSpeech(f"No note named {title} found.")
    #removes entry
    def delete_note(self, prompt):
        title = prompt.replace("delete note", "").strip()
        notes = self.load_notes()
        if title in notes:
            del notes[title]
            self.save_notes(notes)
            self.luna.TextToSpeech(f"Note {title} deleted.")
        else:
            self.luna.TextToSpeech(f"No note named {title} found.")
    #reads all notes using TTS
    def list_notes(self, prompt=None):
        notes = self.load_notes()
        if notes:
            titles = ", ".join(notes.keys())
            self.luna.TextToSpeech(f"Your notes are: {titles}")
        else:
            self.luna.TextToSpeech("You have no notes yet.")
