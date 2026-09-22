# Calendario

<style>
  #cal-wrapper {
    --link: var(--md-typeset-a-color, #0066cc);
    --muted: rgba(150, 150, 150, 0.7);
    max-width: 900px;
    margin: 20px auto;
    padding: 0 16px 40px;
  }
  .cal-title {
    text-align: center;
    font-size: 26px;
    font-weight: bold;
    margin-bottom: 20px;
  }
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
  }
  .btn-filter:hover { background: rgba(150, 150, 150, 0.25); }
  .btn-filter.active { background: var(--link); color: #ffffff; border-color: transparent; }
  .btn-filter.btn-live-filter.active { background: #d00000; color: #ffffff; }

  .cal-sezione { margin-top: 25px; scroll-margin-top: 20px; }
  .cal-sezione-titolo {
    font-size: 20px;
    font-weight: bold;
    padding: 8px 12px;
    border-radius: 6px;
    margin-bottom: 12px;
    background: rgba(150, 150, 150, 0.12);
    border-left: 4px solid var(--link);
  }
  .cal-sezione-titolo.serie-a { color: #64b5f6; background: rgba(25, 118, 210, 0.12); border-left-color: #1976d2; }
  .cal-sezione-titolo.serie-b { color: #66bb6a; background: rgba(46, 125, 50, 0.12); border-left-color: #2e7d32; }
  .cal-sezione-titolo.serie-c { color: #ce93d8; background: rgba(106, 27, 154, 0.12); border-left-color: #6a1b9a; }
  .cal-live-titolo { background: rgba(224, 0, 0, 0.12); color: #e00000; border-left-color: #e00000; }

  .cal-data {
    font-size: 15px;
    font-weight: bold;
    margin: 15px 0 6px;
    padding: 6px 10px;
    background: rgba(150, 150, 150, 0.08);
    border-left: 3px solid var(--muted);
    opacity: 0.9;
  }
  .cal-evento {
    display: grid;
    grid-template-columns: 65px 85px 1fr;
    align-items: start;
    gap: 8px;
    padding: 10px;
    border-bottom: 1px solid rgba(150, 150, 150, 0.15);
  }
  .cal-ora { font-weight: bold; font-size: 14px; }
  .cal-categoria { font-size: 12px; font-weight: bold; opacity: 0.7; text-transform: uppercase; }
  .cal-canali { font-size: 12.5px; opacity: 0.75; margin-top: 3px; }
  .cal-canali.cal-canali-vuoto { font-style: italic; }
  .cal-evento.is-live { background: rgba(224, 0, 0, 0.06); border-left: 3px solid #e00000; }
  .cal-evento.is-live .cal-ora { color: #e00000; }
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
  .cal-caricamento { text-align: center; padding: 30px; opacity: 0.7; }
  .cal-errore {
    color: #ff8a80;
    background: rgba(224, 0, 0, 0.1);
    padding: 15px;
    border-radius: 6px;
    border: 1px solid rgba(224, 0, 0, 0.3);
  }
</style>

<div id="cal-wrapper">
  <div class="cal-title">⚽ Calendario</div>

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
  // Un solo file da leggere: eventi.json ha gia' competizione, titolo, data, ora e canali
  // pronti all'uso, niente piu' tag [COLOR] da ripulire o nomi di mese da riconoscere.
  const EVENTI_URL = "https://raw.githubusercontent.com/aandroide/Livesoccer/master/livesoccertv/output/eventi.json";

  const CLASSE_SERIE = { "Serie A": "serie-a", "Serie B": "serie-b", "Serie C": "serie-c" };
  const HASH_TO_FILTER = { "live": "LIVE", "serie-a": "Serie A", "serie-b": "Serie B", "serie-c": "Serie C" };
  const DURATA_PARTITA_MS = 2.5 * 60 * 60 * 1000;

  let filtroAttivo = "ALL";
  let datiCache = { live: [], futuri: [] };
  const hashIniziale = (window.location.hash || "").replace("#", "").toLowerCase();
  let hashGestito = false;

  function formatDataLunga(data) {
    return data.toLocaleDateString("it-IT", { weekday: "long", day: "numeric", month: "long" });
  }

  async function caricaEventi() {
    const risposta = await fetch(EVENTI_URL);
    if (!risposta.ok) throw new Error(`Impossibile scaricare il calendario (HTTP ${risposta.status})`);
    const json = await risposta.json();

    return (json.eventi || []).map(ev => ({
      categoria: ev.competizione,
      partita: ev.titolo,
      ora: ev.ora,
      data: new Date(`${ev.data}T${ev.ora}:00`),
      canali: Array.isArray(ev.canali) ? ev.canali.filter(Boolean) : []
    }));
  }

  function creaElementoEvento(evento, isLive) {
    const div = document.createElement("div");
    div.className = "cal-evento" + (isLive ? " is-live" : "");

    const canaliHtml = evento.canali.length
      ? `<div class="cal-canali">📺 ${evento.canali.join(", ")}</div>`
      : `<div class="cal-canali cal-canali-vuoto">Canale non indicato</div>`;

    div.innerHTML = `
      <div class="cal-ora">${isLive ? '<span class="badge-live-tag">LIVE</span>' : ''}${evento.ora}</div>
      <div class="cal-categoria">${evento.categoria}</div>
      <div>${evento.partita}${canaliHtml}</div>
    `;
    return div;
  }

  function creaSezioneCategoria(categoria, eventi) {
    const sezione = document.createElement("div");
    sezione.className = "cal-sezione";
    sezione.id = CLASSE_SERIE[categoria] || "";

    const titolo = document.createElement("div");
    titolo.className = "cal-sezione-titolo " + (CLASSE_SERIE[categoria] || "");
    titolo.textContent = `🇮🇹 ${categoria}`;
    sezione.appendChild(titolo);

    const gruppi = {};
    for (const ev of eventi) {
      const chiave = ev.data.toISOString().slice(0, 10);
      (gruppi[chiave] = gruppi[chiave] || []).push(ev);
    }

    for (const chiave of Object.keys(gruppi).sort()) {
      const eventiGiorno = gruppi[chiave].sort((a, b) => a.data - b.data);
      const divData = document.createElement("div");
      divData.className = "cal-data";
      divData.textContent = formatDataLunga(eventiGiorno[0].data);
      sezione.appendChild(divData);
      eventiGiorno.forEach(ev => sezione.appendChild(creaElementoEvento(ev, false)));
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
      liveSezione.id = "live";
      const liveTitolo = document.createElement("div");
      liveTitolo.className = "cal-sezione-titolo cal-live-titolo";
      liveTitolo.textContent = "🔴 In Corso (LIVE)";
      liveSezione.appendChild(liveTitolo);
      live.forEach(ev => liveSezione.appendChild(creaElementoEvento(ev, true)));
      contenitore.appendChild(liveSezione);
    }

    if (filtroAttivo !== "LIVE") {
      const categorie = filtroAttivo === "ALL" ? ["Serie A", "Serie B", "Serie C"] : [filtroAttivo];
      for (const cat of categorie) {
        const eventiCat = futuri.filter(ev => ev.categoria === cat);
        if (eventiCat.length > 0) contenitore.appendChild(creaSezioneCategoria(cat, eventiCat));
      }
    }

    if (contenitore.children.length === 0) {
      contenitore.innerHTML = `<div class="cal-caricamento">Nessun evento disponibile per il filtro selezionato.</div>`;
    }
  }

  function applicaHashIniziale() {
    if (hashGestito) return;
    hashGestito = true;

    if (hashIniziale && HASH_TO_FILTER[hashIniziale]) {
      filtroAttivo = HASH_TO_FILTER[hashIniziale];
      document.querySelectorAll(".btn-filter").forEach(b => {
        b.classList.toggle("active", b.getAttribute("data-filter") === filtroAttivo);
      });
    }

    renderizza();

    if (hashIniziale) {
      const target = document.getElementById(hashIniziale);
      if (target) target.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  }

  async function aggiorna() {
    try {
      const eventi = await caricaEventi();
      const adesso = new Date();
      const live = [], futuri = [];

      for (const ev of eventi) {
        const fine = new Date(ev.data.getTime() + DURATA_PARTITA_MS);
        (adesso >= ev.data && adesso <= fine ? live : futuri).push(ev);
      }
      futuri.sort((a, b) => a.data - b.data);
      live.sort((a, b) => a.data - b.data);

      datiCache = { live, futuri };
      document.getElementById("btn-live-tag").textContent = `🔴 LIVE (${live.length})`;
      document.getElementById("cal-filters").style.display = "flex";

      hashGestito ? renderizza() : applicaHashIniziale();
    } catch (err) {
      document.getElementById("cal-content").innerHTML =
        `<div class="cal-errore"><strong>Errore nel caricamento dei dati:</strong><br>${err.message}</div>`;
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

  aggiorna();
  setInterval(aggiorna, 60000);
})();
</script>
