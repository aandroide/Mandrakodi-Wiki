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
            # Impostiamo argomenti del browser per evitare i blocchi anti-bot su GitHub Actions
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
                print(f"Scraping {lega_nome} da {url}...")

                try:
                    page.goto(url, wait_until="domcontentloaded", timeout=60000)
                    
                    # Attesa esplicita che la tabella del palinsesto sia presente nel DOM
                    page.wait_for_selector("table, .schedules, .match-row", timeout=15000)
                    page.wait_for_timeout(2000)

                    # Simula lo scroll per caricare tutti gli elementi
                    page.evaluate("window.scrollTo(0, document.body.scrollHeight / 2)")
                    page.wait_for_timeout(1000)
                    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                    page.wait_for_timeout(1000)

                    # Estrai il contenuto strutturato via JavaScript direttamente dal browser
                    eventi_pagina = page.evaluate('''() => {
                        const risultati = [];
                        let dataAttuale = "Data non specificata";
                        
                        // Trova tutti gli elementi rilevanti nella pagina
                        const elementi = document.querySelectorAll("th, tr, div.match_row, .schedules_table tr");
                        
                        elementi.forEach(el => {
                            const testo = el.innerText ? el.innerText.trim() : "";
                            if (!testo) return;

                            const testoLower = testo.toLowerCase();

                            // Rileva le intestazioni con i giorni della settimana
                            if (["lunedì", "martedì", "mercoledì", "giovedì", "venerdì", "sabato", "domenica"].some(g => testoLower.includes(g))) {
                                const primaRiga = testo.split("\\n")[0].trim();
                                if (primaRiga.length < 50) {
                                    dataAttuale = primaRiga;
                                }
                                return;
                            }

                            // Verifica se la riga contiene un orario (es. 15:00 o 20:45)
                            const matchOrario = testo.match(/\\b(\\d{1,2}:\\d{2})\\b/);
                            if (matchOrario) {
                                risultati.push({
                                    data: dataAttuale,
                                    orario: matchOrario[1],
                                    testoGrezzio: testo.replace(/\\n/g, " - ")
                                });
                            }
                        });
                        return risultati;
                    }''')

                    for ev in eventi_pagina:
                        testo_completo = ev["testoGrezzio"]
                        
                        # Pulizia del testo
                        testo_pulito = re.sub(r'^(FIN|Live)\s*-\s*\+\s*-\s*', '', testo_completo, flags=re.IGNORECASE)
                        testo_pulito = re.sub(r'^(FIN|Live)\s*-\s*', '', testo_pulito, flags=re.IGNORECASE)
                        testo_pulito = re.sub(r'\s*-\s*Disponibile on-demand', '', testo_pulito, flags=re.IGNORECASE)

                        partite_trovate.append({
                            "lega": lega_nome,
                            "data": ev["data"],
                            "orario": ev["orario"],
                            "dettagli": f"[{ev['data']} - {ev['orario']}] {testo_pulito}",
                            "url": url
                        })

                except Exception as err_target:
                    print(f"Errore su {lega_nome}: {err_target}")

            browser.close()

    except Exception as e:
        print(f"Errore generale: {e}")

    # Salva il JSON anche se vuoto per evitare crash JS
    data_to_save = {
        "ultimo_aggiornamento": datetime.now(tz_roma).strftime("%d/%m/%Y %H:%M:%S"),
        "partite": partite_trovate
    }
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data_to_save, f, ensure_ascii=False, indent=2)
        
    print(f"Totale partite estratte: {len(partite_trovate)}")

if __name__ == "__main__":
    scarica_partite()
