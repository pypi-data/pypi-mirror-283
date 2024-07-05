class S3Config:
	def __init__(self, access_key: str,
							secret_key: str,
							endpoint_url: str,
							bucket_name: str):
		self.access_key = access_key
		self.secret_key = secret_key
		self.endpoint_url = endpoint_url
		self.bucket_name = bucket_name

class Config:
	def __init__(self, database: S3Config,
							traceback_time: bool = True,
							traceback_detailed: bool = False):
		"""Select the parameters (Fields) that are required"""
		self.database = database
		self.traceback_time = traceback_time
		self.traceback_detailed = traceback_detailed
