from utils.aiohttp_worker import AiohttpNamespace
from config import ETHERPAD_URL


class NotepadNamespace:
    @staticmethod
    async def create_page(name: str) -> None:
        await AiohttpNamespace.get_request(url=f"{ETHERPAD_URL}/p/{name}", get_text=True)

    @staticmethod
    async def get_page_content(name: str) -> str:
        return await AiohttpNamespace.get_request(
            url=f"{ETHERPAD_URL}/p/{name}/export/txt"
        )
