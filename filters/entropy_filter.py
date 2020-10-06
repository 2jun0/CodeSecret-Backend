from password_strength import PasswordStats
from models import SecretKey

threshold_value = 0.8

def entropy_filter(keys: list):
	secret_keys = []

	for key in keys:
		entropy = PasswordStats(key.content).strength()
		if entropy > threshold_value:
			secret_keys.append(key)
	
	return secret_keys

import sys
sys.modules[__name__] = entropy_filter