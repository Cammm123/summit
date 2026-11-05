// Stand-in for the claude.ai runtime: an in-memory db and a fake grader.
// Loaded before the page script by run_page_test.py. Not used in production.
(()=>{
const days=[];for(let d=3;d<=18;d++)days.push('2026-11-'+String(d).padStart(2,'0'));
const store={
 'meta/path':{title:'Test Summit',course:'Test Course',student:'Sam',nodes:days.map(d=>d==='2026-11-09'?{date:d,kind:'camp',sub:'Quiz 1'}:d==='2026-11-18'?{date:d,kind:'peak',sub:'Exam 1'}:{date:d,kind:'day'})},
 'levels/2026-11-03':{date:'2026-11-03',target:'Quiz 1',daysLeft:6,why:'Test level.',primer:[{h:'Primer heading',body:'Primer body.'}],
   questions:[{id:'q1',tag:'Topic A',text:'Question one?',key:{mechanism:'Answer one.',mustHave:['point'],traps:[],slides:'L1 slide 2'}},
              {id:'q2',tag:'Topic B',text:'Question two?',key:{mechanism:'Answer two.',mustHave:['point'],traps:[],slides:'L2 slide 5'}}]},
 'levels/2026-11-04':{date:'2026-11-04',target:'Quiz 1',daysLeft:5,questions:[{id:'q1',text:'Done question?',key:{mechanism:'x'}}]},
 'answers/2026-11-04_q1':{date:'2026-11-04',qid:'q1',answer:'a',verdict:'right',gap:'',mechanism:'x',gradedBy:'claude'},
};
const subs=[];
const snap=p=>({id:p.split('/').pop(),exists:p in store,data:()=>store[p],metadata:{fromCache:false,hasPendingWrites:false}});
const fire=()=>subs.forEach(f=>f());
const coll=c=>({path:c,onSnapshot(next){const f=()=>{const docs=Object.keys(store).filter(k=>k.startsWith(c+'/')&&k.split('/').length===2).sort().map(snap);next({docs,size:docs.length,empty:!docs.length,metadata:{fromCache:false},docChanges:()=>[]})};subs.push(f);setTimeout(f,20);return()=>{}}});
const doc=p=>({path:p,id:p.split('/').pop(),get:async()=>snap(p),
  set:async d=>{store[p]=JSON.parse(JSON.stringify(d));setTimeout(fire,5)},
  update:async d=>{if(!(p in store))throw{code:'invalid_argument'};Object.assign(store[p],d);setTimeout(fire,5)},
  onSnapshot(next){const f=()=>next(snap(p));subs.push(f);setTimeout(f,20);return()=>{}}});
const sample=async(input,o)=>{window.__prompts.push(input);const t='Mock checkpoint text.';o&&o.onText&&o.onText({text:t});return{text:t}};
sample.json=async input=>{window.__prompts.push(input);await new Promise(r=>setTimeout(r,50));return{verdict:'partial',gotRight:'Named it',gap:'Missed the second step.',mechanism:'Both steps are needed.',slides:'L1 slide 2'}};
window.__prompts=[];window.__store=store;
if(!window.__noRuntime)window.claude={use:async n=>{await new Promise(r=>setTimeout(r,10));return n==='db'?{doc,collection:coll}:n==='sample'?sample:null}};
})();
