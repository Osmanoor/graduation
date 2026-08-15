param(
    [string]$Only = "",          # comma-separated stems, empty = all
    [string]$Aspect = "16:9",
    [string]$Resolution = "4K"
)

$root  = "C:\Users\moham\AppData\Local\Temp\claude\f--Desktop-graduation\60f05023-192a-45f4-8e47-22a900f4a241\scratchpad"
$outDir = "F:\Desktop\graduation\research_decisions\defence\slides\raw_v3"
if (-not (Test-Path $outDir)) { New-Item -ItemType Directory -Force -Path $outDir | Out-Null }

$style = [System.IO.File]::ReadAllText("$root\style.txt", [System.Text.Encoding]::UTF8)
$all   = [System.IO.File]::ReadAllText("$root\prompts_all.txt", [System.Text.Encoding]::UTF8)

# split on ===stem=== markers
$parts = [regex]::Split($all, '(?m)^===(.+?)===\s*$') | Where-Object { $_.Trim() -ne "" }
$slides = @()
for ($i = 0; $i -lt $parts.Count; $i += 2) {
    $slides += [pscustomobject]@{ Stem = $parts[$i].Trim(); Body = $parts[$i+1].Trim() }
}

if ($Only) {
    $want = $Only -split ',' | ForEach-Object { $_.Trim() }
    $slides = $slides | Where-Object { $want -contains $_.Stem }
}

Write-Host ("{0} slide(s) to generate`n" -f $slides.Count)

$uriBase = "https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-image:generateContent?key=$($env:GEMINI_API_KEY)"
$ok = 0; $fail = @()

foreach ($s in $slides) {
    $dst = Join-Path $outDir "$($s.Stem).png"
    $prompt = $style + "`n`nSLIDE CONTENT AND LAYOUT`n" + $s.Body

    $body = @{
        contents = @(@{ parts = @(@{ text = $prompt }) })
        generationConfig = @{
            responseModalities = @("IMAGE")
            imageConfig = @{ aspectRatio = $Aspect; imageSize = $Resolution }
        }
    } | ConvertTo-Json -Depth 10

    Write-Host ("[{0}] generating ..." -f $s.Stem) -NoNewline
    try {
        $resp = Invoke-RestMethod -Uri $uriBase -Method Post -ContentType "application/json" `
                    -Body ([System.Text.Encoding]::UTF8.GetBytes($body)) -TimeoutSec 600 -ErrorAction Stop
        $part = $resp.candidates[0].content.parts | Where-Object { $_.inlineData } | Select-Object -First 1
        if (-not $part) { throw "no image part in response" }
        [System.IO.File]::WriteAllBytes($dst, [System.Convert]::FromBase64String($part.inlineData.data))
        Write-Host (" ok  ({0:N0} KB)" -f ((Get-Item $dst).Length / 1KB))
        $ok++
    } catch {
        $msg = if ($_.ErrorDetails.Message) { $_.ErrorDetails.Message } else { $_.Exception.Message }
        Write-Host " FAILED"
        Write-Host "   $msg"
        $fail += $s.Stem
    }
}

Write-Host ("`ndone: {0} ok, {1} failed" -f $ok, $fail.Count)
if ($fail.Count) { Write-Host ("failed: {0}" -f ($fail -join ", ")) }

