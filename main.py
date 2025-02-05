from json import loads
from time import sleep
from json import dumps
from websocket import WebSocket
from concurrent.futures import ThreadPoolExecutor

guild_id = input("Guild ID: ")
chid = input("Channel ID: ")
tokenlist = open("tokens.txt").read().splitlines()
executor = ThreadPoolExecutor(max_workers=int(1000000))

def run(token):
    ws = WebSocket()
    ws.connect("wss://gateway.discord.gg/?v=8&encoding=json")
    hello = loads(ws.recv())
    heartbeat_interval = hello['d']['heartbeat_interval']

    # اتصال به WebSocket با توکن
    ws.send(dumps({"op": 2, "d": {"token": token, "properties": {"$os": "windows", "$browser": "Discord", "$device": "desktop"}}}))

    # ارسال تنظیمات مربوط به گیلد و چنل بدون میوت و دیفنس
    ws.send(dumps({"op": 4, "d": {"guild_id": guild_id, "channel_id": chid}}))

    # تغییر منطقه به سنگاپور
    ws.send(dumps({"op": 18, "d": {"type": "guild", "guild_id": guild_id, "channel_id": chid, "preferred_region": "singapore"}}))

    # ارسال وضعیت بازی (در حال بازی Minecraft)
    activity = {
        "name": "Minecraft", # نام بازی
        "type": 0,  # نوع فعالیت (0 یعنی بازی)
        "application_id": 0,  # این برای بازی‌های سفارشی استفاده می‌شود که در اینجا نیازی به آن نیست
        "state": "تو سرور Godrat.ir",  # متن پایین (سرور)
        "start_timestamp": int(time.time()),  # شروع بازی
        "details": "در حال بازی Minecraft"  # جزئیات بالای بازی
    }

    ws.send(dumps({
        "op": 3,
        "d": {
            "since": None,
            "game": activity
        }
    }))

    while True:
        sleep(heartbeat_interval / 1000)
        try:
            ws.send(dumps({"op": 1, "d": None}))
        except Exception:
            break

i = 0
for token in tokenlist:
    executor.submit(run, token)
    i += 1
    print(f"connected ws: {i}")
