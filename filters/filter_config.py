API_REGEX = {
	'Twitter':'[1-9][0-9]+-[0-9a-zA-Z]{40}',
	'Google':'AIza[0-9A-Za-z-_]{35}',
	'Square':'sqOatp-[0-9A-Za-z-_]{22}',
	'GCP':'[A-Za-z0-9_]{21}--[A-Za-z0-9_]{8}',
	'Heroku':'[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}',
	'Slack':'xox.-[0-9]{12}-[0-9]{12}-[0-9]{12}-[a-zA-Z0-9]{32}',
	'Heroku API Key':'[h|H][e|E][r|R][o|O][k|K][u|U].{0,30}[0-9A-F]{8}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{12}',
	'Paypal Braintree':'access_token,production$[0-9a-z]{161[0-9a,]{32}',
	'Twilio':'55[0-9a-fA-F]{32}',
	'MailGun':'key-[0-9a-zA-Z]{32}',
	'MailChimp':'[0-9a-f]{32}-us[0-9]{1,2}',
	'Picatic':'sk_live_[0-9a-z]{32}',
	'AWS':'AKIA[0-9A-Z]{16}',
}

FILE_FILTER = {
	'IGNORE_NAME' : ['^__.*__','^\..*'],
	'SELECT_NAME' : ['.gitignore'],
	'ALLOW_FILE_EXTENSIONS' : ['py', 'js', 'java', 'c',	'cpp'],
}