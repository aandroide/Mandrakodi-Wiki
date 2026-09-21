# Palinsesto Partite

<div id="lista-partite">Caricamento palinsesto completo in corso...</div>

<script>
async function caricaPartite() {
  const container = document.getElementById('lista-partite');
  const urlAssoluto = window.location.origin + '/Mandrakodi-Wiki/partite.json';

  try {
    const res = await fetch(urlAssoluto + '?v=' + new Date().getTime());
    
    if (!res.ok) {
      throw new Error(`File non trovato (HTTP ${res.status})`);
    }
    
    const data = await res.json();
    
    if (!data.partite || data.partite.length === 0) {
      container.innerHTML = "<p>Nessun evento disponibile nel palinsesto.</p>";
      return;
    }
    
    let html = '';
    if (data.ultimo_aggiornamento) {
      html += `<p style="font-size: 0.85em; opacity: 0.7;"><i>Ultimo aggiornamento: ${data.ultimo_aggiornamento}</i></p>`;
    }
    
    html += '<ul style="line-height: 1.8; list-style-type: none; padding-left: 0;">';
    
    data.partite.forEach(p => {
      html += `<li style="margin-bottom: 10px; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 6px;">
        <strong>[${p.lega}]</strong> ${p.dettagli} 
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
