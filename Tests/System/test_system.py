import pytest

from pyrogram import Client

from dotenv import load_dotenv
import os

@pytest.fixture(scope="session")
def client():
    
    load_dotenv()
    api_id = os.getenv('api_id')
    api_hash = os.getenv('api_hash')
    session_string = os.getenv('session_string')

    client = Client(name='client1', api_id=api_id, api_hash=api_hash, in_memory=True, session_string=session_string)
    client.start()

    yield client

    client.stop()

@pytest.mark.system
def test_system1(client):
    client.send_message('me', 'Test_message')
    assert True
