<style>
  .calendar-container {
    max-width: 800px;
    margin: 20px auto;
    font-family: Arial, sans-serif;
  }
  .calendar-tabs {
    display: flex;
    gap: 8px;
    margin-bottom: 15px;
    flex-wrap: wrap;
  }
  .tab-btn {
    padding: 8px 16px;
    background: #252526;
    color: #fff;
    border: 1px solid #444;
    border-radius: 6px;
    cursor: pointer;
    font-weight: bold;
    font-size: 14px;
    transition: background 0.2s;
  }
  .tab-btn:hover { background: #333; }
  .tab-btn.active {
    background: #107c41;
    border-color: #107c41;
  }
  .tab-btn.live-btn {
    background: #b71c1c;
    border-color: #d32f2f;
  }
  .tab-btn.live-btn.active {
    background: #d32f2f;
  }

  .match-card {
    background: #1e1e1e;
    border: 1px solid #333;
    border-radius: 8px;
    padding: 12px 16px;
    margin-bottom: 10px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 10px;
  }
  .match-info { flex-grow: 1; }
  .match-teams { font-weight: bold; font-size: 15px; color: #fff; }
  .match-details { font-size: 13px; color: #aaa; margin-top: 4px; }

  .badge {
    padding: 4px 8px;
    border-radius: 4px;
    font-size: 12px;
    font-weight: bold;
    text-transform: uppercase;
  }
  .badge-live { background: #d32f2f; color: #fff; animation: pulse 1.5s infinite; }
  .badge-upcoming { background: #0288d1; color: #fff; }
  .badge-finished { background: #555; color: #ccc; }

  @keyframes pulse {
    0% { opacity: 1; }
    50% { opacity: 0.5; }
    100% { opacity: 1; }
  }

  @media screen and (max-width: 600px) {
    .match-card {
      flex-direction: column;
      align-items: flex-start;
    }
  }
</style>

<div class="calendar-container">
  <!-- Pulsanti Filtro/Categoria -->
  <div class="calendar-tabs">
    <button class="tab-btn live-btn active" onclick="filtracategoria('Live')">🔴 LIVE (<span id="count-live">0</span>)</button>
    <button class="tab-btn" onclick="filtracategoria('Serie A')">Serie A</button>
    <button class="tab-btn" onclick="filtracategoria('Serie B')">Serie B</button>
    <button class="tab-btn" onclick="filtracategoria('Serie C')">Serie C</button>
  </div>

  <!-- Contenitore Lista Eventi -->
  <div id="lista-eventi">
    <div style="text-align: center; padding: 20px; color: #aaa;">Caricamento palinsesto in corso...</div>
  </div>
</div>

<script>
(function() {
  // URLs grezzi dei tuoi file JSON su GitHub (raw.githubusercontent.com)
  const SOURCES = [
    { lega: "Serie A", url: "https://raw.githubusercontent.com/campipaolo/Livesoccer/93770da86eb3d6bdfcd4f4df1828cafef487afb0/livesoccertv/output/serie-a.json" },
    { lega: "Serie B", url: "https://raw.githubusercontent.com/campipaolo/Livesoccer/93770da86eb3d6bdfcd4f4df1828cafef487afb0/livesoccertv/output/serie-b.json" },
    { lega: "Serie C", url: "https://raw.githubusercontent.com/campipaolo/Livesoccer/93770da86eb3d6bdfcd4f4df1828cafef487afb0/livesoccertv/output/serie-c.json" }
  ];

  let tuttiEventi = [];
  let categoriaAttuale = "Live";

  async function caricaDati() {
    try {
      const richieste = SOURCES.map(async src => {
        const res = await fetch(src.url);
        if (!res.ok) return [];
        const data = await res.json();
        // Aggiunge la categoria 'lega' ad ogni oggetto del file JSON
        return (data.partite || data || []).map(item => ({ ...item, lega: src.lega }));
      });

      const risultati = await Promise.all(richieste);
      tuttiEventi = risultati.flat();
    
      // Normalizzazione e calcolo timestamp per l'ordinamento cronologico
      tuttiEventi.forEach(ev => {
        ev.parsedDate = generaTimestamp(ev.date || ev.data, ev.time || ev.orario);
        ev.isLive = (ev.status || '').toLowerCase() === 'live' || (ev.stato || '').toLowerCase() === 'live';
      });
    
      // Ordinamento cronologico crescente
      tuttiEventi.sort((a, b) => a.parsedDate - b.parsedDate);
    
      // Aggiorna contatore badge LIVE
      const liveCount = tuttiEventi.filter(e => e.isLive).length;
      document.getElementById("count-live").textContent = liveCount;
    
      render();
    } catch (err) {
      console.error("Errore nel caricamento dei JSON:", err);
      document.getElementById("lista-eventi").innerHTML = 
        '<div style="color: #ff5252; text-align: center; padding: 15px;">⚠️ Impossibile caricare il palinsesto.</div>';
    }
  }

  function generaTimestamp(dataStr, oraStr) {
    if (!dataStr) return new Date(0);
    // Tenta di interpretare la data o assegna un valore predefinito
    const isoString = oraStr ? `${dataStr}T${oraStr}:00` : dataStr;
    const d = new Date(isoString);
    return isNaN(d.getTime()) ? new Date() : d;
  }

  window.filtracategoria = function(cat) {
    categoriaAttuale = cat;
    document.querySelectorAll('.tab-btn').forEach(btn => {
      btn.classList.remove('active');
      if (btn.textContent.includes(cat)) btn.classList.add('active');
    });
    render();
  };

  function render() {
    const container = document.getElementById("lista-eventi");
    container.innerHTML = "";

    let filtrati = [];
    if (categoriaAttuale === "Live") {
      filtrati = tuttiEventi.filter(e => e.isLive);
    } else {
      filtrati = tuttiEventi.filter(e => e.lega === categoriaAttuale);
    }
    
    if (filtrati.length === 0) {
      container.innerHTML = `<div style="text-align: center; padding: 20px; color: #888;">Nessun evento disponibile per la sezione <strong>${categoriaAttuale}</strong>.</div>`;
      return;
    }
    
    filtrati.forEach(ev => {
      const isLive = ev.isLive;
      const statusClass = isLive ? 'badge-live' : (ev.status === 'finished' ? 'badge-finished' : 'badge-upcoming');
      const statusText = isLive ? 'LIVE' : (ev.time || ev.orario || 'Programmata');
    
      const card = document.createElement("div");
      card.className = "match-card";
      card.innerHTML = `
        <div class="match-info">
          <div class="match-teams">${ev.teams || ev.partita || ev.dettagli || 'Partita non specificata'}</div>
          <div class="match-details">
            🏆 <strong>${ev.lega}</strong> | 📅 ${ev.date || ev.data || ''} ${ev.time || ev.orario ? '- ' + (ev.time || ev.orario) : ''}
            ${ev.channels ? ' | 📺 ' + (Array.isArray(ev.channels) ? ev.channels.join(', ') : ev.channels) : ''}
          </div>
        </div>
        <div>
          <span class="badge ${statusClass}">${statusText}</span>
        </div>
      `;
      container.appendChild(card);
    });
  }

  // Caricamento iniziale
  caricaDati();
})();
</script>
