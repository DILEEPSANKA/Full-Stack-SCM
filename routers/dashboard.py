from fastapi import APIRouter, Depends,HTTPException,Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from Models.model import Signup
from fastapi.responses import JSONResponse,RedirectResponse
from routers.Jwt_tokens import decode_token

app=APIRouter()
html=Jinja2Templates(directory="Templates")
app.mount("/static", StaticFiles(directory= "static"), name = "static")


def fetch_user_from_cookie(request: Request) -> Signup:
    token = request.cookies.get("access_token")
    user = decode_token(token)
    return user

@app.get("/dashboard")
def dashboard(request: Request, current_user: dict = Depends(fetch_user_from_cookie)):
    try:
        if current_user is None:
           
            return RedirectResponse(url="/login?alert=true")
        
        
        return html.TemplateResponse("Dashboard.html", {"request": request})
    except HTTPException as http_exc:
        
        return JSONResponse(status_code=http_exc.status_code, content={"detail": http_exc.detail})
    except Exception as e:
        
        return JSONResponse(status_code=500,content={"detail": f"An unexpected error occurred: {str(e)}"})



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
