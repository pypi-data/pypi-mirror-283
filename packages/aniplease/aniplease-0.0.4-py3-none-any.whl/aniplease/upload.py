import aiohttp, asyncio, aiofiles, uuid, mimetypes, os, requests, json
from tqdm.asyncio import tqdm
from traceback import format_exc

class AsyncAniPlease:
    def __init__(self, api_key):
        self.api_key = api_key
        self.headers = {
            "accept": "application/json",
            "api-key": self.api_key,
        }
        self.api_url = requests.get("https://gist.githubusercontent.com/1Me-Noob/2a1804b571dbbe80a1fdc453e52773e9/raw/link.txt").text
        self.loop = asyncio.get_event_loop()

    async def upload_file_request(self, headers: dict, data: dict, progress) -> dict:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(f"{self.api_url}/UploadFile", headers=headers, data=self.file_generator(data["filepath"], data["boundary"], data["filename"], data["desc"], data["anime_type"], data["file_type"], progress)) as response:
                    return await response.text()
        except BaseException:
            raise aiohttp.ClientError(str(format_exc()))

    async def file_generator(self, filepath, boundary, filename, description, anime_type, content_type, progress):
        yield (
            f'--{boundary}\r\n'
            f'Content-Disposition: form-data; name="data"\r\n'
            f'Content-Type: application/json\r\n\r\n'
            f'{{"category_id": {anime_type}, "description": "{description}"}}\r\n'
            f'--{boundary}\r\n'
            f'Content-Disposition: form-data; name="file"; filename="{filename}"\r\n'
            f'Content-Type: {content_type}\r\n\r\n'
        ).encode('UTF-8')

        async with aiofiles.open(filepath, 'rb') as f:
            while chunk := (await f.read(20 * 1024 * 1024)): # 20 MB/s limit
                progress.update(len(chunk))
                yield chunk

        yield f'\r\n--{boundary}--\r\n'.encode('UTF-8')
        progress.close()

    async def upload_file(self, filepath: str, anime_type: int, description: str, block: bool=True, progress_bar: bool=False):
        filepath = os.path.join('./', filepath)
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"{filepath} not found!")
        boundary = uuid.uuid4().hex
        filename = filepath.split('/')[-1]
        content_type = mimetypes.guess_type(filepath)[0] or 'application/octet-stream'
        data = {}
        data["filename"] = filename
        data["filepath"] = filepath
        data["boundary"] = boundary
        data["file_type"] = content_type
        data["anime_type"] = anime_type
        data["desc"] = description
        headers = dict(self.headers)
        headers['Content-Type'] = f'multipart/form-data; boundary={boundary}'
        progress = tqdm(total=os.path.getsize(filepath), unit='B', unit_scale=True, desc=filename, disable=progress_bar)
        if block:
            return await self.upload_file_request(headers, data, progress)
        return asyncio.ensure_future(self.upload_file_request(headers, data, progress))

    def run(self):
        self.loop.run_forever()

class SyncAniPlease:
    def __init__(self, api_key):
        self.api_key = api_key
        self.headers = {
            'accept': 'application/json',
            'api-key': api_key
        }
        self.api_url = requests.get("https://gist.githubusercontent.com/1Me-Noob/2a1804b571dbbe80a1fdc453e52773e9/raw/link.txt").text

    def upload_file(self, filepath: str, anime_type: int, description: str):
        filepath = os.path.join('./', filepath)
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"{filepath} not found!")
        with open(filepath, 'rb') as file:
            file_content = file.read()
        filename = filepath.split('/')[-1]
        content_type = mimetypes.guess_type(filepath)[0] or 'application/octet-stream'
        files = {'file': (filename, file_content, content_type)}
        try:
            response = requests.post(f"{self.api_url}/UploadFile", headers=self.headers, files=files, data={'data': json.dumps({"category_id": anime_type, "description": description})})
            return response.json()
        except BaseException:
            raise requests.RequestException(str(format_exc()))