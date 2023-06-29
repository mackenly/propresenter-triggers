class PrintToConsole:
    def __init__(self, message):
        self.message = message or ''

    def run(self):
        print(self.message)
