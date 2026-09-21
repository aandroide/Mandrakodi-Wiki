[:material-book-open-page-variant: Torna alle Guide](../guide/tutorials.md){ .md-button .md-button--primary }  [:material-home: Torna alla Home](../index.md){.md-button .md-button--primary} [:material-face-agent: Assistenza](../ask_help.md){ .md-button .md-button--primary }

------

!!! tip "Ace, flussi P2P ad alta qualità"
    Sono link che sfruttano un protocollo basato sulla condivisione di flussi streaming tramite rete **p2p** (peer to peer) creando interconnessioni dirette tra più utenti senza transitare per un server/sito, proprio come con i famosi  eMule/Torrent<br>Questo significa che “chi guarda in streaming, trasmette anche agli altri utenti, ovvero *più utenti guardano e condividono a loro volta con altri interconnessi*, *meno blocchi ci sono durante la visione*”: **questo avviene esclusivamente se sul proprio router viene aperta la porta 8621 Udp**

!!! warning "Lingua contenuti"
    I link Ace sono **praticamente totalmente stranieri**, in quanto in Italia - salvo rarissime occasioni - poco utilizzati per *mancanza della cultura* di condivisione alla base di tutti i sistemi P2P 

------

!!! important "Fase 1 - Installazione"
    **Installare** sul proprio dispositivo  

??? info "Acestream per Windows"
    **Installer per Windows**

    * <a href="https://download.acestream.media/products/acestream-full/win/latest" target="_blank">Windows</a> 
    * Avviare Acestream

??? info "AceServe per Android Smarthpone/Tablet/Chiavette/Tv/Box/Firestick"
    **Installer MOD per Android Smarthpone/Tablet/Chiavette/Tv/Box/Firestick**

    * <a href="https://www.dropbox.com/scl/fi/uz8q15arnixvo47e9odbm/Aceserve-1.5.5-32bit.apk?rlkey=lhvtazx8sfqmrbd4qdsfsw1l9&st=nzwzt76l&dl=1" target="_blank">Android ARMV7A 32bit</a> Chiavette/Tv/Box/Firestick (Android 9 - 12)
    
    * <a href="https://www.dropbox.com/scl/fi/sz1kjiwgtnww1bjsmryfn/Aceserve-1.5.5-64bit.apk?rlkey=u8ekpvc4yq14wzvrwburg7jis&st=86575k8p&dl=1" target="_blank">Android ARMV8A 64bit</a> Smartphone/Tablet (Android 12 - 16)
    * Avviare AceServe una prima volta per dare i permessi
    * Premere "START" per avviare [(Foto)](../images/aceserve_start.png){ target="_blank" }
    * Tornare alla home page col tasto dedicato per **lasciarlo aperto in background**

??? info "Acestream per Linux"
    **Pacchetti per Linux**

    * Installare Acestream a seconda della propria distribuzione in formato "**Snap**" o "**Flatpak**"
    * Avviare Acestream

??? info "Acestream per macOS"
    **AceStream Engine su macOS con Docker**

    ## 1. Installare Homebrew
    
    Apri il **Terminale** (`⌘ + Spazio` → `Terminale`) ed esegui:
    
    ```bash
    /bin/bash -c "$(curl -fsSL [https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh](https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh))"
    ```
    
    Al termine, segui gli eventuali comandi mostrati dall'installer per aggiungere Homebrew al `PATH`.
    
    Verifica:
    
    ```bash
    brew --version
    ```
    
    > `curl` è già incluso in macOS. Non è necessario installarlo.
    
    ## 2. Installare Docker Desktop, VLC e jq
    
    Esegui:
    
    ```bash
    brew install --cask docker vlc
    brew install jq
    ```
    
    Avvia **Docker Desktop** dal menu Applicazioni e attendi che sia pronto.
    
    Verifica Docker e Docker Compose:
    
    ```bash
    docker --version
    docker compose version
    ```
    
    Verifica `jq`:
    
    ```bash
    jq --version
    ```
    
    ## 3. Creare la cartella del progetto
    
    ```bash
    mkdir -p ~/acestream-engine
    cd ~/acestream-engine
    ```
    
    ## 4. Creare il file Docker Compose
    
    Apri il file:
    
    ```bash
    nano docker-compose.yml
    ```
    
    Incolla questo contenuto:
    
    ```yaml
    services:
      acestream:
        container_name: AcestreamEngine
        image: wafy80/acestream:latest
        restart: unless-stopped
        ports:
          - "6878:6878"
          - "8621:8621/udp"
    ```
    
    Salva e chiudi `nano`:
    
    1. `Control + O`
    2. `Invio`
    3. `Control + X`
    
    Controlla il file:
    
    ```bash
    cat docker-compose.yml
    ```
    
    ## 5. Avviare AceStream Engine
    
    Dalla cartella del progetto:
    
    ```bash
    cd ~/acestream-engine
    docker compose up -d
    ```
    
    Controlla lo stato:
    
    ```bash
    docker compose ps
    ```
    
    ## 6. Verificare che AceStream sia avviato
    
    Esegui:
    
    ```bash
    curl -sS "[http://127.0.0.1:6878/webui/api/service?method=get_version](http://127.0.0.1:6878/webui/api/service?method=get_version)" | jq
    ```
    
    Nella risposta controlla:
    
    ```json
    "error": null
    ```

------

!!! important "Fase 2 - Player interno Kodi / Player esterno (es. Vlc, Mx Player)"
    - "**ENGINE**":   sfrutta motore di Ace **rimanendo all'interno di Kodi**  usando il suo **player interno** <br>                           (richieste più risorse hardware, solo per device con 2Gb Ram)
    - "**DIRETTO**":   sfrutta motore di Ace ma **esce da Kodi** usando un **player esterno** (es. Vlc, Mx Player) <br>                           (richieste meno risorse hardware, per dispositivi con 1,5Gb Ram)  

??? info "Opzione **ENGINE**"
    **Play all'interno di Kodi**

    * Avviare Kodi
    * In Mandrakodi avviare un link Ace
    * Usare opzione "**ENGINE**"



!!! warning "Attenzione"
    Per "Opzione DIRETTO" prima eseguire procedura per abilitare i "[Player Esterno](../guide/kodi_settings.md#players)" (se non precedentemente eseguita)

??? info "Opzione **DIRETTO**"
    **Play fuori da Kodi (es. Vlc, Mx Player)**

    * Avviare Kodi
    * In Mandrakodi avviare un link Ace
    * Usare opzione "**DIRETTO**"
    * Selezionare "**org.free.aceserve**"
    * Selezionare player esterno (es. Vlc, Mx Player)



------

!!! important "EXTRA - AceServe con dispositivi poco performanti"
    Con *dispositivi poco performanti*  (tv/chiavetta con 1Gb/1,5Gb Ram e 8Gb storage) è consigliabile eseguire AceServe su **altro dispositivo** (generalmente smartphone/tablet) **purché connesso alla medesima rete,**  sfruttando maggiori risorse per cache disco e ram 

??? info "Kodi su Tv/Chiavetta + AceServe su Android Smartphone/Tablet"
    **Eseguire AceServe su dispositivo terzo**

    * Installare AcesServe su smartphone/tablet
    * Avviare AcesServe sullo smartphone
    * Avviare Kodi su Tv/Chiavetta, dalla pagina principale, scorrere su addon
    * Tenere premuto sull'icona di Mandrakodi, poi "Impostazioni"
    * Nella scheda "**Personal List**", poi "**Appo1**", copiare come da foto inserendo IP smartphone
      ![acestream_app01](../images/acestream_app01.jpg)
    * N.B.: **IP smartphone** è visibile dalle proprietà della connessione Wifi
    * In Mandrakodi provare un qualunque link ace sempre e solo con opzione “**ENGINE**”

