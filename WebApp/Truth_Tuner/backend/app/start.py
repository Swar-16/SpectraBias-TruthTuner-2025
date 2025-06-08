import webbrowser
import subprocess
import time
import os

#Starts the FastAPI backend server on port 8000
backend_process = subprocess.Popen(
    ["uvicorn", "main:app", "--host", "localhost", "--port", "8000", "--reload"],
    cwd=os.path.dirname(__file__)
)

#Wait backend to start
time.sleep(2)

#Start a simple HTTP server for the frontend on port 3000
frontend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../Frontend"))
frontend_process = subprocess.Popen(
    ["python", "-m", "http.server", "3000"],
    cwd=frontend_dir
)

#Wait frontend server to start
time.sleep(2)

#Open the frontend in browser
webbrowser.open("http://localhost:3000")

#Wait for the backend process to finish
backend_process.wait()