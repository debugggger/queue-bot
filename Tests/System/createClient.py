from pyrogram import Client

from dotenv import load_dotenv
import os

load_dotenv()
api_id = os.getenv('api_id')
api_hash = os.getenv('api_hash')

client = Client(name='client1', api_id=api_id, api_hash=api_hash)

client.start()
print(client.export_session_string())
client.stop()
