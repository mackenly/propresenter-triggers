import json
import logging
import requests


class Request:
    """
    Class name: Request
    Class description: Send a request to a URL
    Example value:
    {
        "url": "https://www.google.com",
        "method": "GET",
        "headers": {
            "Content-Type": "application/json"
        },
        "body": {
            "key": "value"
        }
    }
    """

    def __init__(self, value):
        """
        Method name: __init__
        Method description: Constructor for Request class
        @param value: value used to define request
        """
        if value is None:
            logging.error('Value is required for Request action')
            return
        try:
            self.value = value
            self.url = value.get('url') or ''
            self.method = value.get('method') or 'GET'
            self.headers = value.get('headers') or {}
            self.body = value.get('body') or {}
        except Exception as e:
            logging.error('Value must be a valid JSON object for Request action ' + str(e))
            return

    def run(self):
        """
        Method name: run
        Method description: Runner method that executes the request
        """
        try:
            response = requests.request(
                method=self.method,
                url=self.url,
                headers=self.headers,
                data=self.body
            )
            logging.info("Request response: " + json.loads(response.text))
            return
        except Exception as e:
            logging.error('Request action failed: ' + str(e))
            return
