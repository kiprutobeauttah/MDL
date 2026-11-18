use std::collections::HashMap;

use crate::adb::AdbClient;
use crate::models::{DeviceInfo, MetricEvent};

use super::event;

pub fn collect(adb: &AdbClient) -> Result<DeviceInfo, String> {
    let serial = adb
        .serial()
        .ok_or_else(|| "No device connected".to_string())?;

    let properties = adb
        .execute("getprop")
        .map(|output| parse_getprop(&output))
        .unwrap_or_default();

    let get = |name: &str| {
        properties
            .get(name)
            .filter(|value| !value.is_empty())
            .cloned()
            .unwrap_or_else(|| "Unknown".to_string())
    };

    let uptime = adb
        .execute("cat /proc/uptime")
        .ok()
        .and_then(|output| format_uptime(&output))
        .unwrap_or_else(|| "Unknown".to_string());

    Ok(DeviceInfo {
        serial,
        manufacturer: get("ro.product.manufacturer"),
        model: get("ro.product.model"),
        product: get("ro.product.name"),
        board: get("ro.product.board"),
        android_version: get("ro.build.version.release"),
        sdk_level: get("ro.build.version.sdk"),
        build_number: get("ro.build.display.id"),
        security_patch: get("ro.build.version.security_patch"),
        cpu_arch: get("ro.product.cpu.abi"),
        abi: get("ro.product.cpu.abilist"),
        uptime,
    })
}

pub fn events(info: &DeviceInfo) -> Vec<MetricEvent> {
    vec![
        event(
            "device",
            "device",
            "manufacturer",
            info.manufacturer.clone(),
        ),
        event("device", "device", "model", info.model.clone()),
        event(
            "device",
            "device",
            "android_version",
            info.android_version.clone(),
        ),
        event("device", "device", "sdk_level", info.sdk_level.clone()),
        event("device", "device", "serial", info.serial.clone()),
        event("device", "device", "build", info.build_number.clone()),
        event(
            "device",
            "device",
            "security_patch",
            info.security_patch.clone(),
        ),
        event("device", "device", "cpu_arch", info.cpu_arch.clone()),
        event("device", "device", "uptime", info.uptime.clone()),
    ]
}

fn parse_getprop(output: &str) -> HashMap<String, String> {
    let mut properties = HashMap::new();

    for line in output.lines() {
        let line = line.trim();
        let Some(rest) = line.strip_prefix('[') else {
            continue;
        };
        let Some((key, rest)) = rest.split_once("]: [") else {
            continue;
        };
        let Some(value) = rest.strip_suffix(']') else {
            continue;
        };
        properties.insert(key.to_string(), value.to_string());
    }

    properties
}

fn format_uptime(output: &str) -> Option<String> {
    let seconds = output.split_whitespace().next()?.parse::<f64>().ok()?;
    let total = seconds as u64;
    let days = total / 86_400;
    let hours = (total % 86_400) / 3_600;
    let minutes = (total % 3_600) / 60;

    if days > 0 {
        Some(format!("{days}d {hours}h {minutes}m"))
    } else if hours > 0 {
        Some(format!("{hours}h {minutes}m"))
    } else {
        Some(format!("{minutes}m"))
    }
}
