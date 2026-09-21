# get_partite.py
import json
import requests
from datetime import datetime

BASE_URL = "https://api.football-data.org/v4"

# League IDs su football-data.org
LEAGUES = {
    "Serie A": "SA",
    "Serie B": "SB",
    "Serie C": "SC",  # football-data.org ha solo Serie A e B nel piano free
}

def fetch_fixtures(league_code):
    """Recupera le prossime 10 partite di una lega."""
    url = f"{BASE_URL}/competitions/{league_code}/matches?status=SCHEDULED,FUTURE"
    try:
        resp = requests.get(url, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        return data.get("matches", [])
    except Exception as e:
        print(f"  Errore API: {e}")
        return []


def parse_match(match, competition_name):
    """Converte un match dell'API in formato partite."""
    utc_date = match.get("utcDate", "")
    if not utc_date:
        return None

    try:
        dt = datetime.fromisoformat(utc_date.replace("Z", "+00:00"))
        data_str = dt.strftime("%d/%m/%Y")
        ora_str = dt.strftime("%H:%M")
        data_ordinata = dt.strftime("%Y-%m-%d %H:%M")
    except Exception:
        return None

    home = match.get("homeTeam", {}).get("shortName", "")
    away = match.get("awayTeam", {}).get("shortName", "")
    score_home = match.get("score", {}).get("fullTime", {}).get("home", "")
    score_away = match.get("score", {}).get("fullTime", {}).get("away", "")
    
    # Se la partita non è ancora finita, il punteggio è None
    if score_home is not None and score_away is not None:
        score = f"{score_home}-{score_away}"
    else:
        score = ""

    return {
        "data": data_str,
        "ora": ora_str,
        "data_ordinata": data_ordinata,
        "competizione": competition_name,
        "casa": home,
        "ospite": away,
        "risultato": score,
    }


def main():
    all_matches = []

    for comp_name, league_code in LEAGUES.items():
        print(f"Recupero {comp_name} ...")
        fixtures = fetch_fixtures(league_code)
        print(f"  -> {len(fixtures)} partite trovate")

        for fix in fixtures:
            match = parse_match(fix, comp_name)
            if match:
                all_matches.append(match)

    # Ordina per data
    all_matches.sort(key=lambda m: m["data_ordinata"])

    # Rimuovi duplicati
    seen = set()
    unique_matches = []
    for m in all_matches:
        key = (m["casa"], m["ospite"], m["data_ordinata"])
        if key not in seen:
            seen.add(key)
            unique_matches.append(m)

    output_path = "docs/segnalazioni/partite.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(unique_matches, f, ensure_ascii=False, indent=2)

    print(f"\nScritte {len(unique_matches)} partite in {output_path}")


if __name__ == "__main__":
    main()

