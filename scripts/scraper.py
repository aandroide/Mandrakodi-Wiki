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
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                locale="it-IT"
            )
            page = context.new_page()

            for target in targets:
                lega_nome = target["lega"]
                url = target["url"]
                print(f"Scraping {lega_nome} da {url}...")

                try:
                    page.goto(url, wait_until="domcontentloaded", timeout=40000)
                    page.wait_for_timeout(3000)

                    # Seleziona specificamente le tabelle o i container delle partite
                    matches = page.query_selector_all("tr.match-row, tr[id^='m_'], table.schedules tr")

                    for m in matches:
                        try:
                            # Estrai il testo e rimuovi spazi e a capo multipli
                            inner_text = m.inner_text().strip()
                            if not inner_text:
                                continue

                            # Pulisci le righe e filtra la spazzatura
                            righe = [r.strip() for r in inner_text.split("\n") if r.strip()]
                            testo_completo = " - ".join(righe)

                            # Filtri di esclusione per righe di intestazione / spazzatura
                            testo_lower = testo_completo.lower()
                            parole_da_scartare = [
                                "competizione", "fase", "canale", "trasmessa", 
                                "diritti tv", "prossime partite", "classifica", 
                                "risultati precedenti", "squadra", "ora/stato"
                            ]
                            
                            if any(p in testo_lower for p in parole_da_scartare):
                                continue

                            # Un match valido deve contenere un orario (es. 15:00) o un indicatore di stato
                            has_time = re.search(r'\b\d{1,2}:\d{2}\b', testo_completo)
                            is_live = False

                            # Controllo stato LIVE (tramite classi o testo)
                            html_row = m.inner_html().lower()
                            if "live" in html_row or "in diretta" in testo_lower or "′" in testo_completo:
                                is_live = True

                            # Se non ha né l'orario né è live, né un risultato tipico (es. 2 - 1), scarta
                            has_score = re.search(r'\b\d+\s*-\s*\d+\b', testo_completo)
                            if not (has_time or is_live or has_score):
                                continue

                            partite_trovate.append({
                                "lega": lega_nome,
                                "dettagli": testo_completo,
                                "is_live": is_live,
                                "url": url
                            })

                        except Exception:
                            continue

                except Exception as err_target:
                    print(f"Errore caricamento {lega_nome}: {err_target}")

            browser.close()

    except Exception as e:
        print(f"Errore generale durante lo scraping: {e}")

    data_to_save = {
        "ultimo_aggiornamento": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "partite": partite_trovate
    }
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data_to_save, f, ensure_ascii=False, indent=2)
        
    print(f"Salvate {len(partite_trovate)} partite pulite in: {output_path}")

if __name__ == "__main__":
    scarica_partite()
