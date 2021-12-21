import asyncio


async def ainput(prompt_message):
    loop = asyncio.get_event_loop()
    content = await loop.run_in_executor(None, input, prompt_message)
    return content
