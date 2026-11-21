mod adb;
mod app_control;
mod collectors;
mod filesystem;
mod models;
mod monitor;

use std::sync::Arc;

use tauri::{AppHandle, State};

use adb::AdbClient;
use app_control::LogcatState;
use models::{
    AppDetails, AppEntry, DeviceEntry, DeviceInfo, DirectoryListing, ImagePreview, ShellOutput,
    StatusInfo,
};

struct AppState {
    adb: Arc<AdbClient>,
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
fn disconnect_device(state: State<'_, AppState>, logs: State<'_, LogcatState>) {
    app_control::stop_logs(&logs);
    state.adb.disconnect();
}

#[tauri::command]
fn start_monitoring(app: AppHandle, state: State<'_, AppState>) {
    monitor::start(app, Arc::clone(&state.adb));
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
        .manage(AppState { adb })
        .manage(LogcatState::default())
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
            get_status,
            run_shell_command,
            list_directory,
            read_image_preview
        ])
        .run(tauri::generate_context!())
        .expect("error while running MDL");
}
