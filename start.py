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

symbol_boden = ":white_large_square:"
symbol_wand = ":brick:"

# https://stackoverflow.com/questions/8907236/center-aligning-text-on-console-in-python
zentriere_text_ausdruck = '{:^' + str(terminal_breite) + '}'


# Auf Linux und Mac heisst der Befehl 'clear'
loeschte_terminal_inhalt = 'clear'

# Auf Windows heisst der Befehl 'cls'
if name == 'nt':
    loeschte_terminal_inhalt = 'cls'

spieler = {
    "zeichen": ":snake:",
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

def generiere_volle_welt(breite, hoehe):
    welt = []
    for y in range(hoehe):
        reihe = []
        for x in range(breite):
            reihe.append(symbol_wand)

        welt.append(reihe)
    return welt

def generiere_welt(breite, hoehe, anzahl_boden_flaechen):
#https://blog.jrheard.com/procedural-dungeon-generation-drunkards-walk-in-clojurescript 
    richtungen = ["norden", "osten", "westen", "sueden"]    
    welt = generiere_volle_welt(breite, hoehe)
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


def zeichne_welt(welt):
    for y, reihe in enumerate(welt):
        reihe_text = ""
        for x, zeichen in enumerate(reihe):
            # Ermittle die position des Spielers und zeichne diese.
            if y == spieler["y"] and x == spieler["x"]:
                reihe_text = reihe_text + spieler["zeichen"]
            else:
                reihe_text = reihe_text + zeichen
        rprint(reihe_text)

def spiel_starten():
    breite = 50
    hoehe = 20
    anzahl_boden_flaechen = int(breite * hoehe * 0.5)
    welt = generiere_welt(breite, hoehe, anzahl_boden_flaechen)
    spiel_beenden = False
    while not spiel_beenden:
        system(loeschte_terminal_inhalt)
        zeichne_welt(welt)

        # Werte Aktion aus...
        aktion = console.input("Deine Aktion: ")
        aktion = aktion.lower()
        if aktion == "w":
            spieler["y"] -= 1
        elif aktion == "a":
            spieler["x"] -= 1
        elif aktion == "s":
            spieler["y"] += 1
        elif aktion == "d": 
            spieler["x"] += 1
        elif aktion == "g":
            breite = 50
            hoehe = 20
            anzahl_boden_flaechen = int(breite * hoehe * 0.5)
            welt = generiere_welt(breite, hoehe, anzahl_boden_flaechen)
        
    
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