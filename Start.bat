@echo off
cls
IF EXIST Python (
Python\App\Python\python.exe main.py
) ELSE (
echo No
)
pip install -r requirements.txt
python main.py
pause