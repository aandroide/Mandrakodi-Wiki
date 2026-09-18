<div class="segnalazioni-widget">
  <div class="segnalazioni-info">
    <span class="badge badge-offline">🔴 OFFLINE: <strong id="cnt-offline">-</strong></span>
    <span class="badge badge-attesa">🟡 In Attesa: <strong id="cnt-attesa">-</strong></span>
  </div>

  <div class="segnalazioni-actions">
    <!-- Pulsante Ricarica Dinamico -->
    <button id="btn-reload" onclick="caricaSegnalazioni()" title="Ricarica conteggio">
      🔄
    </button>

    <!-- Pulsante per aprire la pagina delle Segnalazioni completa -->
    <a href="segnalazioni/" class="btn-apri">
      Apri Segnalazioni ➔
    </a>
  </div>
</div>

<style>
/* Stili per la riga compatta */
.segnalazioni-widget {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background-color: var(--md-code-bg-color, #f5f5f5);
  border: 1px solid var(--md-typeset-table-color, #e0e0e0);
  border-radius: 8px;
  padding: 8px 14px;
  margin: 15px 0;
  gap: 10px;
  flex-wrap: wrap;
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
  font-weight: 500;
  background-color: rgba(0,0,0,0.05);
}

.badge-offline { border: 1px solid #e53935; color: #c62828; }
.badge-attesa { border: 1px solid #fdd835; color: #f57f17; }

.segnalazioni-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}

#btn-reload {
  background: transparent;
  border: 1px solid var(--md-typeset-table-color, #ccc);
  border-radius: 4px;
  padding: 4px 8px;
  cursor: pointer;
  font-size: 0.9em;
  transition: transform 0.2s;
}

#btn-reload:hover {
  background-color: rgba(0,0,0,0.05);
}

.btn-apri {
  background-color: var(--md-typeset-a-color, #007bc7);
  color: #fff !important;
  padding: 4px 12px;
  border-radius: 4px;
  text-decoration: none !important;
  font-size: 0.85em;
  font-weight: bold;
}

.btn-apri:hover {
  opacity: 0.9;
}

/* Animazione di rotazione per il refresh */
.spin {
  animation: spin 0.8s linear infinite;
}
@keyframes spin { 100% { transform: rotate(360deg); } }
</style>

<script>
// SOSTITUISCI QUESTO URL CON IL TUO WEB APP URL DI GOOGLE APPS SCRIPT
const SCRIPT_URL = "https://script.google.com/macros/s/AKfycbwTQJzxvLspR-1GdYh1wOXSLrF8h4TIeswEAIUJGtM9z1I4pIUZD3N_ANO2oewKmaI/exec?sheet=Segnalazioni";

async function caricaSegnalazioni() {
  const btnReload = document.getElementById('btn-reload');
  const elemOffline = document.getElementById('cnt-offline');
  const elemAttesa = document.getElementById('cnt-attesa');

  // Animazione pulsante ricarica
  if (btnReload) btnReload.classList.add('spin');
  elemOffline.innerText = "...";
  elemAttesa.innerText = "...";

  try {
    const res = await fetch(SCRIPT_URL);
    const data = await res.json();
    
    let countOffline = 0;
    let countAttesa = 0;
    
    // Legge la colonna F (indice 5) di ogni riga ritornata dal foglio "Segnalazioni"
    data.forEach(riga => {
      const stato = (riga[5] || riga.Stato || "").toString().trim().toUpperCase();
      if (stato === "OFFLINE") countOffline++;
      if (stato === "IN ATTESA") countAttesa++;
    });
    
    elemOffline.innerText = countOffline;
    elemAttesa.innerText = countAttesa;
  } catch (err) {
    console.error("Errore nel caricamento delle segnalazioni:", err);
    elemOffline.innerText = "Err";
    elemAttesa.innerText = "Err";
  } finally {
    if (btnReload) btnReload.classList.remove('spin');
  }
}

// Caricamento automatico al caricamento della pagina
document.addEventListener("DOMContentLoaded", caricaSegnalazioni);
</script>