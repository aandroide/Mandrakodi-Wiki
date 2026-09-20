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

                    # Seleziona le righe della tabella palinsesto
                    rows = page.query_selector_all("tr.match-row, tr[id^='m_'], table.schedules tr")

                    is_sezione_oggi = False

                    for row in rows:
                        try:
                            text = row.inner_text().strip()
                            if not text:
                                continue

                            testo_lower = text.lower()

                            # Identifica se la riga è un'intestazione di data
                            if any(giorno in testo_lower for giorno in ["lunedì", "martedì", "mercoledì", "giovedì", "venerdì", "sabato", "domenica"]):
                                # Se l'intestazione contiene 'oggi', attivi la raccolta, altrimenti la disattivi
                                if "oggi" in testo_lower:
                                    is_sezione_oggi = True
                                else:
                                    is_sezione_oggi = False
                                continue

                            # Filtro di sicurezza: estrai solo se siamo nella sezione "oggi" o se c'è un orario valido senza date nel testo
                            time_match = re.search(r'\b(\d{1,2}:\d{2})\b', text)
                            orario = time_match.group(1) if time_match else None

                            # Se non c'è un orario (es. link/menu vari) o non fa parte delle gare odierne, scarta
                            if not orario:
                                continue

                            # Se si incontrano partite di giorni passati/futuri espliciti
                            if not is_sezione_oggi and ("sabato" in testo_lower or "domenica" in testo_lower or "lunedì" in testo_lower):
                                continue

                            # Pulizia del testo da prefissi indesiderati
                            righe = [r.strip() for r in text.split("\n") if r.strip()]
                            testo_completo = " - ".join(righe)
                            
                            # Rimuovi prefissi 'FIN', 'Live', o 'Disponibile on-demand'
                            testo_pulito = re.sub(r'^(FIN|Live)\s*-\s*\+\s*-\s*', '', testo_completo, flags=re.IGNORECASE)
                            testo_pulito = re.sub(r'\s*-\s*Disponibile on-demand', '', testo_pulito, flags=re.IGNORECASE)

                            partite_trovate.append({
                                "lega": lega_nome,
                                "orario": orario,
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

    data_to_save = {
        "ultimo_aggiornamento": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "partite": partite_trovate
    }
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data_to_save, f, ensure_ascii=False, indent=2)
        
    print(f"Salvate {len(partite_trovate)} partite di oggi in: {output_path}")

if __name__ == "__main__":
    scarica_partite()
