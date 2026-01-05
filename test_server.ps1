# Quick test script to verify the server is working

Write-Host "Testing Image Similarity Search Server..." -ForegroundColor Cyan
Write-Host ""

try {
    # Test API health endpoint
    Write-Host "1. Testing API health endpoint..." -ForegroundColor Yellow
    $health = Invoke-RestMethod -Uri "http://localhost:5000/api/health" -Method Get
    
    if ($health.status -eq "ok") {
        Write-Host "   ✓ Server is running" -ForegroundColor Green
        Write-Host "   ✓ Indexed: $($health.indexed)" -ForegroundColor Green
        Write-Host "   ✓ Total images: $($health.total_images)" -ForegroundColor Green
    } else {
        Write-Host "   ✗ Server health check failed" -ForegroundColor Red
    }
    
    Write-Host ""
    
    # Test React app
    Write-Host "2. Testing React app..." -ForegroundColor Yellow
    $response = Invoke-WebRequest -Uri "http://localhost:5000/" -UseBasicParsing
    
    if ($response.StatusCode -eq 200 -and $response.Content -like "*react*") {
        Write-Host "   ✓ React app is being served" -ForegroundColor Green
    } else {
        Write-Host "   ✗ React app test failed" -ForegroundColor Red
    }
    
    Write-Host ""
    Write-Host "All tests passed! ✅" -ForegroundColor Green
    Write-Host "Open your browser to http://localhost:5000" -ForegroundColor Cyan
    
} catch {
    Write-Host ""
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
    Write-Host "Make sure the server is running:" -ForegroundColor Yellow
    Write-Host "  python app.py" -ForegroundColor White
}
