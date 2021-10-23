class OnHandlers:
    def __init__(self, bot):
        bot.handlers.append(self._handle)
        self.handlers = {}

    async def _handle(self, ctx):
        print('test')
        for key, value in ctx.update.items():
            if key=='update_id': continue
            if key not in self.handlers: return
            return await self.handlers[key](value)

    def on(self, key):
        def func(handler):
            self.handlers[key] = handler
        return func