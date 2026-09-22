<style> /* CSS Adattivo: usa variabili di tema o fallback nativi del browser */ #calendario { max-width: 900px; margin: auto; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; color: var(--md-default-fg-color, inherit); }

.cal-title {
text-align: center;
font-size: 28px;
font-weight: bold;
margin-bottom: 20px;
}

.filtri-container {
display: flex;
flex-wrap: wrap;
gap: 8px;
justify-content: center;
margin-bottom: 25px;
}

.btn-filtro {
background: var(--md-default-bg-color--panel, rgba(150, 150, 150, 0.15));
color: var(--md-default-fg-color, inherit);
border: 1px solid rgba(150, 150, 150, 0.3);
padding: 6px 14px;
border-radius: 20px;
font-size: 14px;
font-weight: 600;
cursor: pointer;
transition: all 0.2s ease;
}

.btn-filtro:hover {
background: rgba(150, 150, 150, 0.25);
}

.btn-filtro.attivo {
background: #007acc;
color: #ffffff;
border-color: #007acc;
}

.sezione {
margin-top: 30px;
}

.sezione-titolo {
font-size: 20px;
font-weight: bold;
padding: 10px 14px;
border-radius: 8px;
margin-bottom: 12px;
background: rgba(150, 150, 150, 0.12);
border-left: 4px solid #007acc;

```
/* Evita che il titolo finisca sotto la barra/header */
scroll-margin-top: 80px;
```

}

.live-titolo {
background: rgba(224, 0, 0, 0.15);
color: #e00000;
border-left-color: #e00000;
}

.data {
font-size: 15px;
font-weight: bold;
margin-top: 18px;
margin-bottom: 6px;
padding: 6px 10px;
background: rgba(150, 150, 150, 0.08);
border-left: 3px solid rgba(150, 150, 150, 0.5);
border-radius: 0 4px 4px 0;
}

.evento {
display: grid;
grid-template-columns: 65px 85px 1fr;
align-items: center;
gap: 8px;
padding: 10px;
border-bottom: 1px solid rgba(150, 150, 150, 0.2);
}

.ora {
font-weight: bold;
opacity: 0.9;
}

.categoria {
font-size: 12px;
font-weight: bold;
opacity: 0.7;
text-transform: uppercase;
}

.partita-container {
display: flex;
flex-direction: column;
gap: 2px;
}

.partita-titolo {
font-weight: 600;
}

.partita-titolo a {
color: inherit;
text-decoration: none;
}

.partita-titolo a:hover {
text-decoration: underline;
}

.partita-broadcaster {
font-size: 12px;
opacity: 0.75;
display: flex;
align-items: center;
gap: 4px;
}

.live {
background: rgba(224, 0, 0, 0.08);
border-left: 3px solid #e00000;
}

.live .ora {
color: #e00000;
}

.badge-live {
display: inline-block;
background: #e00000;
color: #ffffff;
font-size: 10px;
font-weight: bold;
padding: 2px 5px;
border-radius: 4px;
margin-right: 4px;
animation: blink 1.5s infinite;
}

@keyframes blink {
50% {
opacity: 0.5;
}
}

.caricamento {
text-align: center;
padding: 30px;
opacity: 0.7;
}

.errore {
color: #e00000;
background: rgba(224, 0, 0, 0.1);
padding: 15px;
border-radius: 6px;
border: 1px solid rgba(224, 0, 0, 0.3);
}
</style>

<div id="calendario"> <div class="cal-title">⚽ Calendario Events</div> <div class="caricamento">Caricamento eventi in corso...</div> </div> <script> (async function () {

```
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
let cacheEventi = [];
let filtroCorrente = "tutti";
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
    const oggi = new Date();
    let anno = oggi.getFullYear();
    const data = new Date(
        anno,
        mese,
        giorno
    );
    if (
        data.getTime() <
        oggi.getTime() -
        (180 * 24 * 60 * 60 * 1000)
    ) {
        anno++;
    }
    return {
        giorno,
        mese,
        anno,
        data
    };
}
function estraiEvento(
    item,
    dataCorrente,
    categoria
) {
    const titolo = pulisciTesto(
        item.title
    );
    const matchOra = titolo.match(
        /^(\d{1,2}):(\d{2})\s+(.*)$/
    );
    if (
        !matchOra ||
        !dataCorrente
    ) {
        return null;
    }
    const ora =
        parseInt(matchOra[1]);
    const minuti =
        parseInt(matchOra[2]);
    const partita =
        matchOra[3].trim();
    const dataEvento =
        new Date(
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
        const trovato =
            item.info.match(
                /https?:\/\/[^\s]+/i
            );
        if (trovato) {
            link = trovato[0];
        }
    }
    let broadcaster = "";
    if (item.info2) {
        broadcaster =
            pulisciTesto(
                item.info2
            );
    } else if (
        item.info &&
        !link
    ) {
        broadcaster =
            pulisciTesto(
                item.info
            );
    }
    return {
        categoria: categoria,
        partita: partita,
        ora:
            `${String(ora).padStart(2, "0")}:${String(minuti).padStart(2, "0")}`,
        data: dataEvento,
        link: link,
        broadcaster: broadcaster
    };
}
async function caricaFile(file) {
    const response =
        await fetch(file.url);
    if (!response.ok) {
        throw new Error(
            `HTTP ${response.status}`
        );
    }
    const json =
        await response.json();
    const listaItems =
        Array.isArray(json)
            ? json
            : (json.items || []);
    const eventi = [];
    let dataCorrente = null;
    for (
        const item of listaItems
    ) {
        const titolo =
            pulisciTesto(
                item.title
            );
        const nuovaData =
            estraiData(titolo);
        if (nuovaData) {
            dataCorrente =
                nuovaData;
            continue;
        }
        const evento =
            estraiEvento(
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
function creaElementoEvento(
    evento,
    live = false
) {
    const div =
        document.createElement(
            "div"
        );
    div.className =
        "evento" +
        (
            live
                ? " live"
                : ""
        );
    const partitaHtml =
        evento.link
            ? `<a href="${evento.link}" target="_blank" rel="noopener">${evento.partita}</a>`
            : evento.partita;
    const broadcasterHtml =
        evento.broadcaster
            ? `<div class="partita-broadcaster">📺 ${evento.broadcaster}</div>`
            : "";
    div.innerHTML = `
        <div class="ora">
            ${
                live
                    ? '<span class="badge-live">LIVE</span>'
                    : ''
            }
            ${evento.ora}
        </div>
        <div class="categoria">
            ${evento.categoria}
        </div>
        <div class="partita-container">
            <div class="partita-titolo">
                ${partitaHtml}
            </div>
            ${broadcasterHtml}
        </div>
    `;
    return div;
}
/*
 * ============================================================
 * GESTIONE ANCHOR
 * ============================================================
 *
 * Gli elementi Serie A/B/C/LIVE vengono creati
 * dinamicamente da JavaScript.
 *
 * Per questo motivo il browser non può trovare
 * immediatamente #serie-a, #serie-b, #serie-c o #live.
 *
 * Questa funzione viene chiamata DOPO il rendering.
 */
function vaiAllAnchor() {
    const hash =
        window.location.hash;
    if (!hash) {
        return;
    }
    const id =
        decodeURIComponent(
            hash.substring(1)
        );
    if (!id) {
        return;
    }
    const elemento =
        document.getElementById(id);
    if (!elemento) {
        return;
    }
    setTimeout(
        function () {
            elemento.scrollIntoView({
                behavior: "smooth",
                block: "start"
            });
        },
        100
    );
}
function renderingCalendario() {
    const contenitore =
        document.getElementById(
            "calendario"
        );
    contenitore.innerHTML =
        '<div class="cal-title">⚽ Calendario</div>';
    /*
     * FILTRI
     */
    const filtriDiv =
        document.createElement(
            "div"
        );
    filtriDiv.className =
        "filtri-container";
    const opzioniFiltro = [
        {
            id: "tutti",
            label: "Tutti"
        },
        {
            id: "live",
            label: "🔴 Live"
        },
        {
            id: "Serie A",
            label: "Serie A"
        },
        {
            id: "Serie B",
            label: "Serie B"
        },
        {
            id: "Serie C",
            label: "Serie C"
        }
    ];
    opzioniFiltro.forEach(
        f => {
            const btn =
                document.createElement(
                    "button"
                );
            btn.className =
                "btn-filtro" +
                (
                    filtroCorrente === f.id
                        ? " attivo"
                        : ""
                );
            btn.textContent =
                f.label;
            btn.onclick = () => {
                filtroCorrente =
                    f.id;
                renderingCalendario();
            };
            filtriDiv.appendChild(
                btn
            );
        }
    );
    contenitore.appendChild(
        filtriDiv
    );
    const adesso =
        new Date();
    const durataPartita =
        2 * 60 * 60 * 1000;
    /*
     * EVENTI LIVE
     */
    const eventiLive =
        cacheEventi.filter(
            e => {
                const inizio =
                    e.data;
                const fine =
                    new Date(
                        inizio.getTime() +
                        durataPartita
                    );
                return (
                    adesso >= inizio &&
                    adesso <= fine
                );
            }
        );
    const liveSet =
        new Set(eventiLive);
    const eventiFuturi =
        cacheEventi.filter(
            e =>
                !liveSet.has(e)
        );
    /*
     * ========================================================
     * SEZIONE LIVE
     * ========================================================
     */
    if (
        (
            filtroCorrente === "tutti" ||
            filtroCorrente === "live"
        ) &&
        eventiLive.length > 0
    ) {
        const liveSezione =
            document.createElement(
                "div"
            );
        liveSezione.className =
            "sezione";
        const liveTitolo =
            document.createElement(
                "div"
            );
        liveTitolo.className =
            "sezione-titolo live-titolo";
        /* ANCHOR #live */
        liveTitolo.id =
            "live";
        liveTitolo.textContent =
            "🔴 LIVE - In Corso";
        liveSezione.appendChild(
            liveTitolo
        );
        eventiLive.forEach(
            e => {
                liveSezione.appendChild(
                    creaElementoEvento(
                        e,
                        true
                    )
                );
            }
        );
        contenitore.appendChild(
            liveSezione
        );
    }
    if (
        filtroCorrente === "live"
    ) {
        vaiAllAnchor();
        return;
    }
    /*
     * ========================================================
     * SEZIONI SERIE
     * ========================================================
     */
    const categorieDaMostrare =
        filtroCorrente === "tutti"
            ? [
                "Serie A",
                "Serie B",
                "Serie C"
            ]
            : [
                filtroCorrente
            ];
    categorieDaMostrare.forEach(
        cat => {
            const eventiCat =
                eventiFuturi.filter(
                    e =>
                        e.categoria === cat
                );
            if (
                eventiCat.length === 0
            ) {
                return;
            }
            const sezione =
                document.createElement(
                    "div"
                );
            sezione.className =
                "sezione";
            const titolo =
                document.createElement(
                    "div"
                );
            titolo.className =
                "sezione-titolo";
            /*
             * ANCHOR DELLA CATEGORIA
             */
            if (
                cat === "Serie A"
            ) {
                titolo.id =
                    "serie-a";
            } else if (
                cat === "Serie B"
            ) {
                titolo.id =
                    "serie-b";
            } else if (
                cat === "Serie C"
            ) {
                titolo.id =
                    "serie-c";
            }
            /*
             * TESTO DEL TITOLO
             */
            if (
                cat === "Serie A"
            ) {
                titolo.textContent =
                    "🇮🇹 Serie A";
            } else if (
                cat === "Serie B"
            ) {
                titolo.textContent =
                    "🇮🇹 Serie B";
            } else if (
                cat === "Serie C"
            ) {
                titolo.textContent =
                    "🇮🇹 Serie C";
            } else {
                titolo.textContent =
                    cat;
            }
            sezione.appendChild(
                titolo
            );
            /*
             * RAGGRUPPAMENTO PER GIORNO
             */
            const gruppi = {};
            eventiCat.forEach(
                e => {
                    const chiav =
                        e.data
                            .toISOString()
                            .split("T")[0];
                    if (
                        !gruppi[chiav]
                    ) {
                        gruppi[chiav] =
                            [];
                    }
                    gruppi[chiav]
                        .push(e);
                }
            );
            Object.keys(gruppi)
                .sort()
                .forEach(
                    chiav => {
                        const evGiorno =
                            gruppi[chiav]
                                .sort(
                                    (a, b) =>
                                        a.data -
                                        b.data
                                );
                        const dataHeader =
                            document.createElement(
                                "div"
                            );
                        dataHeader.className =
                            "data";
                        dataHeader.textContent =
                            formatData(
                                evGiorno[0]
                                    .data
                            );
                        sezione.appendChild(
                            dataHeader
                        );
                        evGiorno.forEach(
                            e => {
                                sezione.appendChild(
                                    creaElementoEvento(
                                        e,
                                        false
                                    )
                                );
                            }
                        );
                    }
                );
            contenitore.appendChild(
                sezione
            );
        }
    );
    /*
     * ========================================================
     * ANCHOR DOPO IL RENDERING
     * ========================================================
     */
    vaiAllAnchor();
}
/*
 * Se l'utente cambia l'hash
 * senza ricaricare la pagina.
 */
window.addEventListener(
    "hashchange",
    function () {
        vaiAllAnchor();
    }
);
/*
 * ========================================================
 * CARICAMENTO DATI
 * ========================================================
 */
try {
    const risultati =
        await Promise.all(
            FILES.map(
                caricaFile
            )
        );
    cacheEventi =
        risultati
            .flat()
            .sort(
                (a, b) =>
                    a.data - b.data
            );
    /*
     * Prima visualizzazione
     */
    renderingCalendario();
    /*
     * Aggiornamento automatico
     * ogni 60 secondi
     */
    setInterval(
        renderingCalendario,
        60000
    );
} catch (errore) {
    document.getElementById(
        "calendario"
    ).innerHTML = `
        <div class="errore">
            <strong>
                Errore nel caricamento del calendario:
            </strong><br>
            ${errore.message}
        </div>
    `;
    console.error(
        errore
    );
}
```

})();
</script>