<style>
.cal-bar-summary {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  align-items: center;
  justify-content: flex-start;
  margin: 15px 0;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
}

.cal-btn-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 6px 14px;
  border-radius: 20px;
  font-size: 14px;
  font-weight: 600;
  text-decoration: none;
  background: rgba(150, 150, 150, 0.12);
  color: inherit;
  border: 1px solid rgba(150, 150, 150, 0.25);
  transition: all 0.2s ease;
}

.cal-btn-badge:hover {
  background: rgba(150, 150, 150, 0.22);
}

.cal-btn-live {
  background: rgba(224, 0, 0, 0.1);
  color: #d00000;
  border-color: rgba(224, 0, 0, 0.3);
}

.cal-btn-live:hover {
  background: rgba(224, 0, 0, 0.2);
}

.cal-count {
  background: rgba(150, 150, 150, 0.2);
  color: inherit;
  font-size: 12px;
  padding: 2px 7px;
  border-radius: 10px;
  font-weight: bold;
}

.cal-btn-live .cal-count {
  background: #d00000;
  color: #ffffff;
}

.cal-loading-dots {
  font-size: 13px;
  opacity: 0.6;
}
</style>

<div class="cal-bar-summary" id="cal-summary-bar">
  <span class="cal-loading-dots">⏳ Caricamento eventi...</span>
</div>


<script>
(function() {
  const BRANCH = "main";
  const REPO = "campipaolo/Livesoccer";
  const FILES = [
    { nome: "Serie A", url: `https://raw.githubusercontent.com/${REPO}/${BRANCH}/livesoccertv/output/serie-a.json` },
    { nome: "Serie B", url: `https://raw.githubusercontent.com/${REPO}/${BRANCH}/livesoccertv/output/serie-b.json` },
    { nome: "Serie C", url: `https://raw.githubusercontent.com/${REPO}/${BRANCH}/livesoccertv/output/serie-c.json` }
  ];


  const mesi = { gennaio: 0, febbraio: 1, marzo: 2, aprile: 3, maggio: 4, giugno: 5, luglio: 6, agosto: 7, settembre: 8, ottobre: 9, novembre: 10, dicembre: 11 };

  function pulisciTesto(t) {
    return (t || "").replace(/\[COLOR [^\]]+\]/gi, "").replace(/\[\/COLOR\]/gi, "").trim();
  }

  function estraiData(testo) {
    testo = pulisciTesto(testo);
    const parti = testo.toLowerCase().replace(/,/g, "").split(/\s+/);
    let giorno = null, mese = null;

    for (const p of parti) {
      if (/^\d+$/.test(p)) giorno = parseInt(p, 10);
      if (mesi[p] !== undefined) mese = mesi[p];
    }
    if (giorno === null || mese === null) return null;
    
    const oggi = new Date();
    let anno = oggi.getFullYear();
    const data = new Date(anno, mese, giorno);
    if (data.getTime() < oggi.getTime() - (180 * 24 * 60 * 60 * 1000)) anno++;
    
    return { giorno, mese, anno, data };

  }

  async function contaEventi() {
    let totLive = 0;
    const conteggi = { "Serie A": 0, "Serie B": 0, "Serie C": 0 };
    const adesso = new Date();
    const durataMs = 2 * 60 * 60 * 1000;

    for (const f of FILES) {
      try {
        const res = await fetch(f.url);
        if (!res.ok) continue;
        const json = await res.json();
        let dataCorrente = null;
    
        for (const item of json.items || []) {
          const tit = pulisciTesto(item.title);
          const dataEstrapolata = estraiData(tit);
    
          if (dataEstrapolata) {
            dataCorrente = dataEstrapolata;
            continue;
          }
    
          const matchOra = tit.match(/^(\d{1,2}):(\d{2})/);
          if (matchOra && dataCorrente) {
            const ora = parseInt(matchOra[1], 10);
            const min = parseInt(matchOra[2], 10);
            const inizio = new Date(dataCorrente.anno, dataCorrente.mese, dataCorrente.giorno, ora, min);
            const fine = new Date(inizio.getTime() + durataMs);
    
            if (adesso >= inizio && adesso <= fine) {
              totLive++;
            } else {
              conteggi[f.nome]++;
            }
          }
        }
      } catch (e) {
        console.error("Errore conteggio per " + f.nome, e);
      }
    }
    
    const container = document.getElementById("cal-summary-bar");
    container.innerHTML = `
      <a href="../calendario/live_events#live" class="cal-btn-badge cal-btn-live">
        🔴 LIVE <span class="cal-count">${totLive}</span>
      </a>
      <a href="../calendario/live_events#serie-a" class="cal-btn-badge">
        🇮🇹 Serie A <span class="cal-count">${conteggi["Serie A"]}</span>
      </a>
      <a href="../calendario/live_events#serie-b" class="cal-btn-badge">
        🇮🇹 Serie B <span class="cal-count">${conteggi["Serie B"]}</span>
      </a>
      <a href="../calendario/live_events#serie-c" class="cal-btn-badge">
        🇮🇹 Serie C <span class="cal-count">${conteggi["Serie C"]}</span>
      </a>
    `;

  }

  contaEventi();
})();
</script>

------

