#!/usr/bin/env python3

import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from olp.configs import OPTIONS
from olp import __version__ as VERSION

app = FastAPI(
    title="Openlibrary.press",
    description="The public good publishing platform.",
    version=VERSION,
)

def resolve(path):
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), path)

app.mount("/static", StaticFiles(directory=resolve("static")), name="static")

templates = Jinja2Templates(directory=resolve("templates"))

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "appname": "OpenLibrary.press"
    })


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("olp.app:app", **OPTIONS)
