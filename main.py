from fastapi import FastAPI, Request, WebSocket
from fastapi.responses import HTMLResponse
import subprocess
import asyncio
import os

from threading import Thread
from queue import Queue, Empty

os.environ['LD_LIBRARY_PATH'] = '/engines/maia/lib:' + os.environ.get('LD_LIBRARY_PATH', '')

user_playing = {
    'total': 0,
    'stockfish': 0,
    'trollfish': 0,
    'rodent': 0,
    'patricia': 0,
    'maia': 0
}

def enqueue_output(out, queue):
    for line in iter(out.readline, b''):
        queue.put(line)
    out.close()

class EngineChess:
    def __init__(self, path_engine):
        self.path_engine = path_engine
        self._stockfish = subprocess.Popen(
            path_engine,
            universal_newlines=True,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        self.queueOutput = Queue()
        self.thread = Thread(target=enqueue_output, args=(self._stockfish.stdout, self.queueOutput))
        self.thread.daemon = True # thread dies with the program
        self.thread.start()

        self._has_quit_command_been_sent = False
        self._debug_view = True

    def _put(self, command):
        if not self._stockfish.stdin:
            raise BrokenPipeError()
        if self._stockfish.poll() is None and not self._has_quit_command_been_sent:
            self._stockfish.stdin.write(f"{command}\n")
            self._stockfish.stdin.flush()
            if command == "quit":
                self._has_quit_command_been_sent = True

    def _read_line(self) -> str:
        if not self._stockfish.stdout:
            raise BrokenPipeError()
        if self._stockfish.poll() is not None:
            raise StockfishException("The Stockfish process has crashed")

        try:
            line = self.queueOutput.get_nowait() # or q.get(timeout=.1)
        except Empty:
            return ""

        if self._debug_view:
            print(f"Engine {self.path_engine[0]}:", line.strip())
        return line.strip()

    def _is_ready(self) -> None:
        self._put("isready")
        while self._read_line() != "readyok":
            pass

    def put(self, cmd):
        return self._put(cmd)

    def read_line(self) -> str:
        return self._read_line()

app = FastAPI()

# WebSocket endpoints
@app.websocket("/stockfish-{version}")
async def websocket_endpoint(websocket: WebSocket, version: str):
    await websocket.accept()

    user_playing['total'] += 1
    user_playing['stockfish'] += 1

    stockfish = EngineChess([f"./engines/stockfish/stockfish-{version}-uci"])

    async def read_from_socket(websocket: WebSocket):
        async for data in websocket.iter_text():
            print(f"Stockfish Client: {data}")
            stockfish.put(data)

    asyncio.create_task(read_from_socket(websocket))

    try:
        while True:
            while True:
                res = stockfish.read_line()
                if res:
                    await websocket.send_text(f"{res}")
                else:
                    break
            await asyncio.sleep(0.1)
    finally:
        user_playing['total'] -= 1
        user_playing['stockfish'] -= 1

@app.websocket("/maia-{elo}")
async def websocket_endpoint(websocket: WebSocket, elo: str):
    await websocket.accept()

    user_playing['total'] += 1
    user_playing['maia'] += 1

    stockfish = EngineChess([f"./engines/maia/maia-{elo}/lc0", "--backend=trivial"])
    
    async def read_from_socket(websocket: WebSocket):
        async for data in websocket.iter_text():
            print(f"Maia Client: {data}")
            stockfish.put(data)

    asyncio.create_task(read_from_socket(websocket))

    try:
        while True:
            while True:
                res = stockfish.read_line()
                if res:
                    await websocket.send_text(f"{res}")
                else:
                    break
            await asyncio.sleep(0.1)
    finally:
        user_playing['total'] -= 1
        user_playing['maia'] -= 1


@app.websocket("/rodent3-{personality}")
async def websocket_endpoint(websocket: WebSocket, personality: str):
    await websocket.accept()

    user_playing['total'] += 1
    user_playing['rodent'] += 1

    stockfish = EngineChess([f"./engines/RodentIII/rodentIII-debug"])

    await asyncio.sleep(1)
    
    stockfish.put(f"setoption name PersonalityFile value {personality}.txt")
    
    async def read_from_socket(websocket: WebSocket):
        async for data in websocket.iter_text():
            print(f"Rodent Client: {data}")
            stockfish.put(data)

    asyncio.create_task(read_from_socket(websocket))

    try:
        while True:
            while True:
                res = stockfish.read_line()
                if res:
                    await websocket.send_text(f"{res}")
                else:
                    break
            await asyncio.sleep(0.1)
    finally:
        user_playing['total'] -= 1
        user_playing['rodent'] -= 1


@app.websocket("/patricia-{elo}")
async def websocket_endpoint(websocket: WebSocket, elo: str):
    await websocket.accept()

    user_playing['total'] += 1
    user_playing['patricia'] += 1

    stockfish = EngineChess([f"./engines/Patricia/patricia"])
    
    await asyncio.sleep(0.5)

    stockfish.put(f"setoption name UCI_Elo value {elo}")
    stockfish.put("setoption name MultiPV value 3")
    
    async def read_from_socket(websocket: WebSocket):
        async for data in websocket.iter_text():
            print(f"Patricia Client: {data}")
            stockfish.put(data)

    asyncio.create_task(read_from_socket(websocket))

    try:
        while True:
            while True:
                res = stockfish.read_line()
                if res:
                    await websocket.send_text(f"{res}")
                else:
                    break
            await asyncio.sleep(0.1)
    finally:
        user_playing['total'] -= 1
        user_playing['patricia'] -= 1


@app.get("/")
async def root(request: Request):
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Users playing now</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background-color: #1f1f1f;
                color: #f0f0f0;
                margin: 0;
                padding: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                text-align: center;
            }
            .container {
                background-color: #2d2d2d;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 0 20px rgba(0, 0, 0, 0.2);
                max-width: 400px;
                width: 100%;
                margin: 20px;
            }
            h1 {
                color: #f0f0f0;
                font-size: 2.5rem;
                margin-bottom: 20px;
            }
            .stat {
                margin-bottom: 10px;
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 10px;
                border-bottom: 1px solid #444;
            }
            .stat:last-child {
                border-bottom: none;
            }
            .stat label {
                font-weight: bold;
                font-size: 1.2rem;
            }
            .stat span {
                font-size: 1.2rem;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Currently playing users</h1>
            <div class="stat">
                <label>Total Users:</label>
                <span id="total-users">""" + str(user_playing['total']) + """</span>
            </div>
            <div class="stat">
                <label>Stockfish Users:</label>
                <span id="stockfish-users">""" + str(user_playing['stockfish']) + """</span>
            </div>
            <div class="stat">
                <label>Rodent-III Users:</label>
                <span id="rodent3-users">""" + str(user_playing['rodent']) + """</span>
            </div>
            <div class="stat">
                <label>Patricia Users:</label>
                <span id="patricia-users">""" + str(user_playing['patricia']) + """</span>
            </div>
            <div class="stat">
                <label>Maia Users:</label>
                <span id="maia-users">""" + str(user_playing['maia']) + """</span>
            </div>
        </div>
    </body>
    </html>
    """

    return HTMLResponse(content=html_content)