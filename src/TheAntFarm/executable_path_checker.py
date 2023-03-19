
import os
import sys
import shutil


class ExecutablePathChecker:

    def __init__(self):

        self.script_path = ""
        self.application_path = ""
        self.update_paths()

    def update_paths(self):
        script_path = os.path.abspath(os.path.dirname(__file__))
        application_path = ""

        # determine if application is a script file or frozen exe
        if getattr(sys, 'frozen', False):
            print("From Executable")
            application_path = os.path.abspath(os.path.dirname(sys.executable))
        elif __file__:
            print("From Script")
            application_path = script_path
        self.script_path = script_path
        self.application_path = application_path

    def create_data_folders(self):

        print("Script Path: " + str(self.script_path))
        print("Exec Path: " + str(self.application_path))
        if self.script_path != self.application_path:
            macros_path_source = os.path.join(self.script_path, "macros")
            macros_path_dest = os.path.join(self.application_path, "macros")

            if not os.path.isdir(macros_path_dest):
                if os.path.isdir(macros_path_source):
                    print("Local macros Folder Creation")
                    shutil.copytree(macros_path_source, macros_path_dest)

        return self.application_path
