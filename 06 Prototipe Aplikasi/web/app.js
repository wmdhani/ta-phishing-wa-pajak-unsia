(() => {
  const FALLBACK_PRESETS = [
    {
      id: "apk",
      label: "File .apk Palsu",
      tag: "Scam",
      tone: "danger",
      text: "Yth. Wajib Pajak, segera unduh dan instal berkas Pembaruan_Coretax_DJP.apk untuk verifikasi NPWP agar terhindar dari denda administratif.",
    },
    {
      id: "domain",
      label: "Link Pajak Palsu",
      tag: "Scam",
      tone: "danger",
      text: "Pemberitahuan resmi Direktorat Jenderal Pajak: terdapat selisih SPT Tahunan Anda. Segera login melalui https://djp-coretax-verifikasi.xyz/login sebelum pukul 17.00 WIB.",
    },
    {
      id: "official",
      label: "Chat Resmi DJP",
      tag: "Aman",
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
  let showFullBenchmarkTable = false;
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
    el.checkBtnLabel.textContent = loading ? "Memeriksa..." : "Cek Sekarang";
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
        const preferred =
          showHandlers.find((h) => h.kind === "apk" || h.kind === "suspicious_url") ||
          showHandlers[0];
        preferred.showReason();
      }
    }

    if (Array.isArray(triggerWords) && triggerWords.length > 0) {
      const label = document.createElement("span");
      label.textContent = "Trigger words:";
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
      content.className = "reason-line";
      const title = document.createElement("strong");
      title.className = "reason-title";
      title.textContent = `${item.title}: `;

      const detail = document.createElement("span");
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
      showInputAlert("Paste atau ketik chat WA dulu.");
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

  function shortenStageName(rawStage) {
    const map = {
      "Tahap 1: Baseline Holdout 80:20": "Baseline Holdout",
      "Tahap 1: 10-Fold CV Default (Latih)": "10-Fold CV Default",
      "Tahap 2: 10-Fold CV Tuned (Latih)": "10-Fold CV Tuned",
      "Tahap 3: Holdout Tuned & Kalibrasi": "Holdout Final (80:20)",
      "Tahap 4A: Subset Pajak Holdout": "Khusus Chat Pajak",
      "Tahap 4A: 10-Fold CV Korpus Pajak 260": "CV Korpus Pajak (260)",
      "Tahap 4B: Zero-Shot Eksternal (Unseen)": "Zero-Shot Eksternal",
      "Tahap 4C: Holdout Korpus Diperluas 2519 (80:20)": "Holdout 2.519 Teks",
      "Tahap 4C: 10-Fold CV Korpus Diperluas 2519": "10-Fold CV 2.519",
    };
    return map[rawStage] || rawStage || "-";
  }

  function isKeyComparisonRow(row) {
    const st = row.tahap_evaluasi || "";
    const mdl = row.model || "";
    if (st === "Tahap 2: 10-Fold CV Tuned (Latih)") return true;
    if (st === "Tahap 4A: Subset Pajak Holdout") return true;
    if (st === "Tahap 3: Holdout Tuned & Kalibrasi") {
      return mdl.includes("Platt Sigmoid") || mdl.includes("Random Forest");
    }
    return false;
  }

  function renderAcademicSummaryPanel(data) {
    const meta = data.metadata || {};
    const thesis = data.thesis || {};
    const allRows = data.evaluation_rows || [];

    const container = document.createElement("div");
    container.className = "acad-panel";

    const hero = document.createElement("div");
    hero.className = "acad-hero-card";
    const heroTitle = document.createElement("p");
    heroTitle.className = "acad-hero-title";
    heroTitle.textContent = thesis.title || "";
    const heroSub = document.createElement("p");
    heroSub.className = "acad-hero-meta";
    heroSub.textContent = `${thesis.author || "Wan Mirza Dhani (240101020194)"} • Pembimbing: ${thesis.advisor || "Bapak Novi Dian Nathasia, S.Kom., MMSI"} • PJJ Sistem Informasi UNSIA (TKT 6)`;
    hero.append(heroTitle, heroSub);
    container.appendChild(hero);

    const statsGrid = document.createElement("div");
    statsGrid.className = "acad-meta-grid";
    const svmAcc = meta.holdout_accuracy_svm ? formatIdDecimal(meta.holdout_accuracy_svm, 2, true) : "95,69%";
    const rfAcc = meta.holdout_accuracy_rf ? formatIdDecimal(meta.holdout_accuracy_rf, 2, true) : "96,55%";
    const brierVal = meta.holdout_brier_svm_calibrated
      ? formatIdDecimal(meta.holdout_brier_svm_calibrated, 4, false)
      : "0,0254";
    const taxSvmRow = allRows.find(
      (r) => r.tahap_evaluasi === "Tahap 4A: Subset Pajak Holdout" && (r.model || "").includes("Platt")
    );
    const taxRfRow = allRows.find(
      (r) => r.tahap_evaluasi === "Tahap 4A: Subset Pajak Holdout" && (r.model || "").includes("Random Forest")
    );
    const taxAccDisplay = taxSvmRow ? formatIdDecimal(taxSvmRow.accuracy, 2, true) : "95,56%";
    const taxAucSub =
      taxSvmRow && taxRfRow
        ? `AUC ${formatIdDecimal(taxSvmRow.roc_auc, 4, false)} vs RF ${formatIdDecimal(taxRfRow.roc_auc, 4, false)}`
        : "AUC 0,9960 vs RF 0,9752";
    const stats = [
      ["Dataset", `${(meta.n_samples ?? 1159).toLocaleString("id-ID")} Chat`, "899 umum + 260 pajak"],
      ["Accuracy (Holdout)", svmAcc, `LinearSVC vs RF ${rfAcc}`],
      ["Khusus Chat Pajak", taxAccDisplay, taxAucSub],
      ["Speed & Calibration", "~25 ms", `Brier ${brierVal} • Platt Scaling`],
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

    if (allRows.length > 0) {
      const tableToolbar = document.createElement("div");
      tableToolbar.className = "acad-table-toolbar";
      const tableTitle = document.createElement("h3");
      tableTitle.className = "xai-section-title";
      tableTitle.style.margin = "0";
      tableTitle.textContent = showFullBenchmarkTable ? `Full Benchmark (${allRows.length} Rows)` : "Key Comparison (LinearSVC vs RF)";

      const toggleBtn = document.createElement("button");
      toggleBtn.type = "button";
      toggleBtn.className = "xai-preset-btn";
      toggleBtn.textContent = showFullBenchmarkTable ? "Show Compact (6 Rows)" : `Show All ${allRows.length} Rows`;
      toggleBtn.addEventListener("click", () => {
        showFullBenchmarkTable = !showFullBenchmarkTable;
        renderAcademicSummaryPanel(data);
      });
      tableToolbar.append(tableTitle, toggleBtn);
      container.appendChild(tableToolbar);

      const visibleRows = showFullBenchmarkTable ? allRows : allRows.filter(isKeyComparisonRow);
      const colSpecs = [
        ["tahap_evaluasi", "Stage"],
        ["model", "Model"],
        ["n_sampel", "Samples"],
        ["accuracy", "Accuracy"],
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
      visibleRows.forEach((row) => {
        const tr = document.createElement("tr");
        if ((row.model || "").includes("Platt Sigmoid")) {
          tr.className = "row-highlight";
        }
        colSpecs.forEach(([key]) => {
          const td = document.createElement("td");
          const rawVal = row[key];
          if (key === "tahap_evaluasi") {
            td.textContent = shortenStageName(rawVal);
          } else if (key === "n_sampel") {
            const n = Number(rawVal);
            td.textContent = Number.isNaN(n) ? rawVal || "-" : n.toLocaleString("id-ID");
          } else if (key === "accuracy" || key === "f1") {
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
    loading.textContent = "Loading...";
    el.acadPanelSummary.appendChild(loading);
    try {
      const resp = await fetch("/api/academic-summary");
      if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
      const data = await resp.json();
      renderAcademicSummaryPanel(data);
    } catch (err) {
      el.acadPanelSummary.textContent = `Gagal memuat ringkasan: ${err.message}`;
    }
  }

  async function fetchPredictionForInspector(sampleText) {
    const resp = await fetch("/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text: sampleText, top_k: 6 }),
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
    tbLabel.textContent = lastResult ? "Hasil pesan terakhir (atau ganti contoh):" : "Pilih contoh uji:";

    const presetBtns = document.createElement("div");
    presetBtns.className = "xai-preset-btns";
    presetsCache.forEach((p) => {
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "xai-preset-btn";
      btn.textContent = p.label;
      btn.addEventListener("click", () => {
        fetchPredictionForInspector(p.text).catch((err) => {
          el.acadPanelInspector.textContent = `Gagal memuat XAI: ${err.message}`;
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
      waitMsg.textContent = "Loading...";
      el.acadPanelInspector.appendChild(waitMsg);
      return;
    }

    const msgSnippet = document.createElement("div");
    msgSnippet.className = "xai-msg-preview";
    msgSnippet.textContent = inspectorText;
    el.acadPanelInspector.appendChild(msgSnippet);

    const compareGrid = document.createElement("div");
    compareGrid.className = "xai-compare-grid";

    const svmProb = Number(data.svm_probability || 0);
    const rfProb = Number(data.rf_probability || 0);
    const modelCards = [
      {
        name: "LinearSVC (Platt)",
        tag: data.inference_ms ? `Production • ${data.inference_ms} ms` : "Production",
        prob: svmProb,
        note: `Verdict: ${data.risk_level} (${data.label === 1 ? "Scam" : "Aman"})`,
        winner: true,
      },
      {
        name: "Random Forest (100 Trees)",
        tag: "Benchmark",
        prob: rfProb,
        note: `Gap: ${formatIdDecimal(Math.abs(svmProb - rfProb), 2, true)}`,
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

    const triggers = (data.top_triggers || []).slice(0, 6);
    if (triggers.length > 0) {
      const trigBox = document.createElement("div");
      trigBox.className = "xai-section-box";
      const trigTitle = document.createElement("h3");
      trigTitle.className = "xai-section-title";
      trigTitle.textContent = "Top Feature Weights (TF-IDF x Coef w)";

      const list = document.createElement("div");
      list.className = "xai-weights-list";
      triggers.forEach((t) => {
        const row = document.createElement("div");
        row.className = "xai-weight-row";

        const tok = document.createElement("span");
        tok.className = "xai-stem-token";
        tok.textContent = t.token;

        const score = document.createElement("span");
        score.className = "xai-weight-score";
        score.textContent = `${t.contribution > 0 ? "+" : ""}${Number(t.contribution).toFixed(3)} (w=${t.svm_coef > 0 ? "+" : ""}${Number(t.svm_coef).toFixed(2)})`;

        const pill = document.createElement("span");
        pill.className = `xai-dir-pill ${t.direction === "phishing" ? "phishing" : "resmi"}`;
        pill.textContent = t.direction === "phishing" ? "Scam (+)" : "Aman (-)";

        row.append(tok, score, pill);
        list.appendChild(row);
      });
      trigBox.append(trigTitle, list);
      el.acadPanelInspector.appendChild(trigBox);
    }

    const prepBox = document.createElement("div");
    prepBox.className = "xai-clean-line";
    const prepLabel = document.createElement("strong");
    prepLabel.textContent = "Preprocessed (Sastrawi): ";
    const prepText = document.createElement("code");
    prepText.textContent = data.cleaned_text || "(kosong)";
    prepBox.append(prepLabel, prepText);
    el.acadPanelInspector.appendChild(prepBox);
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
    headText.textContent = "Simulasi tombol Cek Pesan Pajak di dalam chat WhatsApp Web (Manifest V3):";

    const headActions = document.createElement("div");
    headActions.style.display = "flex";
    headActions.style.gap = "8px";
    headActions.style.flexWrap = "wrap";

    const runAllBtn = document.createElement("button");
    runAllBtn.type = "button";
    runAllBtn.className = "sim-scan-btn";
    runAllBtn.textContent = "Test All 3 Chats";

    const openFullLink = document.createElement("a");
    openFullLink.className = "btn-soft-link";
    openFullLink.href = "/simulasi-wa";
    openFullLink.target = "_blank";
    openFullLink.rel = "noopener noreferrer";
    openFullLink.textContent = "Full Screen";

    headActions.append(runAllBtn, openFullLink);
    head.append(headText, headActions);
    el.acadPanelExtension.appendChild(head);

    const list = document.createElement("div");
    list.className = "sim-wa-list";
    const senderLabels = [
      "+62 812-9901-xxxx (Unknown)",
      "+62 857-4410-xxxx (Forward)",
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
      scanBtn.textContent = "Cek";

      const badge = document.createElement("div");
      badge.className = "sim-wa-badge";
      badge.hidden = true;

      const runBubbleScan = async () => {
        scanBtn.disabled = true;
        scanBtn.textContent = "Cek...";
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
          strong.textContent = `${res.risk_badge}: ${res.risk_title}`;
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
          badge.textContent = `Gagal cek: ${err.message}`;
          badge.hidden = false;
          scanBtn.textContent = "Cek";
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
      showToast("Berhasil disalin. Siap paste ke grup WA.");
    } catch {
      showToast("Gagal salin. Pakai tombol Share WA.");
    }
  });

  el.scamChecks.forEach((box) => {
    box.addEventListener("change", () => {
      const checkedCount = Array.from(el.scamChecks).filter((c) => c.checked).length;
      if (checkedCount === 0) {
        el.checklistFeedback.className = "checklist-feedback";
        el.checklistFeedback.textContent = "Ada 1 tanda saja? Jangan klik link atau file.";
      } else {
        el.checklistFeedback.className = "checklist-feedback alert";
        el.checklistFeedback.textContent =
          `${checkedCount} ciri ditemukan. Jangan klik link, install file, atau kirim OTP.`;
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
