# Blossom

class Core:
    def __init__(self, name):
        self.name = name
        self.history = []

    def update(self):
        pass

    def run(self):
        self.update()

if __name__ == '__main__':
    core = Core('Blossom')
    core.run()
