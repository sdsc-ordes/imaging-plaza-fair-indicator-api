#!/bin/bash

cd /app
nohup streamlit run imaging_plaza_fair_indicator_api/gui/main.py &
python3 -m uvicorn imaging_plaza_fair_indicator_api.main:app --host 0.0.0.0 --port 15400