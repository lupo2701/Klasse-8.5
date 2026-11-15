# Klasse 8.5 – Lern-App

Startseite für die Klasse 8.5: Fach wählen, dann Thema wählen.

- **Mathe** → *Terme und Gleichungen* öffnet die App x-Quest (Ordner `mathe/`, Kopie aus dem Repo `Mathe`)
- **NaWi** → *Der Weg der Nahrung* öffnet die NaWi-Lern-App (Ordner `nawi/`, Kopie aus dem Repo `Lernapp-Nawi`)
- **Deutsch, Englisch** und weitere Themen: Platz für eigene Notizen

## Was die App kann

- **Zwei Ansichten:** einfache Ansicht oder Spiel-Ansicht mit Figur, Level und Geschenken (umschaltbar auf der Startseite)
- **Punkte:** XP aus der Mathe- und der NaWi-App zählen automatisch mit; ein als „geschafft“ markiertes Thema gibt 25 XP
- **Geschenke je Fach** bei 50, 150 und 300 XP, zum Beispiel Geodreieck (Mathe) oder Keimling (NaWi)
- **Datenschutz-Hinweis** beim ersten Start; alles bleibt im Browser des Geräts, keine fremden Schriften oder Skripte
- **Installierbar** auf dem Startbildschirm und offline nutzbar (`manifest.webmanifest`, `sw.js`); Anleitung in der App unter „Info“
- Eigene Fächer und Themen lassen sich hinzufügen (nur auf dem jeweiligen Gerät)

Die Themen folgen dem Rahmenlehrplan 1–10 Berlin/Brandenburg, Doppeljahrgangsstufe 7/8. Welche davon in Klasse 8 liegen, regelt das schulinterne Curriculum.

Wenn in `mathe/` oder `nawi/` Dateien dazukommen, die Dateiliste in `sw.js` ergänzen und dort `CACHE` hochzählen.

## Neue Themen fest für alle eintragen

In `index.html` steht oben im Skript die Liste `FAECHER`. Dort ein Thema ergänzen:

```js
{id:"prozent", name:"Prozent- und Zinsrechnung"}                    // nur Notizen
{id:"terme", name:"Terme und Gleichungen", kind:"app", src:"mathe/index.html"}  // eigene App im Unterordner
```

## Online stellen

GitHub → Settings → Pages → Branch `main`, Ordner `/ (root)` → Save.
Danach ist die App unter `https://lupo2701.github.io/Klasse-8.5/` erreichbar.
