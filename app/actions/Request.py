import json
import requests
from app.actions.Action import Action
from app.utils import ActionError


class Request(Action):
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
            raise ActionError('Value is required for Request action')
        try:
            self.value = value
            self.url = value.get('url') or ''
            self.method = value.get('method') or 'GET'
            self.headers = value.get('headers') or {}
            self.body = value.get('body') or {}
        except Exception as e:
            raise ActionError('Value must be a valid JSON object for Request action ' + str(e))

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
            raise ActionError("Request response: " + json.loads(response.text))
        except Exception as e:
            raise ActionError('Request action failed: ' + str(e))
