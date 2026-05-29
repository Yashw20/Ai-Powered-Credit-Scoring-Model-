import subprocess
import time
import os

print("🚀 Starting background FastAPI backend on 127.0.0.1:8000...")
# Launch the FastAPI backend locally using global module execution
backend_process = subprocess.Popen([
    "python", "-m", "uvicorn", "app.main:app",
    "--host", "127.0.0.1",
    "--port", "8000"
])

# Give the backend 4 seconds to fully spin up and bind to port 8000
time.sleep(4)

print("🎨 Launching Streamlit frontend dashboard on port 10000...")
# Launch the Streamlit frontend in the foreground
try:
    subprocess.run([
        "python", "-m", "streamlit", "run", "frontend/dashboard.py",
        "--server.port", "10000",
        "--server.address", "0.0.0.0"
    ], check=True)
finally:
    # Ensure backend closes if frontend goes down
    print("🛑 Shutting down backend processes...")
    backend_process.terminate()