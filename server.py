from waitress import serve
import subprocess
import os
from sys import platform as pltfrm_type
from app import app

print("Dash should be running on http://127.0.0.1:8181/artificialintellect")
print("* Serving Flask app 'app'")
print("Press CTRL+C to quit")

server = app.server