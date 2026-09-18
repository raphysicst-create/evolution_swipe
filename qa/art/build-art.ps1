$ErrorActionPreference = 'Stop'
$artDirectory = Split-Path -Parent $MyInvocation.MyCommand.Path
$artNames = @('life', 'worm', 'shield-halved', 'fish', 'frog', 'paw', 'egg', 'cat', 'hippo', 'staff-snake', 'dragon')
$artCss = @('/* Inline creature art: presentation selectors follow existing icon classes. */', '#cardIcon > i{display:block;width:100%;height:100%;background-repeat:no-repeat;background-position:center;background-size:contain;font-size:0;color:transparent;}', '#cardIcon > i::before{content:none;}')
$artCards = @()
foreach ($artName in $artNames) {
    $artSvg = (Get-Content -LiteralPath (Join-Path $artDirectory ($artName + '.svg')) -Raw).Trim()
    $artXml = [xml]$artSvg
    if ($artXml.svg.viewBox -ne '0 0 300 180') { throw "Unexpected viewBox: $artName" }
    $artSelector = if ($artName -eq 'life') { '#cardIcon > i' } else { '#cardIcon .fa-' + $artName }
    $artUrl = [Uri]::EscapeDataString($artSvg)
    $artCss += $artSelector + '{background-image:url("data:image/svg+xml,' + $artUrl + '");}'
    $artCards += '<figure>' + $artSvg + '<figcaption>' + $artName + '</figcaption></figure>'
}
[IO.File]::WriteAllText((Join-Path $artDirectory 'creatures.css'), ($artCss -join "`n"), [Text.UTF8Encoding]::new($false))
$artSheet = '<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>EVO SWIPE Creature Contact Sheet</title><style>*{box-sizing:border-box}body{margin:0;padding:30px;background:#1c242b;color:#f5e7cb;font:16px Segoe UI,sans-serif}h1{font-size:24px;margin:0 0 8px}p{color:#b5babe;margin:0 0 24px}main{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:20px;max-width:1120px}figure{margin:0;background:#293a3d;border:1px solid #405155;border-radius:22px;overflow:hidden}figure svg{display:block;width:100%;background:linear-gradient(#b7cfbe,#a5c1b8 63%,#85b0ad 64%,#92b9b0)}figcaption{padding:10px 16px;font-size:13px;letter-spacing:.08em} @media(max-width:650px){main{grid-template-columns:repeat(2,minmax(0,1fr))}}</style><h1>EVO SWIPE · Creature studies</h1><p>Icon-keyed, filter-free SVG · muted pigments, irregular silhouettes, curious eyes</p><main>' + ($artCards -join '') + '</main></html>'
[IO.File]::WriteAllText((Join-Path $artDirectory 'contact-sheet.html'), $artSheet, [Text.UTF8Encoding]::new($false))
Get-ChildItem -LiteralPath $artDirectory -Filter '*.svg' | Select-Object Name, Length
Get-Item -LiteralPath (Join-Path $artDirectory 'creatures.css') | Select-Object Name, Length
