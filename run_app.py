import subprocess
import sys
import time

print("🚀 Starting background FastAPI backend on 127.0.0.1:8000...")
# Launch the FastAPI backend locally in the background
backend_process = subprocess.Popen([
    sys.executable, "-m", "uvicorn", "app.main:app",
    "--host", "127.0.0.1",
    "--port", "8000"
])

# Give the backend 3 seconds to spin up completely
time.sleep(3)

print("🎨 Launching Streamlit frontend dashboard on port 10000...")
# Launch the Streamlit frontend (This process stays in the foreground for Render)
try:
    subprocess.run([
        sys.executable, "-m", "streamlit", "run", "frontend/dashboard.py",
        "--server.port", "10000",
        "--server.address", "0.0.0.0"
    ], check=True)
finally:
    # Safely terminate the backend if Streamlit closes or crashes
    backend_process.terminate()