param(
    [string]$Python = "python"
)

$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$SourceFile = Join-Path $ProjectRoot "PDF-Combine.py"
$DistDir = Join-Path $ProjectRoot "dist"
$BuildDir = Join-Path $ProjectRoot "build"
$GuiName = "PDF-Combine-GUI"
$CliName = "PDF-Combine-CLI"

if (-not (Test-Path -LiteralPath $SourceFile)) {
    throw "Source file not found: $SourceFile"
}

$targets = @(
    (Join-Path $DistDir "$GuiName.exe"),
    (Join-Path $DistDir "$CliName.exe"),
    (Join-Path $ProjectRoot "$GuiName.spec"),
    (Join-Path $ProjectRoot "$CliName.spec"),
    (Join-Path $BuildDir $GuiName),
    (Join-Path $BuildDir $CliName)
)

foreach ($target in $targets) {
    if (Test-Path -LiteralPath $target) {
        Remove-Item -LiteralPath $target -Recurse -Force
    }
}

New-Item -ItemType Directory -Force -Path $DistDir | Out-Null

& $Python -m PyInstaller --onefile --noconsole --name $GuiName $SourceFile
if ($LASTEXITCODE -ne 0) {
    throw "GUI build failed."
}

& $Python -m PyInstaller --onefile --console --name $CliName $SourceFile
if ($LASTEXITCODE -ne 0) {
    throw "CLI build failed."
}

$outputs = @(
    (Join-Path $DistDir "$GuiName.exe"),
    (Join-Path $DistDir "$CliName.exe")
)

foreach ($output in $outputs) {
    if (-not (Test-Path -LiteralPath $output)) {
        throw "Build output not found: $output"
    }
}

Write-Host "Windows exe build completed:"
foreach ($output in $outputs) {
    Write-Host " - $output"
}
