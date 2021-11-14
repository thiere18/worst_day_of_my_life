from fastapi.testclient import TestClient
from app.main import app

client =TestClient(app)

def test_root():
    res=client.get("/")
    assert res.json().get('Hello')=="Worst day of my life"
    assert res.status_code==200
    
def test_create_user():
    res=client.post("/api/v1/users/",json={"username": "thiere","email": "email@email.com", "password": "password"})
    print(res.json())