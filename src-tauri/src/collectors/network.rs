use std::time::Instant;

use crate::adb::AdbClient;
use crate::models::MetricEvent;

use super::event;

#[derive(Default)]
pub struct NetworkState {
    last_rx_bytes: u64,
    last_tx_bytes: u64,
    last_time: Option<Instant>,
}

pub fn collect(adb: &AdbClient, state: &mut NetworkState) -> Vec<MetricEvent> {
    if adb.serial().is_none() {
        return Vec::new();
    }

    let (connected, connection_type) = connectivity(adb);
    let (rx_bytes, tx_bytes) = network_bytes(adb);

    let now = Instant::now();
    let (rx_rate, tx_rate) = match state.last_time {
        Some(last_time) if state.last_rx_bytes > 0 => {
            let elapsed = now.duration_since(last_time).as_secs_f64();
            if elapsed > 0.0 {
                (
                    (rx_bytes.saturating_sub(state.last_rx_bytes)) as f64 / elapsed,
                    (tx_bytes.saturating_sub(state.last_tx_bytes)) as f64 / elapsed,
                )
            } else {
                (0.0, 0.0)
            }
        }
        _ => (0.0, 0.0),
    };

    state.last_rx_bytes = rx_bytes;
    state.last_tx_bytes = tx_bytes;
    state.last_time = Some(now);

    let (latency, packet_loss) = ping_test(adb);

    let health = calculate_health(connected, connection_type.as_str(), latency, packet_loss);

    vec![
        event("network", "network", "connected", connected),
        event("network", "network", "type", connection_type),
        event("network", "network", "latency", latency),
        event("network", "network", "packet_loss", packet_loss),
        event("network", "network", "rx_rate", rx_rate / 1024.0),
        event("network", "network", "tx_rate", tx_rate / 1024.0),
        event("network", "network", "health", health),
    ]
}

fn connectivity(adb: &AdbClient) -> (bool, String) {
    let Ok(output) = adb.execute("dumpsys connectivity | grep NetworkAgentInfo") else {
        return (false, "None".to_string());
    };

    let connected = output.contains("CONNECTED");
    let upper = output.to_uppercase();

    let connection_type = if upper.contains("WIFI") {
        "Wi-Fi"
    } else if upper.contains("MOBILE") || upper.contains("CELLULAR") {
        "Cellular"
    } else {
        "Unknown"
    };

    (connected, connection_type.to_string())
}

fn network_bytes(adb: &AdbClient) -> (u64, u64) {
    for interface in ["wlan0", "rmnet0"] {
        let rx = adb
            .execute(&format!(
                "cat /sys/class/net/{interface}/statistics/rx_bytes"
            ))
            .ok()
            .and_then(|value| value.trim().parse::<u64>().ok());
        let tx = adb
            .execute(&format!(
                "cat /sys/class/net/{interface}/statistics/tx_bytes"
            ))
            .ok()
            .and_then(|value| value.trim().parse::<u64>().ok());

        if let (Some(rx), Some(tx)) = (rx, tx) {
            return (rx, tx);
        }
    }

    (0, 0)
}

fn ping_test(adb: &AdbClient) -> (f64, f64) {
    let Ok(output) = adb.execute("ping -c 3 -W 1 8.8.8.8") else {
        return (0.0, 0.0);
    };

    let mut latency = 0.0;
    let mut packet_loss = 0.0;

    for line in output.lines() {
        if let Some(index) = line.find("packet loss") {
            let before = &line[..index];
            if let Some(loss) = before.split_whitespace().last() {
                packet_loss = loss.trim_end_matches('%').parse().unwrap_or(0.0);
            }
        }

        if line.contains("rtt min/avg/max") || line.contains("round-trip") {
            if let Some((_, values)) = line.split_once('=') {
                let values: Vec<&str> = values.trim().split('/').collect();
                if values.len() >= 2 {
                    latency = values[1].trim().parse().unwrap_or(0.0);
                }
            }
        }
    }

    (latency, packet_loss)
}

fn calculate_health(connected: bool, connection_type: &str, latency: f64, packet_loss: f64) -> i32 {
    if !connected {
        return 0;
    }

    let mut score = 100;

    if latency > 100.0 {
        score -= 40;
    } else if latency > 50.0 {
        score -= 20;
    } else if latency > 30.0 {
        score -= 10;
    }

    if packet_loss > 5.0 {
        score -= 40;
    } else if packet_loss > 2.0 {
        score -= 20;
    } else if packet_loss > 0.5 {
        score -= 10;
    }

    if connection_type == "Unknown" {
        score -= 20;
    }

    score.clamp(0, 100)
}
