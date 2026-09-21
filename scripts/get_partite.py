# get_partite.py
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

URLS = {
    "Serie A": "https://www.livesoccertv.com/it/competitions/italy/serie-a/",
    "Serie B": "https://www.livesoccertv.com/it/competitions/italy/serie-b/",
    "Serie C": "https://www.livesoccertv.com/it/competitions/italy/lega-pro-1/",
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

def parse_match_row(row):
    """Estrae data, ora, squadra casa, squadra ospite e risultato da una riga."""
    cells = row.find_all("td")
    if len(cells) < 4:
        return None

    # Data e ora — adatta il selettore in base alla struttura reale
    date_cell = cells.find("span", class_="match-date") or cells
    time_cell = cells.find("span", class_="match-time") or cells

    date_str = date_cell.get_text(strip=True) if date_cell else ""
    time_str = time_cell.get_text(strip=True) if time_cell else ""

    # Squadre
    home_cell = cells
    away_cell = cells
    home_team = home_cell.get_text(strip=True).split("\n") if home_cell else ""
    away_team = away_cell.get_text(strip=True).split("\n") if away_cell else ""

    # Risultato (opzionale)
    score_cell = cells
    score = score_cell.get_text(strip=True) if score_cell else ""

    if not date_str or not home_team or not away_team:
        return None

    # Combina data e ora
    match_datetime_str = f"{date_str} {time_str}".strip()
    try:
        match_dt = datetime.strptime(match_datetime_str, "%d/%m/%Y %H:%M")
    except ValueError:
        try:
            match_dt = datetime.strptime(match_datetime_str, "%d/%m/%Y")
        except ValueError:
            match_dt = datetime.now()

    return {
        "data": date_str,
        "ora": time_str,
        "data_ordinata": match_dt.strftime("%Y-%m-%d %H:%M"),
        "competizione": None,  # riempito dopo
        "casa": home_team,
        "ospite": away_team,
        "risultato": score,
    }


def fetch_competition(url, competition_name):
    """Scarica la pagina e restituisce la lista delle partite."""
    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)
        resp.raise_for_status()
    except requests.RequestException as e:
        print(f"Errore nel download di {url}: {e}")
        return []

    soup = BeautifulSoup(resp.text, "html.parser")
    partite = []

    # Adatta il selettore: cerca tutte le righe delle partite
    # LivesoccerTV usa spesso <tr class="match-row"> o <div class="match">
    rows = soup.select("tr.match-row, tr[data-match], .match-row, .match")
    if not rows:
        # Fallback: prova a prendere tutte le righe di tabella
        rows = soup.select("table tr")

    for row in rows:
        match = parse_match_row(row)
        if match:
            match["competizione"] = competition_name
            partite.append(match)

    return partite


def main():
    all_matches = []

    for comp_name, url in URLS.items():
        print(f"Recupero {comp_name} da {url} ...")
        partite = fetch_competition(url, comp_name)
        all_matches.extend(partite)
        print(f"  -> {len(partite)} partite trovate")

    # Ordina per data/ora
    all_matches.sort(key=lambda m: m["data_ordinata"])

    # Rimuovi duplicati (stessa casa, ospite, data)
    seen = set()
    unique_matches = []
    for m in all_matches:
        key = (m["casa"], m["ospite"], m["data_ordinata"])
        if key not in seen:
            seen.add(key)
            unique_matches.append(m)

    # Scrivi il file JSON
    output_path = "partite.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(unique_matches, f, ensure_ascii=False, indent=2)

    print(f"\nScritte {len(unique_matches)} partite in {output_path}")


if __name__ == "__main__":
    main()

