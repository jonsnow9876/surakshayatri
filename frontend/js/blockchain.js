// js/blockchain.js
async function loadBlockchain() {
  const out = document.getElementById('blocks');
  if (!out) {
    console.error('Missing #blocks');
    return;
  }
  out.innerHTML = 'Loading...';

  try {
    const res = await fetch('/blockchain');
    if (!res.ok) throw new Error(`Failed to load blockchain: ${res.status}`);
    const chain = await res.json(); // array of blocks

    out.innerHTML = '';
    (chain || []).forEach(b => {
      const idx = b?.index ?? '—';
      const ts = b?.timestamp ?? '—';
      const hash = b?.hash ?? '—';
      const prev = b?.prevhash ?? '—';
      const dataPretty = JSON.stringify(b?.data ?? {}, null, 2);

      const card = document.createElement('div');
      card.className = 'card mb-2';
      card.style.padding = '12px';
      card.innerHTML = `
        <div><strong>Index:</strong> ${idx}</div>
        <div><strong>Timestamp:</strong> ${ts}</div>
        <div><strong>Hash:</strong> <code>${hash}</code></div>
        <div><strong>Prev:</strong> <code>${prev}</code></div>
        <pre style="white-space:pre-wrap;margin-top:8px;">${dataPretty}</pre>
      `;
      out.appendChild(card);
    });

    if (!out.childElementCount) {
      out.textContent = 'No blocks available.';
    }
  } catch (err) {
    console.error(err);
    out.textContent = `Error: ${err.message}`;
  }
}

document.addEventListener('DOMContentLoaded', loadBlockchain);
