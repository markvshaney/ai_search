<#
.SYNOPSIS
    Activates the Python virtual environment for the AI Search project.
.DESCRIPTION
    This script activates the Python virtual environment located in the project directory.
    It includes error handling to ensure the virtual environment exists before activation.
.NOTES
    Requires PowerShell 3.0 or later
#>

$venvPath = "C:\Users\lbhei\source\ai_search\venv\Scripts\Activate.ps1"

# Verify virtual environment exists
if (-not (Test-Path $venvPath)) {
    Write-Error "Virtual environment not found at: $venvPath"
    exit 1
}

# Activate the virtual environment
try {
    . $venvPath
    Write-Host "Virtual environment activated successfully" -ForegroundColor Green
} catch {
    Write-Error "Failed to activate virtual environment: $_"
    exit 1
}