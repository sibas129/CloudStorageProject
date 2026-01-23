import aiohttp


class AiohttpNamespace:
    @staticmethod
    async def get_request(url: str, headers: dict = None, get_text: bool = False) -> dict:
        async with aiohttp.ClientSession() as session:
            async with session.get(url=url, headers=headers) as response:
                if response.status != 200:
                    raise NotImplementedError("unlucky network request")
                if get_text:
                    return await response.text()
                return await response.json()
                

    @staticmethod
    async def post_request(url: str, json: dict = None, headers: dict = None) -> dict:
        async with aiohttp.ClientSession() as session:
            async with session.post(url=url, json=json, headers=headers) as response:
                if response.status != 200:
                    raise NotImplementedError("unlucky network request")
                return await response.json()

    @staticmethod
    async def put_request(url: str, json: dict = None, headers: dict = None) -> dict:
        async with aiohttp.ClientSession() as session:
            async with session.put(url=url, json=json, headers=headers) as response:
                if response.status != 200:
                    raise NotImplementedError("unlucky network request")
                return await response.json()

    @staticmethod
    async def patch_request(url: str, json: dict = None, headers: dict = None) -> dict:
        async with aiohttp.ClientSession() as session:
            async with session.patch(url=url, json=json, headers=headers) as response:
                if response.status != 200:
                    raise NotImplementedError("unlucky network request")
                return await response.json()

    @staticmethod
    async def delete_request(url: str, json: dict = None, headers: dict = None) -> dict:
        async with aiohttp.ClientSession() as session:
            async with session.delete(url=url, json=json, headers=headers) as response:
                if response.status != 200:
                    raise NotImplementedError("unlucky network request")
                return await response.json()
