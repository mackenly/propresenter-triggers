from app.utils import import_config


class Example:
    """
    Class name: Example
    Class description: Example class showing the capabilities
        of the plugin system including getting data from the
        config.json file and accepting parameters.
    """
    def __init__(self, value):
        """
        Method name: __init__
        Method description: Constructor for Example class
        @param value: value to print
        """
        self.value = value or 'Default Thingy'
        self.config = import_config().get('actions').get('Example') or {}

    def run(self):
        """
        Method name: run
        Method description: Runner method that prints "Hello from Example action!" plus the value and config
        """
        print('Hello from Example action!\n' + self.value + "\n" + self.config)
