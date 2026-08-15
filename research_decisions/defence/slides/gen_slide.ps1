param(
    [Parameter(Mandatory=$true)][string]$PromptPath,
    [Parameter(Mandatory=$true)][string]$OutPath,
    [string]$Size = "1536x1024",
    [string]$Model = "gpt-image-2",
    [string]$Quality = "high"
)

# Key comes from the environment only. Never persisted to disk.
if (-not $env:OPENAI_API_KEY) { Write-Error "OPENAI_API_KEY not set"; exit 1 }

$prompt = [System.IO.File]::ReadAllText((Resolve-Path $PromptPath).Path, [System.Text.Encoding]::UTF8)
Write-Host ("prompt: {0} chars" -f $prompt.Length)

$body = @{
    model   = $Model
    prompt  = $prompt
    size    = $Size
    quality = $Quality
    n       = 1
} | ConvertTo-Json -Depth 5

$headers = @{
    "Authorization" = "Bearer $($env:OPENAI_API_KEY)"
    "Content-Type"  = "application/json"
}

Write-Host "generating -> $OutPath  [$Model $Size $Quality]"

try {
    $resp = Invoke-RestMethod -Uri "https://api.openai.com/v1/images/generations" `
                              -Method Post -Headers $headers `
                              -Body ([System.Text.Encoding]::UTF8.GetBytes($body)) `
                              -TimeoutSec 600 -ErrorAction Stop
} catch {
    Write-Host "FAILED: $($_.Exception.Message)"
    if ($_.ErrorDetails.Message) { Write-Host $_.ErrorDetails.Message }
    exit 1
}

$b64 = $resp.data[0].b64_json
if (-not $b64) { Write-Host "no b64_json in response"; $resp | ConvertTo-Json -Depth 6; exit 1 }

$dir = Split-Path -Parent $OutPath
if (-not (Test-Path $dir)) { New-Item -ItemType Directory -Force -Path $dir | Out-Null }

[System.IO.File]::WriteAllBytes($OutPath, [System.Convert]::FromBase64String($b64))
Write-Host ("saved: {0}  ({1:N0} KB)" -f $OutPath, ((Get-Item $OutPath).Length / 1KB))
