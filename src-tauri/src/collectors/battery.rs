use std::collections::HashMap;

use crate::adb::AdbClient;
use crate::models::MetricEvent;

use super::{event, event_with_severity};

pub fn collect(adb: &AdbClient) -> Vec<MetricEvent> {
    let Ok(output) = adb.execute("dumpsys battery") else {
        return Vec::new();
    };

    let data = parse_battery_dump(&output);
    let level = data
        .get("level")
        .and_then(|value| value.parse::<i32>().ok())
        .unwrap_or(0);
    let temperature = data
        .get("temperature")
        .and_then(|value| value.parse::<f64>().ok())
        .map(|value| value / 10.0)
        .unwrap_or(0.0);
    let voltage = data
        .get("voltage")
        .and_then(|value| value.parse::<f64>().ok())
        .map(|value| value / 1000.0)
        .unwrap_or(0.0);

    let status = data
        .get("status")
        .cloned()
        .unwrap_or_else(|| "Unknown".to_string());
    let health = data
        .get("health")
        .cloned()
        .unwrap_or_else(|| "Unknown".to_string());
    let technology = data
        .get("technology")
        .cloned()
        .unwrap_or_else(|| "Unknown".to_string());
    let plugged = data
        .get("plugged")
        .cloned()
        .unwrap_or_else(|| "None".to_string());

    let temperature_severity = if temperature > 40.0 {
        "warning"
    } else {
        "normal"
    };
    let level_severity = if level < 20 { "warning" } else { "normal" };

    vec![
        event_with_severity("battery", "battery", "level", level, level_severity),
        event_with_severity(
            "battery",
            "battery",
            "temperature",
            temperature,
            temperature_severity,
        ),
        event("battery", "battery", "voltage", voltage),
        event("battery", "battery", "status", status),
        event("battery", "battery", "health", health),
        event("battery", "battery", "technology", technology),
        event("battery", "battery", "plugged", plugged),
    ]
}

fn parse_battery_dump(output: &str) -> HashMap<String, String> {
    let mut data = HashMap::new();

    for line in output.lines() {
        let line = line.trim();
        let Some((key, value)) = line.split_once(':') else {
            continue;
        };
        let key = key.trim().to_lowercase().replace(' ', "_");
        let value = value.trim();

        let value = if key == "status" {
            match value {
                "1" => "Unknown",
                "2" => "Charging",
                "3" => "Discharging",
                "4" => "Not charging",
                "5" => "Full",
                other => other,
            }
        } else if key == "plugged" {
            match value {
                "0" => "None",
                "1" => "AC",
                "2" => "USB",
                "4" => "Wireless",
                other => other,
            }
        } else {
            value
        };

        data.insert(key, value.to_string());
    }

    data
}
