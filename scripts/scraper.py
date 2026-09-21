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

                    # Seleziona le righe della tabella palinsesto (stesso selettore di prima)
                    rows = page.query_selector_all("tr.match-row, tr[id^='m_'], table.schedules tr")

                    for row in rows:
                        try:
                            text = row.inner_text().strip()
                            if not text:
                                continue

                            # Cerca l'orario nel testo della riga (es. 15:00, 18:45, 20:45)
                            time_match = re.search(r'\b(\d{1,2}:\d{2})\b', text)
                            if not time_match:
                                continue

                            orario_str = time_match.group(1)

                            # Pulizia e formattazione testo
                            righe = [r.strip() for r in text.split("\n") if r.strip()]
                            testo_completo = " - ".join(righe)
                            
                            # Rimuove prefissi 'FIN', 'Live' e la scritta 'Disponibile on-demand'
                            testo_pulito = re.sub(r'^(FIN|Live)\s*-\s*\+\s*-\s*', '', testo_completo, flags=re.IGNORECASE)
                            testo_pulito = re.sub(r'^(FIN|Live)\s*-\s*', '', testo_pulito, flags=re.IGNORECASE)
                            testo_pulito = re.sub(r'\s*-\s*Disponibile on-demand', '', testo_pulito, flags=re.IGNORECASE)

                            partite_trovate.append({
                                "lega": lega_nome,
                                "orario": orario_str,
                                "dettagli": testo_pulito,
                                "url": url
                            })

                        except Exception:
                            continue

                except Exception as err_target:
                    print(f"Errore caricamento {lega_nome}: {err_target}")

            browser.close()

    except Exception as e:
        print(f"Errore generale durante lo scraping: {e}")

    # Ordina le partite trovate in ordine cronologico di orario
    partite_trovate.sort(key=lambda x: x["orario"])

    data_to_save = {
        "ultimo_aggiornamento": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "partite": partite_trovate
    }
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data_to_save, f, ensure_ascii=False, indent=2)
        
    print(f"Salvate {len(partite_trovate)} partite in: {output_path}")

if __name__ == "__main__":
    scarica_partite()
