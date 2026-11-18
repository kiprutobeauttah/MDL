use crate::adb::AdbClient;
use crate::models::MetricEvent;

use super::event;

#[derive(Default)]
struct WifiInfo {
    connected: bool,
    ssid: String,
    bssid: String,
    rssi: i32,
    link_speed: i32,
    frequency: String,
    channel: String,
    ip_address: String,
}

pub fn collect(adb: &AdbClient) -> Vec<MetricEvent> {
    if adb.serial().is_none() {
        return Vec::new();
    }

    let info = wifi_info(adb);
    let mut events = vec![event("network", "wifi", "connected", info.connected)];

    if info.connected {
        events.push(event("network", "wifi", "ssid", info.ssid));
        events.push(event("network", "wifi", "bssid", info.bssid));
        events.push(event("network", "wifi", "rssi", info.rssi));
        events.push(event("network", "wifi", "link_speed", info.link_speed));
        events.push(event("network", "wifi", "frequency", info.frequency));
        events.push(event("network", "wifi", "channel", info.channel));
        events.push(event("network", "wifi", "ip_address", info.ip_address));
    }

    events
}

fn wifi_info(adb: &AdbClient) -> WifiInfo {
    let mut info = WifiInfo {
        ssid: "--".to_string(),
        bssid: "--".to_string(),
        frequency: "--".to_string(),
        channel: "--".to_string(),
        ip_address: "--".to_string(),
        ..WifiInfo::default()
    };

    let output = adb
        .execute("dumpsys wifi | grep -A 20 mWifiInfo")
        .unwrap_or_default();

    if output.is_empty() {
        return info;
    }

    for line in output.lines() {
        if let Some(value) = field(line, "SSID:") {
            let ssid = value.trim().replace('"', "");
            if !ssid.is_empty() && !ssid.eq_ignore_ascii_case("<unknown ssid>") {
                info.ssid = ssid;
                info.connected = true;
            }
        }

        if let Some(value) = field(line, "BSSID:") {
            if !value.is_empty() && value != "<none>" {
                info.bssid = value.to_string();
            }
        }

        if let Some(value) = field(line, "RSSI:").or_else(|| field(line, "rssi:")) {
            if let Some(token) = value.split_whitespace().next() {
                info.rssi = token.parse().unwrap_or(info.rssi);
            }
        }

        if let Some(value) = field(line, "Link speed:").or_else(|| field(line, "link_speed:")) {
            let speed = value.replace("Mbps", "").replace("mbps", "");
            info.link_speed = speed.trim().parse().unwrap_or(info.link_speed);
        }

        if let Some(value) = field(line, "Frequency:").or_else(|| field(line, "frequency:")) {
            info.frequency = value.to_string();
            let frequency = value.replace("MHz", "").replace("mhz", "");
            if let Ok(frequency) = frequency.trim().parse::<i32>() {
                let channel = if (2400..=2500).contains(&frequency) {
                    (frequency - 2407) / 5
                } else if (5000..=6000).contains(&frequency) {
                    (frequency - 5000) / 5
                } else {
                    0
                };
                info.channel = channel.to_string();
            }
        }
    }

    if let Ok(output) = adb.execute("ip addr show wlan0 | grep inet") {
        if let Some(line) = output.lines().find(|line| line.contains("inet ")) {
            let parts: Vec<&str> = line.split_whitespace().collect();
            if let Some(address) = parts.get(1) {
                info.ip_address = address.split('/').next().unwrap_or("--").to_string();
            }
        }
    }

    info
}

fn field<'a>(line: &'a str, key: &str) -> Option<&'a str> {
    let mut search_from = 0;

    while let Some(relative) = line[search_from..].find(key) {
        let index = search_from + relative;

        if key.eq_ignore_ascii_case("SSID:") && index > 0 {
            let previous = line.as_bytes()[index - 1];
            if previous.eq_ignore_ascii_case(&b'B') {
                search_from = index + key.len();
                continue;
            }
        }

        let rest = &line[index + key.len()..];
        let value = rest.split(',').next().unwrap_or(rest).trim();
        return Some(value);
    }

    None
}
