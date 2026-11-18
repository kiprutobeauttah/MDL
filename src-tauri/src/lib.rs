mod adb;
mod collectors;
mod models;
mod monitor;

use std::sync::Arc;

use tauri::{AppHandle, State};

use adb::AdbClient;
use models::{AppEntry, DeviceEntry, DeviceInfo, StatusInfo};

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
fn disconnect_device(state: State<'_, AppState>) {
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
fn get_status(state: State<'_, AppState>) -> StatusInfo {
    StatusInfo {
        serial: state.adb.serial(),
        monitoring: state.adb.monitoring(),
    }
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    let adb = Arc::new(AdbClient::new());

    tauri::Builder::default()
        .manage(AppState { adb })
        .invoke_handler(tauri::generate_handler![
            list_devices,
            connect_device,
            disconnect_device,
            start_monitoring,
            stop_monitoring,
            get_device_info,
            get_apps,
            get_status
        ])
        .run(tauri::generate_context!())
        .expect("error while running MDL");
}
