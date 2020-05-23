from rich.console import Console
from rich.panel import Panel
from rich import print as rprint
from os import system, name

# Globale variablen
console = Console()
menu_text = "Wilkommen in Python Adventure!\n\n1: Spiel starten\n2: Spiel laden\n3: Highscore ansehen"
terminal_breite = console.size.width

# https://stackoverflow.com/questions/8907236/center-aligning-text-on-console-in-python
zentriere_text_ausdruck = '{:^' + str(terminal_breite) + '}'

#Auf Linux und Mac heisst der Befehl 'clear'
loeschte_terminal_inhalt = 'clear'

#Auf Windows heisst der Befehl 'cls'
if name == 'nt':
    loeschte_terminal_inhalt = 'cls'

welt = [
        ["#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#"],    
        ["#", "z", ".", ".", ".", ".", ".", ".", ".", ".", "#"],
        ["#", ".", ".", ".", ".", ".", ".", "m", ".", ".", "#"],    
        ["#", ".", ".", ".", ".", ".", ".", ".", ".", ".", "#"],    
        ["#", ".", ".", ".", "#", ".", ".", ".", ".", ".", "#"],    
        ["#", ".", ".", ".", ".", ".", ".", "m", ".", ".", "#"],    
        ["#", ".", ".", "#", ".", ".", ".", ".", ".", ".", "#"],    
        ["#", ".", ".", "#", ".", ".", ".", ".", ".", ".", "#"],    
        ["#", ".", ".", "#", ".", ".", ".", ".", ".", ".", "#"],
        ["#", ".", ".", ".", ".", "t", ".", ".", ".", ".", "#"],    
        ["#", ".", "t", ".", ".", ".", ".", ".", ".", ".", "#"],
        ["#", ".", ".", ".", ".", ".", ".", ".", ".", ".", "#"],
        ["#", ".", ".", ".", ".", ".", ".", ".", ".", ".", "#"],    
        ["#", ".", ".", ".", ".", ".", ".", ".", ".", ".", "#"],    
        ["#", ".", ".", ".", ".", ".", ".", ".", ".", ".", "#"],    
        ["#", ".", ".", ".", ".", ".", ".", ".", ".", ".", "#"],
        ["#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#"]
    ]

spieler = {
    "zeichen": ":snake:",
    "x": 5,
    "y": 12
}

# Diese Funktion zentriert einen Text
def zentriere_text(text):
    return zentriere_text_ausdruck.format(text)

def emoji_zeichen_fuer_welt(zeichen):
    if zeichen == "#":
        return ":brick:"
    elif zeichen == ".":
        return ":black_square_button:"
    elif zeichen == "z":
        return ":castle:"
    elif zeichen == "m":
        return ":dragon:"
    elif zeichen == "t":
        return ":sparkles:"
    return zeichen



def zeichne_welt():
    for y, reihe in enumerate(welt):
        reihe_text = ""
        for x, zeichen in enumerate(reihe):
            # Ermittle die position des Spielers und zeichne diese.
            if y == spieler["y"] and x == spieler["x"]:
                reihe_text = reihe_text + spieler["zeichen"]
            else:
                reihe_text = reihe_text + emoji_zeichen_fuer_welt(zeichen)
        rprint(reihe_text)

def werte_aktion_aus(aktion):
    if aktion == "w":
        spieler["y"] -= 1
    elif aktion == "a":
        spieler["x"] -= 1
    elif aktion == "s":
        spieler["y"] += 1
    elif aktion == "d": 
        spieler["x"] += 1

def spiel_starten():
    spiel_beenden = False
    while not spiel_beenden:
        system(loeschte_terminal_inhalt)
        zeichne_welt()

        # Werte Aktion aus...
        aktion = console.input("Deine Aktion: ")
        aktion = aktion.lower()
        werte_aktion_aus(aktion)
        
    
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