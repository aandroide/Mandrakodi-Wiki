import json
import os
import re
from datetime import datetime
import zoneinfo
from playwright.sync_api import sync_playwright

# Mappatura dei mesi in italiano per convertire le date in oggetti datetime reali
MESI = {
    "gennaio": 1, "febbraio": 2, "marzo": 3, "aprile": 4, "maggio": 5, "giugno": 6,
    "luglio": 7, "agosto": 8, "settembre": 9, "ottobre": 10, "novembren": 11, "dicembre": 12
}

def converti_in_datetime(data_str, orario_str):
    """Converte 'Sabato, 26 Settembre 2026' e '15:00' in un oggetto datetime ordinabile"""
    try:
        # Cerca giorno, mese e anno nella stringa della data
        match = re.search(r'(\d{1,2})\s+([a-zA-Z]+)(?:\s+(\d{4}))?', data_str.lower())
        if match:
            giorno = int(match.group(1))
            mese_nome = match.group(2)
            anno = int(match.group(3)) if match.group(3) else datetime.now().year
            
            mese = MESI.get(mese_nome, 1)
            ora, minuto = map(int, orario_str.split(":"))
            return datetime(anno, mese, giorno, ora, minuto)
    except Exception:
        pass
    return datetime(1970, 1, 1)

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
            browser = p.chromium.launch(
                headless=True,
                args=['--disable-blink-features=AutomationControlled', '--no-sandbox']
            )
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
                locale="it-IT",
                timezone_id="Europe/Rome"
            )
            page = context.new_page()

            for target in targets:
                lega_nome = target["lega"]
                url = target["url"]
                print(f"Scraping {lega_nome}...")

                try:
                    page.goto(url, wait_until="domcontentloaded", timeout=60000)
                    page.wait_for_timeout(3000)

                    # Forziamo lo scroll per caricare tutto il DOM
                    for _ in range(4):
                        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                        page.wait_for_timeout(800)

                    # Estrazione universale tramite JavaScript
                    eventi = page.evaluate('''() => {
                        const items = [];
                        let dataCorrente = "";
                        
                        // Prendi tutti gli elementi di testo o righe della pagina
                        const block = document.querySelectorAll(".schedules_table tr, .match_row, tr, th");
                        
                        block.forEach(el => {
                            const txt = el.innerText ? el.innerText.trim() : "";
                            if (!txt) return;

                            const lower = txt.toLowerCase();

                            // Riconosce le intestazioni di data
                            if (["lunedì", "martedì", "mercoledì", "giovedì", "venerdì", "sabato", "domenica"].some(g => lower.includes(g))) {
                                const primaLinea = txt.split("\\n")[0].trim();
                                if (primaLinea.length < 60) {
                                    dataCorrente = primaLinea;
                                }
                                return;
                            }

                            // Cerca orario HH:MM
                            const mTime = txt.match(/\\b(\\d{1,2}:\\d{2})\\b/);
                            if (mTime) {
                                items.push({
                                    data: dataCorrente || "Data da definire",
                                    orario: mTime[1],
                                    testo: txt.replace(/\\n/g, " - ")
                                });
                            }
                        });
                        return items;
                    }''')

                    for ev in eventi:
                        testo_p = re.sub(r'^(FIN|Live)\s*-\s*\+\s*-\s*', '', ev["testo"], flags=re.IGNORECASE)
                        testo_p = re.sub(r'^(FIN|Live)\s*-\s*', '', testo_p, flags=re.IGNORECASE)
                        testo_p = re.sub(r'\s*-\s*Disponibile on-demand', '', testo_p, flags=re.IGNORECASE)

                        dt_obj = converti_in_datetime(ev["data"], ev["orario"])

                        partite_trovate.append({
                            "lega": lega_nome,
                            "data": ev["data"],
                            "orario": ev["orario"],
                            "dettagli": f"[{ev['data']} - {ev['orario']}] {testo_p}",
                            "timestamp": dt_obj.timestamp(),
                            "url": url
                        })

                except Exception as e_lega:
                    print(f"Errore su {lega_nome}: {e_lega}")

            browser.close()

    except Exception as e:
        print(f"Errore generale: {e}")

    # ORDINAMENTO CRONOLOGICO REALE: Ordina per timestamp (anno-mese-giorno-ora)
    partite_trovate.sort(key=lambda x: x["timestamp"])

    # Pulizia del campo timestamp prima del salvataggio
    for p_item in partite_trovate:
        p_item.pop("timestamp", None)

    data_to_save = {
        "ultimo_aggiornamento": datetime.now(tz_roma).strftime("%d/%m/%Y %H:%M:%S"),
        "partite": partite_trovate
    }
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data_to_save, f, ensure_ascii=False, indent=2)
        
    print(f"Estratti correttamente {len(partite_trovate)} eventi totali.")

if __name__ == "__main__":
    scarica_partite()
