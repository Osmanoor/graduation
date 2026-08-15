# v3 composite: real thesis figures into reserved panels, UofK logo on slide 1,
# faint UofK watermark top-right on every slide, and a page number on every slide.
# Reads slides\raw_v3\, writes slides\final_v3\. Raw generations are never modified.

$RawDir   = "F:\Desktop\graduation\research_decisions\defence\slides\raw_v3"
$OutDir   = "F:\Desktop\graduation\research_decisions\defence\slides\final_v3"
$LogoPath = "F:\Desktop\graduation\University_of_Khartoum__EEE_bachelor_s_thesis_template\Figures\Fig_logo.jpg"
$FigDir   = "F:\Desktop\graduation\thesis_figures\output\png"

Add-Type -AssemblyName System.Drawing
if (-not (Test-Path $OutDir)) { New-Item -ItemType Directory -Force -Path $OutDir | Out-Null }

$order = @(
    "slide_01_title","slide_02_agenda","slide_03_llm","slide_04_rag","slide_05_bottleneck",
    "slide_06_literature","slide_07_arabic","slide_08_rq","slide_09_objectives","slide_10_system",
    "slide_11_baseline","slide_12_query2doc","slide_13_densevsbm25","slide_14_repetition",
    "slide_15_fivenouns","slide_16_csqe","slide_17_placement","slide_18_journey","slide_19_metrics",
    "slide_20_conclusions","slide_21_futurework","slide_22_thanks"
)

# figure -> reserved panel, as fractions of the slide. Panels match the prompt geometry,
# inset at the top to clear each card's heading strip.
$figs = @{
    "slide_06_literature"  = @( @{f="fig_2_3_qe_taxonomy";           L=0.055; T=0.375; R=0.580; B=0.865} )
    "slide_13_densevsbm25" = @( @{f="fig_4_5_models_bar_v1";         L=0.055; T=0.360; R=0.480; B=0.925},
                                @{f="fig_4_5b_models_bar_bm25_v1";   L=0.525; T=0.360; R=0.950; B=0.925} )
    "slide_14_repetition"  = @( @{f="fig_4_7_repetition_v1";         L=0.375; T=0.360; R=0.950; B=0.925} )
    "slide_16_csqe"        = @( @{f="fig_3_8_csqe_aigen_v5a";        L=0.060; T=0.270; R=0.940; B=0.885} )
    "slide_18_journey"     = @( @{f="fig_4_11_progression_v2_annot"; L=0.345; T=0.330; R=0.950; B=0.925} )
}

function New-FadedImage([System.Drawing.Image]$img, [single]$alpha) {
    $bmp = New-Object System.Drawing.Bitmap $img.Width, $img.Height
    $g   = [System.Drawing.Graphics]::FromImage($bmp)
    $cm  = New-Object System.Drawing.Imaging.ColorMatrix
    $cm.Matrix33 = $alpha
    $ia  = New-Object System.Drawing.Imaging.ImageAttributes
    $ia.SetColorMatrix($cm)
    $rect = New-Object System.Drawing.Rectangle 0,0,$img.Width,$img.Height
    $g.DrawImage($img, $rect, 0, 0, $img.Width, $img.Height, [System.Drawing.GraphicsUnit]::Pixel, $ia)
    $g.Dispose(); $ia.Dispose()
    return $bmp
}

$logoSrc = [System.Drawing.Image]::FromFile($LogoPath)
$total   = $order.Count
$n = 0

foreach ($stem in $order) {
    $n++
    $src = Join-Path $RawDir "$stem.png"
    if (-not (Test-Path $src)) { Write-Host "MISSING: $stem"; continue }

    $img = [System.Drawing.Image]::FromFile($src)
    $bmp = New-Object System.Drawing.Bitmap $img.Width, $img.Height
    $g   = [System.Drawing.Graphics]::FromImage($bmp)
    $g.SmoothingMode     = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
    $g.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
    $g.TextRenderingHint = [System.Drawing.Text.TextRenderingHint]::AntiAliasGridFit
    $g.DrawImage($img, 0, 0, $img.Width, $img.Height)
    $W = $img.Width; $H = $img.Height
    $note = @()

    # --- thesis figures into reserved panels
    if ($figs.ContainsKey($stem)) {
        foreach ($spec in $figs[$stem]) {
            $fp = Join-Path $FigDir "$($spec.f).png"
            if (-not (Test-Path $fp)) { $note += "fig missing $($spec.f)"; continue }
            $fig = [System.Drawing.Image]::FromFile($fp)
            $px = $W * $spec.L; $py = $H * $spec.T
            $pw = $W * ($spec.R - $spec.L); $ph = $H * ($spec.B - $spec.T)
            $scale = [Math]::Min($pw / $fig.Width, $ph / $fig.Height)
            $dw = $fig.Width * $scale; $dh = $fig.Height * $scale
            $g.DrawImage($fig, ($px + ($pw-$dw)/2), ($py + ($ph-$dh)/2), $dw, $dh)
            $note += ("{0} {1}x{2}" -f $spec.f, [int]$dw, [int]$dh)
            $fig.Dispose()
        }
    }

    # --- full-strength logo on the title slide, into its reserved square
    if ($stem -eq "slide_01_title") {
        $th = [int]($H * 0.155)
        $tw = [int]($logoSrc.Width * ($th / $logoSrc.Height))
        $g.DrawImage($logoSrc, [int]($W * 0.070), [int]($H * 0.105), $tw, $th)
        $note += "logo"
    }

    # --- faint watermark, top-right, every slide
    $wh = [int]($H * 0.085)
    $ww = [int]($logoSrc.Width * ($wh / $logoSrc.Height))
    $faded = New-FadedImage $logoSrc 0.22
    $g.DrawImage($faded, ($W - $ww - [int]($W * 0.028)), [int]($H * 0.045), $ww, $wh)
    $faded.Dispose()

    # --- page number pill, bottom right
    $fontSize = [float]($H * 0.020)
    $font  = New-Object System.Drawing.Font("Segoe UI", $fontSize, [System.Drawing.FontStyle]::Bold, [System.Drawing.GraphicsUnit]::Pixel)
    $text  = "{0} / {1}" -f $n, $total
    $size  = $g.MeasureString($text, $font)
    $padX = $size.Height * 0.75; $padY = $size.Height * 0.32
    $pillW = $size.Width + 2*$padX; $pillH = $size.Height + 2*$padY
    $pillX = $W - $pillW - ($W * 0.028); $pillY = $H - $pillH - ($H * 0.045)
    $r = $pillH / 2
    $path = New-Object System.Drawing.Drawing2D.GraphicsPath
    $path.AddArc($pillX, $pillY, $r*2, $pillH, 90, 180)
    $path.AddArc($pillX + $pillW - $r*2, $pillY, $r*2, $pillH, 270, 180)
    $path.CloseFigure()
    $pb = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(238,255,255,255))
    $g.FillPath($pb, $path)
    $pen = New-Object System.Drawing.Pen ([System.Drawing.Color]::FromArgb(80,31,138,158)), ([float]($H*0.0015))
    $g.DrawPath($pen, $path)
    $tb = New-Object System.Drawing.SolidBrush ([System.Drawing.ColorTranslator]::FromHtml("#1F6F8A"))
    $g.DrawString($text, $font, $tb, ($pillX + $padX), ($pillY + $padY))
    $path.Dispose(); $pb.Dispose(); $pen.Dispose(); $font.Dispose(); $tb.Dispose()

    $bmp.Save((Join-Path $OutDir "$stem.png"), [System.Drawing.Imaging.ImageFormat]::Png)
    $g.Dispose(); $bmp.Dispose(); $img.Dispose()
    Write-Host ("{0,-24} {1,2}/{2}  {3}" -f $stem, $n, $total, ($note -join "  "))
}

$logoSrc.Dispose()
Write-Host "`nfinal_v3 -> $OutDir"
