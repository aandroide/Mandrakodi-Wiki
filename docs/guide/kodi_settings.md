[:material-book-open-page-variant: Torna alle Guide](../guide/tutorials.md){ .md-button .md-button--primary }  [:material-home: Torna alla Home](../index.md){.md-button .md-button--primary}  [:material-face-agent: Assistenza](../ask_help.md){ .md-button .md-button--primary }

------

!!! tip "Impostazioni Kodi"
    **Settaggi consigliati** per migliori prestazioni dei vari flussi video 

------

!!! important "Players Esterni"
    <span id="players"></span>A partire da Kodi 21.2 per riprodurre flussi video è possibile sfruttare **players esterni** (es. Ace, Vlc, Mx Player, Wuffy Player, ecc)  più stabili del player interno di kodi molto "sensibile" ai flussi streaming <br>Vale sia per *Android* su Smartphone/Tablet/Chiavette/Tv/Box/Firestick che per *Pc* Windows, di seguito i passaggi

!!! warning "Installare i vari players esterni"
    I players esterni (es. Ace, Mx Player, Wuffy Player,  ecc) vanno **prima** installati sul dispositivo<br>

   Mx Player (Android) [Tv/Chiavette/Box/Firestick](https://github.com/campipaolo/Mandrakodi-Wiki/releases/download/Files/mx-player-32bit.apk)<br>    Mx Player (Android) [Smartphone/Tablet](https://github.com/campipaolo/Mandrakodi-Wiki/releases/download/Files/mx-player-64bit.apk)<br>    Wuffy Player (Android) [Tv/Chiavette/Box/Firestick](https://github.com/campipaolo/Mandrakodi-Wiki/releases/download/Files/wuffy-player-32bit.apk)<br>    Wuffy Player (Android) [Smartphone/Tablet](https://github.com/campipaolo/Mandrakodi-Wiki/releases/download/Files/wuffy-player-64bit.apk
    )<br>    Ace (Android/Windows/Linux) [(Guida installazione)](../guide/acestream.md/)

??? info "Impostare Players Esterni su Android Smartphone/Tablet/Chiavette/Tv/Box/Firestick"
    **Avviare Kodi**

    * Entrare in Mandrakodi, sezione “**HELP ME!**”
    * Cliccare "PLAYER .XML (org.free.aceserve)" e confermare
    * Uscire da Kodi e rientrare, accedere a Mandrakodi
    * Selezionare canale (verificare se dispone di seconda pagina con link all'interno)
    * Tenere premuto sul link e selezionare voce "**riproduci con**" [(Foto)](../images/kodi_riproduci_con.png){ target="_blank" }
    * Dall'elenco selezionare player installato

??? info "Impostare Players Esterni su Pc Windows"
    **In Windows**

    * Scaricare <a href="https://github.com/campipaolo/Mandrakodi-Wiki/releases/download/Files/playercorefactory_windows.xml" target="_blank">playercorefactory_windows.xml</a> tasto destro/tenere prenuto sul link e salvare
    * **Rinominare** il file in "playercorefactory.xml" 
    * Con esplora file **abilitare** la visualizzazione di file e cartelle nascoste
    * Copiare il file nel percorso “C:/utenti/**tuonomeutente**/appdata/roaming/kodi/userdata”
    * Entrare in Mandrakodi
    * Selezionare canale (verificare se dispone di seconda pagina con link all'interno)
    * Tenere premuto sul link e selezionare voce "**riproduci con**" [(Foto)](../images/kodi_riproduci_con.png){ target="_blank" }
    * Dall'elenco selezionare player esterno



------

!!! important "Flussi MPD"
    I link MDP sfruttano la libreria di kodi "**inputstream-adaptive**" che *regola automaticamente* la risoluzione video del flusso a seconda della propria connessione e del dispositivo <br> E' possibile sia impostare dei valori min/max sia **selezionare** una **risoluzione video** a piacimento tra quelle disponibili per ogni flusso video<br> N.B.: questi link *sono fruibili solo con il player interno di kodi*, i players esterni non li gestiscono

??? info "Impostazioni Flussi MPD"
    **Avviare Kodi**

    * Impostazioni, "Addon", "I miei addon", "**Lettore Video Inputstream**", Inputstream Adaptive" 
    * "Lettore Video Inputstream", "Inputstream Adaptive", "**Configura**"
    * Tipo selezione del flusso: "**OSD manuale**"
    * Risoluzione massima:  "1080p"
    * Risoluzione massima per video DRM:  "1080p"
    * Premere "OK" per confermare [(Foto)](../images/kodi_inputstream_adaptive.png){ target="_blank" }

!!! warning "Come cambiare risoluzione video"
    Mentre si è in *play*, tasto centrale del telecomando o toccare touch smartphone <br> In basso a destra icona a forma di ingranaggio, "impostazioni video", "traccia video' <br> Si apre finestra con **elenco** delle varie **risoluzioni video disponibili** da poter selezionare

------

!!! important "Flussi DaddyLive"
    I canali **DaddyLive**, utilizzano il plugin **inputstream.ffmpegdirect**.
    Questo plugin, di default, utilizza la funzione **TimeShift** per permettere il **riavvolgimento** della live<br>  Per farlo, salva dei file nella cartella di Kodi che vengono cancellati quando si ferma il video. <br>  Su device con poca memoria (esempio la FireStick), può creare problemi 

??? info "Impostazioni Flussi DaddyLive"
    **Avviare Kodi**

    * Tenere premuto/tasto destro su icona dell'addon Mandrakodi 
    * "Impostazioni"
    * Sezione "**Personal List**" poi "**app02**"
    * All'interno scrivere "no_time_shift"
    * Premere "OK" per confermare [(Foto)](../images/daddylive_no_time_shift.jpg){ target="_blank" }
    * Uscire da Kodi e rientrare

------

!!! important "Buffer/Cache"
    Kodi ha un suo sistema interno per gestire **cache con modalità buffer** per impostare una dimensione memoria per varie tipologie di flussi online/locali

??? info "Impostazioni Buffer/Cache"
    **Avviare Kodi**

    * Impostazioni, "**Servizi**"
    * In basso a sinistra cliccare sul pulsante "Base" fino a selezionare "Esperto"
    * Sulla sinistra compare il menu "**Cache**"
    * Modalità Buffer: selezionare "Buffer di tutti i file system di rete"
    * Dimensione Memoria: "48 MB"
    * Premere "OK" per confermare [(Foto)](../images/Kodi_cache.png){ target="_blank" }
    * Uscire da Kodi e rientrare

!!! warning "Attenzione"
    Si ricorda che, in ogni caso, **quando il server della fonte è sovraccarico il buffering persiste comunque**



