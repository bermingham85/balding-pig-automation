# Immediate File Organization Script for Downloads
# This script will organize your messy downloads folder RIGHT NOW

Write-Host "🗂️ Starting Immediate File Organization..." -ForegroundColor Green

# Define source and destination paths
$SourcePath = "C:\downloads"
$BasePath = "C:\organized_files"

# Create organized folder structure
$Folders = @{
    "PDFs" = @("*.pdf")
    "Images" = @("*.jpg", "*.jpeg", "*.png", "*.gif", "*.bmp", "*.tiff", "*.webp")
    "Documents" = @("*.docx", "*.doc", "*.txt", "*.rtf", "*.odt")
    "Spreadsheets" = @("*.xlsx", "*.xls", "*.csv", "*.ods")
    "Presentations" = @("*.pptx", "*.ppt", "*.odp")
    "Videos" = @("*.mp4", "*.avi", "*.mkv", "*.mov", "*.wmv", "*.flv", "*.webm")
    "Audio" = @("*.mp3", "*.wav", "*.flac", "*.aac", "*.ogg", "*.wma")
    "Archives" = @("*.zip", "*.rar", "*.7z", "*.tar", "*.gz", "*.bz2")
    "Code" = @("*.js", "*.py", "*.java", "*.cpp", "*.c", "*.cs", "*.php", "*.html", "*.css", "*.sql", "*.json", "*.xml", "*.yaml", "*.yml")
    "Executables" = @("*.exe", "*.msi", "*.dmg", "*.pkg", "*.deb", "*.rpm")
    "Scripts" = @("*.ps1", "*.bat", "*.sh", "*.cmd")
}

# Create destination folders
Write-Host "📁 Creating organized folder structure..." -ForegroundColor Yellow
foreach ($FolderName in $Folders.Keys) {
    $DestPath = Join-Path $BasePath $FolderName
    if (!(Test-Path $DestPath)) {
        New-Item -ItemType Directory -Path $DestPath -Force | Out-Null
        Write-Host "   Created: $DestPath" -ForegroundColor Cyan
    }
}

# Get all files in downloads (excluding subdirectories for now)
Write-Host "🔍 Scanning downloads folder..." -ForegroundColor Yellow
$AllFiles = Get-ChildItem -Path $SourcePath -File -Recurse

Write-Host "📊 Found $($AllFiles.Count) files to organize" -ForegroundColor Cyan

$OrganizedCount = 0
$SkippedCount = 0

# Organize files by type
foreach ($File in $AllFiles) {
    $Moved = $false
    
    foreach ($Category in $Folders.Keys) {
        $Extensions = $Folders[$Category]
        
        foreach ($Extension in $Extensions) {
            if ($File.Name -like $Extension) {
                $DestPath = Join-Path $BasePath $Category
                $DestFile = Join-Path $DestPath $File.Name
                
                # Handle duplicate names
                $Counter = 1
                $OriginalName = $File.BaseName
                $FileExt = $File.Extension
                
                while (Test-Path $DestFile) {
                    $NewName = "$OriginalName($Counter)$FileExt"
                    $DestFile = Join-Path $DestPath $NewName
                    $Counter++
                }
                
                try {
                    Move-Item -Path $File.FullName -Destination $DestFile -Force
                    Write-Host "✅ Moved: $($File.Name) → $Category" -ForegroundColor Green
                    $OrganizedCount++
                    $Moved = $true
                    break
                } catch {
                    Write-Host "❌ Failed to move: $($File.Name) - $($_.Exception.Message)" -ForegroundColor Red
                    $SkippedCount++
                }
            }
        }
        
        if ($Moved) { break }
    }
    
    # Handle unmatched files
    if (!$Moved) {
        $MiscPath = Join-Path $BasePath "Miscellaneous"
        if (!(Test-Path $MiscPath)) {
            New-Item -ItemType Directory -Path $MiscPath -Force | Out-Null
        }
        
        $DestFile = Join-Path $MiscPath $File.Name
        $Counter = 1
        $OriginalName = $File.BaseName
        $FileExt = $File.Extension
        
        while (Test-Path $DestFile) {
            $NewName = "$OriginalName($Counter)$FileExt"
            $DestFile = Join-Path $MiscPath $NewName
            $Counter++
        }
        
        try {
            Move-Item -Path $File.FullName -Destination $DestFile -Force
            Write-Host "📦 Moved: $($File.Name) → Miscellaneous" -ForegroundColor Magenta
            $OrganizedCount++
        } catch {
            Write-Host "❌ Failed to move: $($File.Name) - $($_.Exception.Message)" -ForegroundColor Red
            $SkippedCount++
        }
    }
}

Write-Host ""
Write-Host "🎉 File Organization Complete!" -ForegroundColor Green
Write-Host "✅ Files organized: $OrganizedCount" -ForegroundColor Green
Write-Host "⚠️ Files skipped: $SkippedCount" -ForegroundColor Yellow
Write-Host "📁 Organized files location: $BasePath" -ForegroundColor Cyan

# Show summary of organized folders
Write-Host ""
Write-Host "📊 Organization Summary:" -ForegroundColor Yellow
foreach ($Category in $Folders.Keys + "Miscellaneous") {
    $CategoryPath = Join-Path $BasePath $Category
    if (Test-Path $CategoryPath) {
        $FileCount = (Get-ChildItem $CategoryPath -File).Count
        if ($FileCount -gt 0) {
            Write-Host "   $Category`: $FileCount files" -ForegroundColor Cyan
        }
    }
}

Write-Host ""
Write-Host "🔄 To enable automatic organization in the future:" -ForegroundColor Yellow
Write-Host "   1. Import the file organization workflow to N8N" -ForegroundColor White
Write-Host "   2. Schedule this script to run periodically" -ForegroundColor White
Write-Host "   3. Set up folder monitoring service" -ForegroundColor White