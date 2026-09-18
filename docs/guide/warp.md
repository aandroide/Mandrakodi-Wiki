[:material-book-open-page-variant: Torna alle Guide](../guide/tutorials.md){ .md-button .md-button--primary }  [:material-home: Torna alla Home](../index.md){.md-button .md-button--primary} [:material-face-agent: Assistenza](../ask_help.md){ .md-button .md-button--primary }

------

!!! tip "WARP"
    I links con dicitura "**WARP**" *esigono* l'utilizzo di Software/App  <br>    - **Warp** è per *Pc Windows/macOS/Linux & Smartphone-Tablet Android/iOS* <a href="https://one.one.one.one/" target="_blank">(*si installa da qui*)</a> e **non richiede** alcuna configurazione, una volta avviato basta attivare il pulsante/cursore <br>    - **Wireguard** è per *Chiavette/Tv/Box/Firestick*, **necessita** del file ".conf" per funzionare correttamente (di seguito passaggi per configurazione e installazione) 

!!! warning "Attenzione"
    File ".conf" è utilizzabile su *più dispositivi contemporaneamente* da stessa rete e tra reti diverse <br> **Sconsigliamo** di **condividere** il proprio file .conf **con più utenti**, ad esagerare finisce che Cloudlfare poi impone un   file diverso per ogni dispositivo e pure per ogni tipologia di rete....<br> N.B.: con Warp/Wireguard **la velocità si abbassa inevitabilmente**, con dispositivi poco performanti si consiglia di abbassare la risoluzione video  tramite "inputstream-adaptive" come da [impostazioni consigliate](../guide/kodi_settings.md#mpd)

------

!!! important "Fase 1 - creare file configurazione per Wireguard"
    Creare file ".conf" **senza scadenza** da utilizzare in Wireguard su Chiavette/Tv/Box/Firestick

??? info "Web Config Generator + Web Convertitore per Wireguard"
       **Generare file ".conf" senza scadenza** (con Browser da Pc/Smartphone/Tablet - *non usare app Dowmloader*)

    * <a href="https://warp-generator.vercel.app" target="_blank">Config Generator</a>
    * Premere il pulsante "**Generate**" per generare la configurazione
    * Premere il pulsante "**Copy**" per copiare negli appunti la configurazione
    * <a href="/Mandrakodi-Wiki/guide/converter.html" target="_blank">Convertitore per Wireguard</a>
    * Nel box di testo "Input" **incollare** la configurazione
    * Premere il pulsante "**Converti**" per generare configurazione nel box di testo "Ouput"
    * Premere il pulsante "**Scarica file**" per salvare file "wireguard.conf"
    * N.B.: verificare che il file "wireguard" salvato abbia l'estensione "**.conf**" (se diversa, **rinominare** correggendo)

------

!!! important "Fase 2 - Wireguard per Chiavette/Tv/Box/Firestick"
    Play Store Chiavette/Tv/Box - Apk **Firestick** + File Manager

??? info "Wireguard + File Manager"
    **Chiavette/Tv/Box/Firestick**

    * **Chiavette/Tv/Box** 
    * Installare dal Play Store "Wireguard"
    * Installare dal Play Store "Total Commander - File Manager"<br>
    
    * **Firestick FireOs 6.x/7.x** 
    * Scaricare apk Wireguard <a href="https://download.wireguard.com/android-client/" target="_blank">"com.wireguard.android-x.x.xxxxxxxx.apk"</a>
    * installare dallo Store "Total Commander"<br>
    
    * Firestick con **Fire OS 5.x**
    * Scaricare [Wireguard Amdroid 5](https://github.com/campipaolo/Mandrakodi-Wiki/releases/download/Files/WireGuard_1_0_20210924_Android5.apk)

------

!!! important "Fase 3 - Localsend"
    **Inviare** a Chiavette/Tv/Box/Firestick  file ".conf"  e  Apk Wireguard

??? info "Localsend"
    **Windows/macOS/Linux/Android/iOS/Chiavette/Tv/Box/Firestick**

    * Installare "Localsend" su **entrambi** i dispositivi "mittente" e "ricevente"
    * <a href="https://localsend.org/it/download" target="_blank">Loalsend</a>  Windows/macOS/Linux/Android/iOS/Chiavette/Tv/Box/Firestick<br>
    * Firestick con **Fire OS 5.x.x.x**: [LocalSend Android 5](https://github.com/campipaolo/Mandrakodi-Wiki/releases/download/Files/LocalSend_1_8_0_Android5.apk)<br>
    * Avviare Localsend **prima** sul dispositivo "ricevente" e **poi** su quello "mittente"
    * Sul dispositivo "mittente" premere "Invia" e poi "File" 
    * Selezionare files da inviare
    * Selezionare dispositivo "ricevente"
    * Sul dispositivo "ricevente" dare conferma per ricevere  
    * N.B.: la cartella "**Download**" è quella di default per la ricezione dei files
    * Sul dispositivo "ricevente" in alto a destra l'icona a fianco alla “i” elenca la cronologia

------

!!! important "Fase 4 - Installare Wireguard  su  Firestick"
    **Installazione** Wireguard su **Firestick**

??? info "Wireguard su Firestick"
    **Firestick**


    * Avviare Total Commander
    * Recarsi nella cartella "Download"
    * Total Commander richiede conferma di accedere e di avere i permessi del caso, accettare
    * Cliccare sul file apk di Wireguard
    * Installare Wireguard e *NON avviarlo*

------

!!! important " Fase 5 - Configurare Wireguard"
    **Impostare** Wireguard su Chiavette/Tv/Box/Firestick

??? info "Wireguard"
    **Chiavette/Tv/Box/Firestick**


    * **Chiavette/Tv/Box & Firestick FireOs 6.x/7.x**
    * Avviare Total Commander
    * Recarsi nella cartella "Download"
    * Cliccare sul file ".conf"
    * Selezionare "Apri con"
    * Selezionare app Wireguard
    * Cliccare sulla configurazione importata per attivare/disattivare 
    * Al primo avvio verrà chiesta conferma di attivazione
    * Quando attiva, la configurazione selezionata appare blu con scritto "rx" "tx" [(Foto)](../images/wireguard_test.jpg){ target="_blank" }
    <br>
    * **Firestick FireOs 5.x**
    * Avviare Wireguard
    * Premere il pulsante "+" [(Foto)](../images/wireguard_home.jpg){ target="_blank" } <br>
    * Navigare nella cartella "Download" e selezionare il file ".conf"
    * Cliccare sulla configurazione importata per attivare/disattivare 
    * Al primo avvio verrà chiesta conferma di attivazione
    * Quando attiva, la configurazione selezionata appare blu con scritto "rx" "tx" [(Foto)](../images/wireguard_test.jpg){ target="_blank" }



------

!!! important " EXTRA - WG Tunnel (sempre con file ".conf")"
    Installare **alternativa** "WG Tunnel" su Windows/Linux/Android/Chiavette/Tv/Box/Firestick

??? info "WG Tunnel"
    **Windows/Linux/Android/Chiavette/Tv/Box/Firestick**


    * Installare WG Tunnel
    * <a href="https://github.com/wgtunnel/android/releases/latest" target="_blank">Chiavette/Tv/Box/Firestick 32bit</a> (wgtunnel-standalone-vx.x.x-armv7.apk)
    * <a href="https://github.com/wgtunnel/android/releases/latest" target="_blank">Smartphone/Tablet 64bit</a> (wgtunnel-standalone-vx.x.x-armv64.apk)
    * <a href="https://github.com/wgtunnel/desktop/releases/latest" target="_blank">Windows 64bit</a></a> (wgtunnel-x.x.x.x64.msix)
    * <a href="https://github.com/wgtunnel/desktop/releases/latest" target="_blank">Linux 64bit</a> (wgtunnel_x.x.x_amd64.deb)
    * Avviare WG Tunnel
    * Alla prima apertura, WG Tunnel potrebbe chiedere il permesso di accedere ai file
    * Aperto WG Tunnel, premere il pulsante "**+**" e selezionare l'opzione "**importa da file**
    * Importato il file ".conf", sarà presente nella schermata principale 
    * Cliccare l'interruttore in corrispondeza sulla destra per attivare/disattivare 
    * Al primo avvio verrà chiesta conferma di attivazione 

