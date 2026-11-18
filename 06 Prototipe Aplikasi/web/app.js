(() => {
  const FALLBACK_PRESETS = [
    {
      id: "apk",
      label: "Scam File .apk",
      tag: "Berbahaya",
      tone: "danger",
      text: "Yth. Wajib Pajak, segera unduh dan instal berkas Pembaruan_Coretax_DJP.apk untuk verifikasi NPWP agar terhindar dari denda administratif.",
    },
    {
      id: "domain",
      label: "Link Pajak Palsu",
      tag: "Link Palsu",
      tone: "danger",
      text: "Pemberitahuan resmi Direktorat Jenderal Pajak: terdapat selisih SPT Tahunan Anda. Segera login melalui https://djp-coretax-verifikasi.xyz/login sebelum pukul 17.00 WIB.",
    },
    {
      id: "official",
      label: "Chat Resmi DJP",
      tag: "Resmi DJP",
      tone: "safe",
      text: "Direktorat Jenderal Pajak mengimbau Wajib Pajak melaporkan SPT Tahunan tepat waktu melalui laman resmi https://djponline.pajak.go.id atau hubungi Kring Pajak 1500200.",
    },
  ];

  const ICONS = {
    danger: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="15" x2="9" y1="9" y2="15"></line><line x1="9" x2="15" y1="9" y2="15"></line></svg>`,
    warn: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10.29 3.86 1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path><line x1="12" x2="12" y1="9" y2="13"></line><line x1="12" x2="12.01" y1="17" y2="17"></line></svg>`,
    safe: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path><path d="m9 12 2 2 4-4"></path></svg>`,
  };

  const el = {
    navTabs: document.querySelectorAll(".nav-tab"),
    tabPanels: document.querySelectorAll(".tab-panel"),
    servicePill: document.getElementById("service-pill"),
    servicePillText: document.getElementById("service-pill-text"),
    pasteBtn: document.getElementById("paste-btn"),
    clearBtn: document.getElementById("clear-btn"),
    input: document.getElementById("message-input"),
    charCount: document.getElementById("char-count"),
    inputAlert: document.getElementById("input-alert"),
    checkBtn: document.getElementById("check-btn"),
    checkBtnLabel: document.querySelector("#check-btn .btn-label"),
    checkBtnSpinner: document.querySelector("#check-btn .btn-spinner"),
    presetsList: document.getElementById("presets-list"),
    emptyState: document.getElementById("empty-state"),
    resultState: document.getElementById("result-state"),
    verdictBanner: document.getElementById("verdict-banner"),
    verdictIcon: document.getElementById("verdict-icon"),
    verdictBadge: document.getElementById("verdict-badge"),
    confidenceNote: document.getElementById("confidence-note"),
    verdictTitle: document.getElementById("verdict-title"),
    verdictSummary: document.getElementById("verdict-summary"),
    meterFill: document.getElementById("meter-fill"),
    highlightedText: document.getElementById("highlighted-text"),
    highlightHint: document.getElementById("highlight-hint"),
    highlightInspector: document.getElementById("highlight-inspector"),
    triggerChipsRow: document.getElementById("trigger-chips-row"),
    reasonsList: document.getElementById("reasons-list"),
    actionsList: document.getElementById("actions-list"),
    copyWarningBtn: document.getElementById("copy-warning-btn"),
    waShareLink: document.getElementById("wa-share-link"),
    apkEmergencyCta: document.getElementById("apk-emergency-cta"),
    copyToast: document.getElementById("copy-toast"),
    backToCheckerBtn: document.getElementById("back-to-checker-btn"),
    scamChecks: document.querySelectorAll(".scam-check"),
    checklistFeedback: document.getElementById("checklist-feedback"),
    openAcademicBtn: document.getElementById("open-academic-btn"),
    closeAcademicBtn: document.getElementById("close-academic-btn"),
    academicDialog: document.getElementById("academic-dialog"),
    academicContent: document.getElementById("academic-content"),
    acadTabs: document.querySelectorAll(".acad-tab"),
    acadPanels: document.querySelectorAll(".acad-panel"),
    acadPanelSummary: document.getElementById("acad-panel-summary"),
    acadPanelInspector: document.getElementById("acad-panel-inspector"),
    acadPanelExtension: document.getElementById("acad-panel-extension"),
  };

  let lastResult = null;
  let lastCheckedText = "";
  let inspectorResult = null;
  let inspectorText = "";
  let presetsCache = FALLBACK_PRESETS;
  let toastTimer = null;
  let activeCheckController = null;

  function setupTablistKeyboard(tabButtons, activateFn) {
    const buttons = Array.from(tabButtons);
    buttons.forEach((btn, idx) => {
      btn.addEventListener("keydown", (event) => {
        let nextIdx = -1;
        if (event.key === "ArrowRight") nextIdx = (idx + 1) % buttons.length;
        else if (event.key === "ArrowLeft") nextIdx = (idx - 1 + buttons.length) % buttons.length;
        else if (event.key === "Home") nextIdx = 0;
        else if (event.key === "End") nextIdx = buttons.length - 1;
        if (nextIdx >= 0) {
          event.preventDefault();
          activateFn(buttons[nextIdx]);
          buttons[nextIdx].focus();
        }
      });
    });
  }

  function switchTab(tabName) {
    el.navTabs.forEach((btn) => {
      const isMatch = btn.dataset.tab === tabName;
      btn.classList.toggle("active", isMatch);
      btn.setAttribute("aria-selected", String(isMatch));
      btn.tabIndex = isMatch ? 0 : -1;
    });
    el.tabPanels.forEach((panel) => {
      panel.hidden = panel.dataset.panel !== tabName;
    });
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  function showInputAlert(msg) {
    if (!msg) {
      el.inputAlert.hidden = true;
      el.inputAlert.textContent = "";
      return;
    }
    el.inputAlert.textContent = msg;
    el.inputAlert.hidden = false;
  }

  function updateInputControls() {
    const len = el.input.value.length;
    el.charCount.textContent = `${len.toLocaleString("id-ID")} / 5.000`;
    el.clearBtn.hidden = len === 0;
  }

  function setLoading(loading) {
    el.checkBtn.disabled = loading;
    el.checkBtnSpinner.hidden = !loading;
    el.checkBtnLabel.textContent = loading ? "Memeriksa..." : "Cek Pesan Sekarang";
  }

  function clearActivePreset() {
    el.presetsList.querySelectorAll(".preset-pill").forEach((btn) => {
      btn.classList.remove("active");
    });
  }

  function renderPresets(presets) {
    el.presetsList.replaceChildren();
    presets.forEach((preset) => {
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "preset-pill";
      btn.dataset.presetId = preset.id;

      const tag = document.createElement("span");
      tag.className = `preset-tag tone-${preset.tone}`;
      tag.textContent = preset.tag;

      const name = document.createElement("span");
      name.className = "preset-name";
      name.textContent = preset.label;

      btn.append(tag, name);
      btn.addEventListener("click", () => {
        clearActivePreset();
        btn.classList.add("active");
        el.input.value = preset.text;
        updateInputControls();
        showInputAlert("");
        runCheck(preset.text);
      });
      el.presetsList.appendChild(btn);
    });
  }

  function renderHighlightedBubble(rawText, highlights, triggerWords) {
    el.highlightedText.replaceChildren();
    el.highlightHint.hidden = true;
    el.highlightInspector.hidden = true;
    el.triggerChipsRow.replaceChildren();
    el.triggerChipsRow.hidden = true;

    if (!highlights || highlights.length === 0) {
      el.highlightedText.textContent = rawText;
    } else {
      const sorted = [...highlights].sort((a, b) => a.start - b.start);
      let cursor = 0;
      const showHandlers = [];

      sorted.forEach((span) => {
        if (span.start > cursor) {
          el.highlightedText.appendChild(
            document.createTextNode(rawText.slice(cursor, span.start))
          );
        }
        const mark = document.createElement("mark");
        mark.className = `hl hl-${span.kind}`;
        mark.tabIndex = 0;
        mark.textContent = rawText.slice(span.start, span.end);
        mark.title = span.reason;

        const showReason = () => {
          el.highlightInspector.replaceChildren();
          const strong = document.createElement("strong");
          strong.textContent = `${mark.textContent}: `;
          el.highlightInspector.append(strong, document.createTextNode(span.reason));
          el.highlightInspector.hidden = false;
        };
        mark.addEventListener("mouseenter", showReason);
        mark.addEventListener("click", showReason);
        mark.addEventListener("focus", showReason);
        showHandlers.push({ kind: span.kind, showReason });

        el.highlightedText.appendChild(mark);
        cursor = span.end;
      });

      if (cursor < rawText.length) {
        el.highlightedText.appendChild(document.createTextNode(rawText.slice(cursor)));
      }

      if (showHandlers.length > 0) {
        el.highlightHint.hidden = false;
        const preferred =
          showHandlers.find((h) => h.kind === "apk" || h.kind === "suspicious_url") ||
          showHandlers[0];
        preferred.showReason();
      }
    }

    if (Array.isArray(triggerWords) && triggerWords.length > 0) {
      const label = document.createElement("span");
      label.textContent = "Kata pemicu:";
      el.triggerChipsRow.appendChild(label);
      triggerWords.slice(0, 4).forEach((word) => {
        const chip = document.createElement("span");
        chip.className = "trigger-chip";
        chip.textContent = word;
        el.triggerChipsRow.appendChild(chip);
      });
      el.triggerChipsRow.hidden = false;
    }
  }

  function buildShareMessage(rawText, data) {
    const snippet = rawText.length > 120 ? `${rawText.slice(0, 117)}...` : rawText;
    return (
      `[Cek Pesan Pajak]\n` +
      `Status: ${data.risk_title}\n` +
      `Pesan: "${snippet}"\n` +
      `Saran: ${data.recommendation}`
    );
  }

  function renderResult(rawText, data) {
    lastResult = data;
    lastCheckedText = rawText;

    const risk = (data.risk_level || "RENDAH").toLowerCase();
    el.verdictBanner.className = `verdict-banner tone-${risk}`;
    el.verdictIcon.innerHTML =
      risk === "tinggi" ? ICONS.danger : risk === "sedang" ? ICONS.warn : ICONS.safe;
    el.verdictBadge.textContent = data.risk_badge || data.label_text;
    el.confidenceNote.textContent = data.confidence_note || "";
    el.verdictTitle.textContent = data.risk_title || data.label_text;
    el.verdictSummary.textContent = data.verdict_summary || data.recommendation;

    const rawPct = Math.round((data.svm_probability || 0) * 100);
    const meterPct =
      risk === "tinggi"
        ? Math.max(rawPct, data.has_apk ? 92 : 75)
        : risk === "sedang"
          ? Math.max(rawPct, 45)
          : Math.max(100 - rawPct, 12);
    el.meterFill.style.width = `${Math.min(100, meterPct)}%`;

    renderHighlightedBubble(rawText, data.highlights || [], data.trigger_words || []);

    el.reasonsList.replaceChildren();
    (data.plain_reasons || []).forEach((item) => {
      const li = document.createElement("li");
      li.className = `type-${item.type || "warning"}`;

      const dot = document.createElement("span");
      dot.className = "reason-dot";
      dot.setAttribute("aria-hidden", "true");

      const content = document.createElement("div");
      const title = document.createElement("div");
      title.className = "reason-title";
      title.textContent = item.title;

      const detail = document.createElement("div");
      detail.className = "reason-detail";
      detail.textContent = item.detail;

      content.append(title, detail);
      li.append(dot, content);
      el.reasonsList.appendChild(li);
    });

    el.actionsList.replaceChildren();
    (data.action_steps || []).forEach((stepText) => {
      const li = document.createElement("li");
      li.textContent = stepText;
      el.actionsList.appendChild(li);
    });

    const shareText = buildShareMessage(rawText, data);
    el.waShareLink.href = `https://wa.me/?text=${encodeURIComponent(shareText)}`;
    el.apkEmergencyCta.hidden = !data.has_apk;
    el.copyToast.hidden = true;

    el.emptyState.hidden = true;
    el.resultState.hidden = false;

    if (window.innerWidth <= 960) {
      el.resultState.scrollIntoView({ behavior: "smooth", block: "nearest" });
    }
  }

  async function runCheck(textOverride) {
    const text = (textOverride ?? el.input.value).trim();
    if (!text) {
      showInputAlert("Paste atau ketik pesan WA dulu.");
      el.input.focus();
      return;
    }

    if (activeCheckController) {
      activeCheckController.abort();
    }
    activeCheckController = new AbortController();

    showInputAlert("");
    setLoading(true);
    try {
      const resp = await fetch("/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text, top_k: 8 }),
        signal: activeCheckController.signal,
      });
      if (!resp.ok) {
        const errPayload = await resp.json().catch(() => ({}));
        throw new Error(errPayload.detail || `HTTP ${resp.status}`);
      }
      const data = await resp.json();
      renderResult(text, data);
    } catch (err) {
      if (err && err.name === "AbortError") return;
      showInputAlert(`Gagal memeriksa pesan: ${err.message}.`);
    } finally {
      activeCheckController = null;
      setLoading(false);
    }
  }

  function showToast(msg) {
    el.copyToast.textContent = msg;
    el.copyToast.hidden = false;
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => {
      el.copyToast.hidden = true;
    }, 3000);
  }

  async function checkServiceHealth() {
    try {
      const resp = await fetch("/health");
      if (!resp.ok) throw new Error("offline");
      el.servicePill.className = "status-pill status-ready";
      el.servicePillText.textContent = "Siap";
    } catch {
      el.servicePill.className = "status-pill status-offline";
      el.servicePillText.textContent = "Offline";
    }
  }

  async function loadPresets() {
    try {
      const resp = await fetch("/api/presets");
      if (!resp.ok) throw new Error("failed");
      const data = await resp.json();
      if (Array.isArray(data.presets) && data.presets.length > 0) {
        presetsCache = data.presets;
        renderPresets(presetsCache);
        return;
      }
    } catch {
      // Gunakan fallback bawaan bila gagal memuat.
    }
    presetsCache = FALLBACK_PRESETS;
    renderPresets(presetsCache);
  }

  function formatIdDecimal(val, digits = 2, isPct = false) {
    if (val === undefined || val === null || val === "") return "-";
    const num = Number(val);
    if (Number.isNaN(num)) return String(val);
    const scaled = isPct ? num * 100 : num;
    return scaled.toLocaleString("id-ID", {
      minimumFractionDigits: digits,
      maximumFractionDigits: digits,
    }) + (isPct ? "%" : "");
  }

  function switchAcadTab(tabName) {
    el.acadTabs.forEach((btn) => {
      const isMatch = btn.dataset.acadTab === tabName;
      btn.classList.toggle("active", isMatch);
      btn.setAttribute("aria-selected", String(isMatch));
      btn.tabIndex = isMatch ? 0 : -1;
    });
    el.acadPanels.forEach((panel) => {
      panel.hidden = panel.dataset.acadPanel !== tabName;
    });

    if (tabName === "inspector") {
      renderAcademicInspector();
    } else if (tabName === "extension") {
      renderExtensionSimulation();
    }
  }

  function renderAcademicSummaryPanel(data) {
    const meta = data.metadata || {};
    const thesis = data.thesis || {};
    const rows = data.evaluation_rows || [];

    const container = document.createElement("div");
    container.className = "acad-panel";

    const hero = document.createElement("div");
    hero.className = "acad-hero-card";
    const heroTitle = document.createElement("p");
    heroTitle.className = "acad-hero-title";
    heroTitle.textContent = thesis.title || "";

    const identityGrid = document.createElement("div");
    identityGrid.className = "acad-identity-grid";
    const identities = [
      ["Penulis", thesis.author || "Wan Mirza Dhani (240101020194)"],
      ["Dosen Pembimbing", thesis.advisor || "Bapak Novi Dian Nathasia, S.Kom., MMSI"],
      ["Program Studi", thesis.program || "PJJ Sistem Informasi — Universitas Siber Asia"],
      ["Skema", thesis.scheme || "Tugas Akhir Prototype (TKT Level 6)"],
    ];
    identities.forEach(([k, v]) => {
      const item = document.createElement("div");
      item.className = "acad-identity-item";
      const label = document.createElement("span");
      label.textContent = `${k}: `;
      const val = document.createElement("strong");
      val.textContent = v;
      item.append(label, val);
      identityGrid.appendChild(item);
    });
    hero.append(heroTitle, identityGrid);
    container.appendChild(hero);

    const statsGrid = document.createElement("div");
    statsGrid.className = "acad-meta-grid";
    const svmAcc = meta.holdout_accuracy_svm ? formatIdDecimal(meta.holdout_accuracy_svm, 2, true) : "97,42%";
    const rfAcc = meta.holdout_accuracy_rf ? formatIdDecimal(meta.holdout_accuracy_rf, 2, true) : "96,57%";
    const brierVal = meta.holdout_brier_svm_calibrated
      ? formatIdDecimal(meta.holdout_brier_svm_calibrated, 5, false)
      : "0,01900";
    const stats = [
      ["Korpus Induk & Perluasan", `${(meta.n_samples ?? 1164).toLocaleString("id-ID")} / 2.521 pesan`, "904 SMS umum + 260 teks pajak seimbang"],
      ["Holdout LinearSVC (Platt)", svmAcc, `Pembanding Random Forest: ${rfAcc}`],
      ["Ketahanan Subset Pajak (n=44)", "97,73% vs 88,64%", "LinearSVC unggul atas RF (mitigasi keyword bias)"],
      ["Kalibrasi & Latensi", `Brier ${brierVal}`, "14,37 ms lokal • 23,22 ms REST API"],
    ];
    stats.forEach(([label, val, sub]) => {
      const box = document.createElement("div");
      box.className = "acad-stat";
      const s = document.createElement("span");
      s.textContent = label;
      const st = document.createElement("strong");
      st.textContent = val;
      const sm = document.createElement("small");
      sm.textContent = sub;
      box.append(s, st, sm);
      statsGrid.appendChild(box);
    });
    container.appendChild(statsGrid);

    if (rows.length > 0) {
      const colSpecs = [
        ["tahap_evaluasi", "Tahap Evaluasi"],
        ["model", "Model Klasifikasi"],
        ["n_sampel", "Sampel"],
        ["accuracy", "Accuracy"],
        ["precision", "Precision"],
        ["recall", "Recall"],
        ["f1", "F1-Score"],
        ["roc_auc", "ROC-AUC"],
      ];
      const wrap = document.createElement("div");
      wrap.className = "acad-table-wrap";
      const table = document.createElement("table");
      table.className = "acad-table";

      const thead = document.createElement("thead");
      const headRow = document.createElement("tr");
      colSpecs.forEach(([, label]) => {
        const th = document.createElement("th");
        th.textContent = label;
        headRow.appendChild(th);
      });
      thead.appendChild(headRow);

      const tbody = document.createElement("tbody");
      rows.forEach((row) => {
        const tr = document.createElement("tr");
        if ((row.model || "").includes("Platt Sigmoid")) {
          tr.className = "row-highlight";
        }
        colSpecs.forEach(([key]) => {
          const td = document.createElement("td");
          const rawVal = row[key];
          if (key === "n_sampel") {
            const n = Number(rawVal);
            td.textContent = Number.isNaN(n) ? rawVal || "-" : n.toLocaleString("id-ID");
          } else if (["accuracy", "precision", "recall", "f1"].includes(key)) {
            td.textContent = formatIdDecimal(rawVal, 2, true);
          } else if (key === "roc_auc") {
            td.textContent = formatIdDecimal(rawVal, 4, false);
          } else {
            td.textContent = rawVal || "-";
          }
          tr.appendChild(td);
        });
        tbody.appendChild(tr);
      });
      table.append(thead, tbody);
      wrap.appendChild(table);
      container.appendChild(wrap);
    }

    el.acadPanelSummary.replaceChildren(container);
  }

  async function loadAcademicSummary() {
    el.acadPanelSummary.replaceChildren();
    const loading = document.createElement("p");
    loading.className = "dialog-loading";
    loading.textContent = "Memuat ringkasan evaluasi...";
    el.acadPanelSummary.appendChild(loading);
    try {
      const resp = await fetch("/api/academic-summary");
      if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
      const data = await resp.json();
      renderAcademicSummaryPanel(data);
    } catch (err) {
      el.acadPanelSummary.textContent = `Gagal memuat ringkasan akademik: ${err.message}`;
    }
  }

  async function fetchPredictionForInspector(sampleText) {
    const resp = await fetch("/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text: sampleText, top_k: 8 }),
    });
    if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
    inspectorText = sampleText;
    inspectorResult = await resp.json();
    renderInspectorContents();
  }

  function renderInspectorContents() {
    el.acadPanelInspector.replaceChildren();

    const toolbar = document.createElement("div");
    toolbar.className = "xai-toolbar";
    const tbLabel = document.createElement("span");
    tbLabel.className = "xai-toolbar-label";
    tbLabel.textContent = lastResult
      ? "Menampilkan analisis pesan yang baru diperiksa (atau pilih contoh uji):"
      : "Pilih contoh pesan untuk membedah komparasi model & bobot XAI:";

    const presetBtns = document.createElement("div");
    presetBtns.className = "xai-preset-btns";
    presetsCache.forEach((p) => {
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "xai-preset-btn";
      btn.textContent = p.label;
      btn.addEventListener("click", () => {
        fetchPredictionForInspector(p.text).catch((err) => {
          el.acadPanelInspector.textContent = `Gagal memuat inspektor XAI: ${err.message}`;
        });
      });
      presetBtns.appendChild(btn);
    });
    toolbar.append(tbLabel, presetBtns);
    el.acadPanelInspector.appendChild(toolbar);

    const data = inspectorResult;
    if (!data) {
      const waitMsg = document.createElement("p");
      waitMsg.className = "dialog-loading";
      waitMsg.textContent = "Memuat contoh analisis model...";
      el.acadPanelInspector.appendChild(waitMsg);
      return;
    }

    const msgBox = document.createElement("div");
    msgBox.className = "xai-section-box";
    const msgTitle = document.createElement("h3");
    msgTitle.className = "xai-section-title";
    msgTitle.textContent = "Pesan yang Dianalisis";
    const msgText = document.createElement("div");
    msgText.style.fontSize = "0.83rem";
    msgText.style.lineHeight = "1.48";
    msgText.textContent = inspectorText;
    msgBox.append(msgTitle, msgText);
    el.acadPanelInspector.appendChild(msgBox);

    const compareGrid = document.createElement("div");
    compareGrid.className = "xai-compare-grid";

    const svmProb = Number(data.svm_probability || 0);
    const rfProb = Number(data.rf_probability || 0);
    const modelCards = [
      {
        name: "LinearSVC (Platt Scaling)",
        tag: data.inference_ms ? `Model Utama • ${data.inference_ms} ms` : "Model Utama",
        prob: svmProb,
        note: `Vonis sistem: ${data.risk_level} (${data.label === 1 ? "Phishing" : "Aman/Resmi"})`,
        winner: true,
      },
      {
        name: "Random Forest (200 Pohon)",
        tag: "Model Pembanding",
        prob: rfProb,
        note: `Selisih probabilitas: ${formatIdDecimal(Math.abs(svmProb - rfProb), 2, true)}`,
        winner: false,
      },
    ];
    modelCards.forEach((mc) => {
      const card = document.createElement("div");
      card.className = `xai-model-card${mc.winner ? " winner" : ""}`;
      const head = document.createElement("div");
      head.className = "xai-model-head";
      const nm = document.createElement("strong");
      nm.textContent = mc.name;
      const tg = document.createElement("span");
      tg.className = "xai-model-tag";
      tg.textContent = mc.tag;
      head.append(nm, tg);

      const probEl = document.createElement("div");
      probEl.className = "xai-prob-value";
      probEl.textContent = formatIdDecimal(mc.prob, 2, true);

      const track = document.createElement("div");
      track.className = "xai-bar-track";
      const fill = document.createElement("div");
      fill.className = `xai-bar-fill ${mc.prob >= 0.5 ? "tone-danger" : "tone-safe"}`;
      fill.style.width = `${Math.max(4, Math.min(100, Math.round(mc.prob * 100)))}%`;
      track.appendChild(fill);

      const nt = document.createElement("div");
      nt.className = "xai-model-note";
      nt.textContent = mc.note;

      card.append(head, probEl, track, nt);
      compareGrid.appendChild(card);
    });
    el.acadPanelInspector.appendChild(compareGrid);

    const prepBox = document.createElement("div");
    prepBox.className = "xai-section-box";
    const prepTitle = document.createElement("h3");
    prepTitle.className = "xai-section-title";
    prepTitle.textContent = "Hasil Praproses Sastrawi & Penyandian Token Entitas (clean_text)";
    const flow = document.createElement("div");
    flow.className = "xai-tokens-flow";
    const cleanedTokens = (data.cleaned_text || "").split(/\s+/).filter(Boolean);
    if (cleanedTokens.length === 0) {
      const emptyTok = document.createElement("span");
      emptyTok.className = "xai-model-note";
      emptyTok.textContent = "(Tidak ada token tersisa setelah stopword removal)";
      flow.appendChild(emptyTok);
    } else {
      cleanedTokens.forEach((tok) => {
        const chip = document.createElement("span");
        chip.className =
          tok === "token_apk" || tok === "token_url"
            ? "xai-stem-token is-entity"
            : "xai-stem-token";
        chip.textContent = tok;
        flow.appendChild(chip);
      });
    }
    prepBox.append(prepTitle, flow);
    el.acadPanelInspector.appendChild(prepBox);

    const triggers = data.top_triggers || [];
    if (triggers.length > 0) {
      const trigBox = document.createElement("div");
      trigBox.className = "xai-section-box";
      const trigTitle = document.createElement("h3");
      trigTitle.className = "xai-section-title";
      trigTitle.textContent = "Kontribusi Fitur Teratas LinearSVC (TF-IDF x Koefisien Hyperplane w)";

      const wrap = document.createElement("div");
      wrap.className = "acad-table-wrap";
      const table = document.createElement("table");
      table.className = "acad-table xai-coef-table";

      const thead = document.createElement("thead");
      const htr = document.createElement("tr");
      ["Fitur / Token", "Koefisien w", "Kontribusi (TF-IDF x w)", "Arah Dorongan"].forEach((h) => {
        const th = document.createElement("th");
        th.textContent = h;
        htr.appendChild(th);
      });
      thead.appendChild(htr);

      const tbody = document.createElement("tbody");
      triggers.forEach((t) => {
        const tr = document.createElement("tr");
        const tdTok = document.createElement("td");
        tdTok.textContent = t.token;

        const tdCoef = document.createElement("td");
        tdCoef.textContent = `${t.svm_coef > 0 ? "+" : ""}${Number(t.svm_coef).toFixed(4)}`;

        const tdContrib = document.createElement("td");
        tdContrib.textContent = `${t.contribution > 0 ? "+" : ""}${Number(t.contribution).toFixed(4)}`;

        const tdDir = document.createElement("td");
        const pill = document.createElement("span");
        pill.className = `xai-dir-pill ${t.direction === "phishing" ? "phishing" : "resmi"}`;
        pill.textContent = t.direction === "phishing" ? "Phishing (+)" : "Resmi / Normal (-)";
        tdDir.appendChild(pill);

        tr.append(tdTok, tdCoef, tdContrib, tdDir);
        tbody.appendChild(tr);
      });
      table.append(thead, tbody);
      wrap.appendChild(table);
      trigBox.append(trigTitle, wrap);
      el.acadPanelInspector.appendChild(trigBox);
    }
  }

  function renderAcademicInspector() {
    if (lastResult && lastCheckedText) {
      inspectorResult = lastResult;
      inspectorText = lastCheckedText;
      renderInspectorContents();
      return;
    }
    if (!inspectorResult) {
      renderInspectorContents();
      fetchPredictionForInspector(presetsCache[0].text).catch((err) => {
        el.acadPanelInspector.textContent = `Gagal memuat analisis model: ${err.message}`;
      });
      return;
    }
    renderInspectorContents();
  }

  function renderExtensionSimulation() {
    if (el.acadPanelExtension.dataset.initialized === "1") return;
    el.acadPanelExtension.dataset.initialized = "1";
    el.acadPanelExtension.replaceChildren();

    const head = document.createElement("div");
    head.className = "sim-ext-head";
    const headText = document.createElement("span");
    headText.textContent =
      "Simulasi langsung ekstensi Chrome Manifest V3 (content.js + background.js) memindai gelembung WhatsApp Web ke endpoint /predict.";

    const headActions = document.createElement("div");
    headActions.style.display = "flex";
    headActions.style.gap = "8px";
    headActions.style.flexWrap = "wrap";

    const runAllBtn = document.createElement("button");
    runAllBtn.type = "button";
    runAllBtn.className = "sim-scan-btn";
    runAllBtn.textContent = "Uji Semua 3 Gelembung";

    const openFullLink = document.createElement("a");
    openFullLink.className = "btn-soft-link";
    openFullLink.href = "/simulasi-wa";
    openFullLink.target = "_blank";
    openFullLink.rel = "noopener noreferrer";
    openFullLink.textContent = "Buka Simulasi Penuh (/simulasi-wa)";

    headActions.append(runAllBtn, openFullLink);
    head.append(headText, headActions);
    el.acadPanelExtension.appendChild(head);

    const list = document.createElement("div");
    list.className = "sim-wa-list";
    const senderLabels = [
      "+62 812-9901-xxxx (Tidak Dikenal)",
      "+62 857-4410-xxxx (Pesan Terusan)",
      "Kring Pajak / DJP Resmi",
    ];
    const scanButtons = [];

    presetsCache.forEach((preset, idx) => {
      const bubble = document.createElement("div");
      bubble.className = "sim-wa-bubble";

      const sender = document.createElement("div");
      sender.className = "sim-wa-sender";
      sender.textContent = senderLabels[idx] || preset.label;

      const msg = document.createElement("div");
      msg.className = "sim-wa-msg";
      msg.textContent = preset.text;

      const actions = document.createElement("div");
      actions.className = "sim-wa-actions";
      const scanBtn = document.createElement("button");
      scanBtn.type = "button";
      scanBtn.className = "sim-scan-btn";
      scanBtn.textContent = "Cek Pesan Pajak";

      const badge = document.createElement("div");
      badge.className = "sim-wa-badge";
      badge.hidden = true;

      const runBubbleScan = async () => {
        scanBtn.disabled = true;
        scanBtn.textContent = "Memeriksa...";
        try {
          const resp = await fetch("/predict", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text: preset.text, top_k: 5 }),
          });
          if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
          const res = await resp.json();
          const riskCls = (res.risk_level || "RENDAH").toLowerCase();
          badge.className = `sim-wa-badge ${riskCls}`;
          badge.replaceChildren();
          const strong = document.createElement("strong");
          strong.textContent = res.risk_title || res.label_text;
          badge.appendChild(strong);
          badge.appendChild(document.createElement("br"));
          const sub = document.createElement("small");
          const detailText =
            res.plain_reasons && res.plain_reasons.length > 0
              ? res.plain_reasons[0].title
              : res.recommendation;
          sub.textContent = `${detailText}${res.inference_ms ? ` (${res.inference_ms} ms)` : ""}`;
          badge.appendChild(sub);
          badge.hidden = false;
          scanBtn.textContent = "Cek Ulang";
        } catch (err) {
          badge.className = "sim-wa-badge sedang";
          badge.textContent = `Gagal memindai: ${err.message}`;
          badge.hidden = false;
          scanBtn.textContent = "Cek Pesan Pajak";
        } finally {
          scanBtn.disabled = false;
        }
      };

      scanBtn.addEventListener("click", runBubbleScan);
      scanButtons.push(runBubbleScan);
      actions.appendChild(scanBtn);
      bubble.append(sender, msg, actions, badge);
      list.appendChild(bubble);
    });

    runAllBtn.addEventListener("click", () => {
      scanButtons.forEach((fn) => fn());
    });

    el.acadPanelExtension.appendChild(list);
  }

  // Event Listeners
  setupTablistKeyboard(el.navTabs, (btn) => switchTab(btn.dataset.tab));
  setupTablistKeyboard(el.acadTabs, (btn) => switchAcadTab(btn.dataset.acadTab));

  el.navTabs.forEach((btn) => {
    btn.addEventListener("click", () => switchTab(btn.dataset.tab));
  });

  el.acadTabs.forEach((btn) => {
    btn.addEventListener("click", () => switchAcadTab(btn.dataset.acadTab));
  });

  el.backToCheckerBtn.addEventListener("click", () => switchTab("checker"));
  el.apkEmergencyCta.addEventListener("click", () => switchTab("emergency"));

  el.input.addEventListener("input", () => {
    clearActivePreset();
    updateInputControls();
    if (el.input.value.trim()) showInputAlert("");
  });

  el.input.addEventListener("keydown", (event) => {
    if ((event.ctrlKey || event.metaKey) && event.key === "Enter") {
      event.preventDefault();
      runCheck();
    }
  });

  el.checkBtn.addEventListener("click", () => runCheck());

  el.pasteBtn.addEventListener("click", async () => {
    if (!navigator.clipboard || !navigator.clipboard.readText) {
      showInputAlert("Browser tidak mengizinkan paste otomatis. Silakan Ctrl+V manual.");
      el.input.focus();
      return;
    }
    try {
      const clipText = await navigator.clipboard.readText();
      if (!clipText.trim()) {
        showInputAlert("Clipboard masih kosong. Salin chat WA dulu.");
        return;
      }
      clearActivePreset();
      el.input.value = clipText.slice(0, 5000);
      updateInputControls();
      showInputAlert("");
      runCheck(el.input.value);
    } catch {
      showInputAlert("Izin clipboard ditolak browser. Silakan Ctrl+V manual.");
      el.input.focus();
    }
  });

  el.clearBtn.addEventListener("click", () => {
    clearActivePreset();
    el.input.value = "";
    updateInputControls();
    showInputAlert("");
    lastResult = null;
    lastCheckedText = "";
    el.resultState.hidden = true;
    el.emptyState.hidden = false;
    el.input.focus();
  });

  el.copyWarningBtn.addEventListener("click", async () => {
    if (!lastResult) return;
    const textToCopy = buildShareMessage(lastCheckedText, lastResult);
    try {
      await navigator.clipboard.writeText(textToCopy);
      showToast("Alert berhasil disalin — siap paste ke grup WA.");
    } catch {
      showToast("Gagal salin otomatis. Pakai tombol Share WA.");
    }
  });

  el.scamChecks.forEach((box) => {
    box.addEventListener("change", () => {
      const checkedCount = Array.from(el.scamChecks).filter((c) => c.checked).length;
      if (checkedCount === 0) {
        el.checklistFeedback.className = "checklist-feedback";
        el.checklistFeedback.textContent =
          "Salah satu ciri saja sudah cukup jadi alasan untuk tidak klik link atau file.";
      } else {
        el.checklistFeedback.className = "checklist-feedback alert";
        el.checklistFeedback.textContent =
          `${checkedCount} tanda scam tercentang. Jangan klik link, install file, atau kirim OTP.`;
      }
    });
  });

  el.openAcademicBtn.addEventListener("click", () => {
    switchAcadTab("summary");
    if (typeof el.academicDialog.showModal === "function") {
      el.academicDialog.showModal();
    } else {
      el.academicDialog.setAttribute("open", "true");
    }
    loadAcademicSummary();
  });

  el.closeAcademicBtn.addEventListener("click", () => {
    el.academicDialog.close();
  });

  el.academicDialog.addEventListener("click", (event) => {
    if (event.target === el.academicDialog) {
      el.academicDialog.close();
    }
  });

  updateInputControls();
  checkServiceHealth();
  loadPresets();
})();
