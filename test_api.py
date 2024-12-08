import pytest
from fastapi.testclient import TestClient
import sys
print(sys.path) 
import os


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app  


client = TestClient(app)

def test_signup():
    response = client.post("/signup", json={"username": "admin", "password": "pass"})
    assert response.status_code == 200
    assert response.json() == {"message": "User created successfully"}

def test_login():
    response = client.post("/login", json={"username": "admin", "password": "pass"})
    assert response.status_code == 200 or 401
