#!/usr/bin/env python3

import json
import re
from datetime import datetime
from pathlib import Path

import requests
from bs4 import BeautifulSoup


URLS = {
    "Serie A": "https://www.livesoccertv.com/it/competitions/italy/serie-a/",
    "Serie B": "https://www.livesoccertv.com/it/competitions/italy/serie-b/",
    "Serie C": "https://www.livesoccertv.com/it/competitions/italy/lega-pro-1/",
}

OUTPUT_FILE = Path("partite.json")

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/131.0 Safari/537.36"
    ),
}

MONTHS = {
    "gennaio": 1,
    "febbraio": 2,
    "marzo": 3,
    "aprile": 4,
    "maggio": 5,
    "giugno": 6,
    "luglio": 7,
    "agosto": 8,
    "settembre": 9,
    "ottobre": 10,
    "novembre": 11,
    "dicembre": 12,
}


def normalize_text(value):
    """Normalizza gli spazi."""
    if not value:
        return ""

    return re.sub(r"\s+", " ", value).strip()


def parse_date(text, current_year=None):
    """
    Cerca una data italiana del tipo:
    'Sabato, 19 Settembre'
    'Domenica, 20 Settembre 2026'
    """

    text = normalize_text(text)

    pattern = re.compile(
        r"(?:lunedì|lunedi|martedì|martedi|mercoledì|mercoledi|"
        r"giovedì|giovedi|venerdì|venerdi|sabato|domenica)?"
        r"[\s,]*"
        r"(\d{1,2})\s+"
        r"(gennaio|febbraio|marzo|aprile|maggio|giugno|luglio|"
        r"agosto|settembre|ottobre|novembre|dicembre)"
        r"(?:\s+(\d{4}))?",
        re.IGNORECASE,
    )

    match = pattern.search(text)

    if not match:
        return None

    day = int(match.group(1))
    month_name = match.group(2).lower()
    year = match.group(3)

    if year:
        year = int(year)
    elif current_year:
        year = current_year
    else:
        year = datetime.now().year

    month = MONTHS[month_name]

    return datetime(year, month, day).date()


def parse_time(text):
    """
    Cerca un orario tipo:
    20:45
    14:30
    """

    match = re.search(r"\b([01]?\d|2[0-3]):([0-5]\d)\b", text)

    if not match:
        return None

    return f"{int(match.group(1)):02d}:{match.group(2)}"


def find_match_text(element):
    """
    Cerca il testo utile dell'elemento partita.
    """

    text = normalize_text(element.get_text(" ", strip=True))

    # Rimuove alcuni elementi informativi che non fanno parte
    # dell'identificazione della partita.
    text = re.sub(r"\bLive\+\b", "", text, flags=re.IGNORECASE)
    text = normalize_text(text)

    return text


def parse_match(text, competition, match_date):
    """
    Estrae:
      - ora
      - squadra casa
      - squadra ospite
    """

    time = parse_time(text)

    if not time:
        return None

    # Rimuoviamo l'orario e le informazioni Live/FT.
    remaining = re.sub(
        r"\b([01]?\d|2[0-3]):([0-5]\d)\b",
        "",
        text,
        count=1,
    )

    remaining = re.sub(
        r"\bLive\+\b",
        "",
        remaining,
        flags=re.IGNORECASE,
    )

    # Risultati tipo:
    # Venezia 0 - 2 Lazio
    # Juventus 1 - 0 Atalanta
    # Milan - Lecce
    #
    # Per le partite non ancora iniziate ci interessa principalmente
    # il separatore " - ".

    remaining = re.sub(
        r"\bFT\b",
        "",
        remaining,
        flags=re.IGNORECASE,
    )

    remaining = normalize_text(remaining)

    match = re.search(
        r"(.+?)\s+-\s+(.+)$",
        remaining,
    )

    if not match:
        return None

    home = normalize_text(match.group(1))
    away = normalize_text(match.group(2))

    # Elimina eventuali informazioni che possono precedere
    # il nome della squadra.
    home = re.sub(r"^\d+'\s*", "", home)
    home = re.sub(r"^\d+\s*", "", home)

    if not home or not away:
        return None

    # Evita falsi positivi evidenti.
    if len(home) > 80 or len(away) > 80:
        return None

    return {
        "competizione": competition,
        "data": match_date.isoformat(),
        "ora": time,
        "casa": home,
        "trasferta": away,
    }


def extract_competition(competition, url):
    print(f"Scarico {competition}: {url}")

    response = requests.get(
        url,
        headers=HEADERS,
        timeout=30,
    )

    response.raise_for_status()

    soup = BeautifulSoup(
        response.text,
        "html.parser",
    )

    # Testo completo della pagina.
    page_text = normalize_text(soup.get_text(" ", strip=True))

    # Cerchiamo l'anno della stagione.
    season_match = re.search(
        r"Stagione\s+(\d{4})-(\d{4})",
        page_text,
        flags=re.IGNORECASE,
    )

    if season_match:
        current_year = int(season_match.group(1))
    else:
        current_year = datetime.now().year

    matches = []

    current_date = None

    # LiveSoccerTV utilizza diversi elementi HTML a seconda
    # della versione della pagina. Per questo motivo analizziamo
    # il testo dei contenitori in maniera relativamente generica.

    elements = soup.find_all(
        ["h1", "h2", "h3", "h4", "div", "li", "tr"]
    )

    seen = set()

    for element in elements:
        text = find_match_text(element)

        if not text:
            continue

        # Se troviamo una data, diventa la data corrente.
        detected_date = parse_date(
            text,
            current_year=current_year,
        )

        if detected_date:
            current_date = detected_date

        # Senza una data non possiamo associare correttamente
        # la partita.
        if not current_date:
            continue

        # Deve esserci un orario.
        if not parse_time(text):
            continue

        parsed = parse_match(
            text,
            competition,
            current_date,
        )

        if not parsed:
            continue

        key = (
            parsed["competizione"],
            parsed["data"],
            parsed["ora"],
            parsed["casa"],
            parsed["trasferta"],
        )

        if key in seen:
            continue

        seen.add(key)
        matches.append(parsed)

    return matches


def sort_matches(matches):
    return sorted(
        matches,
        key=lambda x: (
            x["data"],
            x["ora"],
            x["competizione"],
            x["casa"],
            x["trasferta"],
        ),
    )


def main():
    all_matches = []

    for competition, url in URLS.items():
        try:
            matches = extract_competition(
                competition,
                url,
            )

            print(
                f"{competition}: "
                f"{len(matches)} partite trovate"
            )

            all_matches.extend(matches)

        except Exception as exc:
            print(
                f"ERRORE durante l'elaborazione di "
                f"{competition}: {exc}"
            )

    all_matches = sort_matches(all_matches)

    data = {
        "aggiornato": datetime.now().astimezone().isoformat(),
        "partite": all_matches,
    }

    OUTPUT_FILE.write_text(
        json.dumps(
            data,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    print(
        f"\nCreato {OUTPUT_FILE} "
        f"con {len(all_matches)} partite."
    )


if __name__ == "__main__":
    main()

