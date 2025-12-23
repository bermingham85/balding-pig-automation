# BALDING PIG COMPLETE DEPLOYMENT SCRIPT
# Deploys the entire autonomous merchandise system

Write-Host "🐷 DEPLOYING THE BALDING PIG AUTONOMOUS SYSTEM..." -ForegroundColor Green
Write-Host "=================================================" -ForegroundColor Cyan

$systemPath = "C:\BaldingPig_Complete_System"
$n8nUrl = "http://192.168.50.246:5678"

# Load configuration
$businessConfig = Get-Content "$systemPath\configs\business_config.json" | ConvertFrom-Json
$envPath = "$systemPath\configs\.env"

Write-Host "✅ Business: $($businessConfig.business_info.name)" -ForegroundColor Yellow
Write-Host "✅ Owner: $($businessConfig.business_info.owner)" -ForegroundColor Yellow
Write-Host "✅ Products: $($businessConfig.product_catalog.categories.Count) categories" -ForegroundColor Yellow

# Check N8N connectivity
Write-Host "`n🔍 Checking N8N connectivity..." -ForegroundColor Cyan
try {
    $response = Invoke-WebRequest -Uri $n8nUrl -TimeoutSec 5 -UseBasicParsing
    Write-Host "✅ N8N is accessible at $n8nUrl" -ForegroundColor Green
} catch {
    Write-Host "❌ Cannot reach N8N at $n8nUrl" -ForegroundColor Red
    Write-Host "Please ensure N8N is running on your QNAP" -ForegroundColor Yellow
    return
}

# List workflows to import
$workflows = Get-ChildItem "$systemPath\workflows\*.json"
Write-Host "`n📋 Workflows ready for import:" -ForegroundColor Cyan
foreach ($workflow in $workflows) {
    Write-Host "  • $($workflow.Name)" -ForegroundColor White
}

Write-Host "`n🎯 DEPLOYMENT STEPS:" -ForegroundColor Cyan
Write-Host "==================" -ForegroundColor Cyan
Write-Host "1. Open N8N: $n8nUrl" -ForegroundColor White
Write-Host "2. Import workflows from: $systemPath\workflows\" -ForegroundColor White
Write-Host "3. Configure API credentials from: $systemPath\configs\.env" -ForegroundColor White
Write-Host "4. Test each workflow" -ForegroundColor White
Write-Host "5. Activate automation" -ForegroundColor White

Write-Host "`n💼 BUSINESS CONFIGURATION:" -ForegroundColor Cyan
Write-Host "=========================" -ForegroundColor Cyan
Write-Host "Brand Voice: $($businessConfig.business_info.brand_voice)" -ForegroundColor White

$productCount = 0
foreach ($category in $businessConfig.product_catalog.categories) {
    $productCount += $category.designs.Count
    Write-Host "• $($category.name): $($category.designs.Count) designs, from $($category.base_price)" -ForegroundColor White
}
Write-Host "Total Products: $productCount designs across $($businessConfig.product_catalog.categories.Count) categories" -ForegroundColor Yellow

Write-Host "`n🛒 SALES PLATFORMS:" -ForegroundColor Cyan
Write-Host "==================" -ForegroundColor Cyan
foreach ($platform in $businessConfig.sales_platforms.PSObject.Properties) {
    $status = if ($platform.Value.enabled) { "✅ Enabled" } else { "❌ Disabled" }
    Write-Host "• $($platform.Name): $status" -ForegroundColor White
}

Write-Host "`n🔑 API CREDENTIALS AVAILABLE:" -ForegroundColor Cyan
if (Test-Path $envPath) {
    $envContent = Get-Content $envPath
    $apiKeys = $envContent | Where-Object { $_ -match "^[A-Z_]+_API_KEY=" }
    foreach ($key in $apiKeys) {
        $keyName = ($key -split "=")[0]
        Write-Host "  ✅ $keyName" -ForegroundColor Green
    }
} else {
    Write-Host "  ❌ .env file not found" -ForegroundColor Red
}

Write-Host "`n🚀 READY TO DEPLOY!" -ForegroundColor Green
Write-Host "Your complete Balding Pig automation system is organized and ready." -ForegroundColor White
Write-Host "Follow the deployment steps above to activate your autonomous merchandise empire." -ForegroundColor White

# Create import guide
$importGuide = "BALDING PIG N8N IMPORT GUIDE`n" +
"============================`n`n" +
"STEP 1: ACCESS N8N`n" +
"- Open: http://192.168.50.246:5678`n" +
"- Login to your N8N instance`n`n" +
"STEP 2: IMPORT WORKFLOWS`n" +
"1. Click + (New Workflow)`n" +
"2. Click menu > Import from file`n" +
"3. Select JSON file from C:\BaldingPig_Complete_System\workflows\`n" +
"4. Click Save`n`n" +
"IMPORT ORDER:`n" +
"1. balding_pig_autonomous_empire.json`n" +
"2. balding_pig_customer_service.json`n" +
"3. balding_pig_sales_analytics.json`n`n" +
"STEP 3: CONFIGURE CREDENTIALS`n" +
"Update API credentials in each workflow`n`n" +
"STEP 4: ACTIVATE`n" +
"- Test each workflow manually first`n" +
"- Then set them to Active`n" +
"- Monitor execution logs`n`n" +
"Your autonomous Balding Pig empire will then be running 24/7!"

$importGuide | Out-File "$systemPath\docs\N8N_Import_Guide.txt" -Encoding UTF8

Write-Host "`n📖 Import guide created: $systemPath\docs\N8N_Import_Guide.txt" -ForegroundColor Cyan