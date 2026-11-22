mod adb;
mod app_control;
mod collectors;
mod filesystem;
mod inspectors;
mod logcat;
mod models;
mod monitor;
mod sessions;

use std::path::PathBuf;
use std::sync::Arc;

use tauri::{AppHandle, Manager, State};

use adb::AdbClient;
use app_control::LogcatState;
use logcat::DeviceLogState;
use models::{
    ActivityState, AppDetails, AppEntry, AppUsageEntry, DeviceEntry, DeviceInfo, DirectoryListing,
    ExportResult, ImagePreview, NotificationEntry, PowerReport, SensorSnapshot, SessionRecord,
    SessionSummary, ShellOutput, StatusInfo,
};
use sessions::SessionRecorder;

struct AppState {
    adb: Arc<AdbClient>,
    recorder: Arc<SessionRecorder>,
}

fn data_dir(app: &AppHandle) -> Result<PathBuf, String> {
    let path = app
        .path()
        .app_data_dir()
        .map_err(|error| format!("Unable to resolve app data directory: {error}"))?;
    std::fs::create_dir_all(&path)
        .map_err(|error| format!("Unable to create app data directory: {error}"))?;
    Ok(path)
}

#[tauri::command]
fn list_devices(state: State<'_, AppState>) -> Vec<DeviceEntry> {
    state.adb.detect_devices()
}

#[tauri::command]
fn connect_device(serial: String, state: State<'_, AppState>) -> Result<DeviceInfo, String> {
    state.adb.connect(&serial)
}

#[tauri::command]
fn disconnect_device(
    app: AppHandle,
    state: State<'_, AppState>,
    logs: State<'_, LogcatState>,
    device_logs: State<'_, DeviceLogState>,
) {
    app_control::stop_logs(&logs);
    logcat::stop(&device_logs);
    if state.recorder.status().is_some() {
        if let Ok(directory) = data_dir(&app) {
            let _ = state.recorder.stop(&directory);
        }
    }
    state.adb.disconnect();
}

#[tauri::command]
fn start_monitoring(app: AppHandle, state: State<'_, AppState>) {
    monitor::start(app, Arc::clone(&state.adb), Arc::clone(&state.recorder));
}

#[tauri::command]
fn stop_monitoring(state: State<'_, AppState>) {
    state.adb.set_monitoring(false);
}

#[tauri::command]
fn get_device_info(state: State<'_, AppState>) -> Result<DeviceInfo, String> {
    collectors::device::collect(&state.adb)
}

#[tauri::command]
fn get_apps(state: State<'_, AppState>) -> Result<Vec<AppEntry>, String> {
    collectors::apps::collect(&state.adb)
}

#[tauri::command]
async fn launch_app(package: String, state: State<'_, AppState>) -> Result<String, String> {
    let adb = Arc::clone(&state.adb);
    tauri::async_runtime::spawn_blocking(move || app_control::launch(&adb, &package))
        .await
        .map_err(|error| error.to_string())?
}

#[tauri::command]
async fn stop_app(package: String, state: State<'_, AppState>) -> Result<String, String> {
    let adb = Arc::clone(&state.adb);
    tauri::async_runtime::spawn_blocking(move || app_control::stop(&adb, &package))
        .await
        .map_err(|error| error.to_string())?
}

#[tauri::command]
async fn get_app_details(
    package: String,
    state: State<'_, AppState>,
) -> Result<AppDetails, String> {
    let adb = Arc::clone(&state.adb);
    tauri::async_runtime::spawn_blocking(move || app_control::details(&adb, &package))
        .await
        .map_err(|error| error.to_string())?
}

#[tauri::command]
fn start_app_logs(
    app: AppHandle,
    package: String,
    session: u64,
    state: State<'_, AppState>,
    logs: State<'_, LogcatState>,
) -> Result<(), String> {
    app_control::start_logs(app, &state.adb, &logs, &package, session)
}

#[tauri::command]
fn stop_app_logs(logs: State<'_, LogcatState>) {
    app_control::stop_logs(&logs);
}

#[tauri::command]
fn start_device_logs(
    app: AppHandle,
    session: u64,
    buffer: String,
    level: String,
    tag: String,
    state: State<'_, AppState>,
    logs: State<'_, DeviceLogState>,
) -> Result<(), String> {
    logcat::start(app, &state.adb, &logs, session, &buffer, &level, &tag)
}

#[tauri::command]
fn stop_device_logs(logs: State<'_, DeviceLogState>) {
    logcat::stop(&logs);
}

#[tauri::command]
fn start_session(
    app: AppHandle,
    name: Option<String>,
    state: State<'_, AppState>,
) -> Result<SessionSummary, String> {
    if state.adb.serial().is_none() {
        return Err("No device connected".to_string());
    }
    let summary = state.recorder.start(name)?;
    if !state.adb.monitoring() {
        monitor::start(app, Arc::clone(&state.adb), Arc::clone(&state.recorder));
    }
    Ok(summary)
}

#[tauri::command]
async fn stop_session(
    app: AppHandle,
    state: State<'_, AppState>,
) -> Result<SessionSummary, String> {
    let directory = data_dir(&app)?;
    let recorder = Arc::clone(&state.recorder);
    tauri::async_runtime::spawn_blocking(move || recorder.stop(&directory))
        .await
        .map_err(|error| error.to_string())?
}

#[tauri::command]
fn get_session_status(state: State<'_, AppState>) -> Option<SessionSummary> {
    state.recorder.status()
}

#[tauri::command]
async fn list_sessions(app: AppHandle) -> Result<Vec<SessionSummary>, String> {
    let directory = data_dir(&app)?;
    tauri::async_runtime::spawn_blocking(move || SessionRecorder::list(&directory))
        .await
        .map_err(|error| error.to_string())
}

#[tauri::command]
async fn get_session(app: AppHandle, id: String) -> Result<SessionRecord, String> {
    let directory = data_dir(&app)?;
    tauri::async_runtime::spawn_blocking(move || SessionRecorder::load(&directory, &id))
        .await
        .map_err(|error| error.to_string())?
}

#[tauri::command]
async fn export_session(
    app: AppHandle,
    id: String,
    format: String,
) -> Result<ExportResult, String> {
    let directory = data_dir(&app)?;
    tauri::async_runtime::spawn_blocking(move || SessionRecorder::export(&directory, &id, &format))
        .await
        .map_err(|error| error.to_string())?
}

#[tauri::command]
async fn get_notifications(state: State<'_, AppState>) -> Result<Vec<NotificationEntry>, String> {
    let adb = Arc::clone(&state.adb);
    tauri::async_runtime::spawn_blocking(move || inspectors::notifications(&adb))
        .await
        .map_err(|error| error.to_string())?
}

#[tauri::command]
async fn get_activity_state(state: State<'_, AppState>) -> Result<ActivityState, String> {
    let adb = Arc::clone(&state.adb);
    tauri::async_runtime::spawn_blocking(move || inspectors::activity(&adb))
        .await
        .map_err(|error| error.to_string())?
}

#[tauri::command]
async fn get_power_report(state: State<'_, AppState>) -> Result<PowerReport, String> {
    let adb = Arc::clone(&state.adb);
    tauri::async_runtime::spawn_blocking(move || inspectors::power(&adb))
        .await
        .map_err(|error| error.to_string())?
}

#[tauri::command]
async fn get_app_usage(state: State<'_, AppState>) -> Result<Vec<AppUsageEntry>, String> {
    let adb = Arc::clone(&state.adb);
    tauri::async_runtime::spawn_blocking(move || inspectors::app_usage(&adb))
        .await
        .map_err(|error| error.to_string())?
}

#[tauri::command]
async fn get_sensor_snapshot(state: State<'_, AppState>) -> Result<SensorSnapshot, String> {
    let adb = Arc::clone(&state.adb);
    tauri::async_runtime::spawn_blocking(move || inspectors::sensors(&adb))
        .await
        .map_err(|error| error.to_string())?
}

#[tauri::command]
fn get_status(state: State<'_, AppState>) -> StatusInfo {
    StatusInfo {
        serial: state.adb.serial(),
        monitoring: state.adb.monitoring(),
    }
}

#[tauri::command]
async fn run_shell_command(
    command: String,
    state: State<'_, AppState>,
) -> Result<ShellOutput, String> {
    let command = command.trim().to_string();
    if command.is_empty() {
        return Err("Enter a command".to_string());
    }

    let adb = Arc::clone(&state.adb);
    tauri::async_runtime::spawn_blocking(move || adb.shell(&command))
        .await
        .map_err(|error| error.to_string())?
}

#[tauri::command]
async fn list_directory(
    path: String,
    state: State<'_, AppState>,
) -> Result<DirectoryListing, String> {
    let adb = Arc::clone(&state.adb);
    tauri::async_runtime::spawn_blocking(move || filesystem::list(&adb, &path))
        .await
        .map_err(|error| error.to_string())?
}

#[tauri::command]
async fn read_image_preview(
    path: String,
    state: State<'_, AppState>,
) -> Result<ImagePreview, String> {
    let adb = Arc::clone(&state.adb);
    tauri::async_runtime::spawn_blocking(move || filesystem::image_preview(&adb, &path))
        .await
        .map_err(|error| error.to_string())?
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    let adb = Arc::new(AdbClient::new());

    tauri::Builder::default()
        .manage(AppState {
            adb,
            recorder: Arc::new(SessionRecorder::default()),
        })
        .manage(LogcatState::default())
        .manage(DeviceLogState::default())
        .invoke_handler(tauri::generate_handler![
            list_devices,
            connect_device,
            disconnect_device,
            start_monitoring,
            stop_monitoring,
            get_device_info,
            get_apps,
            launch_app,
            stop_app,
            get_app_details,
            start_app_logs,
            stop_app_logs,
            start_device_logs,
            stop_device_logs,
            start_session,
            stop_session,
            get_session_status,
            list_sessions,
            get_session,
            export_session,
            get_notifications,
            get_activity_state,
            get_power_report,
            get_app_usage,
            get_sensor_snapshot,
            get_status,
            run_shell_command,
            list_directory,
            read_image_preview
        ])
        .run(tauri::generate_context!())
        .expect("error while running MDL");
}
