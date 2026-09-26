// INCOLLA QUI L'URL DELLA TUA WEB APP GOOGLE APPS SCRIPT
const SCRIPT_URL = "https://script.google.com/macros/s/AKfycbxBf2aK5ILmULSlcuuGR6K47vsuJbdwj1b1jEtBwl8qMEzXCZRr0QKG5wc4ZAoVnj4/exec";

// ALBERO DEI DATI GERARCHICO
const datiStruttura = {
  "SPORT": {
    "Liste Eventi": [
      "Lista 1 (Daddy)",
      "Lista 2 (Platin - Ace)",
      "Lista 3 (Sportzonline)",
      "Lista 4 (SportzX)",
      "Lista 5 (CDN)",
      "Lista 6 (Fitlibre)"
    ],
    "Liste Canali": [
      "MPD (Nazioni)",
      "MPD (All)",
      "Sky",
      "Sky 2",
      "Lista Ace 1",
      "Free Live Sport",
      "Mediahosting Channel",
      "Lista 1 (Github 1)",
      "Lista 2 (Github 2)",
      "Lista 3 (Rocktalk)",
      "Lista 4 (Partite)",
      "Lista 5 (Sportsonline)",
      "Lista 6 (Sports99)",
      "Lista 7 (Rustinco Tv)",
      "Lista 8 (Daddy)"
    ],
    "Roja Tube": [
      "Roja Tube"
    ],
    "Sport Replay": [
      "Soccer Replay",
      "Motor Sport Replay",
      "NBA Replay",
      "WNBA Replay",
      "Eurolegue Replay",
      "NFL Condensed Replay",
      "UFC Replay",
      "Tennis Replay",
      "WWE Replay"
    ]
  },
  "LIVE": {
    "Generale": ["Tutti i canali LIVE"]
  },
  "ONDEMAND": {
    "Generale": ["Tutti i contenuti ONDEMAND"]
  },
  "RADIO": {
    "Generale": ["Tutte le stazioni RADIO"]
  }
};

document.addEventListener("DOMContentLoaded", function() {
  const catPrincipale = document.getElementById('cat_principale');
  const catSecondaria = document.getElementById('cat_secondaria');
  const contenutoSpecifico = document.getElementById('contenuto_specifico');
  const warningDiv = document.getElementById('duplicate-warning');
  const btnSubmit = document.getElementById('btnSubmit');

  if (!catPrincipale) return;

  // POPOLA SUB-CATEGORIA
  catPrincipale.addEventListener('change', function() {
    const val = this.value;
    catSecondaria.innerHTML = '<option value="">-- Seleziona Sotto-Categoria --</option>';
    contenutoSpecifico.innerHTML = '<option value="">-- Prima seleziona la Sotto-Categoria --</option>';
    contenutoSpecifico.disabled = true;

    if (val && datiStruttura[val]) {
      catSecondaria.disabled = false;
      Object.keys(datiStruttura[val]).forEach(function(subCat) {
        const opt = document.createElement('option');
        opt.value = subCat;
        opt.textContent = subCat;
        catSecondaria.appendChild(opt);
      });
    } else {
      catSecondaria.disabled = true;
    }
    checkDuplicate();
  });

  // POPOLA CONTENUTO SPECIFICO
  catSecondaria.addEventListener('change', function() {
    const macro = catPrincipale.value;
    const sub = this.value;
    contenutoSpecifico.innerHTML = '<option value="">-- Seleziona Contenuto/Lista --</option>';

    if (macro && sub && datiStruttura[macro] && datiStruttura[macro][sub]) {
      contenutoSpecifico.disabled = false;
      datiStruttura[macro][sub].forEach(function(item) {
        const opt = document.createElement('option');
        opt.value = item;
        opt.textContent = item;
        contenutoSpecifico.appendChild(opt);
      });
    } else {
      contenutoSpecifico.disabled = true;
    }
    checkDuplicate();
  });

  contenutoSpecifico.addEventListener('change', checkDuplicate);

  // CONTROLLO DUPLICATI
  async function checkDuplicate() {
    const macro = catPrincipale.value;
    const sub = catSecondaria.value;
    const item = contenutoSpecifico.value;

    if (macro && sub && item) {
      const nomeCompleto = `${macro} > ${sub} > ${item}`;
      try {
        const res = await fetch(`${SCRIPT_URL}?action=checkDuplicate&sezione=${encodeURIComponent(macro)}&contenuto=${encodeURIComponent(nomeCompleto)}`);
        const result = await res.json();

        if (result.duplicate) {
          warningDiv.style.display = 'block';
          btnSubmit.disabled = true;
          btnSubmit.style.opacity = '0.5';
        } else {
          warningDiv.style.display = 'none';
          btnSubmit.disabled = false;
          btnSubmit.style.opacity = '1';
        }
      } catch (e) {
        console.error("Errore verifica duplicato", e);
      }
    } else {
      warningDiv.style.display = 'none';
      btnSubmit.disabled = false;
      btnSubmit.style.opacity = '1';
    }
  }

  // CARICAMENTO SEGNALAZIONI
  async function loadReports() {
    try {
      const res = await fetch(`${SCRIPT_URL}?action=getOpen`);
      const data = await res.json();
      const tbody = document.getElementById('tabella-segnalazioni');
      tbody.innerHTML = '';

      if (!data || data.length === 0) {
        tbody.innerHTML = '<tr><td colspan="5">Nessuna segnalazione attiva al momento.</td></tr>';
        return;
      }

      data.forEach(item => {
        tbody.innerHTML += `
          <tr style="border-bottom: 1px solid #444;">
            <td>${item.data}</td>
            <td><span style="background: #333; padding: 2px 6px; border-radius: 4px;">${item.sezione}</span></td>
            <td><strong>${item.contenuto}</strong></td>
            <td>${item.problema}</td>
            <td><span style="background: #ff9800; padding: 2px 6px; border-radius: 4px; font-size: 12px; color: #000;">${item.stato}</span></td>
          </tr>
        `;
      });
    } catch (e) {
      console.error("Errore caricamento tabella:", e);
    }
  }

  // INVIO FORM
  document.getElementById('reportForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    btnSubmit.innerText = "Invio in corso...";
    btnSubmit.disabled = true;

    const macro = catPrincipale.value;
    const sub = catSecondaria.value;
    const item = contenutoSpecifico.value;

    const payload = {
      sezione: macro,
      contenuto: `${macro} > ${sub} > ${item}`,
      problema: document.getElementById('problema').value,
      piattaforma: document.getElementById('piattaforma').value
    };

    try {
      await fetch(SCRIPT_URL, {
        method: 'POST',
        mode: 'no-cors',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
      });

      alert('Segnalazione inviata con successo!');
      
      document.getElementById('reportForm').reset();
      catSecondaria.innerHTML = '<option value="">-- Prima seleziona la Categoria --</option>';
      catSecondaria.disabled = true;
      contenutoSpecifico.innerHTML = '<option value="">-- Prima seleziona la Sotto-Categoria --</option>';
      contenutoSpecifico.disabled = true;

      setTimeout(loadReports, 1500);

    } catch (error) {
      console.error('Errore durante invio:', error);
      alert('Si è verificato un errore durante l invio.');
    } finally {
      btnSubmit.innerText = "Invia Segnalazione";
      btnSubmit.disabled = false;
    }
  });

  loadReports();
});
