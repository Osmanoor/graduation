param(
    [Parameter(Mandatory=$true)][string]$StylePath,
    [Parameter(Mandatory=$true)][string]$PromptPath,
    [Parameter(Mandatory=$true)][string]$OutPath,
    [string]$Model = "gemini-3-pro-image",
    [string]$Aspect = "16:9",
    [string]$Resolution = "4K"
)

if (-not $env:GEMINI_API_KEY) { Write-Error "GEMINI_API_KEY not set"; exit 1 }

$style  = [System.IO.File]::ReadAllText((Resolve-Path $StylePath).Path,  [System.Text.Encoding]::UTF8)
$slide  = [System.IO.File]::ReadAllText((Resolve-Path $PromptPath).Path, [System.Text.Encoding]::UTF8)
$prompt = $style + "`n`n" + $slide

$body = @{
    contents = @(@{ parts = @(@{ text = $prompt }) })
    generationConfig = @{
        responseModalities = @("IMAGE")
        imageConfig = @{ aspectRatio = $Aspect; imageSize = $Resolution }
    }
} | ConvertTo-Json -Depth 10

$uri = "https://generativelanguage.googleapis.com/v1beta/models/$($Model):generateContent?key=$($env:GEMINI_API_KEY)"

Write-Host "gemini -> $OutPath  [$Model $Aspect $Resolution]  prompt $($prompt.Length) chars"

try {
    $resp = Invoke-RestMethod -Uri $uri -Method Post -ContentType "application/json" `
                              -Body ([System.Text.Encoding]::UTF8.GetBytes($body)) `
                              -TimeoutSec 600 -ErrorAction Stop
} catch {
    Write-Host "FAILED: $($_.Exception.Message)"
    if ($_.ErrorDetails.Message) { Write-Host $_.ErrorDetails.Message }
    exit 1
}

$part = $resp.candidates[0].content.parts | Where-Object { $_.inlineData } | Select-Object -First 1
if (-not $part) { Write-Host "no image part returned"; $resp | ConvertTo-Json -Depth 8; exit 1 }

$dir = Split-Path -Parent $OutPath
if (-not (Test-Path $dir)) { New-Item -ItemType Directory -Force -Path $dir | Out-Null }
[System.IO.File]::WriteAllBytes($OutPath, [System.Convert]::FromBase64String($part.inlineData.data))
Write-Host ("saved: {0}  ({1:N0} KB)" -f $OutPath, ((Get-Item $OutPath).Length / 1KB))
