<div id="lista-partite">Caricamento partite in corso...</div>

<script>
async function caricaPartite() {
  const container = document.getElementById('lista-partite');
  const urlAssoluto = window.location.origin + '/Mandrakodi-Wiki/partite.json';

  try {
    const res = await fetch(urlAssoluto);
    
    if (!res.ok) {
      throw new Error(`File non trovato (HTTP ${res.status})`);
    }
    
    const data = await res.json();
    
    if (!data.partite || data.partite.length === 0) {
      container.innerHTML = "<p>Nessun evento trovato per le leghe selezionate.</p>";
      return;
    }
    
    let html = '';
    if (data.ultimo_aggiornamento) {
      html += `<p style="font-size: 0.85em; opacity: 0.7;"><i>Ultimo aggiornamento: ${data.ultimo_aggiornamento}</i></p>`;
    }
    
    html += '<ul style="line-height: 1.8; list-style-type: none; padding-left: 0;">';
    
    const oraAttuale = new Date();
    const minutiAttuali = oraAttuale.getHours() * 60 + oraAttuale.getMinutes();
    
    data.partite.forEach(p => {
      let isLiveOra = p.is_live;
    
      // Se non è segnata già come terminata e ha un orario, calcola la finestra LIVE (orario inizio -> +115 min)
      if (!p.is_finished && p.orario) {
        const partiOrario = p.orario.split(':');
        if (partiOrario.length === 2) {
          const minutiInizio = parseInt(partiOrario[0], 10) * 60 + parseInt(partiOrario[1], 10);
          const minutiFine = minutiInizio + 115; // Un match dura circa 115 minuti
          
          if (minutiAttuali >= minutiInizio && minutiAttuali <= minutiFine) {
            isLiveOra = True;
          }
        }
      }
    
      // Badge LIVE solo se la partita è effettivamente in corso adesso
      const badgeLive = isLiveOra 
        ? '<span style="background-color: #d9534f; color: white; padding: 2px 6px; border-radius: 4px; font-weight: bold; font-size: 0.8em; margin-right: 6px;">🔴 LIVE</span>' 
        : '';
    
      html += `<li style="margin-bottom: 10px; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 6px;">
        ${badgeLive}
        <strong>[${p.lega}]</strong>: ${p.dettagli} 
        <a href="${p.url}" target="_blank" rel="noopener" style="font-size: 0.85em; margin-left: 6px;">🔗 Fonte</a>
      </li>`;
    });
    
    html += '</ul>';
    container.innerHTML = html;

  } catch (err) {
    console.error("Errore recupero file JSON:", err);
    container.innerHTML = `<p style="color: red;">Impossibile caricare il palinsesto: ${err.message}</p>`;
  }
}

document.addEventListener("DOMContentLoaded", caricaPartite);
</script>
