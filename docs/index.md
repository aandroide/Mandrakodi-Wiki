# **Benvenuti nella Wiki ufficiale di MandraKodi**

![icon](images/icon.gif)

[:material-face-agent: Assistenza](ask_help.md){ .md-button .md-button--primary } 

<style>
.cal-bar {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  margin: 15px 0;
  background: linear-gradient(180deg, rgba(150,150,150,0.10), rgba(150,150,150,0.04));
  border: 1px solid rgba(150, 150, 150, 0.25);
  border-radius: 10px;
  padding: 12px 16px;
}

/* Di base si vede solo la versione desktop; le media query sotto scelgono l'altra */
.cal-bar-desktop { display: flex; }
.cal-bar-tablet, .cal-bar-phone { display: none; }

.cal-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 7px 14px;
  border-radius: 20px;
  font-size: 14px;
  font-weight: 700;
  background: rgba(150, 150, 150, 0.08);
  border: 1px solid rgba(150, 150, 150, 0.25);
  color: inherit;
}

.cal-badge .dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: currentColor;
  display: inline-block;
}

.cal-badge-live { color: #ff6659; border-color: rgba(224, 0, 0, 0.35); }
.cal-badge-a { color: #64b5f6; border-color: rgba(25, 118, 210, 0.35); }
.cal-badge-b { color: #81c784; border-color: rgba(46, 125, 50, 0.35); }
.cal-badge-c { color: #ce93d8; border-color: rgba(106, 27, 154, 0.35); }
.cal-badge strong { color: inherit; }

.cal-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  border-radius: 20px;
  font-size: 14px;
  font-weight: 700;
  text-decoration: none;
  background: #1976d2;
  color: #ffffff !important;
  white-space: nowrap;
}

.cal-btn:hover { background: #1565c0; }

/* Il pulsante intelligente (live o prossima partita) puo' avere un testo piu' lungo del
   solito "Apri calendario": il testo vero e proprio sta in uno span a parte perche' i
   puntini di sospensione funzionano in modo affidabile solo su un elemento a blocco, non
   dentro un contenitore flessibile come .cal-btn. */
.cal-cta { min-width: 0; }
.cal-cta-text {
  display: inline-block;
  max-width: 100%;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  vertical-align: bottom;
}
.cal-bar-desktop .cal-cta { max-width: 320px; }
.cal-bar-phone .cal-cta { flex: 1; min-width: 0; }

.cal-bar-desktop { align-items: center; gap: 10px; flex-wrap: wrap; }
.cal-bar-desktop .cal-spacer { flex: 1; }

.cal-bar-tablet { flex-direction: column; gap: 10px; }
.cal-bar-tablet .cal-tablet-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  font-size: 14px;
}
.cal-select {
  flex: 1;
  background: rgba(150, 150, 150, 0.08);
  border: 1px solid rgba(150, 150, 150, 0.3);
  color: inherit;
  border-radius: 8px;
  padding: 9px 10px;
  font-size: 14px;
  font-weight: 600;
}

.cal-bar-phone { align-items: center; justify-content: space-between; gap: 10px; }

.cal-loading { font-size: 13px; opacity: 0.6; }

/* Sotto i 780px: solo il totale + menu a tendina */
@media (max-width: 780px) {
  .cal-bar-desktop { display: none; }
  .cal-bar-tablet { display: flex; }
}

/* Sotto i 480px: solo il badge LIVE + pulsante */
@media (max-width: 480px) {
  .cal-bar-tablet { display: none; }
  .cal-bar-phone { display: flex; }
}
</style>

<div id="cal-bar-desktop" class="cal-bar cal-bar-desktop">
  <span class="cal-loading">⏳ Caricamento eventi...</span>
</div>
<div id="cal-bar-tablet" class="cal-bar cal-bar-tablet"></div>
<div id="cal-bar-phone" class="cal-bar cal-bar-phone"></div>

<script>
(function () {
  // Un solo file: eventi.json ha gia' data, ora e competizione pronti, niente da ripulire.
  const EVENTI_URL = "https://raw.githubusercontent.com/aandroide/Livesoccer/master/livesoccertv/output/eventi.json";
  const PAGINA_CALENDARIO = "calendario/live_events/";
  const DURATA_PARTITA_MS = 2.5 * 60 * 60 * 1000;

  function badge(cls, label, count) {
    return `<span class="cal-badge ${cls}"><span class="dot"></span>${label} <strong>${count}</strong></span>`;
  }

  async function aggiornaBarre() {
    const desktop = document.getElementById("cal-bar-desktop");
    const tablet = document.getElementById("cal-bar-tablet");
    const phone = document.getElementById("cal-bar-phone");

    try {
      const res = await fetch(EVENTI_URL);
      if (!res.ok) throw new Error("HTTP " + res.status);
      const json = await res.json();
      const adesso = new Date();

      let totLive = 0;
      // Non e' detto che ci sia una sola "prossima partita": Serie A, B e C possono avere
      // piu' partite allo stesso identico orario, quindi si tiene l'orario piu' vicino e
      // quante partite lo condividono, non un singolo nome.
      let prossimoInizio = null;
      let prossimoTitolo = "";
      let prossimoOra = "";
      let prossimoConteggio = 0;
      const conteggi = { "Serie A": 0, "Serie B": 0, "Serie C": 0 };

      for (const ev of json.eventi || []) {
        const inizio = new Date(`${ev.data}T${ev.ora}:00`);
        const fine = new Date(inizio.getTime() + DURATA_PARTITA_MS);
        if (adesso >= inizio && adesso <= fine) {
          totLive++;
        } else if (conteggi[ev.competizione] !== undefined) {
          conteggi[ev.competizione]++;
          if (inizio > adesso) {
            if (!prossimoInizio || inizio < prossimoInizio) {
              prossimoInizio = inizio;
              prossimoTitolo = ev.titolo;
              prossimoOra = ev.ora;
              prossimoConteggio = 1;
            } else if (inizio.getTime() === prossimoInizio.getTime()) {
              prossimoConteggio++;
            }
          }
        }
      }

      const totale = totLive + conteggi["Serie A"] + conteggi["Serie B"] + conteggi["Serie C"];

      // Il pulsante principale punta sempre al punto piu' interessante in questo momento:
      // al live se c'e', altrimenti dritto alla prossima partita (o alle prossime, se piu'
      // di una comincia insieme) in assoluto, non solo alla sezione del suo campionato.
      let ctaHref = PAGINA_CALENDARIO;
      let ctaLabel = "Apri il calendario ›";
      if (totLive > 0) {
        ctaHref = `${PAGINA_CALENDARIO}#live`;
        ctaLabel = "🔴 Vai al live ›";
      } else if (prossimoInizio) {
        ctaHref = `${PAGINA_CALENDARIO}#prossimo`;
        ctaLabel = prossimoConteggio > 1
          ? `Prossimi (${prossimoConteggio}) · ${prossimoOra} ›`
          : `Prossima: ${prossimoTitolo} · ${prossimoOra} ›`;
      }
      const ctaHtml = `<a href="${ctaHref}" class="cal-btn cal-cta"><span class="cal-cta-text">${ctaLabel}</span></a>`;

      // Desktop: tutti i contatori affiancati
      desktop.innerHTML = `
        ${badge("cal-badge-live", "LIVE", totLive)}
        ${badge("cal-badge-a", "Serie A", conteggi["Serie A"])}
        ${badge("cal-badge-b", "Serie B", conteggi["Serie B"])}
        ${badge("cal-badge-c", "Serie C", conteggi["Serie C"])}
        <span class="cal-spacer"></span>
        ${ctaHtml}
      `;

      // Tablet: totale eventi, il pulsante intelligente, poi il menu a tendina per le categorie
      tablet.innerHTML = `
        <div class="cal-tablet-top">
          <span>⚽ <strong>${totale}</strong> partite nel calendario</span>
          ${badge("cal-badge-live", "", totLive)}
        </div>
        ${ctaHtml}
        <select class="cal-select" onchange="if(this.value) window.location.href=this.value;">
          <option value="">Scegli una categoria…</option>
          <option value="${PAGINA_CALENDARIO}#live">🔴 In corso ora (${totLive})</option>
          <option value="${PAGINA_CALENDARIO}#serie-a">🇮🇹 Serie A (${conteggi["Serie A"]})</option>
          <option value="${PAGINA_CALENDARIO}#serie-b">🇮🇹 Serie B (${conteggi["Serie B"]})</option>
          <option value="${PAGINA_CALENDARIO}#serie-c">🇮🇹 Serie C (${conteggi["Serie C"]})</option>
        </select>
      `;

      // Telefono: solo il numero di partite in corso ora, il pulsante fa il resto del lavoro
      phone.innerHTML = `
        ${badge("cal-badge-live", "LIVE", totLive)}
        ${ctaHtml}
      `;
    } catch (e) {
      const fallback = `<a href="${PAGINA_CALENDARIO}" class="cal-btn">⚽ Apri il calendario</a>`;
      desktop.innerHTML = fallback;
      tablet.innerHTML = fallback;
      phone.innerHTML = fallback;
      console.error("Errore conteggio calendario", e);
    }
  }

  aggiornaBarre();
  setInterval(aggiornaBarre, 60000);
})();
</script>

------

!!! tip "MandraKodi"
    MandraKodi è un addon che sfrutta dei BOT automatizzati per recuperare, in rete, link di flussi streaming da visualizzare con il player di Kodi e/o con un player esterno. <br>I BOT, per il recupero dei dati, utilizzano la tecnica del Web Scraping (estrazione di dati da un sito webper mezzo di programmi software che simulano la navigazione umana)

!!! warning "Qualità e stabilità"
    La qualità è la stabilità di questi link dipendono esclusivamente dal server che li trasmette.  <br>Molti server (soprattutto quelli che trasmettono eventi live sul web), quando le richieste aumentano, *abbassano la qualità* per *guadagnare sulla stabilità*. <br>Altri, invece, **raggiunta una soglia di banda**, cominciano a dare **problemi di blocchi continui** (il server non riesce a trasmettere la quantità necessaria di “informazioni” per permettere una visione fluida)

------

<div class="segnalazioni-widget">
  <div class="segnalazioni-info">
    <span class="cal-badge cal-badge-attesa"><span class="dot"></span>Attesa <strong id="cnt-attesa">-</strong></span>
    <span class="cal-badge cal-badge-live"><span class="dot"></span>Offline <strong id="cnt-offline">-</strong></span>
  </div>

  <div class="segnalazioni-actions">
    <!-- Pulsante Ricarica Dinamico -->
    <button id="btn-reload" onclick="caricaSegnalazioni()" title="Ricarica conteggio">
      🔄
    </button>

    <!-- Segnalazioni -->
    <a href="segnalazioni/ticket_issue/" class="cal-btn">Segnalazioni ›</a>
  </div>
</div>

<style>
/* Stesso linguaggio visivo delle barre del calendario qui sopra: badge col puntino colorato
   invece della pillola piena, cosi' i due riquadri in home sembrano un'unica famiglia. */
.segnalazioni-widget {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: linear-gradient(180deg, rgba(150,150,150,0.10), rgba(150,150,150,0.04));
  border: 1px solid rgba(150, 150, 150, 0.25);
  border-radius: 10px;
  padding: 12px 16px;
  margin: 15px 0;
  gap: 10px;
  flex-wrap: wrap;
  color: inherit;
}

.segnalazioni-info {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}

.cal-badge-attesa { color: #ffb74d; border-color: rgba(255, 160, 0, 0.35); }

.segnalazioni-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}

#btn-reload {
  background: rgba(150, 150, 150, 0.08);
  color: inherit;
  border: 1px solid rgba(150, 150, 150, 0.3);
  border-radius: 20px;
  padding: 6px 9px;
  cursor: pointer;
  font-size: 0.9em;
  line-height: 1;
}

#btn-reload:hover {
  background: rgba(150, 150, 150, 0.18);
}

.spin {
  animation: spin 0.8s linear infinite;
}
@keyframes spin { 100% { transform: rotate(360deg); } }
</style>

<script>
const SCRIPT_URL = "https://script.google.com/macros/s/AKfycbwTQJzxvLspR-1GdYh1wOXSLrF8h4TIeswEAIUJGtM9z1I4pIUZD3N_ANO2oewKmaI/exec";



function caricaSegnalazioni() {
  const btnReload = document.getElementById('btn-reload');
  const elemOffline = document.getElementById('cnt-offline');
  const elemAttesa = document.getElementById('cnt-attesa');

  if (btnReload) btnReload.classList.add('spin');
  elemOffline.innerText = "...";
  elemAttesa.innerText = "...";

  const cacheBuster = "&_ts=" + new Date().getTime();

  fetch(SCRIPT_URL + "?action=getOpen" + cacheBuster, { method: "GET" })
    .then(function(res) { return res.json(); })
    .then(function(data) {
      let countOffline = 0;
      let countAttesa = 0;

      if (Array.isArray(data)) {
        data.forEach(function(item) {
          const st = (item.stato || '').toString().trim().toUpperCase();
          if (st === "OFFLINE") countOffline++;
          if (st === "IN ATTESA") countAttesa++;
        });
      }
    
      elemOffline.innerText = countOffline;
      elemAttesa.innerText = countAttesa;
    })
    .catch(function(err) {
      console.error("Errore conteggio segnalazioni:", err);
      elemOffline.innerText = "Err";
      elemAttesa.innerText = "Err";
    })
    .finally(function() {
      if (btnReload) btnReload.classList.remove('spin');
    });

}

if (document.readyState === "complete" || document.readyState === "interactive") {
  setTimeout(caricaSegnalazioni, 1);
} else {
  document.addEventListener("DOMContentLoaded", caricaSegnalazioni);
}
</script>

[:material-cog-box: Installazione ](installazione/install.md){.md-button .md-button--primary} [:material-book-open-page-variant: Guide ](guide/tutorials.md){.md-button .md-button--primary} [:material-comment-question: FAQ ](faq/faq.md){.md-button .md-button--primary}
