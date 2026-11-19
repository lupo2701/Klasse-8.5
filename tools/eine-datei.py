#!/usr/bin/env python3
"""Packt die ganze Lern-App in EINE HTML-Datei für die interne Lernplattform.

Startseite, Mathe-, NaWi- und Englisch-App stecken danach komplett in
dist/Lern-App-Klasse-8.5.html. Die Datei lädt nichts nach, braucht kein GitHub
und läuft auch heruntergeladen ohne Internet.

Aufruf im Projektordner:   python3 tools/eine-datei.py
Nach jeder Änderung an der App neu ausführen und die neue Datei hochladen.
"""
import base64
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "dist" / "Lern-App-Klasse-8.5.html"


def replace_once(text, old, new, what):
    if text.count(old) != 1:
        sys.exit(f"Stelle nicht eindeutig gefunden: {what}. Wurde index.html umgebaut? Dann dieses Skript anpassen.")
    return text.replace(old, new)


def cut(text, start, end, new, what):
    """Ersetzt alles von start (einschließlich) bis end (ausschließlich)."""
    a = text.find(start)
    b = text.find(end, a + 1)
    if a < 0 or b < 0:
        sys.exit(f"Stelle nicht gefunden: {what}")
    return text[:a] + new + text[b:]


def inline_app(index_path):
    """Liest eine Unter-App und baut CSS- und JS-Dateien direkt in ihr HTML ein."""
    folder = index_path.parent
    html = index_path.read_text(encoding="utf-8")

    def css(m):
        return "<style>\n" + (folder / m.group(1)).read_text(encoding="utf-8") + "\n</style>"

    def js(m):
        code = (folder / m.group(1)).read_text(encoding="utf-8")
        return "<script>\n" + code.replace("</script", "<\\/script") + "\n</script>"

    html = re.sub(r'<link rel="stylesheet" href="([^"]+)">', css, html)
    html = re.sub(r'<script src="([^"]+)"></script>', js, html)
    leftover = re.findall(r'(?:src|href)="(?!#|data:|https?:)([^"]+\.(?:js|css|png|jpg|svg))"', html)
    if leftover:
        sys.exit(f"{index_path}: diese Dateien konnte ich nicht einbauen: {leftover}")
    return html


page = (ROOT / "index.html").read_text(encoding="utf-8")

# 1. Alle eingebundenen Apps finden und einpacken
srcs = sorted(set(re.findall(r'kind:"app",src:"([^"]+)"', page)))
bundle = {}
for src in srcs:
    bundle[src] = base64.b64encode(inline_app(ROOT / src).encode("utf-8")).decode("ascii")
    print(f"  eingepackt: {src}")

# 2. Kopf: kein Manifest, Symbol direkt in der Datei
icon = base64.b64encode((ROOT / "icon-192.png").read_bytes()).decode("ascii")
page = cut(page, '<link rel="manifest"', "<style>",
           f'<link rel="icon" href="data:image/png;base64,{icon}">\n', "Kopfbereich")

# 3. Apps aus der Datei statt aus Ordnern laden
# Wird die Datei direkt vom Gerät geöffnet (file://), dürfen die eingebetteten Apps
# nicht selbst speichern. Dann speichert die Startseite stellvertretend für sie:
# die App bekommt beim Öffnen eine Kopie der Daten und meldet jede Änderung zurück.
SHIM = ("<script>(function(){try{localStorage.getItem('x');return;}catch(e){}"
        "var d=__SEED__,has=function(k){return Object.prototype.hasOwnProperty.call(d,k);},"
        "tell=function(k,v){try{parent.postMessage({kl85:1,k:k,v:v},'*');}catch(e){}},"
        "s={getItem:function(k){return has(k)?d[k]:null;},setItem:function(k,v){d[k]=String(v);tell(k,d[k]);},"
        "removeItem:function(k){delete d[k];tell(k,null);},clear:function(){for(var k in d)s.removeItem(k);},"
        "key:function(i){return Object.keys(d)[i]||null;}};"
        "Object.defineProperty(s,'length',{get:function(){return Object.keys(d).length;}});"
        "try{Object.defineProperty(window,'localStorage',{value:s,configurable:true});}catch(e){}})();</script>")
loader = ("var BUNDLE=" + "{" + ",".join(f'"{k}":"{v}"' for k, v in bundle.items()) + "}, lastBlob=null;\n"
          "var SHIM=" + repr(SHIM).replace("</", "<\\/") + ";\n"
          "function srcOf(src){ /* App aus dieser Datei als eigene Seite bereitstellen */\n"
          "  if(!BUNDLE[src])return src;\n"
          "  var b=atob(BUNDLE[src]),u=new Uint8Array(b.length);for(var i=0;i<b.length;i++)u[i]=b.charCodeAt(i);\n"
          "  var html=new TextDecoder().decode(u), seed={};\n"
          "  try{for(var j=0;j<localStorage.length;j++){var k=localStorage.key(j);seed[k]=localStorage.getItem(k);}}catch(e){}\n"
          "  html=html.replace(/<head>/i,'<head>'+SHIM.replace('__SEED__',JSON.stringify(seed).replace(/<\\//g,'<\\\\/')));\n"
          "  if(lastBlob)URL.revokeObjectURL(lastBlob);\n"
          "  return lastBlob=URL.createObjectURL(new Blob([html],{type:'text/html;charset=utf-8'}));\n}\n"
          "window.addEventListener('message',function(e){ /* Speicherwunsch einer eingebetteten App */\n"
          "  var fr=main.querySelector('iframe'), m=e.data;\n"
          "  if(!fr||e.source!==fr.contentWindow||!m||m.kl85!==1||typeof m.k!=='string')return;\n"
          "  try{ if(m.v===null)localStorage.removeItem(m.k); else localStorage.setItem(m.k,String(m.v)); }catch(err){}\n"
          "});\n")
page = replace_once(page, "function available(src){",
                    loader + "function available(src){ if(BUNDLE[src])return Promise.resolve(true);", "available()")
page = replace_once(page, """ext.href=t.src; ext.hidden=false; main.innerHTML='<iframe src="'+t.src+'\"""",
                    """ext.hidden=true; main.innerHTML='<iframe src="'+srcOf(t.src)+'\"""", "iframe")

# 4. Kein Installieren und kein Offline-Speicher (gibt es auf der Plattform nicht)
page = re.sub(r"\n\s*if\(!standalone\)h\+='<button class=\"btn ghost\" id=\"hinst\">[^\n]*", "", page)
page = cut(page, '/* Offline-Betrieb', "})();\n</script>", "", "Service Worker")

# 5. Texte für die interne Fassung
page = replace_once(page,
    "<li>Die Seite wird über GitHub Pages geladen. Dabei verarbeitet GitHub wie jeder Webserver technische Daten, zum Beispiel die IP-Adresse.</li>",
    "<li>Die Datei liegt auf der Lernplattform der Schule. Beim Herunterladen verarbeitet die Plattform wie jeder Server technische Daten, zum Beispiel die IP-Adresse.</li>",
    "Datenschutztext")
page = replace_once(page, "Unter <b>Info</b> oben rechts findest du das jederzeit wieder. Dort steht auch, wie du die App auf den Startbildschirm legst.",
                    "Unter <b>Info</b> oben rechts findest du das jederzeit wieder.", "Willkommenstext")
page = cut(page, """'<div class="card"><h3>Als App auf den Startbildschirm</h3>'""",
           """'<div class="card"><h3>Fortschritt löschen""",
           """'<div class="card"><h3>Ohne Internet nutzen</h3><ol><li>Die Datei von der Lernplattform herunterladen.</li>"""
           """<li>Die heruntergeladene Datei mit Chrome, Edge, Firefox oder Safari öffnen.</li>"""
           """<li>Immer dieselbe Datei im selben Browser öffnen, dann bleibt dein Fortschritt erhalten.</li></ol>"""
           """<p class="lead">Kommt eine neue Fassung, ersetze die alte Datei durch die neue an derselben Stelle.</p></div>'+\n"""
           """    '<div class="card"><h3>Quellen</h3><ul><li>NaWi „Der Weg der Nahrung“: neu formuliert nach der Materialsammlung """
           """„Der Weg der Nahrung“ des Bundeszentrums für Ernährung (BZfE/BLE).</li><li>Englisch „Acting green“: Übungen zum Workbook, Seiten 18–21.</li></ul>"""
           """<p class="lead">Nur für den Unterricht der Klasse 8.5, bitte nicht öffentlich weitergeben.</p></div>'+\n    """,
           "Info-Seite")
page = replace_once(page, 'var b=document.getElementById("inst");\n  b.onclick', 'var b=document.getElementById("inst");\n  if(b)b.onclick', "Installieren-Knopf")

OUT.parent.mkdir(exist_ok=True)
OUT.write_text(page, encoding="utf-8")
print(f"Fertig: {OUT.relative_to(ROOT)} ({OUT.stat().st_size // 1024} KB)")
