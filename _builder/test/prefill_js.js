const PCS=require('/workspace/site_v2/assets/pcs.js');
const P=PCS.PCS||PCS; const cases=require('./prefill_cases.json');
let bad=0;
for(const c of cases){
  const row=P.referralRow({destination:c.p,first_name:c.f,rank:P.rankLabel(c.g),num_dependents:c.n,email_address:c.e.trim()});
  const u=P.prefillUrl(row);
  if(u!==c.url){ if(bad++<3) console.log('MISMATCH\n',c.url,'\n',u); }
}
console.log('cases',cases.length,'mismatch',bad);
