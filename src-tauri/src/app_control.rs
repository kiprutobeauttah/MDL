use std::collections::{HashMap, HashSet};
use std::io::{BufRead, BufReader, Read};
use std::process::{Child, Command, Stdio};
use std::sync::Mutex;
use std::thread;

use tauri::{AppHandle, Emitter};

use crate::adb::{shell_quote, AdbClient};
use crate::models::{AppDetails, AppLogEnd, AppLogEvent, AppPermission, ShellOutput};

#[derive(Default)]
pub struct LogcatState {
    session: Mutex<Option<LogcatSession>>,
}

struct LogcatSession {
    child: Child,
}

pub fn launch(adb: &AdbClient, package: &str) -> Result<String, String> {
    validate_package(package)?;

    let resolved = adb.shell(&format!(
        "cmd package resolve-activity --brief -c android.intent.category.LAUNCHER {}",
        shell_quote(package)
    ))?;

    let component = resolved
        .stdout
        .lines()
        .map(str::trim)
        .rev()
        .find(|line| line.contains('/') && !line.contains(char::is_whitespace))
        .map(str::to_string);

    if let Some(component) = component {
        let result = adb.shell(&format!("am start -W -n {}", shell_quote(&component)))?;
        if result.exit_code != 0 {
            return Err(command_error(&result, "Unable to launch the application"));
        }
        if result.stdout.contains("Error:")
            || result.stdout.contains("Error type")
            || result.stdout.contains("Exception")
        {
            return Err(result.stdout.trim().to_string());
        }
        return Ok(format!("Launched {package}"));
    }

    let result = adb.shell(&format!(
        "monkey -p {} -c android.intent.category.LAUNCHER 1",
        shell_quote(package)
    ))?;
    if result.exit_code != 0 {
        return Err(command_error(&result, "Unable to launch the application"));
    }
    if result.stdout.contains("No activities found") || result.stdout.contains("monkey aborted") {
        return Err(format!("{package} has no launchable activity"));
    }

    Ok(format!("Launched {package}"))
}

pub fn stop(adb: &AdbClient, package: &str) -> Result<String, String> {
    validate_package(package)?;

    let result = adb.shell(&format!("am force-stop {}", shell_quote(package)))?;
    if result.exit_code != 0 {
        return Err(command_error(&result, "Unable to stop the application"));
    }

    let combined = format!("{}{}", result.stdout, result.stderr);
    if combined.contains("Error:") || combined.contains("Exception") {
        return Err(combined.trim().to_string());
    }

    Ok(format!("Stopped {package}"))
}

pub fn details(adb: &AdbClient, package: &str) -> Result<AppDetails, String> {
    validate_package(package)?;

    let permissions = permissions(adb, package)?;
    let pids = pids(adb, package).unwrap_or_default();
    let (apk_size, data_size, cache_size) = sizes(adb, package);

    Ok(AppDetails {
        package: package.to_string(),
        running: !pids.is_empty(),
        pids,
        apk_size,
        data_size,
        cache_size,
        permissions,
        services: services(adb, package),
        jobs: matching_lines(adb, "dumpsys jobscheduler | grep -F 'JOB #'", package),
        alarms: matching_lines(adb, "dumpsys alarm | grep -F 'Alarm{'", package),
    })
}

pub fn start_logs(
    app: AppHandle,
    adb: &AdbClient,
    logs: &LogcatState,
    package: &str,
    session: u64,
) -> Result<(), String> {
    validate_package(package)?;

    let serial = adb
        .serial()
        .ok_or_else(|| "No device connected".to_string())?;
    let pids = pids(adb, package)?;
    let pid = pids
        .first()
        .ok_or_else(|| "Application is not running. Launch it first.".to_string())?;

    stop_logs(logs);

    let mut child = Command::new("adb")
        .arg("-s")
        .arg(&serial)
        .arg("logcat")
        .arg("-v")
        .arg("time")
        .arg(format!("--pid={pid}"))
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
        *current = Some(LogcatSession { child });
    }

    let package = package.to_string();
    spawn_reader(app.clone(), stdout, session, package.clone(), None);
    if let Some(stderr) = stderr {
        spawn_reader(app, stderr, session, package, Some("[logcat] "));
    }

    Ok(())
}

pub fn stop_logs(logs: &LogcatState) {
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
    package: String,
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
            let _ = app.emit(
                "app-log",
                AppLogEvent {
                    session,
                    package: package.clone(),
                    line,
                },
            );
        }

        if prefix.is_none() {
            let _ = app.emit("app-log-end", AppLogEnd { session, package });
        }
    });
}

fn pids(adb: &AdbClient, package: &str) -> Result<Vec<u32>, String> {
    let output = adb.shell(&format!("pidof {}", shell_quote(package)))?;
    if output.exit_code != 0 {
        return Ok(Vec::new());
    }

    Ok(output
        .stdout
        .split_whitespace()
        .filter_map(|value| value.parse().ok())
        .collect())
}

fn permissions(adb: &AdbClient, package: &str) -> Result<Vec<AppPermission>, String> {
    let output = adb.shell(&format!("dumpsys package {}", shell_quote(package)))?;

    if output.exit_code != 0 {
        return Err(command_error(&output, "Unable to read package details"));
    }

    if !output.stdout.contains("Package [") {
        let message = output.stdout.trim();
        return Err(if message.is_empty() {
            format!("Package {package} was not found")
        } else {
            message.to_string()
        });
    }

    Ok(parse_permissions(&output.stdout))
}

fn parse_permissions(output: &str) -> Vec<AppPermission> {
    let mut requested: Vec<String> = Vec::new();
    let mut install: HashMap<String, Option<bool>> = HashMap::new();
    let mut runtime: HashMap<String, Option<bool>> = HashMap::new();
    let mut section = "";
    let mut section_indent = 0;

    for line in output.lines() {
        let trimmed = line.trim();
        if trimmed.is_empty() {
            continue;
        }

        let indent = line.len() - line.trim_start().len();
        let header = match trimmed {
            "requested permissions:" => Some("requested"),
            "install permissions:" => Some("install"),
            "runtime permissions:" => Some("runtime"),
            _ => None,
        };

        if let Some(header) = header {
            section = header;
            section_indent = indent;
            continue;
        }

        if !section.is_empty() && indent <= section_indent {
            section = "";
        }

        match section {
            "requested" => {
                if looks_like_permission(trimmed) && !requested.iter().any(|name| name == trimmed) {
                    requested.push(trimmed.to_string());
                }
            }
            "install" => {
                if let Some((name, granted)) = parse_granted(trimmed) {
                    install.entry(name).or_insert(granted);
                }
            }
            "runtime" => {
                if let Some((name, granted)) = parse_granted(trimmed) {
                    runtime.entry(name).or_insert(granted);
                }
            }
            _ => {}
        }
    }

    let mut names = requested;
    for name in install.keys().chain(runtime.keys()) {
        if !names.iter().any(|existing| existing == name) {
            names.push(name.clone());
        }
    }
    names.sort();

    names
        .into_iter()
        .map(|name| {
            let is_runtime = runtime.contains_key(&name);
            let granted = runtime
                .get(&name)
                .copied()
                .flatten()
                .or_else(|| install.get(&name).copied().flatten());

            AppPermission {
                name,
                granted,
                runtime: is_runtime,
            }
        })
        .collect()
}

fn parse_granted(line: &str) -> Option<(String, Option<bool>)> {
    let (name, rest) = line.split_once(':')?;
    let name = name.trim();

    if !looks_like_permission(name) {
        return None;
    }

    let granted = if rest.contains("granted=true") {
        Some(true)
    } else if rest.contains("granted=false") {
        Some(false)
    } else {
        None
    };

    Some((name.to_string(), granted))
}

fn looks_like_permission(value: &str) -> bool {
    value.contains('.')
        && !value.contains(char::is_whitespace)
        && !value.contains('=')
        && !value.contains(':')
        && !value.contains('[')
        && !value.contains('{')
        && !value.contains('/')
}

fn sizes(adb: &AdbClient, package: &str) -> (Option<u64>, Option<u64>, Option<u64>) {
    if let Some(sizes) = diskstats_sizes(adb, package) {
        return sizes;
    }

    (apk_size(adb, package), None, None)
}

fn diskstats_sizes(
    adb: &AdbClient,
    package: &str,
) -> Option<(Option<u64>, Option<u64>, Option<u64>)> {
    let output = adb.execute("dumpsys diskstats").ok()?;
    let names = array_values(&output, "Package Names:")?;
    let index = names.iter().position(|name| name == package)?;

    let app = numeric_array(&output, "App Sizes:").and_then(|values| values.get(index).copied());
    let data =
        numeric_array(&output, "App Data Sizes:").and_then(|values| values.get(index).copied());
    let cache =
        numeric_array(&output, "Cache Sizes:").and_then(|values| values.get(index).copied());

    Some((app, data, cache))
}

fn array_values(output: &str, key: &str) -> Option<Vec<String>> {
    let line = output
        .lines()
        .find(|line| line.trim_start().starts_with(key))?;
    let start = line.find('[')? + 1;
    let end = line.rfind(']')?;

    if end <= start {
        return Some(Vec::new());
    }

    Some(
        line[start..end]
            .split(',')
            .map(|value| value.trim().trim_matches('"').to_string())
            .filter(|value| !value.is_empty())
            .collect(),
    )
}

fn numeric_array(output: &str, key: &str) -> Option<Vec<u64>> {
    Some(
        array_values(output, key)?
            .iter()
            .map(|value| value.parse().unwrap_or(0))
            .collect(),
    )
}

fn apk_size(adb: &AdbClient, package: &str) -> Option<u64> {
    let output = adb
        .execute(&format!("pm path {}", shell_quote(package)))
        .ok()?;
    let mut total = 0;
    let mut found = false;

    for line in output.lines() {
        let Some(path) = line.trim().strip_prefix("package:") else {
            continue;
        };

        if let Ok(size) = adb.execute(&format!("stat -c %s {}", shell_quote(path.trim()))) {
            if let Ok(value) = size.trim().parse::<u64>() {
                total += value;
                found = true;
            }
        }
    }

    if found {
        Some(total)
    } else {
        None
    }
}

fn services(adb: &AdbClient, package: &str) -> Vec<String> {
    let Ok(output) = adb.shell(&format!(
        "dumpsys activity services {}",
        shell_quote(package)
    )) else {
        return Vec::new();
    };

    let mut seen = HashSet::new();
    let mut result = Vec::new();

    for line in output.stdout.lines() {
        let trimmed = line.trim();
        if !trimmed.contains("ServiceRecord{") || !contains_package(trimmed, package) {
            continue;
        }

        let Some(start) = trimmed.find("ServiceRecord{") else {
            continue;
        };
        let inner = &trimmed[start + "ServiceRecord{".len()..];
        let Some(end) = inner.find('}') else {
            continue;
        };
        let Some(component) = inner[..end].split_whitespace().last() else {
            continue;
        };
        let component = component.trim().to_string();
        let belongs = component == package
            || component
                .strip_prefix(package)
                .is_some_and(|rest| rest.starts_with('/'));

        if belongs && seen.insert(component.clone()) {
            result.push(component);
            if result.len() >= 25 {
                break;
            }
        }
    }

    result
}

fn matching_lines(adb: &AdbClient, command: &str, package: &str) -> Vec<String> {
    let command = format!("{command} | grep -F {}", shell_quote(package));
    let Ok(output) = adb.shell(&command) else {
        return Vec::new();
    };

    let mut seen = HashSet::new();
    let mut result = Vec::new();

    for line in output.stdout.lines() {
        let trimmed = line.trim();
        if trimmed.is_empty() || !contains_package(trimmed, package) {
            continue;
        }
        if seen.insert(trimmed.to_string()) {
            result.push(trimmed.to_string());
            if result.len() >= 20 {
                break;
            }
        }
    }

    result
}

fn contains_package(haystack: &str, package: &str) -> bool {
    if package.is_empty() {
        return false;
    }

    let mut offset = 0;

    while let Some(index) = haystack[offset..].find(package) {
        let start = offset + index;
        let end = start + package.len();
        let before_ok = haystack[..start]
            .chars()
            .next_back()
            .map_or(true, |character| {
                !(character.is_ascii_alphanumeric() || character == '.' || character == '_')
            });
        let after_ok = haystack[end..].chars().next().map_or(true, |character| {
            !(character.is_ascii_alphanumeric() || character == '.' || character == '_')
        });

        if before_ok && after_ok {
            return true;
        }

        offset = end;
    }

    false
}

fn validate_package(package: &str) -> Result<(), String> {
    let package = package.trim();
    let valid = !package.is_empty()
        && package.len() <= 255
        && package
            .chars()
            .next()
            .is_some_and(|character| character.is_ascii_alphanumeric())
        && package
            .chars()
            .all(|character| character.is_ascii_alphanumeric() || matches!(character, '.' | '_'));

    if valid {
        Ok(())
    } else {
        Err("Invalid package name".to_string())
    }
}

fn command_error(output: &ShellOutput, fallback: &str) -> String {
    let stderr = output.stderr.trim();
    let stdout = output.stdout.trim();
    let message = if stderr.is_empty() { stdout } else { stderr };

    if message.is_empty() {
        fallback.to_string()
    } else {
        message.to_string()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn parses_permissions_and_stops_at_next_section() {
        let output = "\
    requested permissions:
      android.permission.INTERNET
      android.permission.CAMERA
    install permissions:
      android.permission.INTERNET: granted=true
    User 0:
      runtime permissions:
        android.permission.CAMERA: granted=false, flags=[ USER_SET ]
      enabledComponents:
        com.example.SomeService
    User 11:
      runtime permissions:
        android.permission.CAMERA: granted=true
";

        let permissions = parse_permissions(output);
        assert_eq!(permissions.len(), 2);

        let internet = permissions
            .iter()
            .find(|permission| permission.name == "android.permission.INTERNET")
            .unwrap();
        assert_eq!(internet.granted, Some(true));
        assert!(!internet.runtime);

        let camera = permissions
            .iter()
            .find(|permission| permission.name == "android.permission.CAMERA")
            .unwrap();
        assert_eq!(camera.granted, Some(false));
        assert!(camera.runtime);

        assert!(!permissions
            .iter()
            .any(|permission| permission.name.contains("SomeService")));
    }

    #[test]
    fn matches_only_exact_package_names() {
        assert!(contains_package("Alarm{1 com.example}", "com.example"));
        assert!(contains_package("JOB #1: com.example/.Job", "com.example"));
        assert!(contains_package("com.example:remote", "com.example"));
        assert!(!contains_package(
            "JOB #1: com.example.other/.Job",
            "com.example"
        ));
        assert!(!contains_package("com.example2/.Job", "com.example"));
    }
}
