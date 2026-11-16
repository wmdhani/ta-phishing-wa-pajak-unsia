const API_ENDPOINT = "http://127.0.0.1:8000/predict";

function extractMessageText(bubble) {
  const textNode = bubble.querySelector("span.selectable-text");
  return textNode ? textNode.innerText.trim() : "";
}

function renderResultBadge(container, data) {
  let badge = container.querySelector(".wa-pajak-badge");
  if (!badge) {
    badge = document.createElement("div");
    container.appendChild(badge);
  }

  const riskClass =
    data.risk_level === "TINGGI"
      ? "wa-pajak-tinggi"
      : data.risk_level === "SEDANG"
        ? "wa-pajak-sedang"
        : "wa-pajak-rendah";

  badge.className = `wa-pajak-badge ${riskClass}`;
  const triggers = (data.top_triggers || [])
    .slice(0, 3)
    .map((t) => `${t.token} (${t.contribution >= 0 ? "+" : ""}${t.contribution})`)
    .join(", ");

  const apkInfo = data.has_apk ? " | Peringatan: Pola .apk terdeteksi!" : "";
  badge.innerHTML =
    `<strong>${data.label_text} (${data.risk_level})</strong>` +
    ` — Skor SVM: ${(data.svm_probability * 100).toFixed(1)}%${apkInfo}` +
    (triggers ? `<br><small>Pemicu: ${triggers}</small>` : "");
}

function attachScanButton(bubble) {
  if (bubble.dataset.pajakAttached === "1") return;
  const text = extractMessageText(bubble);
  if (!text || text.length < 10) return;

  bubble.dataset.pajakAttached = "1";
  const btn = document.createElement("button");
  btn.type = "button";
  btn.className = "wa-pajak-btn";
  btn.textContent = "Periksa Phishing Pajak";

  btn.addEventListener("click", async () => {
    btn.disabled = true;
    btn.textContent = "Memeriksa...";
    try {
      const response = await fetch(API_ENDPOINT, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text, top_k: 5 }),
      });
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const data = await response.json();
      renderResultBadge(bubble, data);
    } catch (err) {
      let badge = bubble.querySelector(".wa-pajak-badge");
      if (!badge) {
        badge = document.createElement("div");
        bubble.appendChild(badge);
      }
      badge.className = "wa-pajak-badge wa-pajak-sedang";
      badge.textContent = `Gagal terhubung ke API FastAPI (${err.message}). Pastikan uvicorn aktif.`;
    } finally {
      btn.disabled = false;
      btn.textContent = "Periksa Ulang";
    }
  });

  bubble.appendChild(btn);
}

function scanVisibleMessages() {
  document.querySelectorAll("div.message-in").forEach(attachScanButton);
}

const observer = new MutationObserver(() => scanVisibleMessages());
observer.observe(document.body, { childList: true, subtree: true });
scanVisibleMessages();
