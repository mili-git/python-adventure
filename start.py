from rich.console import Console
from rich.panel import Panel
from rich import print as rprint
from os import system, name
import random

# Globale variablen
console = Console()
menu_text = "Wilkommen in Python Adventure!\n\n1: Spiel starten\n2: Spiel laden\n3: Highscore ansehen"
terminal_breite = console.size.width
terminal_hoehe = console.size.height

# Sollen die Zeichen als Emoji oder normale Text zeichen dargestellt werden
emoji_support = True

# Die unterstützten Emojis können unter folgendem Link gefunden werden: https://github.com/willmcgugan/rich/blob/master/rich/_emoji_codes.py
symbol_boden = ":white_large_square:"
symbol_wand = ":brick:"
symbol_monster = ":dragon:"
symbol_spieler = ":snake:"
symbol_ziel = ":castle:"
symbol_leben = ":sparkling_heart:"

if not emoji_support:
    symbol_boden = "."
    symbol_wand = "#"
    symbol_monster = "m"
    symbol_spieler = "@"
    symbol_ziel = "%"
    symbol_leben = "+"

# https://stackoverflow.com/questions/8907236/center-aligning-text-on-console-in-python
zentriere_text_ausdruck = '{:^' + str(terminal_breite) + '}'


# Auf Linux und Mac heisst der Befehl 'clear'
loeschte_terminal_inhalt = 'clear'

# Auf Windows heisst der Befehl 'cls'
if name == 'nt':
    loeschte_terminal_inhalt = 'cls'

spieler = {
    "zeichen": symbol_spieler,
    "x": 5,
    "y": 12,
    "leben" : 3,
    "anzahl_schritte": 0
}

breite = 50
hoehe = 15
anzahl_aufnehmbare_leben = 5

spiel_beenden = False


# Diese Funktion zentriert einen Text
def zentriere_text(text):
    return zentriere_text_ausdruck.format(text)

def zahl_zwischen(min, max, zahl):
    if zahl < min:
        return min
    if zahl > max:
        return max
    return zahl

def symbol_in_welt(x, y, welt):
    # Stelle sicher, dass sich die Position in der Welt befindet...
    x = zahl_zwischen(0, breite - 1, x)
    y = zahl_zwischen(0, hoehe - 1, y)
    return welt[y][x]

def platziere_spieler(welt):
    while True:
        x = random.randint(0, breite - 1)
        y = random.randint(0, hoehe - 1)
        symbol = symbol_in_welt(x, y, welt)
        if symbol == symbol_boden:
            return (x, y)

def platziere_ziel(welt):
    while True:
        x = random.randint(0, breite - 1)
        y = random.randint(0, hoehe - 1)
        symbol = symbol_in_welt(x, y, welt)
        # Das Ziel kann nur auf einer Bodenfläche platziert werden...
        if symbol == symbol_boden:
            welt[y][x] = symbol_ziel
            return welt

def generiere_volle_welt():
    welt = []
    for y in range(hoehe):
        reihe = []
        for x in range(breite):
            reihe.append(symbol_wand)

        welt.append(reihe)
    return welt


def platziere_leben(welt):
    while True:
        x = random.randint(0, breite - 1)
        y = random.randint(0, hoehe - 1)
        symbol = symbol_in_welt(x, y, welt)
        # Das Leben kann nur auf einer Bodenfläche platziert werden...
        if symbol == symbol_boden:
            return (x, y)

def platziere_aufnehmbare_leben(welt):
    for i in range(anzahl_aufnehmbare_leben):
        x, y = platziere_leben(welt)
        welt[y][x] = symbol_leben
    return welt

def platziere_boden_flaechen(welt, anzahl_boden_flaechen):
    richtungen = ["norden", "osten", "westen", "sueden"]    
    momentane_boden_flaechen = 0

    # Starte immer in der Mitte der Welt
    x = int(breite * 0.5)
    y = int(hoehe * 0.5)
    while momentane_boden_flaechen < anzahl_boden_flaechen:
        # Bestimmte die Richtung, in welche "gelaufen" werden soll.
        richtungs_index = random.randint(0, len(richtungen) - 1)
        neue_richtung = richtungen[richtungs_index]
        if neue_richtung == "norden":
            y -= 1
        elif neue_richtung == "osten":
            x += 1
        elif neue_richtung == "westen":
            x-= 1
        elif neue_richtung == "sueden":
            y += 1

        # Stelle sicher dass sich X und Y noch in der welt befinden
        x = zahl_zwischen(0, breite - 1, x) 
        y = zahl_zwischen(0, hoehe - 1, y)

        if welt[y][x] == symbol_wand:
            welt[y][x] = symbol_boden
            momentane_boden_flaechen += 1
    return welt

def platziere_monster(anzahl_monster, welt):
    richtungen = ["norden", "osten", "westen", "sueden"]    
    momentane_anzahl_monster = 0
    alle_monster = []
    while momentane_anzahl_monster < anzahl_monster:
        x = random.randint(0, breite)
        y = random.randint(0, hoehe)
        # Bestimmte die Richtung, in welche "gelaufen" werden soll.
        richtungs_index = random.randint(0, len(richtungen) - 1)
        neue_richtung = richtungen[richtungs_index]
        if neue_richtung == "norden":
            y -= 1
        elif neue_richtung == "osten":
            x += 1
        elif neue_richtung == "westen":
            x-= 1
        elif neue_richtung == "sueden":
            y += 1

        # Stelle sicher dass sich X und Y noch in der welt befinden
        x = zahl_zwischen(0, breite - 1, x) 
        y = zahl_zwischen(0, hoehe - 1, y)

        if welt[y][x] == symbol_boden:
            alle_monster.append({
                "x": x,
                "y": y
            })
            momentane_anzahl_monster += 1
    return (welt, alle_monster)

def existiert_monster_auf_position(x, y, monster):
    for element in monster:
        if element["y"] == y and element["x"] == x:
            return True
    return False


def generiere_welt(anzahl_boden_flaechen, anzahl_monster):
    welt = generiere_volle_welt()
    welt = platziere_boden_flaechen(welt, anzahl_boden_flaechen)
    welt = platziere_aufnehmbare_leben(welt)
    welt = platziere_ziel(welt)
    welt, monster = platziere_monster(anzahl_monster, welt)

    # Platziere Spieler
    spieler["x"], spieler["y"] = platziere_spieler(welt)
    return (welt, monster)


def zeichne_welt(welt, monster):
    for y, reihe in enumerate(welt):
        reihe_text = ""
        for x, zeichen in enumerate(reihe):
            # Zeichne Spieler
            if x == spieler["x"] and y == spieler["y"]:
                reihe_text = reihe_text + spieler["zeichen"]
            # Zeichne Monster
            elif existiert_monster_auf_position(x, y, monster):
                reihe_text = reihe_text + symbol_monster
            # Zeichne alles andere
            else:
                reihe_text = reihe_text + zeichen
        rprint(reihe_text)

def bewege_spieler(aktion, welt, monster):
    neues_x = spieler["x"]
    neues_y = spieler["y"]
    if aktion == "w":
        neues_y -= 1
    elif aktion == "a":
        neues_x -= 1
    elif aktion == "s":
        neues_y += 1
    elif aktion == "d": 
        neues_x += 1

    neues_x = zahl_zwischen(0, breite - 1, neues_x)
    neues_y = zahl_zwischen(0, hoehe - 1, neues_y)
    symbol = symbol_in_welt(neues_x, neues_y, welt)
    spieler_darf_sich_bewegen = symbol != symbol_wand
    hat_sich_spieler_bewegt = spieler["x"] != neues_x or spieler["y"] != neues_y
    if spieler_darf_sich_bewegen and hat_sich_spieler_bewegt:
        spieler["anzahl_schritte"] += 1
        spieler["x"] = neues_x
        spieler["y"] = neues_y

        # Prüfe ob der Spieler ein Leben aufgenommen hat
        if symbol_in_welt(spieler["x"], spieler["y"], welt) == symbol_leben:
            spieler["leben"] += 1
            # Entferne das Leben aus der Welt
            welt[spieler["y"]][spieler["x"]] = symbol_boden

        # Prüfe ob der Spieler mit einem Monster kollidiert hat...
        if existiert_monster_auf_position(spieler["x"], spieler["y"], monster):
            spieler["leben"] -= 1
            spieler["x"], spieler["y"] = platziere_spieler(welt)

def bewege_monster(monster, welt):
    richtungen = ["norden", "osten", "westen", "sueden"]    
    for element in monster:
        neues_x = element["x"]
        neues_y = element["y"]
        richtungs_index = random.randint(0, len(richtungen) - 1)
        neue_richtung = richtungen[richtungs_index]
        if neue_richtung == "norden":
            neues_y -= 1
        elif neue_richtung == "osten":
            neues_x += 1
        elif neue_richtung == "westen":
            neues_x -= 1
        elif neue_richtung == "sueden":
            neues_y += 1

        # Darf sich das Monster bewegen
        neues_x = zahl_zwischen(0, breite - 1, neues_x)
        neues_y = zahl_zwischen(0, hoehe - 1, neues_y)
        symbol = symbol_in_welt(neues_x, neues_y, welt)
        monster_darf_sich_bewegen = symbol != symbol_wand
        monster_hat_sich_bewegt = element["x"] != neues_x or element["y"] != neues_y
        if monster_darf_sich_bewegen and monster_hat_sich_bewegt:
            element["x"] = neues_x
            element["y"] = neues_y

            # Prüfe ob sich der Spieler auf dieser Position befindet und ziehe Leben ab
            if element["x"] == spieler["x"] and element["y"] == spieler["y"]:
                spieler["leben"] -= 1
                spieler["x"], spieler["y"] = platziere_spieler(welt)


def zeichne_leben():
    lebens_anzeige = "Leben Spieler: [bold red]"
    for i in range(spieler["leben"]):
        lebens_anzeige = lebens_anzeige + symbol_leben + " "
    lebens_anzeige = lebens_anzeige + "[/bold red]"
    return lebens_anzeige

def zeichne_spieler_informationen():
    spieler_informationen = ""

    # Zeichne das Leben des Spielers
    spieler_informationen = spieler_informationen + zeichne_leben()
    
    # Zeichne die Anzahl Schritte, welcher der Spieler vorgenommen hat (wird für High Score verwendet.)
    spieler_informationen = spieler_informationen + "\n\rAnzahl Spielzüge: " + str(spieler["anzahl_schritte"])

    rprint(Panel(spieler_informationen))


def hilfe_text():
    hilfe_text = "Dies ist eine kurze Erklärung bzw. Hilfe zum Spiel\n\r"
    hilfe_text = hilfe_text + "Du bist eine Schlange, welche sich ihre Weg ins Schloss bahnen muss, um ins nächste Level zu gelangen\n\r"
    hilfe_text = hilfe_text + "Das Schloss wird jedoch von einer Horde von Drachen bewacht, weiche ihnen unbedingt aus!\n\r"
    hilfe_text = hilfe_text + "Jedoch gibt es auch Licht am Ende des Tunnels. Auf dem Weg zum Schloss gibt es Lebenselixire, welche du aufsammeln kannst!\n\r"
    hilfe_text = hilfe_text + "Das Spiel ist beendet, wenn du keine Leben mehr hast.\n\r"
    hilfe_text = hilfe_text + "Das Ziel ist es möglichst viele Level mit so wenigen Schritten wie möglich zu absolvieren.\n\r"
    hilfe_text = hilfe_text + "Eine High Score Übersicht mit den Anzahl Schritten pro Level kannst du unter [bold]Highscore ansehen[/bold] im Hauptmenü ansehen.\n\r"
    hilfe_text = hilfe_text + "Dein Fortschritt wird jeweils beim Erreichen des Schloss gespeichert, streng dich also an!!\n\r"
    hilfe_text = hilfe_text + "Jedes Level ist zufalls generiert, es stehen dir folgende Befehle zur Auswahl:\n\r"
    hilfe_text = hilfe_text + "Mit [bold]w[/bold] bewegst du dich nach oben\n\r"
    hilfe_text = hilfe_text + "Mit [bold]a[/bold] bewegst du dich nach links\n\r"
    hilfe_text = hilfe_text + "Mit [bold]s[/bold] bewegst du dich nach unten\n\r"
    hilfe_text = hilfe_text + "Mit [bold]d[/bold] bewegst du dich nach rechts\n\r"
    hilfe_text = hilfe_text + "Mit [bold]h[/bold] kannst du jederzeit diese Hilfe anzeigen\n\r"
    return hilfe_text

def zeige_hilfe_an():
    hilfe_schliessen = False
    text = hilfe_text()
    while not hilfe_schliessen:
        system(loeschte_terminal_inhalt)
        rprint(Panel(text))
        hilfe_schliessen = input("Um die Hilfe zu schliessen drücke bitte 'q': ").lower() == 'q'



def spiel_starten():
    # Benutze die globale variable für spiel_beenden
    global spiel_beenden
    anzahl_boden_flaechen = int(breite * hoehe * 0.5)
    anzahl_monster = 5

    welt, monster = generiere_welt(anzahl_boden_flaechen, anzahl_monster)

    while not spiel_beenden:
        system(loeschte_terminal_inhalt)
        zeichne_welt(welt, monster)
        zeichne_spieler_informationen()

        # Werte Aktion aus...
        aktion = console.input("Deine Aktion: ")
        aktion = aktion.lower()

        if aktion == "h":
            zeige_hilfe_an()
        
        bewege_spieler(aktion, welt, monster)
        bewege_monster(monster, welt)

        # Prüfe ob das Spiel beendet ist -> Der Spieler hat keine Leben mehr
        spiel_beenden = spieler["leben"] <= 0

    
def spiel_laden():
    rprint("Spiel wird geladen...")

def highscore_anzeigen():
    rprint("Highscore wird angezeigt...")

# Zeige Hauptmenu an
rprint(Panel(zentriere_text(menu_text), style="#F08080"))

# Werte die Auswahl für das Hauptmenü aus...
auswahl = ""
gueltige_eingabe = False
while not gueltige_eingabe:
    auswahl = console.input("Bitte triff eine Auswahl: ")
    gueltige_eingabe = auswahl == "1" or auswahl == "2" or auswahl == "3"

if auswahl == "1":
    zeige_hilfe_an()
    spiel_starten()
elif auswahl == "2":
    spiel_laden()
elif auswahl == "3":
    highscore_anzeigen()