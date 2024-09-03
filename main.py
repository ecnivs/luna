# Blossom
from dflow import Dflow

class Core:
    def __init__(self, name):
        self.name = name
        self.agent = Dflow(self.name)

    def run(self):
        while True:
            print(self.agent.get_response(input("Query: ").lower()))

if __name__ == '__main__':
    core = Core('Blossom')
    core.run()
