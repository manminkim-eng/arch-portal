# -*- coding: utf-8 -*-
"""
MANMIN 건축 계산서 통합 포털 — index.html 생성기
  · 도구·근거 데이터는 아래 TOOLS / LAWS 한 곳에서만 관리한다.
  · 원칙(2026-10-29 MIN 승인): 포털에는 근거 조문·시행일만 싣고, 수치 기준은 각 계산서에 둔다.
  · 근거 확인: LawMCP(국가법령정보) 2026-10-30 조회 — 법령 현행 시행일 · 조문 제목, 행정규칙 발령일.
사용: python build_portal.py  →  ../index.html
"""
import html, os, datetime

VER = "1.0.0"   # 1.0.0 (2026-10-30) 신설 — 계산서 10종 · 분류 3 · 근거 법령 · 앱 설치 단추 · 사용자 매뉴얼 연결
CHECKED = "2026-10-30"          # 근거 조문 대조일
BASE = "https://manminkim-eng.github.io"

GROUPS = [
    ("permit", "인허가·법규", "용도변경 · 건폐율·용적률 · 일조 · 주차"),
    ("energy", "에너지",       "열관류율 · 에너지성능지표"),
    ("fee",    "대가·감리·공기", "설계·감리 대가 · 해체감리 · 상주감리 · 공사기간"),
]

# no, group, name, en, repo, ver, accent, desc(정성 서술 — 수치 기재 금지), basis(근거 칩)
TOOLS = [
    ("35", "permit", "용도변경 판정", "Change of Use", "Change-of-Use", "5.0.6", "#f1cd7c",
     "현재 용도와 변경 용도의 시설군을 대조해 허가 · 신고 · 대장 기재변경 대상을 판정합니다.",
     ["건축법 제19조", "시행령 제14조"]),
    ("36", "permit", "건폐율 · 용적률", "Land Use", "Land-Use", "5.1.0", "#fbbf24",
     "용도지역과 도시·군계획조례 값으로 건폐율 · 용적률 한도를 계산합니다.",
     ["국토계획법 제77조 · 제78조", "시행령 제84조 · 제85조", "도시·군계획조례"]),
    ("38", "permit", "일조 · 사선 제한", "Sunlight · Setback", "Architectural-line", "5.0.6", "#fb923c",
     "정북방향 인접 대지경계선 기준의 일조 높이 제한을 검토합니다.",
     ["건축법 제61조", "시행령 제86조", "건축조례"]),
    ("40", "permit", "부설주차장 법정대수", "Parking Lot Act", "Parking-Lot-Act", "5.1.1", "#facc15",
     "시설물 용도와 시설면적으로 부설주차장 법정 대수를 산정합니다.",
     ["주차장법 제19조", "시행령 제6조 · 별표 1", "주차장 조례"]),
    ("31", "energy", "열관류율 검토", "U-Value Review", "u-value-app-", "5.0.9", "#34d399",
     "부위별 단열재 구성으로 열관류율을 계산해 지역별 기준과 대조합니다.",
     ["에너지절약설계기준 별표 1", "녹색건축법 제14조"]),
    ("39", "energy", "에너지성능지표(EPI)", "Energy Performance Index", "Energy-Performance-Index", "5.4.4", "#2dd4bf",
     "에너지절약계획서의 에너지성능지표 평점을 항목별로 산정합니다.",
     ["에너지절약설계기준 제15조", "녹색건축법 제14조"]),
    ("30", "fee", "설계 · 감리 대가", "Architect Fee", "1architect-fee-app", "5.0.4", "#d8ac50",
     "공공발주사업의 건축사 설계 · 감리 대가를 공사비요율 방식으로 산출합니다.",
     ["건축사법 제19조의3", "건축사 대가기준(국토부 고시)", "엔지니어링사업대가의 기준"]),
    ("32", "fee", "해체공사 감리대가", "Demolition Supervision", "demolition-calc", "5.0.6", "#f87171",
     "해체공사비 요율과 실비정액가산 방식으로 해체공사 감리대가를 산출합니다.",
     ["건축물관리법 제31조 · 제32조", "해체감리 기준 제23조 · 별표 2"]),
    ("33", "fee", "상주감리 대가", "Resident Supervision", "arch-supervision", "5.0.6", "#c084fc",
     "상주감리 대상 여부를 판정하고 감리원 배치에 따른 대가를 산출합니다.",
     ["건축법 제25조", "시행령 제19조 ⑤", "건축공사 감리세부기준"]),
    ("34", "fee", "공사기간 산정", "Construction Period", "construction-air", "5.1.1", "#60a5fa",
     "준비 · 비작업일 · 작업일 · 정리기간을 합산해 적정 공사기간을 산정합니다.",
     ["건설기술 진흥법 제45조의2", "공공 건설공사의 공사기간 산정기준"]),
]

# 이름, 구분, 현행(번호 · 시행일), 관련 조문, 적용 도구 번호
LAWS = [
    ("건축법", "법률",
     "2026-02-27 시행", "제19조(용도변경) · 제25조(건축물의 공사감리) · 제61조(일조 등의 확보를 위한 건축물의 높이 제한)", "33 · 35 · 38"),
    ("건축법 시행령", "대통령령",
     "2026-10-06 시행", "제14조(용도변경) · 제19조(공사감리) ⑤ · 제86조(일조 등의 확보를 위한 건축물의 높이 제한)", "33 · 35 · 38"),
    ("국토의 계획 및 이용에 관한 법률 · 시행령", "법률 · 영",
     "법 2026-07-01 · 영 2026-09-18 시행", "법 제77조(용도지역의 건폐율) · 제78조(용도지역에서의 용적률) · 영 제84조 · 제85조", "36"),
    ("주차장법 · 시행령", "법률 · 영",
     "법 · 영 2026-08-28 시행", "법 제19조(부설주차장의 설치·지정) · 영 제6조(부설주차장의 설치기준) · 별표 1(2026-08-25 개정)", "40"),
    ("녹색건축물 조성 지원법", "법률",
     "2026-09-18 시행", "제14조(에너지 절약계획서 제출)", "31 · 39"),
    ("건축물의 에너지절약설계기준", "국토교통부 고시",
     "제2026-360호 · 2026-07-08 시행", "제15조(에너지성능지표) · 별표 1(지역별 건축물 부위의 열관류율표)", "31 · 39"),
    ("건축물관리법 · 해체계획서 작성 및 감리업무 등에 관한 기준", "법률 · 고시",
     "법 2025-06-04 시행 · 고시 제2022-446호 2022-08-04 시행", "법 제31조(건축물 해체공사감리자의 지정 등) · 제32조(해체공사감리자의 업무 등) · 고시 제23조(감리대가 기준) · 별표 2", "32"),
    ("건축사법 · 공공발주사업에 대한 건축사의 업무범위와 대가기준", "법률 · 고시",
     "법 2026-09-18 시행 · 고시 2020-09-14 발령", "법 제19조의3(건축사의 업무범위 및 대가 기준)", "30 · 33"),
    ("엔지니어링산업 진흥법 · 엔지니어링사업대가의 기준", "법률 · 고시",
     "법 2026-06-03 시행 · 고시 2024-12-31 발령", "법 제31조(엔지니어링사업의 대가 기준 등)", "30"),
    ("건축공사 감리세부기준", "국토교통부 고시",
     "2024-07-10 발령", "건축법 제25조제8항 · 제9항에 따른 세부기준", "33"),
    ("건설기술 진흥법 · 공공 건설공사의 공사기간 산정기준", "법률 · 고시",
     "법 2025-10-01 시행 · 고시 2025-01-06 시행", "법 제45조의2(공사기간 산정기준)", "34"),
]

e = html.escape
import re
def nw(t):  # 날짜 · 고시 번호는 줄바꿈 금지
    return re.sub(r"(\d{4}-\d{2}-\d{2}|제\d{4}-\d+호)", r'<span class="nw">\1</span>', t)

def card(t):
    no, g, name, en, repo, ver, acc, desc, basis = t
    chips = "".join(f'<span class="chip">{e(b)}</span>' for b in basis)
    return f'''
    <a class="tcard" data-g="{g}" href="../{repo}/" style="--acc:{acc}" aria-label="{e(name)} 계산서 열기">
      <div class="tc-top"><span class="tc-dot" aria-hidden="true"></span><span class="tc-no">A · {no}</span><span class="tc-ver">Ver {ver}</span></div>
      <h3 class="tc-name">{e(name)}</h3>
      <div class="tc-en">{e(en)}</div>
      <p class="tc-desc">{e(desc)}</p>
      <div class="tc-chips" aria-label="근거 기준">{chips}</div>
      <div class="tc-foot">
        <span class="tc-man" role="link" tabindex="0" data-href="../{repo}/manual/">사용자 매뉴얼</span>
        <span class="tc-go">계산서 열기 <span class="arw" aria-hidden="true">→</span></span>
      </div>
    </a>'''

def group(gid, gname, gsub):
    items = [t for t in TOOLS if t[1] == gid]
    return f'''
  <section class="grp" id="g-{gid}" data-g="{gid}">
    <div class="grp-hd"><span class="grp-tag">{e(gname)}</span><span class="grp-sub">{e(gsub)}</span><span class="grp-n">{len(items)} tools</span></div>
    <div class="grid">{"".join(card(t) for t in items)}
    </div>
  </section>'''

law_rows = "".join(f'''
        <tr><th scope="row">{e(n)}</th><td class="kind">{e(k)}</td><td class="cur">{nw(e(d))}</td><td>{e(a)}</td><td class="num">{e(t)}</td></tr>''' for n, k, d, a, t in LAWS)

tabs = f'<button class="tab on" data-tab="all" role="tab" aria-selected="true">전체 <span class="tn">{len(TOOLS)}</span></button>' + "".join(
    f'<button class="tab" data-tab="{g}" role="tab" aria-selected="false">{e(n)} <span class="tn">{sum(1 for t in TOOLS if t[1]==g)}</span></button>' for g, n, _ in GROUPS)

page = f'''<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>ENGINEER KIM MANMIN · 건축 계산서 통합 포털</title>
<meta name="description" content="건축 계산서 통합 포털 — 인허가·법규 · 에너지 · 대가·감리·공기 10종 계산서와 근거 법령·기준 안내 | Engineer Kim Manmin">
<meta name="theme-color" content="#14110b">
<meta name="color-scheme" content="dark">
<link rel="manifest" href="manifest.json">
<link rel="apple-touch-icon" href="icons/apple-touch-icon.png">
<link rel="icon" type="image/png" sizes="32x32" href="icons/favicon-32.png">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="건축 포털">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700;900&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="./assets/fonts/manmin-fonts.css"><!-- 로컬 폴백 폰트 -->
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
:root{{
  --bg:#0b1220;--bg-card:#121c30;--bg-deep:#080d18;
  --line:#1e2e50;--line2:#2a4070;
  --t-high:#f2f5ff;--t-body:#c2d0ec;--t-sub:#8aa2c8;
  --mech:#d8ac50;--mech-lt:#f1cd7c;--gold:#d8ac50;--gold-lt:#f1cd7c;
  --f-kr:'Noto Sans KR','Noto Sans KR Local','Apple SD Gothic Neo','Malgun Gothic',sans-serif;
  --f-mono:'JetBrains Mono','Noto Sans KR','Noto Sans KR Local',Consolas,monospace;
  --radius:12px;--shadow:0 4px 20px rgba(0,0,0,.35);
}}
html{{scroll-behavior:smooth;-webkit-text-size-adjust:100%}}
body{{font-family:var(--f-kr);background:var(--bg);color:var(--t-body);line-height:1.7;-webkit-font-smoothing:antialiased;overflow-x:hidden;min-height:100vh}}
.bg{{position:fixed;inset:0;z-index:0;pointer-events:none;
  background-image:linear-gradient(rgba(216,172,80,.035) 1px,transparent 1px),linear-gradient(90deg,rgba(216,172,80,.035) 1px,transparent 1px),
  radial-gradient(ellipse 90% 50% at 50% -10%,rgba(120,90,40,.30),transparent 65%);background-size:40px 40px,40px 40px,100% 100%}}
.wrap{{position:relative;z-index:1;max-width:1120px;margin:0 auto;padding:0 24px 80px}}
a{{color:inherit}}
:focus-visible{{outline:2px solid var(--gold);outline-offset:3px}}

/* HEADER */
.hd{{padding:52px 0 8px;text-align:center}}
.pill{{display:inline-flex;align-items:center;gap:8px;padding:6px 14px;border:1px solid var(--line2);border-radius:999px;font-size:.8rem;color:var(--mech-lt);background:rgba(216,172,80,.06)}}
.pill i{{width:7px;height:7px;border-radius:50%;background:#4ade80;box-shadow:0 0 0 3px rgba(74,222,128,.18)}}
.brand{{display:flex;align-items:center;justify-content:center;gap:18px;margin:22px 0 14px;flex-wrap:wrap}}
.brand img{{width:72px;height:72px;border-radius:14px;border:1px solid var(--line2)}}
.brand-t{{text-align:left}}
.brand-e{{font-family:var(--f-mono);font-size:.8rem;letter-spacing:.3em;color:var(--mech-lt);text-transform:uppercase}}
.brand-n{{font-family:var(--f-mono);font-weight:700;font-size:2rem;letter-spacing:.06em;color:var(--t-high);line-height:1.1}}
.ttl{{font-size:clamp(1.6rem,3.6vw,2.4rem);font-weight:900;letter-spacing:-.03em;color:var(--t-high);line-height:1.25}}
.ttl b{{color:var(--mech-lt);font-weight:900}}
.lead{{margin:12px auto 0;max-width:640px;font-size:1rem;color:var(--t-body)}}
.hline{{width:120px;height:2px;margin:26px auto 0;background:linear-gradient(90deg,transparent,var(--mech),transparent)}}

/* STATS */
.stats{{display:grid;grid-template-columns:repeat(5,1fr);gap:1px;margin:30px 0 26px;background:var(--line);border:1px solid var(--line);border-radius:var(--radius);overflow:hidden}}
.st{{background:var(--bg-card);padding:16px 12px;text-align:center}}
.st-n{{font-family:var(--f-mono);font-weight:700;font-size:1.35rem;color:var(--t-high)}}
.st-l{{font-size:.8rem;color:var(--t-sub)}}

/* TABS */
.tabs{{display:flex;gap:8px;flex-wrap:wrap;justify-content:center;margin-bottom:30px}}
.tab{{font:500 .92rem var(--f-kr);color:var(--t-sub);background:var(--bg-card);border:1px solid var(--line2);border-radius:999px;min-height:44px;padding:0 18px;cursor:pointer;display:inline-flex;align-items:center;gap:8px;transition:.2s}}
.tab:hover{{color:var(--t-high);border-color:var(--mech)}}
.tab.on{{color:#0b1220;background:var(--mech-lt);border-color:var(--mech-lt);font-weight:700}}
.tn{{font-family:var(--f-mono);font-size:.78rem;opacity:.8}}
.tab-law{{text-decoration:none}}
.tab-man{{border-color:#9cc3f5;color:#c8dcf8}}.tab-man:hover{{border-color:#c8dcf8;color:var(--t-high)}}

/* GROUP */
.grp{{margin-bottom:40px}}
.grp-hd{{display:flex;align-items:center;gap:12px;margin-bottom:16px;flex-wrap:wrap}}
.grp-tag{{font-weight:700;color:var(--t-high);font-size:1.08rem;padding-left:12px;border-left:3px solid var(--mech)}}
.grp-sub{{font-size:.88rem;color:var(--t-sub)}}
.grp-n{{margin-left:auto;font-family:var(--f-mono);font-size:.78rem;color:var(--t-sub)}}
.grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}}

/* CARD */
.tcard{{position:relative;display:flex;flex-direction:column;background:var(--bg-card);border:1px solid var(--line);border-radius:var(--radius);padding:22px 22px 18px;text-decoration:none;box-shadow:var(--shadow);transition:transform .22s,border-color .22s,box-shadow .22s;overflow:hidden}}
.tcard::before{{content:"";position:absolute;left:0;right:0;top:0;height:3px;background:linear-gradient(90deg,var(--acc),transparent);opacity:.85}}
.tcard:hover{{transform:translateY(-4px);border-color:var(--acc);box-shadow:0 12px 32px rgba(0,0,0,.45)}}
.tc-top{{display:flex;align-items:center;gap:8px;margin-bottom:12px}}
.tc-dot{{width:9px;height:9px;border-radius:50%;background:var(--acc)}}
.tc-no{{font-family:var(--f-mono);font-size:.78rem;letter-spacing:.08em;color:var(--t-sub)}}
.tc-ver{{margin-left:auto;font-family:var(--f-mono);font-size:.76rem;color:var(--t-sub);border:1px solid var(--line2);border-radius:6px;padding:1px 7px}}
.tc-name{{font-size:1.16rem;font-weight:700;letter-spacing:-.01em;color:var(--t-high);line-height:1.35}}
.tc-en{{font-family:var(--f-mono);font-size:.76rem;letter-spacing:.06em;color:var(--t-sub);text-transform:uppercase;margin-top:2px}}
.tc-desc{{margin:12px 0 14px;font-size:.92rem;line-height:1.7;flex:1}}
.tc-chips{{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:16px}}
.chip{{font-size:.78rem;color:var(--t-body);background:var(--bg-deep);border:1px solid var(--line2);border-radius:6px;padding:3px 8px}}
.tc-foot{{display:flex;align-items:center;gap:10px;border-top:1px solid var(--line);padding-top:12px}}
.tc-man{{font-size:.86rem;color:var(--mech-lt);min-height:44px;display:inline-flex;align-items:center;cursor:pointer;text-decoration:underline;text-underline-offset:3px}}
.tc-man:hover{{color:var(--gold-lt)}}
.tc-go{{margin-left:auto;font-size:.88rem;font-weight:700;color:var(--t-high)}}
.arw{{display:inline-block;transition:transform .22s}}
.tcard:hover .arw{{transform:translateX(4px)}}
.grp.off{{display:none}}

/* LAW */
.law{{margin-top:12px;scroll-margin-top:20px}}
.law-hd{{display:flex;align-items:baseline;gap:12px;flex-wrap:wrap;margin-bottom:12px}}
.law-hd h2{{font-size:1.3rem;font-weight:800;color:var(--t-high);letter-spacing:-.02em}}
.law-hd span{{font-size:.86rem;color:var(--t-sub)}}
.tbl-wrap{{overflow-x:auto;border:1px solid var(--line);border-radius:var(--radius);background:var(--bg-card)}}
table{{width:100%;border-collapse:collapse;font-size:.9rem;min-width:760px}}
th,td{{padding:12px 14px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top}}
thead th{{background:var(--bg-deep);color:var(--t-sub);font-weight:500;font-size:.82rem;white-space:nowrap}}
tbody th{{color:var(--t-high);font-weight:700}}
tbody tr:last-child th,tbody tr:last-child td{{border-bottom:0}}
td.num{{font-family:var(--f-mono);font-size:.84rem;white-space:nowrap}}
td.cur{{font-family:var(--f-mono);font-size:.84rem;min-width:150px;word-break:keep-all}}
.nw{{white-space:nowrap}}
td.kind{{white-space:nowrap;font-size:.84rem;color:var(--t-sub)}}
tbody th{{min-width:170px}}
.note{{margin-top:14px;padding:14px 16px;border:1px solid var(--line2);border-left:3px solid var(--gold);border-radius:var(--radius);background:rgba(216,172,80,.05);font-size:.88rem}}
.note b{{color:var(--gold-lt)}}
.note a{{color:var(--mech-lt)}}

/* FOOTER */
.ft{{margin-top:48px;padding-top:22px;border-top:1px solid var(--line);display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap;font-size:.84rem;color:var(--t-sub)}}
.ft a{{color:var(--mech-lt)}}
.ft .mono{{font-family:var(--f-mono)}}

/* 앱 설치 */
.tab-inst{{font-weight:700}}
.tab-inst svg{{width:15px;height:15px;flex-shrink:0}}
.pwa-bar{{position:fixed;left:50%;bottom:16px;transform:translateX(-50%);z-index:40;width:min(560px,calc(100% - 32px));display:flex;align-items:center;gap:12px;
  padding:12px 14px;background:var(--bg-card);border:1px solid var(--line2);border-left:3px solid var(--gold);border-radius:var(--radius);box-shadow:0 12px 32px rgba(0,0,0,.5)}}
.pwa-bar img{{width:40px;height:40px;border-radius:8px;flex-shrink:0}}
.pwa-bar-t{{flex:1;min-width:0;font-size:.88rem;line-height:1.5}}
.pwa-bar-t b{{display:block;color:var(--t-high);font-size:.95rem}}
.pwa-bar button,.ios-x,.ios-ok{{font:600 .88rem var(--f-kr);min-height:44px;padding:0 14px;border-radius:8px;cursor:pointer}}
.pwa-yes,.ios-ok{{background:var(--gold);color:#0b1220;border:0}}
.pwa-yes:hover,.ios-ok:hover{{background:var(--gold-lt)}}
.pwa-no,.ios-x{{background:transparent;color:var(--t-sub);border:1px solid var(--line2)}}
.pwa-no:hover,.ios-x:hover{{color:var(--t-high);border-color:var(--mech)}}
.ios-guide{{position:fixed;inset:0;z-index:50;display:flex;align-items:center;justify-content:center;padding:16px;background:rgba(5,9,18,.72)}}
.ios-box{{width:min(440px,100%);background:var(--bg-card);border:1px solid var(--line2);border-radius:var(--radius);box-shadow:0 16px 48px rgba(0,0,0,.6);padding:22px 22px 18px}}
.ios-box h2{{font-size:1.12rem;font-weight:800;color:var(--t-high);margin-bottom:12px}}
.ios-box ol{{list-style:none;counter-reset:s;display:grid;gap:10px;margin-bottom:12px}}
.ios-box li{{counter-increment:s;display:flex;gap:10px;align-items:flex-start;font-size:.92rem}}
.ios-box li::before{{content:counter(s);flex-shrink:0;width:24px;height:24px;border-radius:50%;background:var(--mech);color:#0b1220;font:700 .8rem var(--f-mono);display:flex;align-items:center;justify-content:center;margin-top:1px}}
.ios-box li svg{{width:16px;height:16px;vertical-align:-3px;color:var(--mech-lt)}}
.ios-note{{font-size:.82rem;color:var(--t-sub);border-top:1px solid var(--line);padding-top:10px;margin-bottom:14px}}
.ios-act{{display:flex;gap:8px;justify-content:flex-end}}
[hidden]{{display:none!important}}

/* 5단계 반응형 */
@media (max-width:1240px){{.wrap{{max-width:100%}}}}
@media (max-width:1024px){{.grid{{grid-template-columns:repeat(2,1fr)}}}}
@media (max-width:760px){{.stats{{grid-template-columns:repeat(3,1fr)}}.st:nth-child(n+4){{grid-column:span 1}}}}
@media (max-width:640px){{
  .wrap{{padding:0 16px 64px}}.hd{{padding-top:36px}}
  .grid{{grid-template-columns:1fr}}
  .stats{{grid-template-columns:repeat(2,1fr)}}.st:last-child{{grid-column:1/-1}}
  .brand img{{width:56px;height:56px}}.brand-n{{font-size:1.6rem}}
  .tab{{min-height:48px}}.tc-man{{min-height:48px}}
  .grp-n{{margin-left:0;width:100%}}
  .ft a{{display:inline-flex;align-items:center;min-height:48px}}
  .pwa-bar{{bottom:12px;flex-wrap:wrap}}.pwa-bar img{{display:none}}.pwa-bar-t{{flex-basis:100%}}
  .pwa-bar button,.ios-x,.ios-ok{{min-height:48px;flex:1}}
}}
@media (max-width:480px){{.brand-e{{letter-spacing:.2em}}.tabs{{justify-content:flex-start}}}}
@media (max-width:400px){{.tcard{{padding:18px 16px 14px}}}}
@media (prefers-reduced-motion:reduce){{*{{transition:none!important;scroll-behavior:auto!important}}}}
@media print{{.bg,.tabs,.pwa-bar,.ios-guide{{display:none!important}}body{{background:#fff;color:#111}}.tcard,.tbl-wrap,.st{{background:#fff;box-shadow:none;break-inside:avoid}}
  .tc-name,.ttl,.law-hd h2,tbody th,.st-n,.brand-n{{color:#111}}.grp.off{{display:block}}}}
</style>
</head>
<body>
<div class="bg" aria-hidden="true"></div>
<div class="wrap">

<header class="hd">
  <div class="pill"><i aria-hidden="true"></i>근거 조문 대조 {CHECKED} · 국가법령정보</div>
  <div class="brand">
    <img src="icons/icon-192.png" alt="ENGINEER KIM MANMIN 로고" width="72" height="72">
    <div class="brand-t"><div class="brand-e">Engineer</div><div class="brand-n">KIM MANMIN</div></div>
  </div>
  <h1 class="ttl">건축 <b>계산서 통합 포털</b></h1>
  <p class="lead">인허가·법규 · 에너지 · 대가·감리·공기 계산서 {len(TOOLS)}종을 한곳에서 열고, 계산서마다 적용한 근거 법령과 고시를 확인합니다.</p>
  <div class="hline" aria-hidden="true"></div>
</header>

<div class="stats">
  <div class="st"><div class="st-n">{len(TOOLS)}</div><div class="st-l">인허가 4 · 에너지 2 · 대가 4</div></div>
  <div class="st"><div class="st-n">{len(LAWS)}</div><div class="st-l">근거 법령 · 고시</div></div>
  <div class="st"><div class="st-n">조례</div><div class="st-l">지자체 값 반영</div></div>
  <div class="st"><div class="st-n">PWA</div><div class="st-l">오프라인 지원</div></div>
  <div class="st"><div class="st-n">A4</div><div class="st-l">계산서 인쇄</div></div>
</div>

<nav class="tabs" role="tablist" aria-label="분류">
  {tabs}
  <a class="tab tab-law" href="#law">근거 법령·고시</a>
  <a class="tab tab-law tab-man" href="./manual/" target="_blank" rel="noopener" aria-label="포털 사용자 매뉴얼 (새 창)">사용자 매뉴얼</a>
  <button class="tab tab-man tab-inst" id="pwa-inst" type="button" hidden aria-label="이 포털을 앱으로 설치"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3v12"/><path d="M7 10l5 5 5-5"/><path d="M5 21h14"/></svg>앱 설치</button>
</nav>
{"".join(group(*g) for g in GROUPS)}

<section class="law" id="law">
  <div class="law-hd"><h2>근거 법령 · 고시</h2><span>대조일 {CHECKED} · 국가법령정보(LawMCP) 기준</span></div>
  <div class="tbl-wrap">
    <table>
      <thead><tr><th scope="col">법령 · 기준</th><th scope="col">구분</th><th scope="col">현행</th><th scope="col">관련 조문 · 코드</th><th scope="col">적용 도구</th></tr></thead>
      <tbody>{law_rows}
      </tbody>
    </table>
  </div>
  <p class="note"><b>안내</b> — 이 포털은 계산서별 근거와 시행일만 안내합니다. 수치 기준(요율 · 한도 · 이격거리 · 주차대수 등)은 각 계산서의 산출근거표에서 확인하십시오. 건폐율 · 용적률 · 주차대수 · 일조 이격거리는 해당 지방자치단체 조례 값을 함께 확인하십시오.</p>
  <p class="note"><b>개정 예정</b> — 「건축법」 제61조제1항(일조 등의 확보를 위한 건축물의 높이 제한)이 법률 제21880호(2026-08-11 공포)로 개정되어 <b>2026-11-12</b>부터 시행됩니다. 시행 이후 건축허가를 신청(건축위원회 심의 신청 포함)하거나 건축신고를 하는 경우부터 적용됩니다(부칙 제1조 단서 · 제4조). 조문 원문은 <a href="https://www.law.go.kr/법령/건축법" target="_blank" rel="noopener">국가법령정보센터</a>에서 확인하십시오.</p>
</section>

<footer class="ft">
  <span>© 2026 김만민 건축사 · (주)대성건축사사무소 — <a href="{BASE}/KIMMANMIN/" target="_blank" rel="noopener">MANMIN 홈페이지</a></span>
  <span class="mono">ARCH PORTAL · Ver {VER}</span>
</footer>
</div>

<div class="pwa-bar" id="pwa-bar" role="region" aria-label="앱 설치 안내" hidden>
  <img src="icons/icon-96.png" alt="" width="40" height="40">
  <div class="pwa-bar-t"><b>건축 포털을 앱으로 설치</b>홈 화면에서 바로 열고, 오프라인에서도 포털을 볼 수 있습니다.</div>
  <button class="pwa-no" id="pwa-no" type="button">닫기</button>
  <button class="pwa-yes" id="pwa-yes" type="button">설치</button>
</div>

<div class="ios-guide" id="ios-guide" role="dialog" aria-modal="true" aria-labelledby="ios-t" hidden>
  <div class="ios-box">
    <h2 id="ios-t">아이폰 · 아이패드에서 설치</h2>
    <ol>
      <li><span>화면 아래(아이패드는 위)의 <b>공유</b> 단추 <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 15V3"/><path d="M7 8l5-5 5 5"/><path d="M5 12v8h14v-8"/></svg>를 누릅니다.</span></li>
      <li><span>목록에서 <b>홈 화면에 추가</b>를 고른 뒤 <b>추가</b>를 누릅니다.</span></li>
    </ol>
    <p class="ios-note">설치되는 범위는 이 포털입니다. 카드에서 연 계산서는 앱 안의 브라우저 창으로 열리며, 계산서도 앱으로 쓰려면 각 계산서 화면에서 같은 방법으로 설치합니다.</p>
    <div class="ios-act"><button class="ios-ok" id="ios-ok" type="button">확인</button></div>
  </div>
</div>

<script>
(function(){{
  var tabs=document.querySelectorAll('.tab[data-tab]'),grps=document.querySelectorAll('.grp');
  tabs.forEach(function(t){{t.addEventListener('click',function(){{
    var k=t.getAttribute('data-tab');
    tabs.forEach(function(x){{var on=x===t;x.classList.toggle('on',on);x.setAttribute('aria-selected',on?'true':'false');}});
    grps.forEach(function(g){{g.classList.toggle('off',k!=='all'&&g.getAttribute('data-g')!==k);}});
  }});}});
  function go(el,ev){{ev.preventDefault();ev.stopPropagation();window.open(el.getAttribute('data-href'),'_blank','noopener');}}
  document.querySelectorAll('.tc-man').forEach(function(m){{
    m.addEventListener('click',function(ev){{go(m,ev);}});
    m.addEventListener('keydown',function(ev){{if(ev.key==='Enter'||ev.key===' ')go(m,ev);}});
  }});
  if('serviceWorker' in navigator){{window.addEventListener('load',function(){{navigator.serviceWorker.register('./sw.js').catch(function(){{}});}});}}

  /* 앱 설치 — 지원 브라우저: beforeinstallprompt · 아이폰/아이패드: 안내 상자 · 설치된 앱 화면: 숨김 */
  var inst=document.getElementById('pwa-inst'),bar=document.getElementById('pwa-bar'),
      yes=document.getElementById('pwa-yes'),no=document.getElementById('pwa-no'),
      ios=document.getElementById('ios-guide'),iosOk=document.getElementById('ios-ok'),dp=null,last=null;
  var standalone=(window.matchMedia&&matchMedia('(display-mode: standalone)').matches)||navigator.standalone===true;
  var isIOS=/iPad|iPhone|iPod/.test(navigator.userAgent)||(navigator.platform==='MacIntel'&&navigator.maxTouchPoints>1);
  function ss(k,v){{try{{if(v===undefined)return sessionStorage.getItem(k);sessionStorage.setItem(k,v);}}catch(e){{return null;}}}}
  function showBar(){{if(standalone||ss('ap-inst-bar'))return;setTimeout(function(){{if(!standalone&&(dp||isIOS))bar.hidden=false;}},2000);}}
  function hideAll(){{inst.hidden=true;bar.hidden=true;}}
  function openIOS(){{last=document.activeElement;bar.hidden=true;ios.hidden=false;iosOk.focus();}}
  function closeIOS(){{ios.hidden=true;if(last&&last.focus)last.focus();}}
  function doInstall(){{
    if(dp){{bar.hidden=true;dp.prompt();dp.userChoice.then(function(c){{if(c.outcome==='accepted')hideAll();dp=null;if(c.outcome!=='accepted')inst.hidden=true;}});}}
    else if(isIOS){{openIOS();}}
  }}
  if(!standalone){{
    window.addEventListener('beforeinstallprompt',function(e){{e.preventDefault();dp=e;inst.hidden=false;showBar();}});
    if(isIOS){{inst.hidden=false;showBar();}}
  }}
  window.addEventListener('appinstalled',function(){{dp=null;hideAll();}});
  inst.addEventListener('click',doInstall);yes.addEventListener('click',doInstall);
  no.addEventListener('click',function(){{bar.hidden=true;ss('ap-inst-bar','1');}});
  iosOk.addEventListener('click',closeIOS);
  ios.addEventListener('click',function(e){{if(e.target===ios)closeIOS();}});
  document.addEventListener('keydown',function(e){{if(e.key==='Escape'&&!ios.hidden)closeIOS();}});
}})();
</script>
</body>
</html>
'''
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "index.html")
open(out, "w", encoding="utf-8").write(page)
print("written", os.path.getsize(out), "bytes ·", len(TOOLS), "tools ·", len(LAWS), "laws")
