from contextlib import asynccontextmanager
from aiobotocore.session import get_session

class S3Client:
	def __init__(self, access_key: str, secret_key: str, endpoint_url: str, bucket_name: str):
		self.config = {
			"aws_access_key_id": access_key,
			"aws_secret_access_key": secret_key,
			"endpoint_url": endpoint_url,
		}
		self.bucket_name = bucket_name
		self.session = get_session()

	@asynccontextmanager
	async def get_client(self):
		async with await self._create_client() as client:
			try:
				yield client
			finally:
				await self._close_client(client)

	async def _create_client(self):
		return self.session.create_client("s3", **self.config)

	async def _close_client(self, client):
		await client.close()

	async def upload_file(self, data: dict):
		async with self.get_client() as client:
			await client.put_object(Bucket=self.bucket_name, Key=data['file']['full_name'], Body=str(data['model']))
			return True
