use crate::adb::AdbClient;
use crate::models::MetricEvent;

use super::{event, parse_number_after};

#[derive(Default)]
struct CellularInfo {
    network_type: String,
    operator: String,
    mcc_mnc: String,
    state: String,
    data_state: String,
    roaming: String,
    rsrp: i32,
    rsrq: i32,
    rssi: i32,
    sinr: i32,
    cell_id: String,
    tac: String,
    pci: String,
    band: String,
}

pub fn collect(adb: &AdbClient) -> Vec<MetricEvent> {
    if adb.serial().is_none() {
        return Vec::new();
    }

    let info = cellular_info(adb);

    vec![
        event("network", "cellular", "network_type", info.network_type),
        event("network", "cellular", "operator", info.operator),
        event("network", "cellular", "mcc_mnc", info.mcc_mnc),
        event("network", "cellular", "state", info.state),
        event("network", "cellular", "data_state", info.data_state),
        event("network", "cellular", "roaming", info.roaming),
        event("network", "cellular", "rsrp", info.rsrp),
        event("network", "cellular", "rsrq", info.rsrq),
        event("network", "cellular", "rssi", info.rssi),
        event("network", "cellular", "sinr", info.sinr),
        event("network", "cellular", "cell_id", info.cell_id),
        event("network", "cellular", "tac", info.tac),
        event("network", "cellular", "pci", info.pci),
        event("network", "cellular", "band", info.band),
    ]
}

fn cellular_info(adb: &AdbClient) -> CellularInfo {
    let mut info = CellularInfo {
        network_type: "--".to_string(),
        operator: "--".to_string(),
        mcc_mnc: "--".to_string(),
        state: "--".to_string(),
        data_state: "--".to_string(),
        roaming: "No".to_string(),
        cell_id: "--".to_string(),
        tac: "--".to_string(),
        pci: "--".to_string(),
        band: "--".to_string(),
        ..CellularInfo::default()
    };

    let Ok(output) = adb.execute("dumpsys telephony.registry") else {
        return info;
    };

    for line in output.lines() {
        let line = line.trim();
        let upper = line.to_uppercase();

        if line.contains("mDataConnectionNetworkType")
            || line.contains("VoiceNetworkType")
            || line.contains("mDataNetworkType")
        {
            if upper.contains("LTE") {
                info.network_type = "LTE".to_string();
            } else if upper.contains("NR") || upper.contains("5G") {
                info.network_type = "5G".to_string();
            } else if upper.contains("UMTS") || upper.contains("HSPA") || upper.contains("3G") {
                info.network_type = "3G".to_string();
            } else if upper.contains("EDGE") || upper.contains("GPRS") || upper.contains("GSM") {
                info.network_type = "2G".to_string();
            } else if let Some(value) = line.split('=').next_back() {
                let detected = match value.trim() {
                    "13" => Some("LTE"),
                    "20" => Some("5G"),
                    "3" => Some("3G"),
                    "2" => Some("2G"),
                    _ => None,
                };
                if let Some(detected) = detected {
                    info.network_type = detected.to_string();
                }
            }
        }

        if line.contains("mOperatorAlphaLong=") {
            if let Some(value) = line.split("mOperatorAlphaLong=").nth(1) {
                info.operator = value.split(',').next().unwrap_or(value).trim().to_string();
            }
        }

        if line.contains("mccMnc") {
            if let Some(value) = line.split('=').next_back() {
                let value = value.trim();
                if !value.is_empty() {
                    info.mcc_mnc = value.trim_end_matches(',').to_string();
                }
            }
        }

        if line.contains("mVoiceRegState") {
            if let Some(value) = line.split('=').nth(1) {
                info.state = match value.trim().trim_end_matches(',').trim() {
                    "0" => "In service",
                    "1" => "Out of service",
                    "2" => "Emergency only",
                    _ => "Unknown",
                }
                .to_string();
            }
        }

        if line.contains("mDataConnectionState") {
            if let Some(value) = line.split('=').nth(1) {
                info.data_state = match value.trim().trim_end_matches(',').trim() {
                    "0" => "Disconnected",
                    "1" => "Connecting",
                    "2" => "Connected",
                    _ => "Suspended",
                }
                .to_string();
            }
        }

        if line.contains("mIsDataRoaming") && line.contains("true") {
            info.roaming = "Yes".to_string();
        }

        if line.contains("mSignalStrength") || line.contains("SignalStrength") {
            if let Some(value) =
                parse_number_after(line, "rsrp=").or_else(|| parse_number_after(line, "RSRP:"))
            {
                info.rsrp = value as i32;
            }
            if let Some(value) =
                parse_number_after(line, "rsrq=").or_else(|| parse_number_after(line, "RSRQ:"))
            {
                info.rsrq = value as i32;
            }
            if let Some(value) =
                parse_number_after(line, "rssi=").or_else(|| parse_number_after(line, "RSSI:"))
            {
                info.rssi = value as i32;
            }
            if let Some(value) =
                parse_number_after(line, "sinr=").or_else(|| parse_number_after(line, "SINR:"))
            {
                info.sinr = value as i32;
            }
        }

        if let Some(value) = value_after(line, "mCi=").or_else(|| value_after(line, "Ci=")) {
            info.cell_id = value;
        }
        if let Some(value) = value_after(line, "mTac=").or_else(|| value_after(line, "Tac=")) {
            info.tac = value;
        }
        if let Some(value) = value_after(line, "mPci=").or_else(|| value_after(line, "Pci=")) {
            info.pci = value;
        }
        if let Some(value) = value_after(line, "mBand=").or_else(|| value_after(line, "band=")) {
            info.band = value;
        }
    }

    info
}

fn value_after(line: &str, key: &str) -> Option<String> {
    let start = line.find(key)? + key.len();
    let rest = line[start..].trim_start();
    let token = rest.split([',', ' ', '}']).next()?.trim();
    if token.is_empty() {
        None
    } else {
        Some(token.to_string())
    }
}
