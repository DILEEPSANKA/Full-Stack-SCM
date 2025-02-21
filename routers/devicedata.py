from fastapi import Request, APIRouter, Depends,HTTPException
from fastapi.responses import JSONResponse, RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from config.config import Device_Data_Stream
from routers.dashboard import fetch_user_from_cookie

app = APIRouter()

html = Jinja2Templates(directory="Templates")

@app.get("/devicedata", response_class=HTMLResponse)
async def device_data_stream(request: Request, current_user: dict = Depends(fetch_user_from_cookie)):
    if not current_user:
        return RedirectResponse(url="/login?alert=true")
    
    user_role = current_user.get("role", "user")
    show_table = False
    device_data = []

    try:
        if user_role == "admin":
            device_data = list(Device_Data_Stream.find({}, {"_id": 0}))  
            show_table = True
        
        return html.TemplateResponse("Devicedata.html", {"request": request,"role": user_role,"device_data": device_data,"show_table": show_table})
    except Exception as e:
        return html.TemplateResponse("Devicedata.html", {"request": request,"role": user_role,"device_data": [],"show_table": False,"error_message": f"Error: {str(e)}"})

@app.post("/devicedata-fetch")
async def fetch_device_data(request: Request):
    try:
        data = await request.json()
        device_id = data.get("Device_ID")
        
        if device_id:
            device_data = list(Device_Data_Stream.find({'Device_Id': int(device_id)}, {'_id': 0}))
            if device_data:
                return JSONResponse(content={"device_data": device_data}, status_code=200)
            else:
                return JSONResponse(content={"error_message": "Device data not found."}, status_code=400)
        else:
            return JSONResponse(content={"error_message": "Device ID is required."}, status_code=400)
    except Exception as e:
        return JSONResponse(content={"error_message": str(e)}, status_code=500)
    

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
