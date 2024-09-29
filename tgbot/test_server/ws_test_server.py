from aiohttp import web
import aiohttp


async def websocket_handler(request) -> web.WebSocketResponse:
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    print("Есть подключение")

    async for msg in ws:
        if msg.type == aiohttp.WSMsgType.TEXT:
            print(f"Запрос: {msg.data}")
            if msg.data == "close":
                await ws.close()
            else:
                await ws.send_str("<b>Ответ</b>\n" + msg.data)
        elif msg.type == aiohttp.WSMsgType.ERROR:
            print("ws connection closed with exception %s" % ws.exception())

    print("Подключение закрыто")

    return ws


app = web.Application()
app.add_routes([web.get("/", websocket_handler)])

if __name__ == "__main__":
    web.run_app(app)

# ws://127.0.0.1:8080
