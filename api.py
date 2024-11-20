from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from typing import List

app = FastAPI()

# Root route
@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI app!"}

# Data model for user
class User(BaseModel):
    id: int
    name: str
    email: EmailStr  # Use EmailStr for email validation

# Sample data
users: List[User] = [
    User(id=1, name="Emanuele", email="levi.emanuele@icloud.com"),
    User(id=2, name="Bob", email="bob@example.com")
]

# Get all users
@app.get("/users", response_model=List[User])
def get_users():
    return users

# Get a single user by ID
@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: int):
    user = next((u for u in users if u.id == user_id), None)
    if user:
        return user
    raise HTTPException(status_code=404, detail="User not found")

# Add a new user
@app.post("/users", response_model=User)
def create_user(user: User):
    # Ensure unique ID
    if any(u.id == user.id for u in users):
        raise HTTPException(status_code=400, detail="User ID already exists")
    # Ensure unique email
    if any(u.email == user.email for u in users):
        raise HTTPException(status_code=400, detail="Email already exists")
    users.append(user)
    return user

# Delete a user by ID
@app.delete("/users/{user_id}", response_model=User)
def delete_user(user_id: int):
    global users
    user = next((u for u in users if u.id == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    users = [u for u in users if u.id != user_id]
    return user
