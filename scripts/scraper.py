import json
import os
import re
from datetime import datetime
import zoneinfo
from playwright.sync_api import sync_playwright

def scarica_partite():
    partite_trovate = []
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.abspath(os.path.join(script_dir, ".."))
    docs_dir = os.path.join(repo_root, "docs")
    
    os.makedirs(docs_dir, exist_ok=True)
    output_path = os.path.join(docs_dir, "partite.json")

    tz_roma = zoneinfo.ZoneInfo("Europe/Rome")

    targets = [
        {"lega": "Italia - Serie A", "url": "https://www.livesoccertv.com/it/competitions/italy/serie-a/"},
        {"lega": "Italia - Serie B", "url": "https://www.livesoccertv.com/it/competitions/italy/serie-b/"},
        {"lega": "Italia - Serie C", "url": "https://www.livesoccertv.com/it/competitions/italy/lega-pro-1/"}
    ]

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                locale="it-IT",
                timezone_id="Europe/Rome"
            )
            page = context.new_page()

            for target in targets:
                lega_nome = target["lega"]
                url = target["url"]
                print(f"Scraping {lega_nome} da {url}...")

                try:
                    page.goto(url, wait_until="domcontentloaded", timeout=40000)
                    page.wait_for_timeout(3000)

                    # Seleziona tutti gli elementi della pagina (date e righe partite)
                    elements = page.query_selector_all("th.date, tr.match-row, tr[id^='m_'], .schedules_table tr")

                    data_corrente = "Data non specificata"

                    for el in elements:
                        try:
                            # Se è un'intestazione di data (th o td di tipo date)
                            tag_name = el.evaluate("el => el.tagName.toLowerCase()")
                            class_attr = el.get_attribute("class") or ""

                            if tag_name == "th" or "date" in class_attr.lower():
                                text_date = el.inner_text().strip()
                                if text_date:
                                    data_corrente = text_date.split("\n")[0].strip()
                                continue

                            text = el.inner_text().strip()
                            if not text:
                                continue

                            # Controlla se c'è un timestamp UTC nativo nell'HTML (data-start o data-time)
                            timestamp_attr = el.get_attribute("data-start") or el.get_attribute("data-time")
                            orario_roma = None
                            dt_evento = None

                            if timestamp_attr and timestamp_attr.isdigit():
                                ts = int(timestamp_attr)
                                # Se il timestamp è in millisecondi
                                if ts > 1e11:
                                    ts /= 1000
                                dt_utc = datetime.fromtimestamp(ts, tz=zoneinfo.ZoneInfo("UTC"))
                                dt_evento = dt_utc.astimezone(tz_roma)
                                orario_roma = dt_evento.strftime("%H:%M")
                                data_corrente = dt_evento.strftime("%d/%m/%Y")

                            # Se non c'è timestamp, estrai l'orario del testo come ripiego
                            if not orario_roma:
                                time_match = re.search(r'\b(\d{1,2}:\d{2})\b', text)
                                if not time_match:
                                    continue
                                orario_roma = time_match.group(1)

                            # Pulizia del testo della partita
                            righe = [r.strip() for r in text.split("\n") if r.strip()]
                            testo_completo = " - ".join(righe)

                            # Rimuovi diciture di stato e prefissi parassiti
                            testo_pulito = re.sub(r'^(FIN|Live)\s*-\s*\+\s*-\s*', '', testo_completo, flags=re.IGNORECASE)
                            testo_pulito = re.sub(r'^(FIN|Live)\s*-\s*', '', testo_pulito, flags=re.IGNORECASE)
                            testo_pulito = re.sub(r'\s*-\s*Disponibile on-demand', '', testo_pulito, flags=re.IGNORECASE)

                            # Creiamo una chiave per l'ordinamento (datetime se disponibile, altrimenti testo)
                            sort_key = dt_evento.timestamp() if dt_evento else 0

                            partite_trovate.append({
                                "lega": lega_nome,
                                "data": data_corrente,
                                "orario": orario_roma,
                                "dettagli": f"[{data_corrente} ore {orario_roma}] {testo_pulito}",
                                "sort_key": sort_key,
                                "url": url
                            })

                        except Exception:
                            continue

                except Exception as err_target:
                    print(f"Errore caricamento {lega_nome}: {err_target}")

            browser.close()

    except Exception as e:
        print(f"Errore generale durante lo scraping: {e}")

    # Ordina cronologicamente in base alla data/ora reale dell'evento
    partite_trovate.sort(key=lambda x: (x["sort_key"], x["data"], x["orario"]))

    # Rimuovi la chiave temporanea prima di salvare il JSON
    for p_item in partite_trovate:
        p_item.pop("sort_key", None)

    data_to_save = {
        "ultimo_aggiornamento": datetime.now(tz_roma).strftime("%d/%m/%Y %H:%M:%S"),
        "partite": partite_trovate
    }
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data_to_save, f, ensure_ascii=False, indent=2)
        
    print(f"Salvate {len(partite_trovate)} partite ordinate in: {output_path}")

if __name__ == "__main__":
    scarica_partite()
