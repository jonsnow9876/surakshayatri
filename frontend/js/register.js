// js/register.js
document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('registerForm');
  const qrArea = document.getElementById('qrArea');
  const qrImage = document.getElementById('qrImage');
  const regMsg = document.getElementById('regMsg');

  if (!form || !qrArea || !qrImage || !regMsg) {
    console.error('Missing required elements: registerForm/qrArea/qrImage/regMsg');
    return;
  }

  form.addEventListener('submit', async (ev) => {
    ev.preventDefault();
    regMsg.textContent = '';
    qrArea.style.display = 'none';
    qrImage.innerHTML = '';

    const fd = new FormData(form);
    const payload = {
      name: fd.get('name'),
      passport: fd.get('passport'),
      itinerary: fd.get('itinerary') || null,
      emergencycontact: fd.get('emergencycontact')
    };

    try {
      const res = await fetch('/register/new', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(payload)
      });
      if (!res.ok) throw new Error(`Server returned ${res.status}`);
      const data = await res.json(); // { touristid, tempid, qrcodebase64 }

      if (data?.qrcodebase64) {
        const img = document.createElement('img');
        img.alt = 'Registration QR';
        img.src = `data:image/png;base64,${data.qrcodebase64}`;
        qrImage.innerHTML = '';
        qrImage.appendChild(img);
        qrArea.style.display = 'block';
      }

      const tid = data?.touristid ?? 'N/A';
      const tmp = data?.tempid ?? 'N/A';
      regMsg.innerHTML = `Registered successfully. Tourist ID: <code>${tid}</code>, Temp ID: <code>${tmp}</code>.`;
    } catch (err) {
      console.error(err);
      regMsg.textContent = `Registration failed: ${err.message}`;
    }
  });
});
