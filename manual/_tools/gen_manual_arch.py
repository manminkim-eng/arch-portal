# -*- coding: utf-8 -*-
"""건축 계산서 통합 포털 사용자 매뉴얼 생성기 (MANMIN 매뉴얼 공통 엔진 v-mh1 · 안내형 도구 — 계산 예제 없음)
   실행: MANUAL_DIR=<manual 폴더> python gen_manual_arch.py  →  <manual>/index.html
   도구·근거 데이터는 ../../_tools/build_portal.py 의 TOOLS · GROUPS · LAWS 를 그대로 읽는다(단일 원천).
   근거(LawMCP 대조 2026-10-30): 건축법(2026-02-27) · 시행령(2026-10-06) · 국토계획법(2026-07-01) · 시행령(2026-09-18) ·
   주차장법 · 시행령(2026-08-28) · 녹색건축법(2026-09-18) · 에너지절약설계기준 제2026-360호(2026-07-08) · 건축물관리법(2025-06-04) ·
   해체감리 기준 제2022-446호 · 건축사법(2026-09-18) · 엔지니어링산업 진흥법(2026-06-03) · 건설기술 진흥법(2025-10-01).
   개정 예정: 건축법 제61조제1항 — 법률 제21880호(2026-08-11 공포) 2026-11-12 시행(부칙 제1조 단서 · 제4조)."""
import os, sys, io, runpy, contextlib
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from manual_engine import fig, T, render, B, MARKS

with contextlib.redirect_stdout(io.StringIO()):
    D = runpy.run_path(os.path.join(HERE, '..', '..', '_tools', 'build_portal.py'))
TOOLS, GROUPS, LAWS, APPVER, CHECKED = D['TOOLS'], D['GROUPS'], D['LAWS'], D['VER'], D['CHECKED']

VER, DATE = 'Ver-1.0', '2026-10-30'
PDF = '건축통합포털_사용자매뉴얼_Ver-1.0.pdf'
APP_URL = 'https://manminkim-eng.github.io/arch-portal/'
APP = '건축 계산서 통합 포털'
G = 'https://manminkim-eng.github.io/'
def F(sid, cap, legend=None, **kw):
    if legend is None:
        legend = [k['label'] for k in MARKS.get(sid, {}).get('marks', [])] or None
    return fig(sid, cap, legend, **kw)
K = lambda t: '<div class="k1">' + t + '</div>'
BR = lambda t: '<div class="brk">' + t + '</div>'
EXTRA_CSS = """<style>
#fig-s07_card{max-width:420px}
#fig-s13_install_bar{max-width:640px}
.k1 td:first-child,.k1 th:first-child{white-space:nowrap}
.lawt td,.lawt th{word-break:keep-all}.lawt td:nth-child(2){white-space:nowrap}.lawt td:first-child{min-width:9em}
.tri{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;align-items:start}
@media (max-width:760px){.tri{grid-template-columns:1fr}}
@media print{
  figure.shot{max-width:none!important}
  figure.shot .frame{width:fit-content;max-width:100%}
  figure.shot img{width:auto;height:auto;max-width:100%;max-height:118mm}
  figure.narrow img{max-height:105mm}
  #fig-s13_install_bar .frame{width:120mm!important}#fig-s13_install_bar img{width:120mm!important;max-height:none}
  .tri{grid-template-columns:repeat(3,1fr)}
  .brk .tbl{break-inside:auto}.brk tr{break-inside:avoid}.brk thead{display:table-header-group}
}
</style>"""
GNAME = {g: n for g, n, _ in GROUPS}
NG = {g: sum(1 for t in TOOLS if t[1] == g) for g, _, _ in GROUPS}
tool_rows = [[GNAME[t[1]], t[0], f'<a href="{G}{t[4]}/" target="_blank" rel="noopener">{t[2]}</a>', 'Ver ' + t[5], ' · '.join(t[8]),
              f'<a href="{G}{t[4]}/manual/" target="_blank" rel="noopener">매뉴얼</a>'] for t in TOOLS]
law_rows = [[n, k, d, a, t] for n, k, d, a, t in LAWS]
TOC = [
 ('ch0', '0. 이 매뉴얼에 대하여', []),
 ('ch1', '1. 한눈에 보기', [('s1-1', '화면 구성'), ('s1-2', f'연결 계산서 {len(TOOLS)}종')]),
 ('ch2', '2. 1분 따라하기', []),
 ('ch3', '3. 화면별 기능', [('s3-1', '머리'), ('s3-2', '분류 탭'), ('s3-3', '계산서 카드'), ('s3-4', '인허가·법규'), ('s3-5', '에너지'), ('s3-6', '대가·감리·공기'), ('s3-7', '근거 법령·고시'), ('s3-8', '휴대전화 화면'), ('s3-9', '앱 설치')]),
 ('ch4', '4. 근거 해설', [('s4-1', '근거 체계'), ('s4-2', '조례 값과 개정 예정'), ('s4-3', '포털과 계산서의 역할')]),
 ('ch5', '5. 문제 해결·FAQ', []),
 ('ch6', '부록', [('a1', '버전 변경 내역'), ('a2', '용어')]),
]
S_ = []
S_.append(f"""{EXTRA_CSS}<section class="ch" id="ch0"><h2><span class="n">00</span>이 매뉴얼에 대하여</h2>
<p class="lead">{APP}은 용도변경 · 건폐율·용적률 · 일조 · 부설주차장 · 열관류율 · 에너지성능지표 · 설계·감리 대가 · 해체감리 · 상주감리 · 공사기간까지 <b>MANMIN 건축 계산서 {len(TOOLS)}종의 진입 화면</b>입니다. 포털은 계산하지 않습니다. 카드를 눌러 계산서로 들어가고, 계산서마다 적용한 근거 법령과 고시를 한 화면에서 확인합니다.</p>
{K(T([
 ['대상 프로그램', f'{APP} <b>Ver {APPVER}</b>'],
 ['접속 주소', f'<a href="{APP_URL}" target="_blank" rel="noopener">manminkim-eng.github.io/arch-portal</a>'],
 ['매뉴얼 판', f'<b>{VER}</b> · {DATE} · 작성 김만민 건축사(㈜대성건축사사무소)'],
 ['내려받기', f'<a href="{PDF}" download>PDF(A4)</a> · <a href="../index.html">포털 열기</a>'],
 ['근거 대조', f'국가법령정보(LawMCP) {CHECKED} — 법령은 현행 시행일 · 조문 제목, 행정규칙(고시)은 발령일 · 시행일'],
 ['범위', '안내 · 연결 도구 — 수치 기준과 계산은 각 계산서에서 합니다'],
], ['항목', '내용']))}
<div class="note"><b>표기</b>그림 위 주황색 번호(①②…)는 그림 아래 범례 번호와 같습니다. 그림을 누르면 크게 볼 수 있습니다.</div>
<div class="warn"><b>책임 한계</b>포털은 근거 조문 · 시행일만 안내합니다. 요율 · 한도 · 이격거리 · 주차대수 등 수치 기준과 판정은 각 계산서의 산출근거표, 법령 · 고시 원문, 해당 지방자치단체 조례로 확인하십시오.</div>
</section>""")
S_.append(f"""<section class="ch" id="ch1"><h2><span class="n">01</span>한눈에 보기</h2>
<p class="lead">설치 없이 브라우저에서 바로 열리는 단일 페이지(PWA)입니다. 입력값이 없고, 연결과 근거 안내만 합니다.</p>
<h3 id="s1-1">1-1. 화면 구성</h3>
{F('s01_overview', '첫 화면')}
{K(T([
 ['머리', '근거 조문 대조일, 포털 이름, 설명'],
 ['요약 5칸', f'계산서 {len(TOOLS)}종(인허가 {NG["permit"]} · 에너지 {NG["energy"]} · 대가 {NG["fee"]}) · 근거 법령 · 고시 {len(LAWS)}행 · 조례 · PWA · A4'],
 ['탭 막대', '전체 · 인허가·법규 · 에너지 · 대가·감리·공기 / 근거 법령·고시 / 사용자 매뉴얼 / 앱 설치(설치할 수 있는 브라우저에서만)'],
 ['계산서 카드', '카드를 누르면 계산서, 「사용자 매뉴얼」을 누르면 그 계산서의 매뉴얼(새 창)'],
 ['근거 법령 · 고시', f'법령 · 고시 {len(LAWS)}행 — 현행 시행일(고시는 번호 · 발령일) · 관련 조문 · 적용 도구, 아래에 안내와 개정 예정'],
], ['영역', '내용']))}
<h3 id="s1-2">1-2. 연결 계산서 {len(TOOLS)}종</h3>
{BR(K(T(tool_rows, ['분류', '번호', '계산서', '버전', '근거 기준', '매뉴얼'])))}
</section>""")
S_.append(f"""<section class="ch" id="ch2"><h2><span class="n">02</span>1분 따라하기</h2>
<p class="lead">예: 근린생활시설을 다른 용도로 바꾸려는 건축물 — 포털에서 계산서를 찾아 들어가고 근거를 확인하는 순서입니다.</p>
<ol class="steps">
<li><b class="t">① 포털 열기</b>manminkim-eng.github.io/arch-portal — 탭 막대의 「앱 설치」로 홈 화면에 설치할 수 있습니다(<a href="#s3-9">3-9</a>).</li>
<li><b class="t">② 분류</b>「인허가·법규」 탭을 누르면 용도변경 · 건폐율·용적률 · 일조 · 부설주차장 카드 4장만 남습니다(<a href="#s3-2">3-2</a>).</li>
<li><b class="t">③ 근거 확인</b>용도변경 판정 카드의 칩 「건축법 제19조」 「시행령 제14조」를 확인합니다(<a href="#s3-4">3-4</a>).</li>
<li><b class="t">④ 매뉴얼</b>카드 아래 「사용자 매뉴얼」 — 그 계산서의 매뉴얼이 새 창으로 열립니다.</li>
<li><b class="t">⑤ 계산서</b>카드를 누르면 계산서로 이동해 허가 · 신고 · 대장 기재변경 대상을 판정하고, 같은 방법으로 부설주차장 계산서에서 추가 확보 대수를 확인합니다.</li>
<li><b class="t">⑥ 시행일 확인</b>포털 아래 「근거 법령 · 고시」 표에서 현행 시행일과 개정 예정을 확인합니다(<a href="#s3-7">3-7</a>).</li>
</ol>
{F('s09_permit_tab', '「인허가·법규」 탭')}
</section>""")
S_.append(f"""<section class="ch" id="ch3"><h2><span class="n">03</span>화면별 기능</h2>
<h3 id="s3-1">3-1. 머리</h3>
{F('s02_header', '머리')}
<p>맨 위 표시줄은 근거 조문을 국가법령정보와 대조한 날짜({CHECKED})입니다.</p>
<h3 id="s3-2">3-2. 분류 탭</h3>
{F('s03_tabs', '탭 막대')}
<p>「전체 {len(TOOLS)}」 · 「인허가·법규 {NG['permit']}」 · 「에너지 {NG['energy']}」 · 「대가·감리·공기 {NG['fee']}」는 누르면 해당 묶음만 보여 줍니다. 「근거 법령·고시」는 아래 근거표로 이동하고, 「사용자 매뉴얼」은 이 문서를 새 창으로 엽니다(온라인 전용). 「앱 설치」는 설치할 수 있는 브라우저에서만 나타납니다(<a href="#s3-9">3-9</a>).</p>
<h3 id="s3-3">3-3. 계산서 카드</h3>
{F('s07_card', '계산서 카드 구성')}
<p>카드 위 번호 「A · 35」는 홈페이지 도구 허브의 공종 표기(A)와 개발 폴더 번호(35)입니다. 버전은 계산서의 현재 판이고, 칩은 그 계산서가 산출근거로 인용하는 법령 · 고시입니다.</p>
<h3 id="s3-4">3-4. 인허가·법규</h3>
{F('s04_permit', f'인허가·법규 카드 {NG["permit"]}장')}
<h3 id="s3-5">3-5. 에너지</h3>
{F('s05_energy', f'에너지 카드 {NG["energy"]}장')}
<h3 id="s3-6">3-6. 대가·감리·공기</h3>
{F('s06_fee', f'대가·감리·공기 카드 {NG["fee"]}장')}
<h3 id="s3-7">3-7. 근거 법령 · 고시</h3>
{F('s08_law', '근거 법령 · 고시 표')}
<p>표 아래 첫 안내문은 포털의 원칙(근거 · 시행일만 안내, 수치 기준은 계산서)과 조례 확인 사항이고, 두 번째는 시행을 앞둔 개정(<a href="#s4-2">4-2</a>)입니다. 조문 원문은 국가법령정보센터에서 확인합니다.</p>
<h3 id="s3-8">3-8. 휴대전화 화면</h3>
<div class="tri"><div>{fig('s10_mobile_top', '첫 화면', narrow=True)}</div><div>{fig('s11_mobile_card', '카드', narrow=True)}</div><div>{fig('s12_mobile_law', '근거표', narrow=True)}</div></div>
<p>좁은 화면에서는 카드가 한 줄씩 쌓이고, 근거표는 좌우로 밀어서 봅니다.</p>
<h3 id="s3-9">3-9. 앱 설치</h3>
{F('s13_install_bar', '첫 방문 설치 안내 띠')}
{K(T([
 ['크롬 · 엣지 · 삼성인터넷 등', '탭 막대 「앱 설치」 또는 안내 띠의 「설치」 → 브라우저 설치 창에서 설치'],
 ['아이폰 · 아이패드', '「앱 설치」를 누르면 안내 상자 — 공유 단추 → 「홈 화면에 추가」 → 「추가」'],
 ['안내 띠', '첫 방문 2초 뒤 한 번 표시 — 「닫기」를 누르면 그 세션 동안 다시 띄우지 않음'],
 ['나타나지 않는 경우', '이미 설치한 앱 화면 · 설치를 지원하지 않는 브라우저(데스크톱 파이어폭스 등) · 설치를 막 거절한 직후'],
 ['설치 범위', '이 포털(/arch-portal/)만 설치됩니다 — 카드에서 연 계산서는 앱 안의 브라우저 창으로 열리고, 계산서도 앱으로 쓰려면 각 계산서에서 설치합니다'],
], ['구분', '방법']))}
<div class="tri"><div>{fig('s14_ios_guide', '아이폰 설치 안내', narrow=True)}</div><div></div><div></div></div>
</section>""")
S_.append(f"""<section class="ch" id="ch4"><h2><span class="n">04</span>근거 해설</h2>
<h3 id="s4-1">4-1. 근거 체계</h3>
<div class="lawt">{BR(T(law_rows, ['법령 · 기준', '구분', '현행', '관련 조문 · 코드', '적용 도구']))}</div>
<h3 id="s4-2">4-2. 조례 값과 개정 예정</h3>
{K(T([
 ['조례 위임', '건폐율 · 용적률(국토계획법 제77조 · 제78조 → 도시·군계획조례), 일조 이격거리(건축법 시행령 제86조제1항 → 건축조례), 부설주차장(주차장법 시행령 제6조 → 주차장 조례)은 법령이 정한 범위 안에서 지방자치단체 조례가 값을 정합니다'],
 ['건축법 제61조제1항', '법률 제21880호(2026-08-11 공포) — <b>2026-11-12 시행</b>. 정북방향 이격거리를 법률에서 높이 구간별 범위로 정하고, 인접 대지가 주거지역이 아닌 경우 등의 예외 단서를 둡니다. 시행 이후 건축허가를 신청(건축위원회 심의 신청 포함)하거나 건축신고를 하는 경우부터 적용합니다(부칙 제1조 단서 · 제4조)'],
 ['주차장법 시행령', '2026-08-25 개정(2026-08-28 시행) — 제6조 · 별표 1. 별표 1의 학생용 기숙사 · 데이터센터 항목은 부설주차장 계산서(40)에 반영되어 있습니다'],
], ['구분', '내용']))}
<h3 id="s4-3">4-3. 포털과 계산서의 역할</h3>
{K(T([
 ['포털', '계산서 진입 · 분류 · 근거 법령과 시행일 · 고시 발령일 안내 — 수치 기준을 싣지 않습니다'],
 ['계산서', '입력 · 계산 · 판정 · 산출근거표 · A4 계산서 — 수치 기준과 조항은 계산서가 정본입니다'],
 ['갱신', '법령이 바뀌면 계산서를 먼저 고치고, 포털 근거표는 시행일 · 번호만 고칩니다(데이터 단일 원천 _tools/build_portal.py)'],
], ['구분', '역할']))}
</section>""")
S_.append(f"""<section class="ch" id="ch5"><h2><span class="n">05</span>문제 해결·FAQ</h2>
{K(T([
 ['포털에서 계산이 되나요', '아닙니다 — 카드를 눌러 각 계산서에서 계산합니다'],
 ['「사용자 매뉴얼」이 안 열려요', '매뉴얼은 온라인 전용입니다(오프라인 캐시에서 제외)'],
 ['수치 기준은 어디 있나요', '각 계산서의 산출근거표와 A4 계산서에 있습니다 — 조례 값은 해당 지방자치단체 조례를 확인합니다'],
 ['「앱 설치」 단추가 안 보여요', '이미 설치했거나, 설치를 지원하지 않는 브라우저입니다 — 크롬 · 엣지에서 열어 보십시오(<a href="#s3-9">3-9</a>)'],
 ['설치한 앱에서 계산서가 브라우저 창으로 열려요', '정상입니다 — 설치 범위가 포털뿐이라서입니다. 계산서도 각자 설치할 수 있습니다'],
 ['계산서마다 디자인이 달라요', '계산서는 각각 별도 저장소의 도구라 헤드 색과 판이 다를 수 있습니다'],
 ['화면이 예전 판이에요', '새로 고침(Ctrl+F5) 또는 앱을 닫았다 다시 여십시오 — 판이 바뀌면 캐시 이름이 바뀝니다'],
], ['증상', '해결']))}
</section>""")
S_.append(f"""<section class="ch" id="ch6"><h2><span class="n">부록</span></h2>
<h3 id="a1">A1. 버전 변경 내역</h3>
{K(T([
 [f'Ver {APPVER} · 매뉴얼 {VER} ({DATE})', f'신설 — 계산서 {len(TOOLS)}종 · 분류 3 · 근거 법령 · 고시표 · 개정 예정 안내 · 앱 설치 단추 · 사용자 매뉴얼'],
], ['버전', '내용']))}
<h3 id="a2">A2. 용어</h3>
{BR(K(T([
 ['시설군', '건축법 제19조제4항의 9개 시설군 — 상위군으로 바꾸면 허가, 하위군이면 신고, 같은 시설군 안이면 건축물대장 기재내용 변경'],
 ['도시·군계획조례', '국토계획법이 정한 범위에서 건폐율 · 용적률 등을 정하는 지방자치단체 조례'],
 ['에너지성능지표(EPI)', '에너지절약계획서의 항목별 평점 합계 — 건축물의 에너지절약설계기준 제15조'],
 ['발령 · 시행', '행정규칙(고시)은 발령일과 시행일이 다를 수 있습니다 — 근거표는 국가법령정보에 표시된 날짜를 적었습니다'],
 ['PWA', '홈 화면에 설치해 오프라인에서도 여는 웹앱'],
], ['용어', '뜻'])))}
</section>""")
html = render(title=f'{APP} 사용자 매뉴얼 {VER} · MANMIN',
              desc=f'{APP} 사용자 매뉴얼 — 연결 계산서 {len(TOOLS)}종, 근거 법령 · 고시 안내',
              eyebrow='MANMIN ENGINEERING · USER MANUAL', h1=f'{APP} 사용자 매뉴얼',
              sub='카드 → 계산서 · 매뉴얼 → 분류 → 근거 법령 · 시행일', ver=VER, date=DATE, app_name='통합 포털',
              pdf=PDF, toc=TOC, sections=S_, foot_note='건축법 · 국토계획법 · 주차장법 · 에너지절약설계기준 제2026-360호(2026-07-08) — 대조 2026-10-30')
html = html.replace('화면 대응 개정 2026-10-12', '화면 대응 개정 ' + DATE)
open(os.path.join(B, 'index.html'), 'w', encoding='utf-8').write(html)
print('manual ok', len(html))
