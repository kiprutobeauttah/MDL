const ICONS = {
  home: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path><polyline points="9 22 9 12 15 12 15 22"></polyline></svg>`,
  activity: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"></polyline></svg>`,
  wifi: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12.55a11 11 0 0 1 14.08 0"></path><path d="M1.42 9a16 16 0 0 1 21.16 0"></path><path d="M8.53 16.11a6 6 0 0 1 6.95 0"></path><line x1="12" y1="20" x2="12.01" y2="20"></line></svg>`,
  smartphone: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="5" y="2" width="14" height="20" rx="2" ry="2"></rect><line x1="12" y1="18" x2="12.01" y2="18"></line></svg>`,
  bluetooth: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6.5 6.5 17.5 17.5 12 23 12 1 17.5 6.5 6.5 17.5"></polyline></svg>`,
  package: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="16.5" y1="9.4" x2="7.5" y2="4.21"></line><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path><polyline points="3.27 6.96 12 12.01 20.73 6.96"></polyline><line x1="12" y1="22.08" x2="12" y2="12"></line></svg>`,
  compass: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76"></polygon></svg>`,
  battery: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="1" y="6" width="18" height="12" rx="2" ry="2"></rect><line x1="23" y1="13" x2="23" y2="11"></line></svg>`,
  cpu: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="4" width="16" height="16" rx="2" ry="2"></rect><rect x="9" y="9" width="6" height="6"></rect><line x1="9" y1="1" x2="9" y2="4"></line><line x1="15" y1="1" x2="15" y2="4"></line><line x1="9" y1="20" x2="9" y2="23"></line><line x1="15" y1="20" x2="15" y2="23"></line><line x1="20" y1="9" x2="23" y2="9"></line><line x1="20" y1="14" x2="23" y2="14"></line><line x1="1" y1="9" x2="4" y2="9"></line><line x1="1" y1="14" x2="4" y2="14"></line></svg>`,
  "hard-drive": `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="22" y1="12" x2="2" y2="12"></line><path d="M5.45 5.11L2 12v6a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-6l-3.45-6.89A2 2 0 0 0 16.76 4H7.24a2 2 0 0 0-1.79 1.11z"></path><line x1="6" y1="16" x2="6.01" y2="16"></line><line x1="10" y1="16" x2="10.01" y2="16"></line></svg>`,
  settings: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"></circle><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path></svg>`,
  "bar-chart-2": `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="20" x2="18" y2="10"></line><line x1="12" y1="20" x2="12" y2="4"></line><line x1="6" y1="20" x2="6" y2="14"></line></svg>`,
  "file-text": `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg>`,
  "alert-triangle": `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path><line x1="12" y1="9" x2="12" y2="13"></line><line x1="12" y1="17" x2="12.01" y2="17"></line></svg>`,
};

const CHARTS = [];

const state = {
  devices: [],
  selectedSerial: null,
  device: {},
  apps: [],
  appsLoaded: false,
  appsLoading: false,
  events: [],
  maxEvents: 100,
  ramUsed: 0,
  ramTotal: 0,
  storageUsed: 0,
  storageTotal: 0,
  batteryLevel: null,
  charts: {},
};

const $ = (selector, root = document) => root.querySelector(selector);
const $$ = (selector, root = document) => Array.from(root.querySelectorAll(selector));

function invoke(command, args) {
  if (window.__TAURI__ && window.__TAURI__.core) {
    return window.__TAURI__.core.invoke(command, args);
  }
  return Promise.reject(new Error("Tauri backend is not available"));
}

function cssVar(name) {
  return getComputedStyle(document.documentElement).getPropertyValue(name).trim();
}

function escapeHtml(value) {
  return String(value).replace(/[&<>"']/g, (character) => {
    const entities = {
      "&": "&amp;",
      "<": "&lt;",
      ">": "&gt;",
      '"': "&quot;",
      "'": "&#39;",
    };
    return entities[character];
  });
}

function formatValue(value) {
  if (value === null || value === undefined) {
    return "--";
  }
  if (typeof value === "boolean") {
    return value ? "true" : "false";
  }
  if (typeof value === "object") {
    return JSON.stringify(value);
  }
  return String(value);
}

function formatNumber(value, digits = 1) {
  if (typeof value !== "number" || !Number.isFinite(value)) {
    return "--";
  }
  return value.toFixed(digits);
}

function setStatus(kind, text) {
  const dot = $("#status-dot");
  dot.className = `status-dot ${kind || ""}`.trim();
  dot.textContent = "●";
  $("#status-text").textContent = text;
}

function setConnectionMessage(text) {
  $("#connection-message").textContent = text || "";
}

function setDetail(root, key, value) {
  const element = $(`[data-detail="${key}"]`, root);
  if (element) {
    element.textContent = value === undefined || value === null || value === "" ? "--" : String(value);
  }
}

class Chart {
  constructor(canvas, series, options = {}) {
    this.canvas = canvas;
    this.series = series.map((item) => ({ ...item, data: [] }));
    this.maxPoints = options.maxPoints || 60;
    this.renderQueued = false;
    CHARTS.push(this);
  }

  push(name, value) {
    const series = this.series.find((item) => item.name === name);
    if (!series) {
      return;
    }
    const number = Number(value);
    series.data.push(Number.isFinite(number) ? number : 0);
    if (series.data.length > this.maxPoints) {
      series.data.shift();
    }
    this.render();
  }

  render() {
    const canvas = this.canvas;
    if (!canvas) {
      return;
    }

    const rect = canvas.getBoundingClientRect();
    if (rect.width < 4 || rect.height < 4) {
      return;
    }

    const dpr = window.devicePixelRatio || 1;
    const width = Math.floor(rect.width);
    const height = Math.floor(rect.height);

    if (canvas.width !== Math.floor(width * dpr) || canvas.height !== Math.floor(height * dpr)) {
      canvas.width = Math.floor(width * dpr);
      canvas.height = Math.floor(height * dpr);
    }

    const context = canvas.getContext("2d");
    context.setTransform(dpr, 0, 0, dpr, 0, 0);
    context.clearRect(0, 0, width, height);

    const padding = { left: 42, right: 10, top: 10, bottom: 18 };
    const plotWidth = width - padding.left - padding.right;
    const plotHeight = height - padding.top - padding.bottom;

    context.font = '10px "Segoe UI", system-ui, sans-serif';
    context.fillStyle = cssVar("--text-secondary");
    context.strokeStyle = cssVar("--border");
    context.lineWidth = 1;

    const values = this.series.flatMap((item) => item.data);
    const hasData = values.length > 0;

    let min = hasData ? Math.min(...values) : 0;
    let max = hasData ? Math.max(...values) : 1;

    if (min === max) {
      min -= 1;
      max += 1;
    }

    const spread = max - min;
    min -= spread * 0.1;
    max += spread * 0.1;

    const rows = 4;
    for (let row = 0; row <= rows; row += 1) {
      const y = padding.top + (plotHeight / rows) * row;
      context.beginPath();
      context.moveTo(padding.left, y);
      context.lineTo(padding.left + plotWidth, y);
      context.stroke();

      const value = max - ((max - min) / rows) * row;
      context.textAlign = "right";
      context.textBaseline = "middle";
      context.fillText(value.toFixed(Math.abs(value) >= 10 ? 0 : 1), padding.left - 6, y);
    }

    if (!hasData) {
      context.textAlign = "center";
      context.textBaseline = "middle";
      context.fillStyle = cssVar("--text-secondary");
      context.fillText("Waiting for data", padding.left + plotWidth / 2, padding.top + plotHeight / 2);
      return;
    }

    const toPoint = (value, index, length) => {
      const x = padding.left + (plotWidth * index) / Math.max(1, length - 1);
      const y = padding.top + plotHeight - ((value - min) / (max - min)) * plotHeight;
      return [x, y];
    };

    for (const series of this.series) {
      if (series.data.length === 0) {
        continue;
      }

      if (this.series.length === 1 && series.data.length > 1) {
        const gradient = context.createLinearGradient(0, padding.top, 0, padding.top + plotHeight);
        gradient.addColorStop(0, series.color);
        gradient.addColorStop(1, "rgba(255, 255, 255, 0)");
        context.save();
        context.globalAlpha = 0.12;
        context.beginPath();
        series.data.forEach((value, index) => {
          const [x, y] = toPoint(value, index, series.data.length);
          if (index === 0) {
            context.moveTo(x, y);
          } else {
            context.lineTo(x, y);
          }
        });
        context.lineTo(padding.left + plotWidth, padding.top + plotHeight);
        context.lineTo(padding.left, padding.top + plotHeight);
        context.closePath();
        context.fillStyle = gradient;
        context.fill();
        context.restore();
      }

      context.beginPath();
      context.lineWidth = 2;
      context.strokeStyle = series.color;
      context.lineJoin = "round";
      context.lineCap = "round";

      series.data.forEach((value, index) => {
        const [x, y] = toPoint(value, index, series.data.length);
        if (index === 0) {
          context.moveTo(x, y);
        } else {
          context.lineTo(x, y);
        }
      });
      context.stroke();

      if (series.data.length === 1) {
        const [x, y] = toPoint(series.data[0], 0, 1);
        context.beginPath();
        context.arc(x, y, 3, 0, Math.PI * 2);
        context.fillStyle = series.color;
        context.fill();
      }
    }
  }
}

function setupCharts() {
  const accent = cssVar("--accent");
  const green = cssVar("--green");

  state.charts.cpu = new Chart($("#chart-cpu"), [{ name: "cpu", color: accent }]);
  state.charts.ram = new Chart($("#chart-ram"), [{ name: "ram", color: green }]);
  state.charts.latency = new Chart($("#chart-latency"), [{ name: "latency", color: accent }]);
  state.charts.throughput = new Chart($("#chart-throughput"), [
    { name: "rx", color: green },
    { name: "tx", color: accent },
  ]);
  state.charts.wifiSignal = new Chart($("#chart-wifi-signal"), [{ name: "rssi", color: green }]);
  state.charts.wifiSpeed = new Chart($("#chart-wifi-speed"), [{ name: "speed", color: accent }]);
  state.charts.cellular = new Chart($("#chart-cellular"), [
    { name: "rsrp", color: green },
    { name: "rsrq", color: accent },
  ]);
}

function renderAllCharts() {
  CHARTS.forEach((chart) => chart.render());
}

function injectIcons() {
  $$("[data-icon]").forEach((element) => {
    const text = element.textContent.trim();
    element.innerHTML = `<span class="icon">${ICONS[element.dataset.icon] || ""}</span><span>${escapeHtml(text)}</span>`;
  });
}

function setupNavigation() {
  $("#nav").addEventListener("click", (event) => {
    const button = event.target.closest(".nav-btn");
    if (!button) {
      return;
    }
    setView(button.dataset.view);
  });
}

function setView(view) {
  $$(".nav-btn").forEach((button) => {
    button.classList.toggle("active", button.dataset.view === view);
  });
  $$(".view").forEach((section) => {
    section.classList.toggle("active", section.id === `view-${view}`);
  });
  $("#content").scrollTop = 0;
  if (view === "apps") {
    loadApps();
  }
  requestAnimationFrame(renderAllCharts);
}

function setupConnection() {
  $("#refresh-btn").addEventListener("click", refreshDevices);
  $("#connect-btn").addEventListener("click", connectDevice);
}

async function refreshDevices() {
  setConnectionMessage("Scanning for devices...");
  try {
    state.devices = await invoke("list_devices");
    if (state.selectedSerial && !state.devices.some((device) => device.serial === state.selectedSerial)) {
      state.selectedSerial = null;
    }
    renderDevices();
    setConnectionMessage(state.devices.length === 0 ? "No devices found" : "");
  } catch (error) {
    state.devices = [];
    renderDevices();
    setConnectionMessage(String(error));
  }
}

function renderDevices() {
  const list = $("#device-list");
  const empty = $("#device-empty");
  list.innerHTML = "";

  if (state.devices.length === 0) {
    list.classList.add("hidden");
    empty.classList.remove("hidden");
    $("#connect-btn").disabled = true;
    return;
  }

  list.classList.remove("hidden");
  empty.classList.add("hidden");

  for (const device of state.devices) {
    const online = device.state === "device";
    const row = document.createElement("div");
    row.className = "device-row";
    row.dataset.serial = device.serial;
    row.innerHTML = `
      <span class="dot ${online ? "online" : ""}">${online ? "●" : "○"}</span>
      <div>
        <div class="device-serial">${escapeHtml(device.serial)}</div>
        <div class="device-meta">${escapeHtml(device.connection_type)} • ${escapeHtml(device.state)}</div>
      </div>
    `;
    row.addEventListener("click", () => selectDevice(device.serial));
    list.append(row);
  }

  applySelection();
}

function selectDevice(serial) {
  state.selectedSerial = serial;
  applySelection();
}

function applySelection() {
  $$(".device-row", $("#device-list")).forEach((row) => {
    row.classList.toggle("selected", row.dataset.serial === state.selectedSerial);
  });
  $("#connect-btn").disabled = !state.selectedSerial;
}

async function connectDevice() {
  if (!state.selectedSerial) {
    return;
  }

  const serial = state.selectedSerial;
  $("#connect-btn").disabled = true;
  setConnectionMessage(`Connecting to ${serial}...`);
  setStatus("connecting", "Connecting...");

  try {
    const info = await invoke("connect_device", { serial });
    state.device = { ...info };
    renderDeviceInfo();
    await invoke("start_monitoring");
    $("#connection-screen").classList.add("hidden");
    $("#app-screen").classList.remove("hidden");
    setView("overview");
    setStatus("connected", `${deviceName()} - Connected`);
    setConnectionMessage("");
  } catch (error) {
    $("#connect-btn").disabled = false;
    setConnectionMessage(String(error));
    setStatus("error", "Connection error");
  }
}

function deviceName() {
  const parts = [state.device.manufacturer, state.device.model].filter(
    (value) => value && value !== "Unknown"
  );
  return parts.length > 0 ? parts.join(" ") : "Unknown device";
}

function renderDeviceInfo() {
  $("#ov-device-name").textContent = deviceName();

  const android = state.device.android_version;
  const sdk = state.device.sdk_level;
  if (android || sdk) {
    $("#ov-android").textContent = `Android ${android || "--"} (SDK ${sdk || "--"})`;
  } else {
    $("#ov-android").textContent = "";
  }

  const details = {
    serial: state.device.serial,
    build: state.device.build_number,
    security_patch: state.device.security_patch,
    cpu_arch: state.device.cpu_arch,
    uptime: state.device.uptime,
  };

  for (const [key, value] of Object.entries(details)) {
    setDetail($("#ov-details"), key, value);
  }
}

function setupSearch() {
  $("#apps-search").addEventListener("input", renderApps);
  $("#apps-refresh").addEventListener("click", () => loadApps(true));
  $("#events-search").addEventListener("input", scheduleEventsRender);
  $("#events-category").addEventListener("change", scheduleEventsRender);
}

async function loadApps(force = false) {
  if (state.appsLoading || (!force && state.appsLoaded)) {
    if (state.appsLoaded) {
      renderApps();
    }
    return;
  }

  state.appsLoading = true;
  $("#apps-count").textContent = "Loading...";

  try {
    state.apps = await invoke("get_apps");
    state.appsLoaded = true;
    $("#apps-count").textContent = `${state.apps.length} apps`;
    renderApps();
  } catch (error) {
    state.apps = [];
    state.appsLoaded = false;
    $("#apps-count").textContent = "Failed to load apps";
    $("#apps-list").innerHTML = `<div class="empty-list">${escapeHtml(String(error))}</div>`;
  } finally {
    state.appsLoading = false;
  }
}

function renderApps() {
  const list = $("#apps-list");
  const query = $("#apps-search").value.trim().toLowerCase();
  const filtered = query
    ? state.apps.filter(
        (app) =>
          app.package.toLowerCase().includes(query) || app.label.toLowerCase().includes(query)
      )
    : state.apps;

  if (filtered.length === 0) {
    list.innerHTML = `<div class="empty-list">No applications found</div>`;
    return;
  }

  list.innerHTML = filtered
    .map(
      (app) => `
        <div class="list-item">
          <div>
            <div class="title">${escapeHtml(app.label)}</div>
            <div class="sub">${escapeHtml(app.package)}</div>
          </div>
        </div>
      `
    )
    .join("");
}

function renderSensors() {
  const sensors = [
    ["Accelerometer", "TYPE_ACCELEROMETER"],
    ["Gyroscope", "TYPE_GYROSCOPE"],
    ["Magnetometer", "TYPE_MAGNETIC_FIELD"],
    ["Light", "TYPE_LIGHT"],
    ["Proximity", "TYPE_PROXIMITY"],
    ["Pressure", "TYPE_PRESSURE"],
    ["Temperature", "TYPE_AMBIENT_TEMPERATURE"],
    ["Humidity", "TYPE_RELATIVE_HUMIDITY"],
  ];

  $("#sensors-grid").innerHTML = sensors
    .map(
      ([name, type]) => `
        <div class="sensor-card">
          <div class="sensor-name">${escapeHtml(name)}</div>
          <div class="sensor-type">${escapeHtml(type)}</div>
          <div class="sensor-values">--</div>
        </div>
      `
    )
    .join("");
}

function renderSessions() {
  const sessions = [
    { id: 1, start: "2026-08-10 14:30", duration: "1h 23m" },
    { id: 2, start: "2026-08-09 10:15", duration: "45m" },
    { id: 3, start: "2026-08-08 16:00", duration: "2h 10m" },
  ];

  $("#sessions-count").textContent = `${sessions.length} sessions`;
  $("#sessions-list").innerHTML = sessions
    .map(
      (session) => `
        <div class="list-item">
          <div>
            <div class="title">Session #${session.id}</div>
            <div class="sub">Started: ${escapeHtml(session.start)}</div>
            <div class="sub">Duration: ${escapeHtml(session.duration)}</div>
          </div>
        </div>
      `
    )
    .join("");
}

let eventsFrame = null;

function scheduleEventsRender() {
  if (eventsFrame) {
    return;
  }
  eventsFrame = requestAnimationFrame(() => {
    eventsFrame = null;
    renderEvents();
  });
}

function renderEvents() {
  const list = $("#events-list");
  const query = $("#events-search").value.trim().toLowerCase();
  const category = $("#events-category").value.toLowerCase();

  $("#events-count").textContent = `${state.events.length} events`;

  const filtered = state.events.filter((event) => {
    if (category !== "all categories" && event.category !== category) {
      return false;
    }
    if (!query) {
      return true;
    }
    return (
      event.source.toLowerCase().includes(query) ||
      event.metric.toLowerCase().includes(query) ||
      formatValue(event.value).toLowerCase().includes(query)
    );
  });

  if (filtered.length === 0) {
    list.innerHTML = `<div class="empty-list">No events yet</div>`;
    return;
  }

  list.innerHTML = filtered
    .map((event) => {
      const severityClass = ["info", "warning", "critical"].includes(event.severity)
        ? event.severity
        : "";
      return `
        <div class="event-item">
          <span class="event-dot ${severityClass}">●</span>
          <div>
            <div class="event-time">${escapeHtml(event.timestamp || "--")}</div>
            <div class="event-message">${escapeHtml(
              `${event.source}.${event.metric} = ${formatValue(event.value)}`
            )}</div>
            <div class="event-category">${escapeHtml(event.category.toUpperCase())}</div>
          </div>
        </div>
      `;
    })
    .join("");
}

function renderBluetoothDevices(devices) {
  const list = $("#bt-list");
  const count = Array.isArray(devices) ? devices.length : 0;
  $("#bt-count").textContent = `${count} devices`;

  if (count === 0) {
    list.innerHTML = `<div class="empty-list">No paired devices</div>`;
    return;
  }

  list.innerHTML = devices
    .map((device) => {
      const connected = Boolean(device.connected);
      const paired = Boolean(device.paired);
      const status = connected ? "Connected" : paired ? "Paired" : "Available";
      return `
        <div class="list-item">
          <span class="dot ${connected ? "online" : ""}">${connected ? "●" : "○"}</span>
          <div>
            <div class="title">${escapeHtml(device.name || "Unknown Device")}</div>
            <div class="sub">${escapeHtml(device.address || "")}</div>
            <div class="sub">${status}</div>
          </div>
        </div>
      `;
    })
    .join("");
}

function updateHealth(score) {
  const element = $("#net-health-score");
  element.textContent = String(score);
  element.classList.remove("good", "fair", "bad");

  let status = "Critical";
  if (score >= 90) {
    status = "Excellent";
  } else if (score >= 75) {
    status = "Good";
  } else if (score >= 50) {
    status = "Fair";
  } else if (score >= 25) {
    status = "Poor";
  }

  if (score >= 75) {
    element.classList.add("good");
  } else if (score >= 25) {
    element.classList.add("fair");
  } else {
    element.classList.add("bad");
  }

  $("#net-health-status").textContent = status;
}

function updateBatteryMetric(metric, value) {
  if (metric === "level") {
    state.batteryLevel = value;
    $("#bat-level").textContent = `${value}%`;
    $("#ov-battery").textContent = `${value}%`;

    const progress = $("#battery-progress");
    const color = value < 20 ? "red" : value < 50 ? "yellow" : "green";
    progress.className = `progress-fill ${color}`;
    progress.style.width = `${Math.max(0, Math.min(100, value))}%`;
    $("#battery-progress-label").textContent = `${value}%`;
  } else if (metric === "temperature") {
    $("#bat-temp").textContent = `${formatNumber(value)}°C`;
  } else if (metric === "voltage") {
    $("#bat-voltage").textContent = `${formatNumber(value)} V`;
  } else if (metric === "status") {
    $("#bat-status").textContent = value;
  } else if (["health", "technology", "plugged"].includes(metric)) {
    setDetail($("#battery-details"), metric, value);
  }
}

function updatePerformance(metric, value) {
  const ramBar = $("#perf-ram-bar");
  const storageBar = $("#perf-storage-bar");

  if (metric === "ram_used") {
    state.ramUsed = value;
    $("#perf-ram").textContent = `${value} MB`;
    if (state.ramTotal > 0) {
      const percent = Math.round((state.ramUsed / state.ramTotal) * 100);
      ramBar.style.width = `${Math.max(0, Math.min(100, percent))}%`;
      $("#ov-ram").textContent = `${percent}%`;
    }
    state.charts.ram.push("ram", value);
  } else if (metric === "ram_total") {
    state.ramTotal = value;
    if (state.ramTotal > 0) {
      const percent = Math.round((state.ramUsed / state.ramTotal) * 100);
      ramBar.style.width = `${Math.max(0, Math.min(100, percent))}%`;
      $("#ov-ram").textContent = `${percent}%`;
    }
  } else if (metric === "storage_used") {
    state.storageUsed = value;
    $("#perf-storage").textContent = `${formatNumber(value / 1024)} GB`;
    const total = state.storageTotal > 0 ? state.storageTotal : 256 * 1024;
    const percent = Math.round((state.storageUsed / total) * 100);
    storageBar.style.width = `${Math.max(0, Math.min(100, percent))}%`;
    $("#ov-storage").textContent = `${percent}%`;
    updateStorageView();
  } else if (metric === "storage_total") {
    state.storageTotal = value;
    if (state.storageUsed > 0) {
      const percent = Math.round((state.storageUsed / state.storageTotal) * 100);
      storageBar.style.width = `${Math.max(0, Math.min(100, percent))}%`;
      $("#ov-storage").textContent = `${percent}%`;
    }
    updateStorageView();
  } else if (metric === "cpu_usage") {
    $("#perf-cpu").textContent = `${formatNumber(value)}%`;
    $("#ov-cpu").textContent = `${formatNumber(value)}%`;
    $("#perf-cpu-bar").style.width = `${Math.max(0, Math.min(100, value))}%`;
    state.charts.cpu.push("cpu", value);
  }
}

function updateStorageView() {
  if (state.storageUsed > 0) {
    $("#storage-used").textContent = `${formatNumber(state.storageUsed / 1024)} GB`;
  }
  if (state.storageTotal > 0) {
    $("#storage-total").textContent = `${formatNumber(state.storageTotal / 1024)} GB`;
  }
  if (state.storageTotal > 0) {
    const percent = Math.round((state.storageUsed / state.storageTotal) * 100);
    $("#storage-progress").style.width = `${Math.max(0, Math.min(100, percent))}%`;
    $("#storage-progress-label").textContent = `${percent}%`;
  }
}

function updateNetworkMetric(metric, value) {
  if (metric === "health") {
    updateHealth(value);
  } else if (metric === "latency") {
    $("#net-latency").textContent = `${formatNumber(value)} ms`;
    state.charts.latency.push("latency", value);
  } else if (metric === "packet_loss") {
    $("#net-loss").textContent = `${formatNumber(value)}%`;
  } else if (metric === "rx_rate") {
    $("#net-rx").textContent = `${formatNumber(value)} KB/s`;
    state.charts.throughput.push("rx", value);
  } else if (metric === "tx_rate") {
    $("#net-tx").textContent = `${formatNumber(value)} KB/s`;
    state.charts.throughput.push("tx", value);
  }
}

function updateWifiMetric(metric, value) {
  if (metric === "connected") {
    const status = $("#wifi-status");
    status.textContent = value ? "● Connected" : "● Disconnected";
    status.classList.toggle("success", Boolean(value));
  } else if (metric === "ssid") {
    $("#wifi-ssid").textContent = value;
  } else if (metric === "rssi") {
    $("#wifi-rssi").textContent = `${value} dBm`;
    state.charts.wifiSignal.push("rssi", value);
  } else if (metric === "link_speed") {
    $("#wifi-speed").textContent = `${value} Mbps`;
    state.charts.wifiSpeed.push("speed", value);
  } else if (["bssid", "frequency", "channel", "ip_address"].includes(metric)) {
    setDetail($("#wifi-details"), metric, value);
  }
}

function updateCellularMetric(metric, value) {
  if (metric === "network_type") {
    $("#cell-network-type").textContent = value;
  } else if (metric === "operator") {
    $("#cell-operator").textContent = value;
  } else if (metric === "rsrp") {
    $("#cell-rsrp").textContent = `${value} dBm`;
    state.charts.cellular.push("rsrp", value);
  } else if (metric === "rsrq") {
    $("#cell-rsrq").textContent = `${value} dB`;
    state.charts.cellular.push("rsrq", value);
  } else if (metric === "rssi") {
    $("#cell-rssi").textContent = `${value} dBm`;
  } else if (metric === "sinr") {
    $("#cell-sinr").textContent = `${value} dB`;
  } else if (["mcc_mnc", "state", "data_state", "roaming"].includes(metric)) {
    setDetail($("#cell-details"), metric, value);
  } else if (["cell_id", "tac", "pci", "band"].includes(metric)) {
    setDetail($("#cell-serving"), metric, value);
  }
}

function updateBluetoothMetric(metric, value) {
  if (metric === "enabled") {
    const status = $("#bt-status");
    status.textContent = value ? "● Enabled" : "● Disabled";
    status.classList.toggle("success", Boolean(value));
  } else if (metric === "devices") {
    renderBluetoothDevices(value);
  } else if (["adapter_address", "adapter_name", "adapter_state"].includes(metric)) {
    setDetail($("#bt-details"), metric, value);
  }
}

function handleMetric(event) {
  state.events.unshift(event);
  if (state.events.length > state.maxEvents) {
    state.events.pop();
  }
  scheduleEventsRender();

  const { category, source, metric, value } = event;

  if (category === "device") {
    if (metric === "build") {
      state.device.build_number = value;
    } else {
      state.device[metric] = value;
    }
    renderDeviceInfo();
    return;
  }

  if (category === "battery") {
    updateBatteryMetric(metric, value);
    return;
  }

  if (category === "performance") {
    updatePerformance(metric, value);
    return;
  }

  if (category === "network") {
    if (source === "network") {
      updateNetworkMetric(metric, value);
    } else if (source === "wifi") {
      updateWifiMetric(metric, value);
    } else if (source === "cellular") {
      updateCellularMetric(metric, value);
    } else if (source === "bluetooth") {
      updateBluetoothMetric(metric, value);
    }
  }
}

async function listenMetrics() {
  if (!window.__TAURI__ || !window.__TAURI__.event) {
    return;
  }
  await window.__TAURI__.event.listen("metric", (event) => {
    if (event.payload) {
      handleMetric(event.payload);
    }
  });
}

document.addEventListener("DOMContentLoaded", () => {
  injectIcons();
  setupNavigation();
  setupConnection();
  setupSearch();
  setupCharts();
  renderSensors();
  renderSessions();
  renderEvents();
  listenMetrics().catch((error) => console.error(error));
  refreshDevices();
});

window.addEventListener("resize", () => {
  renderAllCharts();
});
