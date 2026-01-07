import asyncio
from bot.services.fallback_api import generate_fallback_image
from bot.services.stability_api import generate_image

async def generate_image_for_session(prompt: str, is_vip: bool) -> str:
    generator = generate_image if is_vip else generate_fallback_image
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, generator, prompt)
