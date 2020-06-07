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

symbol_boden = ":white_large_square:"
symbol_wand = ":brick:"
symbol_monster = ":dragon:"
symbol_spieler = ":snake:"

if not emoji_support:
    
    symbol_boden = "."
    symbol_wand = "#"
    symbol_monster = "m"
    symbol_spieler = "@"


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
    "y": 12
}

# Diese Funktion zentriert einen Text
def zentriere_text(text):
    return zentriere_text_ausdruck.format(text)

def zahl_zwischen(min, max, zahl):
    if zahl < min:
        return min
    if zahl > max:
        return max
    return zahl

def symbol_in_welt(x, y, breite, hoehe, welt):
    # Stelle sicher, dass sich die Position in der Welt befindet...
    x = zahl_zwischen(0, breite - 1, x)
    y = zahl_zwischen(0, hoehe - 1, y)
    return welt[y][x]

def platziere_spieler(breite, hoehe, welt):
    while True:
        x = random.randint(0, breite - 1)
        y = random.randint(0, hoehe - 1)
        symbol = symbol_in_welt(x, y, breite, hoehe, welt)
        if symbol != symbol_wand:
            return (x, y)

def generiere_volle_welt(breite, hoehe):
    welt = []
    for y in range(hoehe):
        reihe = []
        for x in range(breite):
            reihe.append(symbol_wand)

        welt.append(reihe)
    return welt

def platziere_boden_flaechen(anzahl_boden_flaechen, breite, hoehe, welt):
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

def platziere_monster(anzahl_monster, breite, hoehe, welt):
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


def generiere_welt(breite, hoehe, anzahl_boden_flaechen, anzahl_monster):
    welt = generiere_volle_welt(breite, hoehe)
    welt = platziere_boden_flaechen(anzahl_boden_flaechen, breite, hoehe, welt)
    welt, monster = platziere_monster(anzahl_monster, breite, hoehe, welt)
    
    # Platziere Spieler

    spieler["x"], spieler["y"] = platziere_spieler(breite, hoehe, welt)
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

def bewege_spieler(aktion, breite, hoehe, welt):
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
    symbol = symbol_in_welt(neues_x, neues_y, breite, hoehe, welt)
    spieler_darf_sich_bewegen = symbol != symbol_wand
    if spieler_darf_sich_bewegen:
        spieler["x"] = neues_x
        spieler["y"] = neues_y

def bewege_monster(monster, breite, hoehe, welt):
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
        symbol = symbol_in_welt(neues_x, neues_y, breite, hoehe, welt)
        monster_darf_sich_bewegen = symbol != symbol_wand
        if monster_darf_sich_bewegen:
            element["x"] = neues_x
            element["y"] = neues_y

def spiel_starten():
    breite = 50
    hoehe = 20
    anzahl_boden_flaechen = int(breite * hoehe * 0.5)
    anzahl_monster = 5

    welt, monster = generiere_welt(breite, hoehe, anzahl_boden_flaechen, anzahl_monster)
    spiel_beenden = False
    while not spiel_beenden:
        system(loeschte_terminal_inhalt)
        zeichne_welt(welt, monster)

        # Werte Aktion aus...
        aktion = console.input("Deine Aktion: ")
        aktion = aktion.lower()
        
        bewege_spieler(aktion, breite, hoehe, welt)
        bewege_monster(monster, breite, hoehe, welt)
    
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
    spiel_starten()
elif auswahl == "2":
    spiel_laden()
elif auswahl == "3":
    highscore_anzeigen()