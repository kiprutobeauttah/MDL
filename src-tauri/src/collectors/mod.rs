pub mod apps;
pub mod battery;
pub mod bluetooth;
pub mod cellular;
pub mod device;
pub mod network;
pub mod performance;
pub mod wifi;

use chrono::Local;
use serde_json::Value;

use crate::models::MetricEvent;

pub fn event(category: &str, source: &str, metric: &str, value: impl Into<Value>) -> MetricEvent {
    event_with_severity(category, source, metric, value, "normal")
}

pub fn event_with_severity(
    category: &str,
    source: &str,
    metric: &str,
    value: impl Into<Value>,
    severity: &str,
) -> MetricEvent {
    MetricEvent {
        timestamp: Local::now().format("%H:%M:%S").to_string(),
        category: category.to_string(),
        source: source.to_string(),
        metric: metric.to_string(),
        value: value.into(),
        severity: severity.to_string(),
        message: String::new(),
    }
}

pub fn parse_number_after(line: &str, key: &str) -> Option<f64> {
    let start = line.find(key)? + key.len();
    let rest = line[start..].trim_start();
    let token = rest.split([',', ' ', '}']).next()?;
    let token = token.trim_end_matches(|character: char| {
        !character.is_ascii_digit() && character != '.' && character != '-'
    });
    token.parse().ok()
}
