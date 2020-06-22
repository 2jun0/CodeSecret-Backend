from password_strength import PasswordStats
from models import SecretKey

threshold_value = 0.8

def entropy_filter(keys: list):
	result_keys = []

	for key in keys:
		entropy = PasswordStats(key.content)
		if entropy > threshold_value:
			result_keys.append(key)
	
	return result_keys

import sys
sys.modules[__name__] = entropy_filter