#!/usr/bin/env python3

import os
from fastapi import FastAPI, Request, Form, Query, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from io import BytesIO
from olp.configs import OPTIONS, DOMAIN
from olp import __version__ as VERSION
from olp import apis

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

@app.post("/checkout")
async def checkout(name: str = Form(...), item: str = Form(...), filename: str = Form(...), price: str = Form(...)):
    try:
        checkout_session = apis.stripe_create_payment(DOMAIN, name, price, item, filename)
        return RedirectResponse(checkout_session.url, status_code=303)
    except Exception as e:
        return {"error": str(e)}

@app.get("/success")
async def success(session_id: str = Query(...)):
    try:
        tx = apis.stripe_fulfill(session_id)
        item, filename = tx.metadata.get('item'), tx.metadata.get('filename')
        # Return PDF as downloadable file
        return StreamingResponse(
            content=apis.download_book(item, filename),
            media_type='application/pdf',
            headers={
                "Content-Disposition":
                f"attachment; filename={filename}"
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("olp.app:app", **OPTIONS)
