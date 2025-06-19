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
        "appname": "OpenLibrary.press",
    })

@app.post("/checkout")
async def checkout(
        request: Request,
        name: str = Form(...),
        olid: str = Form(...),
        item: str = Form(...),
        price: str = Form(...),
):
    callback_url = request.headers.get("X-Lenny-Callback")

    try:
        checkout_session = apis.stripe_create_payment(
            DOMAIN, name, price, item, olid,
            callback_url=callback_url
        )
        return RedirectResponse(checkout_session.url, status_code=303)
    except Exception as e:
        return {"error": str(e)}

@app.get("/success")
async def success(session_id: str = Query(...)):
    try:
        tx = apis.stripe_fulfill(session_id)
        item = tx.metadata.get('item')
        olid = tx.metadata.get('olid')
        callback_url = tx.metadata.get('callback_url')

        epub = apis.download_book(item)

        if callback_url and callback_url.startswith('http'):
            apis.Lenny.upload(callback_url, olid, epub)
            return RedirectResponse(apis.Lenny.redirect(callback_url), status_code=303)
        
        # Return PDF as downloadable file
        return StreamingResponse(
            content=epub,
            media_type='application/epub+zip',
            headers={
                "Content-Disposition":
                f"attachment; filename={olid}.epub"
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("olp.app:app", **OPTIONS)
