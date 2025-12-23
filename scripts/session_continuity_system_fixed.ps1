# CLAUDE SESSION CONTINUITY SYSTEM
# Copy/paste this at the start of EVERY session for full project continuity

Write-Host "Initializing Claude Session Continuity..." -ForegroundColor Green

# Check if continuity log exists, if not create it
$logPath = "C:\claude_work_log\session_history.json"
$projectsPath = "C:\claude_work_log\active_projects.json"
$systemsPath = "C:\claude_work_log\functioning_systems.json"

if (!(Test-Path "C:\claude_work_log")) {
    New-Item -ItemType Directory -Path "C:\claude_work_log" -Force
    Write-Host "Created continuity log directory" -ForegroundColor Yellow
}

# Initialize log files if they don't exist
if (!(Test-Path $logPath)) {
    @{
        "system_info" = @{
            "created" = (Get-Date).ToString()
            "last_updated" = (Get-Date).ToString()
            "total_sessions" = 0
            "claude_version" = "Sonnet 4"
        }
        "sessions" = @()
        "completed_projects" = @()
        "failed_attempts" = @()
    } | ConvertTo-Json -Depth 10 | Out-File $logPath -Encoding UTF8
}

if (!(Test-Path $projectsPath)) {
    @{
        "active_projects" = @()
        "priority_queue" = @()
        "blocked_projects" = @()
    } | ConvertTo-Json -Depth 10 | Out-File $projectsPath -Encoding UTF8
}

if (!(Test-Path $systemsPath)) {
    @{
        "functioning_systems" = @()
        "system_status" = @()
        "integration_map" = @{}
    } | ConvertTo-Json -Depth 10 | Out-File $systemsPath -Encoding UTF8
}

# Read current state
$workLog = Get-Content $logPath -Encoding UTF8 | ConvertFrom-Json
$activeProjects = Get-Content $projectsPath -Encoding UTF8 | ConvertFrom-Json
$functioningSystems = Get-Content $systemsPath -Encoding UTF8 | ConvertFrom-Json

# Display current state
Write-Host ""
Write-Host "CURRENT PROJECT STATE SUMMARY:" -ForegroundColor Cyan
Write-Host "===============================" -ForegroundColor Cyan
Write-Host "Total Sessions: $($workLog.system_info.total_sessions)" -ForegroundColor White
Write-Host "Active Projects: $($activeProjects.active_projects.Count)" -ForegroundColor White
Write-Host "Functioning Systems: $($functioningSystems.functioning_systems.Count)" -ForegroundColor White
Write-Host "Last Updated: $($workLog.system_info.last_updated)" -ForegroundColor White
Write-Host ""

# Show active projects
if ($activeProjects.active_projects.Count -gt 0) {
    Write-Host "ACTIVE PROJECTS:" -ForegroundColor Yellow
    foreach ($project in $activeProjects.active_projects) {
        $status = if ($project.status -eq "completed") { "Completed" } 
                 elseif ($project.status -eq "in_progress") { "In Progress" }
                 elseif ($project.status -eq "blocked") { "Blocked" }
                 else { "Pending" }
        Write-Host "  - $($project.name) - $($project.status)" -ForegroundColor White
        if ($project.next_steps) {
            Write-Host "    Next: $($project.next_steps)" -ForegroundColor Gray
        }
    }
    Write-Host ""
}

# Show functioning systems
if ($functioningSystems.functioning_systems.Count -gt 0) {
    Write-Host "FUNCTIONING SYSTEMS:" -ForegroundColor Green
    foreach ($system in $functioningSystems.functioning_systems) {
        $statusIcon = if ($system.status -eq "operational") { "Active" } else { "Inactive" }
        Write-Host "  - $($system.name) - $($system.location)" -ForegroundColor White
        Write-Host "    Access: $($system.access_method)" -ForegroundColor Gray
    }
    Write-Host ""
}

# Show priority queue
if ($activeProjects.priority_queue.Count -gt 0) {
    Write-Host "PRIORITY QUEUE:" -ForegroundColor Red
    for ($i = 0; $i -lt $activeProjects.priority_queue.Count; $i++) {
        $item = $activeProjects.priority_queue[$i]
        Write-Host "  $($i + 1). $($item.task) - $($item.priority)" -ForegroundColor White
    }
    Write-Host ""
}

# Generate session initialization data for Claude
$sessionData = @{
    "timestamp" = (Get-Date).ToString()
    "session_number" = $workLog.system_info.total_sessions + 1
    "work_history" = $workLog
    "active_projects" = $activeProjects  
    "functioning_systems" = $functioningSystems
    "user_context" = @{
        "name" = "Michael Bermingham"
        "business" = "Rentasling, Bermech Ltd, The Balding Pig"
        "focus" = "AI automation, N8N workflows, QNAP systems"
        "working_directory" = "C:\Users\bermi"
        "qnap_access" = "admin@192.168.50.246"
        "preference" = "Complete functioning systems, not code dumps"
    }
    "system_requirements" = @{
        "must_complete_projects" = $true
        "must_track_progress" = $true
        "must_verify_functionality" = $true
        "must_provide_access_methods" = $true
        "no_abandoned_code" = $true
    }
}

Write-Host "SESSION DATA GENERATED FOR CLAUDE" -ForegroundColor Green
Write-Host "==================================" -ForegroundColor Green
Write-Host ""
Write-Host "PASTE THIS TO CLAUDE:" -ForegroundColor Yellow
Write-Host "====================" -ForegroundColor Yellow
Write-Host ""

$claudeMessage = @"
CLAUDE SESSION CONTINUITY INITIALIZATION:

Session #$($sessionData.session_number) - $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")

CONTEXT SUMMARY:
- User: Michael Bermingham (Rentasling, Bermech Ltd, The Balding Pig)
- Total previous sessions: $($workLog.system_info.total_sessions)
- Active projects: $($activeProjects.active_projects.Count)
- Functioning systems: $($functioningSystems.functioning_systems.Count)

CRITICAL REQUIREMENT: You must complete projects to functioning state, not just provide code. User requires working systems with clear access methods, not abandoned code dumps.

ACTIVE PROJECTS NEEDING COMPLETION:
$($activeProjects.active_projects | Where-Object { $_.status -ne "completed" } | ForEach-Object { "- $($_.name): $($_.status) - $($_.description)" } | Out-String)

FUNCTIONING SYSTEMS CONFIRMED WORKING:
$($functioningSystems.functioning_systems | Where-Object { $_.status -eq "operational" } | ForEach-Object { "- $($_.name): $($_.location) - Access: $($_.access_method)" } | Out-String)

PRIORITY QUEUE:
$($activeProjects.priority_queue | ForEach-Object { "- $($_.task) ($($_.priority) priority)" } | Out-String)

USER'S CONTINUATION REQUIREMENTS:
1. Maintain continuity from previous sessions
2. Complete existing projects before starting new ones
3. Verify all systems are actually functioning
4. Provide clear access methods for all deliverables
5. Update project status throughout session
6. Save detailed work log before session ends

Please acknowledge this context and confirm you understand the continuity requirements. Then provide status on the highest priority incomplete projects.
"@

Write-Output $claudeMessage

Write-Host ""
Write-Host "INSTRUCTIONS:" -ForegroundColor Cyan
Write-Host "1. Copy the message above and paste it to Claude" -ForegroundColor White
Write-Host "2. Claude will acknowledge and provide project status" -ForegroundColor White
Write-Host "3. Work with Claude to complete projects systematically" -ForegroundColor White
Write-Host "4. Claude will auto-save progress throughout session" -ForegroundColor White
Write-Host ""