---
layout: page
title: Segnalazioni
---

[:material-home: Torna alla Home](../){ .md-button .md-button--primary } [:material-comment-question: FAQ](faq/faq.md){ .md-button .md-button--primary }

<hr style="border: 0; border-top: 1px solid #444; margin: 20px 0;">

!!! tip "Segnalazioni"
    Da questa pagina è possibile inviare segnalazioni oltre che monitorarne lo stato<br>
    Ad ogni apertura viene caricato nel box "Segnalazioni Attive" le segnalazioi aperte, quando risolte vengono automaticamente eliminate dall'elenco<br>
    Non esiste una tempistica certa in mertio alla risoluzione della segnalazione stessa, dipende dalla complessità in base a cambiamenti/contromisure della fonte da cui l'addon attinge facendo l'estrapolazione.

!!! warning "ATTENZIONE"
    Le segnalazioni vanno fatte *solamente* quando è **TUTTA LA SEZIONE non funzionante** e NON per alcuni link non funzionanti (un singolo link, tra tutti quelli presenti, può avere il flusso offline)

!!! important "Compilare form "Invia Nuova Segnalazione""
    - Attendere il caricamento completo della pagina con le "Segnalazioni Attive"
    - Compilare il form in tutte le sue parti (diversamente non verrà inviato)
    - Se uno o più menù a discesa non caricano/risultano vuoti ricaricare la pagina
    N.B.: eventuali segnalazioni già presenti non verranno inviate e registrate

<style>
  .ticket-container { max-width: 800px; margin: 0 auto; font-family: Arial, sans-serif; color: #fff; }
  .ticket-table { width: 100%; border-collapse: collapse; text-align: left; background: #1e1e1e; color: #fff; border-radius: 8px; overflow: hidden; margin-bottom: 30px; }
  .ticket-table th, .ticket-table td { padding: 10px; border-bottom: 1px solid #333; }
  .ticket-table th { background: #333; }
  .ticket-form { background: #252526; padding: 20px; border-radius: 8px; }
  .form-group { margin-bottom: 15px; }
  .form-group label { display: block; margin-bottom: 5px; font-weight: bold; }
  .form-control { width: 100%; padding: 10px; background: #333; color: #fff; border: 1px solid #555; border-radius: 4px; box-sizing: border-box; }
  .btn-submit { width: 100%; padding: 12px; background: #107c41; color: white; border: none; border-radius: 4px; font-weight: bold; cursor: pointer; font-size: 16px; }
  .status-msg { margin-top: 15px; padding: 10px; border-radius: 4px; display: none; text-align: center; }
</style>

<div class="ticket-container">

  <h2>📋 Segnalazioni Attive</h2>
  <div style="overflow-x: auto;">
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
  </div>

  <hr style="border: 0; border-top: 1px solid #444; margin: 30px 0;">

  <h2>📌 Invia Nuova Segnalazione</h2>

  <form id="form-segnalazione" class="ticket-form">

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
        <option value="Android TV / Kodi">Android TV / Kodi</option>
        <option value="Fire TV Stick / Kodi">Fire TV Stick / Kodi</option>
        <option value="PC Windows / Linux / Kodi">PC Windows / Linux / Kodi</option>
        <option value="Smartphone / Tablet Android">Smartphone / Tablet Android</option>
        <option value="Altro">Altro</option>
      </select>
    </div>
    
    <div style="margin-bottom: 20px; background: #3a2e12; border: 1px solid #ffa000; padding: 12px; border-radius: 6px;">
      <label style="cursor: pointer; display: flex; align-items: flex-start; gap: 10px;">
        <input type="checkbox" id="check-conferma" required style="margin-top: 3px;">
        <span><strong>Confermo:</strong> La segnalazione riguarda l'<strong>INTERA sezione o sottosezione</strong> non funzionante e non un singolo canale/link temporaneamente offline.</span>
      </label>
    </div>
    
    <button type="submit" id="btn-invia" class="btn-submit">Invia Segnalazione</button>
    <div id="messaggio-stato" class="status-msg"></div>

  </form>

</div>

<script>
(function() {
  var SCRIPT_URL = "https://script.google.com/macros/s/AKfycbwTQJzxvLspR-1GdYh1wOXSLrF8h4TIeswEAIUJGtM9z1I4pIUZD3N_ANO2oewKmaI/exec";
  var rawData = null;

  function init() {
    loadReports();
    loadMenu();

    document.getElementById("categoria-principale").addEventListener("change", onCatChange);
    document.getElementById("sotto-categoria").addEventListener("change", onSubChange);
    document.getElementById("contenuto-lista").addEventListener("change", onContChange);
    document.getElementById("form-segnalazione").addEventListener("submit", onSubmit);
  }

  function loadReports() {
    var tbody = document.getElementById('tabella-segnalazioni');
    if (!tbody) return;

    var cacheBuster = "&_ts=" + new Date().getTime();
    
    fetch(SCRIPT_URL + "?action=getOpen" + cacheBuster, { method: "GET" })
      .then(function(res) { return res.json(); })
      .then(function(data) {
        tbody.innerHTML = '';
        if (!data || data.length === 0 || data.error) {
          tbody.innerHTML = '<tr><td colspan="5" style="text-align: center;">Nessuna segnalazione attiva al momento.</td></tr>';
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
        tbody.innerHTML = '<tr><td colspan="5" style="text-align: center;">Nessuna segnalazione attiva.</td></tr>';
      });
  }

  function loadMenu() {
    fetch(SCRIPT_URL + "?action=getMenu", { method: "GET" })
      .then(function(res) { return res.json(); })
      .then(function(data) { 
        rawData = data || {}; 
        var catSelect = document.getElementById("categoria-principale");
        if (catSelect && catSelect.value) {
          onCatChange();
        }
      })
      .catch(function(err) { 
        console.error("Errore recupero menu:", err); 
        rawData = {};
      });
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
    } else if (cat === "Live") {
      if (!rawData) {
        subSel.innerHTML = '<option value="">Caricamento sotto-categorie in corso...</option>';
        return;
      }
      var list = rawData["Live"] || [];
      if (list.length === 0) {
        subSel.innerHTML = '<option value="">Nessuna sotto-categoria trovata</option>';
      } else {
        list.forEach(function(item) {
          var opt = document.createElement("option");
          opt.value = item; opt.textContent = item;
          subSel.appendChild(opt);
        });
      }
    } else if (cat === "On Demand") {
      var opts = ["Movie Club", "Anime & Cartoon", "Old Tv", "Doctor Who", "Raiplay", "Pluto Tv", "Federmoto Tv", "MandraTube"];
      opts.forEach(function(o) {
        var opt = document.createElement("option");
        opt.value = o; opt.textContent = o;
        subSel.appendChild(opt);
      });
    } else if (cat === "Radio") {
      if (!rawData) {
        subSel.innerHTML = '<option value="">Caricamento sotto-categorie in corso...</option>';
        return;
      }
      var list = rawData["Radio"] || [];
      if (list.length === 0) {
        subSel.innerHTML = '<option value="">Nessuna sotto-categoria trovata</option>';
      } else {
        list.forEach(function(item) {
          var opt = document.createElement("option");
          opt.value = item; opt.textContent = item;
          subSel.appendChild(opt);
        });
      }
    }
  }

  function onSubChange() {
    var cat = document.getElementById("categoria-principale").value;
    var sub = document.getElementById("sotto-categoria").value;
    var contSel = document.getElementById("contenuto-lista");
    var groupCont = document.getElementById("group-contenuto");
    var groupDet = document.getElementById("group-dettaglio");

    contSel.innerHTML = '<option value="">-- Seleziona Contenuto --</option>';
    groupCont.style.display = "none";
    groupDet.style.display = "none";
    
    if (!cat || !sub || !rawData) return;
    
    if (cat === "Sport") {
      if (sub === "Live Eventi") {
        groupCont.style.display = "block";
        (rawData["Sport_LiveEventi"] || []).forEach(function(i) {
          var opt = document.createElement("option");
          opt.value = i; opt.textContent = i;
          contSel.appendChild(opt);
        });
      } else if (sub === "Liste Canali") {
        groupCont.style.display = "block";
        (rawData["Sport_ListeCanali"] || []).forEach(function(i) {
          var opt = document.createElement("option");
          opt.value = i; opt.textContent = i;
          contSel.appendChild(opt);
        });
      } else if (sub === "Sport Replay") {
        groupCont.style.display = "block";
        (rawData["Sport_Replay"] || []).forEach(function(i) {
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
      (rawData["Sport_MPDNazioni"] || []).forEach(function(i) {
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
        msg.innerHTML = "✅ Segnalazione inviata con successo!<br><small style='margin-top:5px; display:inline-block;'>🔄 Ricarica la pagina per visualizzare la richiesta inviata.</small>";
        document.getElementById("form-segnalazione").reset();
        onCatChange();
        loadReports();
      } else if (data.result === "duplicate") {
        msg.style.background = "#b71c1c";
        msg.style.color = "#fff";
        msg.innerHTML = "⚠️ Risulta già una segnalazione attiva per questo contenuto.";
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