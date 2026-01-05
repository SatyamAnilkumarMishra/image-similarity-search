# Image Similarity Search Startup Script

Write-Host "=================================================" -ForegroundColor Cyan
Write-Host "    Image Similarity Search - Starting Server    " -ForegroundColor Cyan
Write-Host "=================================================" -ForegroundColor Cyan
Write-Host ""

# Check if virtual environment is activated
if (-not $env:VIRTUAL_ENV) {
    Write-Host "Activating virtual environment..." -ForegroundColor Yellow
    if (Test-Path "venv\Scripts\Activate.ps1") {
        & "venv\Scripts\Activate.ps1"
    } else {
        Write-Host "Virtual environment not found. Please create one first:" -ForegroundColor Red
        Write-Host "  python -m venv venv" -ForegroundColor Yellow
        Write-Host "  .\venv\Scripts\Activate.ps1" -ForegroundColor Yellow
        Write-Host "  pip install -r requirements.txt" -ForegroundColor Yellow
        exit 1
    }
}

# Check if React build exists
if (-not (Test-Path "frontend\build\index.html")) {
    Write-Host "React build not found. Building..." -ForegroundColor Yellow
    Set-Location frontend
    
    if (-not (Test-Path "node_modules")) {
        Write-Host "Installing npm dependencies..." -ForegroundColor Yellow
        npm install
    }
    
    Write-Host "Building React app..." -ForegroundColor Yellow
    npm run build
    Set-Location ..
}

# Check if index exists
if (-not (Test-Path "models\image_features.pkl")) {
    Write-Host ""
    Write-Host "WARNING: Image index not found!" -ForegroundColor Red
    Write-Host "You need to build the index first by running:" -ForegroundColor Yellow
    Write-Host "  python src\indexer.py" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Make sure you have images in the 'data' directory first." -ForegroundColor Yellow
    Write-Host ""
    $response = Read-Host "Do you want to continue anyway? (y/n)"
    if ($response -ne "y") {
        exit 1
    }
}

Write-Host ""
Write-Host "Starting Flask server..." -ForegroundColor Green
Write-Host "Access the app at: http://localhost:5000" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

python app.py
