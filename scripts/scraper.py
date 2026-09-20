import json
import os
import sys
from playwright.sync_api import sync_playwright

def scarica_partite():
    partite_trovate = []
    
    # Determina la cartella docs/ rispetto alla posizione dello script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.abspath(os.path.join(script_dir, ".."))
    docs_dir = os.path.join(repo_root, "docs")
    
    os.makedirs(docs_dir, exist_ok=True)
    output_path = os.path.join(docs_dir, "partite.json")

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                locale="it-IT"
            )
            page = context.new_page()

            # Pagina palinsesto programmazione
            url = "https://www.livesoccertv.com/it/schedules/"
            print(f"Connecting to {url}...")
            page.goto(url, wait_until="domcontentloaded", timeout=60000)
            
            # Attendi il caricamento completo del palinsesto
            page.wait_for_timeout(4000)

            # Cerca tutte le righe di partite presenti nel palinsesto
            rows = page.query_selector_all("tr")

            for row in rows:
                try:
                    text = row.inner_text().strip()
                    if not text:
                        continue

                    # Parole chiave per intercettare gli eventi inerenti l'Italia / campionati italiani
                    keywords = [
                        "Serie A", "Serie B", "Serie C", "Coppa Italia", 
                        "Supercoppa", "Italia", "Italian"
                    ]

                    if any(k.lower() in text.lower() for k in keywords):
                        # Pulisci e formatta il testo eliminando troppi a capo consecutivi
                        righe_pulite = [r.strip() for r in text.split("\n") if r.strip()]
                        testo_formattato = " - ".join(righe_pulite)
                        
                        # Evita duplicati o blocchi di testo troppo lunghi
                        if len(testo_formattato) < 400:
                            partite_trovate.append({"raw_data": testo_formattato})
                except Exception as inner_e:
                    continue

            browser.close()

    except Exception as e:
        print(f"Errore durante lo scraping: {e}")

    # Salva i dati estratti nel file JSON
    data_to_save = {
        "partite": partite_trovate
    }
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data_to_save, f, ensure_ascii=False, indent=2)
        
    print(f"Salvate {len(partite_trovate)} partite in: {output_path}")

if __name__ == "__main__":
    scarica_partite()
