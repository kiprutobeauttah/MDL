use serde::Serialize;
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

#[derive(Debug, Clone, Serialize)]
pub struct MetricEvent {
    pub timestamp: String,
    pub category: String,
    pub source: String,
    pub metric: String,
    pub value: Value,
    pub severity: String,
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
