import asyncio


def get_best_event_loop():
    try:
        import uvloop
    except ImportError:
        return asyncio.get_event_loop()
    else:
        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    return asyncio.get_event_loop()
