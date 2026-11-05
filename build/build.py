# 브랜드 페이지(src.html → ../index.html)와 제품 정보 페이지(dpp-src.html → ../dpp.html)를 만든다.
# 두 원본에 쓰인 글자만 골라 Pretendard 부분 글꼴을 만들고 각 파일 안에 넣는다. 실행: python build/build.py
import re, base64, subprocess, sys, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
pages = [('src.html', '../index.html'), ('dpp-src.html', '../dpp.html')]
srcs = {a: open(a, encoding='utf-8').read() for a, _ in pages}
chars = set(''.join(re.sub(r'\s', '', s) for s in srcs.values())) | set(''.join(chr(c) for c in range(32, 127))) | set('·↗—–’“”…')
open('font/chars.txt', 'w', encoding='utf-8').write(''.join(sorted(chars)))
subprocess.check_call([sys.executable, '-m', 'fontTools.subset', 'font/PretendardVariable.woff2', '--text-file=font/chars.txt',
                       '--flavor=woff2', '--layout-features=*', '--output-file=font/sub.woff2'])
b = base64.b64encode(open('font/sub.woff2', 'rb').read()).decode()
ff = '@font-face{font-family:"Pretendard";font-weight:100 900;font-style:normal;font-display:swap;src:url(data:font/woff2;base64,%s) format("woff2")}' % b
for a, out in pages:
    open(out, 'w', encoding='utf-8').write(srcs[a].replace('/*FONT_FACE*/', ff))
    print(out, os.path.getsize(out) // 1024, 'KB')
print('font KB', os.path.getsize('font/sub.woff2') // 1024)
