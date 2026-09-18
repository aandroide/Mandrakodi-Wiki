# **Benvenuti nella Wiki ufficiale di MandraKodi**

![icon](/home/server/Documenti/Mandrakodi-Wiki/docs/images/icon.gif)

[:material-face-agent: Assistenza](ask_help.md){ .md-button .md-button--primary } 

<div class="segnalazioni-actions">
    <!-- Pulsante Ricarica Dinamico -->
    <button id="btn-reload" onclick="caricaSegnalazioni()" title="Ricarica conteggio">
      🔄
    </button>

<div class="segnalazioni-widget">
  <div class="segnalazioni-info">
    <span class="badge badge-offline">🔴 FONTI OFFLINE: <strong id="cnt-offline">-</strong></span>
    <span class="badge badge-attesa">🟡 SEGNALAZIONI IN ATTESA: <strong id="cnt-attesa">-</strong></span>
  </div>




    <!-- Pulsante per aprire la pagina delle Segnalazioni completa -->
    <a href="../segnalazioni/ticket_issue/" class="md-button md-button--primary">
      Elenco Segnalazioni
    </a>
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

------

!!! tip "MandraKodi"
    MandraKodi è un addon che sfrutta dei BOT automatizzati per recuperare, in rete, link di flussi streaming da visualizzare con il player di Kodi e/o con un player esterno. <br>I BOT, per il recupero dei dati, utilizzano la tecnica del Web Scraping (estrazione di dati da un sito webper mezzo di programmi software che simulano la navigazione umana)

!!! warning "Qualità e stabilità"
    La qualità è la stabilità di questi link dipendono esclusivamente dal server che li trasmette.  <br>Molti server (soprattutto quelli che trasmettono eventi live sul web), quando le richieste aumentano, *abbassano la qualità* per *guadagnare sulla stabilità*. <br>Altri, invece, **raggiunta una soglia di banda**, cominciano a dare **problemi di blocchi continui** (il server non riesce a trasmettere la quantità necessaria di “informazioni” per permettere una visione fluida)

------

[:material-cog-box: Installazione ](installazione/install.md){.md-button .md-button--primary} [:material-book-open-page-variant: Guide ](guide/tutorials.md){.md-button .md-button--primary} [:material-comment-question: FAQ ](faq/faq.md){.md-button .md-button--primary}

