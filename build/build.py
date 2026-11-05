import re,base64,subprocess,sys,os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
s=open('src.html',encoding='utf-8').read()
chars=set(re.sub(r'<[^>]+>|\s','',s))|set(''.join(chr(c) for c in range(32,127)))|set('·↗—–’“”…')
open('font/chars.txt','w',encoding='utf-8').write(''.join(sorted(chars)))
subprocess.check_call([sys.executable,'-m','fontTools.subset','font/PretendardVariable.woff2','--text-file=font/chars.txt','--flavor=woff2','--layout-features=*','--output-file=font/sub.woff2'])
b=base64.b64encode(open('font/sub.woff2','rb').read()).decode()
ff='@font-face{font-family:"Pretendard";font-weight:100 900;font-style:normal;font-display:swap;src:url(data:font/woff2;base64,%s) format("woff2")}'%b
open('../index.html','w',encoding='utf-8').write(s.replace('/*FONT_FACE*/',ff))
print('font KB',os.path.getsize('font/sub.woff2')//1024,'index KB',os.path.getsize('../index.html')//1024)
