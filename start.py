from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import print as rprint
from os import system, name
import random
import json

# Globale variablen
console = Console()
menu_text = "Wilkommen in Python Adventure!\n\n1: Spiel starten\n2: Highscore ansehen"
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

breite = 50
hoehe = 15
anzahl_aufnehmbare_leben = 5

spiel_beenden = False


# Diese Funktion zentriert einen Text
def zentriere_text(text):
    return zentriere_text_ausdruck.format(text)


def lade_daten_aus_json (pfad, standard_wert = []):
    #https://www.programiz.com/python-programming/json
    try:
        with open(pfad, 'r') as datei:
            return json.load(datei)
    except Exception:
        return standard_wert

def schreibe_daten_in_json(pfad, daten):
    #https://stackoverflow.com/questions/17043860/how-to-dump-a-dict-to-a-json-file
    with open(pfad, 'w') as datei:
        json.dump(daten, datei, indent = 4)

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


def generiere_welt(spieler, anzahl_boden_flaechen, anzahl_monster):
    print("Volle Welt wird generiert...")
    welt = generiere_volle_welt()
    print("Bodenflächen werden platziert...")
    welt = platziere_boden_flaechen(welt, anzahl_boden_flaechen)
    print("Aufnehmbare Leben werden platziert...")
    welt = platziere_aufnehmbare_leben(welt)
    print("Ziel wird platziert")
    welt = platziere_ziel(welt)
    print("Platziere monster...")
    welt, monster = platziere_monster(anzahl_monster, welt)

    # Platziere Spieler
    print("Platziere Spieler...")
    spieler["x"], spieler["y"] = platziere_spieler(welt)
    print("Welt ist fertig generiert...")
    return (spieler, welt, monster)


def zeichne_welt(welt, monster, spieler):
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

def bewege_spieler(aktion, spieler, welt, monster):
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


def bewege_monster(monster, welt, spieler):
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


def zeichne_leben(spieler):
    lebens_anzeige = "Leben Spieler: [bold red]"
    for i in range(spieler["leben"]):
        lebens_anzeige = lebens_anzeige + symbol_leben + " "
    lebens_anzeige = lebens_anzeige + "[/bold red]"
    return lebens_anzeige

def zeichne_spieler_informationen(spieler):
    spieler_informationen = ""

    # Zeichne das Leben des Spielers
    spieler_informationen = spieler_informationen + zeichne_leben(spieler)
    
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

def generiere_welt_fuer_spieler(spieler):
    if spieler["momentanes_level"] == 0:
        anzahl_boden_flaechen = int(breite * hoehe * 0.45)
        anzahl_monster = 10
        return generiere_welt(spieler, anzahl_boden_flaechen, anzahl_monster)
    elif spieler["momentanes_level"] == 1:
        anzahl_boden_flaechen = int(breite * hoehe * 0.85)
        anzahl_monster = 8
        return generiere_welt(spieler, anzahl_boden_flaechen, anzahl_monster)
    else:
        return None

def zeige_alle_levels_geschafft_meldung():
    rprint(Panel(zentriere_text("Du hast alle Levels die verfügbar sind gemeister, toll gemacht!!")))

def zeige_gestorben_meldung():
    rprint(Panel(zentriere_text("Leider hast du verloren, versuch doch dein Glück erneut!!")))

def highscore_speicher(spieler, highscores):
    # Prüfe ob für dieses Level bereist Schritte gemacht wurden.
    eintrag_bereits_vorhanden = False
    for highscore in highscores:
        # Es gibt bereits einen Eintrag für dieses Level, füge einfach einen neuen Eintrag
        # für die Anzahl Schritte hinzu...
        if highscore["level"] == spieler["momentanes_level"]:
            highscore["anzahl_schritte"].append(spieler["anzahl_schritte"])
            eintrag_bereits_vorhanden = True

    # Für dieses Level gibt es noch keine Einträge, erstelle einen neuen
    if not eintrag_bereits_vorhanden:
        highscores.append({
            "level": spieler["momentanes_level"],
            "anzahl_schritte": [spieler["anzahl_schritte"]]
        })

    # Schreibe die Highscore Daten in die Datei
    schreibe_daten_in_json("highscore.json", highscores)
    return highscores

def spiel_starten():
    spieler = {
        "zeichen": symbol_spieler,
        "x": 5,
        "y": 12,
        "leben" : 3,
        "anzahl_schritte": 0,
        "momentanes_level": 0
    }

    # Lade alle Daten aus der Highscore Datei
    highscores = lade_daten_aus_json("highscore.json")


    alle_level_gemeister = False
    gestorben = False

    if generiere_welt_fuer_spieler(spieler) == None:
        alle_level_gemeister = True
    else:
        spieler, welt, monster = generiere_welt_fuer_spieler(spieler)


    while not gestorben and not alle_level_gemeister:
        system(loeschte_terminal_inhalt)
        zeichne_welt(welt, monster, spieler)
        zeichne_spieler_informationen(spieler)

        # Werte Aktion aus...
        aktion = console.input("Deine Aktion: ")
        aktion = aktion.lower()

        # Prüfe ob die Hilfe angezeigt werden soll...
        if aktion == "h":
            zeige_hilfe_an()
        
        bewege_spieler(aktion, spieler, welt, monster)

        # Prüfe ob sich der Spieler bereits beim Schloss befindet...
        if symbol_in_welt(spieler["x"], spieler["y"], welt) == symbol_ziel:         

            highscores = highscore_speicher(spieler, highscores)

            # Der Spieler hat das nächste Level erreicht
            spieler["momentanes_level"] += 1

            # Initialisiere die Schritte für das nächste Level
            spieler["anzahl_schritte"] = 0

            # Prüfe ob der Spieler alle Level gemeistert hat
            if generiere_welt_fuer_spieler(spieler) == None:
                alle_level_gemeister = True
            else:
                # Generiere eine neue Welt mit Monstern etc.
                spieler, welt, monster = generiere_welt_fuer_spieler(spieler)

        bewege_monster(monster, welt, spieler)

        # Prüfe ob das Spiel beendet ist -> Der Spieler hat keine Leben mehr
        gestorben = spieler["leben"] <= 0

    # Prüfe den Grund für das Beenden des Levels und zeige eine entsprechende Meldung an:
    # a) Der Spieler hat alle Levels gemeister
    # b) Der Spieler ist gestorben
    if alle_level_gemeister:
        zeige_alle_levels_geschafft_meldung()
    elif gestorben:
        zeige_gestorben_meldung()

    start()

def highscore_anzeigen():
    # Lade alle Daten für den Highscore
    highscores = lade_daten_aus_json("highscore.json")
    # https://rich.readthedocs.io/en/latest/tables.html
    highscore_table = Table(title="Highscore")

    # Füge die relevanten Spalten der Tabelle hinzu...
    highscore_table.add_column("Level", justify="left")
    highscore_table.add_column("Anzahl Schritte", justify="right")

    for highscore in highscores:
        level = highscore["level"]
        anzahl_schritte_liste = highscore["anzahl_schritte"]
        for schritte in anzahl_schritte_liste:
            highscore_table.add_row("Level " + str(level + 1), str(schritte))

    beenden = False
    while not beenden:
        system(loeschte_terminal_inhalt)
        console.print(highscore_table)
        beenden = input("Drücke 'q' um zum Hauptmenü zurückzukehren: ").lower() == 'q'

def start():
    # Zeige Hauptmenu an
    rprint(Panel(zentriere_text(menu_text), style="#F08080"))

    # Werte die Auswahl für das Hauptmenü aus...
    auswahl = ""
    gueltige_eingabe = False
    while not gueltige_eingabe:
        auswahl = console.input("Bitte triff eine Auswahl: ")
        gueltige_eingabe = auswahl == "1" or auswahl == "2"

    if auswahl == "1":
        zeige_hilfe_an()
        spiel_starten()
    elif auswahl == "2":
        highscore_anzeigen()
        start()

start()