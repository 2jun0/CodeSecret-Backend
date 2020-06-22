import re
from filters.filter_config import API_REGEX
from models import File, SecretKey

api_regex = re.compile('(%s)'%(')|('.join(API_REGEX.values())))

def patern_finder(file: File, content):
	matches = api_regex.finditer(content)
	keys = []

	y = 0
	temp_len = 0

	for m in matches:
		if m.group == '\n':
			y = y + 1
			temp_len = m.end()
			continue

		x = m.start() - temp_len
		keys.append(SecretKey(y, x, file.fullname, m.group()))
	
	return keys

import sys
sys.modules[__name__] = patern_finder