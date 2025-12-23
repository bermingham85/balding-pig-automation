# CLAUDE WORK LOGGER - Auto-saves detailed work throughout sessions
# This runs automatically during Claude sessions to maintain detailed logs

param(
    [Parameter(Mandatory=$true)]
    [string]$Action,
    
    [Parameter(Mandatory=$false)]
    [string]$ProjectName = "",
    
    [Parameter(Mandatory=$false)]
    [string]$Details = "",
    
    [Parameter(Mandatory=$false)]
    [string]$Status = "",
    
    [Parameter(Mandatory=$false)]
    [string]$Location = "",
    
    [Parameter(Mandatory=$false)]
    [string]$AccessMethod = ""
)

$logPath = "C:\claude_work_log\session_history.json"
$projectsPath = "C:\claude_work_log\active_projects.json"
$systemsPath = "C:\claude_work_log\functioning_systems.json"

# Ensure log directory exists
if (!(Test-Path "C:\claude_work_log")) {
    New-Item -ItemType Directory -Path "C:\claude_work_log" -Force
}

# Load current logs
$workLog = if (Test-Path $logPath) { Get-Content $logPath -Encoding UTF8 | ConvertFrom-Json } else { @{ sessions = @(); completed_projects = @(); failed_attempts = @() } }
$activeProjects = if (Test-Path $projectsPath) { Get-Content $projectsPath -Encoding UTF8 | ConvertFrom-Json } else { @{ active_projects = @(); priority_queue = @(); blocked_projects = @() } }
$functioningSystems = if (Test-Path $systemsPath) { Get-Content $systemsPath -Encoding UTF8 | ConvertFrom-Json } else { @{ functioning_systems = @(); system_status = @(); integration_map = @{} } }

$timestamp = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")

switch ($Action.ToLower()) {
    "start_session" {
        $sessionEntry = @{
            "session_id" = $Details
            "start_time" = $timestamp
            "projects_worked" = @()
            "systems_created" = @()
            "status" = "active"
        }
        $workLog.sessions += $sessionEntry
        Write-Host "📝 Session started: $Details" -ForegroundColor Green
    }
    
    "add_project" {
        $project = @{
            "name" = $ProjectName
            "description" = $Details
            "status" = if ($Status) { $Status } else { "pending" }
            "created" = $timestamp
            "last_updated" = $timestamp
            "location" = $Location
            "access_method" = $AccessMethod
            "completion_criteria" = @()
            "work_log" = @()
        }
        $activeProjects.active_projects += $project
        Write-Host "➕ Project added: $ProjectName" -ForegroundColor Yellow
    }
    
    "update_project" {
        $project = $activeProjects.active_projects | Where-Object { $_.name -eq $ProjectName }
        if ($project) {
            $project.status = if ($Status) { $Status } else { $project.status }
            $project.last_updated = $timestamp
            $project.work_log += @{
                "timestamp" = $timestamp
                "action" = $Details
                "status_change" = $Status
            }
            Write-Host "🔄 Project updated: $ProjectName - $Status" -ForegroundColor Cyan
        }
    }
    
    "complete_project" {
        $projectIndex = $activeProjects.active_projects | ForEach-Object { $i = 0 } { if ($_.name -eq $ProjectName) { $i }; $i++ }
        if ($projectIndex -ge 0) {
            $project = $activeProjects.active_projects[$projectIndex]
            $project.status = "completed"
            $project.completed_date = $timestamp
            $project.final_location = $Location
            $project.final_access_method = $AccessMethod
            
            # Move to completed projects
            $workLog.completed_projects += $project
            $activeProjects.active_projects = $activeProjects.active_projects | Where-Object { $_.name -ne $ProjectName }
            
            Write-Host "✅ Project completed: $ProjectName" -ForegroundColor Green
        }
    }
    
    "add_system" {
        $system = @{
            "name" = $ProjectName
            "description" = $Details
            "location" = $Location
            "access_method" = $AccessMethod
            "status" = if ($Status) { $Status } else { "operational" }
            "created" = $timestamp
            "last_verified" = $timestamp
            "dependencies" = @()
            "integration_points" = @()
        }
        $functioningSystems.functioning_systems += $system
        Write-Host "⚡ System registered: $ProjectName" -ForegroundColor Green
    }
    
    "verify_system" {
        $system = $functioningSystems.functioning_systems | Where-Object { $_.name -eq $ProjectName }
        if ($system) {
            $system.status = $Status
            $system.last_verified = $timestamp
            $system.verification_notes = $Details
            Write-Host "🔍 System verified: $ProjectName - $Status" -ForegroundColor Cyan
        }
    }
    
    "add_priority" {
        $priorityItem = @{
            "task" = $ProjectName
            "description" = $Details  
            "priority" = if ($Status) { $Status } else { "medium" }
            "added" = $timestamp
        }
        $activeProjects.priority_queue += $priorityItem
        Write-Host "🔥 Priority added: $ProjectName" -ForegroundColor Red
    }
    
    "session_summary" {
        $currentSession = $workLog.sessions | Where-Object { $_.status -eq "active" } | Select-Object -Last 1
        if ($currentSession) {
            $currentSession.end_time = $timestamp
            $currentSession.status = "completed"
            $currentSession.summary = $Details
            $currentSession.projects_completed = ($workLog.completed_projects | Where-Object { $_.completed_date -gt $currentSession.start_time }).Count
        }
        
        # Update system info
        $workLog.system_info.last_updated = $timestamp
        $workLog.system_info.total_sessions = $workLog.sessions.Count
        
        Write-Host "📋 Session summary saved" -ForegroundColor Green
    }
}

# Save updated logs
$workLog | ConvertTo-Json -Depth 10 | Out-File $logPath -Encoding UTF8
$activeProjects | ConvertTo-Json -Depth 10 | Out-File $projectsPath -Encoding UTF8  
$functioningSystems | ConvertTo-Json -Depth 10 | Out-File $systemsPath -Encoding UTF8

Write-Host "💾 Work log auto-saved: $timestamp" -ForegroundColor Gray