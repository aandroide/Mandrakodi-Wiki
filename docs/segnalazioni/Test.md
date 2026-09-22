<style>
body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}

#calendario {
    max-width: 900px;
    margin: auto;
}

.cal-title {
    text-align: center;
    font-size: 28px;
    font-weight: bold;
    margin-bottom: 25px;
}

.sezione {
    margin-top: 30px;
}

.sezione-titolo {
    font-size: 22px;
    font-weight: bold;
    padding: 10px 14px;
    border-radius: 8px;
    margin-bottom: 12px;
    background: #f1f1f1;
}

.live-titolo {
    background: #ffe5e5;
    color: #d00000;
}

.data {
    font-size: 17px;
    font-weight: bold;
    margin-top: 18px;
    margin-bottom: 6px;
    padding: 7px 10px;
    background: #f5f5f5;
    border-left: 4px solid #777;
}

.evento {
    display: grid;
    grid-template-columns: 65px 90px 1fr;
    align-items: center;
    gap: 8px;
    padding: 9px 10px;
    border-bottom: 1px solid #e5e5e5;
}

.ora {
    font-weight: bold;
    color: #333;
}

.categoria {
    font-size: 13px;
    font-weight: bold;
    color: #777;
}

.partita a {
    color: inherit;
    text-decoration: none;
}

.partita a:hover {
    text-decoration: underline;
}

.live {
    background: #fff0f0;
    border-left: 4px solid #e00000;
}

.live .ora {
    color: #d00000;
}

.badge-live {
    display: inline-block;
    background: #e00000;
    color: white;
    font-size: 11px;
    font-weight: bold;
    padding: 3px 6px;
    border-radius: 4px;
    margin-right: 6px;
}

.caricamento {
    text-align: center;
    padding: 30px;
    color: #777;
}

.errore {
    color: #c00000;
    background: #ffeaea;
    padding: 15px;
    border-radius: 6px;
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
        gennaio: 0,
        febbraio: 1,
        marzo: 2,
        aprile: 3,
        maggio: 4,
        giugno: 5,
        luglio: 6,
        agosto: 7,
        settembre: 8,
        ottobre: 9,
        novembre: 10,
        dicembre: 11
    };
    
    const giorni = {
        domenica: 0,
        lunedì: 1,
        lunedi: 1,
        martedì: 2,
        martedi: 2,
        mercoledì: 3,
        mercoledi: 3,
        giovedì: 4,
        giovedi: 4,
        venerdì: 5,
        venerdi: 5,
        sabato: 6
    };
    
    function pulisciTesto(testo) {
        return (testo || "")
            .replace(/\[COLOR [^\]]+\]/gi, "")
            .replace(/\[\/COLOR\]/gi, "")
            .trim();
    }
    
    function estraiData(testo) {
    
        testo = pulisciTesto(testo);
    
        const parti = testo
            .toLowerCase()
            .replace(/,/g, "")
            .split(/\s+/);
    
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
    
        if (giorno === null || mese === null) {
            return null;
        }
    
        /*
         * I tuoi JSON non riportano l'anno.
         * Usiamo l'anno corrente e correggiamo automaticamente
         * il passaggio dicembre -> gennaio.
         */
    
        const oggi = new Date();
        let anno = oggi.getFullYear();
    
        const data = new Date(
            anno,
            mese,
            giorno
        );
    
        /*
         * Se la data è molto indietro rispetto ad oggi,
         * la consideriamo dell'anno successivo.
         */
    
        if (data.getTime() < oggi.getTime() - (180 * 24 * 60 * 60 * 1000)) {
            anno++;
        }
    
        return {
            giorno,
            mese,
            anno,
            data
        };
    }
    
    function estraiEvento(item, dataCorrente, categoria) {
    
        const titolo = pulisciTesto(item.title);
    
        const matchOra = titolo.match(/^(\d{1,2}):(\d{2})\s+(.*)$/);
    
        if (!matchOra || !dataCorrente) {
            return null;
        }
    
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
            const trovato = item.info.match(
                /https?:\/\/[^\s]+/i
            );
    
            if (trovato) {
                link = trovato[0];
            }
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
            throw new Error(
                `Errore caricamento ${file.nome}: HTTP ${response.status}`
            );
        }
    
        const json = await response.json();
    
        const eventi = [];
        let dataCorrente = null;
    
        for (const item of json.items || []) {
    
            const titolo = pulisciTesto(item.title);
    
            /*
             * Riconosce le righe data:
             *
             * Sabato 10 Ottobre
             * Mercoledi 23 Settembre
             * ecc.
             */
    
            const nuovaData = estraiData(titolo);
    
            if (nuovaData) {
                dataCorrente = nuovaData;
                continue;
            }
    
            const evento = estraiEvento(
                item,
                dataCorrente,
                file.nome
            );
    
            if (evento) {
                eventi.push(evento);
            }
        }
    
        return eventi;
    }
    
    function formatData(data) {
    
        return data.toLocaleDateString(
            "it-IT",
            {
                weekday: "long",
                day: "numeric",
                month: "long"
            }
        );
    }
    
    function creaEvento(evento, live = false) {
    
        const div = document.createElement("div");
    
        div.className = "evento" + (live ? " live" : "");
    
        let contenutoPartita = "";
    
        if (evento.link) {
    
            contenutoPartita =
                `<a href="${evento.link}" target="_blank">
                    ${evento.partita}
                </a>`;
    
        } else {
    
            contenutoPartita = evento.partita;
    
        }
    
        div.innerHTML = `
            <div class="ora">
                ${live ? '<span class="badge-live">LIVE</span>' : ''}
                ${evento.ora}
            </div>
    
            <div class="categoria">
                ${evento.categoria}
            </div>
    
            <div class="partita">
                ${contenutoPartita}
            </div>
        `;
    
        return div;
    }
    
    function creaSezione(categoria, eventi) {
    
        const sezione = document.createElement("div");
    
        sezione.className = "sezione";
    
        const titolo = document.createElement("div");
    
        titolo.className = "sezione-titolo";
    
        titolo.textContent =
            categoria === "Serie A" ? "🇮🇹 Serie A" :
            categoria === "Serie B" ? "🇮🇹 Serie B" :
            "🇮🇹 Serie C";
    
        sezione.appendChild(titolo);
    
        /*
         * Raggruppamento per giorno
         */
    
        const gruppi = {};
    
        for (const evento of eventi) {
    
            const chiave =
                evento.data.getFullYear() +
                "-" +
                String(evento.data.getMonth() + 1).padStart(2, "0") +
                "-" +
                String(evento.data.getDate()).padStart(2, "0");
    
            if (!gruppi[chiave]) {
                gruppi[chiave] = [];
            }
    
            gruppi[chiave].push(evento);
        }
    
        const date = Object.keys(gruppi).sort();
    
        for (const chiave of date) {
    
            const eventiGiorno = gruppi[chiave];
    
            eventiGiorno.sort(
                (a, b) => a.data - b.data
            );
    
            const data = document.createElement("div");
    
            data.className = "data";
    
            data.textContent =
                formatData(eventiGiorno[0].data);
    
            sezione.appendChild(data);
    
            for (const evento of eventiGiorno) {
    
                sezione.appendChild(
                    creaEvento(evento)
                );
    
            }
        }
    
        return sezione;
    }
    
    try {
    
        const risultati =
            await Promise.all(
                FILES.map(caricaFile)
            );
    
        let tuttiGliEventi =
            risultati.flat();
    
        /*
         * Ordine cronologico generale
         */
    
        tuttiGliEventi.sort(
            (a, b) => a.data - b.data
        );
    
        /*
         * LIVE
         *
         * Consideriamo LIVE una partita iniziata
         * e non terminata da più di 2 ore.
         */
    
        const adesso = new Date();
    
        const durataPartita =
            2 * 60 * 60 * 1000;
    
        const live = tuttiGliEventi.filter(evento => {
    
            const inizio = evento.data;
    
            const fine =
                new Date(
                    inizio.getTime() +
                    durataPartita
                );
    
            return (
                adesso >= inizio &&
                adesso <= fine
            );
        });
    
        /*
         * Eliminiamo gli eventi LIVE dal calendario
         * normale.
         */
    
        const liveSet = new Set(live);
    
        const futuri =
            tuttiGliEventi.filter(
                evento => !liveSet.has(evento)
            );
    
        /*
         * LIVE ordinati cronologicamente
         */
    
        live.sort(
            (a, b) => a.data - b.data
        );
    
        /*
         * Costruzione pagina
         */
    
        const contenitore =
            document.getElementById("calendario");
    
        contenitore.innerHTML =
            '<div class="cal-title">⚽ Calendario</div>';
    
        /*
         * SEZIONE LIVE
         */
    
        if (live.length > 0) {
    
            const liveSezione =
                document.createElement("div");
    
            liveSezione.className =
                "sezione";
    
            const liveTitolo =
                document.createElement("div");
    
            liveTitolo.className =
                "sezione-titolo live-titolo";
    
            liveTitolo.textContent =
                "🔴 LIVE";
    
            liveSezione.appendChild(
                liveTitolo
            );
    
            for (const evento of live) {
    
                liveSezione.appendChild(
                    creaEvento(evento, true)
                );
    
            }
    
            contenitore.appendChild(
                liveSezione
            );
        }
    
        /*
         * SERIE A / B / C
         */
    
        for (const categoria of [
            "Serie A",
            "Serie B",
            "Serie C"
        ]) {
    
            const eventi =
                futuri.filter(
                    evento =>
                        evento.categoria === categoria
                );
    
            if (eventi.length > 0) {
    
                contenitore.appendChild(
                    creaSezione(
                        categoria,
                        eventi
                    )
                );
            }
        }
    
        /*
         * Aggiornamento automatico
         * ogni 60 secondi per aggiornare LIVE.
         */
    
        setTimeout(
            () => location.reload(),
            60000
        );
    
    } catch (errore) {
    
        document.getElementById(
            "calendario"
        ).innerHTML = `
            <div class="errore">
                <strong>Errore:</strong><br>
                ${errore.message}
            </div>
        `;
    
        console.error(errore);
    }

})();
</script>
