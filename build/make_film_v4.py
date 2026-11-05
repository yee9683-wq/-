# 이든 브랜드 필름 v4 (약 51초) 장면 생성기. 실행: python build/make_film_v4.py
import os
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "idden-film")
COMP = os.path.join(ROOT, "compositions")
os.makedirs(COMP, exist_ok=True)
for f in os.listdir(COMP):
    if f.endswith(".html"):
        os.remove(os.path.join(COMP, f))

GREEN, GREY, SAGE = "#193B2A", "#66716A", "#EEF0E9"
FONTS = ('@font-face { font-family: "Outfit"; src: url("assets/fonts/Outfit.woff2") format("woff2"); font-weight: 100 900; }\n'
         '    @font-face { font-family: "Pretendard"; src: url("assets/fonts/PretendardVariable.woff2") format("woff2"); font-weight: 100 900; }')

def scene(cid, dur, bg, css, body, js):
    return f"""<template>
  <style>
    {FONTS}
    #root {{ position:absolute; inset:0; overflow:hidden; background:{bg}; font-family:"Pretendard", sans-serif; }}
    .line {{ position:absolute; left:108px; right:108px; top:150px; color:{GREEN}; font-size:76px; line-height:1.24; font-weight:600; letter-spacing:-0.04em; word-break:keep-all; }}
    .line span {{ display:inline-block; }}
    .line .l1 {{ color:{GREY}; }}
    .line.on-dark {{ color:#FFFFFF; }}
    .line.on-dark .l1 {{ color:#C9D8CD; }}
    .src {{ position:absolute; left:108px; right:108px; bottom:150px; color:{GREY}; font-size:36px; line-height:1.3; font-weight:500; letter-spacing:-0.02em; }}
    .obj img {{ display:block; width:100%; height:auto; filter:drop-shadow(0 20px 30px rgba(25,59,42,.16)); }}
    .obj {{ position:absolute; }}
{css}
  </style>
  <div id="root" data-composition-id="{cid}" data-width="1080" data-height="1350">
{body}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
{js}
    window.__timelines["{cid}"] = tl;
  </script>
</template>
"""

def line(cid, l1, l2, dur, dark=False, top=150):
    cls = "line on-dark" if dark else "line"
    return (f'    <p id="{cid}-line" class="{cls} clip" data-start="0" data-duration="{dur}" data-track-index="2" style="top:{top}px">'
            f'<span class="l1" id="{cid}-l1">{l1}</span><br><span id="{cid}-l2">{l2}</span></p>')

def line_in(cid, t=0.3, kind="blur"):
    if kind == "ink":
        return (f'    tl.fromTo("#{cid}-l1", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.22, ease: "power2.out" }}, {t});\n'
                f'    tl.fromTo("#{cid}-l2", {{ opacity: 0, color: "#C9D0CB" }}, {{ opacity: 1, color: "{GREEN}", duration: 0.24, ease: "power2.out" }}, {t + 0.12});\n')
    return (f'    tl.fromTo("#{cid}-l1", {{ opacity: 0, filter: "blur(8px)" }}, {{ opacity: 1, filter: "blur(0px)", duration: 0.2, ease: "power4.out" }}, {t});\n'
            f'    tl.fromTo("#{cid}-l2", {{ opacity: 0, filter: "blur(8px)" }}, {{ opacity: 1, filter: "blur(0px)", duration: 0.2, ease: "power4.out" }}, {t + 0.12});\n')

def out(sel, t):
    arr = ", ".join(f'"{s}"' for s in sel)
    return f'    tl.to([{arr}], {{ opacity: 0, filter: "blur(10px)", duration: 0.2, ease: "power3.in", stagger: 0.03 }}, {t});\n'

S = []  # (id, start, dur, html)

# 1. why — 여행지의 플라스틱
d = 5.0
S.append(("why", d, scene("why", d, "#FFFFFF", """
    #why-cam { position:absolute; inset:0; }
    #why-img { position:absolute; inset:0; width:100%; height:100%; object-fit:cover; object-position:50% 30%; }
    #why-scrim { position:absolute; left:0; right:0; bottom:0; height:58%; background:linear-gradient(180deg, rgba(12,28,20,0), rgba(12,28,20,.55) 50%, rgba(12,28,20,.82)); }
    #why-wipe, #why-white { position:absolute; inset:0; }
    #why-wipe { background:#193B2A; } #why-white { background:#FFFFFF; }""",
f"""    <div id="why-cam"><img id="why-img" src="assets/img/sun.jpg" alt="서선미 대표와 아들이 여행 중 보트 위에서 웃는 모습"></div>
    <div id="why-scrim"></div>
{line("why", "아이와 떠난 여행지마다", "일회용 플라스틱이 남았습니다", d, dark=True, top=1000)}
    <div id="why-white" class="clip" data-start="0" data-duration="{d}" data-track-index="3" data-layout-ignore></div>
    <div id="why-wipe" class="clip" data-start="0" data-duration="0.7" data-track-index="4" data-layout-ignore></div>""",
'    tl.fromTo("#why-wipe", { clipPath: "inset(0% 0% 0% 0%)" }, { clipPath: "inset(0% 0% 100% 0%)", duration: 0.55, ease: "power3.inOut" }, 0.05);\n'
'    tl.fromTo("#why-cam", { scale: 1.1 }, { scale: 1.0, duration: 5, ease: "power2.out" }, 0);\n'
+ line_in("why", 0.6) + out(["#why-line"], 4.45) +
'    tl.fromTo("#why-white", { opacity: 0 }, { opacity: 1, duration: 0.25, ease: "power2.in" }, 4.72);\n')))

# 2. waste — 3억 5,300만 톤
d = 5.5
S.append(("waste", d, scene("waste", d, "#FFFFFF", """
    #waste-num { position:absolute; left:108px; top:500px; color:#193B2A; font-family:"Outfit", sans-serif; font-size:150px; line-height:1; font-weight:500; letter-spacing:-0.04em; font-variant-numeric:tabular-nums; white-space:nowrap; }
    #waste-num small { font-family:"Pretendard", sans-serif; font-size:72px; font-weight:600; margin-left:10px; letter-spacing:-0.03em; }
    #waste-sub { position:absolute; left:108px; right:108px; top:680px; color:#66716A; font-size:48px; line-height:1.35; font-weight:600; letter-spacing:-0.03em; }
    .wb { position:absolute; left:108px; right:108px; height:120px; }
    #waste-b1 { top:860px; } #waste-b2 { top:1000px; }
    .wb span { display:block; color:#66716A; font-size:38px; font-weight:600; letter-spacing:-0.02em; margin-bottom:12px; }
    .wb i { display:block; height:40px; border-radius:20px; background:#193B2A; transform-origin:0% 50%; }
    #waste-b1 i { width:44%; background:#B9C7BD; } #waste-b2 i { width:100%; }""",
f"""{line("waste", "한 해 버려지는", "플라스틱 쓰레기", d)}
    <div id="waste-num" class="clip" data-start="0" data-duration="{d}" data-track-index="3"><span id="waste-n">0</span><small>톤</small></div>
    <p id="waste-sub" class="clip" data-start="0" data-duration="{d}" data-track-index="4">2000년보다 두 배 넘게 늘었습니다</p>
    <div class="wb clip" id="waste-b1" data-start="0" data-duration="{d}" data-track-index="6"><span>2000년</span><i id="waste-f1"></i></div>
    <div class="wb clip" id="waste-b2" data-start="0" data-duration="{d}" data-track-index="7"><span>2019년</span><i id="waste-f2"></i></div>
    <p class="src clip" id="waste-src" data-start="0" data-duration="{d}" data-track-index="5" style="bottom:100px">OECD 글로벌 플라스틱 전망, 2019년 기준</p>""",
line_in("waste", 0.25, "ink") +
'    const c = { v: 0 }; const n = document.querySelector("#waste-n");\n'
'    tl.fromTo("#waste-num", { opacity: 0 }, { opacity: 1, duration: 0.15, ease: "power2.out" }, 0.7);\n'
'    tl.fromTo(c, { v: 0 }, { v: 353000000, duration: 1.6, ease: "power3.out", onUpdate: () => { n.textContent = (Math.round(c.v / 1000000) * 1000000).toLocaleString("en-US"); } }, 0.7);\n'
'    tl.fromTo("#waste-b1", { opacity: 0 }, { opacity: 1, duration: 0.2, ease: "power2.out" }, 0.7);\n'
'    tl.fromTo("#waste-f1", { scaleX: 0 }, { scaleX: 1, duration: 0.8, ease: "power3.out" }, 0.75);\n'
'    tl.fromTo("#waste-b2", { opacity: 0 }, { opacity: 1, duration: 0.2, ease: "power2.out" }, 1.0);\n'
'    tl.fromTo("#waste-f2", { scaleX: 0 }, { scaleX: 1, duration: 1.3, ease: "power3.out" }, 1.05);\n'
'    tl.fromTo("#waste-sub", { opacity: 0, filter: "blur(8px)" }, { opacity: 1, filter: "blur(0px)", duration: 0.2, ease: "power4.out" }, 2.1);\n'
'    tl.fromTo("#waste-src", { opacity: 0 }, { opacity: 1, duration: 0.3, ease: "power2.out" }, 2.3);\n'
+ out(["#waste-line", "#waste-num", "#waste-sub", "#waste-b1", "#waste-b2", "#waste-src"], 5.22))))

# 3. recycle — 9%
d = 5.0
dots = "".join(f'<i class="dot{" g" if i in (0,1,2,3,4,5,6,7,8) else ""}"></i>' for i in range(100))
S.append(("recycle", d, scene("recycle", d, "#FFFFFF", """
    #recycle-grid { position:absolute; left:108px; top:450px; width:620px; display:grid; grid-template-columns:repeat(10, 44px); gap:20px; }
    #recycle-grid .dot { display:block; width:44px; height:44px; border-radius:50%; background:#DCE3DD; }
    #recycle-big { position:absolute; right:108px; top:460px; color:#193B2A; font-family:"Outfit", sans-serif; font-size:170px; line-height:1; font-weight:500; letter-spacing:-0.05em; }
    #recycle-sub { position:absolute; left:108px; right:108px; top:1110px; color:#66716A; font-size:44px; line-height:1.35; font-weight:600; letter-spacing:-0.03em; }""",
f"""{line("recycle", "그중 다시 쓰이는 건", "9%뿐입니다", d)}
    <div id="recycle-grid" data-layout-ignore>{dots}</div>
    <div id="recycle-big" class="clip" data-start="0" data-duration="{d}" data-track-index="3">9%</div>
    <p id="recycle-sub" class="clip" data-start="0" data-duration="{d}" data-track-index="4">나머지는 묻히거나 태워집니다</p>
    <p class="src clip" id="recycle-src" data-start="0" data-duration="{d}" data-track-index="5" style="bottom:110px">OECD 글로벌 플라스틱 전망, 2019년 기준</p>""",
line_in("recycle", 0.15, "ink") +
'    tl.fromTo("#recycle-grid .dot", { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.3, ease: "expo.out", stagger: 0.006 }, 0.45);\n'
'    tl.fromTo("#recycle-grid .dot.g", { backgroundColor: "#DCE3DD" }, { backgroundColor: "#193B2A", duration: 0.2, ease: "power2.out", stagger: 0.07 }, 1.45);\n'
'    tl.fromTo("#recycle-big", { opacity: 0, filter: "blur(10px)" }, { opacity: 1, filter: "blur(0px)", duration: 0.25, ease: "power4.out" }, 1.9);\n'
'    tl.fromTo("#recycle-sub", { opacity: 0, filter: "blur(8px)" }, { opacity: 1, filter: "blur(0px)", duration: 0.2, ease: "power4.out" }, 2.2);\n'
'    tl.fromTo("#recycle-src", { opacity: 0 }, { opacity: 1, duration: 0.3, ease: "power2.out" }, 2.3);\n'
+ out(["#recycle-line", "#recycle-grid", "#recycle-big", "#recycle-sub", "#recycle-src"], 4.72))))

# 4. hotel — 일회용품 무상 제공 금지
d = 5.0
items = ["칫솔", "치약", "샴푸", "린스", "면도기"]
rows = "\n".join(f'    <div class="h-item clip" id="hotel-i{i}" data-start="0" data-duration="{d}" data-track-index="{3+i}" style="top:{530+i*112}px"><span>{w}</span><i id="hotel-s{i}"></i></div>' for i, w in enumerate(items))
hjs = "".join(
    f'    tl.fromTo("#hotel-i{i}", {{ opacity: 0, x: 20 }}, {{ opacity: 1, x: 0, duration: 0.4, ease: "expo.out" }}, {0.5 + i*0.12:.2f});\n'
    f'    tl.fromTo("#hotel-s{i}", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.3, ease: "power3.inOut" }}, {1.35 + i*0.14:.2f});\n'
    for i in range(5))
S.append(("hotel", d, scene("hotel", d, "#FFFFFF", """
    .h-item { position:absolute; left:108px; height:100px; display:flex; align-items:center; color:#193B2A; font-size:80px; font-weight:600; letter-spacing:-0.04em; }
    .h-item span { position:relative; z-index:1; }
    .h-item i { position:absolute; left:-12px; right:-12px; top:52%; height:8px; border-radius:4px; background:#193B2A; transform-origin:0% 50%; z-index:2; }""",
f"""{line("hotel", "2024년부터 호텔은", "일회용품을 무료로<br>줄 수 없습니다", d)}
{rows}
    <p class="src clip" id="hotel-src" data-start="0" data-duration="{d}" data-track-index="9">자원재활용법 개정, 객실 50실 이상 숙박업소</p>""",
line_in("hotel", 0.15, "ink") + hjs +
'    tl.fromTo("#hotel-src", { opacity: 0 }, { opacity: 1, duration: 0.3, ease: "power2.out" }, 2.2);\n'
+ out(["#hotel-line"] + [f"#hotel-i{i}" for i in range(5)] + ["#hotel-src"], 4.65))))

# 5. reveal — 그래서 이든은
d = 4.0
S.append(("reveal", d, scene("reveal", d, "#FFFFFF", """
    #reveal-ground { position:absolute; inset:0; background:#193B2A; }
    #reveal-mark { position:absolute; left:108px; top:430px; width:110px; height:auto; }
    #reveal-white { position:absolute; inset:0; background:#FFFFFF; }""",
f"""    <div id="reveal-ground" data-layout-ignore></div>
    <img id="reveal-mark" class="clip" data-start="0" data-duration="{d}" data-track-index="2" src="assets/img/mark-white.png" alt="이든 나무 로고">
{line("reveal", "그래서 이든은", "버려지던 것으로 만듭니다", d, dark=True, top=620).replace('data-track-index="2"', 'data-track-index="3"')}
    <div id="reveal-white" class="clip" data-start="0" data-duration="{d}" data-track-index="4" data-layout-ignore></div>""",
'    tl.fromTo("#reveal-ground", { clipPath: "inset(100% 0% 0% 0%)" }, { clipPath: "inset(0% 0% 0% 0%)", duration: 0.45, ease: "power2.inOut" }, 0);\n'
'    tl.fromTo("#reveal-mark", { opacity: 0, y: 24, filter: "blur(8px)" }, { opacity: 1, y: 0, filter: "blur(0px)", duration: 0.6, ease: "expo.out" }, 0.45);\n'
+ line_in("reveal", 0.7) + out(["#reveal-mark", "#reveal-line"], 3.45) +
'    tl.fromTo("#reveal-white", { clipPath: "inset(100% 0% 0% 0%)" }, { clipPath: "inset(0% 0% 0% 0%)", duration: 0.4, ease: "power2.inOut" }, 3.6);\n')))

# 6. apple — 사과박, 토마토 부산물
d = 3.5
S.append(("apple", d, scene("apple", d, "#FFFFFF", """
    #apple-obj { left:355px; top:500px; width:350px; }""",
f"""{line("apple", "주스를 짜고 남은 사과박,", "토마토 농장의 부산물을 모아", d)}
    <div id="apple-obj" class="obj"><img src="assets/img/apple-cut.png" alt="풋사과 위에 놓인 이든 HB02 향수병"></div>""",
'    tl.fromTo("#apple-obj", { y: 90, opacity: 0, filter: "blur(14px)" }, { y: 0, opacity: 1, filter: "blur(0px)", duration: 0.9, ease: "expo.out" }, 0.05);\n'
'    tl.to("#apple-obj", { scale: 1.04, duration: 2.5, ease: "power1.inOut" }, 0.6);\n'
+ line_in("apple", 0.25, "ink") + out(["#apple-line", "#apple-obj"], 3.22))))

# 7. process — 흐름도
d = 4.0
S.append(("process", d, scene("process", d, "#FFFFFF", """
    .pr-row { position:absolute; left:108px; right:108px; height:200px; display:flex; align-items:center; gap:44px; }
    #process-r1 { top:430px; } #process-r2 { top:680px; } #process-r3 { top:930px; }
    .pr-node { flex:none; width:180px; height:180px; border-radius:50%; background:#EEF0E9; display:grid; place-items:center; overflow:hidden; }
    .pr-node img { max-width:70%; max-height:76%; width:auto; height:auto; }
    #process-r2 .pr-node { background:#193B2A; }
    #process-r2 .pr-node img { max-width:46%; }
    .pr-text strong { display:block; color:#193B2A; font-size:54px; line-height:1.2; font-weight:600; letter-spacing:-0.035em; }
    .pr-text small { display:block; margin-top:6px; color:#66716A; font-size:38px; line-height:1.3; font-weight:500; letter-spacing:-0.03em; }
    #process-rail { position:absolute; left:197px; top:610px; width:2px; height:500px; background:#193B2A; transform-origin:50% 0%; }
    #process-dot { position:absolute; left:189px; top:600px; width:18px; height:18px; border-radius:50%; background:#193B2A; }""",
f"""{line("process", "쓸모 있는 성분을 찾아", "원료로 되살립니다", d)}
    <div id="process-rail" data-layout-ignore></div>
    <div id="process-dot" data-layout-ignore></div>
    <div id="process-r1" class="pr-row clip" data-start="0" data-duration="{d}" data-track-index="3"><div class="pr-node"><img src="assets/img/apple-only.png" alt="사과"></div><div class="pr-text"><strong>농장 부산물</strong><small>사과박, 토마토 부산물</small></div></div>
    <div id="process-r2" class="pr-row clip" data-start="0" data-duration="{d}" data-track-index="4"><div class="pr-node"><img src="assets/img/mark-white.png" alt="이든 나무 표시"></div><div class="pr-text"><strong>업사이클 원료</strong><small>쓸모 있는 성분을 추려냄</small></div></div>
    <div id="process-r3" class="pr-row clip" data-start="0" data-duration="{d}" data-track-index="5"><div class="pr-node"><img src="assets/img/bar-white-cut.png" alt="이든 얼스바"></div><div class="pr-text"><strong>뷰티 제품</strong><small>얼스바, 바디 로션, 향</small></div></div>""",
line_in("process", 0.1) +
'    tl.fromTo("#process-rail", { scaleY: 0 }, { scaleY: 1, duration: 1.2, ease: "power2.inOut" }, 0.35);\n'
'    tl.fromTo("#process-dot", { opacity: 0 }, { opacity: 1, duration: 0.15, ease: "power2.out" }, 0.4);\n'
'    tl.fromTo("#process-dot", { y: 0 }, { y: 500, duration: 1.5, ease: "power1.inOut" }, 0.4);\n'
'    tl.to("#process-dot", { opacity: 0, duration: 0.15, ease: "power2.in" }, 1.95);\n'
'    tl.fromTo("#process-r1", { opacity: 0, x: 24, filter: "blur(8px)" }, { opacity: 1, x: 0, filter: "blur(0px)", duration: 0.45, ease: "expo.out" }, 0.3);\n'
'    tl.fromTo("#process-r2", { opacity: 0, x: 24, filter: "blur(8px)" }, { opacity: 1, x: 0, filter: "blur(0px)", duration: 0.45, ease: "expo.out" }, 0.75);\n'
'    tl.fromTo("#process-r3", { opacity: 0, x: 24, filter: "blur(8px)" }, { opacity: 1, x: 0, filter: "blur(0px)", duration: 0.45, ease: "expo.out" }, 1.2);\n'
+ out(["#process-line", "#process-r1", "#process-r2", "#process-r3", "#process-rail"], 3.72))))

# 8. bar — 얼스바 하나로
d = 3.2
S.append(("bar", d, scene("bar", d, "#FFFFFF", """
    #bar-obj { left:250px; top:560px; width:520px; }
    .tag { position:absolute; color:#193B2A; font-size:44px; font-weight:600; letter-spacing:-0.03em; padding:12px 26px; border-radius:999px; background:#EEF0E9; white-space:nowrap; }
    #bar-t1 { left:108px; top:470px; } #bar-t2 { left:700px; top:620px; } #bar-t3 { left:150px; top:1100px; }""",
f"""{line("bar", "얼스바 하나로", "샴푸, 린스, 바디워시까지", d)}
    <div id="bar-obj" class="obj"><img src="assets/img/bar-white-cut.png" alt="이든 얼스바"></div>
    <div class="tag clip" id="bar-t1" data-start="0" data-duration="{d}" data-track-index="3" data-layout-allow-overlap>샴푸</div>
    <div class="tag clip" id="bar-t2" data-start="0" data-duration="{d}" data-track-index="4" data-layout-allow-overlap>린스</div>
    <div class="tag clip" id="bar-t3" data-start="0" data-duration="{d}" data-track-index="5" data-layout-allow-overlap>바디워시</div>""",
'    tl.fromTo("#bar-obj", { scale: 1.15, opacity: 0, filter: "blur(14px)" }, { scale: 1, opacity: 1, filter: "blur(0px)", duration: 0.8, ease: "expo.out" }, 0);\n'
'    tl.fromTo("#bar-obj", { rotation: -4 }, { rotation: 4, duration: 3.2, ease: "none" }, 0);\n'
+ line_in("bar", 0.2) +
'    tl.fromTo(["#bar-t1", "#bar-t2", "#bar-t3"], { opacity: 0, scale: 0.92, filter: "blur(6px)" }, { opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.35, ease: "expo.out", stagger: 0.12 }, 0.7);\n'
+ out(["#bar-line", "#bar-obj", "#bar-t1", "#bar-t2", "#bar-t3"], 2.92))))

# 9. oral — 고체 치약, 대나무 칫솔
d = 3.2
S.append(("oral", d, scene("oral", d, "#FFFFFF", """
    #oral-tabs { left:200px; top:480px; width:345px; }
    #oral-brush { left:720px; top:440px; width:66px; }""",
f"""{line("oral", "튜브 대신 유리병,", "칫솔모까지 식물성으로", d)}
    <div id="oral-tabs" class="obj"><img src="assets/img/tabs-cut.png" alt="이든 고체 치약"></div>
    <div id="oral-brush" class="obj"><img src="assets/img/brush-cut.png" alt="이든 대나무 칫솔"></div>""",
'    tl.fromTo("#oral-tabs", { x: -80, opacity: 0, filter: "blur(12px)" }, { x: 0, opacity: 1, filter: "blur(0px)", duration: 0.7, ease: "expo.out" }, 0.05);\n'
'    tl.fromTo("#oral-brush", { x: 80, opacity: 0, filter: "blur(12px)" }, { x: 0, opacity: 1, filter: "blur(0px)", duration: 0.7, ease: "expo.out" }, 0.25);\n'
'    tl.to(["#oral-tabs", "#oral-brush"], { y: -12, duration: 2.4, ease: "power1.inOut" }, 0.6);\n'
+ line_in("oral", 0.25, "ink") + out(["#oral-line", "#oral-tabs", "#oral-brush"], 2.92))))

# 10. kit — 종이 상자, 뚜껑 나무에서 숲으로
d = 3.4
S.append(("kit", d, scene("kit", d, "#FFFFFF", """
    #kit-cam { left:170px; top:400px; width:740px; }
    #kit-iris { position:absolute; inset:0; }
    #kit-iris img { position:absolute; inset:0; width:100%; height:100%; object-fit:cover; }""",
f"""{line("kit", "포장은", "종이 상자에 담습니다", d)}
    <div id="kit-cam" class="obj"><img src="assets/img/kit-cut.png" alt="종이 상자에 담긴 이든 스타터 키트"></div>
    <div id="kit-iris" class="clip" data-start="0" data-duration="{d}" data-track-index="3" data-layout-ignore><img src="assets/img/borneo.jpg" alt="보르네오 숲"></div>""",
'    tl.fromTo("#kit-cam", { scale: 1.1, opacity: 0, filter: "blur(12px)" }, { scale: 1, opacity: 1, filter: "blur(0px)", duration: 0.8, ease: "expo.out" }, 0);\n'
'    tl.to("#kit-cam", { scale: 1.06, duration: 2.1, ease: "power1.inOut" }, 0.8);\n'
+ line_in("kit", 0.25, "ink") +
'    tl.to("#kit-line", { opacity: 0, filter: "blur(8px)", duration: 0.15, ease: "power3.in" }, 2.75);\n'
'    tl.fromTo("#kit-iris", { clipPath: "circle(0% at 662px 730px)" }, { clipPath: "circle(120% at 662px 730px)", duration: 0.55, ease: "power3.in" }, 2.85);\n')))

# 11. forest — 10,000그루
d = 5.0
S.append(("forest", d, scene("forest", d, "#193B2A", """
    #forest-cam { position:absolute; inset:0; }
    #forest-img { position:absolute; inset:0; width:100%; height:100%; object-fit:cover; }
    #forest-top { position:absolute; left:0; right:0; top:0; height:42%; background:linear-gradient(180deg, rgba(12,28,20,.8), rgba(12,28,20,0)); }
    #forest-bot { position:absolute; left:0; right:0; bottom:0; height:50%; background:linear-gradient(180deg, rgba(12,28,20,0), rgba(12,28,20,.82)); }
    #forest-count { position:absolute; left:108px; bottom:260px; color:#FFFFFF; font-family:"Outfit", sans-serif; font-size:200px; line-height:1; font-weight:500; letter-spacing:-0.04em; font-variant-numeric:tabular-nums; }
    #forest-unit { position:absolute; left:108px; right:108px; bottom:160px; color:#D9E4DC; font-size:46px; line-height:1.3; font-weight:600; letter-spacing:-0.03em; }
    #forest-flood { position:absolute; inset:0; background:#193B2A; }""",
f"""    <div id="forest-cam"><img id="forest-img" src="assets/img/borneo.jpg" alt="보르네오 열대우림 사이로 흐르는 강"></div>
    <div id="forest-top"></div><div id="forest-bot"></div>
{line("forest", "제품이 팔릴수록", "보르네오의 숲이 자랍니다", d, dark=True)}
    <div id="forest-count" class="clip" data-start="0" data-duration="{d}" data-track-index="3">0</div>
    <p id="forest-unit" class="clip" data-start="0" data-duration="{d}" data-track-index="4">그루, 탄중푸팅 국립공원에 심은 나무</p>
    <div id="forest-flood" class="clip" data-start="0" data-duration="{d}" data-track-index="5" data-layout-ignore></div>""",
'    tl.fromTo("#forest-cam", { scale: 1.0 }, { scale: 1.08, duration: 5, ease: "power1.inOut" }, 0);\n'
+ line_in("forest", 0.2) +
'    const c = { v: 0 }; const el = document.querySelector("#forest-count");\n'
'    tl.fromTo("#forest-count", { opacity: 0 }, { opacity: 1, duration: 0.15, ease: "power2.out" }, 1.0);\n'
'    tl.fromTo(c, { v: 0 }, { v: 10000, duration: 1.5, ease: "power3.out", onUpdate: () => { el.textContent = Math.round(c.v).toLocaleString("en-US"); } }, 1.0);\n'
'    tl.fromTo("#forest-unit", { opacity: 0, filter: "blur(8px)" }, { opacity: 1, filter: "blur(0px)", duration: 0.2, ease: "power4.out" }, 1.4);\n'
+ out(["#forest-line", "#forest-count", "#forest-unit"], 4.45) +
'    tl.fromTo("#forest-flood", { clipPath: "inset(100% 0% 0% 0%)" }, { clipPath: "inset(0% 0% 0% 0%)", duration: 0.4, ease: "power2.inOut" }, 4.58);\n')))

# 12. end
d = 4.0
S.append(("end", d, scene("end", d, "#193B2A", """
    #end-mark { position:absolute; left:108px; top:380px; width:100px; height:auto; }
    #end-title { position:absolute; left:108px; top:540px; color:#FFFFFF; font-family:"Outfit", sans-serif; font-size:132px; line-height:1.02; font-weight:500; letter-spacing:-0.035em; }
    #end-title span { display:inline-block; }
    #end-sign { position:absolute; left:108px; top:860px; color:#B9CBBE; font-family:"Outfit", sans-serif; font-size:44px; line-height:1.3; font-weight:400; }""",
f"""    <img id="end-mark" class="clip" data-start="0" data-duration="{d}" data-track-index="2" src="assets/img/mark-white.png" alt="이든 나무 로고">
    <h2 id="end-title" class="clip" data-start="0" data-duration="{d}" data-track-index="3" data-hold><span id="end-w1">Less Plastic.</span><br><span id="end-w2">More Trees.</span></h2>
    <p id="end-sign" class="clip" data-start="0" data-duration="{d}" data-track-index="4" data-hold>Idden by Sustainable LAB</p>""",
'    tl.fromTo("#end-mark", { opacity: 0, y: 16, filter: "blur(6px)" }, { opacity: 1, y: 0, filter: "blur(0px)", duration: 0.5, ease: "expo.out" }, 0.1);\n'
'    tl.fromTo("#end-w1", { opacity: 0, filter: "blur(8px)" }, { opacity: 1, filter: "blur(0px)", duration: 0.22, ease: "power4.out" }, 0.25);\n'
'    tl.fromTo("#end-w2", { opacity: 0, filter: "blur(8px)" }, { opacity: 1, filter: "blur(0px)", duration: 0.22, ease: "power4.out" }, 0.6);\n'
'    tl.fromTo("#end-sign", { opacity: 0, filter: "blur(6px)" }, { opacity: 1, filter: "blur(0px)", duration: 0.22, ease: "power4.out" }, 0.95);\n'
+ out(["#end-mark", "#end-title", "#end-sign"], 3.72))))

# write scenes and index
t = 0.0
hosts = []
for cid, dur, html in S:
    open(os.path.join(COMP, f"{cid}.html"), "w", encoding="utf-8").write(html)
    hosts.append(f'      <div id="{cid}" data-composition-id="{cid}" data-composition-src="compositions/{cid}.html" data-start="{round(t,2)}" data-duration="{dur}" data-track-index="1" data-track-kind="graphics" data-width="1080" data-height="1350"></div>')
    t += dur
total = round(t, 2)
index = f"""<!doctype html>
<html lang="ko" data-composition-variables='[
  {{"id":"color-ground","type":"color","label":"Background","default":"#FFFFFF"}},
  {{"id":"color-ink","type":"color","label":"Text","default":"#193B2A"}}
]'>
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1350" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
      /* v4 약 {total}초. SPEC.md 참고. 흰 바탕 #FFFFFF, 짙은 초록 #193B2A, Outfit 500, Pretendard 600. */
      @font-face {{ font-family: "Pretendard"; src: url("assets/fonts/PretendardVariable.woff2") format("woff2"); font-weight: 100 900; }}
      :root {{ --color-ground:#FFFFFF; --color-ink:#193B2A; }}
      * {{ margin:0; padding:0; box-sizing:border-box; }}
      html, body {{ margin:0; width:1080px; height:1350px; overflow:hidden; background:var(--color-ground); }}
      #root {{ position:relative; width:100%; height:100%; font-family:"Pretendard", sans-serif; }}
      #ground {{ position:absolute; inset:0; background:var(--color-ground); }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{total}" data-width="1080" data-height="1350">
      <div id="ground"></div>
{chr(10).join(hosts)}
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""
open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(index)
print("scenes", len(S), "total", total)
