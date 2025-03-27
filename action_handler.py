from settings import *
import webbrowser

class ActionHandler:
    def __init__(self, core):
        self.core = core

    def run_cmd(self, command):
        os.system(command)

    def turn_on_camera(self):
        self.core.handler.llm.cam = True

    def turn_off_camera(self):
        self.core.handler.llm.cam = False

    def open_site(self, url):
        webbrowser.open(url)
