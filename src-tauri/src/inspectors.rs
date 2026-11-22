use std::collections::HashMap;

use crate::adb::AdbClient;
use crate::models::{
    ActivityState, AppUsageEntry, NotificationEntry, PowerReport, SensorEntry, SensorSnapshot,
    TaskEntry, ThermalZone, WakelockEntry,
};

pub fn notifications(adb: &AdbClient) -> Result<Vec<NotificationEntry>, String> {
    let output = adb.execute("dumpsys notification --noredact")?;
    Ok(parse_notifications(&output))
}

pub fn activity(adb: &AdbClient) -> Result<ActivityState, String> {
    let output = adb.execute("dumpsys activity activities")?;
    let mut foreground = parse_foreground(&output);

    if foreground.is_none() {
        if let Ok(window) = adb.execute("dumpsys window") {
            foreground = parse_foreground(&window);
        }
    }

    let foreground_package = foreground
        .as_ref()
        .and_then(|component| component.split('/').next())
        .filter(|value| !value.is_empty())
        .map(str::to_string);

    Ok(ActivityState {
        foreground_package,
        foreground_component: foreground,
        tasks: parse_tasks(&output),
    })
}

pub fn power(adb: &AdbClient) -> Result<PowerReport, String> {
    let output = adb.execute("dumpsys power")?;
    let idle = adb.execute("dumpsys deviceidle").unwrap_or_default();
    Ok(parse_power(&output, &idle))
}

pub fn app_usage(adb: &AdbClient) -> Result<Vec<AppUsageEntry>, String> {
    let cpu = adb.execute("dumpsys cpuinfo").unwrap_or_default();
    let memory = adb.execute("dumpsys meminfo").unwrap_or_default();
    Ok(parse_app_usage(&cpu, &memory))
}

pub fn sensors(adb: &AdbClient) -> Result<SensorSnapshot, String> {
    let thermal = adb.execute("dumpsys thermalservice").unwrap_or_default();
    let sensors = adb.execute("dumpsys sensorservice")?;
    Ok(SensorSnapshot {
        thermal_status: parse_thermal_status(&thermal),
        thermal_zones: parse_thermal_zones(&thermal),
        sensors: parse_sensors(&sensors),
    })
}

fn parse_notifications(output: &str) -> Vec<NotificationEntry> {
    let mut entries = Vec::new();
    let mut current: Option<NotificationEntry> = None;

    for line in output.lines() {
        if line.contains("NotificationRecord(") {
            if let Some(entry) = current.take() {
                entries.push(entry);
            }
            let tag = field_value(line, "tag=").unwrap_or_default();
            current = Some(NotificationEntry {
                package: field_value(line, "pkg=").unwrap_or_default(),
                id: field_value(line, "id=").unwrap_or_default(),
                tag: if tag == "null" { String::new() } else { tag },
                channel: field_value(line, "channel=").unwrap_or_default(),
                importance: field_value(line, "importance=").and_then(|value| value.parse().ok()),
                title: None,
                text: None,
                created_at_ms: None,
            });
            continue;
        }

        let Some(entry) = current.as_mut() else {
            continue;
        };
        let trimmed = line.trim();

        if entry.title.is_none() {
            if let Some(value) = notification_string(trimmed, "android.title=") {
                entry.title = Some(value);
            }
        }
        if entry.text.is_none() {
            if let Some(value) = notification_string(trimmed, "android.text=") {
                entry.text = Some(value);
            }
        }
        if entry.text.is_none() {
            if let Some(value) = notification_string(trimmed, "android.bigText=") {
                entry.text = Some(value);
            }
        }
        if entry.created_at_ms.is_none() {
            entry.created_at_ms = field_value(trimmed, "mCreationTimeMs=")
                .or_else(|| field_value(trimmed, "mUpdateTimeMs="))
                .and_then(|value| value.parse().ok());
        }
    }

    if let Some(entry) = current {
        entries.push(entry);
    }

    entries.retain(|entry| !entry.package.is_empty() && entry.tag != "ranker_group");
    entries
}

fn notification_string(line: &str, key: &str) -> Option<String> {
    let rest = line.strip_prefix(key)?.trim();
    let value = match rest.split_once(' ') {
        Some((_, value)) => value.trim(),
        None => rest,
    };
    let value = value.strip_prefix('(').unwrap_or(value);
    let value = value.strip_suffix(')').unwrap_or(value);
    if value.is_empty() || value == "null" {
        None
    } else {
        Some(value.to_string())
    }
}

fn parse_foreground(output: &str) -> Option<String> {
    for line in output.lines() {
        let trimmed = line.trim();
        if trimmed.starts_with("ResumedActivity:")
            || trimmed.starts_with("mResumedActivity:")
            || trimmed.starts_with("topResumedActivity=")
            || trimmed.starts_with("mTopResumedActivity=")
            || trimmed.starts_with("mFocusedApp=")
            || trimmed.starts_with("mCurrentFocus=")
        {
            if let Some(component) = activity_component(trimmed) {
                return Some(component);
            }
        }
    }
    None
}

fn activity_component(line: &str) -> Option<String> {
    let start = line.find('{')?;
    let end = line.rfind('}')?;
    if end <= start {
        return None;
    }
    line[start + 1..end]
        .split_whitespace()
        .find(|token| token.contains('/') && token.contains('.'))
        .map(|token| token.trim_end_matches('}').to_string())
}

fn parse_tasks(output: &str) -> Vec<TaskEntry> {
    let mut tasks: Vec<TaskEntry> = Vec::new();
    let mut current: Option<TaskEntry> = None;

    for line in output.lines() {
        let trimmed = line.trim();
        if trimmed.starts_with("* Task{") || trimmed.starts_with("Task{") {
            if let Some(task) = current.take() {
                tasks.push(task);
            }

            let Some(open) = trimmed.find('{') else {
                continue;
            };
            let Some(close) = trimmed.rfind('}') else {
                continue;
            };
            if close <= open {
                continue;
            }
            let inner = &trimmed[open + 1..close];
            let id = inner
                .split('#')
                .nth(1)
                .and_then(|value| value.split_whitespace().next())
                .unwrap_or("?")
                .to_string();
            let package = field_value(inner, "A=")
                .and_then(|value| {
                    value
                        .split_once(':')
                        .map(|(_, package)| package.to_string())
                })
                .or_else(|| {
                    field_value(inner, "I=")
                        .and_then(|value| value.split('/').next().map(str::to_string))
                })
                .unwrap_or_default();
            let visible = inner.contains("visible=true");

            current = Some(TaskEntry {
                id,
                package,
                activity: None,
                visible,
            });
        } else if let Some(task) = current.as_mut() {
            if task.activity.is_none() && trimmed.contains("ActivityRecord{") {
                task.activity = activity_component(trimmed);
            }
        }
    }

    if let Some(task) = current {
        tasks.push(task);
    }

    tasks.retain(|task| !task.package.is_empty());
    tasks.truncate(30);
    tasks
}

fn parse_power(output: &str, idle: &str) -> PowerReport {
    let mut wakelocks = Vec::new();
    let mut in_locks = false;

    for line in output.lines() {
        let trimmed = line.trim();
        if trimmed.starts_with("Wake Locks: size=") {
            in_locks = true;
            continue;
        }
        if in_locks {
            if trimmed.is_empty() || trimmed.starts_with("Suspend Blockers:") {
                in_locks = false;
                continue;
            }
            if let Some(wakelock) = parse_wakelock(trimmed) {
                wakelocks.push(wakelock);
            }
        }
    }

    PowerReport {
        wakefulness: field_value(output, "mWakefulness=").unwrap_or_else(|| "Unknown".to_string()),
        doze_state: field_value(idle, "mState=").unwrap_or_else(|| "Unknown".to_string()),
        light_doze_state: field_value(idle, "mLightState=")
            .unwrap_or_else(|| "Unknown".to_string()),
        battery_saver: output.contains("Battery Saver is currently: ON"),
        powered: field_value(output, "mIsPowered=")
            .map(|value| value == "true")
            .unwrap_or(false),
        wakelocks,
    }
}

fn parse_wakelock(line: &str) -> Option<WakelockEntry> {
    let kind = line.split_whitespace().next()?.to_string();
    if !kind.contains("WAKE_LOCK") {
        return None;
    }

    let tag = line
        .find('\'')
        .and_then(|start| {
            line[start + 1..]
                .find('\'')
                .map(|end| line[start + 1..start + 1 + end].to_string())
        })
        .unwrap_or_default();

    Some(WakelockEntry {
        kind,
        tag,
        held: field_value(line, "ACQ=").unwrap_or_default(),
        uid: field_value(line, "uid=").map(|value| trim_punctuation(&value)),
        pid: field_value(line, "pid=").map(|value| trim_punctuation(&value)),
    })
}

fn parse_app_usage(cpu: &str, memory: &str) -> Vec<AppUsageEntry> {
    let mut usage: HashMap<String, AppUsageEntry> = HashMap::new();

    for line in cpu.lines() {
        let trimmed = line.trim();
        let Some((percent, rest)) = trimmed.split_once('%') else {
            continue;
        };
        let Ok(percent) = percent.trim().parse::<f64>() else {
            continue;
        };
        let rest = rest.trim_start();
        let Some((pid, process)) = rest.split_once('/') else {
            continue;
        };
        if pid.trim().is_empty() || !pid.trim().chars().all(|value| value.is_ascii_digit()) {
            continue;
        }
        let process = process.split(':').next().unwrap_or(process).trim();
        if process.is_empty() {
            continue;
        }

        let entry = usage
            .entry(process.to_string())
            .or_insert_with(|| AppUsageEntry {
                package: process.to_string(),
                cpu_percent: 0.0,
                pss_kb: 0,
            });
        entry.cpu_percent += percent;
    }

    let mut in_pss = false;
    for line in memory.lines() {
        let trimmed = line.trim();
        if trimmed.starts_with("Total PSS by process:") {
            in_pss = true;
            continue;
        }
        if !in_pss {
            continue;
        }
        if trimmed.starts_with("Total PSS by OOM adjustment:")
            || trimmed.starts_with("Total PSS by category:")
        {
            break;
        }
        if trimmed.is_empty() {
            continue;
        }
        let Some((size, rest)) = trimmed.split_once("K:") else {
            continue;
        };
        let Ok(size) = size.replace(',', "").trim().parse::<u64>() else {
            continue;
        };
        let process = rest
            .trim()
            .split(" (pid")
            .next()
            .unwrap_or("")
            .trim()
            .split(':')
            .next()
            .unwrap_or("")
            .trim();
        if process.is_empty() {
            continue;
        }

        let entry = usage
            .entry(process.to_string())
            .or_insert_with(|| AppUsageEntry {
                package: process.to_string(),
                cpu_percent: 0.0,
                pss_kb: 0,
            });
        entry.pss_kb += size;
    }

    let mut entries: Vec<AppUsageEntry> = usage
        .into_values()
        .filter(|entry| entry.cpu_percent > 0.0 || entry.pss_kb > 0)
        .collect();
    entries.sort_by(|left, right| {
        right
            .cpu_percent
            .partial_cmp(&left.cpu_percent)
            .unwrap_or(std::cmp::Ordering::Equal)
            .then_with(|| right.pss_kb.cmp(&left.pss_kb))
    });
    entries.truncate(40);
    entries
}

fn parse_thermal_status(output: &str) -> Option<i32> {
    output
        .lines()
        .find_map(|line| field_value(line, "Thermal Status:"))
        .and_then(|value| value.parse().ok())
}

fn parse_thermal_zones(output: &str) -> Vec<ThermalZone> {
    let mut zones: Vec<ThermalZone> = Vec::new();

    for line in output.lines() {
        let trimmed = line.trim();
        if !trimmed.contains("Temperature{") {
            continue;
        }
        let Some(value) = field_value(trimmed, "mValue=") else {
            continue;
        };
        let Ok(temperature_c) = value.parse::<f64>() else {
            continue;
        };
        let Some(name) = field_value(trimmed, "mName=") else {
            continue;
        };
        if zones.iter().any(|zone| zone.name == name) {
            continue;
        }
        zones.push(ThermalZone {
            name,
            temperature_c,
            status: field_value(trimmed, "mStatus=").and_then(|value| value.parse().ok()),
        });
    }

    zones
}

fn parse_sensors(output: &str) -> Vec<SensorEntry> {
    let mut sensors = Vec::new();
    let mut in_list = false;

    for line in output.lines() {
        let trimmed = line.trim();
        if trimmed == "Sensor List:" {
            in_list = true;
            continue;
        }
        if !in_list {
            continue;
        }
        if trimmed.is_empty() {
            in_list = false;
            continue;
        }
        if let Some(sensor) = parse_sensor_line(trimmed) {
            sensors.push(sensor);
        }
    }

    let events = parse_sensor_events(output);
    for sensor in &mut sensors {
        if let Some(values) = events.get(&sensor.name) {
            sensor.values = values.clone();
        }
    }

    sensors
}

fn parse_sensor_line(line: &str) -> Option<SensorEntry> {
    if !line.starts_with("0x") {
        return None;
    }
    let end = line.find(')')?;
    let handle = line[..end].trim().to_string();
    let rest = line[end + 1..].trim();
    let parts: Vec<&str> = rest.split('|').map(str::trim).collect();
    if parts.len() < 4 {
        return None;
    }

    let name = parts[0].to_string();
    let vendor = parts[1].to_string();
    let type_name = parts[3]
        .strip_prefix("type:")
        .map(str::trim)
        .unwrap_or(parts[3])
        .to_string();
    let wake_up = parts
        .get(5)
        .and_then(|value| value.strip_prefix("flags:"))
        .and_then(|value| u32::from_str_radix(value.trim().trim_start_matches("0x"), 16).ok())
        .map(|flags| flags & 1 != 0)
        .unwrap_or(false);

    Some(SensorEntry {
        handle,
        name,
        vendor,
        type_name,
        wake_up,
        values: Vec::new(),
    })
}

fn parse_sensor_events(output: &str) -> HashMap<String, Vec<f64>> {
    let mut events = HashMap::new();
    let mut in_events = false;
    let mut current: Option<String> = None;

    for line in output.lines() {
        let trimmed = line.trim();
        if trimmed == "Recent Sensor events:" {
            in_events = true;
            continue;
        }
        if !in_events {
            continue;
        }
        if line.starts_with(char::is_whitespace) {
            if let (Some(name), Some(values)) = (current.as_ref(), event_values(trimmed)) {
                events.insert(name.clone(), values);
            }
            continue;
        }
        if trimmed.is_empty() {
            continue;
        }
        if trimmed.ends_with("events") {
            current = trimmed
                .split(": last ")
                .next()
                .map(str::trim)
                .filter(|value| !value.is_empty())
                .map(str::to_string);
        } else {
            current = None;
        }
    }

    events
}

fn event_values(line: &str) -> Option<Vec<f64>> {
    if !line.contains("(ts=") {
        return None;
    }
    let end = line.rfind(')')?;
    let values: Vec<f64> = line[end + 1..]
        .split(',')
        .filter_map(|value| value.trim().parse::<f64>().ok())
        .collect();
    if values.is_empty() {
        None
    } else {
        Some(values)
    }
}

fn field_value(source: &str, key: &str) -> Option<String> {
    let start = source.find(key)? + key.len();
    let value = source[start..]
        .trim_start()
        .split(|character: char| {
            character.is_whitespace()
                || character == ','
                || character == '}'
                || character == ')'
                || character == ']'
        })
        .next()
        .unwrap_or("")
        .trim();
    if value.is_empty() {
        None
    } else {
        Some(value.to_string())
    }
}

fn trim_punctuation(value: &str) -> String {
    value
        .trim_matches(|character: char| {
            character == ')' || character == '(' || character == ',' || character == '}'
        })
        .to_string()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn parses_notifications() {
        let output = r#"
    NotificationRecord(0x01: pkg=com.example user=UserHandle{0} id=42 tag=null importance=4 key=0|com.example|42|null|1000: Notification(channel=alerts shortcut=null))
        android.title=String (Hello (world))
        android.text=String (Body text)
        mCreationTimeMs=1700000000000
    NotificationRecord(0x02: pkg=android user=UserHandle{-1} id=1 tag=ranker_group importance=1 key=x: Notification(channel=group))
"#;
        let entries = parse_notifications(output);
        assert_eq!(entries.len(), 1);
        assert_eq!(entries[0].package, "com.example");
        assert_eq!(entries[0].id, "42");
        assert_eq!(entries[0].tag, "");
        assert_eq!(entries[0].channel, "alerts");
        assert_eq!(entries[0].importance, Some(4));
        assert_eq!(entries[0].title.as_deref(), Some("Hello (world)"));
        assert_eq!(entries[0].text.as_deref(), Some("Body text"));
        assert_eq!(entries[0].created_at_ms, Some(1700000000000));
    }

    #[test]
    fn parses_activity_and_tasks() {
        let output = r#"
  ResumedActivity: ActivityRecord{abc123 u0 com.example/.MainActivity t12 d0}
  * Task{def456 #12 type=standard A=10123:com.example U=0 visible=true}
    mResumedActivity: ActivityRecord{abc123 u0 com.example/.MainActivity t12 d0}
  * Task{ghi789 #13 type=standard A=10124:com.other U=0 visible=false}
    * Hist #0: ActivityRecord{jkl012 u0 com.other/.Launcher t13}
"#;
        let foreground = parse_foreground(output);
        assert_eq!(foreground.as_deref(), Some("com.example/.MainActivity"));
        let tasks = parse_tasks(output);
        assert_eq!(tasks.len(), 2);
        assert_eq!(tasks[0].id, "12");
        assert_eq!(tasks[0].package, "com.example");
        assert!(tasks[0].visible);
        assert_eq!(tasks[1].package, "com.other");
        assert_eq!(tasks[1].activity.as_deref(), Some("com.other/.Launcher"));
    }

    #[test]
    fn parses_power_report() {
        let power = r#"
  mWakefulness=Dozing
  mIsPowered=true
  Battery Saver is currently: OFF
  Wake Locks: size=2
    DOZE_WAKE_LOCK                 'DreamManagerService' ACQ=-33m49s456ms (uid=1000 pid=989)
    PARTIAL_WAKE_LOCK              'AudioMix' ACQ=1m2s (uid=10123 pid=4321)
  Suspend Blockers: size=5
"#;
        let idle = "  mState=ACTIVE mLightState=IDLE\n";
        let report = parse_power(power, idle);
        assert_eq!(report.wakefulness, "Dozing");
        assert_eq!(report.doze_state, "ACTIVE");
        assert_eq!(report.light_doze_state, "IDLE");
        assert!(report.powered);
        assert!(!report.battery_saver);
        assert_eq!(report.wakelocks.len(), 2);
        assert_eq!(report.wakelocks[0].tag, "DreamManagerService");
        assert_eq!(report.wakelocks[0].uid.as_deref(), Some("1000"));
        assert_eq!(report.wakelocks[1].held, "1m2s");
    }

    #[test]
    fn parses_app_usage() {
        let cpu = r#"
Load: 2.1 / 2.0 / 1.8
CPU usage: 12.3% user + 7.7% kernel
  4.5% 1234/com.example: 3.0% user + 1.5% kernel
  1.0% 1235/com.example:remote: 0.5% user + 0.5% kernel
  2.0% 999/system_server: 1.0% user + 1.0% kernel
100% TOTAL: 12.3% user + 7.7% kernel
"#;
        let memory = r#"
Total PSS by process:
    120,000K: com.example (pid 1234)
     30,000K: com.example:remote (pid 1235)
     80,000K: system_server (pid 999)
Total PSS by OOM adjustment:
"#;
        let usage = parse_app_usage(cpu, memory);
        assert_eq!(usage.len(), 2);
        let example = usage
            .iter()
            .find(|entry| entry.package == "com.example")
            .unwrap();
        assert!((example.cpu_percent - 5.5).abs() < 0.001);
        assert_eq!(example.pss_kb, 150_000);
        assert!(usage.iter().any(|entry| entry.package == "system_server"));
    }

    #[test]
    fn parses_sensors_and_thermal() {
        let thermal = r#"
Thermal Status: 2
Current temperatures from HAL:
  Temperature{mValue=36.5, mType=0, mName=CPU, mStatus=0}
  Temperature{mValue=41.2, mType=1, mName=GPU, mStatus=1}
"#;
        assert_eq!(parse_thermal_status(thermal), Some(2));
        let zones = parse_thermal_zones(thermal);
        assert_eq!(zones.len(), 2);
        assert_eq!(zones[0].name, "CPU");
        assert!((zones[0].temperature_c - 36.5).abs() < 0.001);

        let sensors = r#"
Sensor List:
0x00000001) Accelerometer Sensor | Vendor Inc. | ver: 1 | type: android.sensor.accelerometer(1) | perm: n/a | flags: 0x00000000
0x00000002) Wake Up Proximity | Vendor Inc. | ver: 1 | type: android.sensor.proximity(8) | perm: n/a | flags: 0x00000001

Recent Sensor events:
Accelerometer Sensor: last 30 events
    1 (ts=1000, wall=2000) 0.10, 0.20, 9.81, 
    2 (ts=1100, wall=2100) 0.11, 0.21, 9.82, 
Wake Up Proximity: last 10 events
    1 (ts=1200, wall=2200) 5.00, 
"#;
        let sensors = parse_sensors(sensors);
        assert_eq!(sensors.len(), 2);
        assert_eq!(sensors[0].name, "Accelerometer Sensor");
        assert!(!sensors[0].wake_up);
        assert_eq!(sensors[0].values, vec![0.11, 0.21, 9.82]);
        assert!(sensors[1].wake_up);
        assert_eq!(sensors[1].values, vec![5.0]);
    }
}
