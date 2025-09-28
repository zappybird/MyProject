<#
Cleanup script for development: removes generated artifacts that are safe to delete.
It will remove:
- compiled Python caches under puzzle_solver/__pycache__
- generated tile images under static/tiles matching *_tile_*.png and tile_*.png
- any files in uploads/

Run from project root:
  powershell -ExecutionPolicy Bypass -NoProfile -File .\tools\cleanup_workspace.ps1
#>

Write-Host "Starting workspace cleanup..."

# Resolve project root (script is in tools/) - we want parent of the tools folder
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = Split-Path -Parent $scriptDir

# Delete compiled cache files if present
$pycache = Join-Path $projectRoot "puzzle_solver\__pycache__"
if (Test-Path $pycache) {
    Write-Host "Removing compiled .pyc files in $pycache"
    Get-ChildItem -Path $pycache -Filter *.pyc -File -ErrorAction SilentlyContinue | Remove-Item -Force -ErrorAction SilentlyContinue
    # remove directory if empty
    if (-not (Get-ChildItem -Path $pycache -Force -ErrorAction SilentlyContinue | Select-Object -First 1)) {
        Remove-Item -Path $pycache -Force -Recurse -ErrorAction SilentlyContinue
        Write-Host "Removed empty directory: $pycache"
    }
}

# Remove generated tile images (both UUID-prefixed and tile_*.png samples)
$tilesDir = Join-Path $projectRoot "static\tiles"
if (Test-Path $tilesDir) {
    $patterns = @("*_tile_*.png", "tile_*.png")
    foreach ($p in $patterns) {
        $matches = Get-ChildItem -Path $tilesDir -Filter $p -File -ErrorAction SilentlyContinue
        if ($matches) {
            Write-Host "Removing $($matches.Count) files matching $p in $tilesDir"
            $matches | Remove-Item -Force -ErrorAction SilentlyContinue
        }
    }
}

# Clear uploads folder if anything there
$uploads = Join-Path $projectRoot "uploads"
if (Test-Path $uploads) {
    $u = Get-ChildItem -Path $uploads -File -ErrorAction SilentlyContinue
    if ($u) {
        Write-Host "Removing $($u.Count) uploaded files in $uploads"
        $u | Remove-Item -Force -ErrorAction SilentlyContinue
    }
}

Write-Host "Workspace cleanup completed."
