"""Builds the installable web game (index.html) from game.html.
game.html is the source; it is also what runs inside Claude.
Run: python3 build.py 0.6   (the version goes into the offline cache name)
     python3 build.py release  (Play Store build: real ads instead of test ads)"""
import sys,re
ver=sys.argv[1] if len(sys.argv)>1 else 'dev'
s=open('game.html').read().replace('<title>Pocket Blox</title>\n','',1)
# The public build never contains the private test language.
s=re.sub(r'/\*HR-START\*/.*?/\*HR-END\*/','',s,flags=re.S)
assert "hr:{" not in s
head='''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no,viewport-fit=cover">
<title>Pocket Blox</title>
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="Pocket Blox">
<meta name="theme-color" content="#1e2124">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<link rel="icon" href="icon-192.png">
<link rel="manifest" href="manifest.webmanifest">
<style>html,body{margin:0;overscroll-behavior:none;touch-action:manipulation}body{padding-top:max(16px,env(safe-area-inset-top))!important;padding-bottom:max(16px,env(safe-area-inset-bottom))!important}</style>
</head>
<body>
'''
tail='''
<script>if('serviceWorker' in navigator)window.addEventListener('load',()=>navigator.serviceWorker.register('sw.js').catch(()=>{}));</script>
</body>
</html>
'''
open('index.html','w').write(head+s+tail)
# Android/iOS app shell (Capacitor): same game, no service worker, files bundled in the app.
import os,shutil
os.makedirs('app/www',exist_ok=True)
# Test builds show Google test ads; only `python3 build.py release` switches the app to real ads.
app=s.replace('testing:true/*TESTING*/','testing:false/*TESTING*/') if ver=='release' else s
assert 'testing:true/*TESTING*/' in s
open('app/www/index.html','w').write(head.replace('<link rel="manifest" href="manifest.webmanifest">\n','')+app+'\n</body>\n</html>\n')
for f in ('icon-192.png','icon-512.png','apple-touch-icon.png'):shutil.copy(f,'app/www/'+f)
sw=open('sw.js').read()
sw=re.sub(r"const VERSION='[^']*';",f"const VERSION='pocket-blox-v{ver}';",sw)
open('sw.js','w').write(sw)
print('built',ver)
