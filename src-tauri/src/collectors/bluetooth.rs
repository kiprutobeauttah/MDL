use serde_json::json;

use crate::adb::AdbClient;
use crate::models::MetricEvent;

use super::event;

#[derive(Default)]
struct BluetoothInfo {
    enabled: bool,
    adapter_address: String,
    adapter_name: String,
    adapter_state: String,
    devices: Vec<BondedDevice>,
}

#[derive(Default)]
struct BondedDevice {
    address: String,
    name: String,
    paired: bool,
    connected: bool,
}

pub fn collect(adb: &AdbClient) -> Vec<MetricEvent> {
    if adb.serial().is_none() {
        return Vec::new();
    }

    let info = bluetooth_info(adb);
    let devices = info
        .devices
        .iter()
        .map(|device| {
            json!({
                "address": device.address,
                "name": device.name,
                "paired": device.paired,
                "connected": device.connected,
            })
        })
        .collect::<Vec<_>>();

    vec![
        event("network", "bluetooth", "enabled", info.enabled),
        event(
            "network",
            "bluetooth",
            "adapter_address",
            info.adapter_address,
        ),
        event("network", "bluetooth", "adapter_name", info.adapter_name),
        event("network", "bluetooth", "adapter_state", info.adapter_state),
        event("network", "bluetooth", "devices", devices),
    ]
}

fn bluetooth_info(adb: &AdbClient) -> BluetoothInfo {
    let mut info = BluetoothInfo {
        adapter_address: "--".to_string(),
        adapter_name: "--".to_string(),
        adapter_state: "OFF".to_string(),
        ..BluetoothInfo::default()
    };

    let Ok(output) = adb.execute("dumpsys bluetooth_manager") else {
        return info;
    };

    for line in output.lines() {
        let line = line.trim();

        if let Some((key, value)) = line.split_once(':') {
            let key = key.trim().to_lowercase();
            let value = value.trim();

            if key == "enabled" {
                info.enabled = value.eq_ignore_ascii_case("true");
                info.adapter_state = if info.enabled { "ON" } else { "OFF" }.to_string();
            } else if key == "state" {
                let value = value.to_lowercase();
                if value == "on" || value == "turning_on" {
                    info.enabled = true;
                    info.adapter_state = "ON".to_string();
                } else if value == "off" || value == "turning_off" {
                    info.enabled = false;
                    info.adapter_state = "OFF".to_string();
                }
            } else if key == "address" && value.len() == 17 {
                info.adapter_address = value.to_string();
            } else if key == "name" && !value.is_empty() && value.len() < 50 {
                info.adapter_name = value.to_string();
            }
        }
    }

    if let Ok(output) = adb.execute("dumpsys bluetooth_manager | grep -A 5 Bonded") {
        info.devices = parse_bonded_devices(&output);
    }

    info
}

fn parse_bonded_devices(output: &str) -> Vec<BondedDevice> {
    let mut devices = Vec::new();
    let mut current: Option<BondedDevice> = None;

    for line in output.lines() {
        let line = line.trim();
        let lower = line.to_lowercase();

        let address = line.split_whitespace().next().unwrap_or(line);
        if address.matches(':').count() >= 5 {
            if let Some(device) = current.take() {
                devices.push(device);
            }
            current = Some(BondedDevice {
                address: address.trim_end_matches(',').to_string(),
                name: "Unknown Device".to_string(),
                paired: true,
                connected: false,
            });
        } else if lower.contains("name:") {
            if let Some(device) = current.as_mut() {
                if let Some(value) = line.split_once(':').map(|(_, value)| value.trim()) {
                    if !value.is_empty() {
                        device.name = value.to_string();
                    }
                }
            }
        } else if lower.contains("connected") && lower.contains("true") {
            if let Some(device) = current.as_mut() {
                device.connected = true;
            }
        }
    }

    if let Some(device) = current {
        devices.push(device);
    }

    devices
}
