import requests
from app.actions.Action import Action
from app.utils import ActionError


class Discord(Action):
    """
    Class name: Discord
    Class description: Send a message to a Discord channel via webhook
    Example value:
    {
        "webhook_url": "https://discord.com/api/webhooks/00000000000000000/er3t5v4635g4rrt8",
        "message": "Hey <@00000000000000000>, this is a test message!"
    },
    """

    def __init__(self, value):
        """
        Method name: __init__
        Method description: Constructor for Discord class
        @param value: value used to define Discord message
        """
        if value is None:
            raise ActionError("Value is required for Discord action")
        try:
            self.value = value
            self.webhook_url = value.get('webhook_url') or ''
            self.message = value.get('message') or ''
        except Exception as e:
            raise ActionError("Value must be a valid JSON object for Discord action " + str(e))

    def run(self):
        try:
            requests.post(
                url=self.webhook_url,
                json={"content": self.message}
            )
            return
        except Exception as e:
            raise ActionError("Action failed: " + str(e))
