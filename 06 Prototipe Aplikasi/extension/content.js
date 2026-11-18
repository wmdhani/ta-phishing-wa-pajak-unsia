const FALLBACK_API_ENDPOINT = "http://127.0.0.1:8000/predict";
const APK_INLINE_RE = /\b[a-z0-9_.-]+\.apk\b/i;
const URL_INLINE_RE = /(?:https?:\/\/|www\.)\S+|\b[a-z0-9-]+\.(?:go\.id|co\.id|my\.id|com|xyz|id)\b/i;
const TAX_SELF_TEST_RE = /\b(?:pajak|djp|npwp|spt|coretax|efin|billing|kring)\b/i;

function extractMessageText(row) {
  const parts = [];
  const copyables = row.querySelectorAll("div.copyable-text[data-pre-plain-text], [data-pre-plain-text]");
  const roots = copyables.length > 0 ? Array.from(copyables) : [row];

  roots.forEach((root) => {
    if (root.closest('[data-testid="quoted-message"], .quoted-mention')) return;
    const textNodes = root.querySelectorAll(
      'span.selectable-text, .selectable-text, [data-testid="selectable-text"]'
    );
    if (textNodes.length > 0) {
      textNodes.forEach((node) => {
        if (node.closest('[data-testid="quoted-message"], .quoted-mention')) return;
        const val = (node.innerText || node.textContent || "").trim();
        if (val && !parts.includes(val)) parts.push(val);
      });
    } else {
      const val = (root.innerText || "").trim();
      if (val && !parts.includes(val)) parts.push(val);
    }
  });

  // Tangkap nama berkas .apk pada lampiran dokumen WhatsApp Web tanpa caption panjang.
  row.querySelectorAll('[title*=".apk" i], span[dir="auto"], span[dir="ltr"]').forEach((el) => {
    if (el.closest(".wa-pajak-wrap")) return;
    const candidate = (el.getAttribute("title") || el.textContent || "").trim();
    const match = candidate.match(APK_INLINE_RE);
    if (match && !parts.some((p) => p.toLowerCase().includes(match[0].toLowerCase()))) {
      parts.push(match[0]);
    }
  });

  return parts.join(" ").trim();
}

function mountWrapInBubble(row, wrap) {
  const copyables = row.querySelectorAll("div.copyable-text[data-pre-plain-text], [data-pre-plain-text]");
  const mainCopyable = Array.from(copyables).find(
    (node) => !node.closest('[data-testid="quoted-message"], .quoted-mention')
  );

  let anchor = mainCopyable;
  if (!anchor) {
    anchor = row.querySelector('span.selectable-text, .selectable-text, [data-testid="selectable-text"]');
  }

  if (anchor) {
    let target = anchor;
    while (target.parentElement && target.parentElement !== row) {
      const parentStyle = window.getComputedStyle(target.parentElement);
      const isRowFlex =
        parentStyle.display.includes("flex") && parentStyle.flexDirection === "row";
      const isInline = parentStyle.display.startsWith("inline");
      if (isRowFlex || isInline) {
        target = target.parentElement;
      } else {
        break;
      }
    }
    if (target.parentElement) {
      target.insertAdjacentElement("afterend", wrap);
      return;
    }
  }

  row.appendChild(wrap);
}

function renderResultBadge(wrap, data) {
  let badge = wrap.querySelector(".wa-pajak-badge");
  if (!badge) {
    badge = document.createElement("div");
    wrap.appendChild(badge);
  }

  const riskClass =
    data.risk_level === "TINGGI"
      ? "wa-pajak-tinggi"
      : data.risk_level === "SEDANG"
        ? "wa-pajak-sedang"
        : "wa-pajak-rendah";

  badge.className = `wa-pajak-badge ${riskClass}`;
  badge.replaceChildren();

  const titleEl = document.createElement("strong");
  titleEl.textContent = data.risk_title || data.label_text;
  badge.appendChild(titleEl);

  const detailParts = [];
  if (data.has_apk) {
    detailParts.push("Ada file .apk berbahaya");
  }
  if (data.suspicious_domains && data.suspicious_domains.length > 0) {
    detailParts.push(`Link luar DJP: ${data.suspicious_domains.join(", ")}`);
  } else if (data.official_domains && data.official_domains.length > 0 && data.risk_level === "RENDAH") {
    detailParts.push(`Link resmi: ${data.official_domains.join(", ")}`);
  }
  if (detailParts.length === 0 && data.plain_reasons && data.plain_reasons.length > 0) {
    detailParts.push(data.plain_reasons[0].title);
  }

  if (detailParts.length > 0) {
    badge.appendChild(document.createElement("br"));
    const subEl = document.createElement("small");
    subEl.textContent = detailParts.join(" • ");
    badge.appendChild(subEl);
  }
}

function renderErrorBadge(wrap, messageText) {
  let badge = wrap.querySelector(".wa-pajak-badge");
  if (!badge) {
    badge = document.createElement("div");
    wrap.appendChild(badge);
  }
  badge.className = "wa-pajak-badge wa-pajak-sedang";
  badge.textContent = messageText;
}

function predictViaExtension(text) {
  return new Promise((resolve, reject) => {
    if (typeof chrome !== "undefined" && chrome.runtime && chrome.runtime.sendMessage) {
      try {
        chrome.runtime.sendMessage({ type: "WA_PAJAK_PREDICT", text, topK: 5 }, (reply) => {
          if (chrome.runtime.lastError) {
            const msg = chrome.runtime.lastError.message || "";
            if (msg.includes("Extension context invalidated")) {
              reject(new Error("Ekstensi baru diperbarui. Silakan refresh (F5) halaman WhatsApp Web."));
              return;
            }
            reject(new Error(msg));
            return;
          }
          if (reply && reply.ok) {
            resolve(reply.data);
          } else {
            reject(new Error((reply && reply.error) || "Server port 8000 belum aktif."));
          }
        });
        return;
      } catch (err) {
        reject(err);
        return;
      }
    }

    fetch(FALLBACK_API_ENDPOINT, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text, top_k: 5 }),
    })
      .then((res) => {
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return res.json();
      })
      .then(resolve)
      .catch(reject);
  });
}

function attachScanButton(row) {
  if (!row || row.dataset.pajakAttached === "1" || row.querySelector(".wa-pajak-wrap")) return;

  const text = extractMessageText(row);
  if (!text) return;

  const dataId = row.getAttribute("data-id") || "";
  const isOutgoing =
    row.classList.contains("message-out") ||
    dataId.startsWith("true_") ||
    Boolean(row.closest(".message-out, [data-id^='true_']"));

  const hasHighSignal = APK_INLINE_RE.test(text) || URL_INLINE_RE.test(text);
  if (isOutgoing) {
    if (!hasHighSignal && !TAX_SELF_TEST_RE.test(text)) return;
  } else if (!hasHighSignal && text.length < 8) {
    return;
  }

  row.dataset.pajakAttached = "1";

  const wrap = document.createElement("div");
  wrap.className = "wa-pajak-wrap";

  const btn = document.createElement("button");
  btn.type = "button";
  btn.className = "wa-pajak-btn";
  btn.textContent = "Cek Pesan Pajak";

  btn.addEventListener("click", async (event) => {
    event.preventDefault();
    event.stopPropagation();
    const latestText = extractMessageText(row) || text;
    btn.disabled = true;
    btn.textContent = "Memeriksa...";
    try {
      const data = await predictViaExtension(latestText);
      renderResultBadge(wrap, data);
    } catch (err) {
      const msg =
        err && err.message && err.message.includes("refresh (F5)")
          ? err.message
          : "Server belum aktif di port 8000. Jalankan Cek Pesan Pajak dulu.";
      renderErrorBadge(wrap, msg);
    } finally {
      btn.disabled = false;
      btn.textContent = "Cek Ulang";
    }
  });

  wrap.appendChild(btn);
  mountWrapInBubble(row, wrap);
}

function scanVisibleMessages() {
  const seen = new Set();
  const candidates = document.querySelectorAll(
    'div.message-in, div[data-id^="false_"], div[data-id^="true_"], div[data-pre-plain-text], [data-testid="msg-container"], #main div[role="row"] span.selectable-text, #main div[role="row"] [data-testid="selectable-text"]'
  );
  candidates.forEach((node) => {
    if (node.closest('#pane-side, [data-testid="quoted-message"], .quoted-mention')) return;
    const row =
      node.closest('div.message-in, [data-testid="msg-container"], div[data-id], #main div[role="row"]') ||
      node;
    if (!row || seen.has(row)) return;
    seen.add(row);
    attachScanButton(row);
  });
}

let scanTimer = null;
const observer = new MutationObserver(() => {
  if (scanTimer) return;
  scanTimer = setTimeout(() => {
    scanTimer = null;
    scanVisibleMessages();
  }, 150);
});
observer.observe(document.body, { childList: true, subtree: true });
setInterval(scanVisibleMessages, 1500);
scanVisibleMessages();
