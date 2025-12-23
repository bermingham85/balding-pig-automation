# BALDING PIG SYSTEM DEPLOYMENT
Write-Host "DEPLOYING THE BALDING PIG AUTONOMOUS SYSTEM..." -ForegroundColor Green
Write-Host "===============================================" -ForegroundColor Cyan

$systemPath = "C:\BaldingPig_Complete_System"
$n8nUrl = "http://192.168.50.246:5678"

Write-Host "Business: The Balding Pig" -ForegroundColor Yellow
Write-Host "Owner: Michael Bermingham" -ForegroundColor Yellow

# Check workflows
$workflows = Get-ChildItem "$systemPath\workflows\*.json"
Write-Host "`nWorkflows ready for import:" -ForegroundColor Cyan
foreach ($workflow in $workflows) {
    Write-Host "  • $($workflow.Name)" -ForegroundColor White
}

# Check configs
Write-Host "`nConfiguration files:" -ForegroundColor Cyan
if (Test-Path "$systemPath\configs\business_config.json") {
    Write-Host "  ✅ Business configuration ready" -ForegroundColor Green
}
if (Test-Path "$systemPath\configs\.env") {
    Write-Host "  ✅ API credentials ready" -ForegroundColor Green
}

Write-Host "`nDEPLOYMENT STEPS:" -ForegroundColor Cyan
Write-Host "1. Open N8N: $n8nUrl" -ForegroundColor White
Write-Host "2. Import workflows from: $systemPath\workflows\" -ForegroundColor White
Write-Host "3. Configure API credentials from .env file" -ForegroundColor White
Write-Host "4. Test and activate workflows" -ForegroundColor White

Write-Host "`nSYSTEM READY FOR DEPLOYMENT!" -ForegroundColor Green