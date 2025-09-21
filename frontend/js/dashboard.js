let map;
const markers = {}; // alert_uuid -> Leaflet marker

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
    const res = await fetch('/alerts/?unresolved_only=false'); // fetch all alerts
    if (!res.ok) throw new Error(`Failed to fetch alerts: ${res.status}`);
    const alerts = await res.json();

    console.log("Fetched alerts:", alerts);

    if (!Array.isArray(alerts)) return console.error("Expected an array of alerts");

    updateAlerts(alerts);
  } catch (err) {
    console.error("Error fetching alerts:", err);
  }
}

function updateAlerts(alerts) {
  const table = document.getElementById('alertsTable');
  if (!table) return console.error('Missing #alertsTable');

  const tbody = table.querySelector('tbody');
  tbody.innerHTML = '';

  const seen = new Set();

  alerts.forEach(alert => {
    const alertId = alert.alert_uuid;
    const tempId = alert.temp_id;
    const lat = alert.lat != null ? Number(alert.lat) : null;
    const lon = alert.lon != null ? Number(alert.lon) : null;
    const ts = alert.timestamp ? new Date(alert.timestamp).toLocaleString() : '';
    const resolved = Boolean(alert.resolved);

    // Table row
    const tr = document.createElement('tr');
    if (resolved) tr.classList.add('table-success');

    tr.innerHTML = `
      <td>${tempId}</td>
      <td>${ts}</td>
      <td>${lat != null ? lat.toFixed(5) : '—'}</td>
      <td>${lon != null ? lon.toFixed(5) : '—'}</td>
    `;
    tbody.appendChild(tr);

    // Map marker
    if (lat != null && lon != null && !(lat === 0 && lon === 0)) {
      if (markers[alertId]) {
        markers[alertId].setLatLng([lat, lon]);
        markers[alertId].setPopupContent(
          `<b>Temp ID:</b> ${tempId}<br/><b>Time:</b> ${ts}<br/><b>Resolved:</b> ${resolved ? 'Yes' : 'No'}`
        );
      } else {
        const marker = L.marker([lat, lon]).addTo(map);
        marker.bindPopup(
          `<b>Temp ID:</b> ${tempId}<br/><b>Time:</b> ${ts}<br/><b>Resolved:</b> ${resolved ? 'Yes' : 'No'}`
        );
        markers[alertId] = marker;
      }
      seen.add(alertId);
    }
  });

  // Remove stale markers
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
  setInterval(fetchAlerts, 15000);

  const refreshBtn = document.getElementById('refreshBtn');
  if (refreshBtn) refreshBtn.addEventListener('click', fetchAlerts);
});
