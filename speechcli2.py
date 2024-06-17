import cmd
import os
import shutilji
import subprocess
import speech_recognition as sr

class CommandForgeCLI(cmd.Cmd):
    prompt = 'CommandForge>> '
    intro = 'Welcome to CommandForgeCLI. Type "help" for available commands.'

    def __init__(self):
        super().__init__()
        self.current_directory = os.getcwd()
        self.favorites = []
        self.recognizer = sr.Recognizer()

    def do_list(self, line):
        """List files and directories in the current directory."""
        files_and_dirs = os.listdir(self.current_directory)
        for item in files_and_dirs:
            print(item)


    def do_quit(self, line):
        """Exit the CLI."""
        return True

    def listen_and_execute(self):
        print("Listening...")
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)

        try:
            # Recognize speech using Google Speech Recognition
            command = self.recognizer.recognize_google(audio).lower()
            print("You said:", command)
            self.onecmd(command)  # Run the recognized command
        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))

    def cmdloop_with_voice(self):
        while True:
            self.listen_and_execute()

if __name__ == '__main__':
    CommandForgeCLI().cmdloop_with_voice()
