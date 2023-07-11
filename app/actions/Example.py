import logging
from app.actions.Action import Action
from app.utils import import_config
from app.utils import ActionError


class Example(Action):
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

        # See how to throw an exceptions by setting the value to "Test" or "Ronald"
        if self.value == "Test" or self.value == "Ronald":
            # Demonstrate how to raise an exception
            if self.value == "Ronald":
                raise ActionError("Ronald isn't allowed")

            # Demonstrate try/except
            try:
                # this will always fail
                print(1 / 0)
            except Exception as e:
                # You can log to the server console
                logging.info('You can\'t divide by zero')
                # Then raise an exception to block the action
                raise ActionError('Example try/except error: ' + str(e))

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
