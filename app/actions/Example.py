import logging
from app.utils import import_config


class Example:
    """
    Class name: Example
    Class description: Example class showing the capabilities
        of the plugin system including getting data from the
        config.json file and accepting parameters.
    """

    def __init__(self, value='Default Thingy'):
        """
        Method name: __init__
        Method description: Constructor for Example class
        @param value: value to print
        """
        # Use the value passed in as a parameter (if any) or the default value
        self.value = value

        # Get the config value from the config.json file or an empty string
        self.config = import_config().get('actions')['Example'] or ""

    def run(self):
        """
        Method name: run
        Method description: Runner method that prints "Hello from Example action!" plus the value and config
        """
        # Print to the console
        print('Hello from Example action!\n' + self.value + "\n" + self.config)

        # Log to the server console
        logging.info('Hello from Example action! ' + self.value + " " + self.config)
