<style>
/* CSS con supporto nativo a Light/Dark Mode (MkDocs / GitHub Pages) */
#calendario {
    max-width: 900px;
    margin: auto;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    color: var(--md-typeset-color, inherit);
}

.cal-title {
    text-align: center;
    font-size: 28px;
    font-weight: bold;
    margin-bottom: 20px;
}

/* Barra Filtri */
.filtri-container {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    justify-content: center;
    margin-bottom: 25px;
}

.btn-filtro {
    background: var(--md-default-bg-color--panel, rgba(150, 150, 150, 0.15));
    color: var(--md-typeset-color, inherit);
    border: 1px solid var(--md-default-fg-color--lightest, rgba(150, 150, 150, 0.3));
    padding: 8px 16px;
    border-radius: 20px;
    font-size: 14px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
}

.btn-filtro:hover {
    opacity: 0.8;
}

.btn-filtro.attivo {
    background: #007acc;
    color: #ffffff !important;
    border-color: #007acc;
}

.btn-filtro.live-btn.attivo {
    background: #e00000;
    border-color: #e00000;
}

/* Sezioni e Titoli */
.sezione {
    margin-top: 30px;
}

.sezione-titolo {
    font-size: 22px;
    font-weight: bold;
    padding: 10px 14px;
    border-radius: 8px;
    margin-bottom: 12px;
    background: var(--md-default-bg-color--panel, rgba(150, 150, 150, 0.15));
    color: var(--md-typeset-color, inherit);
    border: 1px solid var(--md-default-fg-color--lightest, rgba(150, 150, 150, 0.2));
}

.live-titolo {
    background: rgba(224, 0, 0, 0.15);
    color: #e00000;
    border: 1px solid rgba(224, 0, 0, 0.3);
}

.data {
    font-size: 17px;
    font-weight: bold;
    margin-top: 18px;
    margin-bottom: 6px;
    padding: 7px 10px;
    background: var(--md-default-bg-color--panel, rgba(150, 150, 150, 0.1));
    color: var(--md-typeset-color, inherit);
    border-left: 4px solid var(--md-default-fg-color--light, #777);
}

.evento {
    display: grid;
    grid-template-columns: 75px 90px 1fr;
    align-items: center;
    gap: 8px;
    padding: 9px 10px;
    border-bottom: 1px solid var(--md-default-fg-color--lightest, rgba(150, 150, 150, 0.2));
}

.ora {
    font-weight: bold;
    color: var(--md-typeset-color, inherit);
}

.categoria {
    font-size: 13px;
    font-weight: bold;
    opacity: 0.7;
    color: var(--md-typeset-color, inherit);
}

.partita a {
    color: var(--md-typeset-a-color, #007acc);
    text-decoration: none;
}

.partita a:hover {
    text-decoration: underline;
}

.live {
    background: rgba(224, 0, 0, 0.08);
    border-left: 4px solid #e00000;
}

.live .ora {
    color: #e00000;
}

.badge-live {
    display: inline-block;
    background: #e00000;
    color: #ffffff !important;
    font-size: 11px;
    font-weight: bold;
    padding: 3px 6px;
    border-radius: 4px;
    margin-right: 6px;
}

.caricamento {
    text-align: center;
    padding: 30px;
    opacity: 0.7;
}

.errore {
    color: #d00000;
    background: rgba(224, 0, 0, 0.1);
    padding: 15px;
    border-radius: 6px;
    border: 1px solid rgba(224, 0, 0, 0.3);
}
</style>

<div id="calendario">
    <div class="cal-title">⚽ Calendario</div>
    <div class="caricamento">Caricamento eventi...</div>
</div>

<script>
(async function () {

    const FILES = [
        {
            nome: "Serie A",
            url: "https://raw.githubusercontent.com/campipaolo/Livesoccer/93770da86eb3d6bdfcd4f4df1828cafef487afb0/livesoccertv/output/serie-a.json"
        },
        {
            nome: "Serie B",
            url: "https://raw.githubusercontent.com/campipaolo/Livesoccer/93770da86eb3d6bdfcd4f4df1828cafef487afb0/livesoccertv/output/serie-b.json"
        },
        {
            nome: "Serie C",
            url: "https://raw.githubusercontent.com/campipaolo/Livesoccer/93770da86eb3d6bdfcd4f4df1828cafef487afb0/livesoccertv/output/serie-c.json"
        }
    ];
    
    const mesi = {
        gennaio: 0, febbraio: 1, marzo: 2, aprile: 3, maggio: 4, giugno: 5,
        luglio: 6, agosto: 7, settembre: 8, ottobre: 9, novembre: 10, dicembre: 11
    };
    
    function pulisciTesto(testo) {
        return (testo || "")
            .replace(/\[COLOR [^\]]+\]/gi, "")
            .replace(/\[\/COLOR\]/gi, "")
            .trim();
    }
    
    function estraiData(testo) {
        testo = pulisciTesto(testo);
        const parti = testo.toLowerCase().replace(/,/g, "").split(/\s+/);
    
        let giorno = null;
        let mese = null;
    
        for (const parte of parti) {
            if (/^\d+$/.test(parte)) {
                giorno = parseInt(parte);
            }
            if (mesi[parte] !== undefined) {
                mese = mesi[parte];
            }
        }
    
        if (giorno === null || mese === null) return null;
    
        const oggi = new Date();
        let anno = oggi.getFullYear();
        const data = new Date(anno, mese, giorno);
    
        if (data.getTime() < oggi.getTime() - (180 * 24 * 60 * 60 * 1000)) {
            anno++;
        }
    
        return { giorno, mese, anno, data };
    }
    
    function estraiEvento(item, dataCorrente, categoria) {
        const titolo = pulisciTesto(item.title);
        const matchOra = titolo.match(/^(\d{1,2}):(\d{2})\s+(.*)$/);
    
        if (!matchOra || !dataCorrente) return null;
    
        const ora = parseInt(matchOra[1]);
        const minuti = parseInt(matchOra[2]);
        const partita = matchOra[3].trim();
    
        const dataEvento = new Date(
            dataCorrente.anno,
            dataCorrente.mese,
            dataCorrente.giorno,
            ora,
            minuti,
            0,
            0
        );
    
        let link = "";
        if (item.info) {
            const trovato = item.info.match(/https?:\/\/[^\s]+/i);
            if (trovato) link = trovato[0];
        }
    
        return {
            categoria: categoria,
            partita: partita,
            ora: `${String(ora).padStart(2, "0")}:${String(minuti).padStart(2, "0")}`,
            data: dataEvento,
            link: link
        };
    }
    
    async function caricaFile(file) {
        const response = await fetch(file.url);
        if (!response.ok) {
            throw new Error(`Errore caricamento ${file.nome}: HTTP ${response.status}`);
        }
    
        const json = await response.json();
        const eventi = [];
        let dataCorrente = null;
    
        for (const item of json.items || []) {
            const titolo = pulisciTesto(item.title);
            const nuovaData = estraiData(titolo);
    
            if (nuovaData) {
                dataCorrente = nuovaData;
                continue;
            }
    
            const evento = estraiEvento(item, dataCorrente, file.nome);
            if (evento) eventi.push(evento);
        }
    
        return eventi;
    }
    
    function formatData(data) {
        return data.toLocaleDateString("it-IT", {
            weekday: "long",
            day: "numeric",
            month: "long"
        });
    }
    
    function creaEvento(evento, live = false) {
        const div = document.createElement("div");
        div.className = "evento" + (live ? " live" : "");
    
        let contenutoPartita = evento.link
            ? `<a href="${evento.link}" target="_blank">${evento.partita}</a>`
            : evento.partita;
    
        div.innerHTML = `
            <div class="ora">
                ${live ? '<span class="badge-live">LIVE</span>' : ''}
                ${evento.ora}
            </div>
            <div class="categoria">${evento.categoria}</div>
            <div class="partita">${contenutoPartita}</div>
        `;
    
        return div;
    }
    
    function creaSezione(categoria, eventi) {
        const sezione = document.createElement("div");
        sezione.className = "sezione";
        sezione.dataset.categoria = categoria;
    
        const titolo = document.createElement("div");
        titolo.className = "sezione-titolo";
        titolo.textContent = 
            categoria === "Serie A" ? "🇮🇹 Serie A" :
            categoria === "Serie B" ? "🇮🇹 Serie B" : "🇮🇹 Serie C";
    
        sezione.appendChild(titolo);
    
        const gruppi = {};
        for (const evento of eventi) {
            const chiave = evento.data.getFullYear() + "-" +
                String(evento.data.getMonth() + 1).padStart(2, "0") + "-" +
                String(evento.data.getDate()).padStart(2, "0");
    
            if (!gruppi[chiave]) gruppi[chiave] = [];
            gruppi[chiave].push(evento);
        }
    
        const date = Object.keys(gruppi).sort();
    
        for (const chiave of date) {
            const eventiGiorno = gruppi[chiave];
            eventiGiorno.sort((a, b) => a.data - b.data);
    
            const dataDiv = document.createElement("div");
            dataDiv.className = "data";
            dataDiv.textContent = formatData(eventiGiorno[0].data);
    
            sezione.appendChild(dataDiv);
    
            for (const evento of eventiGiorno) {
                sezione.appendChild(creaEvento(evento));
            }
        }
    
        return sezione;
    }
    
    function applicaFiltro(filtro, bottoni) {
        bottoni.forEach(btn => {
            if (btn.dataset.filtro === filtro) {
                btn.classList.add("attivo");
            } else {
                btn.classList.remove("attivo");
            }
        });
    
        const sezioni = document.querySelectorAll("#calendario-sezioni .sezione");
        sezioni.forEach(sez => {
            if (filtro === "tutti") {
                sez.style.display = "block";
            } else if (filtro === "LIVE") {
                sez.style.display = sez.dataset.categoria === "LIVE" ? "block" : "none";
            } else {
                sez.style.display = sez.dataset.categoria === filtro ? "block" : "none";
            }
        });
    }
    
    try {
        const risultati = await Promise.all(FILES.map(caricaFile));
        let tuttiGliEventi = risultati.flat();
        tuttiGliEventi.sort((a, b) => a.data - b.data);
    
        const adesso = new Date();
        const durataPartita = 2 * 60 * 60 * 1000;
    
        const live = tuttiGliEventi.filter(evento => {
            const inizio = evento.data;
            const fine = new Date(inizio.getTime() + durataPartita);
            return adesso >= inizio && adesso <= fine;
        });
    
        const liveSet = new Set(live);
        const futuri = tuttiGliEventi.filter(evento => !liveSet.has(evento));
    
        live.sort((a, b) => a.data - b.data);
    
        const contenitore = document.getElementById("calendario");
        contenitore.innerHTML = '<div class="cal-title">⚽ Calendario</div>';
    
        // Barra Filtri
        const filtriContainer = document.createElement("div");
        filtriContainer.className = "filtri-container";
    
        const opzioniFiltro = [
            { id: "tutti", label: "Tutti" },
            { id: "LIVE", label: "🔴 LIVE", classExtra: "live-btn" },
            { id: "Serie A", label: "Serie A" },
            { id: "Serie B", label: "Serie B" },
            { id: "Serie C", label: "Serie C" }
        ];
    
        const bottoniFiltro = [];
    
        opzioniFiltro.forEach(opt => {
            const btn = document.createElement("button");
            btn.className = `btn-filtro ${opt.classExtra || ""}`.trim();
            btn.textContent = opt.label;
            btn.dataset.filtro = opt.id;
            btn.addEventListener("click", () => applicaFiltro(opt.id, bottoniFiltro));
            filtriContainer.appendChild(btn);
            bottoniFiltro.push(btn);
        });
    
        contenitore.appendChild(filtriContainer);
    
        const sezioniWrapper = document.createElement("div");
        sezioniWrapper.id = "calendario-sezioni";
    
        // Sezione LIVE
        if (live.length > 0) {
            const liveSezione = document.createElement("div");
            liveSezione.className = "sezione";
            liveSezione.dataset.categoria = "LIVE";
    
            const liveTitolo = document.createElement("div");
            liveTitolo.className = "sezione-titolo live-titolo";
            liveTitolo.textContent = "🔴 LIVE";
    
            liveSezione.appendChild(liveTitolo);
    
            for (const evento of live) {
                liveSezione.appendChild(creaEvento(evento, true));
            }
    
            sezioniWrapper.appendChild(liveSezione);
        }
    
        // Sezioni Serie A / B / C
        for (const categoria of ["Serie A", "Serie B", "Serie C"]) {
            const eventi = futuri.filter(evento => evento.categoria === categoria);
            if (eventi.length > 0) {
                sezioniWrapper.appendChild(creaSezione(categoria, eventi));
            }
        }
    
        contenitore.appendChild(sezioniWrapper);
    
        // Imposta filtro predefinito "Tutti"
        applicaFiltro("tutti", bottoniFiltro);
    
        // Reload automatico ogni 60 secondi
        setTimeout(() => location.reload(), 60000);
    
    } catch (errore) {
        document.getElementById("calendario").innerHTML = `
            <div class="errore">
                <strong>Errore:</strong><br>
                ${errore.message}
            </div>
        `;
        console.error(errore);
    }

})();
</script>
