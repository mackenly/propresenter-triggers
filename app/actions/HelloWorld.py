from app.actions.Action import Action


class HelloWorld(Action):
    """
    Class name: HelloWorld
    Class description: Class used for testing that prints "Hello World!"
    """
    def __init__(self):
        """
        Method name: __init__
        Method description: Constructor for HelloWorld class
        """
        pass

    def run(self):
        """
        Method name: run
        Method description: Runner method that prints "Hello World!"
        """
        print("Hello World!")
