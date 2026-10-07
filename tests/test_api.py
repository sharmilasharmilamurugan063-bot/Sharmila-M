import os
os.environ.setdefault("SECRET_KEY", "test-secret")
os.environ.setdefault("GEMINI_API_KEY", "")

from fastapi.testclient import TestClient
from app.main import app


def test_health():
    with TestClient(app) as client:
        r = client.get('/api/health')
        assert r.status_code == 200
        assert r.json()['status'] == 'ok'


def test_register_login_and_home_plan(tmp_path):
    email = 'test@example.com'
    with TestClient(app) as client:
        r = client.post('/api/auth/register', json={'name':'Test User','email':email,'password':'secret123'})
        assert r.status_code in (201, 409)
        r = client.post('/api/auth/login', json={'email':email,'password':'secret123'})
        assert r.status_code == 200
        r = client.post('/api/planners/generate-home', json={'budget':50000,'rooms':['Living Room'],'lights':2,'fans':1,'dining_tables':1,'style':'modern','notes':''})
        assert r.status_code == 200
        body = r.json()
        assert body['planner'] == 'home'
        assert body['source'] == 'fallback'
        assert body['history_id'] is not None
