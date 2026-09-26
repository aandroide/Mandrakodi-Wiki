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
  details.cal-chiudibile { margin-top: 14px; }
  details.cal-chiudibile > summary { font-size: 17px; font-weight: bold; cursor: pointer; }
  details.cal-chiudibile > summary small { opacity: 0.7; font-weight: normal; }
  details.cal-chiudibile[open] > summary { margin-bottom: 10px; }
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
  .cal-ora-blocco { width: 64px; flex-shrink: 0; text-align: center; }
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
  .cal-data-evento { font-weight: bold; font-size: 15px; line-height: 1.2; }
  .cal-ora-evento { font-weight: normal; font-size: 14px; margin-top: 3px; opacity: 0.85; }
  .cal-evento.is-live .cal-ora-evento { color: #ff6659; opacity: 1; }
  .cal-ordina { display: flex; justify-content: center; gap: 8px; margin: -6px 0 16px; font-size: 13px; }
  .cal-ordina span { opacity: 0.7; align-self: center; }
  .cal-legenda { text-align: center; font-size: 12px; opacity: 0.65; margin: -8px 0 18px; }
  .cal-aggiornato { text-align: center; font-size: 12px; opacity: 0.55; margin-top: 30px; }
</style>

<div id="cal-wrapper">
  <div class="cal-title">🏆 Calendario sport</div>

  <div class="cal-filters" id="cal-filters" style="display:none;"></div>
  <input type="search" id="cal-search" class="cal-search" placeholder="Cerca squadra, pilota, torneo o canale..." style="display:none;">
  <div class="cal-ordina" id="cal-ordina" style="display:none;">
    <span>Ordina:</span>
    <button class="btn-filter active" data-ordine="data">📆 Per data</button>
    <button class="btn-filter" data-ordine="campionato">🗂️ Per categoria</button>
  </div>
  <div class="cal-legenda" id="cal-legenda" style="display:none;">Bordo tratteggiato: differita. Canale sbiadito: streaming.</div>

  <div id="cal-content">
    <div class="cal-caricamento">Caricamento palinsesto in corso...</div>
  </div>
  <div class="cal-aggiornato" id="cal-aggiornato"></div>
</div>

<script>
(function () {
  // Un solo file con tutte le categorie gia' divise in cartelle e sottocartelle.
  const CALENDARIO_URL = "https://raw.githubusercontent.com/aandroide/Livesoccer/refs/heads/master/output/calendario_sport.json";

  // Durata stimata per capire se un evento e' in corso (in minuti)
  const DURATA = { prove: 75, qualifiche: 75, sprint_quali: 60, sprint: 60, gara: 150, evento: 150 };
  const DURATA_DEFAULT = 135;
  const ICONE = { "Oggi": "📅", "Motori": "🏎️", "Calcio": "⚽", "Tennis": "🎾", "Basket": "🏀", "Volley": "🏐", "Altri sport": "🏅" };

  let dati = null;
  let filtro = "ALL";
  let testo = "";
  let ordine = "data";

  // icona dello sport nella scheda: per le moto (MotoGP, Moto2/Moto3, Superbike e le gare
  // moto degli eventi speciali, es. Macau Motorcycle GP) la moto al posto della macchina
  const MOTO_RX = /moto\s?gp|moto2|moto3|superbike|\bwsbk\b|motorcycle/i;
  function iconaEvento(ev) {
    if (ev.categoria === "Motori" && MOTO_RX.test(`${ev.competizione || ""} ${ev.evento || ""}`)) return "🏍️ ";
    return ICONE[ev.categoria] ? ICONE[ev.categoria] + " " : "";
  }
  // categorie aperte a mano nella vista "Tutti": restano aperte quando la pagina si ridisegna
  const sezioniAperte = new Set();
  document.addEventListener("toggle", e => {
    const d = e.target;
    if (!d.matches || !d.matches("details.cal-chiudibile") || testo) return;
    if (d.open) sezioniAperte.add(d.dataset.sezione); else sezioniAperte.delete(d.dataset.sezione);
  }, true);

  function giornoLungo(d) {
    const oggi = new Date(); oggi.setHours(0, 0, 0, 0);
    const g = new Date(d); g.setHours(0, 0, 0, 0);
    const diff = Math.round((g - oggi) / 86400000);
    const testo = g.toLocaleDateString("it-IT", { weekday: "long", day: "numeric", month: "long" });
    const t = testo.charAt(0).toUpperCase() + testo.slice(1);
    return diff === 0 ? "Oggi, " + t : diff === 1 ? "Domani, " + t : t;
  }

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

  // Liste "Altri paesi" aperte: la pagina si ridisegna ogni minuto, cosi' restano aperte
  const mondoAperti = new Set();
  window.calToggleMondo = function (chiave, id) {
    const el = document.getElementById(id);
    if (!el) return;
    el.classList.toggle("aperta");
    if (el.classList.contains("aperta")) mondoAperti.add(chiave); else mondoAperti.delete(chiave);
  };

  function mondoHtml(ev) {
    const lista = Array.isArray(ev.canali_mondo) ? ev.canali_mondo : [];
    if (!lista.length) return "";
    const chiave = ev.inizio + "|" + (ev.titolo || "");
    const id = "cal-mondo-" + slug(chiave);
    const righe = lista.map(p =>
      `<div class="cal-mondo-riga"><span class="cal-mondo-paese">${esc(p.paese)}</span><span class="cal-mondo-canali">${esc((p.canali || []).join(", "))}</span></div>`).join("");
    const aperta = mondoAperti.has(chiave) ? " aperta" : "";
    return `<button type="button" class="cal-mondo-btn" onclick="calToggleMondo('${esc(chiave).replace(/'/g, "\\'")}', '${id}')">🌍 Altri paesi (${lista.length})</button>
            <div id="${id}" class="cal-mondo-lista${aperta}">${righe}</div>`;
  }

  function cardEvento(ev, adesso) {
    const st = stato(ev, adesso);
    const tag = st === "live" ? '<span class="badge-live-tag">LIVE</span>' : "";
    return `
      <div class="cal-evento ${st === "live" ? "is-live" : ""}">
        <div class="cal-ora-blocco">${tag}<div class="cal-data-evento">${esc(giorno(ev))}</div><div class="cal-ora-evento">${esc(ev.ora || "--:--")}</div></div>
        <div>
          <div class="cal-categoria">${iconaEvento(ev)}${esc(ev.competizione || ev.sport || "")}</div>
          <div class="cal-partita-nome">${esc(ev.evento || ev.titolo)}</div>
          ${chipCanali(ev)}
          ${mondoHtml(ev)}
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

  // conteggi calcolati nella pagina: gli eventi finiti non contano, cosi' "Oggi" e le altre
  // categorie scendono da sole durante la giornata, senza aspettare un nuovo giro del workflow
  function contaAttivi(cart, adesso) {
    const evs = cart.eventi || (cart.sottocartelle || []).flatMap(sub => sub.eventi);
    return evs.filter(ev => stato(ev, adesso) !== "finito").length;
  }

  function disegnaFiltri(adesso) {
    const live = tuttiGliEventi().filter(ev => stato(ev, adesso) === "live").length;
    const bottoni = [`<button class="btn-filter ${filtro === "ALL" ? "active" : ""}" data-filter="ALL">Tutti</button>`,
      `<button class="btn-filter btn-live-filter ${filtro === "LIVE" ? "active" : ""}" data-filter="LIVE">🔴 LIVE (${live})</button>`];
    for (const cart of dati.cartelle) {
      bottoni.push(`<button class="btn-filter ${filtro === slug(cart.nome) ? "active" : ""}" data-filter="${slug(cart.nome)}">${ICONE[cart.nome] || ""} ${esc(cart.nome)} (${contaAttivi(cart, adesso)})</button>`);
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
        let gruppi = cart.eventi ? [{ nome: "", eventi: cart.eventi }] : cart.sottocartelle;
        if (ordine === "data" && !cart.eventi) {
          // stessi eventi, ma raggruppati per giorno invece che per campionato
          const tutti = cart.sottocartelle.flatMap(sub => sub.eventi)
            .sort((a, b) => a.inizio.localeCompare(b.inizio));
          const perGiorno = new Map();
          for (const ev of tutti) {
            const k = ev.inizio.slice(0, 10);
            if (!perGiorno.has(k)) perGiorno.set(k, []);
            perGiorno.get(k).push(ev);
          }
          gruppi = Array.from(perGiorno.values()).map(evs => ({ nome: giornoLungo(evs[0].inizio), eventi: evs }));
        }
        for (const sub of gruppi) {
          const evs = sub.eventi.filter(ev => stato(ev, adesso) !== "finito" && corrisponde(ev));
          if (!evs.length) continue;
          if (sub.nome) corpo += `<div class="cal-sotto-titolo">${esc(sub.nome)} <small>(${evs.length})</small></div>`;
          corpo += evs.map(ev => cardEvento(ev, adesso)).join("");
        }
        if (!corpo) continue;
        if (filtro === "ALL") {
          // vista "Tutti": categorie chiuse e apribili con un clic, come nel resto della wiki.
          // Con una ricerca in corso si aprono da sole, cosi' i risultati restano visibili.
          const aperta = testo || sezioniAperte.has(id) ? " open" : "";
          const n = (corpo.match(/class="cal-evento/g) || []).length;
          html += `<details class="cal-sezione cal-chiudibile" id="${id}" data-sezione="${id}"${aperta}><summary>${ICONE[cart.nome] || ""} ${esc(cart.nome)} <small>(${n})</small></summary>${corpo}</details>`;
        } else {
          html += `<div class="cal-sezione" id="${id}"><div class="cal-sezione-titolo">${ICONE[cart.nome] || ""} ${esc(cart.nome)}</div>${corpo}</div>`;
        }
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
      const boxOrdine = document.getElementById("cal-ordina");
      boxOrdine.style.display = "flex";
      boxOrdine.querySelectorAll("button").forEach(b => b.onclick = () => {
        ordine = b.dataset.ordine;
        boxOrdine.querySelectorAll("button").forEach(x => x.classList.toggle("active", x === b));
        disegna();
      });
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
