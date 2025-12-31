@echo off
echo ========================================
echo Dependency Checker for Color Picker
echo ========================================
echo.

REM Check Python
echo [1/4] Checking Python...
python --version >nul 2>&1
if %errorlevel% equ 0 (
    for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
    echo [OK] Python is installed - Version: %PYTHON_VERSION%
) else (
    echo [FAIL] Python is NOT installed
    echo        Please install Python from https://www.python.org/
)
echo.

REM Check pyautogui
echo [2/4] Checking pyautogui...
python -c "import pyautogui" >nul 2>&1
if %errorlevel% equ 0 (
    for /f "tokens=2" %%i in ('python -m pip show pyautogui 2^>nul ^| findstr /C:"Version:"') do set PYAUTOGUI_VERSION=%%i
    if defined PYAUTOGUI_VERSION (
        echo [OK] pyautogui is installed - Version: %PYAUTOGUI_VERSION%
    ) else (
        echo [OK] pyautogui is installed
    )
) else (
    echo [FAIL] pyautogui is NOT installed
    echo        Installing pyautogui...
    python -m pip install pyautogui --quiet
    if %errorlevel% equ 0 (
        echo [OK] pyautogui installed successfully
    ) else (
        echo [ERROR] Failed to install pyautogui
    )
)
echo.

REM Check pynput
echo [3/4] Checking pynput...
python -c "import pynput" >nul 2>&1
if %errorlevel% equ 0 (
    for /f "tokens=2" %%i in ('python -m pip show pynput 2^>nul ^| findstr /C:"Version:"') do set PYNPUT_VERSION=%%i
    if defined PYNPUT_VERSION (
        echo [OK] pynput is installed - Version: %PYNPUT_VERSION%
    ) else (
        echo [OK] pynput is installed
    )
) else (
    echo [FAIL] pynput is NOT installed
    echo        Installing pynput...
    python -m pip install pynput --quiet
    if %errorlevel% equ 0 (
        echo [OK] pynput installed successfully
    ) else (
        echo [ERROR] Failed to install pynput
    )
)
echo.

REM Check screeninfo
echo [4/4] Checking screeninfo...
python -c "import screeninfo" >nul 2>&1
if %errorlevel% equ 0 (
    for /f "tokens=2" %%i in ('python -m pip show screeninfo 2^>nul ^| findstr /C:"Version:"') do set SCREENINFO_VERSION=%%i
    if defined SCREENINFO_VERSION (
        echo [OK] screeninfo is installed - Version: %SCREENINFO_VERSION%
    ) else (
        echo [OK] screeninfo is installed
    )
) else (
    echo [FAIL] screeninfo is NOT installed
    echo        Installing screeninfo...
    python -m pip install screeninfo --quiet
    if %errorlevel% equ 0 (
        echo [OK] screeninfo installed successfully
    ) else (
        echo [ERROR] Failed to install screeninfo
    )
)
echo.

REM Optional: Check PyInstaller
echo [Optional] Checking PyInstaller...
python -c "import PyInstaller" >nul 2>&1
if %errorlevel% equ 0 (
    for /f "tokens=2" %%i in ('python -m pip show pyinstaller 2^>nul ^| findstr /C:"Version:"') do set PYINSTALLER_VERSION=%%i
    if defined PYINSTALLER_VERSION (
        echo [OK] PyInstaller is installed - Version: %PYINSTALLER_VERSION%
    ) else (
        echo [OK] PyInstaller is installed
    )
) else (
    echo [INFO] PyInstaller is NOT installed (optional, only needed for .exe conversion)
)
echo.

echo ========================================
echo Dependency check complete!
echo ========================================
echo.
pause
