from password_strength import PasswordPolicy
from models import SecretKey

policy = PasswordPolicy.from_names(strength=(0.8, 10))

def entropy_filter(keys: list):
	secret_keys = []

	for key in keys:
		if len(policy.test(key.content)) == 0:
			secret_keys.append(key)
	
	return secret_keys

import sys
sys.modules[__name__] = entropy_filter