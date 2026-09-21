import json
import os
import re
from datetime import datetime
from playwright.sync_api import sync_playwright

def scarica_partite():
    partite_trovate = []
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.abspath(os.path.join(script_dir, ".."))
    docs_dir = os.path.join(repo_root, "docs")
    
    os.makedirs(docs_dir, exist_ok=True)
    output_path = os.path.join(docs_dir, "partite.json")

    targets = [
        {"lega": "Italia - Serie A", "url": "https://www.livesoccertv.com/it/competitions/italy/serie-a/"},
        {"lega": "Italia - Serie B", "url": "https://www.livesoccertv.com/it/competitions/italy/serie-b/"},
        {"lega": "Italia - Serie C", "url": "https://www.livesoccertv.com/it/competitions/italy/lega-pro-1/"}
    ]

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            # Impostiamo fuso orario italiano fisso per Playwright
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

                    # Trova tutte le tabelle o i blocchi con le partite
                    rows = page.query_selector_all("tr")
                    
                    data_corrente = "Data non specificata"

                    for row in rows:
                        try:
                            text = row.inner_text().strip()
                            if not text:
                                continue

                            testo_lower = text.lower()

                            # Se la riga è un'intestazione di data (es. "Sabato, 19 Settembre 2026")
                            if any(giorno in testo_lower for giorno in ["lunedì", "martedì", "mercoledì", "giovedì", "venerdì", "sabato", "domenica"]):
                                data_corrente = text.split("\n")[0].strip()
                                continue

                            # Cerca l'orario (formato HH:MM)
                            time_match = re.search(r'\b(\d{1,2}:\d{2})\b', text)
                            if not time_match:
                                continue

                            orario_str = time_match.group(1)

                            # Pulizia delle righe
                            righe = [r.strip() for r in text.split("\n") if r.strip()]
                            testo_completo = " - ".join(righe)

                            # Rimuove prefissi inutili e stato della gara
                            testo_pulito = re.sub(r'^(FIN|Live)\s*-\s*\+\s*-\s*', '', testo_completo, flags=re.IGNORECASE)
                            testo_pulito = re.sub(r'^(FIN|Live)\s*-\s*', '', testo_pulito, flags=re.IGNORECASE)
                            testo_pulito = re.sub(r'\s*-\s*Disponibile on-demand', '', testo_pulito, flags=re.IGNORECASE)

                            partite_trovate.append({
                                "lega": lega_nome,
                                "data": data_corrente,
                                "orario": orario_str,
                                "dettagli": f"[{data_corrente}] {testo_pulito}",
                                "url": url
                            })

                        except Exception:
                            continue

                except Exception as err_target:
                    print(f"Errore caricamento {lega_nome}: {err_target}")

            browser.close()

    except Exception as e:
        print(f"Errore generale durante lo scraping: {e}")

    # Ordina prima per data e poi per orario
    partite_trovate.sort(key=lambda x: (x["data"], x["orario"]))

    data_to_save = {
        "ultimo_aggiornamento": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "partite": partite_trovate
    }
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data_to_save, f, ensure_ascii=False, indent=2)
        
    print(f"Salvate {len(partite_trovate)} partite con data e orario in: {output_path}")

if __name__ == "__main__":
    scarica_partite()
