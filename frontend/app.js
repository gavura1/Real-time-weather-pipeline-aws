const BASE_URL = 'http://localhost:8000';
const CITY = 'Banska Bystrica';

function getIcon(temp, description) {
  const d = (description || '').toLowerCase();
  if (d.includes('rain') || d.includes('drizzle')) return 'ti-cloud-rain';
  if (d.includes('snow')) return 'ti-snowflake';
  if (d.includes('thunder') || d.includes('storm')) return 'ti-storm';
  if (d.includes('cloud')) return 'ti-cloud';
  if (d.includes('fog') || d.includes('mist')) return 'ti-mist';
  if (temp < 0) return 'ti-snowflake';
  return 'ti-sun';
}

function getTempColor(temp) {
  if (temp <= 0) return '#60a5fa';
  if (temp <= 10) return '#94a3b8';
  if (temp <= 20) return '#4ade80';
  if (temp <= 30) return '#fbbf24';
  return '#f87171';
}

async function loadWeather() {
  const statusBar = document.getElementById('status-bar');
  const content = document.getElementById('weather-content');
  const lastUpdated = document.getElementById('last-updated');

  let healthy = false;
  try {
    const r = await fetch(`${BASE_URL}/health`);
    healthy = r.ok;
  } catch {}

  try {
    const [weatherRes, statusRes] = await Promise.all([
      fetch(`${BASE_URL}/weather/current?city=${encodeURIComponent(CITY)}`),
      fetch(`${BASE_URL}/weather/status?city=${encodeURIComponent(CITY)}`)
    ]);

    const statusData = statusRes.ok ? await statusRes.json() : null;
    const source = statusData?.source || 'unknown';
    const redis = statusData?.redis || 'unknown';
    const ageSeconds = statusData?.age_seconds;

    let ageText = '';
    if (ageSeconds != null) {
      ageText = ageSeconds < 60 ? `pred ${ageSeconds}s` : `pred ${Math.round(ageSeconds / 60)}min`;
    }

    const sourceBadgeClass = source === 'current' ? 'ok' : source === 'last_good' ? 'warn' : 'error';
    const sourceLabel = source === 'current' ? 'live data' : source === 'last_good' ? 'záložné dáta' : 'žiadne dáta';

    statusBar.innerHTML = `
      <span class="badge ${healthy ? 'ok' : 'error'}">
        <i class="ti ${healthy ? 'ti-circle-check' : 'ti-circle-x'}"></i>
        backend ${healthy ? 'ok' : 'nedostupný'}
      </span>
      <span class="badge ${redis === 'ok' ? 'ok' : 'error'}">
        <i class="ti ti-database"></i> redis ${redis}
      </span>
      <span class="badge ${sourceBadgeClass}">
        <i class="ti ti-database-import"></i> ${sourceLabel}
      </span>
      ${ageText ? `<span class="badge"><i class="ti ti-clock"></i> ${ageText}</span>` : ''}
    `;

    if (!weatherRes.ok) throw new Error(`HTTP ${weatherRes.status}`);
    const w = await weatherRes.json();

    const temp = Math.round(w.temperature ?? 0);
    const feelsLike = Math.round(w.feels_like ?? temp);
    const windNum = w.wind ? Math.round(parseFloat(w.wind)) : null;
    const wind = windNum !== null ? `${windNum} km/h` : '—';
    const description = w.condition || '';
    const icon = getIcon(temp, description);
    const tempColor = getTempColor(temp);

    content.className = 'main-card';
    content.innerHTML = `
      <div class="city-row">
        <div class="city-name">
          <i class="ti ti-map-pin" style="font-size:16px; vertical-align:-2px; margin-right:4px;"></i>
          ${CITY}
        </div>
        <i class="ti ${icon} weather-icon"></i>
      </div>
      <div class="temp-big" style="color:${tempColor}">${temp}°C</div>
      <div class="meta-grid">
        <div class="meta-card">
          <div class="meta-label"><i class="ti ti-thermometer" style="font-size:13px;"></i> Pocitovo</div>
          <div class="meta-value">${feelsLike}°C</div>
        </div>
        <div class="meta-card">
          <div class="meta-label"><i class="ti ti-wind" style="font-size:13px;"></i> Vietor</div>
          <div class="meta-value">${wind}</div>
        </div>
      </div>
    `;

    lastUpdated.textContent = `Posledná aktualizácia: ${new Date().toLocaleTimeString('sk-SK')}`;

  } catch (err) {
    statusBar.innerHTML = `<span class="badge error"><i class="ti ti-circle-x"></i> backend nedostupný</span>`;
    content.className = 'error-card';
    content.innerHTML = `<i class="ti ti-alert-circle"></i><p>Nepodarilo sa načítať počasie.</p>`;
  }
}

loadWeather();
setInterval(loadWeather, 30000);