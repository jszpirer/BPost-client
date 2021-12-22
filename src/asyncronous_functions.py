import asyncio


async def ainput(prompt_message):
    """Modified input function that waits for the user, adapted for the use of input with coroutines"""
    loop = asyncio.get_event_loop()
    content = await loop.run_in_executor(None, input, prompt_message)
    return content
