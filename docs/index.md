# **Benvenuti nella Wiki ufficiale di MandraKodi**

![icon](images/icon.gif)



<style>
.cal-bar {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  margin: 15px 0;
  background: linear-gradient(180deg, rgba(150,150,150,0.10), rgba(150,150,150,0.04));
  border: 1px solid rgba(150, 150, 150, 0.25);
  border-radius: 10px;
  padding: 12px 16px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.cal-bar-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  flex-wrap: wrap;
  font-size: 14px;
}

.cal-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 6px 13px;
  border-radius: 20px;
  font-weight: 700;
  font-size: 13.5px;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(150, 150, 150, 0.3);
  color: inherit;
  white-space: nowrap;
}

.cal-badge .dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: currentColor;
  display: inline-block;
}

.cal-badge-live { color: #ff6659; border-color: rgba(224, 0, 0, 0.35); }
.cal-badge-attesa { color: #ffb74d; border-color: rgba(255, 160, 0, 0.35); }
.cal-badge strong { color: inherit; }

.cal-bar-row {
  display: flex;
  gap: 8px;
}

.cal-select {
  flex: 1;
  min-width: 0;
  background: rgba(150, 150, 150, 0.08);
  border: 1px solid rgba(150, 150, 150, 0.3);
  color: inherit;
  border-radius: 8px;
  padding: 9px 10px;
  font-size: 14px;
  font-weight: 600;
}

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

.cal-loading { font-size: 13px; opacity: 0.6; }
</style>

<div id="cal-bar" class="cal-bar">
  <span class="cal-loading">⏳ Caricamento eventi...</span>
</div>

<script>
(function () {
  // Un solo file con tutti gli sport, gia' diviso in cartelle (Oggi, Motori, Calcio, ...)
  const CALENDARIO_URL = "https://raw.githubusercontent.com/aandroide/Livesoccer/refs/heads/master/output/calendario_sport.json";
  const PAGINA = "calendario/sport/";
  const DURATA = { prove: 75, qualifiche: 75, sprint_quali: 60, sprint: 60, gara: 150, evento: 150 };
  const ICONE = { "Oggi": "📅", "Motori": "🏎️", "Calcio": "⚽", "Tennis": "🎾", "Basket": "🏀", "Volley": "🏐", "Altri sport": "🏅" };
  const slug = s => s.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "").replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");

  function badge(cls, label, count) {
    return `<span class="cal-badge ${cls}"><span class="dot"></span>${label} <strong>${count}</strong></span>`;
  }

  async function aggiornaBarra() {
    const bar = document.getElementById("cal-bar");
    try {
      const res = await fetch(CALENDARIO_URL, { cache: "no-store" });
      if (!res.ok) throw new Error("HTTP " + res.status);
      const json = await res.json();
      const adesso = new Date();
      let live = 0;
      for (const cart of json.cartelle || []) {
        if (cart.nome === "Oggi") continue;
        for (const sub of cart.sottocartelle || []) for (const ev of sub.eventi) {
          const inizio = new Date(ev.inizio);
          const fine = new Date(inizio.getTime() + (DURATA[ev.sessione] || 135) * 60000);
          if (adesso >= inizio && adesso <= fine) live++;
        }
      }
      const opzioni = (json.cartelle || []).map(c =>
        `<option value="${PAGINA}#${slug(c.nome)}">${ICONE[c.nome] || ""} ${c.nome} (${c.totale})</option>`).join("");

      bar.innerHTML = `
        <div class="cal-bar-top">
          <span>🏆 <strong>${json.totale || 0}</strong> eventi nel calendario</span>
          ${badge("cal-badge-live", "Live", live)}
        </div>
        <div class="cal-bar-row">
          <select class="cal-select" onchange="if(this.value) window.location.href=this.value;">
            <option value="">Scegli una categoria…</option>
            <option value="${PAGINA}#live">🔴 Live (${live})</option>
            ${opzioni}
          </select>
          <a href="${PAGINA}" class="cal-btn">Apri calendario ›</a>
        </div>
      `;
    } catch (e) {
      bar.innerHTML = `<a href="${PAGINA}" class="cal-btn">🏆 Apri il calendario</a>`;
      console.error("Errore calendario", e);
    }
  }

  aggiornaBarra();
  setInterval(aggiornaBarra, 60000);
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

[:material-cog-box: Installazione ](installazione/install.md){.md-button .md-button--primary} [:material-book-open-page-variant: Guide ](guide/tutorials.md){.md-button .md-button--primary} [:material-comment-question: FAQ ](faq/faq.md){.md-button .md-button--primary} [:material-face-agent: Assistenza](ask_help.md){ .md-button .md-button--primary } 
