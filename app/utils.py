import os
import json
import logging
import importlib.util


def load_class_and_initialize(key, value):
    """
    Method name: load_class_and_initialize
    Description: load class locate in actions folder and initialize it
    @param key: action key - file and class name
    @param value: action value - parameter to pass to action's constructor
    @return: object of action class
    """
    try:
        # create path to python file
        path_to_module = os.path.join('.', 'actions', f'{key}.py')

        # load module
        spec = importlib.util.spec_from_file_location(key, path_to_module)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        # get class from module
        class_ = getattr(module, key)

        # if object accepts 1 parameter, pass value to constructor
        if len(class_.__init__.__code__.co_varnames) == 2:
            new_object = class_(value)
        else:
            new_object = class_()

        return new_object
    except Exception as e:
        print(e)
        return None


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
