const API_HOST = 'http://localhost:8001'; // Backend host
let map;
const markers = {};

/** Initialize Leaflet map */
function ensureMap() {
    if (!map) {
        map = L.map('map').setView([25.57, 91.88], 8);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 18,
            attribution: '© OpenStreetMap contributors'
        }).addTo(map);
    }
    return map;
}

/** Consolidate raw alerts with same UUID */
function processAndConsolidateAlerts(rawAlerts) {
    const alertsMap = new Map();
    rawAlerts.forEach(record => {
        if (!record?.alert_uuid) return;
        const existing = alertsMap.get(record.alert_uuid);
        alertsMap.set(record.alert_uuid, { ...existing, ...record });
    });
    return Array.from(alertsMap.values());
}

/** Fetch alerts from API */
async function fetchAlerts() {
    try {
        const filter = document.getElementById('resolvedFilter').value;
        let path = '/alerts/';
        if (filter === 'unresolved') path = '/alerts/?unresolved_only=true';
        if (filter === 'resolved') path = '/alerts/?resolved_only=true';
        const url = `${API_HOST}${path}`;

        const res = await fetch(url);
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const rawData = await res.json();
        if (!Array.isArray(rawData)) throw new Error("Invalid API response");

        const alerts = processAndConsolidateAlerts(rawData);
        updateDashboard(alerts);
    } catch (err) {
        console.error(err);
        const tbody = document.getElementById('alertsTableBody');
        if (tbody) tbody.innerHTML = `<tr><td colspan="7" class="text-center text-danger">Failed to load alerts.</td></tr>`;
    }
}

/** Update table and map markers */
function updateDashboard(alerts) {
    const tbody = document.getElementById('alertsTableBody');
    if (!tbody) return;

    tbody.innerHTML = '';
    const mapInstance = ensureMap();
    const seen = new Set();

    if (alerts.length === 0) {
        tbody.innerHTML = `<tr><td colspan="7" class="text-center">No alerts found.</td></tr>`;
        return;
    }

    alerts.forEach(alert => {
        const { alert_uuid, temp_id, lat, lon, timestamp, resolved, message, resolved_by, resolved_at } = alert;
        const tr = document.createElement('tr');
        if (resolved) tr.classList.add('table-success');

        const displayLat = lat != null ? Number(lat).toFixed(5) : '—';
        const displayLon = lon != null ? Number(lon).toFixed(5) : '—';
        const time = timestamp ? new Date(timestamp).toLocaleString() : '—';
        const status = resolved ? 'Resolved' : 'Unresolved';
        const actionButton = !resolved ? `<button class="btn btn-sm btn-success" onclick="resolveAlert('${alert_uuid}')">Resolve</button>` : '—';

        tr.innerHTML = `
            <td>${temp_id || '—'}</td>
            <td>${time}</td>
            <td>${displayLat}</td>
            <td>${displayLon}</td>
            <td>${message || '—'}</td>
            <td>${status}</td>
            <td>${actionButton}</td>
        `;
        tbody.appendChild(tr);

        if (lat != null && lon != null && !(lat === 0 && lon === 0)) {
            const popup = `
                <b>Tourist ID:</b> ${temp_id}<br>
                <b>Time:</b> ${time}<br>
                <b>Message:</b> ${message || 'N/A'}<br>
                <b>Status:</b> ${status}
                ${resolved ? `<br><b>Resolved By:</b> ${resolved_by} at ${resolved_at ? new Date(resolved_at).toLocaleTimeString() : 'N/A'}` : ''}
            `;
            if (markers[alert_uuid]) {
                markers[alert_uuid].setLatLng([lat, lon]).setPopupContent(popup);
            } else {
                const marker = L.marker([lat, lon]).addTo(mapInstance).bindPopup(popup);
                markers[alert_uuid] = marker;
            }
            seen.add(alert_uuid);
        }
    });

    Object.keys(markers).forEach(id => {
        if (!seen.has(id)) {
            mapInstance.removeLayer(markers[id]);
            delete markers[id];
        }
    });
}

/** Placeholder resolve function */
function resolveAlert(alertId) {
    if (!confirm(`Resolve alert ${alertId}?`)) return;
    alert(`Demo: would call API to resolve ${alertId}`);
    fetchAlerts();
}

// --- Initialize dashboard ---
document.addEventListener('DOMContentLoaded', () => {
    ensureMap();
    fetchAlerts();
    setInterval(fetchAlerts, 30000);
    document.getElementById('refreshBtn')?.addEventListener('click', fetchAlerts);
    document.getElementById('resolvedFilter')?.addEventListener('change', fetchAlerts);
});
