// js/register.js - CORRECTED VERSION WITH ALL API FIXES
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
      emergency_contact: fd.get('emergency_contact')  // FIX 1: Changed from 'emergencycontact'
    };

    try {
      const res = await fetch('/register', {  // FIX 2: Changed from '/register/new'
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(payload)
      });
      if (!res.ok) throw new Error(`Server returned ${res.status}`);
      const data = await res.json(); // { tourist_id, temp_id, qr_code_base64 }

      if (data?.qr_code_base64) {  // FIX 3: Changed from 'qrcodebase64'
        const img = document.createElement('img');
        img.alt = 'Registration QR';
        img.src = `data:image/png;base64,${data.qr_code_base64}`;  // FIX 4: Changed from 'qrcodebase64'
        qrImage.innerHTML = '';
        qrImage.appendChild(img);
        qrArea.style.display = 'block';
      }

      const tid = data?.tourist_id ?? 'N/A';  // FIX 5: Changed from 'touristid'
      const tmp = data?.temp_id ?? 'N/A';     // FIX 6: Changed from 'tempid'
      regMsg.innerHTML = `Registered successfully. Tourist ID: <code>${tid}</code>, Temp ID: <code>${tmp}</code>.`;
    } catch (err) {
      console.error(err);
      regMsg.textContent = `Registration failed: ${err.message}`;
    }
  });
});