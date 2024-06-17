import cmd
import os
import shutil
import subprocess
import platform
import datetime
import replicate
import zipfile

class AIAssistantCLI(cmd.Cmd):
    prompt = 'AIAssistantCLI>> '
    intro = 'Welcome to AIAssistantCLI. Type "help" for available commands.'

    def __init__(self):
        super().__init__()
        self.current_directory = os.getcwd()
        self.favorites = []
        self.command_history = []


    def do_list(self, line):
        """List files and directories in the current directory."""
        files_and_dirs = os.listdir(self.current_directory)
        if 'list' not in self.command_history:
            self.command_history.append('list')
        for item in files_and_dirs:
            print(item)

    def do_change_dir(self, directory):
        """Change the current directory."""
        new_dir = os.path.join(self.current_directory, directory)
        if 'change_dir  '+directory  not in self.command_history:
            self.command_history.append('change_dir  '+directory )
        if os.path.exists(new_dir) and os.path.isdir(new_dir):
            self.current_directory = new_dir
            print(f"Current directory changed to {self.current_directory}")
        else:
            print(f"Directory '{directory}' does not exist.")

    def do_create_file(self, filename):
        """Create a new text file in the current directory."""
        file_path = os.path.join(self.current_directory, filename)
        if 'create_file  '+filename  not in self.command_history:
            self.command_history.append('create_file  '+filename )
        try:
            with open(file_path, 'w') as new_file:
                print(f"File '{filename}' created in {self.current_directory}")
        except Exception as e:
            print(f"Error: {e}")

    def do_read_file(self, filename):
        """Read the contents of a text file in the current directory."""
        file_path = os.path.join(self.current_directory, filename)
        if 'read_file  '+filename  not in self.command_history:
            self.command_history.append('read_file  '+filename )
        try:
            with open(file_path, 'r') as existing_file:
                print(existing_file.read())
        except FileNotFoundError:
            print(f"File '{filename}' not found.")
        except Exception as e:
            print(f"Error: {e}")

    def do_delete_file(self, filename):
        """Delete a file in the current directory."""
        file_path = os.path.join(self.current_directory, filename)
        if 'delete_file  '+filename  not in self.command_history:
            self.command_history.append('delete_file  '+filename )
        try:
            os.remove(file_path)
            print(f"File '{filename}' deleted from {self.current_directory}")
        except FileNotFoundError:
            print(f"File '{filename}' not found.")
        except Exception as e:
            print(f"Error: {e}")

    def do_copy_file(self, args):
        """Copy a file to another location."""
        args = args.split()
        if len(args) != 2:
            print("Usage: copy_file <source_file> <destination_directory>")
            return
        source_file = os.path.join(self.current_directory, args[0])
        destination_dir = os.path.join(self.current_directory, args[1])
        if 'copy_file  '+args[0]+'  '+args[1] not in self.command_history:
            self.command_history.append('copy_file  '+args[0]+'  '+args[1])
        try:
            shutil.copy(source_file, destination_dir)
            print(f"File '{args[0]}' copied to '{args[1]}'")
        except FileNotFoundError:
            print("File not found.")
        except Exception as e:
            print(f"Error: {e}")

    def do_move_file(self, args):
        """Move a file to another location."""
        if 'move_file  '+args[0]+'  '+args[1] not in self.command_history:
            self.command_history.append('move_file  '+args[0]+'  '+args[1])
        args = args.split()
        if len(args) != 2:
            print("Usage: move_file <source_file> <destination_directory>")
            return
        source_file = os.path.join(self.current_directory, args[0])
        destination_dir = os.path.join(self.current_directory, args[1])
        try:
            shutil.move(source_file, destination_dir)
            print(f"File '{args[0]}' moved to '{args[1]}'")
        except FileNotFoundError:
            print("File not found.")
        except Exception as e:
            print(f"Error: {e}")
            

    def do_fav(self, filename):
        """Add a file to favorites."""
        file_path = os.path.join(self.current_directory, filename)
        if 'fav  '+filename not in self.command_history:
            self.command_history.append('fav  '+filename)
        if os.path.exists(file_path):
            if not os.path.exists(os.path.join(self.current_directory, "favorites")):
                os.mkdir(os.path.join(self.current_directory, "favorites"))
            favorites_folder = os.path.join(self.current_directory, "favorites")
            try:
                shutil.copy(file_path, favorites_folder)
                print(f"File '{filename}' added to favorites.")
            except Exception as e:
                print(f"Error: {e}")
        else:
            print(f"File '{filename}' not found.")

    def do_show_favorites(self, line):
        """Show all files in the favorites folder."""
        favorites_folder = os.path.join(self.current_directory, "favorites")
        if 'show_favorites' not in self.command_history:
            self.command_history.append('show_favorites')
        if os.path.exists(favorites_folder) and os.path.isdir(favorites_folder):
            favorites_files = os.listdir(favorites_folder)
            if favorites_files:
                print("Files in Favorites:")
                for file in favorites_files:
                    print(file)
            else:
                print("No files in Favorites folder.")
        else:
            print("Favorites folder does not exist or is not a directory.")

    def do_run_script(self, script_name):
        """Run a Python script in the current directory."""
        if 'run_script  '+script_name not in self.command_history:
            self.command_history.append('run_script  '+script_name)
        script_path = os.path.join(self.current_directory, script_name)
        if os.path.exists(script_path) and os.path.isfile(script_path) and script_name.endswith('.py'):
            subprocess.run(['python', script_path])
        else:
            print(f"Script '{script_name}' not found or is not a Python script.")


    def do_search(self, keyword):
        """Search for files containing a specific keyword in the current directory."""
        if 'search  '+keyword not in self.command_history:
            self.command_history.append('search  '+keyword)
        found_files = []
        for root, dirs, files in os.walk(self.current_directory):
            for file in files:
                if keyword in file:
                    found_files.append(os.path.relpath(os.path.join(root, file), self.current_directory))
        if found_files:
            print("Files containing the keyword:")
            for file_path in found_files:
                print(file_path)
        else:
            print("No files found containing the keyword.")

    def do_system_info(self, line):
        """Display system information."""
        if 'system_info' not in self.command_history:
            self.command_history.append('system_info')
        print(f"System: {platform.system()}")
        print(f"Node Name: {platform.node()}")
        print(f"Release: {platform.release()}")
        print(f"Version: {platform.version()}")
        print(f"Machine: {platform.machine()}")

    def do_disk_usage(self, line):
        """Display disk usage of the current directory."""
        if 'disk_usage' not in self.command_history:
            self.command_history.append('disk_usage')
        total, used, free = shutil.disk_usage(self.current_directory)
        print(f"Total Disk Space: {total // (2**30)} GB")
        print(f"Used Disk Space: {used // (2**30)} GB")
        print(f"Free Disk Space: {free // (2**30)} GB")

    def do_date_time(self, line):
        """Display the current date and time."""
        if 'date_time' not in self.command_history:
            self.command_history.append('date_time')
        now = datetime.datetime.now()
        print(f"Current Date and Time: {now}")


    def do_make_directory(self, directory_name):
        """Create a new directory in the current directory."""
        if 'make_directory  '+directory_name not in self.command_history:
            self.command_history.append('make_directory  '+directory_name)
        try:
            os.mkdir(os.path.join(self.current_directory, directory_name))
            print(f"Directory '{directory_name}' created in {self.current_directory}")
        except Exception as e:
            print(f"Error: {e}")

    def do_show_environment(self, line):
        """Display environment variables."""
        if 'show_environment' not in self.command_history:
            self.command_history.append('show_environment')
        for key, value in os.environ.items():
            print(f"{key}: {value}")


    # def do_open_file(self, filename):
    #     """Open a file using the default associated application."""
    #     if 'open_file  '+filename not in self.command_history:
    #         self.command_history.append('open_file  '+filename)
    #     file_path = os.path.join(self.current_directory, filename)
    #     try:
    #         subprocess.run(['open ', file_path])  
    #     except Exception as e:
    #         print(f"Error: {e}")

    def do_chatbot(self, line):
        """Interact with the chatbot AI model."""
        if 'chatbot  '+line not in self.command_history:
            self.command_history.append('chatbot  '+line)
        try:
            os.environ['REPLICATE_API_TOKEN'] = 'r8_EitPANSDsEqDlSrYoGiIiQa9zrssLWi1vFriQ'
            # Call the AI model API to generate a response
            output = replicate.run(
                "meta/llama-2-70b-chat:02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3",
                input={
                    "prompt": line,
                    "max_new_tokens": 250
                },
            )
            for item in output:
                # https://replicate.com/meta/llama-2-70b-chat/api#output-schema
                print(item, end="")
        except Exception as e:
            print(f"Error interacting with the chatbot AI model: {e}")

    def do_com_history(self, line):
        """Display the history of all commands executed."""
        if 'com_history' not in self.command_history:
            self.command_history.append('com_history')
        if self.command_history:
            print("Command History:")
            for i, command in enumerate(self.command_history, start=1):
                print(f"{i}. {command}")
        else:
            print("No commands in history.")

    def do_compress_directory(self, directory_name):
        """Compress a directory into a zip file."""
        directory_path = os.path.join(self.current_directory, directory_name)
        if not os.path.exists(directory_path) or not os.path.isdir(directory_path):
            print(f"Directory '{directory_name}' does not exist or is not a directory.")
            return

        zip_file_name = f"{directory_name}.zip"
        zip_file_path = os.path.join(self.current_directory, zip_file_name)

        try:
            with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(directory_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        relative_path = os.path.relpath(file_path, directory_path)
                        zipf.write(file_path, relative_path)

            print(f"Directory '{directory_name}' compressed into '{zip_file_name}'.")
        except Exception as e:
            print(f"Error compressing directory: {e}")


    def do_quit(self, line):
        """Exit the CLI."""
        return True

    # def postcmd(self, stop, line):
    #     print()  # Add an empty line for better readability
    #     return stop

if __name__ == '__main__':
    AIAssistantCLI().cmdloop()

