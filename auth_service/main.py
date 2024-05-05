from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from models import User
from mongo import fetch_documents, insert_document

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.post("/register")
async def register_user(user: User):
    # Check if user already exists
    existing_user = fetch_documents("auth_db", "users", {"username": user.username})
    if existing_user["status"] and len(existing_user["data"]) > 0:
        raise HTTPException(status_code=400, detail="User already exists")

    # Create new user
    result = insert_document("auth_db", "users", user.dict())
    if result["status"]:
        return {"message": "User registered successfully"}
    else:
        raise HTTPException(status_code=500, detail="Error registering user")

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # Authenticate user
    user = fetch_documents("auth_db", "users", {"username": form_data.username})
    if not user["status"] or len(user["data"]) == 0:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    # Verify password
    if user["data"][0]["password"] != form_data.password:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    return {"access_token": user["data"][0]["username"], "token_type": "bearer"}

@app.get("/users/me")
async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fetch_documents("auth_db", "users", {"username": token})
    if not user["status"] or len(user["data"]) == 0:
        raise HTTPException(status_code=401, detail="Invalid authentication")
    return user["data"][0]