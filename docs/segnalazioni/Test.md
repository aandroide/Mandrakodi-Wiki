```markdown
# Partite di calcio

Le prossime partite di Serie A, Serie B e Serie C.

<div id="partite">
  Caricamento partite...
</div>

<script>
async function caricaPartite() {
  const container = document.getElementById("partite");

  try {
    const response = await fetch("./partite.json");

    if (!response.ok) {
      throw new Error("Impossibile caricare partite.json");
    }

    const data = await response.json();

    if (!data.partite || data.partite.length === 0) {
      container.innerHTML = "<p>Nessuna partita trovata.</p>";
      return;
    }

    const gruppi = {};

    for (const partita of data.partite) {
      if (!gruppi[partita.data]) {
        gruppi[partita.data] = [];
      }

      gruppi[partita.data].push(partita);
    }

    let html = "";

    for (const dataPartita of Object.keys(gruppi).sort()) {
      const dataObj = new Date(dataPartita + "T00:00:00");

      const dataFormattata = dataObj.toLocaleDateString(
        "it-IT",
        {
          weekday: "long",
          day: "2-digit",
          month: "long",
          year: "numeric"
        }
      );

      html += `
        <section class="giornata">
          <h2>${dataFormattata}</h2>
      `;

      for (const partita of gruppi[dataPartita]) {
        html += `
          <div class="partita">
            <div class="ora">
              ${partita.ora}
            </div>

            <div class="squadre">
              <strong>${partita.casa}</strong>
              <span> - </span>
              <strong>${partita.trasferta}</strong>
            </div>

            <div class="competizione">
              ${partita.competizione}
            </div>
          </div>
        `;
      }

      html += `
        </section>
      `;
    }

    html += `
      <p class="aggiornamento">
        Ultimo aggiornamento:
        ${new Date(data.aggiornato).toLocaleString("it-IT")}
      </p>
    `;

    container.innerHTML = html;

  } catch (error) {
    console.error(error);

    container.innerHTML = `
      <p>
        Errore durante il caricamento delle partite.
      </p>
    `;
  }
}

caricaPartite();
</script>

<style>
#partite {
  max-width: 900px;
  margin: 0 auto;
}

.giornata {
  margin-bottom: 30px;
}

.giornata h2 {
  border-bottom: 2px solid #ddd;
  padding-bottom: 8px;
  text-transform: capitalize;
}

.partita {
  display: grid;
  grid-template-columns: 70px 1fr 100px;
  align-items: center;

  padding: 12px;
  margin: 6px 0;

  border: 1px solid #ddd;
  border-radius: 8px;

  background: #fff;
}

.ora {
  font-size: 18px;
  font-weight: bold;
}

.squadre {
  font-size: 16px;
}

.competizione {
  text-align: right;
  font-size: 13px;
  color: #666;
}

.aggiornamento {
  margin-top: 30px;
  color: #777;
  font-size: 13px;
}

@media (max-width: 600px) {
  .partita {
    grid-template-columns: 60px 1fr;
  }

  .competizione {
    grid-column: 2;
    text-align: left;
    margin-top: 4px;
  }

  .squadre {
    font-size: 14px;
  }
}
</style>
```
