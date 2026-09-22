<script>
(function () {
  const BRANCH = "master";
  const REPO = "campipaolo/Livesoccer";
  const FILES = [
    { nome: "Serie A", url: `https://raw.githubusercontent.com/${REPO}/${BRANCH}/livesoccertv/output/serie-a.json` },
    { nome: "Serie B", url: `https://raw.githubusercontent.com/${REPO}/${BRANCH}/livesoccertv/output/serie-b.json` },
    { nome: "Serie C", url: `https://raw.githubusercontent.com/${REPO}/${BRANCH}/livesoccertv/output/serie-c.json` }
  ];

  const CLASSE_SERIE = { "Serie A": "serie-a", "Serie B": "serie-b", "Serie C": "serie-c" };
  const mesi = { gennaio: 0, febbraio: 1, marzo: 2, aprile: 3, maggio: 4, giugno: 5, luglio: 6, agosto: 7, settembre: 8, ottobre: 9, novembre: 10, dicembre: 11 };

  // Mappatura tra l'hash nell'URL e il valore del filtro
  const HASH_MAP = {
    "#live": "LIVE",
    "#serie-a": "Serie A",
    "#serie-b": "Serie B",
    "#serie-c": "Serie C"
  };

  let filtroAttivo = "ALL";
  let datiCache = { live: [], futuri: [] };

  // Legge l'hash dall'URL e imposta il filtro attivo
  function applicaFiltroDaHash() {
    const hash = window.location.hash.toLowerCase();
    if (HASH_MAP[hash]) {
      filtroAttivo = HASH_MAP[hash];
    } else {
      filtroAttivo = "ALL";
    }

    // Aggiorna lo stato visivo dei pulsanti filtro
    document.querySelectorAll(".btn-filter").forEach(b => {
      const f = b.getAttribute("data-filter");
      if (f === filtroAttivo) {
        b.classList.add("active");
      } else {
        b.classList.remove("active");
      }
    });
  }

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
    
    const canali = Array.isArray(item.canali) ? item.canali.filter(Boolean) : [];
    
    return {
      categoria,
      partita,
      ora: `${String(ora).padStart(2, "0")}:${String(minuti).padStart(2, "0")}`,
      data: dataEvento,
      link,
      canali
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
    
    const canaliHtml = evento.canali.length
      ? `<div class="cal-canali">📺 ${evento.canali.join(", ")}</div>`
      : `<div class="cal-canali cal-canali-vuoto">Canale non indicato</div>`;
    
    div.innerHTML = `
      <div class="cal-ora">
        ${isLive ? '<span class="badge-live-tag">LIVE</span>' : ''}
        ${evento.ora}
      </div>
      <div class="cal-categoria">${evento.categoria}</div>
      <div class="cal-partita">
        ${contenutoPartita}
        ${canaliHtml}
      </div>
    `;
    return div;
  }

  function creaSezioneCategoria(categoria, eventi) {
    const sezione = document.createElement("div");
    sezione.className = "cal-sezione";

    const titolo = document.createElement("div");
    titolo.className = "cal-sezione-titolo " + (CLASSE_SERIE[categoria] || "");
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
      const durataPartitaMs = 2 * 60 * 60 * 1000;
    
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
    
      const btnLive = document.getElementById("btn-live-tag");
      btnLive.textContent = `🔴 LIVE (${live.length})`;
    
      document.getElementById("cal-filters").style.display = "flex";
      
      applicaFiltroDaHash();
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

  document.getElementById("cal-filters").addEventListener("click", (e) => {
    if (!e.target.classList.contains("btn-filter")) return;

    document.querySelectorAll(".btn-filter").forEach(b => b.classList.remove("active"));
    e.target.classList.add("active");
    
    filtroAttivo = e.target.getAttribute("data-filter");
    renderizza();
  });

  // Listener per aggiornare la vista se l'utente naviga cambiando l'hash dell'URL
  window.addEventListener("hashchange", () => {
    applicaFiltroDaHash();
    renderizza();
  });

  eseguiAggiornamento();
  setInterval(eseguiAggiornamento, 60000);
})();
</script>