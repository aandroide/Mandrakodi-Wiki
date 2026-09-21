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
                print(f"Scraping completo di {lega_nome} da {url}...")

                try:
                    page.goto(url, wait_until="networkidle", timeout=60000)
                    
                    # Forzare lo scroll in fondo alla pagina per caricare tutti gli eventi pigri/lazy-loaded
                    for _ in range(5):
                        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                        page.wait_for_timeout(1000)

                    # Seleziona tutte le righe di tabella e intestazioni
                    rows = page.query_selector_all("tr, th")

                    data_corrente = "Data non definita"

                    for row in rows:
                        try:
                            text = row.inner_text().strip()
                            if not text:
                                continue

                            testo_lower = text.lower()

                            # Individua le intestazioni di data
                            if any(giorno in testo_lower for giorno in ["lunedì", "martedì", "mercoledì", "giovedì", "venerdì", "sabato", "domenica"]):
                                # Prendi solo la prima riga del testo per evitare residui
                                data_corrente = text.split("\n")[0].strip()
                                continue

                            # Cerca l'orario (es. 15:00, 18:45, 20:45)
                            time_match = re.search(r'\b(\d{1,2}:\d{2})\b', text)
                            if not time_match:
                                continue

                            orario_str = time_match.group(1)

                            # Estrai timestamp Unix se disponibile per la massima precisione oraria
                            timestamp_attr = row.get_attribute("data-start") or row.get_attribute("data-time")
                            dt_sort = 0
                            if timestamp_attr and timestamp_attr.isdigit():
                                ts = int(timestamp_attr)
                                if ts > 1e11:
                                    ts /= 1000
                                dt_utc = datetime.fromtimestamp(ts, tz=zoneinfo.ZoneInfo("UTC"))
                                dt_roma = dt_utc.astimezone(tz_roma)
                                orario_str = dt_roma.strftime("%H:%M")
                                dt_sort = dt_roma.timestamp()

                            # Pulizia testo della partita
                            righe = [r.strip() for r in text.split("\n") if r.strip()]
                            testo_completo = " - ".join(righe)

                            # Rimuovi diciture di stato
                            testo_pulito = re.sub(r'^(FIN|Live)\s*-\s*\+\s*-\s*', '', testo_completo, flags=re.IGNORECASE)
                            testo_pulito = re.sub(r'^(FIN|Live)\s*-\s*', '', testo_pulito, flags=re.IGNORECASE)
                            testo_pulito = re.sub(r'\s*-\s*Disponibile on-demand', '', testo_pulito, flags=re.IGNORECASE)

                            partite_trovate.append({
                                "lega": lega_nome,
                                "data": data_corrente,
                                "orario": orario_str,
                                "dettagli": f"[{data_corrente} - {orario_str}] {testo_pulito}",
                                "dt_sort": dt_sort,
                                "url": url
                            })

                        except Exception:
                            continue

                except Exception as err_target:
                    print(f"Errore caricamento {lega_nome}: {err_target}")

            browser.close()

    except Exception as e:
        print(f"Errore generale durante lo scraping: {e}")

    # Ordina rigorosamente per data/ora
    partite_trovate.sort(key=lambda x: (x["dt_sort"], x["data"], x["orario"]))

    # Pulizia chiave temporanea
    for p_item in partite_trovate:
        p_item.pop("dt_sort", None)

    data_to_save = {
        "ultimo_aggiornamento": datetime.now(tz_roma).strftime("%d/%m/%Y %H:%M:%S"),
        "partite": partite_trovate
    }
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data_to_save, f, ensure_ascii=False, indent=2)
        
    print(f"Estratti complessivamente {len(partite_trovate)} eventi in: {output_path}")

if __name__ == "__main__":
    scarica_partite()
