class PrintToConsole:
    """
    Class name: PrintToConsole
    Class description: Provide users with the ability to print the server console
    """
    def __init__(self, message):
        """
        Method name: __init__
        Method description: Constructor for PrintToConsole
        @param message: message to be printed to the console
        """
        self.message = message or ''

    def run(self):
        """
        Method name: run
        Method description: runner for PrintToConsole class
        """
        print(self.message)
