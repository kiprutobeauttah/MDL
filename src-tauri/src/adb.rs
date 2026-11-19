use std::process::Command;
use std::sync::atomic::{AtomicBool, Ordering};
use std::sync::RwLock;

use crate::collectors;
use crate::models::{DeviceEntry, DeviceInfo, ShellOutput};

#[derive(Default)]
pub struct AdbClient {
    serial: RwLock<Option<String>>,
    monitoring: AtomicBool,
}

impl AdbClient {
    pub fn new() -> Self {
        Self::default()
    }

    pub fn serial(&self) -> Option<String> {
        self.serial.read().ok().and_then(|value| value.clone())
    }

    pub fn monitoring(&self) -> bool {
        self.monitoring.load(Ordering::SeqCst)
    }

    pub fn set_monitoring(&self, value: bool) {
        self.monitoring.store(value, Ordering::SeqCst);
    }

    pub fn detect_devices(&self) -> Vec<DeviceEntry> {
        let output = match run_adb(&["devices", "-l"]) {
            Ok(output) => output,
            Err(error) => {
                eprintln!("Error detecting devices: {error}");
                return Vec::new();
            }
        };

        let mut devices = Vec::new();

        for line in output.lines().skip(1) {
            let line = line.trim();
            if line.is_empty() {
                continue;
            }

            let mut parts = line.split_whitespace();
            let serial = match parts.next() {
                Some(value) => value.to_string(),
                None => continue,
            };
            let state = parts.next().unwrap_or("unknown").to_string();

            let mut model = String::new();
            for part in parts {
                if let Some(value) = part.strip_prefix("model:") {
                    model = value.replace('_', " ");
                }
            }

            let connection_type = if serial.contains(':') {
                "wireless"
            } else {
                "usb"
            };

            devices.push(DeviceEntry {
                serial,
                state,
                connection_type: connection_type.to_string(),
                model,
            });
        }

        devices
    }

    pub fn connect(&self, serial: &str) -> Result<DeviceInfo, String> {
        let state = run_adb(&["-s", serial, "get-state"])?;
        if state.trim() != "device" {
            return Err(format!("Device is not available ({})", state.trim()));
        }

        if let Ok(mut current) = self.serial.write() {
            *current = Some(serial.to_string());
        }

        let info = collectors::device::collect(self)?;
        Ok(info)
    }

    pub fn disconnect(&self) {
        self.set_monitoring(false);
        if let Ok(mut current) = self.serial.write() {
            *current = None;
        }
    }

    pub fn execute(&self, command: &str) -> Result<String, String> {
        let serial = self
            .serial()
            .ok_or_else(|| "No device connected".to_string())?;
        self.execute_on(&serial, command)
    }

    pub fn execute_on(&self, serial: &str, command: &str) -> Result<String, String> {
        run_adb(&["-s", serial, "shell", command])
    }

    pub fn shell(&self, command: &str) -> Result<ShellOutput, String> {
        let serial = self
            .serial()
            .ok_or_else(|| "No device connected".to_string())?;
        let output = Command::new("adb")
            .arg("-s")
            .arg(&serial)
            .arg("shell")
            .arg(command)
            .output()
            .map_err(|error| format!("Failed to run adb: {error}"))?;

        Ok(ShellOutput {
            stdout: String::from_utf8_lossy(&output.stdout).to_string(),
            stderr: String::from_utf8_lossy(&output.stderr).to_string(),
            exit_code: output.status.code().unwrap_or(-1),
        })
    }

    pub fn read_file_bytes(&self, path: &str) -> Result<Vec<u8>, String> {
        let serial = self
            .serial()
            .ok_or_else(|| "No device connected".to_string())?;
        let output = Command::new("adb")
            .arg("-s")
            .arg(&serial)
            .arg("exec-out")
            .arg(format!("cat {}", shell_quote(path)))
            .output()
            .map_err(|error| format!("Failed to run adb: {error}"))?;

        if !output.status.success() {
            let stderr = String::from_utf8_lossy(&output.stderr);
            let stdout = String::from_utf8_lossy(&output.stdout);
            let message = if stderr.trim().is_empty() {
                stdout.trim()
            } else {
                stderr.trim()
            };
            return Err(if message.is_empty() {
                format!("Unable to read {path}")
            } else {
                message.to_string()
            });
        }

        Ok(output.stdout)
    }
}

pub(crate) fn shell_quote(value: &str) -> String {
    format!("'{}'", value.replace('\'', "'\\''"))
}

fn run_adb(args: &[&str]) -> Result<String, String> {
    let output = Command::new("adb")
        .args(args)
        .output()
        .map_err(|error| format!("Failed to run adb: {error}"))?;

    if !output.status.success() {
        let stderr = String::from_utf8_lossy(&output.stderr);
        let stdout = String::from_utf8_lossy(&output.stdout);
        let message = if stderr.trim().is_empty() {
            stdout.trim().to_string()
        } else {
            stderr.trim().to_string()
        };
        return Err(message);
    }

    Ok(String::from_utf8_lossy(&output.stdout).trim().to_string())
}
