"""Developer-only visual evidence; the delivered game has no dependency on this file."""
from pathlib import Path
import argparse, json
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
ap=argparse.ArgumentParser()
ap.add_argument('--label',required=True)
ap.add_argument('--source',type=Path,default=ROOT/'index.html')
args=ap.parse_args()
out=ROOT/'qa'/'captures'/args.label
out.mkdir(parents=True,exist_ok=True)
(out/'index.html').write_bytes(args.source.read_bytes())
with sync_playwright() as p:
    browser=p.chromium.launch()
    summary=[]
    for name,w,h in [('desktop',1440,1000),('mobile',390,844),('small',320,740)]:
        ctx=browser.new_context(viewport={'width':w,'height':h},device_scale_factor=1,has_touch=name!='desktop')
        page=ctx.new_page()
        errors=[]
        page.on('pageerror',lambda e:errors.append(str(e)))
        page.goto(out.joinpath('index.html').as_uri()+'?seed=1234')
        page.screenshot(path=out/f'{name}-tutorial.png',full_page=True)
        page.locator('#tutSkip').click()
        page.screenshot(path=out/f'{name}-game.png',full_page=True)
        box=page.locator('#swipeCard').bounding_box()
        x,y=box['x']+box['width']/2,box['y']+box['height']*.52
        page.mouse.move(x,y)
        page.mouse.down()
        page.mouse.move(x-70,y,steps=5)
        page.screenshot(path=out/f'{name}-drag.png',full_page=True)
        page.mouse.up()
        page.keyboard.press('ArrowRight')
        page.wait_for_function('pending!==null')
        page.wait_for_function("document.getElementById('verdictBox').style.opacity==='1'")
        page.wait_for_timeout(550)
        page.screenshot(path=out/f'{name}-result.png',full_page=True)
        page.locator('#contBtn').click()
        page.locator('#openTree').click()
        page.wait_for_timeout(100)
        page.screenshot(path=out/f'{name}-tree.png',full_page=True)
        page.locator('#closeTree').click()
        page.locator('#openData').click()
        page.screenshot(path=out/f'{name}-data.png',full_page=True)
        summary.append({'viewport':name,'width':w,'errors':errors,'card':box})
        ctx.close()
    browser.close()
(out/'capture.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
print(out)
