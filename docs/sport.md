[:material-home: Torna alla Home](../index.md){.md-button .md-button--primary} [:material-comment-question: FAQ](../faq/faq.md){ .md-button .md-button--primary } [:material-face-agent: Assistenza](../ask_help.md){ .md-button .md-button--primary }

------



# Calendario sport

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
    display: flex;
    gap: 14px;
    align-items: flex-start;
    padding: 12px;
    margin-bottom: 8px;
    background: rgba(150, 150, 150, 0.05);
    border: 1px solid rgba(150, 150, 150, 0.18);
    border-left: 3px solid var(--link);
    border-radius: 10px;
  }
  .cal-ora-blocco { width: 52px; flex-shrink: 0; text-align: center; }
  .cal-ora { font-weight: bold; font-size: 16px; }
  .cal-categoria { font-size: 12px; font-weight: bold; opacity: 0.7; text-transform: uppercase; }
  .cal-partita-nome { font-size: 16px; font-weight: 600; margin-bottom: 6px; }
  .cal-canali { display: flex; flex-wrap: wrap; gap: 6px; align-items: center; }
  .cal-canale-chip {
    font-size: 12px;
    font-weight: 600;
    padding: 3px 9px;
    border-radius: 12px;
    background: rgba(150, 150, 150, 0.12);
    border: 1px solid rgba(150, 150, 150, 0.25);
    white-space: nowrap;
  }
  .cal-canali.cal-canali-vuoto { font-size: 12.5px; font-style: italic; opacity: 0.6; }

  /* Pulsante "Altri paesi": stesso stile compatto dei chip dei canali, ma cliccabile */
  .cal-mondo-btn {
    display: inline-block;
    margin-top: 8px;
    font: inherit;
    font-size: 12px;
    font-weight: 600;
    background: rgba(150, 150, 150, 0.08);
    border: 1px solid rgba(150, 150, 150, 0.3);
    border-radius: 14px;
    padding: 5px 10px;
    color: inherit;
    cursor: pointer;
  }
  .cal-mondo-btn:hover { background: rgba(150, 150, 150, 0.18); }
  .cal-mondo-lista {
    display: none;
    margin-top: 8px;
    max-height: 240px;
    overflow-y: auto;
    border-top: 1px solid rgba(150, 150, 150, 0.2);
    padding-top: 6px;
  }
  .cal-mondo-lista.aperta { display: block; }
  .cal-mondo-riga {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    gap: 10px;
    font-size: 12.5px;
    padding: 3px 0;
    border-bottom: 1px solid rgba(150, 150, 150, 0.08);
  }
  .cal-mondo-paese { opacity: 0.75; flex-shrink: 0; }
  .cal-mondo-canali { text-align: right; }
  .cal-evento.is-live { border-left-color: #e00000; background: rgba(224, 0, 0, 0.06); }
  .cal-evento.is-live .cal-ora { color: #ff6659; }
  .cal-evento.is-prossimo {
    border-left-color: #ffca28;
    background: rgba(255, 202, 40, 0.06);
    box-shadow: inset 0 0 0 1px rgba(255, 202, 40, 0.25);
    scroll-margin-top: 80px;
  }
  .badge-live-tag, .prossima-tag {
    display: block;
    font-size: 9.5px;
    font-weight: bold;
    letter-spacing: .04em;
    margin-bottom: 2px;
  }
  .badge-live-tag { color: #ff6659; }
  .prossima-tag { color: #ffca28; }
  .cal-caricamento { text-align: center; padding: 30px; opacity: 0.7; }
  .cal-errore {
    color: #ff8a80;
    background: rgba(224, 0, 0, 0.1);
    padding: 15px;
    border-radius: 6px;
    border: 1px solid rgba(224, 0, 0, 0.3);
  }

  /* Aggiunte per il calendario sport */
  .cal-search {
    display: block;
    width: 100%;
    max-width: 420px;
    margin: 0 auto 18px;
    padding: 9px 14px;
    border-radius: 20px;
    border: 1px solid rgba(150, 150, 150, 0.3);
    background: rgba(150, 150, 150, 0.08);
    color: inherit;
    font: inherit;
    font-size: 14px;
  }
  .cal-sotto-titolo {
    font-size: 15px;
    font-weight: bold;
    margin: 18px 0 8px;
    padding: 6px 10px;
    border-radius: 6px;
    background: rgba(150, 150, 150, 0.08);
    border-left: 3px solid var(--link);
  }
  .cal-sotto-titolo small { opacity: 0.6; font-weight: 600; }
  .cal-canale-chip.differita { border-style: dashed; opacity: 0.85; }
  .cal-canale-chip.streaming { opacity: 0.75; }
  .cal-canale-chip .cal-canale-tipo { font-weight: 500; opacity: 0.7; }
  .cal-giorno-evento { font-size: 11px; opacity: 0.65; margin-top: 2px; }
  .cal-legenda { text-align: center; font-size: 12px; opacity: 0.65; margin: -8px 0 18px; }
  .cal-aggiornato { text-align: center; font-size: 12px; opacity: 0.55; margin-top: 30px; }
</style>

<div id="cal-wrapper">
  <div class="cal-title">🏆 Calendario sport</div>

  <div class="cal-filters" id="cal-filters" style="display:none;"></div>
  <input type="search" id="cal-search" class="cal-search" placeholder="Cerca squadra, pilota, torneo o canale..." style="display:none;">
  <div class="cal-legenda" id="cal-legenda" style="display:none;">Bordo tratteggiato: differita. Canale sbiadito: streaming.</div>

  <div id="cal-content">
    <div class="cal-caricamento">Caricamento palinsesto in corso...</div>
  </div>
  <div class="cal-aggiornato" id="cal-aggiornato"></div>
</div>

<script>
(function () {
  // Un solo file con tutte le categorie gia' divise in cartelle e sottocartelle.
  const CALENDARIO_URL = "https://raw.githubusercontent.com/TUO_UTENTE/TUO_REPO/main/output/calendario_sport.json";

  // Durata stimata per capire se un evento e' in corso (in minuti)
  const DURATA = { prove: 75, qualifiche: 75, sprint_quali: 60, sprint: 60, gara: 150, evento: 150 };
  const DURATA_DEFAULT = 135;
  const ICONE = { "Oggi": "📅", "Motori": "🏎️", "Calcio": "⚽", "Tennis": "🎾", "Basket": "🏀", "Volley": "🏐", "Altri sport": "🏅" };

  let dati = null;
  let filtro = "ALL";
  let testo = "";

  const slug = s => s.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "").replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
  const esc = s => String(s == null ? "" : s).replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));

  function stato(ev, adesso) {
    const inizio = new Date(ev.inizio);
    const minuti = DURATA[ev.sessione] || DURATA_DEFAULT;
    const fine = new Date(inizio.getTime() + minuti * 60000);
    if (adesso >= inizio && adesso <= fine) return "live";
    if (adesso > fine) return "finito";
    return "futuro";
  }

  function giorno(ev) {
    return new Date(ev.inizio).toLocaleDateString("it-IT", { weekday: "short", day: "numeric", month: "short" });
  }

  function chipCanali(ev) {
    if (!ev.canali || !ev.canali.length) return '<div class="cal-canali cal-canali-vuoto">Canale da confermare</div>';
    return '<div class="cal-canali">' + ev.canali.map(c => {
      let extra = "";
      if (c.tipo === "differita") extra = ` <span class="cal-canale-tipo">differita${c.orario ? " " + esc(c.orario.slice(11, 16)) : ""}</span>`;
      const num = c.numero ? ` (${esc(c.numero)})` : "";
      return `<span class="cal-canale-chip ${esc(c.tipo)}">${esc(c.nome)}${num}${extra}</span>`;
    }).join("") + "</div>";
  }

  function cardEvento(ev, adesso) {
    const st = stato(ev, adesso);
    const tag = st === "live" ? '<span class="badge-live-tag">LIVE</span>' : "";
    return `
      <div class="cal-evento ${st === "live" ? "is-live" : ""}">
        <div class="cal-ora-blocco">${tag}<div class="cal-ora">${esc(ev.ora || "--:--")}</div><div class="cal-giorno-evento">${esc(giorno(ev))}</div></div>
        <div>
          <div class="cal-categoria">${esc(ev.competizione || ev.sport || "")}</div>
          <div class="cal-partita-nome">${esc(ev.evento || ev.titolo)}</div>
          ${chipCanali(ev)}
        </div>
      </div>`;
  }

  function corrisponde(ev) {
    if (!testo) return true;
    const blob = [ev.titolo, ev.evento, ev.competizione, ev.sport, ev.circuito,
                  ...(ev.canali || []).map(c => c.nome)].join(" ").toLowerCase();
    return blob.includes(testo);
  }

  function tuttiGliEventi() {
    const out = [];
    for (const cart of dati.cartelle) {
      if (cart.nome === "Oggi") continue;
      for (const sub of cart.sottocartelle || []) for (const ev of sub.eventi) out.push(ev);
    }
    return out;
  }

  function disegnaFiltri(adesso) {
    const live = tuttiGliEventi().filter(ev => stato(ev, adesso) === "live").length;
    const bottoni = [`<button class="btn-filter ${filtro === "ALL" ? "active" : ""}" data-filter="ALL">Tutti</button>`,
      `<button class="btn-filter btn-live-filter ${filtro === "LIVE" ? "active" : ""}" data-filter="LIVE">🔴 LIVE (${live})</button>`];
    for (const cart of dati.cartelle) {
      bottoni.push(`<button class="btn-filter ${filtro === slug(cart.nome) ? "active" : ""}" data-filter="${slug(cart.nome)}">${ICONE[cart.nome] || ""} ${esc(cart.nome)} (${cart.totale})</button>`);
    }
    const box = document.getElementById("cal-filters");
    box.innerHTML = bottoni.join("");
    box.style.display = "flex";
    box.querySelectorAll(".btn-filter").forEach(b => b.onclick = () => {
      filtro = b.dataset.filter;
      history.replaceState(null, "", filtro === "ALL" ? location.pathname : "#" + filtro);
      disegna();
    });
  }

  function disegna() {
    const adesso = new Date();
    disegnaFiltri(adesso);
    const box = document.getElementById("cal-content");
    let html = "";

    if (filtro === "LIVE") {
      const live = tuttiGliEventi().filter(ev => stato(ev, adesso) === "live" && corrisponde(ev));
      html += `<div class="cal-sezione" id="live"><div class="cal-sezione-titolo cal-live-titolo">🔴 In diretta adesso</div>`;
      html += live.length ? live.map(ev => cardEvento(ev, adesso)).join("") : '<div class="cal-canali-vuoto">Nessun evento in corso.</div>';
      html += "</div>";
    } else {
      for (const cart of dati.cartelle) {
        const id = slug(cart.nome);
        if (filtro !== "ALL" && filtro !== id) continue;
        if (filtro === "ALL" && cart.nome === "Oggi") continue;
        let corpo = "";
        const gruppi = cart.eventi ? [{ nome: "", eventi: cart.eventi }] : cart.sottocartelle;
        for (const sub of gruppi) {
          const evs = sub.eventi.filter(ev => stato(ev, adesso) !== "finito" && corrisponde(ev));
          if (!evs.length) continue;
          if (sub.nome) corpo += `<div class="cal-sotto-titolo">${esc(sub.nome)} <small>(${evs.length})</small></div>`;
          corpo += evs.map(ev => cardEvento(ev, adesso)).join("");
        }
        if (corpo) html += `<div class="cal-sezione" id="${id}"><div class="cal-sezione-titolo">${ICONE[cart.nome] || ""} ${esc(cart.nome)}</div>${corpo}</div>`;
      }
    }
    box.innerHTML = html || '<div class="cal-caricamento">Nessun evento trovato.</div>';
  }

  async function avvia() {
    try {
      const res = await fetch(CALENDARIO_URL, { cache: "no-store" });
      if (!res.ok) throw new Error("HTTP " + res.status);
      dati = await res.json();
      const hash = (location.hash || "").replace("#", "").toLowerCase();
      if (hash === "live") filtro = "LIVE";
      else if (dati.cartelle.some(c => slug(c.nome) === hash)) filtro = hash;
      const cerca = document.getElementById("cal-search");
      cerca.style.display = "block";
      cerca.oninput = () => { testo = cerca.value.trim().toLowerCase(); disegna(); };
      document.getElementById("cal-legenda").style.display = "block";
      document.getElementById("cal-aggiornato").textContent =
        "Aggiornato: " + new Date(dati.aggiornato).toLocaleString("it-IT", { dateStyle: "short", timeStyle: "short" });
      disegna();
      setInterval(disegna, 60000);
    } catch (e) {
      document.getElementById("cal-content").innerHTML =
        `<div class="cal-errore">Impossibile caricare il calendario (${esc(e.message)}). Riprova tra qualche minuto.</div>`;
    }
  }

  avvia();
})();
</script>
