import threading
import logging
import requests
import time
import json
import waitress
import wsgi
from app.utils import trigger_thread
from app.utils import import_config

# last slide uuid
last_slide_uuid = None

# last slide notes
config_file = import_config()

# retry count
retry_count = 0


def execute_triggers(triggers, is_current=True):
    """
    Method name: execute_triggers
    Description: execute triggers passed as parameter
    @param triggers: triggers to execute
    @param is_current: if True, execute only triggers with when_next = False or not present
    """
    for trigger in triggers:
        # print(trigger)
        try:
            trigger_type = trigger.get("type") or "action"
            trigger_key = trigger.get("key")
            trigger_value = trigger.get("value") or ""
            trigger_delay = trigger.get("delay") or 0
            trigger_then = trigger.get("then") or None
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
                # trigger_thread(trigger_key, trigger_value, trigger_delay, trigger_then)
                thread = threading.Thread(
                    target=trigger_thread,
                    args=(trigger_key, trigger_value, trigger_delay, trigger_then)
                )
                thread.start()
        except Exception as e:
            logging.error(f'Invalid trigger: {e}')
    return True


def process_triggers(data):
    """
    Method name: process_triggers
    Process triggers by comparing current slide uuid with last slide uuid,
    if they are different, process triggers from the notes of the current and next slide
    @param data: data from ProPresenter API
    """

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


def retry_checker(propresenter_api_url):
    global retry_count
    delay = 1
    retry_count += 1
    if retry_count > 10:
        delay = 5
    elif retry_count > 3:
        delay = 3
    logging.info(f'Retrying listener in {delay} second(s)')
    time.sleep(delay)
    check_for_slide_changes(propresenter_api_url)


def check_for_slide_changes(propresenter_api_url="http://localhost:1025"):
    if propresenter_api_url[-1] != "/":
        propresenter_api_url += "/"
    propresenter_api_url += "v1/status/slide?chunked=true"
    response = None
    try:
        response = requests.get(propresenter_api_url, headers={
            "accept": "application/json",
        }, stream=True)
    except Exception as e:
        logging.error("Error connecting to ProPresenter: " + str(e))
        retry_checker(propresenter_api_url)

    # reset retry count
    global retry_count
    if retry_count > 0:
        logging.info("ProPresenter API connection restored")
    retry_count = 0

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


def run_flask():
    """
    Method name: run_flask
    Description: run flask app using waitress to serve the API
    Default port is 1027
    """
    try:
        waitress.serve(wsgi.app, listen='*:1027')
    except Exception as e:
        logging.error("Error running API server")
        print(e)


if __name__ == "__main__":
    # Logging Config
    log_format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=log_format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    # Creating threads
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()
    checker_thread = threading.Thread(target=check_for_slide_changes(config_file.get('PROPRESENTER_API_URL')))

    # Starting threads
    checker_thread.start()

    # Wait until both threads finish
    flask_thread.join()
    checker_thread.join()
