// Browser check after rollover: every /bah/ page 200, no console errors/failed requests, no overflow at 1280/390, yoy 24 rows visible, as-of stamp visible, year in H1. UNOFFICIAL / PERSONAL
// Usage: node rollover_browser.cjs http://127.0.0.1:<port> <NEW_YEAR> <slug,slug,...>
const puppeteer = require(process.env.PUPPETEER || '/workspace/build_v2/tools/node_modules/puppeteer-core');
const [BASE, NY, LIST] = process.argv.slice(2); const S = LIST.split(',');
let pass=0, fail=0; const ok=(c,m)=>{if(c)pass++;else{fail++;console.log('FAIL',m)}};
(async()=>{const b=await puppeteer.launch({executablePath:process.env.CHROME||'/usr/bin/google-chrome',args:['--no-sandbox'],headless:'new'});
for(const s of ['', ...S])for(const w of [1280,390]){const p=await b.newPage();const errs=[],bad=[];await p.setCacheEnabled(false);await p.setViewport({width:w,height:900});
 p.on('console',m=>{if(m.type()==='error')errs.push(m.text())});p.on('requestfailed',r=>{if(!/fonts\.g|googletagmanager|google-analytics/.test(r.url()))bad.push(r.url())});
 const url=BASE+'/bah/'+(s?s+'/':''); const r=await p.goto(url,{waitUntil:'networkidle0'}); ok(r.status()===200,url+' status '+r.status());
 const d=await p.evaluate(()=>({ov:document.documentElement.scrollWidth-window.innerWidth,h1:document.querySelector('h1').textContent,
   yr:document.querySelectorAll('#yoy tbody tr').length,yv:!!document.querySelector('#yoy')&&document.querySelector('#yoy').offsetHeight>0,
   st:!!document.querySelector('#asof')&&document.querySelector('#asof').offsetHeight>0}));
 ok(d.ov<=0,url+'@'+w+' overflow '+d.ov); ok(d.h1.includes(NY),url+' h1 year '+d.h1);
 if(s){ok(d.yr===24&&d.yv,url+' yoy rows '+d.yr);ok(d.st,url+' stamp');}
 ok(errs.length===0,url+' console '+errs); ok(bad.length===0,url+' failed '+bad); await p.close();}
await b.close(); console.log('pages',S.length+1,'PASS',pass,'FAIL',fail); process.exit(fail?1:0)})();
