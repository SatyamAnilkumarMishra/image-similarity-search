@echo off
echo =================================================
echo     Image Similarity Search - Starting Server
echo =================================================
echo.

REM Check if in virtual environment
if not defined VIRTUAL_ENV (
    echo Activating virtual environment...
    if exist "venv\Scripts\activate.bat" (
        call venv\Scripts\activate.bat
    ) else (
        echo Virtual environment not found!
        echo Please create one first:
        echo   python -m venv venv
        echo   venv\Scripts\activate.bat
        echo   pip install -r requirements.txt
        pause
        exit /b 1
    )
)

REM Check if React build exists
if not exist "frontend\build\index.html" (
    echo React build not found. Building...
    cd frontend
    
    if not exist "node_modules" (
        echo Installing npm dependencies...
        call npm install
    )
    
    echo Building React app...
    call npm run build
    cd ..
)

REM Check if index exists
if not exist "models\image_features.pkl" (
    echo.
    echo WARNING: Image index not found!
    echo You need to build the index first by running:
    echo   python src\indexer.py
    echo.
    echo Make sure you have images in the 'data' directory first.
    echo.
    pause
)

echo.
echo Starting Flask server...
echo Access the app at: http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo.

python app.py
