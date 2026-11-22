use serde::{Deserialize, Serialize};
use serde_json::Value;

#[derive(Debug, Clone, Serialize)]
pub struct DeviceEntry {
    pub serial: String,
    pub state: String,
    pub connection_type: String,
    pub model: String,
}

#[derive(Debug, Clone, Default, Serialize)]
pub struct DeviceInfo {
    pub serial: String,
    pub manufacturer: String,
    pub model: String,
    pub product: String,
    pub board: String,
    pub android_version: String,
    pub sdk_level: String,
    pub build_number: String,
    pub security_patch: String,
    pub cpu_arch: String,
    pub abi: String,
    pub uptime: String,
}

#[derive(Debug, Clone, Serialize)]
pub struct AppEntry {
    pub package: String,
    pub label: String,
}

#[derive(Debug, Clone, Serialize)]
pub struct AppPermission {
    pub name: String,
    pub granted: Option<bool>,
    pub runtime: bool,
}

#[derive(Debug, Clone, Serialize)]
pub struct AppDetails {
    pub package: String,
    pub running: bool,
    pub pids: Vec<u32>,
    pub apk_size: Option<u64>,
    pub data_size: Option<u64>,
    pub cache_size: Option<u64>,
    pub permissions: Vec<AppPermission>,
    pub services: Vec<String>,
    pub jobs: Vec<String>,
    pub alarms: Vec<String>,
}

#[derive(Debug, Clone, Serialize)]
pub struct AppLogEvent {
    pub session: u64,
    pub package: String,
    pub line: String,
}

#[derive(Debug, Clone, Serialize)]
pub struct AppLogEnd {
    pub session: u64,
    pub package: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct MetricEvent {
    pub timestamp: String,
    pub category: String,
    pub source: String,
    pub metric: String,
    pub value: Value,
    pub severity: String,
    pub message: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SessionSummary {
    pub id: String,
    pub name: String,
    pub started_at: String,
    pub ended_at: Option<String>,
    pub event_count: usize,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SessionRecord {
    pub id: String,
    pub name: String,
    pub started_at: String,
    pub ended_at: String,
    pub events: Vec<MetricEvent>,
}

#[derive(Debug, Clone, Serialize)]
pub struct ExportResult {
    pub path: String,
    pub events: usize,
}

#[derive(Debug, Clone, Serialize)]
pub struct DeviceLogEvent {
    pub session: u64,
    pub line: String,
}

#[derive(Debug, Clone, Serialize)]
pub struct DeviceLogEnd {
    pub session: u64,
}

#[derive(Debug, Clone, Serialize)]
pub struct NotificationEntry {
    pub package: String,
    pub id: String,
    pub tag: String,
    pub channel: String,
    pub importance: Option<i32>,
    pub title: Option<String>,
    pub text: Option<String>,
    pub created_at_ms: Option<u64>,
}

#[derive(Debug, Clone, Serialize)]
pub struct TaskEntry {
    pub id: String,
    pub package: String,
    pub activity: Option<String>,
    pub visible: bool,
}

#[derive(Debug, Clone, Serialize)]
pub struct ActivityState {
    pub foreground_package: Option<String>,
    pub foreground_component: Option<String>,
    pub tasks: Vec<TaskEntry>,
}

#[derive(Debug, Clone, Serialize)]
pub struct WakelockEntry {
    pub kind: String,
    pub tag: String,
    pub held: String,
    pub uid: Option<String>,
    pub pid: Option<String>,
}

#[derive(Debug, Clone, Serialize)]
pub struct PowerReport {
    pub wakefulness: String,
    pub doze_state: String,
    pub light_doze_state: String,
    pub battery_saver: bool,
    pub powered: bool,
    pub wakelocks: Vec<WakelockEntry>,
}

#[derive(Debug, Clone, Serialize)]
pub struct AppUsageEntry {
    pub package: String,
    pub cpu_percent: f64,
    pub pss_kb: u64,
}

#[derive(Debug, Clone, Serialize)]
pub struct ThermalZone {
    pub name: String,
    pub temperature_c: f64,
    pub status: Option<i32>,
}

#[derive(Debug, Clone, Serialize)]
pub struct SensorEntry {
    pub handle: String,
    pub name: String,
    pub vendor: String,
    pub type_name: String,
    pub wake_up: bool,
    pub values: Vec<f64>,
}

#[derive(Debug, Clone, Serialize)]
pub struct SensorSnapshot {
    pub thermal_status: Option<i32>,
    pub thermal_zones: Vec<ThermalZone>,
    pub sensors: Vec<SensorEntry>,
}

#[derive(Debug, Clone, Serialize)]
pub struct UsbDevice {
    pub id: String,
    pub location: String,
    pub description: String,
    pub vendor: Option<String>,
    pub product: Option<String>,
}

#[derive(Debug, Clone, Serialize)]
pub struct UsbStatus {
    pub supported: bool,
    pub platform: String,
    pub devices: Vec<UsbDevice>,
    pub mtp_roots: Vec<String>,
    pub message: String,
}

#[derive(Debug, Clone, Serialize)]
pub struct StatusInfo {
    pub serial: Option<String>,
    pub monitoring: bool,
}

#[derive(Debug, Clone, Serialize)]
pub struct ShellOutput {
    pub stdout: String,
    pub stderr: String,
    pub exit_code: i32,
}

#[derive(Debug, Clone, Serialize)]
pub struct FsEntry {
    pub name: String,
    pub path: String,
    pub is_dir: bool,
    pub is_link: bool,
    pub size: u64,
    pub modified: String,
    pub permissions: String,
    pub link_target: Option<String>,
}

#[derive(Debug, Clone, Serialize)]
pub struct DirectoryListing {
    pub path: String,
    pub entries: Vec<FsEntry>,
}

#[derive(Debug, Clone, Serialize)]
pub struct ImagePreview {
    pub mime: String,
    pub data: String,
}
