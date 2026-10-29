// 건축 계산서 통합 포털 매뉴얼 화면 캡처 — usage: node capture_arch.js <repoDir> <outDir>  (1440×900 · DSF 1.25 · sw block)
const {chromium}=require('playwright');const fs=require('fs');const path=require('path');const {setup,server}=require('./serve');
const repo=path.resolve(process.argv[2]),out=path.resolve(process.argv[3]);fs.mkdirSync(out,{recursive:true});
const VW=1440,VH=900,DSF=1.25,PORT=8963;
// 설치 지원 브라우저 모사(beforeinstallprompt) · 안내 띠는 해당 캡처에서만 표시
const FAKE=`window.__fire=function(){var e=new Event('beforeinstallprompt');e.prompt=function(){};e.userChoice=Promise.resolve({outcome:'dismissed'});window.dispatchEvent(e);};`;
const HIDEBAR='.pwa-bar{display:none!important}html{scroll-behavior:auto!important}';
const HELP=`window.__vis=e=>e&&e.getClientRects().length>0;
window.__find=sel=>{if(sel.startsWith('nth:')){const [q,i]=sel.slice(4).split('|');return [...document.querySelectorAll(q)].filter(__vis)[+i]||null;}
 if(sel.startsWith('card:')){const t=sel.slice(5);return [...document.querySelectorAll('.tcard')].find(c=>c.textContent.includes(t)&&__vis(c))||null;}
 if(sel.startsWith('row:')){const t=sel.slice(4);return [...document.querySelectorAll('table tbody tr')].find(r=>r.textContent.includes(t)&&__vis(r))||null;}
 for(const s of sel.split(',')){const e=[...document.querySelectorAll(s)].find(__vis);if(e)return e;}return null;};
window.__tab=t=>{document.querySelector('.tab[data-tab="'+t+'"]').click();};`;
const SHOTS=[
 {id:'s01_overview',pre:"__tab('all');window.scrollTo(0,0)",clip:'viewport',m:[['.pill','근거 조문 대조일'],['.ttl','포털 이름'],['.stats','요약 5칸'],['.tabs','분류 탭 · 근거 · 매뉴얼 · 앱 설치'],['nth:.tcard|0','계산서 카드']]},
 {id:'s02_header',clip:'.hd',m:[['.pill','근거 조문 대조일'],['.brand','ARCHITECT KIM MANMIN'],['.ttl','건축 계산서 통합 포털'],['.lead','포털 설명']]},
 {id:'s03_tabs',clip:'.tabs',m:[['nth:.tab|0','전체 10'],['nth:.tab|1','인허가·법규 4'],['nth:.tab|2','에너지 2'],['nth:.tab|3','대가·감리·공기 4'],['nth:.tab|4','근거 법령·고시'],['nth:.tab-man|0','사용자 매뉴얼'],['#pwa-inst','앱 설치']]},
 {id:'s04_permit',clip:'#g-permit',m:[['card:용도변경','35 용도변경 판정'],['card:건폐율','36 건폐율 · 용적률'],['card:일조','38 일조 · 사선 제한'],['card:주차','40 부설주차장 법정대수']]},
 {id:'s05_energy',clip:'#g-energy',m:[['card:열관류율','31 열관류율 검토'],['card:EPI','39 에너지성능지표']]},
 {id:'s06_fee',clip:'#g-fee',m:[['card:설계 · 감리','30 설계 · 감리 대가'],['card:해체','32 해체공사 감리대가'],['card:상주','33 상주감리 대가'],['card:공사기간','34 공사기간 산정']]},
 {id:'s07_card',clip:'nth:.tcard|0',m:[['nth:.tc-no|0','공종 번호(A · 폴더 번호)'],['nth:.tc-ver|0','계산서 현재 버전'],['nth:.tc-name|0','계산서 이름'],['nth:.tc-desc|0','계산 내용'],['nth:.tc-chips|0','근거 기준 칩'],['nth:.tc-man|0','사용자 매뉴얼(새 창)'],['nth:.tc-go|0','계산서 열기']]},
 {id:'s08_law',clip:'#law',m:[['row:건축법 시행령','건축법 · 시행령'],['row:국토의 계획','국토계획법 · 시행령'],['row:주차장법','주차장법 · 시행령'],['row:에너지절약','에너지절약설계기준 — 제2026-360호'],['row:건축물관리법','해체감리'],['row:건축사법','건축사 대가기준'],['nth:.note|1','개정 예정 — 건축법 제61조①']]},
 {id:'s13_install_bar',pre:"document.getElementById('mm-hidebar').disabled=true;window.scrollTo(0,0)",wait:500,clip:'#pwa-bar',post:"document.getElementById('mm-hidebar').disabled=false",m:[['.pwa-bar-t','설치 안내'],['#pwa-no','닫기 — 이 세션 동안 다시 띄우지 않음'],['#pwa-yes','설치 — 브라우저 설치 창']]},
 {id:'s09_permit_tab',pre:"__tab('permit');window.scrollTo(0,0)",wait:600,clip:'viewport',post:"__tab('all')",m:[['nth:.tab|1','인허가·법규만 보기'],['#g-permit','인허가·법규 카드 4장']]},
];
(async()=>{
 const s=await server(repo,PORT);const b=await chromium.launch();
 const ctx=await b.newContext({viewport:{width:VW,height:VH},deviceScaleFactor:DSF,serviceWorkers:'block',locale:'ko-KR'});await setup(ctx);
 const pg=await ctx.newPage();await pg.addInitScript(FAKE);const errs=[];pg.on('pageerror',e=>errs.push(e.message));
 await pg.goto(`http://127.0.0.1:${PORT}/index.html`);await pg.addStyleTag({content:HIDEBAR}).then(h=>h.evaluate(e=>e.id='mm-hidebar'));await pg.evaluate(()=>document.fonts.ready);await pg.evaluate(()=>__fire());await pg.waitForTimeout(2400);await pg.evaluate(HELP);
 const meta={};
 for(const S of SHOTS){
  if(S.pre){try{await pg.evaluate(S.pre);}catch(e){errs.push(S.id+' pre '+e.message);}}
  await pg.waitForTimeout(S.wait||400);
  if(S.clip!=='viewport'){await pg.evaluate(c=>{const e=__find(c);if(e){window.scrollTo(0,e.getBoundingClientRect().top+scrollY-40);}},S.clip);await pg.waitForTimeout(300);}
  const info=await pg.evaluate(({S,VW,VH})=>{
   const abs=e=>{const r=e.getBoundingClientRect();return {x:r.left+scrollX,y:r.top+scrollY,w:r.width,h:r.height};};
   let clip;
   if(S.clip==='viewport'){clip={x:0,y:scrollY,width:VW,height:VH};}
   else{const el=__find(S.clip);if(!el)return {err:'clip '+S.clip};const a=abs(el);const P=12;clip={x:Math.max(0,a.x-P),y:Math.max(0,a.y-P),width:a.w+2*P,height:a.h+2*P};}
   const marks=[];(S.m||[]).forEach(([sel,label],i)=>{const e=__find(sel);if(!e){marks.push({n:i+1,label,miss:sel});return;}const a=abs(e);
     marks.push({n:i+1,label,x:+((a.x-clip.x)/clip.width*100).toFixed(2),y:+((a.y-clip.y)/clip.height*100).toFixed(2),w:+(Math.min(a.w,clip.x+clip.width-a.x)/clip.width*100).toFixed(2),h:+(Math.min(a.h,clip.y+clip.height-a.y)/clip.height*100).toFixed(2)});});
   return {clip,marks};},{S,VW,VH});
  if(info.err){errs.push(S.id+' '+info.err);continue;}
  const c=info.clip;const cl={x:Math.max(0,c.x),y:Math.max(0,c.y),width:Math.min(c.width,VW-Math.max(0,c.x)),height:c.height};
  if(S.clip==='viewport'){await pg.screenshot({path:path.join(out,S.id+'.png'),clip:{x:0,y:0,width:VW,height:VH}});}
  else{await pg.screenshot({path:path.join(out,S.id+'.png'),clip:cl,fullPage:true});}
  meta[S.id]={w:Math.round(cl.width),h:Math.round(cl.height),marks:info.marks};
  if(S.post){try{await pg.evaluate(S.post);}catch(e){errs.push(S.id+' post '+e.message);}await pg.waitForTimeout(300);}
 }
 // 홈페이지 카드용 전체 화면 1800×1125 (1440×900 × 1.25)
 await pg.evaluate(()=>window.scrollTo(0,0));await pg.waitForTimeout(300);
 await pg.screenshot({path:path.join(out,'_full_1440.png'),clip:{x:0,y:0,width:VW,height:VH}});
 const mctx=await b.newContext({viewport:{width:390,height:844},deviceScaleFactor:2,serviceWorkers:'block',isMobile:true,hasTouch:true,locale:'ko-KR',userAgent:'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1'});await setup(mctx);
 const mp=await mctx.newPage();await mp.goto(`http://127.0.0.1:${PORT}/index.html`);await mp.addStyleTag({content:HIDEBAR}).then(h=>h.evaluate(e=>e.id='mm-hidebar'));await mp.waitForTimeout(2400);
 await mp.screenshot({path:path.join(out,'s10_mobile_top.png')});meta['s10_mobile_top']={w:390,h:844,marks:[]};
 await mp.evaluate(()=>{const e=document.getElementById('g-permit');window.scrollTo(0,e.getBoundingClientRect().top+scrollY-12);});await mp.waitForTimeout(400);
 await mp.screenshot({path:path.join(out,'s11_mobile_card.png')});meta['s11_mobile_card']={w:390,h:844,marks:[]};
 await mp.evaluate(()=>{const e=document.getElementById('law');window.scrollTo(0,e.getBoundingClientRect().top+scrollY-12);});await mp.waitForTimeout(400);
 await mp.screenshot({path:path.join(out,'s12_mobile_law.png')});meta['s12_mobile_law']={w:390,h:844,marks:[]};

 await mp.evaluate(()=>{window.scrollTo(0,0);document.getElementById('pwa-inst').click();});await mp.waitForTimeout(400);
 await mp.screenshot({path:path.join(out,'s14_ios_guide.png')});meta['s14_ios_guide']={w:390,h:844,marks:[]};
 await mp.evaluate(()=>document.getElementById('ios-ok').click());
 const mob=await mp.evaluate(()=>({page:document.documentElement.scrollWidth,vw:innerWidth}));
 fs.writeFileSync(path.join(out,'_marks.json'),JSON.stringify(meta,null,1));
 const miss=[];Object.entries(meta).forEach(([k,v])=>v.marks.forEach(m=>{if(m.miss)miss.push(k+':'+m.miss);else if(m.x<0||m.y<0||m.x+m.w>100.5||m.y+m.h>100.5||m.w<=0||m.h<=0)miss.push(k+':OUT '+m.label);}));
 console.log(JSON.stringify({mobile:mob,sizes:Object.fromEntries(Object.entries(meta).map(([k,v])=>[k,v.w+'x'+v.h])),miss,errs},null,1));
 await b.close();s.close();
})();
