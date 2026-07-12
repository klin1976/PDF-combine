param(
    [string]$Python = "python",
    [ValidateSet("OneFile", "OneDir", "Both")]
    [string]$Layout = "OneFile",
    [switch]$Clean
)

$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$SourceFile = Join-Path $ProjectRoot "PDF-Combine.py"
$DistDir = Join-Path $ProjectRoot "dist"
$BuildDir = Join-Path $ProjectRoot "build"
$SpecDir = Join-Path $BuildDir "spec"
$GuiName = "PDF-Combine-GUI"
$CliName = "PDF-Combine-CLI"

if (-not (Test-Path -LiteralPath $SourceFile)) {
    throw "Source file not found: $SourceFile"
}

if ($Clean) {
    $targets = @(
        $DistDir,
        (Join-Path $BuildDir $GuiName),
        (Join-Path $BuildDir $CliName),
        (Join-Path $BuildDir "$GuiName-OneDir"),
        (Join-Path $BuildDir "$CliName-OneDir"),
        $SpecDir
    )

    foreach ($target in $targets) {
        if (Test-Path -LiteralPath $target) {
            Remove-Item -LiteralPath $target -Recurse -Force
        }
    }
}

New-Item -ItemType Directory -Force -Path $DistDir | Out-Null
New-Item -ItemType Directory -Force -Path $BuildDir | Out-Null
New-Item -ItemType Directory -Force -Path $SpecDir | Out-Null

$outputs = [System.Collections.Generic.List[string]]::new()

function Invoke-PyInstallerBuild {
    param(
        [string]$Name,
        [string[]]$ModeArgs,
        [string]$WorkSubdir,
        [string]$ExpectedOutput
    )

    $workPath = Join-Path $BuildDir $WorkSubdir
    & $Python -m PyInstaller @ModeArgs --name $Name --distpath $DistDir --workpath $workPath --specpath $SpecDir $SourceFile
    if ($LASTEXITCODE -ne 0) {
        throw "$Name build failed."
    }

    if (-not (Test-Path -LiteralPath $ExpectedOutput)) {
        throw "Build output not found: $ExpectedOutput"
    }

    $outputs.Add($ExpectedOutput)
}

if ($Layout -in @("OneFile", "Both")) {
    Invoke-PyInstallerBuild -Name $GuiName -ModeArgs @("--onefile", "--noconsole") -WorkSubdir $GuiName -ExpectedOutput (Join-Path $DistDir "$GuiName.exe")
    Invoke-PyInstallerBuild -Name $CliName -ModeArgs @("--onefile", "--console") -WorkSubdir $CliName -ExpectedOutput (Join-Path $DistDir "$CliName.exe")
}

if ($Layout -in @("OneDir", "Both")) {
    Invoke-PyInstallerBuild -Name "$GuiName-OneDir" -ModeArgs @("--onedir", "--noconsole") -WorkSubdir "$GuiName-OneDir" -ExpectedOutput (Join-Path $DistDir "$GuiName-OneDir")
    Invoke-PyInstallerBuild -Name "$CliName-OneDir" -ModeArgs @("--onedir", "--console") -WorkSubdir "$CliName-OneDir" -ExpectedOutput (Join-Path $DistDir "$CliName-OneDir")
}

Write-Host "Windows build completed:"
foreach ($output in $outputs) {
    Write-Host " - $output"
}
