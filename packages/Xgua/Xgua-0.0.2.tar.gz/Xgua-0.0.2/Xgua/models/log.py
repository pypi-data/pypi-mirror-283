from dataclasses import dataclass
from datetime import datetime

@dataclass()
class Log:
	id: int
	traceback: str
	traceback_detail: str
	timestamp: datetime