# Blossom
from dflow import Dflow
import subprocess

class Core:
    def __init__(self, name):
        self.name = name
        self.agent = Dflow(self)

    def speak(self, text):
        subprocess.run(['espeak', '-ven+f3', '-s 150', '-p 50', text])
        print(text)

    def run(self):
        while True:
            self.speak(self.agent.get_response(input("Query: ").lower()))

if __name__ == '__main__':
    core = Core('Blossom')
    core.run()
