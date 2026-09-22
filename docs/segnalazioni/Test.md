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
  const BASE_COMMIT = "93770da86eb3d6bdfcd4f4df1828cafef487afb0";
  const FILES = [
    { nome: "Serie A", url: `https://raw.githubusercontent.com/campipaolo/Livesoccer/${BASE_COMMIT}/livesoccertv/output/serie-a.json` },
    { nome: "Serie B", url: `https://raw.githubusercontent.com/campipaolo/Livesoccer/${BASE_COMMIT}/livesoccertv/output/serie-b.json` },
    { nome: "Serie C", url: `https://raw.githubusercontent.com/campipaolo/Livesoccer/${BASE_COMMIT}/livesoccertv/output/serie-c.json` }
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
    
    // Se vuoi collegare i pulsanti alla pagina del calendario completo, inserisci il link in 'href' (es: href="calendario.html")
    const container = document.getElementById("cal-summary-bar");
    container.innerHTML = `
      <a href="./#live" class="cal-btn-badge cal-btn-live">
        🔴 LIVE <span class="cal-count">${totLive}</span>
      </a>
      <a href="./#serie-a" class="cal-btn-badge">
        🇮🇹 Serie A <span class="cal-count">${conteggi["Serie A"]}</span>
      </a>
      <a href="./#serie-b" class="cal-btn-badge">
        🇮🇹 Serie B <span class="cal-count">${conteggi["Serie B"]}</span>
      </a>
      <a href="./#serie-c" class="cal-btn-badge">
        🇮🇹 Serie C <span class="cal-count">${conteggi["Serie C"]}</span>
      </a>
    `;
  }

  contaEventi();
})();
</script>

<style>
/* Reset dinamico dei colori basato sul tema corrente */
#cal-wrapper {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  max-width: 900px;
  margin: 20px auto;
  color: inherit;
}

.cal-title {
  text-align: center;
  font-size: 26px;
  font-weight: bold;
  margin-bottom: 20px;
}

/* Pulsanti Filtro */
.cal-filters {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  justify-content: center;
  margin-bottom: 25px;
}

.btn-filter {
  background: rgba(150, 150, 150, 0.15);
  color: inherit;
  border: 1px solid rgba(150, 150, 150, 0.3);
  padding: 8px 14px;
  border-radius: 20px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-filter:hover {
  background: rgba(150, 150, 150, 0.25);
}

.btn-filter.active {
  background: var(--md-typeset-a-color, #0066cc);
  color: #ffffff !important;
  border-color: transparent;
}

.btn-filter.btn-live-filter.active {
  background: #d00000;
  color: #ffffff !important;
}

/* Sezioni e Intestazioni */
.cal-sezione {
  margin-top: 25px;
}

.cal-sezione-titolo {
  font-size: 20px;
  font-weight: bold;
  padding: 8px 12px;
  border-radius: 6px;
  margin-bottom: 12px;
  background: rgba(150, 150, 150, 0.12);
  border-left: 4px solid var(--md-typeset-a-color, #0066cc);
}

.cal-live-titolo {
  background: rgba(224, 0, 0, 0.12);
  color: #e00000;
  border-left-color: #e00000;
}

.cal-data {
  font-size: 15px;
  font-weight: bold;
  margin-top: 15px;
  margin-bottom: 6px;
  padding: 6px 10px;
  background: rgba(150, 150, 150, 0.08);
  border-left: 3px solid rgba(150, 150, 150, 0.5);
  opacity: 0.9;
}

/* Elemento Evento */
.cal-evento {
  display: grid;
  grid-template-columns: 65px 85px 1fr;
  align-items: center;
  gap: 8px;
  padding: 10px;
  border-bottom: 1px solid rgba(150, 150, 150, 0.15);
}

.cal-ora {
  font-weight: bold;
  font-size: 14px;
}

.cal-categoria {
  font-size: 12px;
  font-weight: bold;
  opacity: 0.7;
  text-transform: uppercase;
}

.cal-partita a {
  color: var(--md-typeset-a-color, #0066cc);
  text-decoration: none;
}

.cal-partita a:hover {
  text-decoration: underline;
}

.cal-evento.is-live {
  background: rgba(224, 0, 0, 0.06);
  border-left: 3px solid #e00000;
}

.cal-evento.is-live .cal-ora {
  color: #e00000;
}

.badge-live-tag {
  display: inline-block;
  background: #e00000;
  color: #ffffff;
  font-size: 10px;
  font-weight: bold;
  padding: 2px 5px;
  border-radius: 3px;
  margin-right: 4px;
  vertical-align: middle;
}

.cal-caricamento {
  text-align: center;
  padding: 30px;
  opacity: 0.7;
}

.cal-errore {
  color: #c00000;
  background: rgba(224, 0, 0, 0.1);
  padding: 15px;
  border-radius: 6px;
  border: 1px solid rgba(224, 0, 0, 0.3);
}
</style>

<div id="cal-wrapper">
  <div class="cal-title">⚽ Calendario</div>

  <!-- Barra dei Filtri -->
  <div class="cal-filters" id="cal-filters" style="display:none;">
    <button class="btn-filter active" data-filter="ALL">Tutti</button>
    <button class="btn-filter btn-live-filter" data-filter="LIVE" id="btn-live-tag">🔴 LIVE (0)</button>
    <button class="btn-filter" data-filter="Serie A">Serie A</button>
    <button class="btn-filter" data-filter="Serie B">Serie B</button>
    <button class="btn-filter" data-filter="Serie C">Serie C</button>
  </div>

  <div id="cal-content">
    <div class="cal-caricamento">Caricamento palinsesto in corso...</div>
  </div>
</div>

<script>
(function () {
  const BASE_COMMIT = "93770da86eb3d6bdfcd4f4df1828cafef487afb0";
  const FILES = [
    { nome: "Serie A", url: `https://raw.githubusercontent.com/campipaolo/Livesoccer/${BASE_COMMIT}/livesoccertv/output/serie-a.json` },
    { nome: "Serie B", url: `https://raw.githubusercontent.com/campipaolo/Livesoccer/${BASE_COMMIT}/livesoccertv/output/serie-b.json` },
    { nome: "Serie C", url: `https://raw.githubusercontent.com/campipaolo/Livesoccer/${BASE_COMMIT}/livesoccertv/output/serie-c.json` }
  ];

  const mesi = { gennaio: 0, febbraio: 1, marzo: 2, aprile: 3, maggio: 4, giugno: 5, luglio: 6, agosto: 7, settembre: 8, ottobre: 9, novembre: 10, dicembre: 11 };

  let filtroAttivo = "ALL";
  let datiCache = { live: [], futuri: [] };

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
    
    return { giorno, mese, anno, data };
  }

  function estraiEvento(item, dataCorrente, categoria) {
    const titolo = pulisciTesto(item.title);
    const matchOra = titolo.match(/^(\d{1,2}):(\d{2})\s+(.*)$/);

    if (!matchOra || !dataCorrente) return null;
    
    const ora = parseInt(matchOra[1], 10);
    const minuti = parseInt(matchOra[2], 10);
    const partita = matchOra[3].trim();
    
    const dataEvento = new Date(dataCorrente.anno, dataCorrente.mese, dataCorrente.giorno, ora, minuti, 0, 0);
    
    let link = "";
    if (item.info) {
      const trovato = item.info.match(/https?:\/\/[^\s]+/i);
      if (trovato) link = trovato[0];
    }
    
    return {
      categoria,
      partita,
      ora: `${String(ora).padStart(2, "0")}:${String(minuti).padStart(2, "0")}`,
      data: dataEvento,
      link
    };
  }

  async function caricaFile(file) {
    const response = await fetch(file.url);
    if (!response.ok) throw new Error(`Impossibile scaricare ${file.nome} (HTTP ${response.status})`);
    const json = await response.json();

    const eventi = [];
    let dataCorrente = null;
    
    for (const item of json.items || []) {
      const titolo = pulisciTesto(item.title);
      const nuovaData = estraiData(titolo);
    
      if (nuovaData) {
        dataCorrente = nuovaData;
        continue;
      }
    
      const evento = estraiEvento(item, dataCorrente, file.nome);
      if (evento) eventi.push(evento);
    }
    
    return eventi;
  }

  function formatData(data) {
    return data.toLocaleDateString("it-IT", { weekday: "long", day: "numeric", month: "long" });
  }

  function creaElementoEvento(evento, isLive = false) {
    const div = document.createElement("div");
    div.className = "cal-evento" + (isLive ? " is-live" : "");

    const contenutoPartita = evento.link 
      ? `<a href="${evento.link}" target="_blank" rel="noopener">${evento.partita}</a>`
      : evento.partita;
    
    div.innerHTML = `
      <div class="cal-ora">
        ${isLive ? '<span class="badge-live-tag">LIVE</span>' : ''}
        ${evento.ora}
      </div>
      <div class="cal-categoria">${evento.categoria}</div>
      <div class="cal-partita">${contenutoPartita}</div>
    `;
    return div;
  }

  function creaSezioneCategoria(categoria, eventi) {
    const sezione = document.createElement("div");
    sezione.className = "cal-sezione";

    const titolo = document.createElement("div");
    titolo.className = "cal-sezione-titolo";
    titolo.textContent = `🇮🇹 ${categoria}`;
    sezione.appendChild(titolo);
    
    const gruppi = {};
    for (const evento of eventi) {
      const chiave = `${evento.data.getFullYear()}-${String(evento.data.getMonth() + 1).padStart(2, "0")}-${String(evento.data.getDate()).padStart(2, "0")}`;
      if (!gruppi[chiave]) gruppi[chiave] = [];
      gruppi[chiave].push(evento);
    }
    
    const dateOrdinate = Object.keys(gruppi).sort();
    
    for (const chiave of dateOrdinate) {
      const eventiGiorno = gruppi[chiave].sort((a, b) => a.data - b.data);
      
      const divData = document.createElement("div");
      divData.className = "cal-data";
      divData.textContent = formatData(eventiGiorno[0].data);
      sezione.appendChild(divData);
    
      for (const ev of eventiGiorno) {
        sezione.appendChild(creaElementoEvento(ev, false));
      }
    }
    
    return sezione;
  }

  function renderizza() {
    const contenitore = document.getElementById("cal-content");
    contenitore.innerHTML = "";

    const { live, futuri } = datiCache;
    
    // 1. Render SEZIONE LIVE
    if ((filtroAttivo === "ALL" || filtroAttivo === "LIVE") && live.length > 0) {
      const liveSezione = document.createElement("div");
      liveSezione.className = "cal-sezione";
    
      const liveTitolo = document.createElement("div");
      liveTitolo.className = "cal-sezione-titolo cal-live-titolo";
      liveTitolo.textContent = "🔴 In Corso (LIVE)";
      liveSezione.appendChild(liveTitolo);
    
      for (const ev of live) {
        liveSezione.appendChild(creaElementoEvento(ev, true));
      }
      contenitore.appendChild(liveSezione);
    }
    
    // 2. Render SEZIONI CATEGORIA
    if (filtroAttivo !== "LIVE") {
      const categorie = (filtroAttivo === "ALL") ? ["Serie A", "Serie B", "Serie C"] : [filtroAttivo];
    
      for (const cat of categorie) {
        const eventiCat = futuri.filter(ev => ev.categoria === cat);
        if (eventiCat.length > 0) {
          contenitore.appendChild(creaSezioneCategoria(cat, eventiCat));
        }
      }
    }
    
    if (contenitore.children.length === 0) {
      contenitore.innerHTML = `<div class="cal-caricamento">Nessun evento disponibile per il filtro selezionato.</div>`;
    }
  }

  async function eseguiAggiornamento() {
    try {
      const risultati = await Promise.all(FILES.map(caricaFile));
      const tuttiGliEventi = risultati.flat().sort((a, b) => a.data - b.data);

      const adesso = new Date();
      const durataPartitaMs = 2 * 60 * 60 * 1000; // 2 ore
    
      const live = [];
      const futuri = [];
    
      for (const ev of tuttiGliEventi) {
        const inizio = ev.data;
        const fine = new Date(inizio.getTime() + durataPartitaMs);
    
        if (adesso >= inizio && adesso <= fine) {
          live.push(ev);
        } else {
          futuri.push(ev);
        }
      }
    
      datiCache = { live, futuri };
    
      // Aggiorna Badge e contatore LIVE
      const btnLive = document.getElementById("btn-live-tag");
      btnLive.textContent = `🔴 LIVE (${live.length})`;
    
      document.getElementById("cal-filters").style.display = "flex";
      renderizza();
    
    } catch (err) {
      document.getElementById("cal-content").innerHTML = `
        <div class="cal-errore">
          <strong>Errore nel caricamento dei dati:</strong><br>${err.message}
        </div>
      `;
      console.error(err);
    }
  }

  // Event Listeners per i Pulsanti Filtro
  document.getElementById("cal-filters").addEventListener("click", (e) => {
    if (!e.target.classList.contains("btn-filter")) return;

    document.querySelectorAll(".btn-filter").forEach(b => b.classList.remove("active"));
    e.target.classList.add("active");
    
    filtroAttivo = e.target.getAttribute("data-filter");
    renderizza();
  });

  // Avvio iniziale
  eseguiAggiornamento();

  // Polling automatico in background senza ricaricare la pagina
  setInterval(eseguiAggiornamento, 60000);

})();
</script>
