<style>
/* Grid Container per la Home Page */
.home-stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 16px;
  max-width: 900px;
  margin: 20px auto;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
}

/* Card Singola */
.home-stat-card {
  background: rgba(150, 150, 150, 0.08);
  border: 1px solid rgba(150, 150, 150, 0.2);
  border-radius: 12px;
  padding: 18px 15px;
  text-align: center;
  text-decoration: none !important;
  color: inherit !important;
  transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  cursor: pointer;
}

.home-stat-card:hover {
  transform: translateY(-3px);
  border-color: var(--md-typeset-a-color, #0066cc);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

/* Stile Speciale Card LIVE */
.home-stat-card.card-live {
  background: rgba(224, 0, 0, 0.05);
  border-color: rgba(224, 0, 0, 0.3);
}

.home-stat-card.card-live:hover {
  border-color: #e00000;
  box-shadow: 0 4px 12px rgba(224, 0, 0, 0.15);
}

.home-stat-card.card-live.has-live {
  animation: pulse-live 2s infinite;
}

@keyframes pulse-live {
  0% { box-shadow: 0 0 0 0 rgba(224, 0, 0, 0.4); }
  70% { box-shadow: 0 0 0 8px rgba(224, 0, 0, 0); }
  100% { box-shadow: 0 0 0 0 rgba(224, 0, 0, 0); }
}

/* Elementi Interni */
.home-stat-icon {
  font-size: 20px;
  margin-bottom: 6px;
}

.home-stat-label {
  font-size: 14px;
  font-weight: 600;
  opacity: 0.8;
  margin-bottom: 8px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.home-stat-count {
  font-size: 32px;
  font-weight: 800;
  line-height: 1;
}

.card-live .home-stat-count {
  color: #e00000;
}

/* Indicatori di Caricamento/Errore */
.home-stat-count.loading {
  font-size: 18px;
  opacity: 0.5;
}
</style>

<!-- Grid Pulsanti Home Page -->
<div class="home-stats-grid">
  <!-- Sostituisci "calendario.html" con il percorso/URL della tua pagina Calendario -->
  <a href="calendario.html" class="home-stat-card card-live" id="card-live">
    <div class="home-stat-icon">🔴</div>
    <div class="home-stat-label">In Corso</div>
    <div class="home-stat-count loading" id="cnt-live">...</div>
  </a>

  <a href="calendario.html" class="home-stat-card">
    <div class="home-stat-icon">🇮🇹</div>
    <div class="home-stat-label">Serie A</div>
    <div class="home-stat-count loading" id="cnt-serie-a">...</div>
  </a>

  <a href="calendario.html" class="home-stat-card">
    <div class="home-stat-icon">⚽</div>
    <div class="home-stat-label">Serie B</div>
    <div class="home-stat-count loading" id="cnt-serie-b">...</div>
  </a>

  <a href="calendario.html" class="home-stat-card">
    <div class="home-stat-icon">🏟️</div>
    <div class="home-stat-label">Serie C</div>
    <div class="home-stat-count loading" id="cnt-serie-c">...</div>
  </a>
</div>

<script>
(function () {
  const BASE_COMMIT = "93770da86eb3d6bdfcd4f4df1828cafef487afb0";
  const FILES = [
    { key: "serie-a", url: `https://raw.githubusercontent.com/campipaolo/Livesoccer/${BASE_COMMIT}/livesoccertv/output/serie-a.json` },
    { key: "serie-b", url: `https://raw.githubusercontent.com/campipaolo/Livesoccer/${BASE_COMMIT}/livesoccertv/output/serie-b.json` },
    { key: "serie-c", url: `https://raw.githubusercontent.com/campipaolo/Livesoccer/${BASE_COMMIT}/livesoccertv/output/serie-c.json` }
  ];

  const mesi = { gennaio: 0, febbraio: 1, marzo: 2, aprile: 3, maggio: 4, giugno: 5, luglio: 6, agosto: 7, settembre: 8, ottobre: 9, novembre: 10, dicembre: 11 };

  function pulisciTesto(testo) {
    return (testo || "").replace(/\[COLOR [^\]]+\]/gi, "").replace(/\[\/COLOR\]/gi, "").trim();
  }

  function estraiData(testo) {
    testo = pulisciTesto(testo);
    const parti = testo.toLowerCase().replace(/,/g, "").split(/\s+/);
    let giorno = null, mese = null;

    for (const parte of parti) {
      if (/^\d+$/.test(parte)) giorno = parseInt(parte, 10);
      if (mesi[parte] !== undefined) mese = mesi[parte];
    }
    
    if (giorno === null || mese === null) return null;
    
    const oggi = new Date();
    let anno = oggi.getFullYear();
    const data = new Date(anno, mese, giorno);
    
    if (data.getTime() < oggi.getTime() - (180 * 24 * 60 * 60 * 1000)) {
      anno++;
    }
    
    return { giorno, mese, anno };
  }

  function estraiEvento(item, dataCorrente) {
    const titolo = pulisciTesto(item.title);
    const matchOra = titolo.match(/^(\d{1,2}):(\d{2})\s+(.*)$/);

    if (!matchOra || !dataCorrente) return null;
    
    const ora = parseInt(matchOra[1], 10);
    const minuti = parseInt(matchOra[2], 10);
    
    return new Date(dataCorrente.anno, dataCorrente.mese, dataCorrente.giorno, ora, minuti, 0, 0);
  }

  async function calcolaStatistiche() {
    const adesso = new Date();
    const durataPartitaMs = 2 * 60 * 60 * 1000; // 2 ore

    let totaleLive = 0;
    const conteggi = { "serie-a": 0, "serie-b": 0, "serie-c": 0 };
    
    await Promise.all(FILES.map(async (file) => {
      try {
        const response = await fetch(file.url);
        if (!response.ok) return;
        const json = await response.json();
    
        let dataCorrente = null;
    
        for (const item of json.items || []) {
          const titolo = pulisciTesto(item.title);
          const nuovaData = estraiData(titolo);
    
          if (nuovaData) {
            dataCorrente = nuovaData;
            continue;
          }
    
          const dataEvento = estraiEvento(item, dataCorrente);
          if (dataEvento) {
            conteggi[file.key]++;
    
            // Controllo Live
            const fine = new Date(dataEvento.getTime() + durataPartitaMs);
            if (adesso >= dataEvento && adesso <= fine) {
              totaleLive++;
            }
          }
        }
      } catch (e) {
        console.error(`Errore nel caricamento di ${file.key}:`, e);
      }
    }));
    
    // Aggiornamento DOM
    aggiornaConteggio("cnt-live", totaleLive);
    aggiornaConteggio("cnt-serie-a", conteggi["serie-a"]);
    aggiornaConteggio("cnt-serie-b", conteggi["serie-b"]);
    aggiornaConteggio("cnt-serie-c", conteggi["serie-c"]);
    
    // Effetto Pulsante Se Ci Sono Partite Live
    const cardLive = document.getElementById("card-live");
    if (totaleLive > 0) {
      cardLive.classList.add("has-live");
    } else {
      cardLive.classList.remove("has-live");
    }
  }

  function aggiornaConteggio(id, valore) {
    const el = document.getElementById(id);
    if (el) {
      el.textContent = valore;
      el.classList.remove("loading");
    }
  }

  // Esecuzione iniziale e Refresh automatico ogni 60 secondi
  calcolaStatistiche();
  setInterval(calcolaStatistiche, 60000);
})();
</script>
