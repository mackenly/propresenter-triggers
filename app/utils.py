import os
import json
import logging
import importlib.util
import time


def load_class_and_initialize(key, value):
    """
    Method name: load_class_and_initialize
    Description: load class locate in actions folder and initialize it
    @param key: action key - file and class name
    @param value: action value - parameter to pass to action's constructor
    @return: object of action class
    """
    # create path to python file
    path_to_module = os.path.join('.', 'actions', f'{key}.py')

    # load module
    spec = importlib.util.spec_from_file_location(key, path_to_module)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    # get class from module
    class_ = getattr(module, key)

    # if object accepts 1 parameter, pass value to constructor
    if len(class_.__init__.__code__.co_varnames) >= 2:
        new_object = class_(value)
    else:
        new_object = class_()

    return new_object


def trigger_thread(key, value, delay=0, then=None):
    """
    Method name: trigger_thread
    Description: create a thread to execute a trigger asynchronously, if delay is greater than 0 wait for delay milliseconds
    @param key: action key - file and class name
    @param value: action value - parameter to pass to action's constructor
    @param delay: delay in milliseconds
    @param then: trigger to execute after this trigger completes
    """
    try:
        if delay > 0:
            time.sleep(delay / 1000)
        try:
            new_object = load_class_and_initialize(key, value)
            new_object.run()
        except ActionError as e:
            logging.error(f'Internal action error: {e}')
            return False
        except Exception as e:
            logging.error(f'Invalid action: {e}')
            return False
        try:
            if then is not None:
                trigger_thread(then.get("key"), then.get("value"), then.get("delay") or 0, then.get("then") or None)
        except Exception as e:
            logging.error(f'Invalid "then" trigger: {e}')
    except Exception as e:
        logging.error(f'Invalid trigger: {e}')
    return True


def import_config():
    """
    Method name: import_config
    Description: import config.json file
    @return: config.json file as dictionary
    """
    try:
        with open("config.json") as f:
            return json.load(f)
    except Exception as e:
        logging.error("Error importing config file")
        return None


class ActionError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message
