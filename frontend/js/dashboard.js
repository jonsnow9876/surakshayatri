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

/** Fetch alerts from API (relative path) */
async function fetchAlerts() {
    try {
        const filter = document.getElementById('resolvedFilter')?.value;
        let path = '/alerts/';
        if (filter === 'unresolved') path = '/alerts/?unresolved_only=true';
        if (filter === 'resolved') path = '/alerts/?resolved_only=true';

        const res = await fetch(path);
        if (!res.ok) throw new Error(`HTTP ${res.status}`);

        const rawData = await res.json();
        if (!Array.isArray(rawData)) throw new Error("Invalid API response");

        const alerts = processAndConsolidateAlerts(rawData);
        updateDashboard(alerts);
    } catch (err) {
        console.error('Failed to fetch alerts:', err);
        const tbody = document.getElementById('alertsTableBody');
        if (tbody) {
            tbody.innerHTML = `<tr><td colspan="7" class="text-center text-danger">
                Failed to load alerts.
            </td></tr>`;
        }
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
        Object.keys(markers).forEach(id => {
            mapInstance.removeLayer(markers[id]);
            delete markers[id];
        });
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
        const actionButton = !resolved
            ? `<button class="btn btn-sm btn-success" onclick="resolveAlert('${alert_uuid}')">Resolve</button>`
            : '—';

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
                markers[alert_uuid] = L.marker([lat, lon]).addTo(mapInstance).bindPopup(popup);
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

/** Resolve an alert by its ID */
async function resolveAlert(alertId) {
    if (!confirm(`Are you sure you want to resolve this alert?`)) return;

    try {
        const resolvedBy = prompt("Enter your name or ID for resolution log:", "dashboard_user");
        if (!resolvedBy) return;

        const url = `/alerts/${alertId}/resolve?resolved_by=${encodeURIComponent(resolvedBy)}`;

        const res = await fetch(url, {
            method: "PATCH", // ✅ CHANGED FROM POST TO PATCH
            headers: { 'Content-Type': 'application/json' }
        });

        if (!res.ok) {
            const errData = await res.json();
            throw new Error(errData.detail || `Failed to resolve. HTTP ${res.status}`);
        }

        console.log("Alert resolved successfully:", await res.json());
        fetchAlerts();
    } catch (err) {
        console.error("Error resolving alert:", err);
        alert(`Failed to resolve alert: ${err.message}`);
    }
}


// --- Initialize dashboard ---
document.addEventListener('DOMContentLoaded', () => {
    ensureMap();
    fetchAlerts();
    setInterval(fetchAlerts, 15000);
    document.getElementById('refreshBtn')?.addEventListener('click', fetchAlerts);
    document.getElementById('resolvedFilter')?.addEventListener('change', fetchAlerts);
});