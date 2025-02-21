from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse,JSONResponse
from config.config import Shipments
from routers.dashboard import fetch_user_from_cookie

app = APIRouter()
html = Jinja2Templates(directory="Templates")
app.mount("/static", StaticFiles(directory="static"), name="static")



@app.get("/myshipment")
def my_shipments(request: Request, current_user: dict = Depends(fetch_user_from_cookie)):
    
    if current_user is None:
        return RedirectResponse(url="/login?alert=true", status_code=302)

    try:
        role = current_user.get("role", "user") 
        email = current_user.get("email")

        if role == "admin":
            
            shipments = list(Shipments.find({},  {"_id": 0},))
        else:
           
            if not email:
                raise HTTPException(status_code=400, detail="User email not found.")
            shipments = list(
                Shipments.find({"email": email}, {"_id": 0},))

       
        return html.TemplateResponse("Myshipment.html",{"request": request,"shipments": shipments,"role": role,"error_message": None if shipments else "No shipments found.",},)

    except Exception as e:
      
        print(f"Error fetching shipments: {e}")
        return html.TemplateResponse(
            "Myshipment.html",{"request": request,"shipments": [],"role": current_user.get("role", "user"),"error_message": "An error occurred while fetching shipments.",},)

COOKIE_NAME = "access_token"
@app.post("/logout")
async def logout(request: Request):
    
    try:
        response = JSONResponse(content={"message": "Logged out"})
        response.delete_cookie(COOKIE_NAME, path="/", domain=None)
        return response

    except KeyError as exc:
        raise HTTPException(status_code=400, detail="Cookie name not found.") from exc

    except Exception as exception:
        raise HTTPException(status_code=500, detail=str(exception)) from exception
