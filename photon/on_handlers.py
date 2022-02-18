class OnHandlers:
    def __init__(self, bot):
        bot.handlers.append(self._handle)
        self.handlers = {}

    async def _handle(self, request):
        for key, value in request.update.items():
            if key=='update_id': continue
            if key not in self.handlers: return
            return await self.handlers[key](request, value)

    def on(self, key):
        def func(handler):
            self.handlers[key] = handler
        return func