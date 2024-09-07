@echo off

:: Execute the script by double-clicking it or running it from the Command Prompt.

:: Check if pip is installed
where pip >nul 2>nul
if errorlevel 1 (
    echo pip could not be found, please install it first.
    exit /b 1
)

:: Install dependencies from requirements.txt
pip install -r requirements.txt
echo Dependencies have been installed.
