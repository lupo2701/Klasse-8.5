# Klasse 8.5 – Lern-App

Startseite für die Klasse 8.5: Fach wählen, dann Thema wählen.

- **Mathe** → *Terme und Gleichungen* öffnet die App x-Quest (Ordner `mathe/`, Kopie aus dem Repo `Mathe`)
- **NaWi** → *Der Weg der Nahrung* öffnet die NaWi-Lern-App (Ordner `nawi/`, Kopie aus dem Repo `Lernapp-Nawi`)
- **Deutsch, Englisch** und weitere Themen: Platz für eigene Notizen

In der App lassen sich eigene Fächer und Themen hinzufügen. Sie werden nur auf dem jeweiligen Gerät gespeichert.

## Neue Themen fest für alle eintragen

In `index.html` steht oben im Skript die Liste `FAECHER`. Dort ein Thema ergänzen:

```js
{id:"prozent", name:"Prozent- und Zinsrechnung"}                    // nur Notizen
{id:"terme", name:"Terme und Gleichungen", kind:"app", src:"mathe/index.html"}  // eigene App im Unterordner
```

## Online stellen

GitHub → Settings → Pages → Branch `main`, Ordner `/ (root)` → Save.
Danach ist die App unter `https://lupo2701.github.io/Klasse-8.5/` erreichbar.
