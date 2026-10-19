// Browser check for the 8 deepened BAH pages: 200, console errors, failed requests, 390/1280 horizontal overflow, yoy table rendered, other-posts count. UNOFFICIAL / PERSONAL
const puppeteer = require('/workspace/build_v2/tools/node_modules/puppeteer-core');
const BASE = process.argv[2]; const S=['fort-bragg','fort-hood','fort-campbell','fort-carson','joint-base-lewis-mcchord','fort-drum','fort-bliss','national-capital-region'];
let pass=0,fail=0; const ok=(c,m)=>{if(c)pass++;else{fail++;console.log('FAIL',m)}};
(async()=>{const b=await puppeteer.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox'],headless:'new'});
for(const s of S)for(const w of [1280,390]){const p=await b.newPage();const errs=[],bad=[];await p.setViewport({width:w,height:900});
p.on('console',m=>{if(m.type()==='error')errs.push(m.text())});p.on('requestfailed',r=>{if(!/fonts\.g/.test(r.url()))bad.push(r.url())});
const r=await p.goto(BASE+'/bah/'+s+'/',{waitUntil:'networkidle0'});ok(r.status()===200,s+' status');
const d=await p.evaluate(()=>({ov:document.documentElement.scrollWidth-window.innerWidth,yr:document.querySelectorAll('#yoy tbody tr').length,yv:document.querySelector('#yoy').offsetHeight>0,op:document.querySelectorAll('ul.bases li a').length,st:!!document.querySelector('#asof')&&document.querySelector('#asof').offsetHeight>0}));
ok(d.ov<=0,s+'@'+w+' overflow '+d.ov);ok(d.yr===24&&d.yv,s+' yoy');ok(d.op===19,s+' other posts '+d.op);ok(d.st,s+' stamp visible');
ok(errs.length===0,s+' console '+errs);ok(bad.length===0,s+' failed '+bad);await p.close();}
await b.close();console.log('pages',S.length,'PASS',pass,'FAIL',fail)})();
