import os
os.environ["DATABASE_URL"]="sqlite:///./test_pocketsmart.db"
os.environ["SECRET_KEY"]="test-secret"
os.environ["GEMINI_API_KEY"]=""
from fastapi.testclient import TestClient
from app.main import app

client=TestClient(app)

def unique_email():
    import uuid
    return f"test-{uuid.uuid4().hex[:8]}@example.com"

def test_health():
    r=client.get('/health'); assert r.status_code==200; assert r.json()['status']=='ok'

def login_user():
    email=unique_email(); password='Password123!'
    r=client.post('/register',json={'full_name':'Test User','email':email,'password':password}); assert r.status_code==200
    r=client.post('/login',json={'email':email,'password':password}); assert r.status_code==200
    return r.json()['access_token']

def test_home_requires_auth():
    r=client.post('/generate-home',json={'budget':50000,'rooms':['Living Room'],'style':'modern','items':[{'category':'lighting','quantity':2}]})
    assert r.status_code==401

def test_home_fallback():
    token=login_user()
    r=client.post('/generate-home',headers={'Authorization':f'Bearer {token}'},json={'budget':50000,'rooms':['Living Room'],'style':'modern','items':[{'category':'lighting','quantity':2},{'category':'decor','quantity':1}]})
    assert r.status_code==200
    data=r.json(); assert data['planner']=='home'; assert data['allocated_total']<=50000

def test_party_fallback():
    token=login_user()
    r=client.post('/generate-party',headers={'Authorization':f'Bearer {token}'},json={'budget':50000,'guests':20,'event_type':'birthday','venue':'indoor','city':'Nagercoil'})
    assert r.status_code==200; assert r.json()['planner']=='party'

def test_jewelry_fallback():
    token=login_user()
    r=client.post('/generate-jewelry',headers={'Authorization':f'Bearer {token}'},data={'budget':5000,'occasion':'wedding','style':'traditional','outfit_notes':'red saree'})
    assert r.status_code==200; assert r.json()['planner']=='jewelry'
