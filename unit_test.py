import pytest
import json
from api import app as flask_app
from google.cloud import storage
import firebase_admin
from firebase_admin import credentials, firestore
import os 
import time
import string 
import random 
from google.oauth2 import service_account
import csv
from io import StringIO
from db_conn import initialize_db
letters = string.ascii_letters

@pytest.fixture
def app():
    yield flask_app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def db():
    return initialize_db()

def test_twitter_api(app, client, db):
    payload = {
        "uid": ''.join(random.choice(letters) for _ in range(10)),
        "limit": 10, 
        "topic": "lebron james"
    }
    res = client.post('/twitter_api', json=payload, follow_redirects=True)
    json_data = res.json
    data = json_data['data']
    
    assert json_data['success'] == 1
    assert data['tweet_count'] == payload['limit']
    assert len(data['texts']) == payload['limit']