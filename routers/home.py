from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles



app=APIRouter()
html=Jinja2Templates(directory="Templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def home(request: Request):
    return html.TemplateResponse("Home.html", {"request": request})
