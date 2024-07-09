import os
import pytest
from pymongo import MongoClient
from repository_mongodb.mongo_config import MongoConfig
from repository_mongodb.mongo_client import get_mongo_client, get_mongo_database

@pytest.fixture(scope="session")
def mongo_config():
    os.environ['MONGO_HOST'] = 'localhost'
    os.environ['MONGO_PORT'] = '27017'
    os.environ['MONGO_USERNAME'] = ''
    os.environ['MONGO_PASSWORD'] = ''
    os.environ['MONGO_DATABASE'] = 'test_database'
    return MongoConfig()

@pytest.fixture(scope="session")
def mongo_client(mongo_config):
    client = MongoClient(mongo_config.get_connection_uri())
    yield client
    client.close()

@pytest.fixture(scope="session")
def mongo_database(mongo_client, mongo_config):
    return mongo_client[mongo_config.database]