---
layout: page
title: Segnalazioni
---

[:material-face-agent: Torna ad Assistenza](../ask_help.md){ .md-button .md-button--primary }  [:material-home: Torna alla Home](../index.md){ .md-button .md-button--primary } [:material-comment-question: FAQ](../ask_help.md){ .md-button .md-button--primary }

---

!!! tip "Segnalazioni"
    Da questa pagina è possibile inviare segnalazioni oltre che monitorarne lo stato<br>Ad ogni apertura viene caricato la tabella "Segnalazioni Attive" con le segnalazioni eventualmente aperte, mentre quando risolte vengono automaticamente eliminate dall'elenco<br>Non  esiste una tempistica certa in merito alla risoluzione della segnalazione stessa, dipende dalla complessità in base a cambiamenti/contromisure della fonte da cui l'addon attinge facendo l'estrapolazione

!!! warning "ATTENZIONE"
    Le segnalazioni vanno fatte solamente quando è TUTTA LA SEZIONE non funzionante e NON per alcuni link non funzionanti (un singolo link, tra tutti quelli presenti, può avere il flusso offline)

!!! important "Compilare form "Invia Nuova Segnalazione""
    - Attendere il caricamento completo delle "Segnalazioni Attive" (in caso di errore, premere il pulsante per ricaricare l'elenco)
    - Compilare il form in tutte le sue parti, diversamente non verrà inviato (attendere sempre il caricamento delle voci nei menù a discesa)
    - Dopo l'invio della segnalazione, la tabella "Segnalazioni Attive" si aggiorna automaticamente senza dover ricaricare la pagina<br>
    - N.B.: eventuali segnalazioni già presenti non verranno inviate e registrate (quando non presenti segnalazioni viene mostrato messaggio di "Nessuna segnalazione aperta")

<style>
  .ticket-container { max-width: 800px; margin: 0 auto; font-family: Arial, sans-serif; color: #fff; }
  .ticket-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }
  .ticket-table { width: 100%; border-collapse: collapse; text-align: left; background: #1e1e1e; color: #fff; border-radius: 8px; overflow: hidden; margin-bottom: 30px; }
  .ticket-table th, .ticket-table td { padding: 10px; border-bottom: 1px solid #333; }
  .ticket-table th { background: #333; }
  .ticket-form { background: #252526; padding: 20px; border-radius: 8px; }
  .form-group { margin-bottom: 15px; }
  .form-group label { display: block; margin-bottom: 5px; font-weight: bold; }
  .form-control { width: 100%; padding: 10px; background: #333; color: #fff; border: 1px solid #555; border-radius: 4px; box-sizing: border-box; }
  .btn-submit { width: 100%; padding: 12px; background: #107c41; color: white; border: none; border-radius: 4px; font-weight: bold; cursor: pointer; font-size: 16px; }
  .btn-refresh { padding: 6px 12px; background: #252526; color: #fff; border: 1px solid #555; border-radius: 4px; cursor: pointer; font-size: 14px; display: none; align-items: center; gap: 5px; }
  .btn-refresh:hover { background: #333; }
  .btn-reset-form { margin-top: 10px; padding: 8px 15px; background: #107c41; color: white; border: none; border-radius: 4px; cursor: pointer; font-weight: bold; font-size: 14px; }
  .status-msg { margin-top: 15px; padding: 10px; border-radius: 4px; display: none; text-align: center; }
</style>

<div class="ticket-container">
  <div class="ticket-header">
    <h3>📋 Segnalazioni Attive</h3>
    <button id="btn-refresh-list" class="btn-refresh">🔄 Aggiorna Elenco</button>
  </div>
  <table class="ticket-table">
    <thead>
      <tr>
        <th>Data</th>
        <th>Sezione</th>
        <th>Contenuto</th>
        <th>Problema</th>
        <th>Stato</th>
      </tr>
    </thead>
    <tbody id="tabella-segnalazioni">
      <tr>
        <td colspan="5" style="text-align: center;">Caricamento in corso...</td>
      </tr>
    </tbody>
  </table>

  <div class="ticket-form">
    <h3>📌 Invia Nuova Segnalazione</h3>
    <form id="form-segnalazione">

      <!-- Livello 1: Categoria Madre -->
      <div class="form-group">
        <label for="categoria-principale">Categoria Madre (Obbligatorio):</label>
        <select id="categoria-principale" class="form-control" required>
          <option value="">-- Seleziona Categoria --</option>
          <option value="Sport">Sport</option>
          <option value="Live">Live</option>
          <option value="On Demand">On Demand</option>
          <option value="Radio">Radio</option>
        </select>
      </div>
    
      <!-- Livello 2: Sotto-Categoria -->
      <div class="form-group">
        <label for="sotto-categoria">Sotto-Categoria (Obbligatorio):</label>
        <select id="sotto-categoria" class="form-control" required>
          <option value="">-- Seleziona Prima Categoria --</option>
        </select>
      </div>
    
      <!-- Livello 3: Contenuto / Lista -->
      <div class="form-group" id="group-contenuto" style="display: none;">
        <label for="contenuto-lista">Contenuto / Lista Specifica:</label>
        <select id="contenuto-lista" class="form-control">
          <option value="">-- Seleziona Contenuto --</option>
        </select>
      </div>
    
      <!-- Livello 4: Dettaglio / Nazione -->
      <div class="form-group" id="group-dettaglio" style="display: none;">
        <label for="dettaglio-lista">Dettaglio Nazione:</label>
        <select id="dettaglio-lista" class="form-control">
          <option value="">-- Seleziona Nazione --</option>
        </select>
      </div>
    
      <div class="form-group">
        <label for="problema">Tipo di Problema (Obbligatorio):</label>
        <select id="problema" class="form-control" required>
          <option value="INTERA sezione offline (NON singolo link)" selected>INTERA sezione offline (NON singolo link)</option>
        </select>
      </div>
    
      <div class="form-group">
        <label for="piattaforma">Dispositivo / Piattaforma (Obbligatorio):</label>
        <select id="piattaforma" class="form-control" required>
          <option value="">-- Seleziona Dispositivo --</option>
          <option value="Android Tv/Chiavette/Box">Android Tv/Chiavette/Box</option>
          <option value="Fire Tv Stick/Fire Cube Tv">Fire Tv Stick/Fire Cube Tv</option>
          <option value="Pc Windows/Mac/Linux">Pc Windows/Mac/Linux</option>
          <option value="Smartphone-Tablet Android / iPhone-iPad">Smartphone-Tablet Android / iPhone-iPad</option>
          <option value="RPI-Pc LibreElec">RPI-Pc LibreElec</option>
        </select>
      </div>
    
      <div style="margin-bottom: 20px; background: #3a2e12; border: 1px solid #ffa000; padding: 12px; border-radius: 6px;">
        <label style="cursor: pointer; display: flex; align-items: flex-start; gap: 10px;">
          <input type="checkbox" id="check-conferma" required style="margin-top: 3px;">
          <span><strong>Confermo:</strong>  la segnalazione riguarda <strong>TUTTA LA SEZIONE</strong> non funzionante e NON solamente per alcuni link offline</span>
        </label>
      </div>
    
      <button type="submit" id="btn-invia" class="btn-submit">Invia Segnalazione</button>
      <div id="messaggio-stato" class="status-msg"></div>
    </form>

  </div>
</div>

<script>
(function() {
  var SCRIPT_URL = "https://script.google.com/macros/s/AKfycbwTQJzxvLspR-1GdYh1wOXSLrF8h4TIeswEAIUJGtM9z1I4pIUZD3N_ANO2oewKmaI/exec";
  var rawData = null;
  var isMenuLoading = false;

  function init() {
    loadReports();
    loadMenu();
    document.getElementById("btn-refresh-list").addEventListener("click", loadReports);
    document.getElementById("categoria-principale").addEventListener("change", onCatChange);
    document.getElementById("sotto-categoria").addEventListener("change", onSubChange);
    document.getElementById("contenuto-lista").addEventListener("change", onContChange);
    document.getElementById("form-segnalazione").addEventListener("submit", onSubmit);
  }

  function resetForm() {
    document.getElementById("form-segnalazione").reset();
    var msg = document.getElementById("messaggio-stato");
    msg.style.display = "none";
    msg.innerHTML = "";
    onCatChange();
  }

  function loadReports() {
    var tbody = document.getElementById('tabella-segnalazioni');
    var btnRefresh = document.getElementById("btn-refresh-list");
    if (!tbody) return;

    if (btnRefresh) {
      btnRefresh.disabled = true;
      btnRefresh.textContent = "⏳ Aggiornamento...";
    }
    
    var cacheBuster = "&_ts=" + new Date().getTime();
    
    fetch(SCRIPT_URL + "?action=getOpen" + cacheBuster, { method: "GET" })
      .then(function(res) { return res.json(); })
      .then(function(data) {
        tbody.innerHTML = '';
        
        if (data && data.error) {
          if (btnRefresh) {
            btnRefresh.style.display = "inline-flex";
            btnRefresh.disabled = false;
            btnRefresh.textContent = "🔄 Aggiorna Elenco";
          }
          tbody.innerHTML = '<tr><td colspan="5" style="text-align: center; color: #ff5252;">⚠️ Impossibile caricare l\'elenco. Riprova con il tasto in alto.</td></tr>';
          return;
        }
    
        if (btnRefresh) {
          btnRefresh.style.display = "none";
          btnRefresh.disabled = false;
          btnRefresh.textContent = "🔄 Aggiorna Elenco";
        }
    
        if (!data || data.length === 0) {
          tbody.innerHTML = '<tr><td colspan="5" style="text-align: center; color: #4caf50; font-weight: bold; background: #1b3e20; padding: 15px;">✅ Nessuna segnalazione aperta al momento.</td></tr>';
          return;
        }
    
        data.forEach(function(item) {
          var st = (item.stato || '').toUpperCase();
          var bgStyle = "background: #ff9800; color: #000;";
    
          if (st === "OFFLINE") {
            bgStyle = "background: #d32f2f; color: #fff;";
          } else if (st === "IN LAVORAZIONE") {
            bgStyle = "background: #0288d1; color: #fff;";
          }
    
          tbody.innerHTML += '<tr>' +
            '<td>' + (item.data || '') + '</td>' +
            '<td><span style="background: #444; padding: 3px 8px; border-radius: 4px;">' + (item.sezione || '') + '</span></td>' +
            '<td><strong>' + (item.contenuto || '') + '</strong></td>' +
            '<td>' + (item.problema || '') + '</td>' +
            '<td><span style="' + bgStyle + ' padding: 3px 8px; border-radius: 4px; font-weight: bold;">' + (item.stato || 'In attesa') + '</span></td>' +
          '</tr>';
        });
      })
      .catch(function(err) {
        console.error("Errore caricamento segnalazioni:", err);
        if (btnRefresh) {
          btnRefresh.style.display = "inline-flex";
          btnRefresh.disabled = false;
          btnRefresh.textContent = "🔄 Aggiorna Elenco";
        }
        tbody.innerHTML = '<tr><td colspan="5" style="text-align: center; color: #ff5252;">⚠️ Errore di connessione. Riprova con il tasto in alto.</td></tr>';
      });
  }

  function loadMenu(callback) {
    isMenuLoading = true;
    var cacheBuster = "&_ts=" + new Date().getTime();

    fetch(SCRIPT_URL + "?action=getMenu" + cacheBuster, { method: "GET" })
      .then(function(res) { return res.json(); })
      .then(function(data) { 
        rawData = data || {}; 
        isMenuLoading = false;
        if (callback) callback(true);
      })
      .catch(function(err) { 
        console.error("Errore recupero menu:", err); 
        rawData = null;
        isMenuLoading = false;
        if (callback) callback(false);
      });
  }

  function getCategoryItems(catKey) {
    if (!rawData) return [];
    if (rawData[catKey]) return rawData[catKey];
    var keys = Object.keys(rawData);
    for (var i = 0; i < keys.length; i++) {
      if (keys[i].toLowerCase() === catKey.toLowerCase()) {
        return rawData[keys[i]];
      }
    }
    return [];
  }

  function onCatChange() {
    var cat = document.getElementById("categoria-principale").value;
    var subSel = document.getElementById("sotto-categoria");
    var groupCont = document.getElementById("group-contenuto");
    var groupDet = document.getElementById("group-dettaglio");

    subSel.innerHTML = '<option value="">-- Seleziona Sotto-Categoria --</option>';
    groupCont.style.display = "none";
    groupDet.style.display = "none";
    
    if (!cat) return;
    
    if (cat === "Sport") {
      var opts = ["Live Eventi", "Liste Canali", "Roja Tube", "Sport Replay"];
      opts.forEach(function(o) {
        var opt = document.createElement("option");
        opt.value = o; opt.textContent = o;
        subSel.appendChild(opt);
      });
    } else if (cat === "On Demand") {
      var opts = ["Movie Club", "Anime & Cartoon", "Old Tv", "Doctor Who", "Raiplay", "Pluto Tv", "Federmoto Tv", "MandraTube"];
      opts.forEach(function(o) {
        var opt = document.createElement("option");
        opt.value = o; opt.textContent = o;
        subSel.appendChild(opt);
      });
    } else if (cat === "Live" || cat === "Radio") {
      if (rawData) {
        populateSubCategories(cat);
      } else {
        subSel.innerHTML = '<option value="">⏳ Caricamento sotto-categorie in corso...</option>';
        loadMenu(function(success) {
          if (success) {
            populateSubCategories(cat);
          } else {
            subSel.innerHTML = '<option value="RETRY">⚠️ Connessione lenta. Clicca qui per Riprovare</option>';
          }
        });
      }
    }
  }

  function populateSubCategories(cat) {
    var subSel = document.getElementById("sotto-categoria");
    subSel.innerHTML = '<option value="">-- Seleziona Sotto-Categoria --</option>';

    var list = getCategoryItems(cat);
    if (!list || list.length === 0) {
      subSel.innerHTML = '<option value="">Nessuna sotto-categoria trovata</option>';
    } else {
      list.forEach(function(item) {
        var opt = document.createElement("option");
        opt.value = item; opt.textContent = item;
        subSel.appendChild(opt);
      });
    }
  }

  function renderContentOptions(cat, sub) {
    var contSel = document.getElementById("contenuto-lista");
    var groupCont = document.getElementById("group-contenuto");
    contSel.innerHTML = '<option value="">-- Seleziona Contenuto --</option>';

    if (cat === "Sport") {
      if (sub === "Live Eventi") {
        groupCont.style.display = "block";
        (getCategoryItems("Sport_LiveEventi") || []).forEach(function(i) {
          var opt = document.createElement("option");
          opt.value = i; opt.textContent = i;
          contSel.appendChild(opt);
        });
      } else if (sub === "Liste Canali") {
        groupCont.style.display = "block";
        (getCategoryItems("Sport_ListeCanali") || []).forEach(function(i) {
          var opt = document.createElement("option");
          opt.value = i; opt.textContent = i;
          contSel.appendChild(opt);
        });
      } else if (sub === "Sport Replay") {
        groupCont.style.display = "block";
        (getCategoryItems("Sport_Replay") || []).forEach(function(i) {
          var opt = document.createElement("option");
          opt.value = i; opt.textContent = i;
          contSel.appendChild(opt);
        });
      }
    } else if (cat === "On Demand") {
      if (sub === "Movie Club") {
        groupCont.style.display = "block";
        var movieOpts = ["Sala 1", "K-Drama", "Vod Iptv 1", "Vod Iptv 2"];
        movieOpts.forEach(function(i) {
          var opt = document.createElement("option");
          opt.value = i; opt.textContent = i;
          contSel.appendChild(opt);
        });
      }
    }
  }

  function onSubChange() {
    var cat = document.getElementById("categoria-principale").value;
    var subSel = document.getElementById("sotto-categoria");
    var sub = subSel.value;
    var contSel = document.getElementById("contenuto-lista");
    var groupCont = document.getElementById("group-contenuto");
    var groupDet = document.getElementById("group-dettaglio");

    if (sub === "RETRY") {
      onCatChange();
      return;
    }
    
    contSel.innerHTML = '<option value="">-- Seleziona Contenuto --</option>';
    groupCont.style.display = "none";
    groupDet.style.display = "none";
    
    if (!cat || !sub) return;
    
    if (rawData) {
      renderContentOptions(cat, sub);
    } else {
      groupCont.style.display = "block";
      contSel.innerHTML = '<option value="">⏳ Caricamento contenuti in corso...</option>';
      loadMenu(function(success) {
        if (success) {
          renderContentOptions(cat, sub);
        } else {
          contSel.innerHTML = '<option value="">⚠️ Errore di caricamento. Seleziona nuovamente la sotto-categoria.</option>';
        }
      });
    }
  }

  function onContChange() {
    var cat = document.getElementById("categoria-principale").value;
    var sub = document.getElementById("sotto-categoria").value;
    var cont = document.getElementById("contenuto-lista").value;
    var detSel = document.getElementById("dettaglio-lista");
    var groupDet = document.getElementById("group-dettaglio");

    detSel.innerHTML = '<option value="">-- Seleziona Nazione --</option>';
    groupDet.style.display = "none";
    
    if (cat === "Sport" && sub === "Liste Canali" && cont === "MPD (Nazioni)" && rawData) {
      groupDet.style.display = "block";
      (getCategoryItems("Sport_MPDNazioni") || []).forEach(function(i) {
        var opt = document.createElement("option");
        opt.value = i; opt.textContent = i;
        detSel.appendChild(opt);
      });
    }
  }

  function onSubmit(e) {
    e.preventDefault();
    var btn = document.getElementById("btn-invia");
    var msg = document.getElementById("messaggio-stato");

    var cat = document.getElementById("categoria-principale").value;
    var sub = document.getElementById("sotto-categoria").value;
    var cont = document.getElementById("contenuto-lista").value;
    var det = document.getElementById("dettaglio-lista").value;
    var prob = document.getElementById("problema").value;
    var plat = document.getElementById("piattaforma").value;
    
    var sezioneStr = [cat, sub].filter(Boolean).join(" > ");
    var contenutoFinale = det || cont || sub;
    
    var payload = {
      sezione: sezioneStr,
      contenuto: contenutoFinale,
      problema: prob,
      piattaforma: plat
    };
    
    btn.disabled = true;
    btn.textContent = "Invio in corso...";
    msg.style.display = "none";
    
    fetch(SCRIPT_URL, {
      method: "POST",
      redirect: "follow",
      headers: { "Content-Type": "text/plain;charset=utf-8" },
      body: JSON.stringify(payload)
    })
    .then(function(res) { return res.json(); })
    .then(function(data) {
      btn.disabled = false;
      btn.textContent = "Invia Segnalazione";
      msg.style.display = "block";
    
      if (data.result === "success") {
        msg.style.background = "#1b5e20";
        msg.style.color = "#fff";
        msg.innerHTML = "✅ Segnalazione inviata con successo!";
        resetForm();
        loadReports();
      } else if (data.result === "duplicate") {
        msg.style.background = "#b71c1c";
        msg.style.color = "#fff";
        msg.innerHTML = "⚠️ Risulta già una segnalazione attiva per questo contenuto.<br>" +
                        "<button type='button' id='btn-reset-dup' class='btn-reset-form'>🔄 Nuova Segnalazione</button>";
        
        var btnResetDup = document.getElementById("btn-reset-dup");
        if (btnResetDup) {
          btnResetDup.addEventListener("click", resetForm);
        }
      } else {
        msg.style.background = "#b71c1c";
        msg.style.color = "#fff";
        msg.innerHTML = "❌ Errore durante l'invio.";
      }
    })
    .catch(function() {
      btn.disabled = false;
      btn.textContent = "Invia Segnalazione";
      msg.style.display = "block";
      msg.style.background = "#b71c1c";
      msg.style.color = "#fff";
      msg.innerHTML = "❌ Errore di connessione.";
    });
  }

  if (document.readyState === "complete" || document.readyState === "interactive") {
    setTimeout(init, 1);
  } else {
    document.addEventListener("DOMContentLoaded", init);
  }
})();
</script>