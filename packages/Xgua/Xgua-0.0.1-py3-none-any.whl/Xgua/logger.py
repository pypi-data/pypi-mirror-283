from .config import Config
from .s3.client import S3Client
from .processing.upload import Upload
from .models.log import Log
from datetime import datetime
import traceback

class Logger:
	def __init__(self, config: Config) -> None:
		self.__config = config
		self.client = S3Client(config.database.access_key, config.database.secret_key, config.database.endpoint_url, config.database.bucket_name)
		self.upload = Upload()

	async def log(self, exception: Exception) -> None:
		log_id = self.upload.get_next_log_id()
		log = Log(
			id=log_id,
			traceback=exception,
			traceback_detail=traceback.format_exc() if self.__config.traceback_detailed else None,
			timestamp=datetime.now() if self.__config.traceback_time else None
		)

		data = self.upload.upload(log)
		if await self.client.upload_file(data):
			self.upload.update_old_id(log_id)