# coding: utf-8

import ui
from scene import *

class MainView (ui.View):
	def __init__(self):
		pass

v = ui.load_view('main')
if ui.get_screen_size()[1] >= 768:
	# iPad
	v.present('popover')
else:
	# iPhone
	v.present(orientations=['portrait'])

