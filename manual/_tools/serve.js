// 공용(공종 통합 포털): 저장소를 로컬 서버로 띄우고 구글폰트 요청을 매뉴얼 로컬 woff2로 대체 · 외부 요청 차단
const http=require('http'),fs=require('fs'),path=require('path');
const FD=path.join(__dirname,'..','assets','fonts');
const F=f=>'data:font/woff2;base64,'+fs.readFileSync(path.join(FD,f)).toString('base64');
function fontCSS(){return `@font-face{font-family:'Noto Sans KR';src:url(${F('NotoSansKR-var.woff2')}) format('woff2');font-weight:100 900}\n`+
 ['400','600','700'].map(w=>`@font-face{font-family:'JetBrains Mono';src:url(${F('JetBrainsMono-latin-'+w+'.woff2')});font-weight:${w}}`).join('\n');}
async function setup(ctx){const css=fontCSS();
  await ctx.route(/fonts\.googleapis\.com\/css/, r=>r.fulfill({status:200,contentType:'text/css',body:css}));
  await ctx.route(/^https?:\/\/(?!127\.0\.0\.1)(?!fonts\.googleapis)/, r=>r.abort());}
function server(repo,port){return new Promise(res=>{const s=http.createServer((q,w)=>{let p=decodeURIComponent(q.url.split('?')[0]);if(p.endsWith('/'))p+='index.html';
 fs.readFile(path.join(repo,p),(e,d)=>{if(e){w.writeHead(404);w.end();return;}const ext=path.extname(p);const ct={'.html':'text/html; charset=utf-8','.js':'application/javascript','.css':'text/css','.json':'application/json','.webp':'image/webp','.png':'image/png','.woff2':'font/woff2','.pdf':'application/pdf','.ico':'image/x-icon'}[ext]||'application/octet-stream';w.writeHead(200,{'Content-Type':ct});w.end(d);});});s.listen(port,()=>res(s));});}
module.exports={setup,server};
