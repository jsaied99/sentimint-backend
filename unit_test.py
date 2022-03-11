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

def test_all_queries_success(app, client, db):
    payload = {
        "uid": 'maryann',
    }
    res = client.post('/all_queries', json=payload, follow_redirects=True)
    json_data = res.json
    
    assert json_data['status'] == 1
    assert len(json_data['data']) > 0
    
def test_all_queries_failure(app, client, db):
    payload = {
        "uid": 'not_existing_user',
    }
    res = client.post('/all_queries', json=payload, follow_redirects=True)
    json_data = res.json
    
    assert json_data['status'] == 1
    assert len(json_data['data']) == 0


def test_single_topic_success(app, client, db):
    topic = 'Cat%20Fish'
    res = client.get('/topic/'+topic , follow_redirects=True)
    json_data = res.json
    
    assert json_data['status'] == 1
    assert len(json_data['data']) > 0
    
def test_single_topic_failure(app, client, db):
    topic = 'Cat'
    res = client.get('/topic/'+topic , follow_redirects=True)
    json_data = res.json
    
    assert json_data['status'] == 0
    assert len(json_data['data']) == 0
    
    
    
def test_all_topics_success(app, client, db):
    res = client.get('/all_topics', follow_redirects=True)
    json_data = res.json
    
    assert json_data['status'] == 1
    assert len(json_data['data']) > 0


    
    
def test_twitter_api_success(app, client, db):
    payload = {
        "uid": ''.join(random.choice(letters) for _ in range(10)),
        "limit": 10, 
        "topic": "lebron james"
    }
    res = client.post('/twitter_api', json=payload, follow_redirects=True)
    json_data = res.json
    data = json_data['data']
    
    assert json_data['status'] == 1
    assert data['tweet_count'] == payload['limit']
    assert len(data['texts']) == payload['limit']

def test_twitter_api_failure(app, client, db):
    payload = {
        "uid": ''.join(random.choice(letters) for _ in range(10)),
        "limit": 110, 
        "topic": "lebron james"
    }
    res = client.post('/twitter_api', json=payload, follow_redirects=True)
    json_data = res.json
    data = json_data['data']
    
    assert json_data['status'] == 0
    assert len(data) == 0


def test_wrong_path(app, client, db):
    res = client.get('/wrong_path', follow_redirects=True)
    json_data = res.json
    
    assert json_data['status'] == 0
    assert json_data['message'] == 'wrong path'