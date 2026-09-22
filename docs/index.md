# **Benvenuti nella Wiki ufficiale di MandraKodi**

![icon](images/icon.gif)

[:material-face-agent: Assistenza](ask_help.md){ .md-button .md-button--primary } 

------

!!! tip "MandraKodi"
    MandraKodi è un addon che sfrutta dei BOT automatizzati per recuperare, in rete, link di flussi streaming da visualizzare con il player di Kodi e/o con un player esterno. <br>I BOT, per il recupero dei dati, utilizzano la tecnica del Web Scraping (estrazione di dati da un sito webper mezzo di programmi software che simulano la navigazione umana)

!!! warning "Qualità e stabilità"
    La qualità è la stabilità di questi link dipendono esclusivamente dal server che li trasmette.  <br>Molti server (soprattutto quelli che trasmettono eventi live sul web), quando le richieste aumentano, *abbassano la qualità* per *guadagnare sulla stabilità*. <br>Altri, invece, **raggiunta una soglia di banda**, cominciano a dare **problemi di blocchi continui** (il server non riesce a trasmettere la quantità necessaria di “informazioni” per permettere una visione fluida)

------

[:material-cog-box: Installazione ](installazione/install.md){.md-button .md-button--primary} [:material-book-open-page-variant: Guide ](guide/tutorials.md){.md-button .md-button--primary} [:material-comment-question: FAQ ](faq/faq.md){.md-button .md-button--primary}



<div class="segnalazioni-widget">
  <div class="segnalazioni-info">
    <span class="badge badge-offline">🔴 FONTI OFFLINE: <strong id="cnt-offline">-</strong></span>
    <span class="badge badge-attesa">🟡 SEGNALAZIONI IN ATTESA: <strong id="cnt-attesa">-</strong></span>
  </div>



  <div class="segnalazioni-actions">
    <!-- Pulsante Ricarica Dinamico -->
    <button id="btn-reload" onclick="caricaSegnalazioni()" title="Ricarica conteggio">
      🔄
    </button>



    <!-- Visualizzare/Inviare Segnalazioni -->
    <a href="segnalazioni/ticket_issue/" class="btn-apri">Visualizzare/Inviare Segnalazioni ➔</a>

  </div>
</div>

<style>
.segnalazioni-widget {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background-color: #252526;
  border: 1px solid #444;
  border-radius: 8px;
  padding: 8px 14px;
  margin: 15px 0;
  gap: 10px;
  flex-wrap: wrap;
  color: #fff;
}



.segnalazioni-info {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 0.9em;
}

.badge {
  padding: 4px 10px;
  border-radius: 20px;
  font-weight: bold;
  background-color: #1e1e1e;
}

.badge-offline { border: 1px solid #d32f2f; color: #ff5252; }
.badge-attesa { border: 1px solid #ffa000; color: #ffb74d; }

.segnalazioni-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}

#btn-reload {
  background: #333;
  color: #fff;
  border: 1px solid #555;
  border-radius: 4px;
  padding: 4px 8px;
  cursor: pointer;
  font-size: 0.9em;
  transition: transform 0.2s;
}

#btn-reload:hover {
  background-color: #444;
}

.btn-apri {
  background-color: #107c41;
  color: #fff !important;
  padding: 6px 12px;
  border-radius: 4px;
  text-decoration: none !important;
  font-size: 0.85em;
  font-weight: bold;
}

.btn-apri:hover {
  opacity: 0.9;
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
}

.cal-btn-badge:hover { background: rgba(150, 150, 150, 0.22); }

.cal-btn-live {
  background: rgba(224, 0, 0, 0.1);
  color: #d00000;
  border-color: rgba(224, 0, 0, 0.3);
}

.cal-btn-live:hover { background: rgba(224, 0, 0, 0.2); }

.cal-count {
  background: rgba(150, 150, 150, 0.2);
  color: inherit;
  font-size: 12px;
  padding: 2px 7px;
  border-radius: 10px;
  font-weight: bold;
}

.cal-btn-live .cal-count { background: #d00000; color: #ffffff; }
.cal-loading-dots { font-size: 13px; opacity: 0.6; }
</style>

<div class="cal-bar-summary" id="cal-summary-bar">
  <span class="cal-loading-dots">⏳ Caricamento eventi...</span>
</div>

<script>
(function () {
  // Un solo file: eventi.json ha gia' data, ora e competizione pronti, niente da ripulire.
  const EVENTI_URL = "https://raw.githubusercontent.com/aandroide/Livesoccer/master/livesoccertv/output/eventi.json";
  const PAGINA_CALENDARIO = "calendario/live_events/";
  const DURATA_PARTITA_MS = 2.5 * 60 * 60 * 1000;

  async function contaEventi() {
    const container = document.getElementById("cal-summary-bar");
    try {
      const res = await fetch(EVENTI_URL);
      if (!res.ok) throw new Error("HTTP " + res.status);
      const json = await res.json();
      const adesso = new Date();

      let totLive = 0;
      const conteggi = { "Serie A": 0, "Serie B": 0, "Serie C": 0 };

      for (const ev of json.eventi || []) {
        const inizio = new Date(`${ev.data}T${ev.ora}:00`);
        const fine = new Date(inizio.getTime() + DURATA_PARTITA_MS);
        if (adesso >= inizio && adesso <= fine) {
          totLive++;
        } else if (conteggi[ev.competizione] !== undefined) {
          conteggi[ev.competizione]++;
        }
      }

      container.innerHTML = `
        <a href="${PAGINA_CALENDARIO}#live" class="cal-btn-badge cal-btn-live">
          🔴 LIVE <span class="cal-count">${totLive}</span>
        </a>
        <a href="${PAGINA_CALENDARIO}#serie-a" class="cal-btn-badge">
          🇮🇹 Serie A <span class="cal-count">${conteggi["Serie A"]}</span>
        </a>
        <a href="${PAGINA_CALENDARIO}#serie-b" class="cal-btn-badge">
          🇮🇹 Serie B <span class="cal-count">${conteggi["Serie B"]}</span>
        </a>
        <a href="${PAGINA_CALENDARIO}#serie-c" class="cal-btn-badge">
          🇮🇹 Serie C <span class="cal-count">${conteggi["Serie C"]}</span>
        </a>
      `;
    } catch (e) {
      container.innerHTML = `<a href="${PAGINA_CALENDARIO}" class="cal-btn-badge">⚽ Apri il calendario</a>`;
      console.error("Errore conteggio calendario", e);
    }
  }

  contaEventi();
})();
</script>

