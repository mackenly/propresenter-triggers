import threading
import logging
import requests
import time
import json
import waitress
import wsgi
from app.utils import load_class_and_initialize

# last slide uuid
last_slide_uuid = None


def execute_triggers(triggers, is_current=True):
    for trigger in triggers:
        # print(trigger)
        try:
            trigger_type = trigger.get("type") or "action"
            trigger_key = trigger.get("key")
            trigger_value = trigger.get("value") or ""
            trigger_when_next = trigger.get("when_next") or False
            # if is_current is True and trigger_when_next is True, skip this trigger
            if is_current and trigger_when_next:
                continue
            # if is_current is False and trigger_when_next is False, skip this trigger
            if not is_current and not trigger_when_next:
                continue
            # if is_current is True and trigger_when_next is False, execute this trigger
            # if is_current is False and trigger_when_next is True, execute this trigger
            if trigger_type == "action":
                # create object of action's class
                new_object = load_class_and_initialize(trigger_key, trigger_value)
                # run the run method of the action's class
                new_object.run()
        except Exception as e:
            logging.error("Invalid trigger")
    return True


def process_triggers(data):
    """
    Sample data:
    {
      "current": {
        "text": "You are here\nworking in this place",
        "notes": "",
        "uuid": "4a9c32bf-d190-40d9-b010-5944eae87d13"
      },
      "next": {
        "text": "I worship You\nI worship You",
        "notes": "",
        "uuid": "dedf78ae-423c-45c7-8300-14fbca06d584"
      }
    }
    """

    global last_slide_uuid
    if data.get('current').get('uuid') == last_slide_uuid:
        return
    else:
        # get notes from current slide
        current_note_value = data.get('current').get('notes')
        next_note_value = data.get('next').get('notes')

        if current_note_value != "" and current_note_value is not None:
            try:
                note = json.loads(current_note_value)
            except Exception as e:
                logging.error("Invalid current note")
                return
            triggers = note.get("triggers")
            triggers_result = execute_triggers(triggers)
            if not triggers_result:
                logging.error("Error executing current triggers")

        if next_note_value != "" and next_note_value is not None:
            try:
                note = json.loads(next_note_value)
            except Exception as e:
                logging.error("Invalid next note")
                return
            triggers = note.get("triggers")
            triggers_result = execute_triggers(triggers, is_current=False)
            if not triggers_result:
                logging.error("Error executing next triggers")

        last_slide_uuid = data.get('current').get('uuid')


def retry_checker(propresenter_api_url="http://localhost:1025"):
    logging.info("Retrying listener in 1 second")
    time.sleep(1)
    check_for_changes(propresenter_api_url)


def check_for_changes(propresenter_api_url="http://localhost:1025"):
    if propresenter_api_url[-1] != "/":
        propresenter_api_url += "/"
    propresenter_api_url += "v1/status/slide?chunked=true"
    try:
        response = requests.get('http://localhost:1025/v1/status/slide?chunked=true', headers={
            "accept": "application/json",
        }, stream=True)
    except Exception as e:
        logging.error("Error connecting to ProPresenter")
        print(e)
        retry_checker(propresenter_api_url)

    if response.encoding is None:
        response.encoding = 'utf-8'

    data = ""

    try:
        for line in response.iter_lines(decode_unicode=True):
            if line:
                data += line
            else:
                # End of message
                try:
                    data = json.loads(data)
                    process_triggers(data)
                    data = ""
                except Exception as e:
                    logging.error("Error parsing ProPresenter API JSON")
                    data = ""
    except Exception as e:
        logging.error("ProPresenter API connection error")
        retry_checker(propresenter_api_url)


def import_config():
    try:
        with open("config.json") as f:
            return json.load(f)
    except Exception as e:
        logging.error("Error importing config file")
        return None


def run_flask():
    # Running waitress server to serve flask app
    waitress.serve(wsgi.app, listen='*:1027')


if __name__ == "__main__":
    config_file = import_config()

    # Logging Config
    log_format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=log_format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    # Creating threads
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()
    checker_thread = threading.Thread(target=check_for_changes(config_file.get('PROPRESENTER_API_URL')))

    # Starting threads
    checker_thread.start()

    # Wait until both threads finish
    flask_thread.join()
    checker_thread.join()
