use std::fs;
use std::path::{Path, PathBuf};
use std::sync::Mutex;

use chrono::Local;

use crate::models::{ExportResult, MetricEvent, SessionRecord, SessionSummary};

#[derive(Default)]
pub struct SessionRecorder {
    current: Mutex<Option<ActiveSession>>,
}

struct ActiveSession {
    id: String,
    name: String,
    started_at: String,
    events: Vec<MetricEvent>,
}

impl SessionRecorder {
    pub fn start(&self, name: Option<String>) -> Result<SessionSummary, String> {
        let mut current = self
            .current
            .lock()
            .map_err(|_| "Session recorder is unavailable".to_string())?;

        if current.is_some() {
            return Err("A session is already recording".to_string());
        }

        let now = Local::now();
        let id = now.format("%Y%m%d-%H%M%S-%3f").to_string();
        let started_at = now.to_rfc3339();
        let name = name
            .map(|value| value.trim().to_string())
            .filter(|value| !value.is_empty())
            .unwrap_or_else(|| format!("Session {}", now.format("%b %d, %H:%M:%S")));

        *current = Some(ActiveSession {
            id: id.clone(),
            name: name.clone(),
            started_at: started_at.clone(),
            events: Vec::new(),
        });

        Ok(SessionSummary {
            id,
            name,
            started_at,
            ended_at: None,
            event_count: 0,
        })
    }

    pub fn record(&self, event: &MetricEvent) {
        if let Ok(mut current) = self.current.lock() {
            if let Some(session) = current.as_mut() {
                session.events.push(event.clone());
            }
        }
    }

    pub fn stop(&self, data_dir: &Path) -> Result<SessionSummary, String> {
        let mut current = self
            .current
            .lock()
            .map_err(|_| "Session recorder is unavailable".to_string())?;

        let session = current
            .take()
            .ok_or_else(|| "No session is recording".to_string())?;
        let ended_at = Local::now().to_rfc3339();
        let record = SessionRecord {
            id: session.id.clone(),
            name: session.name.clone(),
            started_at: session.started_at.clone(),
            ended_at: ended_at.clone(),
            events: session.events,
        };

        if let Err(error) = save(data_dir, &record) {
            *current = Some(ActiveSession {
                id: record.id,
                name: record.name,
                started_at: record.started_at,
                events: record.events,
            });
            return Err(error);
        }

        Ok(SessionSummary {
            id: record.id,
            name: record.name,
            started_at: record.started_at,
            ended_at: Some(ended_at),
            event_count: record.events.len(),
        })
    }

    pub fn status(&self) -> Option<SessionSummary> {
        self.current.lock().ok().and_then(|current| {
            current.as_ref().map(|session| SessionSummary {
                id: session.id.clone(),
                name: session.name.clone(),
                started_at: session.started_at.clone(),
                ended_at: None,
                event_count: session.events.len(),
            })
        })
    }

    pub fn list(data_dir: &Path) -> Vec<SessionSummary> {
        let directory = sessions_dir(data_dir);
        let Ok(entries) = fs::read_dir(directory) else {
            return Vec::new();
        };

        let mut sessions = Vec::new();
        for entry in entries.flatten() {
            let path = entry.path();
            if path.extension().and_then(|value| value.to_str()) != Some("json") {
                continue;
            }
            if let Ok(contents) = fs::read_to_string(&path) {
                if let Ok(record) = serde_json::from_str::<SessionRecord>(&contents) {
                    sessions.push(SessionSummary {
                        id: record.id,
                        name: record.name,
                        started_at: record.started_at,
                        ended_at: Some(record.ended_at),
                        event_count: record.events.len(),
                    });
                }
            }
        }

        sessions.sort_by(|left, right| right.started_at.cmp(&left.started_at));
        sessions
    }

    pub fn load(data_dir: &Path, id: &str) -> Result<SessionRecord, String> {
        validate_id(id)?;
        let path = sessions_dir(data_dir).join(format!("{id}.json"));
        let contents = fs::read_to_string(&path)
            .map_err(|error| format!("Unable to read session: {error}"))?;
        serde_json::from_str(&contents).map_err(|error| format!("Invalid session file: {error}"))
    }

    pub fn export(data_dir: &Path, id: &str, format: &str) -> Result<ExportResult, String> {
        let record = Self::load(data_dir, id)?;
        let format = format.trim().to_lowercase();
        let directory = data_dir.join("exports");
        fs::create_dir_all(&directory)
            .map_err(|error| format!("Unable to create export directory: {error}"))?;

        let (extension, contents) = match format.as_str() {
            "json" => (
                "json",
                serde_json::to_string_pretty(&record).map_err(|error| error.to_string())?,
            ),
            "csv" => ("csv", to_csv(&record)),
            _ => return Err("Unsupported export format. Use csv or json.".to_string()),
        };

        let path = directory.join(format!("{}.{}", record.id, extension));
        fs::write(&path, contents).map_err(|error| format!("Unable to write export: {error}"))?;

        Ok(ExportResult {
            path: path.to_string_lossy().to_string(),
            events: record.events.len(),
        })
    }
}

fn save(data_dir: &Path, record: &SessionRecord) -> Result<(), String> {
    validate_id(&record.id)?;
    let directory = sessions_dir(data_dir);
    fs::create_dir_all(&directory)
        .map_err(|error| format!("Unable to create session directory: {error}"))?;
    let contents = serde_json::to_string_pretty(record).map_err(|error| error.to_string())?;
    fs::write(directory.join(format!("{}.json", record.id)), contents)
        .map_err(|error| format!("Unable to save session: {error}"))
}

fn sessions_dir(data_dir: &Path) -> PathBuf {
    data_dir.join("sessions")
}

fn validate_id(id: &str) -> Result<(), String> {
    if id.is_empty()
        || !id
            .chars()
            .all(|value| value.is_ascii_alphanumeric() || value == '-' || value == '_')
    {
        return Err("Invalid session id".to_string());
    }
    Ok(())
}

fn to_csv(record: &SessionRecord) -> String {
    let mut output = String::from("timestamp,category,source,metric,value,severity,message\n");
    for event in &record.events {
        let value = serde_json::to_string(&event.value).unwrap_or_default();
        output.push_str(&csv_row(&[
            event.timestamp.clone(),
            event.category.clone(),
            event.source.clone(),
            event.metric.clone(),
            value,
            event.severity.clone(),
            event.message.clone(),
        ]));
    }
    output
}

fn csv_row(fields: &[String]) -> String {
    let mut row = fields
        .iter()
        .map(|field| csv_field(field))
        .collect::<Vec<_>>()
        .join(",");
    row.push('\n');
    row
}

fn csv_field(value: &str) -> String {
    if value.contains(',') || value.contains('"') || value.contains('\n') || value.contains('\r') {
        format!("\"{}\"", value.replace('"', "\"\""))
    } else {
        value.to_string()
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use serde_json::json;

    fn event(message: &str) -> MetricEvent {
        MetricEvent {
            timestamp: "2026-01-01T00:00:00+00:00".to_string(),
            category: "battery".to_string(),
            source: "battery".to_string(),
            metric: "level".to_string(),
            value: json!(42),
            severity: "info".to_string(),
            message: message.to_string(),
        }
    }

    #[test]
    fn csv_escapes_commas_and_quotes() {
        assert_eq!(csv_field("plain"), "plain");
        assert_eq!(csv_field("a,b"), "\"a,b\"");
        assert_eq!(csv_field("say \"hi\""), "\"say \"\"hi\"\"\"");
    }

    #[test]
    fn session_round_trip_and_export() {
        let dir = std::env::temp_dir().join(format!("mdl-session-test-{}", std::process::id()));
        let _ = fs::remove_dir_all(&dir);
        let recorder = SessionRecorder::default();
        let summary = recorder.start(Some("Test session".to_string())).unwrap();
        recorder.record(&event("hello, world"));
        let stopped = recorder.stop(&dir).unwrap();
        assert_eq!(stopped.event_count, 1);

        let sessions = SessionRecorder::list(&dir);
        assert_eq!(sessions.len(), 1);
        assert_eq!(sessions[0].id, summary.id);

        let export = SessionRecorder::export(&dir, &summary.id, "csv").unwrap();
        assert_eq!(export.events, 1);
        let csv = fs::read_to_string(export.path).unwrap();
        assert!(csv.contains("\"hello, world\""));

        let _ = fs::remove_dir_all(&dir);
    }

    #[test]
    fn rejects_unsafe_ids() {
        assert!(validate_id("../escape").is_err());
        assert!(validate_id("ok-id_1").is_ok());
    }
}
