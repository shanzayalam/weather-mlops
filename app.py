from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import mlflow.pyfunc
import bcrypt
import sqlite3
from fastapi.middleware.cors import CORSMiddleware
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
# FastAPI app instance
app = FastAPI()

# CORS configuration to allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specify a list of allowed origins like ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database initialization
def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()  
# JWT Token settings
SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Pydantic models for data validation
class PredictionRequest(BaseModel):
    humidity: float
    wind_speed: float

class UserSignup(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

# Function to add user to the database with hashed password
def add_user_to_db(username: str, password: str):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    cursor.execute('''
        INSERT INTO users (username, password) VALUES (?, ?)
    ''', (username, hashed_password))
    conn.commit()
    conn.close()

# Function to verify user credentials during login
def verify_user_credentials(username: str, password: str):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    if user and bcrypt.checkpw(password.encode('utf-8'), user[2]):
        return True
    return False

# Function to create JWT token
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        return username
    except JWTError:
        raise credentials_exception


# Authentication Routes
@app.post("/signup")
async def signup(user: UserSignup):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ?', (user.username,))
    existing_user = cursor.fetchone()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    add_user_to_db(user.username, user.password)
    return {"message": "User created successfully"}

@app.post("/login")
async def login(user: UserLogin):
    if not verify_user_credentials(user.username, user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    # Generate JWT token on successful login
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

# Weather Prediction Routes
@app.get("/")
def read_root():
    return {"message": "Weather Model API is up and running!"}

@app.get("/model/{model_name}/version/{version}")
def get_model_details(model_name: str, version: int):
    try:
        # Access MLFlow Model Registry
        client = mlflow.tracking.MlflowClient()
        model_details = client.get_model_version(name=model_name, version=version)
        return {
            "name": model_details.name,
            "version": model_details.version,
            "stage": model_details.current_stage,
            "status": model_details.status,
        }
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Model version not found: {e}")

@app.post("/model/{model_name}/version/{version}/set_alias")
def set_model_alias(model_name: str, version: int, alias: str):
    try:
        client = mlflow.tracking.MlflowClient()
        client.set_registered_model_alias(name=model_name, alias=alias, version=version)
        return {"message": f"Alias '{alias}' set for model '{model_name}', version {version}."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error setting alias: {e}")

@app.post("/predict")
def predict(data: PredictionRequest):
    try:
        # Load model by alias or stage
        model_uri = "models:/WeatherModel@staging"  
        model = mlflow.pyfunc.load_model(model_uri)
        
        input_data = [[data.humidity, data.wind_speed]]
        
        prediction = model.predict(input_data)
        return {"prediction": prediction[0]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {e}")
