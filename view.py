from sanic.log import logger
from sanic import Sanic

from feed import Feed

app = Sanic(__name__)



@app.websocket('/ws/<feed_name:[A-z][A-z0-9]+>')
async def feed(request, ws, feed_name):
    logger.info("Incoming WS request")
    print(feed_name)
    feed, is_existing = await Feed.get(feed_name)

    if not is_existing:
        request.app.add_task(feed.receiver())
    client = await feed.register(ws)

    try:
        await client.receiver()
    finally:
        await feed.unregister(client)



if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=int(8001),
        workers=int(4),
        debug=bool(int(1)),
        access_log=bool(int(1)),
        auto_reload=bool(int(1)),
    )