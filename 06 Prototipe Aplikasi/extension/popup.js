const BASE_URL = "http://127.0.0.1:8000";

async function checkHealth() {
  const statusEl = document.getElementById("api-status");
  try {
    const resp = await fetch(`${BASE_URL}/health`);
    if (!resp.ok) throw new Error("offline");
    statusEl.textContent = "Status API: Terhubung (FastAPI aktif)";
    statusEl.style.color = "#166534";
  } catch {
    statusEl.textContent = "Status API: Offline (jalankan uvicorn api:app)";
    statusEl.style.color = "#991b1b";
  }
}

document.getElementById("check-btn").addEventListener("click", async () => {
  const text = document.getElementById("msg-input").value.trim();
  const out = document.getElementById("output");
  if (!text) {
    out.style.display = "block";
    out.style.background = "#fffbeb";
    out.textContent = "Masukkan teks pesan terlebih dahulu.";
    return;
  }

  try {
    const resp = await fetch(`${BASE_URL}/predict`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text, top_k: 5 }),
    });
    const data = await resp.json();
    out.style.display = "block";
    out.style.background =
      data.risk_level === "TINGGI"
        ? "#fef2f2"
        : data.risk_level === "SEDANG"
          ? "#fffbeb"
          : "#f0fdf4";
    out.innerHTML =
      `<strong>${data.label_text} (${data.risk_level})</strong><br>` +
      `Probabilitas SVM: ${(data.svm_probability * 100).toFixed(1)}%<br>` +
      `${data.recommendation}`;
  } catch (err) {
    out.style.display = "block";
    out.style.background = "#fef2f2";
    out.textContent = `Gagal menghubungi FastAPI: ${err.message}`;
  }
});

checkHealth();
