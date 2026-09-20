import json
import os
import sys
from playwright.sync_api import sync_playwright

def scarica_partite():
    partite_trovate = []
    
    # Determina la radice del repository (risale di un livello se lo script è in scripts/)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.abspath(os.path.join(script_dir, ".."))
    docs_dir = os.path.join(repo_root, "docs")
    
    os.makedirs(docs_dir, exist_ok=True)
    output_path = os.path.join(docs_dir, "partite.json")

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )
            page = context.new_page()

            url = "https://www.livesoccertv.com/it/schedules/"
            print(f"Connecting to {url}...")
            page.goto(url, wait_until="domcontentloaded", timeout=60000)
            page.wait_for_timeout(3000)

            # Estrazione sicura
            elements = page.query_selector_all("tr, div")
            for el in elements:
                try:
                    txt = el.inner_text().strip()
                    if any(k in txt for k in ["Serie A", "Serie B", "Coppa Italia"]) and len(txt) < 300:
                        partite_trovate.append({"raw_data": txt.replace("\n", " - ")})
                except Exception:
                    continue

            browser.close()
    except Exception as e:
        print(f"Errore durante lo scraping: {e}")

    # Salva comunque un JSON valido per evitare errori 404
    data_to_save = {
        "partite": partite_trovate
    }
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data_to_save, f, ensure_ascii=False, indent=2)
        
    print(f"File salvato con successo in: {output_path}")

if __name__ == "__main__":
    scarica_partite()
