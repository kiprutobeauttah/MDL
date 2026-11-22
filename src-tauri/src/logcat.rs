use std::io::{BufRead, BufReader, Read};
use std::process::{Child, Command, Stdio};
use std::sync::Mutex;
use std::thread;

use tauri::{AppHandle, Emitter};

use crate::adb::AdbClient;
use crate::models::{DeviceLogEnd, DeviceLogEvent};

#[derive(Default)]
pub struct DeviceLogState {
    session: Mutex<Option<DeviceLogSession>>,
}

struct DeviceLogSession {
    child: Child,
}

pub fn start(
    app: AppHandle,
    adb: &AdbClient,
    logs: &DeviceLogState,
    session: u64,
    buffer: &str,
    level: &str,
    tag: &str,
) -> Result<(), String> {
    let serial = adb
        .serial()
        .ok_or_else(|| "No device connected".to_string())?;

    let buffer = match buffer.trim().to_lowercase().as_str() {
        "system" => "system",
        "crash" => "crash",
        "all" => "all",
        _ => "main",
    };
    let level = match level.trim().to_uppercase().as_str() {
        "V" => "V",
        "D" => "D",
        "W" => "W",
        "E" => "E",
        "F" => "F",
        _ => "I",
    };
    let tag = tag.trim();
    if !tag.is_empty()
        && !tag.chars().all(|value| {
            value.is_ascii_alphanumeric() || value == '_' || value == '.' || value == '-'
        })
    {
        return Err(
            "Tag may only contain letters, numbers, dots, dashes and underscores".to_string(),
        );
    }

    stop(logs);

    let mut args = vec![
        "-s".to_string(),
        serial,
        "logcat".to_string(),
        "-v".to_string(),
        "time".to_string(),
        "-b".to_string(),
        buffer.to_string(),
    ];
    if tag.is_empty() {
        args.push(format!("*:{level}"));
    } else {
        args.push(format!("{tag}:{level}"));
        args.push("*:S".to_string());
    }

    let mut child = Command::new("adb")
        .args(&args)
        .stdout(Stdio::piped())
        .stderr(Stdio::piped())
        .spawn()
        .map_err(|error| format!("Failed to start logcat: {error}"))?;

    let stdout = child
        .stdout
        .take()
        .ok_or_else(|| "Failed to capture logcat output".to_string())?;
    let stderr = child.stderr.take();

    {
        let mut current = logs
            .session
            .lock()
            .map_err(|_| "Log stream is unavailable".to_string())?;
        *current = Some(DeviceLogSession { child });
    }

    spawn_reader(app.clone(), stdout, session, None);
    if let Some(stderr) = stderr {
        spawn_reader(app, stderr, session, Some("[logcat] "));
    }

    Ok(())
}

pub fn stop(logs: &DeviceLogState) {
    if let Ok(mut current) = logs.session.lock() {
        if let Some(mut session) = current.take() {
            let _ = session.child.kill();
            let _ = session.child.wait();
        }
    }
}

fn spawn_reader<R: Read + Send + 'static>(
    app: AppHandle,
    source: R,
    session: u64,
    prefix: Option<&'static str>,
) {
    thread::spawn(move || {
        let reader = BufReader::new(source);
        for line in reader.lines() {
            let Ok(line) = line else {
                break;
            };
            let line = match prefix {
                Some(prefix) => format!("{prefix}{line}"),
                None => line,
            };
            let _ = app.emit("device-log", DeviceLogEvent { session, line });
        }

        if prefix.is_none() {
            let _ = app.emit("device-log-end", DeviceLogEnd { session });
        }
    });
}
