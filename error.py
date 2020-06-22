from flask import jsonify, make_response

class CustomError(Exception):
	def __init__(self, error, msg=None, status=None, exception=None):
		self.error = error
		self.msg = msg
		self.status = status
		self.exception = exception

	def __str__(self):
		if self.exception is not None:
			return "[exception]\n{}\n[{}:{}]:{}".format(self.exception, self.status, self.error, self.msg)
		else:
			return "[{}:{}]:{}".format(self.status, self.error, self.msg)

	def to_jsonify(self):
		return jsonify(error=self.error, msg=self.msg)

	def to_response(self):
		return make_response(self.to_jsonify(), self.status)