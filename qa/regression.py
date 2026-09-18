"""Offline presentation-only regression audit. Uses installed Playwright; installs nothing.

Run: python qa/regression.py --label iteration-1
The original files live outside the repository and are verified against pinned SHA-256s.
No game file is written by this harness. Browser state changes are test-only.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import time
from html.parser import HTMLParser
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BASELINE = Path(os.environ.get("TEMP", ".")) / "evo-swipe-presentation-baseline-20260919"
HASHES = {
    "index.html": "f7b9e3ff9b8d23ef5b1ed9cb04894076e47a6359800e29b942fca2dc161ce921",
    "evolution_swipe.html": "66fd0cc18f56f43934da83d9a8da30dab8766d77d5d9b8cf53cfbfeb7de273ec",
}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def game_script(data):
    scripts = re.findall(rb"<script\b[^>]*>(.*?)</script>", data, re.S | re.I)
    return next(s for s in scripts if b"function mulberry32" in s)


class Contract(HTMLParser):
    def __init__(self, source):
        super().__init__()
        self.ids, self.data, self.steps, self.external = {}, [], [], []
        self.duplicates = []
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            if a["id"] in self.ids:
                self.duplicates.append(a["id"])
            self.ids[a["id"]] = tag
        d = sorted((k, v) for k, v in attrs if k.startswith("data-"))
        if d:
            self.data.append([tag, a.get("id"), d])
        if "tut-step" in a.get("class", "").split():
            self.steps.append(a.get("data-step"))
        if (tag == "script" and a.get("src")) or (tag == "link" and a.get("rel") == "stylesheet"):
            self.external.append(a.get("src", a.get("href")))


ENGINE_TESTS = r"""() => {
  const records = [], coverage = new Set();
  const reset = (s=1234, n='pikaia', p=100) => {
    clearEvTimers(); tutClose();
    ['eventModal','endModal','treeModal','dataModal'].forEach(shut);
    seed=s; rng=mulberry32(seed); node='pikaia'; pending=null;
    path=[]; log=[]; locked=false; pop=p;
    reached.clear(); reached.add('pikaia'); seen.clear(); runEdges.clear();
    render(n); wheelRot=0;
  };
  const snapshot = () => ({
    node,pop,seed,locked,pending:pending?JSON.parse(JSON.stringify(pending)):null,
    path:[...path],log:JSON.parse(JSON.stringify(log)),reached:[...reached],seen:[...seen],runEdges:[...runEdges],
    foundEdges:[...foundEdges()],endOpen:!$('endModal').classList.contains('hidden'),
    eventOpen:!$('eventModal').classList.contains('hidden'),
    text:Object.fromEntries(['eraBadge','speciesTitle','scenarioText','badgeL','badgeR','popVal','endTitle','endTag','endDesc','evTrait','envName','envDesc','verdictTag','verdictNote','popDelta'].map(id=>[id,$(id).textContent]))
  });
  const seeds=[1,2,3,42,1234,98765,-17,2147483647];
  const random=seeds.map(s=>{const r=mulberry32(s);return [s,Array.from({length:256},()=>r())]});
  // Every payoff at six populations tests cap, both -45 overrides, collapse, perish and destinations.
  for(const id of Object.keys(TREE)) for(const side of ['L','R']) for(let i=0;i<TREE[id].envs.length;i++) for(const p of [1,20,45,50,100,120]) {
    reset(1234,id,p);
    rng=()=> (i+.5)/TREE[id].envs.length;
    choose(side);
    const before=snapshot();
    coverage.add(`${id}|${side}|${pending.env}`);
    proceed();
    records.push({kind:'payoff',id,side,i,p,before,after:snapshot()});
  }
  // Real seed streams and route progress; tests independently restart the test page state.
  for(const s of seeds) for(const pattern of ['LLLLLLLL','RRRRRRRR','LRLRLRLR','RLRLRLRL','LRRRRLLL','RRRRLRRR','RLRRRRRL','RRRLRRRL']) {
    reset(s); const turns=[];
    for(const side of pattern) {
      choose(side); const before=snapshot(); proceed();
      turns.push({before,after:snapshot()});
      if(!$('endModal').classList.contains('hidden')) break;
    }
    records.push({kind:'route',s,pattern,turns,nextRandom:rng()});
  }
  reset(42); choose('R'); proceed();
  const beforeRestart=snapshot(); restart(); const afterRestart=snapshot();
  const reachedNode=[...reached].find(x=>x!=='pikaia');
  restart(reachedNode); const checkpoint=snapshot();
  records.push({kind:'restart',beforeRestart,afterRestart,checkpoint,nextRandom:rng()});
  // Seed application preserves discoveries/log; zero/negative integer are accepted here.
  for(const value of ['0','-42','1234abc','not a number']) {
    $('seedInput').value=value; $('applySeed').click();
    records.push({kind:'seedApply',value,state:snapshot(),message:$('copyMsg').textContent,nextRandom:rng()});
  }
  reset(9); choose('L'); proceed();
  const beforeTut=snapshot(), expectedNext=mulberry32(9); expectedNext();
  tutOpen(); for(let i=0;i<4;i++) $('tutNext').click();
  const gated=$('tutNext').disabled;
  tutPass('R'); const passed=!$('tutNext').disabled;
  $('tutNext').click();
  const afterTut=snapshot();
  records.push({kind:'tutorial',gated,passed,closed:$('tutModal').classList.contains('hidden'),beforeTut,afterTut,nextRandom:rng(),expectedNextRandom:expectedNext()});
  // Diagram graph and bounds are data and controls, even though the visual layer changes.
  reset(12); choose('R'); proceed(); choose('R'); proceed();
  const graph=treeGraph(), dimensions=renderTree(); tW=dimensions.W;tH=dimensions.H;
  zoomAt(100,100,100); const max=tScale; zoomAt(.0001,100,100); const min=tScale;
  records.push({kind:'tree',graph,dimensions,zoomMax:max,zoomMin:min});
  const data={ENV,END,TREE,VERDICT,HEX,POPD,MAXPOP,allEdges:[...ALL_EDGES],BADGE_MIN,BADGE_FULL,SWIPE_THRESHOLD,WH_C,WH_R,WH_SPIN,WH_EASE};
  clearEvTimers();
  return {data,random,records,coverage:[...coverage],counts:{nodes:Object.keys(TREE).length,environments:Object.keys(ENV).length,endings:Object.keys(END).length,payoffs:coverage.size,branches:ALL_EDGES.size,transactions:records.filter(x=>x.kind==='payoff').length,seededRoutes:64}};
}"""

POINTER_TESTS = r"""async () => {
  const cases=[];
  for(const [delta,cancel,button] of [[-81,false,0],[-80,false,0],[80,false,0],[81,false,0],[120,true,0],[120,false,2]]) {
    clearEvTimers(); tutClose(); ['eventModal','endModal'].forEach(shut);
    seed=42; rng=mulberry32(seed); pending=null;path=[];log=[];pop=100;render('pikaia');
    const e=(type,x)=>card.dispatchEvent(new PointerEvent(type,{bubbles:true,pointerId:17,pointerType:'touch',isPrimary:true,button,clientX:x,clientY:300}));
    e('pointerdown',300);e('pointermove',300+delta);
    const badge=[$('badgeL').style.opacity,$('badgeR').style.opacity];
    e(cancel?'pointercancel':'pointerup',300+delta);
    const immediate={locked,pending:!!pending,log:log.length};
    await new Promise(r=>setTimeout(r,280));
    const final={locked,trait:pending?.trait,env:pending?.env,log:log.length};
    cases.push({delta,cancel,button,badge,immediate,final});
  }
  clearEvTimers();return cases;
}"""

EXPORT_TESTS = r"""async () => {
  clearEvTimers();tutClose();['eventModal','endModal'].forEach(shut);
  seed=1234;rng=mulberry32(seed);pending=null;path=[];log=[];pop=100;render('pikaia');
  choose('R');proceed();choose('L');proceed();
  let clipboard='',blob=null,download='';
  Object.defineProperty(navigator,'clipboard',{configurable:true,value:{writeText:async x=>{clipboard=x}}});
  const oldURL=URL.createObjectURL,oldClick=HTMLAnchorElement.prototype.click;
  URL.createObjectURL=b=>{blob=b;return 'blob:test'};
  HTMLAnchorElement.prototype.click=function(){download=this.download};
  $('copyLog').click();await Promise.resolve();const copyMessage=$('copyMsg').textContent;
  $('dlLog').click();const csv=await blob.text(), csvBytes=Array.from(new Uint8Array(await blob.arrayBuffer()).slice(0,3)),csvMessage=$('copyMsg').textContent;
  URL.createObjectURL=oldURL;HTMLAnchorElement.prototype.click=oldClick;
  const old={node,pop,seed,path:[...path],seen:[...seen]};
  $('clearLog').click();
  return {clipboard,copyMessage,csv,csvBytes,csvMessage,download,cleared:log.length,count:$('logCount').textContent,old,after:{node,pop,seed,path:[...path],seen:[...seen]}};
}"""


def canonical(value):
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"), sort_keys=True)


def run_browser(browser, path, original=False):
    context = browser.new_context(reduced_motion="reduce")
    requested, errors = [], []
    context.route(re.compile(r"https?://"), lambda route: (requested.append(route.request.url), route.abort()))
    # The original has an external Tailwind config script. Stub its absent offline global only;
    # the original game script, markup and data are untouched.
    if original:
        context.add_init_script("window.tailwind={};")
    page = context.new_page()
    page.on("pageerror", lambda error: errors.append(str(error)))
    start = time.perf_counter()
    page.goto(path.as_uri() + "?seed=1234", wait_until="load")
    load_ms = (time.perf_counter() - start) * 1000
    initial = page.evaluate("({node,pop,seed,pending,log,path,reached:[...reached],seen:[...seen],tutOpen:!$('tutModal').classList.contains('hidden')})")
    start = time.perf_counter()
    engine = page.evaluate(ENGINE_TESTS)
    engine_ms = (time.perf_counter() - start) * 1000
    pointers = page.evaluate(POINTER_TESTS)
    exports = page.evaluate(EXPORT_TESTS)
    storage = page.evaluate("Object.keys(localStorage)")
    context.close()
    return {"initial": initial, "engine": engine, "pointers": pointers, "exports": exports, "storageKeys": storage}, {"pageErrors": errors, "networkRequests": requested, "loadMs": round(load_ms, 1), "engineSuiteMs": round(engine_ms, 1)}


def ui_smoke(browser, path, mobile=False):
    context = browser.new_context(viewport={"width": 390 if mobile else 1280, "height": 844 if mobile else 900}, is_mobile=mobile, has_touch=mobile, reduced_motion="reduce")
    errors, requests = [], []
    context.route(re.compile(r"https?://"), lambda route: (requests.append(route.request.url), route.abort()))
    page = context.new_page()
    page.on("pageerror", lambda error: errors.append(str(error)))
    page.goto(path.as_uri() + "?seed=42", wait_until="load")
    result = {"mobile": mobile}
    result["tutorialVisible"] = page.locator("#tutModal").is_visible()
    page.locator("#tutSkip").click(timeout=3000)
    result["tutorialSkipped"] = not page.locator("#tutModal").is_visible()
    card = page.locator("#swipeCard")
    box = card.bounding_box()
    result["cardBounds"] = box
    result["noHorizontalOverflow"] = page.evaluate("document.documentElement.scrollWidth<=innerWidth+1")
    x,y = box["x"]+box["width"]*.45,box["y"]+box["height"]*.52
    result["cardHitTarget"] = page.evaluate("([x,y])=>document.getElementById('swipeCard').contains(document.elementFromPoint(x,y))", [x,y])
    if mobile:
        client = context.new_cdp_session(page)
        client.send("Input.dispatchTouchEvent", {"type":"touchStart","touchPoints":[{"x":x,"y":y}]})
        for i in range(1,11):
            client.send("Input.dispatchTouchEvent", {"type":"touchMove","touchPoints":[{"x":x+10*i,"y":y}]})
        client.send("Input.dispatchTouchEvent", {"type":"touchEnd","touchPoints":[]})
    else:
        page.mouse.move(x,y);page.mouse.down();page.mouse.move(x+110,y,steps=10);page.mouse.up()
    page.wait_for_function("pending!==null", timeout=3000)
    page.wait_for_function("document.getElementById('verdictBox').style.opacity==='1'", timeout=2000)
    result["realSwipe"] = page.evaluate("({trait:pending.trait,env:pending.env,node,pop,rows:log.length})")
    result["resultNoHorizontalOverflow"] = page.evaluate("document.documentElement.scrollWidth<=innerWidth+1")
    result["resultOverflowMetrics"] = page.evaluate("({viewport:innerWidth,documentScrollWidth:document.documentElement.scrollWidth,bodyScrollWidth:document.body.scrollWidth})")
    result["continueVisible"] = page.locator("#contBtn").is_visible()
    page.locator("#contBtn").click(timeout=3000)
    result["proceeded"] = page.evaluate("({node,pop,pending,rows:log.length})")
    page.locator("#openTree").click(timeout=3000)
    result["treeVisible"] = page.locator("#treeModal").is_visible()
    page.locator("#treeIn").click(timeout=3000)
    page.locator("#treeOut").click(timeout=3000)
    page.locator("#treeFit").click(timeout=3000)
    page.locator("#closeTree").click(timeout=3000)
    page.locator("#openData").click(timeout=3000)
    page.locator("#seedInput").fill("7")
    page.locator("#applySeed").click(timeout=3000)
    result["seedApplied"] = page.evaluate("({seed,node,pop})")
    page.locator("#closeData").click(timeout=3000)
    page.keyboard.press("ArrowLeft")
    page.wait_for_function("pending!==null", timeout=3000)
    page.keyboard.press("Enter")
    result["keyboardProceeded"] = page.evaluate("pending===null")
    result["pageErrors"],result["networkRequests"] = errors,requests
    context.close()
    return result


def normal_roulette(browser, path, original=False):
    context=browser.new_context(reduced_motion="no-preference")
    context.route(re.compile(r"https?://"),lambda route: route.abort())
    if original:
        context.add_init_script("window.tailwind={};")
    page=context.new_page()
    page.goto(path.as_uri()+"?seed=42",wait_until="load")
    result=page.evaluate(r"""async () => {
      tutClose();const stages=[],timing=[],frames=[],longTasks=[],longTaskDetails=[],frameGaps=[];
      const start=performance.now();let prev=start,active=true;
      const sample=t=>{if(prev!==start){frames.push(t-prev);if(t-prev>34)frameGaps.push({atMs:t-start,durationMs:t-prev})}prev=t;if(active)requestAnimationFrame(sample)};
      requestAnimationFrame(sample);
      let observer;try{observer=new PerformanceObserver(l=>l.getEntries().forEach(e=>{longTasks.push(e.duration);longTaskDetails.push({startMs:e.startTime-start,durationMs:e.duration,name:e.name,attribution:e.attribution.map(a=>({containerType:a.containerType,containerName:a.containerName}))})}));observer.observe({type:'longtask',buffered:false})}catch(_){}
      const record=(label)=>{if(!stages.includes(label)){stages.push(label);timing.push({label,ms:performance.now()-start})}};
      const watches=[['wheelSvg',()=>{if(wheelRot>0)record('spin')}],['envResult',()=>{if($('envResult').style.opacity==='1')record('environment')}],['verdictBox',()=>{if($('verdictBox').style.opacity==='1')record('verdict')}]];
      const mutations=watches.map(([id,fn])=>{const o=new MutationObserver(fn);o.observe($(id),{attributes:true,attributeFilter:['style']});return o});
      choose('R');record('chosen');const before={node,pop,log:log.length,pending:pending.env,rot:wheelRot};
      await new Promise(r=>setTimeout(r,3380));
      const idx=pending.envs.indexOf(pending.env),count=pending.envs.length,seg=360/count;
      const expected=(((360-(idx+.5)*seg-seg*.16*(idx%2?1:-1))%360)+360)%360;
      const actual=((wheelRot%360)+360)%360;
      const after={node,pop,log:log.length,pending:pending.env,rot:wheelRot,actual,expected,winningFill:$('wseg'+idx).getAttribute('fill'),environmentOpacity:$('envResult').style.opacity,verdictOpacity:$('verdictBox').style.opacity};
      active=false;mutations.forEach(o=>o.disconnect());observer?.disconnect();clearEvTimers();
      frames.sort((a,b)=>a-b);const percentile=p=>frames[Math.min(frames.length-1,Math.floor(frames.length*p))];
      return {stages,before,after,timing,performance:{frameSamples:frames.length,medianFrameMs:percentile(.5),p95FrameMs:percentile(.95),maxFrameMs:frames.at(-1),longTasksMs:longTasks,longTaskDetails,frameGaps}};
    }""")
    context.close()
    return result


def short_screen_scroll(browser,path,width,height):
    context=browser.new_context(viewport={"width":width,"height":height},is_mobile=True,has_touch=True,reduced_motion="reduce")
    context.route(re.compile(r"https?://"),lambda route:route.abort())
    page=context.new_page();page.goto(path.as_uri()+"?seed=42",wait_until="load")
    stages=[]
    for expected in range(5):
        stages.append({"step":expected,"visible":page.locator(f'[data-step="{expected}"]').is_visible(),"nextVisible":page.locator('#tutNext').is_visible()})
        if expected==4:
            page.keyboard.press('ArrowRight')
        page.locator('#tutNext').click(timeout=3000)
    closed=not page.locator('#tutModal').is_visible()
    page.keyboard.press('ArrowRight');page.wait_for_function('pending!==null');page.keyboard.press('Enter')
    page.keyboard.press('ArrowLeft');page.wait_for_function('pending!==null');page.keyboard.press('Enter')
    end_open=page.locator('#endModal').is_visible()
    page.locator('#ckSelect').select_option('jawed_fish')
    page.locator('#ckBtn').click(timeout=3000)
    checkpoint=page.evaluate('({node,pop,endClosed:$("endModal").classList.contains("hidden")})')
    context.close()
    return {"viewport":[width,height],"tutorialSteps":stages,"tutorialClosed":closed,"endingVisible":end_open,"checkpointAfterActualClick":checkpoint}


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--label",default="current")
    ap.add_argument("--baseline",type=Path,default=DEFAULT_BASELINE)
    ap.add_argument("--skip-ui",action="store_true",help="Baseline-only harness development; not final acceptance")
    ap.add_argument("--performance-repeats",type=int,default=3,help="Candidate normal-motion samples; repeated because iteration 2 showed one isolated long task")
    args=ap.parse_args()
    failures=[]
    def check(ok,message):
        if not ok: failures.append(message)
        return bool(ok)
    base={name:(args.baseline/name).read_bytes() for name in HASHES}
    current={name:(ROOT/name).read_bytes() for name in HASHES}
    report={"label":args.label,"baselineDirectory":str(args.baseline),"checks":{},"failures":failures}
    for name in HASHES:
        report["checks"][f"baselineHash:{name}"]=check(sha(base[name])==HASHES[name],f"Baseline corruption: {name}")
    old,new=Contract(base["index.html"].decode("utf-8-sig")),Contract(current["index.html"].decode("utf-8-sig"))
    script=game_script(base["index.html"])
    report["gameScriptSha256"]=sha(script)
    report["gameScriptBytes"]=len(script)
    report["fileBytes"]={k:len(v) for k,v in current.items()}
    report["candidateSha256"]={k:sha(v) for k,v in current.items()}
    report["checks"]["gameScriptByteExact"]=check(script==game_script(current["index.html"]),"Frozen game script changed")
    report["checks"]["legacyByteExact"]=check(base["evolution_swipe.html"]==current["evolution_swipe.html"],"Legacy file changed")
    report["checks"]["originalIdsAndTags"]=check(all(new.ids.get(k)==v for k,v in old.ids.items()),"Original DOM IDs/tags changed")
    report["checks"]["uniqueIds"]=check(not new.duplicates,"Duplicate DOM IDs")
    report["checks"]["dataContract"]=check(all(item in new.data for item in old.data),"Original data attributes changed")
    report["checks"]["tutorialSections"]=check(old.steps==new.steps,"Tutorial data-step order changed")
    report["originalIdCount"]=len(old.ids)
    report["candidateExternalResources"]=new.external
    if not args.skip_ui:
        report["checks"]["standaloneResources"]=check(not new.external,"External runtime dependencies remain")
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=True)
        baseline,base_meta=run_browser(browser,args.baseline/"index.html",True)
        candidate,candidate_meta=run_browser(browser,ROOT/"index.html")
        report["baselineBrowser"]=base_meta;report["candidateBrowser"]=candidate_meta
        for key in baseline:
            report["checks"][f"differential:{key}"]=check(canonical(baseline[key])==canonical(candidate[key]),f"Browser differential mismatch: {key}")
        report["coverage"]=candidate["engine"]["counts"]
        report["differentialSha256"]={"original":sha(canonical(baseline).encode()),"candidate":sha(canonical(candidate).encode())}
        report["checks"]["noCandidateJsErrors"]=check(not candidate_meta["pageErrors"],"Candidate JavaScript errors")
        if not args.skip_ui:
            report["checks"]["offlineNoRequests"]=check(not candidate_meta["networkRequests"],"Candidate made external network requests")
            report["ui"]=[]
            for mobile in [False,True]:
                try:
                    ui=ui_smoke(browser,ROOT/"index.html",mobile)
                    report["ui"].append(ui)
                    for key in ["tutorialVisible","tutorialSkipped","noHorizontalOverflow","resultNoHorizontalOverflow","cardHitTarget","continueVisible","treeVisible","keyboardProceeded"]:
                        check(ui[key],f"{'Mobile' if mobile else 'Desktop'} UI failed: {key}")
                    check(not ui["pageErrors"],"UI JavaScript errors")
                    check(not ui["networkRequests"],"UI external requests")
                except Exception as e:
                    failures.append(f"{'Mobile' if mobile else 'Desktop'} UI smoke: {e}")
            original_wheel=normal_roulette(browser,args.baseline/"index.html",True)
            candidate_wheel=normal_roulette(browser,ROOT/"index.html")
            report["normalMotionRoulette"]={"original":original_wheel,"candidate":candidate_wheel}
            report["checks"]["normalRouletteDifferential"]=check(all(canonical(original_wheel[k])==canonical(candidate_wheel[k]) for k in ["stages","before","after"]),"Normal-motion roulette differs from original")
            report["checks"]["normalRouletteOrder"]=check(candidate_wheel["stages"]==["chosen","spin","environment","verdict"],"Roulette reveal order changed")
            report["checks"]["normalRouletteAlignment"]=check(abs(candidate_wheel["after"]["actual"]-candidate_wheel["after"]["expected"])<.000001,"Roulette pointer mismatch")
            report["normalMotionRepeatedSamples"]=[candidate_wheel]
            for _ in range(max(0,args.performance_repeats-1)):
                repeat=normal_roulette(browser,ROOT/"index.html")
                report["normalMotionRepeatedSamples"].append(repeat)
                check(all(canonical(original_wheel[k])==canonical(repeat[k]) for k in ["stages","before","after"]),"Repeated roulette differs from original")
            report["shortScreenScrolling"]=[]
            for width,height in [(320,568),(844,390)]:
                try:
                    small=short_screen_scroll(browser,ROOT/'index.html',width,height)
                    report["shortScreenScrolling"].append(small)
                    check(all(x['visible'] and x['nextVisible'] for x in small['tutorialSteps']) and small['tutorialClosed'] and small['endingVisible'] and small['checkpointAfterActualClick']=={'node':'jawed_fish','pop':50,'endClosed':True},f'Short-screen tutorial/ending scrolling failed at {width}x{height}')
                except Exception as e:
                    failures.append(f'Short-screen {width}x{height}: {e}')
        browser.close()
    report["checks"]["candidateStableDuringAudit"]=check((ROOT/"index.html").read_bytes()==current["index.html"],"Candidate changed during audit; rerun on a stable iteration")
    report["pass"]=not failures
    if report["pass"]:
        snapshot=args.baseline/f"verified-{args.label}.html"
        snapshot.write_bytes(current["index.html"])
        report["verifiedSnapshot"]=str(snapshot)
    output=ROOT/"qa"/f"results-{args.label}.json"
    output.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
    print(json.dumps({"pass":report["pass"],"report":str(output),"coverage":report["coverage"],"failures":failures},ensure_ascii=False,indent=2))
    return 0 if report["pass"] else 1


if __name__=="__main__":
    raise SystemExit(main())
