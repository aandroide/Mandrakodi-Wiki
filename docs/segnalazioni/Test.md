<style>
  .calendar-container {
    font-family: var(--md-text-font-family, sans-serif);
    margin-top: 20px;
  }
  .calendar-section {
    margin-bottom: 30px;
  }
  .calendar-section h3 {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 12px;
    border-bottom: 2px solid var(--md-accent-fg-color, #007acc);
    padding-bottom: 6px;
  }
  .live-header {
    border-bottom-color: #e53935 !important;
    color: #e53935;
  }
  .calendar-table-wrapper {
    width: 100%;
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
  }
  .calendar-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.9em;
  }
  .calendar-table th, .calendar-table td {
    padding: 10px 12px;
    text-align: left;
    border-bottom: 1px solid var(--md-default-fg-color--lightest, #333);
  }
  .calendar-table th {
    background-color: var(--md-default-bg-color--panel, #1e1e1e);
    font-weight: bold;
  }
  .badge-live {
    background-color: #e53935;
    color: #fff;
    padding: 2px 6px;
    border-radius: 4px;
    font-size: 0.8em;
    font-weight: bold;
    text-transform: uppercase;
    animation: blink 1.5s infinite;
  }
  .badge-lega {
    background-color: var(--md-default-fg-color--lightest, #444);
    color: var(--md-default-fg-color, #fff);
    padding: 2px 6px;
    border-radius: 4px;
    font-size: 0.85em;
  }
  @keyframes blink {
    50% { opacity: 0.5; }
  }
  .empty-msg {
    font-style: italic;
    opacity: 0.7;
    padding: 10px 0;
  }
</style>

<div class="calendar-container">
  <div id="calendar-loading">⏳ Caricamento palinsesto in corso...</div>
  <div id="calendar-content" style="display: none;">

    <!-- Sezione Eventi LIVE -->
    <div class="calendar-section" id="section-live" style="display: none;">
      <h3 class="live-header">🔴 Eventi In Corso (LIVE)</h3>
      <div class="calendar-table-wrapper">
        <table class="calendar-table">
          <thead>
            <tr>
              <th>Lega</th>
              <th>Data / Ora</th>
              <th>Partita / Dettagli</th>
              <th>Stato</th>
            </tr>
          </thead>
          <tbody id="tbody-live"></tbody>
        </table>
      </div>
    </div>
    
    <!-- Sezione Serie A -->
    <div class="calendar-section">
      <h3>⚽ Serie A</h3>
      <div class="calendar-table-wrapper">
        <table class="calendar-table">
          <thead>
            <tr>
              <th>Data</th>
              <th>Ora</th>
              <th>Incontro</th>
            </tr>
          </thead>
          <tbody id="tbody-serie-a"></tbody>
        </table>
      </div>
    </div>
    
    <!-- Sezione Serie B -->
    <div class="calendar-section">
      <h3>⚽ Serie B</h3>
      <div class="calendar-table-wrapper">
        <table class="calendar-table">
          <thead>
            <tr>
              <th>Data</th>
              <th>Ora</th>
              <th>Incontro</th>
            </tr>
          </thead>
          <tbody id="tbody-serie-b"></tbody>
        </table>
      </div>
    </div>
    
    <!-- Sezione Serie C -->
    <div class="calendar-section">
      <h3>⚽ Serie C</h3>
      <div class="calendar-table-wrapper">
        <table class="calendar-table">
          <thead>
            <tr>
              <th>Data</th>
              <th>Ora</th>
              <th>Incontro</th>
            </tr>
          </thead>
          <tbody id="tbody-serie-c"></tbody>
        </table>
      </div>
    </div>

  </div>
</div>

<script>
(function() {
  const BASE_COMMIT = "93770da86eb3d6bdfcd4f4df1828cafef487afb0";
  const SOURCES = [
    { key: "serie-a", name: "Serie A", url: `https://raw.githubusercontent.com/campipaolo/Livesoccer/${BASE_COMMIT}/livesoccertv/output/serie-a.json` },
    { key: "serie-b", name: "Serie B", url: `https://raw.githubusercontent.com/campipaolo/Livesoccer/${BASE_COMMIT}/livesoccertv/output/serie-b.json` },
    { key: "serie-c", name: "Serie C", url: `https://raw.githubusercontent.com/campipaolo/Livesoccer/${BASE_COMMIT}/livesoccertv/output/serie-c.json` }
  ];

  const MESI = {
    "gennaio": 0, "febbraio": 1, "marzo": 2, "aprile": 3, "maggio": 4, "giugno": 5,
    "luglio": 6, "agosto": 7, "settembre": 8, "ottobre": 9, "novembre": 10, "dicembre": 11
  };

  // Helper per convertire stringhe di data/ora in timestamp per l'ordinamento
  function parseMatchDate(dataStr, orarioStr) {
    try {
      if (!dataStr) return new Date(0);
      const match = dataStr.toLowerCase().match(/(\d{1,2})\s+([a-z]+)(?:\s+(\d{4}))?/);
      if (match) {
        const giorno = parseInt(match[1], 10);
        const mese = MESI[match[2]] !== undefined ? MESI[match[2]] : 0;
        const anno = match[3] ? parseInt(match[3], 10) : new Date().getFullYear();
        
        let ora = 0, minuto = 0;
        if (orarioStr && orarioStr.includes(":")) {
          const parts = orarioStr.split(":");
          ora = parseInt(parts[0], 10);
          minuto = parseInt(parts[1], 10);
        }
        return new Date(anno, mese, giorno, ora, minuto);
      }
    } catch (e) {
      console.error("Errore parsing data:", e);
    }
    return new Date(0);
  }

  async function loadCalendars() {
    const liveMatches = [];
    
    for (const src of SOURCES) {
      const tbody = document.getElementById(`tbody-${src.key}`);
      try {
        const res = await fetch(src.url);
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = await res.json();
        
        let matches = Array.isArray(data) ? data : (data.partite || data.events || []);
    
        // Estrai gli eventuali match in LIVE
        const regularMatches = [];
        matches.forEach(m => {
          const isLive = (m.stato && m.stato.toLowerCase().includes("live")) || 
                         (m.dettagli && m.dettagli.toLowerCase().includes("live")) ||
                         (m.orario && m.orario.toLowerCase().includes("live"));
          
          const dt = parseMatchDate(m.data || m.date, m.orario || m.time);
          const item = { ...m, legaNome: src.name, timestamp: dt.getTime() };
    
          if (isLive) {
            liveMatches.push(item);
          } else {
            regularMatches.push(item);
          }
        });
    
        // Ordinamento Cronologico
        regularMatches.sort((a, b) => a.timestamp - b.timestamp);
    
        // Renderizza la tabella di categoria
        if (regularMatches.length === 0) {
          tbody.innerHTML = '<tr><td colspan="3" class="empty-msg">Nessun evento in programma.</td></tr>';
        } else {
          tbody.innerHTML = regularMatches.map(m => `
            <tr>
              <td>${m.data || '-'}</td>
              <td><strong>${m.orario || '-'}</strong></td>
              <td>${m.dettagli || m.partita || m.match || '-'}</td>
            </tr>
          `).join('');
        }
    
      } catch (err) {
        console.error(`Errore caricamento ${src.name}:`, err);
        tbody.innerHTML = '<tr><td colspan="3" class="empty-msg" style="color:#f44336;">Impossibile caricare i dati.</td></tr>';
      }
    }
    
    // Renderizza la Sezione LIVE se sono presenti match in corso
    if (liveMatches.length > 0) {
      liveMatches.sort((a, b) => a.timestamp - b.timestamp);
      const tbodyLive = document.getElementById("tbody-live");
      tbodyLive.innerHTML = liveMatches.map(m => `
        <tr>
          <td><span class="badge-lega">${m.legaNome}</span></td>
          <td>${m.data || ''} ${m.orario || ''}</td>
          <td><strong>${m.dettagli || m.partita || m.match || '-'}</strong></td>
          <td><span class="badge-live">IN CORSO</span></td>
        </tr>
      `).join('');
      document.getElementById("section-live").style.display = "block";
    }
    
    document.getElementById("calendar-loading").style.display = "none";
    document.getElementById("calendar-content").style.display = "block";
  }

  if (document.readyState === "complete" || document.readyState === "interactive") {
    setTimeout(loadCalendars, 1);
  } else {
    document.addEventListener("DOMContentLoaded", loadCalendars);
  }
})();
</script>
