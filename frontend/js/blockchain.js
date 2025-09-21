async function loadBlockchain() {
  const out = document.getElementById('blocks');
  const status = document.getElementById('blockchainStatus');

  if (!out || !status) {
    console.error('Missing #blocks or #blockchainStatus');
    return;
  }

  out.innerHTML = 'Loading...';
  status.textContent = 'Checking blockchain validity...';

  try {
    // 1️⃣ Check blockchain validity
    const valRes = await fetch('/blockchain/validate');
    if (!valRes.ok) throw new Error(`Validation failed: ${valRes.status}`);
    const valData = await valRes.json();
    if (valData.valid) {
      status.textContent = '✅ Blockchain is valid';
      status.className = 'mb-3 text-success fw-bold';
    } else {
      status.textContent = '❌ Blockchain is invalid';
      status.className = 'mb-3 text-danger fw-bold';
    }

    // 2️⃣ Load blocks
    const res = await fetch('/blockchain/list');
    if (!res.ok) throw new Error(`Failed to load blockchain: ${res.status}`);
    const data = await res.json();
    const chain = data && Array.isArray(data.chain) ? data.chain : [];

    out.innerHTML = '';
    if (chain.length === 0) {
      out.textContent = 'No blocks available.';
      return;
    }

    chain.forEach(block => {
      const idx = block.index ?? '—';
      const ts = block.timestamp ?? '—';
      const hash = block.hash ?? '—';
      const prev = block.prev_hash ?? '—';
      const dataPretty = JSON.stringify(block.data ?? {}, null, 2);

      const card = document.createElement('div');
      card.className = 'card mb-2';
      card.style.padding = '12px';
      card.innerHTML = `
        <div><strong>Index:</strong> ${idx}</div>
        <div><strong>Timestamp:</strong> ${ts}</div>
        <div><strong>Hash:</strong> <code>${hash}</code></div>
        <div><strong>Prev Hash:</strong> <code>${prev}</code></div>
        <pre style="white-space:pre-wrap;margin-top:8px;">${dataPretty}</pre>
      `;
      out.appendChild(card);
    });

  } catch (err) {
    console.error(err);
    status.textContent = `❌ Error: ${err.message}`;
    status.className = 'mb-3 text-danger fw-bold';
    out.textContent = '';
  }
}

// Reload button
document.addEventListener('DOMContentLoaded', () => {
  loadBlockchain();
  const btn = document.getElementById('loadBtn');
  if (btn) btn.addEventListener('click', loadBlockchain);
});
