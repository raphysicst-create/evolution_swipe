"""Actual rendered stage/tutorial/ending gallery. Test-only browser state setup."""
from pathlib import Path
import argparse,json
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
ap=argparse.ArgumentParser();ap.add_argument('--label',required=True);a=ap.parse_args()
out=ROOT/'qa/captures'/a.label;out.mkdir(parents=True,exist_ok=True)
report=[]
with sync_playwright() as p:
    browser=p.chromium.launch()
    page=browser.new_page(viewport={'width':548,'height':930},device_scale_factor=1,reduced_motion='reduce')
    page.goto((ROOT/'index.html').as_uri()+'?seed=1234');page.locator('#tutSkip').click()
    stages=page.evaluate('Object.keys(TREE)')
    for i,stage in enumerate(stages):
        page.evaluate('(id)=>render(id)',stage)
        page.locator('.evo-game').screenshot(path=out/f'stage-{i}.png')
        report.append(page.evaluate('({node,title:speciesTitle.textContent,icon:cardIcon.firstChild.className,art:getComputedStyle(cardIcon.firstChild).backgroundImage.length})'))
    page.evaluate("cardIcon.innerHTML='<i class=\"fa-solid fa-future-unknown\"></i>'")
    page.locator('.card-stage').screenshot(path=out/'unknown-icon.png')
    report.append({'unknownArtBytes':page.locator('#cardIcon>i').evaluate('(el)=>getComputedStyle(el).backgroundImage.length')})
    for name,w,h in [('small-short',320,568),('landscape',844,390),('tablet',768,1024)]:
        page.set_viewport_size({'width':w,'height':h})
        page.reload();page.locator('#tutSkip').click();page.locator('#openTut').click()
        for i in range(5):
            page.screenshot(path=out/f'{name}-tut-{i}.png',full_page=True)
            if i<4:page.locator('#tutNext').click()
        page.keyboard.press('ArrowRight');page.locator('#tutNext').click()
        # Deterministic test setup, no production code or data writes.
        page.evaluate("render(Object.keys(TREE).find(k=>TREE[k].title.length===Math.max(...Object.values(TREE).map(n=>n.title.length))))")
        page.screenshot(path=out/f'{name}-long-title.png',full_page=True)
        page.evaluate("path=['원시 척삭동물 (피카이아) · 해양 무산소 → 번성','원시 유턱어류 · 연안 습지 확대 → 번성']; reached.add('jawed_fish'); pop=120; showEnd('end_shark')")
        page.screenshot(path=out/f'{name}-ending.png',full_page=True)
        page.locator('#ckBtn').click()
        page.locator('#openData').click();page.screenshot(path=out/f'{name}-tools.png',full_page=True);page.locator('#closeData').click()
        page.locator('#openTree').click();page.screenshot(path=out/f'{name}-tree.png',full_page=True);page.locator('#closeTree').click()
    gallery='<html><head><meta charset="utf-8"><style>body{margin:0;padding:24px;background:#1c272d;color:#f3e3c3;font:16px sans-serif}main{display:grid;grid-template-columns:repeat(5,1fr);gap:12px}img{width:100%;display:block}h2{font-size:14px}article{border:1px solid #567;border-radius:12px;overflow:hidden}</style></head><body><h1>Actual stage renders / existing icon metadata</h1><main>'
    gallery+=''.join(f'<article><h2>{row["title"]}</h2><img src="stage-{i}.png"></article>' for i,row in enumerate(report[:-1]))+'</main></body></html>'
    (out/'stage-gallery.html').write_text(gallery,encoding='utf-8')
    page.set_viewport_size({'width':1600,'height':1100});page.goto((out/'stage-gallery.html').as_uri());page.screenshot(path=out/'stage-gallery.png',full_page=True)
    browser.close()
(out/'extended.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(out)
