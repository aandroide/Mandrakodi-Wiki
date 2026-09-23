



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
  // Un solo file: eventi.json ha gia' data, ora e competizione pronti, niente da ripulire.
  const EVENTI_URL = "https://raw.githubusercontent.com/campipaolo/Livesoccer/master/livesoccertv/output/eventi.json";
  const PAGINA_CALENDARIO = "calendario/live_events/";
  const DURATA_PARTITA_MS = 2.5 * 60 * 60 * 1000;


  function badge(cls, label, count) {
    return `<span class="cal-badge ${cls}"><span class="dot"></span>${label} <strong>${count}</strong></span>`;
  }

  async function aggiornaBarra() {
    const bar = document.getElementById("cal-bar");
    try {
      const res = await fetch(EVENTI_URL);
      if (!res.ok) throw new Error("HTTP " + res.status);
      const json = await res.json();
      const adesso = new Date();

      let totLive = 0;
      // "In arrivo" e' un orario, non una singola partita: Serie A, B e C possono avere
      // piu' partite insieme, quindi si conta quante condividono l'orario piu' vicino.
      let prossimoInizio = null;
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
              prossimoConteggio = 1;
            } else if (inizio.getTime() === prossimoInizio.getTime()) {
              prossimoConteggio++;
            }
          }
        }
      }
    
      const totale = totLive + conteggi["Serie A"] + conteggi["Serie B"] + conteggi["Serie C"];
    
      // Un widget solo, uguale su desktop e telefono: il totale e il live in alto, sotto
      // il menu a tendina per saltare a una categoria (o a "In arrivo") e, a fianco, il
      // pulsante che apre comunque la pagina intera del calendario.
      bar.innerHTML = `
        <div class="cal-bar-top">
          <span>⚽ <strong>${totale}</strong> partite nel calendario</span>
          ${badge("cal-badge-live", "Live", totLive)}
        </div>
        <div class="cal-bar-row">
          <select class="cal-select" onchange="if(this.value) window.location.href=this.value;">
            <option value="">Scegli una categoria…</option>
            <option value="${PAGINA_CALENDARIO}#live">🔴 Live (${totLive})</option>
            <option value="${PAGINA_CALENDARIO}#prossimo">🟡 In arrivo (${prossimoConteggio})</option>
            <option value="${PAGINA_CALENDARIO}#serie-a">🇮🇹 Serie A (${conteggi["Serie A"]})</option>
            <option value="${PAGINA_CALENDARIO}#serie-b">🇮🇹 Serie B (${conteggi["Serie B"]})</option>
            <option value="${PAGINA_CALENDARIO}#serie-c">🇮🇹 Serie C (${conteggi["Serie C"]})</option>
          </select>
          <a href="${PAGINA_CALENDARIO}" class="cal-btn">Apri calendario ›</a>
        </div>
      `;
    } catch (e) {
      bar.innerHTML = `<a href="${PAGINA_CALENDARIO}" class="cal-btn">⚽ Apri il calendario</a>`;
      console.error("Errore conteggio calendario", e);
    }
  }

  aggiornaBarra();
  setInterval(aggiornaBarra, 60000);
})();
</script>

------

