

from photon.client.methods import sendMessage

class Context:
    def __init__(self, chat_id, message):
        self.chat_id = chat_id
        self.message = message
    
    def transform(self, message, keyboard=None):
        kwargs = {}
        if keyboard: kwargs['keyboard'] = keyboard
        return sendMessage(message, self.chat_id, **kwargs )


class ContextExtractor:
    def __init__(self, ):
        pass
    
    def extract(self, update):
        return _extract_context(update)

def _extract_context(update):
    if "message" in update:
        context = Context(
            update["message"]["chat"]["id"],
            update["message"]["text"],
        )
        return context
