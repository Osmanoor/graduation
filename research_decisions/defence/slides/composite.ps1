# Composite pass: stamps the real UofK logo (slide 1) and a page number (all slides).
# Reads slides\raw\, writes slides\final\. Raw generations are never modified.

param(
    [string]$RawDir   = "F:\Desktop\graduation\research_decisions\defence\slides\raw",
    [string]$OutDir   = "F:\Desktop\graduation\research_decisions\defence\slides\final",
    [string]$LogoPath = "F:\Desktop\graduation\University_of_Khartoum__EEE_bachelor_s_thesis_template\Figures\Fig_logo.jpg"
)

Add-Type -AssemblyName System.Drawing
if (-not (Test-Path $OutDir)) { New-Item -ItemType Directory -Force -Path $OutDir | Out-Null }

$order = @(
    "slide_01_title", "slide_02_agenda", "slide_03_llm", "slide_04_rag",
    "slide_05_bottleneck", "slide_06_literature", "slide_07_arabic", "slide_08_rq",
    "slide_09_objectives", "slide_10_system", "slide_11_baseline", "slide_12_query2doc",
    "slide_13_densevsbm25", "slide_14_repetition", "slide_15_fivenouns", "slide_16_csqe",
    "slide_17_placement", "slide_18_journey", "slide_19_metrics", "slide_20_conclusions",
    "slide_21_futurework", "slide_22_thanks"
)

$numColor = [System.Drawing.ColorTranslator]::FromHtml("#5A6B67")
$total    = $order.Count
$n        = 0

foreach ($stem in $order) {
    $n++
    $src = Join-Path $RawDir "$stem.png"
    if (-not (Test-Path $src)) { Write-Host "skip (missing): $stem"; continue }

    $img = [System.Drawing.Image]::FromFile($src)
    $bmp = New-Object System.Drawing.Bitmap $img.Width, $img.Height
    $g   = [System.Drawing.Graphics]::FromImage($bmp)
    $g.SmoothingMode     = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
    $g.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
    $g.TextRenderingHint = [System.Drawing.Text.TextRenderingHint]::AntiAliasGridFit
    $g.DrawImage($img, 0, 0, $img.Width, $img.Height)

    $W = $img.Width; $H = $img.Height

    # logo: title slide only, into the reserved blank square
    if ($stem -eq "slide_01_title") {
        $logo = [System.Drawing.Image]::FromFile($LogoPath)
        $targetH = [int]($H * 0.150)
        $targetW = [int]($logo.Width * ($targetH / $logo.Height))
        $g.DrawImage($logo, [int]($W * 0.075), [int]($H * 0.115), $targetW, $targetH)
        $logo.Dispose()
    }

    # page number: white pill + dark teal text, so it reads on the gradient wave as well
    # as on plain background. Identical placement on every slide; skipped on the closing slide.
    if ($stem -ne "slide_22_thanks") {
        $fontSize = [float]($H * 0.020)
        $font  = New-Object System.Drawing.Font("Segoe UI", $fontSize, [System.Drawing.FontStyle]::Bold, [System.Drawing.GraphicsUnit]::Pixel)
        $text  = "{0:D2} / {1}" -f $n, $total
        $size  = $g.MeasureString($text, $font)

        $padX = $size.Height * 0.75
        $padY = $size.Height * 0.32
        $pillW = $size.Width  + 2 * $padX
        $pillH = $size.Height + 2 * $padY
        $pillX = $W - $pillW - ($W * 0.030)
        $pillY = $H - $pillH - ($H * 0.045)
        $r     = $pillH / 2

        $path = New-Object System.Drawing.Drawing2D.GraphicsPath
        $path.AddArc($pillX, $pillY, $r*2, $pillH, 90, 180)
        $path.AddArc($pillX + $pillW - $r*2, $pillY, $r*2, $pillH, 270, 180)
        $path.CloseFigure()

        $pillBrush = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(235, 255, 255, 255))
        $g.FillPath($pillBrush, $path)
        $penCol = [System.Drawing.Color]::FromArgb(70, 31, 138, 158)
        $pen = New-Object System.Drawing.Pen $penCol, ([float]($H * 0.0015))
        $g.DrawPath($pen, $path)

        $brush = New-Object System.Drawing.SolidBrush ([System.Drawing.ColorTranslator]::FromHtml("#1F6F8A"))
        $g.DrawString($text, $font, $brush, ($pillX + $padX), ($pillY + $padY))

        $path.Dispose(); $pillBrush.Dispose(); $pen.Dispose(); $font.Dispose(); $brush.Dispose()
    }

    $bmp.Save((Join-Path $OutDir "$stem.png"), [System.Drawing.Imaging.ImageFormat]::Png)
    $g.Dispose(); $bmp.Dispose(); $img.Dispose()
    Write-Host ("{0,-24} page {1:D2}/{2}   {3}x{4}" -f $stem, $n, $total, $W, $H)
}

Write-Host "`nfinal slides in: $OutDir"
