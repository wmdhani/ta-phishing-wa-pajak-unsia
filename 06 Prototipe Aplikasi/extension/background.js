const API_BASES = ["http://127.0.0.1:8000", "http://localhost:8000"];

async function requestPredict(text, topK = 5) {
  let lastError = null;
  for (const base of API_BASES) {
    try {
      const resp = await fetch(`${base}/predict`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text, top_k: topK }),
      });
      if (!resp.ok) {
        const detail = await resp.text().catch(() => "");
        throw new Error(`HTTP ${resp.status}${detail ? `: ${detail}` : ""}`);
      }
      return await resp.json();
    } catch (err) {
      lastError = err;
    }
  }
  throw lastError || new Error("Server lokal port 8000 tidak aktif.");
}

async function requestHealth() {
  for (const base of API_BASES) {
    try {
      const resp = await fetch(`${base}/health`);
      if (resp.ok) {
        return { ok: true, baseUrl: base, data: await resp.json() };
      }
    } catch {
      // Coba host lokal alternatif.
    }
  }
  return { ok: false };
}

chrome.runtime.onMessage.addListener((message, _sender, sendResponse) => {
  if (!message || typeof message !== "object") return false;

  if (message.type === "WA_PAJAK_PREDICT") {
    requestPredict(message.text, message.topK || 5)
      .then((data) => sendResponse({ ok: true, data }))
      .catch((err) => sendResponse({ ok: false, error: err?.message || "Gagal terhubung" }));
    return true;
  }

  if (message.type === "WA_PAJAK_HEALTH") {
    requestHealth()
      .then((result) => sendResponse(result))
      .catch(() => sendResponse({ ok: false }));
    return true;
  }

  return false;
});
