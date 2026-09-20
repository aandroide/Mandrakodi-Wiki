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

    # URL unico del palinsesto di OGGI
    url_oggi = "https://www.livesoccertv.com/it/schedules/"

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                locale="it-IT"
            )
            page = context.new_page()

            print(f"Scraping palinsesto odierno da {url_oggi}...")
            page.goto(url_oggi, wait_until="domcontentloaded", timeout=40000)
            page.wait_for_timeout(4000)

            # Cerca tutte le righe del palinsesto odierno
            rows = page.query_selector_all("tr")

            for row in rows:
                try:
                    text = row.inner_text().strip()
                    if not text:
                        continue

                    # Identifica la lega di appartenenza
                    lega_trovata = None
                    if "Serie A" in text:
                        lega_trovata = "Italia - Serie A"
                    elif "Serie B" in text:
                        lega_trovata = "Italia - Serie B"
                    elif "Serie C" in text or "Lega Pro" in text:
                        lega_trovata = "Italia - Serie C"

                    # Se la riga appartiene a una delle 3 leghe target
                    if lega_trovata:
                        righe = [r.strip() for r in text.split("\n") if r.strip()]
                        testo_completo = " - ".join(righe)

                        # Salva solo se è presente un orario
                        if re.search(r'\b\d{1,2}:\d{2}\b', testo_completo):
                            # Pulizia da diciture superflue
                            testo_pulito = re.sub(r'\s*-\s*Disponibile on-demand', '', testo_completo, flags=re.IGNORECASE)

                            partite_trovate.append({
                                "lega": lega_trovata,
                                "dettagli": testo_pulito,
                                "url": url_oggi
                            })

                except Exception:
                    continue

            browser.close()

    except Exception as e:
        print(f"Errore generale durante lo scraping: {e}")

    data_to_save = {
        "ultimo_aggiornamento": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "partite": partite_trovate
    }
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data_to_save, f, ensure_ascii=False, indent=2)
        
    print(f"Salvate {len(partite_trovate)} partite di oggi in: {output_path}")

if __name__ == "__main__":
    scarica_partite()
