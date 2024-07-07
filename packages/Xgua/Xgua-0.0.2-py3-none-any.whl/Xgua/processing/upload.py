import os
from ..models.log import Log

class Upload:
	def __init__(self) -> None:
		self.prefix = "log"
		self.divisor = "_"
		self.type = ".json"
		self.old_id = self.get_old_id()

	def get_old_id(self) -> int:
		try:
			with open("s3_old_id.txt") as f:
				old_id = f.readline().strip()
				return int(old_id) if old_id.isdigit() else 0
		except FileNotFoundError:
			with open("s3_old_id.txt", "w") as f:
				return 0

	def update_old_id(self, _id: int) -> None:
		with open("s3_old_id.txt", "w") as f:
			f.write(str(_id))

	def get_next_log_id(self) -> int:
		return self.old_id + 1

	def upload(self, log: Log) -> dict:
		model = {
			"id": log.id,
			"traceback": log.traceback,
			"traceback_detail": log.traceback_detail,
			"timestamp": log.timestamp
		}
		file = {
			"id": log.id,
			"full_name": f"{self.prefix}{self.divisor}{log.id}{self.type}",
			"prefix": self.prefix,
			"type": self.type,
			"sep": self.divisor
		}
		return {"file": file, "model": model}
