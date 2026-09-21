# get_partite.py
import json
import re
from datetime import datetime
from playwright.sync_api import sync_playwright

URLS = {
    "Serie A": "https://www.livesoccertv.com/it/competitions/italy/serie-a/",
    "Serie B": "https://www.livesoccertv.com/it/competitions/italy/serie-b/",
    "Serie C": "https://www.livesoccertv.com/it/competitions/italy/lega-pro-1/",
}


def parse_date_str(raw: str) -> str:
    """Normalizza una stringa tipo '21/09/2025' o '21/09/2025 20:45' in 'YYYY-MM-DD HH:MM'."""
    raw = raw.strip()
    # Prova con ora
    for fmt in ("%d/%m/%Y %H:%M", "%d/%m/%Y %H.%M", "%d/%m/%Y"):
        try:
            dt = datetime.strptime(raw, fmt)
            return dt.strftime("%Y-%m-%d %H:%M")
        except ValueError:
            continue
    return datetime.now().strftime("%Y-%m-%d %H:%M")


def extract_matches(page, competition_name: str) -> list[dict]:
    """Estrae le partite dalla pagina corrente."""
    partite = []

    # Cerca tutti i contenitori di match — proviamo più selettori
    match_containers = page.query_selector_all(
        "tr.match-row, tr[data-match], div.match, div.match-item, table tr"
    )

    if not match_containers:
        # Fallback: cerca pattern nel testo della pagina
        body_text = page.inner_text("body")
        partite = parse_from_text(body_text, competition_name)
        return partite

    for row in match_containers:
        try:
            # Data e ora — spesso in una cella con classe match-date o simile
            date_span = row.query_selector("span.match-date, span.date, td:first-child span")
            time_span = row.query_selector("span.match-time, span.time, td:first-child span.time")

            date_str = date_span.inner_text(strip=True) if date_span else ""
            time_str = time_span.inner_text(strip=True) if time_span else ""

            # Squadra casa (spesso la prima cella o un link)
            home_cell = row.query_selector("td:nth-child(2), .home-team, .team-home")
            home_team = home_cell.inner_text(strip=True).split("\n") if home_cell else ""

            # Squadra ospite
            away_cell = row.query_selector("td:nth-child(3), .away-team, .team-away")
            away_team = away_cell.inner_text(strip=True).split("\n") if away_cell else ""

            # Risultato
            score_cell = row.query_selector("td:nth-child(4), .score, .result")
            score = score_cell.inner_text(strip=True) if score_cell else ""

            # Pulisci i nomi delle squadre (togli spazi multipli)
            home_team = re.sub(r'\s+', ' ', home_team).strip()
            away_team = re.sub(r'\s+', ' ', away_team).strip()

            if not date_str or not home_team or not away_team:
                continue

            match_dt = parse_date_str(f"{date_str} {time_str}")

            partite.append({
                "data": date_str,
                "ora": time_str,
                "data_ordinata": match_dt,
                "competizione": competition_name,
                "casa": home_team,
                "ospite": away_team,
                "risultato": score,
            })
        except Exception:
            continue

    return partite


def parse_from_text(body_text: str, competition_name: str) -> list[dict]:
    """Fallback: cerca pattern tipo '21/09/2025 20:45  Milan - Inter 2-1' nel testo."""
    partite = []
    # Pattern: data ora  casa - ospite  risultato
    pattern = r"(\d{2}/\d{2}/\d{4}\s+\d{2}:\d{2})\s+(.+?)\s+-\s+(.+?)\s+(\d+-\d+)"
    for match in re.finditer(pattern, body_text):
        date_time_str, casa, ospite, risultato = match.groups()
        date_str, time_str = date_time_str.split(None, 1)
        match_dt = parse_date_str(date_time_str)
        partite.append({
            "data": date_str,
            "ora": time_str,
            "data_ordinata": match_dt,
            "competizione": competition_name,
            "casa": casa.strip(),
            "ospite": ospite.strip(),
            "risultato": risultato.strip(),
        })
    return partite


def main():
    all_matches = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
            locale="it-IT",
        )
        page = context.new_page()

        for comp_name, url in URLS.items():
            print(f"Recupero {comp_name} da {url} ...")
            try:
                page.goto(url, wait_until="domcontentloaded", timeout=30000)
                # Attendi che il contenuto si carichi
                page.wait_for_timeout(3000)
                partite = extract_matches(page, comp_name)
                all_matches.extend(partite)
                print(f"  -> {len(partite)} partite trovate")
            except Exception as e:
                print(f"  -> Errore: {e}")
            print()

        browser.close()

    # Ordina per data/ora
    all_matches.sort(key=lambda m: m["data_ordinata"])

    # Rimuovi duplicati
    seen = set()
    unique_matches = []
    for m in all_matches:
        key = (m["casa"], m["ospite"], m["data_ordinata"])
        if key not in seen:
            seen.add(key)
            unique_matches.append(m)

    output_path = "partite.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(unique_matches, f, ensure_ascii=False, indent=2)

    print(f"\nScritte {len(unique_matches)} partite in {output_path}")


if __name__ == "__main__":
    main()

