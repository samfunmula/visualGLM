from typing import Optional
from aiohttp import ClientSession
import base64

async def fetch_image_base64(url: str) -> Optional[str]:
    try:
        async with ClientSession() as session:
            async with await session.get(url) as res:
                if res.status != 200:
                    return None
                img_byte = await res.read()
                img_base64 = base64.b64encode(img_byte).decode('utf-8')
                return img_base64
    except:
        return None
