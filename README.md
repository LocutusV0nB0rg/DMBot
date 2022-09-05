# DMBot
DMBot für D&amp;D Sucht Selbsthilfegruppe

## Funktionen

Der Bot antwortet im in der Config angegebenen Channel auf Fragen von Spielern und auf die Antworten von den DM's.

Spielernichtfrage (Satz ohne ?): Das ist keine Frage!
Spielerfrage: Das ist eine dumme Frage!
Antwort des DM's: Gute Antwort! :)

## Setup

In dem Verzeichnis vom Bot muss eine Datei bot.yml angelegt werden, die die Konfigurationsdaten des Bots enthält. Diese muss in etwa so aussehen:

```yaml

bot:
    token: "bot.auth.token"
    channel: "General"
	logchannel: 0123456789
    
roles:
    dungeon_master: "Almighty DM"
```

Danach müssen die in der dependencies.txt angegebenen Python-Module installiert werden. Ich empfehle pip für diesen Schritt.

Anschließend kann der Bot mit `python3 dmbot.py` gestartet werden.
