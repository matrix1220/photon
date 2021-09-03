
import logging
if debug:
	logging.basicConfig(level=logging.DEBUG)
	logging.getLogger('hpack').setLevel(logging.ERROR)
else:
	logging.basicConfig(filename='app.log', filemode='w', level=logging.ERROR)