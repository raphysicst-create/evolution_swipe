"""Optional fair, offline cached-original vs standalone-candidate Chromium benchmark.

Capture original public presentation dependencies once: python qa/performance.py --capture
Then run isolated: python qa/performance.py --label final --trials 5
All captured third-party resources stay in TEMP, never become game dependencies.
"""
import argparse
import base64
import hashlib
import json
import os
from pathlib import Path
import statistics
import time

from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
BASE=Path(os.environ.get('TEMP','.'))/'evo-swipe-presentation-baseline-20260919'
CACHE=BASE/'original-presentation-cache.json'


def capture(browser):
    cache={};errors=[]
    context=browser.new_context(viewport={'width':1280,'height':900})
    page=context.new_page()
    def save(response):
        if not response.url.startswith(('http://','https://')):
            return
        headers={k:v for k,v in response.headers.items() if k not in ['content-encoding','content-length','transfer-encoding']}
        try:
            body=response.body() if response.status==200 else b''
            cache[response.url]={'status':response.status,'headers':headers,'body':base64.b64encode(body).decode()}
        except Exception as e:
            errors.append({'url':response.url,'error':str(e)})
    page.on('response',save)
    page.goto((BASE/'index.html').as_uri()+'?seed=42',wait_until='networkidle',timeout=45000)
    page.evaluate('document.fonts.ready')
    page.evaluate("tutClose();choose('R')")
    page.wait_for_timeout(3500)
    valid=page.evaluate("(()=>{const e=document.createElement('div');e.className='hidden';document.body.append(e);const v=getComputedStyle(e).display==='none';e.remove();return {tailwind:typeof tailwind!=='undefined',hiddenUtility:v,fontLoaded:document.fonts.check('900 16px \"Font Awesome 6 Free\"'),fontStatus:document.fonts.status}})()")
    context.close()
    CACHE.write_text(json.dumps({'cache':cache,'validation':valid,'captureErrors':errors},ensure_ascii=False),encoding='utf-8')
    return {'cachePath':str(CACHE),'resources':len(cache),'decodedBytes':sum(len(base64.b64decode(x['body'])) for x in cache.values()),'validation':valid,'errors':errors}


MEASURE = r"""async () => {
  // Let both the original font-backed page and the candidate complete initial paint.
  await document.fonts.ready;
  tutClose(); await new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)));
  let frames=[],longtasks=[],active=true,last=null,firstFrameCallbackMs=null;
  const start=performance.now();
  const frame=t=>{if(firstFrameCallbackMs===null)firstFrameCallbackMs=performance.now()-start;if(last!==null)frames.push({at:t-start,ms:t-last});last=t;if(active)requestAnimationFrame(frame)};
  requestAnimationFrame(frame);
  const obs=new PerformanceObserver(l=>l.getEntries().forEach(e=>longtasks.push({startMs:e.startTime-start,durationMs:e.duration})));
  obs.observe({type:'longtask',buffered:false});
  let overlayAt=null;const watcher=new MutationObserver(()=>{if(overlayAt===null&&!$('eventModal').classList.contains('hidden'))overlayAt=performance.now()-start});
  watcher.observe($('eventModal'),{attributes:true,attributeFilter:['class']});
  choose('R');const syncChooseMs=performance.now()-start;
  await new Promise(r=>setTimeout(r,3370));
  active=false;obs.disconnect();watcher.disconnect();
  const after=frames.filter(x=>x.at>200).map(x=>x.ms).sort((a,b)=>a-b);
  const all=frames.map(x=>x.ms).sort((a,b)=>a-b);
  const pct=(a,p)=>a[Math.min(a.length-1,Math.floor(a.length*p))];
  const initialFrames=frames.filter(x=>x.at<=200).map(x=>x.ms);
  const roulette={syncChooseMs,overlayMutationMs:overlayAt,firstFrameCallbackMs,firstTwoHundredMsMaxFrame:initialFrames.length?Math.max(...initialFrames):null,initialLongTaskMaxMs:Math.max(0,...longtasks.filter(x=>x.startMs<=200).map(x=>x.durationMs)),allMedianMs:pct(all,.5),allP95Ms:pct(all,.95),steadyP95Ms:pct(after,.95),steadyMaxMs:Math.max(...after),longtasks,frameCount:frames.length};
  proceed();if(!$('endModal').classList.contains('hidden'))restart();
  await new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)));
  const deltas=[],handlers=[];let prior=null;
  const dispatch=(type,x)=>card.dispatchEvent(new PointerEvent(type,{pointerId:99,pointerType:'touch',isPrimary:true,button:0,clientX:x,clientY:400,bubbles:true}));
  dispatch('pointerdown',300);
  await new Promise(resolve=>{
    let i=0;const move=t=>{if(prior!==null)deltas.push(t-prior);prior=t;const st=performance.now();dispatch('pointermove',300+Math.sin(i/10)*65);handlers.push(performance.now()-st);if(++i<120)requestAnimationFrame(move);else resolve()};requestAnimationFrame(move);
  });
  dispatch('pointercancel',300);deltas.sort((a,b)=>a-b);handlers.sort((a,b)=>a-b);
  return {roulette,drag:{frames:deltas.length,medianMs:pct(deltas,.5),p95Ms:pct(deltas,.95),maxMs:Math.max(...deltas),handlerP95Ms:pct(handlers,.95),pending:pending!==null},currentPopulation:pop};
}"""


def trial(browser,path,cache,rate,original):
    context=browser.new_context(viewport={'width':1280,'height':900},reduced_motion='no-preference')
    missing=[];requests=[];errors=[]
    def route(request):
        url=request.request.url;requests.append(url)
        entry=cache.get(url) if original else None
        if entry:
            request.fulfill(status=entry['status'],headers=entry['headers'],body=base64.b64decode(entry['body']))
        else:
            missing.append(url);request.abort()
    context.route('http://**/*',route);context.route('https://**/*',route)
    page=context.new_page();page.on('pageerror',lambda e:errors.append(str(e)))
    client=context.new_cdp_session(page)
    client.send('Emulation.setCPUThrottlingRate',{'rate':rate})
    start=time.perf_counter()
    page.goto(path.as_uri()+'?seed=42',wait_until='load')
    page.evaluate('document.fonts.ready')
    page.wait_for_function("(()=>{const e=document.createElement('div');e.className='hidden';document.body.append(e);const v=getComputedStyle(e).display==='none';e.remove();return v})()")
    load_ms=(time.perf_counter()-start)*1000
    metrics=page.evaluate(MEASURE)
    metrics.update({'readyMs':load_ms,'missingCachedResources':missing,'externalResourceLoads':len(requests),'pageErrors':errors})
    context.close()
    return metrics


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--capture',action='store_true');ap.add_argument('--label',default='final');ap.add_argument('--trials',type=int,default=5)
    args=ap.parse_args()
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=True)
        if args.capture:
            print(json.dumps(capture(browser),ensure_ascii=False,indent=2));browser.close();return
        saved=json.loads(CACHE.read_text(encoding='utf-8'));cache=saved['cache']
        results={'label':args.label,'method':'Headless Chromium 1280x900; exact original CDN responses replayed from TEMP, no live networking; candidate fully standalone. CPU throttle is simulation, not a hardware certification.','cacheValidation':saved['validation'],'trialsPerGroup':args.trials,'candidateSha256':hashlib.sha256((ROOT/'index.html').read_bytes()).hexdigest(),'samples':{},'summary':{}}
        for rate in [1,4]:
            for original in [True,False]:
                name=('original' if original else 'candidate')+f'-cpu{rate}x'
                path=BASE/'index.html' if original else ROOT/'index.html'
                samples=[]
                for i in range(args.trials):
                    samples.append(trial(browser,path,cache,rate,original));print(f'{name} sample {i+1}/{args.trials}',flush=True)
                results['samples'][name]=samples
                results['summary'][name]={'readyMedianMs':statistics.median(x['readyMs'] for x in samples),'syncChooseMedianMs':statistics.median(x['roulette']['syncChooseMs'] for x in samples),'firstOverlayFrameCallbackMedianMs':statistics.median(x['roulette']['firstFrameCallbackMs'] for x in samples),'initialLongTaskMaxMedianMs':statistics.median(x['roulette']['initialLongTaskMaxMs'] for x in samples),'rouletteSteadyP95MedianMs':statistics.median(x['roulette']['steadyP95Ms'] for x in samples),'rouletteSteadyMaxMs':max(x['roulette']['steadyMaxMs'] for x in samples),'dragP95MedianMs':statistics.median(x['drag']['p95Ms'] for x in samples),'dragHandlerP95MedianMs':statistics.median(x['drag']['handlerP95Ms'] for x in samples),'errors':[e for x in samples for e in x['pageErrors']],'missingResources':[e for x in samples for e in x['missingCachedResources']]}
        browser.close()
    results['candidateStable']=results['candidateSha256']==hashlib.sha256((ROOT/'index.html').read_bytes()).hexdigest()
    output=ROOT/'qa'/f'performance-{args.label}.json';output.write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'report':str(output),'summary':results['summary'],'candidateStable':results['candidateStable']},ensure_ascii=False,indent=2))


if __name__=='__main__':main()
