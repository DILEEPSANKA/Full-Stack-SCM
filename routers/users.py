from fastapi import APIRouter, Request, Depends, HTTPException, Body
from fastapi.responses import RedirectResponse, JSONResponse
from config.config import User_details
from routers.dashboard import fetch_user_from_cookie
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = APIRouter()
html = Jinja2Templates(directory="Templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/users")
def admin_page(request: Request, current_user: dict = Depends(fetch_user_from_cookie)):
    if current_user is None:
        return RedirectResponse(url="/login?alert=true")

    try:
        role = current_user.get("role", "user")  
        username = current_user.get("username", "User")

        if role == "admin":
            users = list(User_details.find({}, {"_id": 0}))  
        elif role == "user":
            return html.TemplateResponse("Users.html", {
                "request": request, 
                "user_details": [], 
                "error_message": "You are a normal user and do not have access to this page.",
                "role": role,
                "username": username
            })
        else:
            return RedirectResponse(url="/dashboard?alert=unauthorized")

        return html.TemplateResponse("Users.html", {
            "request": request, 
            "user_details": users,
            "role": role,
            "username": username
        })

    except Exception as e:
        return html.TemplateResponse("Users.html", {
            "request": request, 
            "user_details": [], 
            "error_message": str(e),
            "role": role,
            "username": username
        })

@app.put("/update_user")
async def update_user(
    request: Request,
    data: dict = Body(...), 
    current_user: dict = Depends(fetch_user_from_cookie)
):
    if current_user is None:
        return JSONResponse(status_code=400, content={"detail": "User not logged in."})

    try:
        role = current_user.get("role", "user")

        if role != "admin":
            return JSONResponse(status_code=403, content={"detail": "Unauthorized."})

        user = data.get("user")
        new_role = data.get("role")

        user_to_update = User_details.find_one({"user": user})

        if user_to_update:
            result = User_details.update_one({"user": user}, {"$set": {"role": new_role}})

            if result.matched_count > 0:
                return JSONResponse(status_code=200, content={"detail": "User updated successfully!"})
            else:
                return JSONResponse(status_code=404, content={"detail": "User not found or no changes made."})
        else:
            return JSONResponse(status_code=404, content={"detail": "User not found."})

    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": str(e)})

@app.delete("/delete_user")
async def delete_user(request: Request, data: dict = Body(...), current_user: dict = Depends(fetch_user_from_cookie)):
    if current_user is None:
        return JSONResponse(status_code=400, content={"detail": "User not logged in."})

    role = current_user.get("role", "user")

    if role != "admin":
        return JSONResponse(status_code=403, content={"detail": "Unauthorized."})

    try:
        user = data.get("user")

        result = User_details.delete_one({"user": user})

        if result.deleted_count > 0:
            return JSONResponse(status_code=200, content={"detail": "User deleted successfully!"})
        else:
            return JSONResponse(status_code=404, content={"detail": "User not found."})

    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": str(e)})
