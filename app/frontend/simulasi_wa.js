(() => {
  const popupStatus = document.getElementById("sim-popup-status");
  const popupInput = document.getElementById("sim-popup-input");
  const popupBtn = document.getElementById("sim-popup-btn");
  const popupOut = document.getElementById("sim-popup-out");
  const messageBubbles = document.querySelectorAll(".message-in");

  function riskBadgeClass(riskLevel) {
    const level = (riskLevel || "RENDAH").toUpperCase();
    if (level === "TINGGI") return "wa-pajak-tinggi";
    if (level === "SEDANG") return "wa-pajak-sedang";
    return "wa-pajak-rendah";
  }

  async function predictText(text, topK = 5) {
    const resp = await fetch("/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text, top_k: topK }),
    });
    if (!resp.ok) {
      const payload = await resp.json().catch(() => ({}));
      throw new Error(payload.detail || `HTTP ${resp.status}`);
    }
    return resp.json();
  }

  function renderBubbleVerdict(badgeEl, data) {
    badgeEl.className = `wa-pajak-badge ${riskBadgeClass(data.risk_level)}`;
    badgeEl.replaceChildren();
    const strong = document.createElement("strong");
    strong.textContent = data.risk_title || data.label_text;
    badgeEl.appendChild(strong);

    const details = [];
    if (data.has_apk) details.push("Ada berkas .apk berbahaya");
    if (Array.isArray(data.suspicious_domains) && data.suspicious_domains.length > 0) {
      details.push(`Tautan luar DJP: ${data.suspicious_domains.join(", ")}`);
    } else if (
      data.risk_level === "RENDAH" &&
      Array.isArray(data.official_domains) &&
      data.official_domains.length > 0
    ) {
      details.push(`Tautan resmi: ${data.official_domains.join(", ")}`);
    } else if (Array.isArray(data.plain_reasons) && data.plain_reasons.length > 0) {
      details.push(data.plain_reasons[0].title);
    }

    if (details.length > 0) {
      badgeEl.appendChild(document.createElement("br"));
      const sub = document.createElement("small");
      const timing = data.inference_ms ? ` (${data.inference_ms} ms)` : "";
      sub.textContent = `${details.join(" | ")}${timing}`;
      badgeEl.appendChild(sub);
    }
  }

  messageBubbles.forEach((bubble) => {
    const btn = bubble.querySelector(".wa-pajak-btn");
    const textNode = bubble.querySelector(".selectable-text");
    const badge = bubble.querySelector(".wa-pajak-badge");
    if (!btn || !textNode || !badge) return;

    btn.addEventListener("click", async () => {
      const text = (textNode.textContent || "").trim();
      if (!text) return;
      btn.disabled = true;
      btn.textContent = "Memeriksa...";
      try {
        const data = await predictText(text, 5);
        renderBubbleVerdict(badge, data);
      } catch (err) {
        badge.className = "wa-pajak-badge wa-pajak-sedang";
        badge.textContent = `Gagal memeriksa: ${err.message}`;
      } finally {
        btn.disabled = false;
        btn.textContent = "Periksa Ulang";
      }
    });
  });

  async function refreshHealth() {
    if (!popupStatus) return;
    try {
      const resp = await fetch("/health");
      if (!resp.ok) throw new Error("offline");
      popupStatus.textContent = "Layanan Siap";
      popupStatus.className = "popup-status status-ok";
    } catch {
      popupStatus.textContent = "Layanan Offline";
      popupStatus.className = "popup-status status-warn";
    }
  }

  if (popupBtn && popupInput && popupOut) {
    popupBtn.addEventListener("click", async () => {
      const rawText = popupInput.value.trim();
      if (!rawText) {
        popupOut.className = "popup-out tone-warn";
        popupOut.textContent = "Tempel isi pesan WA terlebih dahulu.";
        return;
      }
      popupBtn.disabled = true;
      popupBtn.textContent = "Memeriksa...";
      try {
        const data = await predictText(rawText.slice(0, 5000), 5);
        const tone =
          data.risk_level === "TINGGI"
            ? "tone-danger"
            : data.risk_level === "SEDANG"
              ? "tone-warn"
              : "tone-safe";
        popupOut.className = `popup-out ${tone}`;
        popupOut.replaceChildren();

        const title = document.createElement("strong");
        title.textContent = data.risk_title || data.label_text;
        popupOut.appendChild(title);

        if (data.confidence_note) {
          popupOut.appendChild(document.createElement("br"));
          const conf = document.createElement("small");
          conf.textContent = data.confidence_note;
          popupOut.appendChild(conf);
        }

        if (Array.isArray(data.plain_reasons) && data.plain_reasons.length > 0) {
          popupOut.appendChild(document.createElement("br"));
          const reason = document.createElement("span");
          reason.textContent = `Alasan: ${data.plain_reasons[0].title}.`;
          popupOut.appendChild(reason);
        }

        popupOut.appendChild(document.createElement("br"));
        const rec = document.createElement("span");
        rec.textContent = data.recommendation;
        popupOut.appendChild(rec);
      } catch (err) {
        popupOut.className = "popup-out tone-danger";
        popupOut.textContent = `Gagal memeriksa: ${err.message}`;
      } finally {
        popupBtn.disabled = false;
        popupBtn.textContent = "Cek Pesan Sekarang";
      }
    });
  }

  refreshHealth();
})();
