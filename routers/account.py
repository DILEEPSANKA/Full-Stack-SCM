from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse, JSONResponse
from routers.dashboard import fetch_user_from_cookie


app = APIRouter()
html = Jinja2Templates(directory="Templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/account")
async def account(request: Request, user: dict = Depends(fetch_user_from_cookie)):
    try:
        if not user:
            return RedirectResponse(url="/login?alert=true")

       
        username = user.get("user") 
        email = user.get("email")

        return html.TemplateResponse(
            "Account.html", {"request": request, "username": username, "email": email}
        )
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        return JSONResponse(
            content={"error": "An unexpected error occurred. Please try again later."},
            status_code=500,
        )
    

COOKIE_NAME = "access_token"  
@app.post("/logout")
async def logout(request: Request):
    try:
       
        response = JSONResponse(content={"message": "Logged out"})
        response.delete_cookie(COOKIE_NAME)  
        return response 

    except KeyError as exc:
        raise HTTPException(status_code=400, detail="Cookie name not found.") from exc
    except Exception as exception:
        raise HTTPException(status_code=500, detail=str(exception)) from exception
