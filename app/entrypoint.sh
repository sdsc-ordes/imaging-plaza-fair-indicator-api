#!/bin/bash
nohup streamlit run /app/webapp/main.py &
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 15400