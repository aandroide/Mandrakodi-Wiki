<div id="lista-partite">Caricamento partite in corso...</div>

<script>
async function caricaPartite() {
  const container = document.getElementById('lista-partite');
  try {
    // Percorso relativo al file JSON nella cartella docs
    const res = await fetch('./partite.json');
    const data = await res.json();

    if (!data.partite || data.partite.length === 0) {
      container.innerHTML = "<p>Nessuna partita trovata per oggi.</p>";
      return;
    }
    
    let html = '<ul>';
    data.partite.forEach(p => {
      html += `<li>${p.raw_data}</li>`;
    });
    html += '</ul>';
    container.innerHTML = html;

  } catch (err) {
    console.error("Errore recupero file JSON:", err);
    container.innerHTML = "<p>Impossibile caricare il palinsesto.</p>";
  }
}

document.addEventListener("DOMContentLoaded", caricaPartite);
</script>
