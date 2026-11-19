const FALLBACK_BASE_URL = "http://127.0.0.1:8000";

function sendExtensionMessage(payload) {
  return new Promise((resolve, reject) => {
    if (typeof chrome !== "undefined" && chrome.runtime && chrome.runtime.sendMessage) {
      chrome.runtime.sendMessage(payload, (reply) => {
        if (chrome.runtime.lastError) {
          reject(new Error(chrome.runtime.lastError.message));
          return;
        }
        resolve(reply);
      });
      return;
    }
    reject(new Error("no-runtime"));
  });
}

async function checkHealth() {
  const statusEl = document.getElementById("api-status");
  try {
    const reply = await sendExtensionMessage({ type: "WA_PAJAK_HEALTH" });
    if (reply && reply.ok) {
      statusEl.textContent = "Siap";
      statusEl.style.background = "#f0fdf4";
      statusEl.style.color = "#166534";
      return;
    }
    throw new Error("offline");
  } catch {
    try {
      const resp = await fetch(`${FALLBACK_BASE_URL}/health`);
      if (!resp.ok) throw new Error("offline");
      statusEl.textContent = "Siap";
      statusEl.style.background = "#f0fdf4";
      statusEl.style.color = "#166534";
    } catch {
      statusEl.textContent = "Server Offline";
      statusEl.style.background = "#fffbeb";
      statusEl.style.color = "#92400e";
    }
  }
}

document.getElementById("check-btn").addEventListener("click", async () => {
  const rawText = document.getElementById("msg-input").value.trim();
  const out = document.getElementById("output");
  if (!rawText) {
    out.style.display = "block";
    out.style.background = "#fffbeb";
    out.style.color = "#92400e";
    out.textContent = "Paste pesan WA dulu.";
    return;
  }
  const text = rawText.slice(0, 5000);

  try {
    let data;
    try {
      const reply = await sendExtensionMessage({ type: "WA_PAJAK_PREDICT", text, topK: 5 });
      if (!reply || !reply.ok) throw new Error((reply && reply.error) || "offline");
      data = reply.data;
    } catch {
      const resp = await fetch(`${FALLBACK_BASE_URL}/predict`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text, top_k: 5 }),
      });
      if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
      data = await resp.json();
    }

    out.style.display = "block";
    if (data.risk_level === "TINGGI") {
      out.style.background = "#fef2f2";
      out.style.color = "#991b1b";
    } else if (data.risk_level === "SEDANG") {
      out.style.background = "#fffbeb";
      out.style.color = "#92400e";
    } else {
      out.style.background = "#f0fdf4";
      out.style.color = "#166534";
    }

    const firstReason =
      data.plain_reasons && data.plain_reasons.length > 0
        ? data.plain_reasons[0].title
        : "";

    out.replaceChildren();
    const titleEl = document.createElement("strong");
    titleEl.textContent = data.risk_title || data.label_text;
    out.appendChild(titleEl);

    if (data.confidence_note) {
      out.appendChild(document.createElement("br"));
      const confEl = document.createElement("small");
      confEl.textContent = data.confidence_note;
      out.appendChild(confEl);
    }

    if (firstReason) {
      out.appendChild(document.createElement("br"));
      const reasonEl = document.createElement("div");
      reasonEl.style.marginTop = "4px";
      reasonEl.textContent = `Alasan: ${firstReason}.`;
      out.appendChild(reasonEl);
    }

    out.appendChild(document.createElement("br"));
    const recEl = document.createElement("div");
    recEl.style.marginTop = "4px";
    recEl.textContent = data.recommendation;
    out.appendChild(recEl);
  } catch (err) {
    const errMsg = (err && err.message) || "";
    out.style.display = "block";
    out.style.background = "#fef2f2";
    out.style.color = "#991b1b";
    if (errMsg.includes("HTTP 429")) {
      out.textContent = "Terlalu banyak permintaan. Coba lagi sebentar.";
    } else if (errMsg.includes("HTTP 422")) {
      out.textContent = "Format teks pesan tidak valid atau melebihi batas panjang.";
    } else {
      out.textContent = "Server belum aktif di port 8000. Jalankan Cek Pesan Pajak dulu.";
    }
  }
});

checkHealth();
