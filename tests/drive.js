// Scenario driver: runs after the page loads, writes results into <pre id="test-result">.
setTimeout(async()=>{
 const wait=ms=>new Promise(r=>setTimeout(r,ms));
 const click=t=>{const b=[...document.querySelectorAll('button')].find(x=>x.textContent.trim()===t);if(b)b.click();return !!b};
 const R={scenario:window.__scenario};
 try{
  if(R.scenario==='map'){
   R.h1=document.getElementById('h1').textContent;
   R.levels=document.querySelectorAll('#levels .lvl').length;
   R.unlocked=document.querySelectorAll('#levels .lvl:not(.locked)').length;
   R.listButtons=document.querySelectorAll('#list .lvlbtn').length;
   R.climber=document.getElementById('climber').getAttribute('transform')||'';
   R.sub=document.getElementById('sub').textContent;
  }else if(R.scenario==='level'){
   R.primer=click('Start climbing');await wait(150);
   const ta=document.querySelector('textarea');ta.value='My answer.';ta.dispatchEvent(new Event('input'));
   click('Submit');await wait(500);
   R.pill1=(document.querySelector('.pill')||{}).textContent;
   R.verdict1=(window.__store['answers/2026-11-03_q1']||{}).verdict;
   R.gradePromptHasCourse=window.__prompts.some(p=>typeof p==='string'&&p.includes('Test Course')&&p.includes('Answer one.'));
   R.gradePromptClean=!window.__prompts.some(p=>typeof p==='string'&&/Cameron|03-121|Carnegie/.test(p));
   click('Next question');await wait(150);
   click('Skip, show me');await wait(400);
   R.verdict2=(window.__store['answers/2026-11-03_q2']||{}).verdict;
   click('Finish level');await wait(500);
   R.summary=!!document.querySelector('#levelView h2')&&document.querySelector('#levelView h2').textContent;
   R.checkpoint=(window.__store['checkpoints/2026-11-03']||{}).text||null;
  }else if(R.scenario==='noruntime'){
   await wait(200);R.note=document.getElementById('note').textContent;
  }
 }catch(e){R.error=String(e)}
 const pre=document.createElement('pre');pre.id='test-result';pre.textContent=JSON.stringify(R);document.body.appendChild(pre);
},700);
