<div id="lista-partite">Caricamento partite in corso...</div>

<script>
async function caricaPartite() {
  const container = document.getElementById('lista-partite');

  // Costruisce l'URL assoluto puntando sempre alla radice /Mandrakodi-Wiki/partite.json
  const urlAssoluto = window.location.origin + '/Mandrakodi-Wiki/partite.json';

  try {
    const res = await fetch(urlAssoluto);
    
    if (!res.ok) {
      throw new Error(`File non trovato (HTTP ${res.status})`);
    }
    
    const contentType = res.headers.get("content-type");
    if (contentType && contentType.includes("text/html")) {
      throw new Error("MkDocs ha restituito una pagina 404 invece del file JSON.");
    }
    
    const data = await res.json();
    
    if (!data.partite || data.partite.length === 0) {
      container.innerHTML = "<p>Nessuna partita trovata per oggi.</p>";
      return;
    }
    
    let html = '<ul style="line-height: 1.6;">';
    data.partite.forEach(p => {
      html += `<li>${p.raw_data}</li>`;
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
