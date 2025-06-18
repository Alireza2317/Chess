def colored_str(text: str, color: str):
	"""
	supported colors:
	red, green, yellow, blue, magenta, cyan
	"""
	if color in ('red', 'r'):
		start = '\033[91m'
	elif color in ('green', 'g'):
		start = '\033[92m'
	elif color in ('yellow', 'y'):
		start = '\033[93m'
	elif color in ('blue', 'b'):
		start = '\033[94m'
	elif color in ('magenta', 'm'):
		start = '\033[95m'
	elif color in ('cyan', 'c'):
		start = '\033[96m'


	return start + text + '\033[0m'