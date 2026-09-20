import json
import os
from playwright.sync_api import sync_playwright

def scarica_partite():
    partite_trovate = []
    
    with sync_playwright() as p:
        # Avvia un browser headless impostando un User-Agent credibile
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        try:
            # Pagina palinsesto Italia di LiveSoccerTV
            url = "https://www.livesoccertv.com/it/schedules/"
            print(f"Collegamento a {url}...")
            page.goto(url, wait_until="domcontentloaded", timeout=60000)

            # Attendi il caricamento della tabella o dei blocchi partite
            page.wait_for_timeout(3000)

            # Estrazione dei dati tramite selettori DOM
            # (Adatta i selettori CSS se la struttura HTML di LiveSoccerTV cambia)
            rows = page.query_selector_all("tr.match-row, div.match-container")

            for row in rows:
                testo = row.inner_text()
                # Filtra per competizioni italiane o keyword di interesse
                if any(k in testo for k in ["Serie A", "Serie B", "Coppa Italia", "Italia"]):
                    partite_trovate.append({
                        "raw_data": testo.strip().replace("\n", " - ")
                    })

        except Exception as e:
            print(f"Errore durante lo scraping: {e}")
        finally:
            browser.close()

    # Assicurati che la cartella docs/ esista
    os.makedirs("docs", exist_ok=True)
    
    # Salva i dati in docs/partite.json
    output_path = os.path.join("docs", "partite.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump({"aggiornato_il": "", "partite": partite_trovate}, f, ensure_ascii=False, indent=2)
        
    print(f"Salvate {len(partite_trovate)} partite in {output_path}")

if __name__ == "__main__":
    scarica_partite()
