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
