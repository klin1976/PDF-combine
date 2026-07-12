param(
    [string]$CliPath = "dist\PDF-Combine-CLI.exe",
    [string]$GuiPath = "dist\PDF-Combine-GUI.exe",
    [ValidateRange(1, 20)]
    [int]$Runs = 5,
    [ValidateRange(1, 120)]
    [int]$GuiTimeoutSeconds = 45
)

$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$CliExe = Join-Path $ProjectRoot $CliPath
$GuiExe = Join-Path $ProjectRoot $GuiPath

function Get-Stats {
    param([double[]]$Values)

    $sorted = $Values | Sort-Object
    $average = ($Values | Measure-Object -Average).Average
    $middle = [int]($sorted.Count / 2)
    if ($sorted.Count % 2 -eq 0) {
        $median = ($sorted[$middle - 1] + $sorted[$middle]) / 2
    } else {
        $median = $sorted[$middle]
    }

    [pscustomobject]@{
        Runs = $Values.Count
        AverageSeconds = [math]::Round($average, 3)
        MedianSeconds = [math]::Round($median, 3)
        MinSeconds = [math]::Round(($sorted | Select-Object -First 1), 3)
        MaxSeconds = [math]::Round(($sorted | Select-Object -Last 1), 3)
    }
}

function Measure-CliStartup {
    if (-not (Test-Path -LiteralPath $CliExe)) {
        Write-Warning "CLI executable not found: $CliExe"
        return
    }

    $times = @()
    for ($i = 1; $i -le $Runs; $i++) {
        $elapsed = Measure-Command { & $CliExe --help | Out-Null }
        $times += $elapsed.TotalSeconds
    }

    Write-Host "CLI startup ($CliExe):"
    Get-Stats -Values $times | Format-List
}

function Measure-GuiStartup {
    if (-not (Test-Path -LiteralPath $GuiExe)) {
        Write-Warning "GUI executable not found: $GuiExe"
        return
    }

    $times = @()
    for ($i = 1; $i -le $Runs; $i++) {
        $process = Start-Process -FilePath $GuiExe -PassThru -WindowStyle Hidden
        $started = Get-Date
        $deadline = $started.AddSeconds($GuiTimeoutSeconds)
        $ready = $false

        while ((Get-Date) -lt $deadline) {
            $process.Refresh()
            if ($process.HasExited) {
                break
            }
            if ($process.MainWindowHandle -ne 0) {
                $ready = $true
                break
            }
            Start-Sleep -Milliseconds 250
        }

        $elapsed = ((Get-Date) - $started).TotalSeconds
        if ($ready) {
            $times += $elapsed
        } else {
            Write-Warning "GUI run $i did not expose a main window within $GuiTimeoutSeconds seconds."
        }

        if (-not $process.HasExited) {
            Stop-Process -Id $process.Id -Force
        }
    }

    if ($times.Count -gt 0) {
        Write-Host "GUI startup ($GuiExe):"
        Get-Stats -Values $times | Format-List
    }
}

Measure-CliStartup
Measure-GuiStartup
