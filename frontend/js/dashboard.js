// js/dashboard.js
// Ensure Leaflet assets are loaded in dashboard.html before this script.
let map;
const markers = {}; // tempid -> Leaflet marker

function ensureMap() {
  if (!map) {
    map = L.map('map').setView([25.57, 91.88], 8);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 18,
      attribution: '© OpenStreetMap contributors'
    }).addTo(map);
  }
}

async function fetchAlerts() {
  try {
    const res = await fetch('/alerts?unresolved_only=false');
    if (!res.ok) throw new Error(`Failed to fetch alerts: ${res.status}`);
    const alerts = await res.json(); // [{ alertuuid, tempid, lat, lon, timestamp, resolved, ... }]
    updateAlerts(alerts || []);
  } catch (err) {
    console.error(err);
  }
}

function updateAlerts(alerts) {
  const table = document.getElementById('alertsTable');
  if (!table) {
    console.error('Missing #alertsTable');
    return;
  }
  const tbody = table.querySelector('tbody') || table.createTBody();
  tbody.innerHTML = '';

  const seen = new Set();

  alerts.forEach(a => {
    const id = a?.tempid || 'unknown';
    const lat = Number(a?.lat);
    const lon = Number(a?.lon);
    const ts = a?.timestamp || '';
    const resolved = Boolean(a?.resolved);

    // Table row
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td>${id}</td>
      <td>${ts}</td>
      <td>${isFinite(lat) && isFinite(lon) ? `${lat.toFixed(5)}, ${lon.toFixed(5)}` : '—'}</td>
      <td>${resolved ? 'Yes' : 'No'}</td>
    `;
    tbody.appendChild(tr);

    // Marker
    if (isFinite(lat) && isFinite(lon)) {
      if (markers[id]) {
        markers[id].setLatLng([lat, lon]);
      } else {
        const m = L.marker([lat, lon]).addTo(map);
        m.bindPopup(`<b>Temp ID:</b> ${id}<br/><b>Time:</b> ${ts}<br/><b>Resolved:</b> ${resolved ? 'Yes' : 'No'}`);
        markers[id] = m;
      }
      seen.add(id);
    }
  });

  // Cleanup stale markers
  Object.keys(markers).forEach(id => {
    if (!seen.has(id)) {
      map.removeLayer(markers[id]);
      delete markers[id];
    }
  });
}

document.addEventListener('DOMContentLoaded', () => {
  ensureMap();
  fetchAlerts();
  // Auto-refresh every 15s; adjust as needed.
  setInterval(fetchAlerts, 15000);
});
