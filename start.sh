#!/bin/bash
# Start FastAPI backend in the background on port 8000
uvicorn app.main:app --host 127.0.0.1 --port 8000 &

# Start Streamlit frontend on port 10000 (which Render exposes)
streamlit run frontend/dashboard.py --server.port 10000 --server.address 0.0.0.0