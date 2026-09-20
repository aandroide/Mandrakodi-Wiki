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

                    # Trova le righe delle partite nella tabella
                    rows = page.query_selector_all("tr.match-row, tr[id^='m_'], table.schedules tr")

                    for row in rows:
                        try:
                            text = row.inner_text().strip()
                            if not text:
                                continue

                            righe = [r.strip() for r in text.split("\n") if r.strip()]
                            testo_completo = " - ".join(righe)
                            testo_lower = testo_completo.lower()

                            # Scarta intestazioni di data e menu
                            if any(header in testo_lower for header in [
                                "competizione", "fase", "canale", "squadra", "lunedì", "martedì", 
                                "mercoledì", "giovedì", "venerdì", "sabato", "domenica", "gennaio", 
                                "febbraio", "marzo", "aprile", "maggio", "giugno", "luglio", 
                                "agosto", "settembre", "ottobre", "novembre", "dicembre"
                            ]) and not re.search(r'\d{1,2}:\d{2}', testo_completo):
                                continue

                            # Cerca l'orario (es. 13:00, 15:00, 18:45, 20:45)
                            time_match = re.search(r'\b(\d{1,2}:\d{2})\b', testo_completo)
                            orario = time_match.group(1) if time_match else None

                            # Se è una partita terminata (FIN), scartala o segnala non live
                            is_finished = "fin" in testo_lower or "disponibile on-demand" in testo_lower
                            
                            # Rileva se è REALE LIVE (es. presenta minuto di gioco 89', 90+5' e non è finita)
                            has_minutes = re.search(r"\b\d{1,2}'|\b\d{1,2}\+\d{1,2}'", testo_completo)
                            is_live = False
                            if (has_minutes or "in diretta" in testo_lower or "live -" in testo_lower) and not is_finished:
                                is_live = True

                            # Deve avere almeno un orario o essere in corso
                            if not (orario or is_live or has_minutes):
                                continue

                            # Pulisci il testo rimuovendo prefissi inutili come "FIN - + -" o "Live - + -"
                            testo_pulito = re.sub(r'^(FIN|Live)\s*-\s*\+\s*-\s*', '', testo_completo, flags=re.IGNORECASE)

                            partite_trovate.append({
                                "lega": lega_nome,
                                "orario": orario,
                                "dettagli": testo_pulito,
                                "is_live": is_live,
                                "is_finished": is_finished,
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
        
    print(f"Salvate {len(partite_trovate)} partite in: {output_path}")

if __name__ == "__main__":
    scarica_partite()
