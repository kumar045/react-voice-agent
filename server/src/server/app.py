import uvicorn
import os
from starlette.applications import Starlette
from starlette.responses import HTMLResponse
from starlette.routing import Route, WebSocketRoute
from starlette.staticfiles import StaticFiles
from starlette.websockets import WebSocket
from langchain_openai_voice import OpenAIVoiceReactAgent
from server.utils import websocket_stream
from server.prompt import INSTRUCTIONS
from server.tools import TOOLS

async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    browser_receive_stream = websocket_stream(websocket)

    agent = OpenAIVoiceReactAgent(
        api_key=os.getenv("OPENAI_API_KEY"),
        model="gpt-4o-realtime-preview",
        tools=TOOLS,
        instructions=INSTRUCTIONS,
    )

    await agent.aconnect(browser_receive_stream, websocket.send_text)

async def homepage(request):
    with open("src/server/static/index.html") as f:
        html = f.read()
        return HTMLResponse(html)

# Define routes
routes = [
    Route("/", homepage),
    WebSocketRoute("/ws", websocket_endpoint),
]

# Create the app
app = Starlette(debug=True, routes=routes)

# Mount static files under a specific path to avoid conflicts
app.mount("/static", StaticFiles(directory="src/server/static"), name="static")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3000)
