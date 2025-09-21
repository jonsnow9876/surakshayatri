document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('registerForm');
  const qrArea = document.getElementById('qrArea');
  const qrImage = document.getElementById('qrImage');
  const regMsg = document.getElementById('regMsg');
  const submitBtn = form.querySelector('button[type="submit"]');

  form.addEventListener('submit', async (ev) => {
    ev.preventDefault();

    // Reset UI
    regMsg.textContent = '';
    qrArea.style.display = 'none';
    qrImage.innerHTML = '';

    // Disable button during request
    submitBtn.disabled = true;
    submitBtn.textContent = 'Registering...';

    const fd = new FormData(form);
    const payload = {
      name: fd.get('name'),
      passport: fd.get('passport'),
      itinerary: fd.get('itinerary') || null,
      emergency_contact: fd.get('emergency_contact')
    };

    try {
      const res = await fetch('/register/new', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(payload)
      });

      const data = await res.json();

      if (!res.ok) {
        const msg = data?.detail || `Server returned ${res.status}`;
        regMsg.textContent = `Registration failed: ${msg}`;
        return;
      }

      // Success: show QR
      if (data?.qr_code_base64) {
        const img = document.createElement('img');
        img.alt = 'Registration QR';
        img.src = `data:image/png;base64,${data.qr_code_base64}`;
        qrImage.appendChild(img);
        qrArea.style.display = 'block';
      }

      regMsg.innerHTML = `Registered successfully.<br>
        Tourist ID: <code>${data?.tourist_id ?? 'N/A'}</code><br>
        Temp ID: <code>${data?.temp_id ?? 'N/A'}</code>`;
      form.reset();

    } catch (err) {
      console.error(err);
      regMsg.textContent = 'Registration failed: could not reach the server.';
    } finally {
      submitBtn.disabled = false;
      submitBtn.textContent = 'Register & Generate QR';
    }
  });
});