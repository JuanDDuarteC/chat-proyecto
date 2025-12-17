from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()

clients = []

@app.get("/")
def root():
    return {"status": "ok"}

@app.websocket("/chat")
async def chat(ws: WebSocket):
    await ws.accept()
    clients.append(ws)
    try:
        while True:
            msg = await ws.receive_text()
            for c in clients:
                if c != ws:
                    await c.send_text(msg)
    except WebSocketDisconnect:
        clients.remove(ws)
