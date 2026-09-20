[:material-book-open-page-variant: Torna alle Guide](../guide/tutorials.md){ .md-button .md-button--primary }  [:material-home: Torna alla Home](../index.md){.md-button .md-button--primary} [:material-face-agent: Assistenza](../ask_help.md){ .md-button .md-button--primary }

------

!!! tip "DNS: questi sconosciuti"

❓ Cosa c'entra con KODI/MANDRAKODI?

La maggior parte dei siti di streaming italiani non ha server in Italia: la magistratura, non potendo chiuderli, chiede a tutti i provider Internet di oscurarli, ossia di cancellare i record dei siti dal loro database
In questo modo, chiunque usi i loro DNS (tutti in pratica) non riuscirà a raggiungerli
Alcuni siti cercano di contrastare questi continui oscuramenti cambiando dominio di frequente (pertanto a volte potrebbero andare, a volte no), altri invece hanno proprio rinunciato a modificarlo<br>
Per provare se il vostro problema sia davvero legato ai DNS basta visitare con un browser lo stesso sito (esempio https://1.dlhd.sx)<br>
Se la pagina non si apre, o se vi compare la scritta che il sito è sotto sequestro, avete i DNS di default

❓ Come posso RISOLVERE?
Basta **cambiare** server DNS, impostandone uno che non oscura

!!! warning "DNS: obbligatori al giorno d'oggi!"
    Mandrakodi, come anche altri addon, non fa altro che visitare i vari siti per estrapolarne il contenuto, anch'esso **senza** aver impostato i **DNS**, **non** sarà in grado di **raggiungere** i vari **siti** delle porprie fonti web

------

!!! important "DNS suggeriti"    
    <span id="dns"></span>Di seguito elenco DNS suggeriti per rete **fissa** e **mobile** (scegliere uno dei due proposti)

??? info "DNS rete fissa"
    **Elenco DNS**

    * Opendns formato **IPV4**:<br>
      208.67.222.222<br>
      208.67.220.220
    
    * Opendns formato **IPV6**:<br>
      2620:119:35::35<br>
      2620:119:53::53
    
    * Cloudflare formato **IPV4**:<br>
      1.1.1.1<br>
      1.0.0.1
    
    * Cloudflare formato **IPV6**:<br>
      2606:4700:4700::1111<br>
      2606:4700:4700::1001

??? info "DNS  rete mobile"
    **Elenco DNS**

    * Opendns:<br>
      dns.opendns.com
      
    * Cloudflare:<br> 
      1dot1dot1dot1.cloudflare-dns.com 

------

!!! important "Guide per router di rete fissa"
    Di seguito guide per impostare i DNS sui router dei principali Internet Service Provider Italiani (menù/voci **potrebbero variare leggermente** a seconda del modello e del firmware cambiato nel tempo)

??? info "Vodafone"
    **Vodafone Station FTTC e FTTH**

    * Con un browser (Chrome, Firefox, ecc.) da un dispositivo connesso alla Station 
    * Digitare nella barra degli indirizzi: http://vodafone.station/ 
    * Inserire le credenziali di accesso 
      Se non sono state cambiate, si trovano sull'etichetta posta sotto / lato della Station 
    * Nell'angolo in alto a destra un menu a tendina,  o un pulsante che mostri la modalità  attuale (es. "Modalità base"), selezionare “**Modalità Utente Esperto**” 
    * Nel menu a sinistra o in alto, cliccare su "Internet" 
    * All'interno di questa sezione, cliccare la voce "DNS" 
    * Nella sezione “**DNS Sicuro**”, selezionare “**Manuale**” 
    * Appena sotto attivare opzione “Configura il DNS per tutti i tuoi dispositivi” 
    * Inserire i dns sia in formato **IPV4** che **IPV6** 
    * Salvare i cambiamenti premendo il pulsante “**Applica**” 
    * Riavviare Vodafine Station 
    * Eseguire <a href="https://dnsleaktest.com" target="_blank">test dns</a>
    * Selezionare "Extended test" e attendere, deve segnare ISP con nome dei dns impostati



??? info "Iliad"
    **IliadBox FTTH**

    * Con un browser (Chrome, Firefox, ecc.) da un dispositivo connesso alla Station 
    * Digitare nella barra degli indirizzi: 192.168.1.254 
    * Effettuare l’accesso al pannello di gestione dell’iliadbox inserendo la password scelta
    * Doppio clic sull’icona Parametri della iliadbox
    * Cliccare su ""**Modalità avanzata**"" 
    * Doppio clic su "**DHCP**"" 
    * Selezionare scheda Server DHCP 
    * Inserire dns primario e secondario in formato **IPV4** 
    * Cliccare su Salva e poi su OK 
    * Doppio clic su "**Configurazione IPv6**" 
    * Selezionare scheda DNS IPv6 
    * Spuntare la voce "**Forza l’uso di server DNS IPv6 personalizzati**" 
    * Inserire dns primario e secondario in formato **IPV6** 
    * Eseguire <a href="https://dnsleaktest.com" target="_blank">test dns</a>
    * Selezionare "Extended test" e attendere, deve segnare ISP con nome dei dns impostati



??? info "Fastweb"
    **Fastweb FTTH**

    * Con un browser (Chrome, Firefox, ecc.) da un dispositivo connesso alla Station 
    * Digitare nella barra degli indirizzi: 192.168.1.254
    * Nell'angolo in alto a destra un menu a tendina,  o un pulsante che mostri la modalità attuale (es. "Modalità base"), selezionare “**Modalità Utente Esperto**” 
    * Cliccare sulla scheda “**Internet**”
    * Nella sezione “DNS & DDNS”  disabilitare “**DNS protetto**”
    * Salvare le modifiche 
    * Sui vari dispositivi ricreare connessione alla rete Fastweb in modalità avanzata 
    * Sui vari dispositivi impostare manualmente i Dns 
    * Eseguire <a href="https://dnsleaktest.com" target="_blank">test dns</a>
    * Selezionare "Extended test" e attendere, deve segnare ISP con nome dei dns impostati



??? info "Poste"
    **Poste FTTH**

    * Con un browser (Chrome, Firefox, ecc.) da un dispositivo connesso alla Station 
    * Digitare l'indirizzo IP del router ed inserire le credenziali, indicate nell'etichetta sul router
    * In alto premere su “**Rete Locale**”
    * Sulla sinistra premere su ”LAN”
    * Sulla destra selezionare “**Server DHCP**” 
    * Nella sezione “ISP DNS” premere “**Off**” 
    * Inserire i  Dns in formato **IPV4** 
    * Salvare le modifiche
    * Eseguire <a href="https://dnsleaktest.com" target="_blank">test dns</a>
    * Selezionare "Extended test" e attendere, deve segnare ISP con nome dei dns impostati



??? info "WINDTRE"
    **WINDTRE FTTC e FTTH**

    * Verificare se attivo il servizio “Più Sicuri Casa & Ufficio controlla” 
    * Da browser digitare l’indirizzo https://test.sicurezzaw3.it 
    * Se attivo disattivarlo da app windtre / area clienti / servizio clienti
    * Con un browser (Chrome, Firefox, ecc.) da un dispositivo connesso al Router
    * Digitare l'indirizzo IP del router ed inserire le credenziali, indicate nell'etichetta sul router 
    * Accedere  al menu di configurazione tramite il pulsante (tre linee in alto a destra) 
    * Selezionare  sezione “Network”  e poi  “**Rete Locale LAN**”
    * Scorrere le impostazioni fino alla sezione “Valori DNS” impostare DNS su “**DNS statico**” 
    * nserire i dns in formato **IPV4**
    * Salvare la configurazione cliccando sul tasto “Applica” 
    * Eseguire <a href="https://dnsleaktest.com" target="_blank">test dns</a>
    * Selezionare "Extended test" e attendere, deve segnare ISP con nome dei dns impostati



??? info "Aruba"
    **Aruba  FTTH**

    * N.B.: necessario richiedere **IP Pubblico Dinamico** con una tantum €10 
    * Con un browser (Chrome, Firefox, ecc.) da un dispositivo connesso al Router 
    * Digitare nella barra degli indirizzi: 192.168.1.1 
    * fare login come utente "admin",  tutta la stringa dopo la voce "D-SN", dopo l'ultimo carattere della stringa, scrivere "@aruba" (in minuscolo) riportata sul retro del router
    * Gestione e diagnosi, **Ipv6 Switch**
    * **Abilitazione IPv6**: off 
    * Rete locale, LAN, **IPv4**, Server DHCP
    * Server DHCP: ON
    * ISP dns: OFF 
    * DNS Primario: inserire DNS primario in formato **Ipv4** 
    * DNS Secondario: inserire DNS primario in formato **Ipv4** 
    * Eseguire <a href="https://dnsleaktest.com" target="_blank">test dns</a>
    * Selezionare "Extended test" e attendere, deve segnare ISP con nome dei dns impostati



??? info "Edison"
    **Edison  FTTC e FTTH**

    * Dns non si possono inserire né sul router dell’operatore né sul singolo dispositivo poiché non vengono comunque accettati, è possibile con:
    * Solo Router di proprietà (rifare i passaggi di attivazione seguendo link inviato via mail al momento dell'attivazione linea)
    * Router di proprietà in cascata a quello dell'operatore (dns da inserire su quello di proprietà)



??? info "Tim"
    **Tim FTTC e FTTH**

    * Dns non si possono inserire sul router dell’operatore 
    * Inserirli sul **singolo dispositivo** (SOLO Dns Opendns)




??? info "SKY Wifi"
    **SKY Wifi  FTTH**

    * Dns non si possono inserire né sul router dell’operatore  né sul singolo dispositivo poiché non vengono comunque accettati
    * Usare app "Dns Changer" o simili



??? info "Eolo"
    **Eolo FWA**

    * Dns non si possono inserire né sul router dell’operatore  né sul singolo dispositivo poiché non vengono comunque accettati, è possibile con:
    * Router di proprietà in cascata a quello dell'operatore (dns da inserire su quello di proprietà) 
    * Router di proprietà richiedendo **IP Pubblico Statico** a €4,90 al mese



------

!!! important "DNS su singolo dipositivo"
    <span id="dnsdispositivo"></span>Di seguito guide per impostare i DNS sui **singolo dispositivo** ove router non disponga di opzione per inserirli al suo interno e per connessioni di rete mobile/hotspot 

??? info "Android Smartphone/Tablet (a seconda della marca e del modello, alcuni passaggi potrebbero essere diversi)"
    **Smartphone/Tablet**

    * Impostazioni, rete e internet
    * In alto a destra premere su icona a forma di matita (modifica impostazioni) 
    * Se attivo disattivarlo da app windtre / area clienti / servizio clienti
    * Nella sezione “Impostazioni IP” selezionare “**IP Statico**”
    * Nella sezione “Gateway” inserire ip del proprio router (es. 192.168.1.1)
    * Nella sezione “Lunghezza prefisso rete” inserire “24”
    * Nella sezione “Indirizzo IP” inserire ip diverso da Gateway (es. 192.168.1.10)
    * Nelle sezioni “DNS 1” e “DNS 2” inserire Dns primario e secondario
    * Inserire i dns in formato **IPV4**
    * Salvare le impostazioni 
    * Eseguire <a href="https://dnsleaktest.com" target="_blank">test dns</a>
    * Selezionare "Extended test" e attendere, deve segnare ISP con nome dei dns impostati

??? info "Android Tv/Chiavette/Box"
    **Tv/Chiavette/Box**

    * Impostazioni (icona a forma di ingranaggio in alto a destra)
    * Rete Internet 
    * Selezionare la propria connessione wifi
    * Nella sezione “Impostazioni IP” e selezionare “**Statico**”
    * Nella sezione “Indirizzo IP” inserire ip diverso da quello del proprio router
    * Nella sezione “Lunghezza prefisso rete” inserire “24”
    * Nelle sezioni “DNS 1” e “DNS 2” inserire Dns primario e secondario
    * Inserire i dns in formato **IPV4**
    * Salvare le impostazioni 
    * Eseguire <a href="https://dnsleaktest.com" target="_blank">test dns</a>
    * Selezionare "Extended test" e attendere, deve segnare ISP con nome dei dns impostati

??? info "Firestick"
    **Chiavette Firestick Fire OS** 

    * Cliccare su "Impostazioni"
    * Selezionare "Sistemi" 
    * Selezionare "WI-FI"
    * Selezionare la tua rete WI-FI e **dimentica la rete WI-FI** premendo il pulsante con 3 linee
    * Nella sezione “Indirizzo IP” inserire ip diverso da quello del proprio router
    * Premere il pulsante di selezione
    * Selezionare la propria rete WI-FI
    * Immettere la psw WI-FI e fare clic su "Avanzate"
    * Inserire ip diverso da quello del proprio router 
    * Per il “Gateway” predefinito, inserire ip del proprio router (es. 192.168.1.1)
    *  Inserire '24' per 'Lunghezza prefisso di rete' e fare clic su 'Avanti'
    * Inserire i dns in formato **IPV4**
    * Eseguire <a href="https://dnsleaktest.com" target="_blank">test dns</a>
    * Selezionare "Extended test" e attendere, deve segnare ISP con nome dei dns impostati



??? info "Rete mobile/Hotspot (a seconda della marca e del modello, alcuni passaggi potrebbero essere diversi)"
    **Smartphone/Tablet Android**

    * Impostazioni, rete e internet
    * Selezionare “DNS Privato”
    * Selezionare “Nome host del provider DNS Privato”
    * Inserire DNS per rete mobile
    * Eseguire <a href="https://dnsleaktest.com" target="_blank">test dns</a>
    * Selezionare "Extended test" e attendere, deve segnare ISP con nome dei dns impostati



