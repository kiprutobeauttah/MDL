use crate::adb::AdbClient;
use crate::models::MetricEvent;

use super::event;

pub fn collect(adb: &AdbClient) -> Vec<MetricEvent> {
    if adb.serial().is_none() {
        return Vec::new();
    }

    let (ram_total, ram_available) = memory_info(adb);
    let ram_used = ram_total.saturating_sub(ram_available);
    let (storage_total, storage_used) = storage_info(adb);

    vec![
        event("performance", "performance", "ram_used", ram_used),
        event("performance", "performance", "ram_total", ram_total),
        event("performance", "performance", "ram_available", ram_available),
        event("performance", "performance", "storage_used", storage_used),
        event("performance", "performance", "storage_total", storage_total),
    ]
}

fn memory_info(adb: &AdbClient) -> (u64, u64) {
    let Ok(output) = adb.execute("cat /proc/meminfo") else {
        return (0, 0);
    };

    let mut total = 0;
    let mut available = 0;

    for line in output.lines() {
        let Some((key, value)) = line.split_once(':') else {
            continue;
        };
        let Some(value) = value.split_whitespace().next() else {
            continue;
        };
        let Ok(value_kb) = value.parse::<u64>() else {
            continue;
        };

        match key.trim() {
            "MemTotal" => total = value_kb / 1024,
            "MemAvailable" => available = value_kb / 1024,
            _ => {}
        }
    }

    (total, available)
}

fn storage_info(adb: &AdbClient) -> (u64, u64) {
    let Ok(output) = adb.execute("df /data") else {
        return (0, 0);
    };

    let mut lines = output.lines();
    let _header = lines.next();

    let Some(line) = lines.next() else {
        return (0, 0);
    };

    let parts: Vec<&str> = line.split_whitespace().collect();
    if parts.len() < 4 {
        return (0, 0);
    }

    let total = parts[1].parse::<u64>().unwrap_or(0) / 1024;
    let used = parts[2].parse::<u64>().unwrap_or(0) / 1024;

    (total, used)
}
